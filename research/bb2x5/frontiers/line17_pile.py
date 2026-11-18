"""Execute line 17 exactly on a normalized register with a compressed pile of 12 pairs."""
from bisect import bisect_right
from dataclasses import dataclass
from itertools import chain
from pathlib import Path
import subprocess

from line17 import ReachesTerminal, native_counts, record

from prior_frontier import HEAD, T17


NODE_LIMIT = 100_000
CALL_LIMIT = 100_000
OUTER_LIMIT = 200_000


class Budget(Exception):
    """Stop at the last completed top-level crossing or raw instruction."""


@dataclass
class Crossing:
    key: tuple
    children: list
    index: int
    steps: int = 0
    calls: int = 0


class Pile:
    """Intern finite tape intervals. Leaves 0–4 store single symbols."""
    def __init__(self):
        self.nodes = [None]*5
        self.length = [1]*5
        # Whether every cell is legal in a data word with the given starting parity.
        self.valid = [(s in (0, 1, 2), s in (2, 3)) for s in range(5)]
        self.carpet = [(s == 0, s == 4) for s in range(5)]
        self.intern = {}
        self.cache = {}

    def join(self, left, right):
        key = left, right
        if key not in self.intern:
            if len(self.nodes) >= NODE_LIMIT:
                raise Budget('node_budget')
            self.intern[key] = len(self.nodes)
            self.nodes.append(key)
            self.length.append(self.length[left] + self.length[right])
            odd = self.length[left] % 2
            self.carpet.append(tuple(self.carpet[left][p] and self.carpet[right][p ^ odd]
                                     for p in (0, 1)))
            self.valid.append(tuple(self.valid[left][p] and self.valid[right][p ^ odd]
                                    for p in (0, 1)))
        return self.intern[key]

    def cross(self, node, from_right, state):
        """Return the interval, exit direction/state, defined steps and any local halt index.

        A parent requests a child's first exit, replaces that child with its
        resulting word and follows the direction of motion. The memo key includes
        the whole incoming word, entry side and state. An explicit stack supports
        piles larger than the interpreter's recursion limit.
        """
        stack = []
        request = node, from_right, state
        while True:
            node, from_right, state = request
            if request in self.cache:
                result = self.cache[request]
            elif self.nodes[node] is None:
                op = T17[state][node]
                result = (node, 0, state, 0, 0) if op is None else (*op, 1, None)
            else:
                children = list(self.nodes[node])
                index = int(from_right)
                stack.append(Crossing(request, children, index))
                request = children[index], from_right, state
                continue

            while stack:
                frame = stack[-1]
                child, direction, state, steps, halt = result
                frame.children[frame.index] = child
                frame.steps += steps
                frame.calls += 1
                if frame.calls > CALL_LIMIT:
                    raise Budget('child_crossing_budget')
                following = frame.index + direction
                if direction and following in (0, 1):
                    frame.index = following
                    request = frame.children[following], direction < 0, state
                    break
                if not direction and frame.index:
                    halt += self.length[frame.children[0]]
                result = self.join(*frame.children), direction, state, frame.steps, halt
                self.cache[frame.key] = result
                stack.pop()
            else:
                return result


EMBEDDED = '13031302'
RESIDUAL = '24044'


