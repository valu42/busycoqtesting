"""Independently replay a line 18 suffix clock with literal, variable-width strips."""
import argparse
from bisect import bisect_right
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

    def before_exception(passed):
        """Number of parent calls completed before child request passed+1."""
        if passed < calls[start]:
            return bisect_right(calls, passed) - 1
        # Here the requested child lies in the period, so its call count
        # is positive. A zero-output period can never produce an exception.
        repeats, residual = divmod(passed - calls[start], calls[-1] - calls[start])
        index = bisect_right(calls, residual + calls[start], start, len(phases)) - 1
        return repeats * (len(phases) - start) + index

    return after, before_exception


class StripReplay:
    def __init__(self, suffix):
        self.tape = bytearray(map(int, suffix))
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
        # Group up to five 2- or 3-cell tiles. Only the literal trace of
        # the resulting strip determines its emitted calls and costs.
        size = 0
        for _ in range(5):
            i = pos + size
            if i + 1 >= len(self.tape) or self.tape[i] != 3 or self.tape[i+1] not in (1, 2):
                break
            size += 3 if i + 3 < len(self.tape) and self.tape[i+2] == self.tape[i+3] == 3 else 2
        return size

    def batch(self, pos, count):
        """Yield nested requests, consuming the first exceptional A if present."""
        done = 0
        while done < count:
            width = self.width(pos)
            edge = pos + width
            transfer = cycle(tuple(self.tape[pos:edge])) if width else None
            if transfer is None:
                if self.literal(pos, 'B', pos) == 'A':
                    return done
                done += 1
                continue

            prefix, before_exception = transfer
            remaining = count - done
            word, requests, elapsed = prefix(remaining)
            passed = yield self.batch(edge, requests)
            if passed == requests:
                self.tape[pos:edge] = word
                self.steps += elapsed
                return count

            # Locate the suspended parent call. Fast-forward the strip to
            # its start, then inspect the actual A return in physical order.
            low = before_exception(passed)
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


def check(path, first_edge=None):
    if first_edge is not None and first_edge < 1:
        raise ValueError('right-edge threshold must be positive')
    verify()
    target = load(path)
    seed = blank_entry()
    machine = StripReplay(seed['suffix'])
    raw = int(seed['steps_hex'], 16)
    prior_max = None
    for k in range(1, target['record']):
        if first_edge is not None:
            edge = k + 2 + len(machine.tape.rstrip(b'\0'))
            if edge >= first_edge:
                raise ValueError(f'record {k} already reached right edge +{edge}')
            prior_max = edge if prior_max is None else max(prior_max, edge)
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
    if first_edge is not None:
        edge = target['record'] + 2 + len(suffix)
        if edge < first_edge:
            raise ValueError(f'target right edge +{edge} lies below +{first_edge}')
        message = f"First record at or past +{first_edge} has right edge +{edge}."
        if prior_max is not None:
            message += f' Largest earlier right edge was +{prior_max}.'
        print(message)
    print(f"Strip replay matched the full suffix and raw clock at record {target['record']}.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint', type=Path)
    parser.add_argument('--first-edge', type=int, help='also verify the first record at this right edge or beyond')
    args = parser.parse_args()
    check(args.checkpoint, args.first_edge)
