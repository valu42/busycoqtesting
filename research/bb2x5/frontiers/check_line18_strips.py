"""Independently replay a line 18 suffix clock with literal, variable-width strips."""
import argparse
from functools import lru_cache
from pathlib import Path

from line18 import blank_entry, load
from line18_header import MACHINE, local_steps, verify
from prior_sweeps import parse

RULES = parse(MACHINE)


@lru_cache(maxsize=16384)
def ordinary(word):
    """Try one B input on a finite strip, supplying B for every child B call."""
    tape = list(word)
    pos, requests, state = 0, 0, 'B'
    for elapsed in range(5000):
        if pos < 0:
            if state == 'B':
                return tuple(tape), requests, elapsed
            break
        if pos == len(word):
            if state != 'B':
                break
            requests += 1
            pos -= 1
        rule = RULES.get((state, tape[pos]))
        if rule is None:
            break
        tape[pos], delta, state = rule
        pos += delta
    return None


@lru_cache(maxsize=16384)
def cycle(word):
    """Trace complete strip states until one recurs. Counts are cumulative."""
    seen, phases, calls, costs = {}, [], [0], [0]
    while word not in seen:
        result = ordinary(word)
        if result is None or len(phases) >= 100:
            return None
        seen[word] = len(phases)
        phases.append(word)
        word, count, elapsed = result
        calls.append(calls[-1] + count)
        costs.append(costs[-1] + elapsed)
    start = seen[word]

    def after(n):
        if n < start:
            return phases[n], calls[n], costs[n]
        repeats, offset = divmod(n - start, len(phases) - start)
        i = start + offset
        return (phases[i], calls[i] + repeats * (calls[-1] - calls[start]),
                costs[i] + repeats * (costs[-1] - costs[start]))

    return after


class StripReplay:
    def __init__(self, suffix):
        self.tape = list(map(int, suffix))
        self.steps = 0

    def literal(self, pos, state, left):
        for _ in range(1_000_000):
            if pos < left:
                return state
            if pos == len(self.tape):
                self.tape.append(0)
            rule = RULES.get((state, self.tape[pos]))
            if rule is None:
                raise ValueError('undefined instruction during strip replay')
            self.tape[pos], delta, state = rule
            self.steps += 1
            pos += delta
        raise ValueError('literal strip replay work limit')

    def width(self, pos):
        # Group up to three 2- or 3-cell tiles. Only the literal trace of
        # the resulting strip determines its emitted calls and costs.
        size = 0
        for _ in range(3):
            i = pos + size
            if self.tape[i:i+1] != [3] or self.tape[i+1:i+2] not in ([1], [2]):
                break
            size += 3 if self.tape[i+2:i+4] == [3, 3] else 2
        return size

    def batch(self, pos, count):
        """Yield nested requests, consuming the first exceptional A if present."""
        done = 0
        while done < count:
            width = self.width(pos)
            edge = pos + width
            prefix = cycle(tuple(self.tape[pos:edge])) if width else None
            if prefix is None:
                if self.literal(pos, 'B', pos) == 'A':
                    return done
                done += 1
                continue

            remaining = count - done
            word, requests, elapsed = prefix(remaining)
            passed = yield self.batch(edge, requests)
            if passed == requests:
                self.tape[pos:edge] = word
                self.steps += elapsed
                return count

            # Locate the suspended parent call. Fast-forward the strip to
            # its start, then inspect the actual A return in physical order.
            low, high = 0, remaining
            while low + 1 < high:
                mid = (low + high) // 2
                if prefix(mid)[1] <= passed:
                    low = mid
                else:
                    high = mid
            word, earlier, elapsed = prefix(low)
            self.tape[pos:edge] = word
            self.steps += elapsed
            done += low
            i, state = pos, 'B'
            while True:
                if i == edge:
                    i -= 1
                    if earlier == passed:
                        break
                    earlier += 1
                    state = 'B'
                self.tape[i], delta, state = RULES[state, self.tape[i]]
                self.steps += 1
                i += delta
            if self.literal(i, 'A', pos) == 'A':
                return done
            done += 1
        return done

    def b_calls(self, n):
        frames = [self.batch(0, n)]
        result = None
        while frames:
            try:
                child = frames[-1].send(result)
            except StopIteration as end:
                result = end.value
                frames.pop()
            else:
                frames.append(child)
                result = None
        return result


def check(path):
    verify()
    target = load(path)
    seed = blank_entry()
    machine = StripReplay(seed['suffix'])
    raw = int(seed['steps_hex'], 16)
    for k in range(1, target['record']):
        if machine.literal(0, 'A', 0) != 'B':
            raise ValueError(f'exceptional A call at record {k}')
        n = 1 << (k - 1)
        if machine.b_calls(n) != n or machine.tape[0] != 3:
            raise ValueError(f'exceptional B return at record {k}')
        del machine.tape[0]
        raw += local_steps(k)
    suffix = ''.join(map(str, machine.tape)).rstrip('0')
    if (suffix, hex(raw + machine.steps)) != (target['suffix'], target['steps_hex']):
        raise ValueError('strip replay disagrees with the saved tape or clock')
    print(f"Strip replay matched the full suffix and raw clock at record {target['record']}.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint', type=Path)
    check(parser.parse_args().checkpoint)