def jump_embedded(epochs, register, engine, word_bits, finite_slots):
    """Batch exact normal sweeps of the embedded header, refusing any terminal call."""
    worker = [str(Path(engine).resolve()), str(epochs), str(word_bits), str(finite_slots)]
    run = subprocess.run(worker, input=register, text=True, capture_output=True)
    if run.returncode:
        # These cases require ordinary physical execution from the entry.
        if any(reason in run.stderr for reason in ('overlapping marked bursts', 'slot budget',
                                                   'chunk budget', 'counter limit')):
            return None
        raise ValueError(run.stderr.strip() or 'embedded sweep worker failed')
    counts = native_counts(run.stdout.splitlines(), 4*epochs, len(register)//2)
    try:
        return embedded_tally(epochs, register, counts)
    except ReachesTerminal:
        return None


def embedded_tally(epochs, register, counts):
    # The embedded header issues the same probes and takes eight extra local moves.
    # record() checks all pairs and rejects a nonzero final-cut tally.
    normal = record(epochs, counts, register=register, base_steps=0, base_head=0)
    return normal['steps'] + 8*epochs, normal['register']


def exceptional_sweep(pile_pairs, register, expected_suspended=None, *, engine=None,
                      word_bits=2**28, finite_slots=100_000_000_000, embedded_log=None):
    """Run the full physical sweep from head 0 just left of the original header."""
    return _execute(pile_pairs, register, HEAD, '', expected_suspended, engine,
                    word_bits, finite_slots, embedded_log)


def _execute(pile_pairs, register, header, left_word, expected_suspended, engine,
             word_bits, finite_slots, embedded_log):
    """Head 0 scans blank. The optional residual word ends immediately to its left."""
    if type(pile_pairs) is not int or pile_pairs < 0 or pile_pairs.bit_length()+5 > NODE_LIMIT:
        raise ValueError('invalid pile size or initial representation exceeds the node budget')
    if (not register or len(register)%2 or any(s not in '102' for s in register[::2])
            or any(s not in '23' for s in register[1::2])):
        raise ValueError('expected a nonempty register of data pairs')
    # Expose the pile's rightmost pairs so that a newly formed local header
    # can be identified and verified in full on both sides of the head.
    exposed = min(32, pile_pairs) if engine is not None else 0
    pile_pairs -= exposed
    register = '12'*exposed + register
    pile = Pile()
    chunks, starts = [], []
    power = pile.join(1, 2)
    remaining = pile_pairs
    pile_x = 1 + len(header)
    data_x = pile_x
    while remaining:
        if remaining % 2:
            chunks.append(power)
            starts.append(data_x)
            data_x += pile.length[power]
        remaining //= 2
        if remaining:
            power = pile.join(power, power)
    edge = data_x + len(register) + 1
    tape = {i: int(s) for i, s in enumerate(header, 1) if s != '0'}
    tape.update({i: int(s) for i, s in enumerate(left_word, -len(left_word)) if s != '0'})
    tape.update({data_x+i: int(s) for i, s in enumerate(register+'2') if s != '0'})

    def header_width(head):
        if any(pos <= head for pos in tape):
            return None
        first = head+1
        if first+6 > pile_x or ''.join(str(tape.get(i, 0)) for i in range(first, first+6)) != HEAD:
            return None
        right = max(tape)
        width, unmatched = divmod(right-first-6, 2)
        if unmatched or right < data_x or tape[right] != 2:
            return None
        first += 6
        for pos in chain(range(first, pile_x), range(data_x, right)):
            allowed = (2, 3) if (pos-first)%2 else (0, 1, 2)
            if tape.get(pos, 0) not in allowed:
                return None
        if all(pile.valid[block][(at-first)%2] for block, at in zip(chunks, starts)):
            return width
        return None

    def embedded_entry(head):
        # The entire word must be 24044 (04)^L [A0] 13031302 D 2, blank elsewhere.
        if head < data_x or head < 7 or (head-5)%2 or min(tape) < 0:
            return None
        if ''.join(str(tape.get(i, 0)) for i in range(5)) != RESIDUAL:
            return None
        if any(tape.get(i, 0) != (4 if (i-5)%2 else 0)
               for i in chain(range(5, pile_x), range(data_x, head+1))):
            return None
        if not all(pile.carpet[block][(at-5)%2] for block, at in zip(chunks, starts)):
            return None
        right = max(tape)
        word = ''.join(str(tape.get(i, 0)) for i in range(head+1, right+1))
        if not word.startswith(EMBEDDED) or not word.endswith('2'):
            return None
        data = word[len(EMBEDDED):-1]
        if (not data or len(data)%2 or data[-1]!='2' or any(s not in '102' for s in data[::2])
                or any(s not in '23' for s in data[1::2])):
            return None
        return (head-5)//2, data

    x, state, steps = 0, 0, 0
    first_edge = 0 if left_word else None
    for _ in range(OUTER_LIMIT):
        if pile_x <= x < data_x:
            j = bisect_right(starts, x)-1
            lo = starts[j]
            hi = lo + pile.length[chunks[j]]
            if x not in (lo, hi-1):
                raise ValueError('non-boundary block entry')
            try:
                block, direction, state, n, halt = pile.cross(chunks[j], x == hi-1, state)
            except Budget as stop:
                return str(stop), steps, first_edge, x, None
            chunks[j] = block
            steps += n
            if not direction:
                return 'halt', steps, first_edge, lo+halt, None
            x = lo-1 if direction < 0 else hi
            continue
        if first_edge is None and x == edge:
            if state != 1:
                raise ValueError('unexpected first edge state')
            if expected_suspended is not None:
                suspended = ''.join(str(tape.get(j, 0)) for j in range(data_x, edge))
                if suspended[2*exposed:] != expected_suspended:
                    raise ValueError('literal pile crossing and pulse reconstruction disagree')
            first_edge = steps
        if engine is not None and first_edge is not None and state == 0 and tape.get(x,0) == 0:
            entry = embedded_entry(x)
            if entry is not None:
                count, data = entry
                jump = jump_embedded(count, data, engine, word_bits, finite_slots)
                if jump is None:
                    # A partial batch gives no state update. Keep following this
                    # unchanged physical configuration with the ordinary interpreter.
                    engine = None
                    continue
                elapsed, updated = jump
                end, extra, _, head, width = _execute(count, updated, EMBEDDED, RESIDUAL,
                                                      None, None, word_bits, finite_slots, None)
                if embedded_log is not None:
                    embedded_log.update(sweeps=count, width=len(data)//2,
                                        entry_delay=steps-first_edge, sweep_steps=elapsed,
                                        tail_steps=extra)
                return end, steps+elapsed+extra, first_edge, 5+head, width
        if first_edge is not None and state == 0 and x <= 0:
            width = header_width(x)
            if width is not None:
                return 'header', steps, first_edge, x, width
        op = T17[state][tape.get(x, 0)]
        if op is None:
            return 'halt', steps, first_edge, x, None
        symbol, direction, state = op
        if symbol:
            tape[x] = symbol
        else:
            tape.pop(x, None)
        x += direction
        steps += 1
    return 'outer_visit_budget', steps, first_edge, x, None
