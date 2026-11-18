"""Construct free continuations of the first 32 genuine periods at line-17 cut 53."""
from itertools import product
from prior_frontier import DATA, digits, marks_on_word, periodic_marks


def scan_homogeneous(marks):
    """Propagate timed mark events through one digit initially in state (1,0)."""
    result = []
    trit = 1
    last_input = 0
    output_slots = 0
    for when in marks:
        plain = when - last_input - 1
        assert plain >= 0
        output_slots += (trit + plain) // 3
        trit = (trit + plain) % 3
        if trit:
            result.append(output_slots + 2*trit)
        output_slots += 2*trit + 1
        last_input = when + trit
        trit = 2
    return result, last_input, output_slots


def check_extensions():
    # Check the event calculation independently against individual slot transitions.
    for first in range(1,7):
        for gaps in product(range(3,9),repeat=3):
            marks=[first]
            for gap in gaps:
                marks.append(marks[-1]+gap)
            bits=bytearray(marks[-1]+2)
            for when in marks:
                bits[when-1]=1
            _,out=marks_on_word((1,0),bits)
            assert scan_homogeneous(marks)[0]==[i for i,b in enumerate(out,1) if b]
    d = digits(DATA)
    prefix, period = b'', bytes((0,1,0,0))
    for i in range(53):
        prefix, period = periodic_marks((d[i][0], d[i-1][1] if i else 0), prefix, period)
    assert not prefix and len(period)==147740
    one = [i for i,bit in enumerate(period,1) if bit]
    assert one[:6] == [5,11,17,23,27,43]
    known = [t*len(period)+i for t in range(32) for i in one]
    assert len(known)==590976
    a = known
    ends = []
    for _ in range(35):
        a, last, emitted = scan_homogeneous(a)
        ends.append((last,emitted))
    assert a == [5,11,17,23]

    next_mark = 23+6+5*3**314
    for last,emitted in reversed(ends):
        triples = next_mark-emitted-4
        assert triples >= 1
        next_mark = last + 3*triples + 1
    assert next_mark > 32*len(period)
    for target_gap in (6,13,17,56):
        gap = 6+3**349*(3*target_gap-14)
        a = known + [next_mark+j*gap for j in range(120)]
        for _ in range(350):
            a, _, _ = scan_homogeneous(a)
        assert a == [5,11,17,23] + [29+j*target_gap for j in range(120)]
    print('line 17: the first 4727680 genuine slots admit all three chosen edge symbols and a halting continuation')
