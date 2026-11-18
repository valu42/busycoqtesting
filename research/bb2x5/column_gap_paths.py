"""Line 26. Exact residue paths between records and literal checks of two altered inputs."""
from fractions import Fraction
from pathlib import Path
from itertools import product, repeat

from column_tick import column, finish
from column_raw_time import PAIRS
from prior_frontier import M26, parse

HERE = Path(__file__).resolve().parent
BLOCKS = ((0,), (3, 2), (0, 2), (3,))


def transfer(word, gap):
    carry = (gap, True)
    out = []
    for digit in word:
        carry, digit = column(carry, digit)
        out.append(digit)
    return tuple(out), *carry


def residue_paths(word):
    """Each leaf terminates on the first Q to pass this entire block."""
    exponent = 1 + sum(d % 2 for d in word[:-1])
    ones = sum(d % 2 for d in word)
    for residue in range(1 << exponent):
        updated, sent, passed = transfer(word, residue)
        tag = (exponent, residue, 1 << (exponent - ones))
        if passed:
            yield (tag,), sent
        else:
            for path, remaining in residue_paths(updated):
                yield (tag, *path), sent + remaining


def classify():
    expected = {(2,): (3,2,1), (0,): (3,2,2), (3,2): (11,3,1),
                (0,2): (12,4,2), (3,): (2,1,0)}
    maxima = {}
    for word, (count, horizon, cap) in expected.items():
        paths = list(residue_paths(word))
        assert (len(paths), max(len(path) for path, _ in paths),
                max(rest for _, rest in paths)) == (count, horizon, cap)
        # Cross-check the symbolic affine formula against full, unrounded gaps.
        for path, remainder in paths:
            for quotients in product((0, 1, 3), repeat=len(path)):
                state = word
                total = 0
                for i, ((exponent, residue, weight), quotient) in enumerate(zip(path, quotients)):
                    state, output, passed = transfer(state, (quotient << exponent) + residue)
                    assert bool(passed) == (i+1 == len(path))
                    total += output
                assert total == remainder + sum(q*t[2] for q,t in zip(quotients,path))
        maxima[word] = cap
    return maxima


def emitted_gaps(state, incoming):
    pending = 0
    for gap in incoming:
        state, sent, passed = transfer(state, gap)
        pending += sent
        if passed:
            yield pending
            pending = 0


def rooted_terms():
    # After tick 1 the source at cut 3 still supplies nine P per Q.
    incoming = repeat(9)
    state = (2,)
    while True:
        complete = gap = 0
        for lower in incoming:
            exponent = 1 + sum(d%2 for d in state[:-1])
            ones = sum(d%2 for d in state)
            complete += (lower >> exponent) << (exponent-ones)
            state, sent, passed = transfer(state, lower)
            gap += sent
            if passed:
                break
        yield gap, complete
        incoming = emitted_gaps(state, incoming)
        state = BLOCKS[gap%4]


def check_records(maxima):
    text = (HERE/'column-records.txt').read_text()
    rows = [tuple(map(int,line.split())) for line in text.splitlines() if not line.startswith('#')]
    state = (2,)
    total = 0
    averages = []
    for n, (_, _, gap, _, _) in enumerate(rows, 1):
        total += max(0, gap-maxima[state])
        averages.append(Fraction(total,n))
        state = BLOCKS[gap%4]
    assert (len(rows),total,min(averages[3:])) == (63,632,Fraction(37,5))
    source = rooted_terms()
    initial = [next(source) for _ in range(12)]
    assert [g for g,_ in initial] == [row[2] for row in rows[:12]]
    assert [v for _,v in initial[:3]] == [12,2,6]
    assert min(averages) == Fraction(19,3)
    print(f'{len(rows)} record transitions: at least {total} safe tokens in complete cycles; '
          f'exact least prefix average 20/3.')


def witness(changes, rejoin, expected_tick):
    # At tick 1 both altered inputs exactly match the physical blank seed.
    word = (2,1)
    for tick in range(2,expected_tick+1):
        digits, safe, danger = transfer(word,9+changes.get(tick,0))
        tail = finish((safe,danger))
        if tail is None:
            assert tick == expected_tick
            break
        word = digits+tail
        if tick == rejoin:
            saved = word
    else:
        raise AssertionError('missing failure')

    # Independently start the actual ten-entry machine at the stated rejoin tape.
    table = parse(M26)
    head = -8*rejoin-1
    cells = '4'*(-head) + ''.join(PAIRS[d] for d in (0,0,0,*saved)) + '3'
    tape = {head+i: int(symbol) for i,symbol in enumerate(cells,1)}
    state = steps = 0
    completed = rejoin
    while True:
        symbol = tape.get(head,0)
        move = table[state][symbol]
        if move is None:
            assert (state,symbol,completed+1)==(1,3,expected_tick)
            break
        new, sign, state = move
        if new:
            tape[head] = new
        else:
            tape.pop(head,None)
        head += sign
        steps += 1
        assert steps < 12_000_000
        if head == -8*(completed+1)-1:
            assert state == 0
            completed += 1
    data = ''.join(map(str,saved))
    print(f'Rejoin tick {rejoin}, upper word {data}: B3 at {head} on tick {expected_tick}, '
          f'{steps} defined instructions from rejoin.')
    return data,head,steps


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Enable assertions.')
    check_records(classify())
    blank = (2,1)
    for tick in range(2,19):
        state, sent, passed = transfer(blank,9)
        blank = state+finish((sent,passed))
        if tick in (15,18):
            assert len(blank)+3 == {15:21,18:24}[tick]
    assert witness({6:1,7:-1,10:1,11:-1,14:1,15:-1},15,41)==('223233233210',35,287750)
    assert witness({6:1,9:1,18:1},18,224)==('301203111200',43,9638408)
    assert witness({4:4,6:4,7:4,34:4},34,55)==('11112331322012',37,365400)
