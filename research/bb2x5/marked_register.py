"""Line 17, finite blank-orbit certificate. Run with plain python3 and assertions on."""
from array import array
from itertools import product

from prior_frontier import (
    DATA, LIST, M17, blank17, check_second_marks, digits, marks_on_word, periodic_marks,
)


def output_length(state, prefix, period, slots):
    """Exact output length on an ultimately periodic input, skipping full state cycles."""
    initial = prefix[:slots]
    state, head = marks_on_word(state, initial)
    count = len(head)
    whole, leftover = divmod(slots - len(initial), len(period))
    seen = {}
    i = 0
    while i < whole and state not in seen:
        seen[state] = (i, count)
        state, word = marks_on_word(state, period)
        count += len(word)
        i += 1
    if i < whole:
        previous, previous_count = seen[state]
        laps, remainder = divmod(whole - i, i - previous)
        count += laps * (count - previous_count)
        for _ in range(remainder):
            state, word = marks_on_word(state, period)
            count += len(word)
    _, tail = marks_on_word(state, period[:leftover])
    return count + len(tail)


def lift_period(period, marks, slots):
    """Pure periodic input to a trit initially (1,0). Return a period and a length bound."""
    coefficient = 0
    children = array('Q')
    for copies in range(1, 4):
        offset = (copies - 1) * period
        for t in marks:
            x = t + offset + coefficient
            r = x % 3
            if r:
                children.append((x + 5*r)//3)
            coefficient += 4*(1 + r)
        if (copies*period + coefficient) % 3 == 0:
            break
    else:
        raise AssertionError('period phase did not return')
    output_period = (copies*period + coefficient)//3
    assert all(1 <= t <= output_period for t in children)
    turns, remainder = divmod(slots, copies*period)
    partial = 0
    for i in range(copies):
        for t in marks:
            t += i*period
            if t > remainder:
                break
            partial += 4*(1 + (t + partial) % 3)
        if remainder <= (i+1)*period:
            break
    bound = (slots + turns*coefficient + partial + 1)//3
    return output_period, children, bound


def finite_event(x, width):
    """Change in the packed coefficient and eventual mark time, or None if extinguished."""
    change = 0
    power = 1
    for _ in range(width):
        r = x % 3
        change += 4*(1+r)*power
        if r == 0:
            return change, None
        x = (x + 5*r)//3
        power *= 3
    return change, x


def infinite_event(x):
    """Return the signed change, depth checked, and whether the common tail survives."""
    assert x >= 0
    change = 0
    power = 1
    depth = 0
    while x != 5:
        r = x % 3
        change += 4*(1+r)*power
        depth += 1
        if r == 0:
            return change, depth, False
        x = (x + 5*r)//3
        power *= 3
    return change - 6*power, depth, True


def finite_cache(width):
    """Low residues with a zero in the first width tests; other residues need a full test."""
    table = []
    for r in range(3**width):
        change, child = finite_event(r, width)
        table.append(change if child is None else None)
    return table


def deep_prefix(period, marks, slots, width):
    """Upper bound for slot count and possible marked positions through width identical digits."""
    cache_width = min(7, width)
    table = finite_cache(cache_width)
    scale = 3**width
    carry = 0
    surviving = []
    max_depth = 0
    event_count = 0
    for offset in range(0, slots, period):
        for t in marks:
            t += offset
            if t > slots:
                break
            x = t + carry
            assert x >= 0
            change = table[x % len(table)]
            if change is None:
                change, depth, passes = infinite_event(x)
                assert depth <= width
                max_depth = max(max_depth, depth)
                if passes:
                    assert change == -2-4*(x//5) and x % 5 == 0
                    surviving.append(5 + 6*len(surviving))
            carry += change
            event_count += 1
    finite_carry = carry + 6*len(surviving)*scale
    bound = (slots + finite_carry + (scale-1)//2)//scale
    max_depth = max(max_depth, cache_width)  # an upper bound also for cached events
    return bound, surviving, (event_count, max_depth, carry)


def literal_audit():
    """Independently check the formulas on short words, including pulses split at the cut."""
    for first in range(1, 5):
        for gaps in product(range(3, 7), repeat=3):
            times = [first]
            for g in gaps:
                times.append(times[-1]+g)
            for width in (1, 2, 4, 6):
                trits = (0, 2, 1, 0, 1, 2)[:width]
                c = sum((v-1)*3**i for i, v in enumerate(trits))
                # Zero completion allows every descendant mark in the finite list to appear.
                word = bytearray(times[-1]+4*3**width)
                for t in times:
                    word[t-1] = 1
                for v in trits:
                    _, word = marks_on_word((v,0), word)
                predicted = []
                for t in times:
                    change, child = finite_event(t+c, width)
                    c += change
                    if child is not None:
                        predicted.append(child)
                assert predicted == [i for i,b in enumerate(word,1) if b]

    for period, marks in [(6,[5]), (7,[1,4]), (10,[4,7]), (28,[3,7,14,23])]:
        block = bytes(int(i in marks) for i in range(1,period+1))
        for n in range(4*period+1):
            p, ts, bound = lift_period(period, marks, n)
            _, actual_prefix = marks_on_word((1,0),(block*5)[:n])
            assert len(actual_prefix) <= bound
            if n == 0:
                _, actual = marks_on_word((1,0),block*20)
                predicted = bytes(int(i in ts) for i in range(1,p+1))
                assert actual == (predicted*(1+len(actual)//p))[:len(actual)]

    # Cross-check the special initial pending input in digit 2. Its trit is zero.
    d = digits(DATA)
    assert [v for v,_ in d[:6]] == [2,1,0,2,0,2]
    c = sum((v-1)*3**i for i,(v,_) in enumerate(d[:6])) + 4*3**2
    assert c+2 == 219
    cycles = 2000
    word = bytes([0,1,0,0])*cycles
    for i in range(6):
        _, word = marks_on_word((d[i][0],d[i-1][1] if i else 0),word)
    predicted = []
    for t in range(2,4*cycles,4):
        change, child = finite_event(t+c,6)
        c += change
        if child is not None and child <= len(word):
            predicted.append(child)
    assert predicted == [i for i,b in enumerate(word,1) if b]
    for x in range(2000):
        change, depth, passes = infinite_event(x)
        y = x//5-1
        ternary_ok = y >= 0
        while y > 0:
            ternary_ok &= y%3 != 2
            y //= 3
        assert passes == (x%5 == 0 and ternary_ok)
        w = depth+3
        fc, child = finite_event(x,w)
        assert (fc,child) == ((change+6*3**w,5) if passes else (change,None))
    print('Independent short-word checks passed.')


def blank_bound():
    assert M17 == LIST[16] == '1RB2RA3LB---2LB_2LA0LA4RB0RB1LA'
    blank17()
    d = digits(DATA)
    check_second_marks(d)
    assert len(d) == 424 and all(pair == (1,0) for pair in d[6:403])
    epochs = 10**18
    slots = 4*epochs
    prefix, cycle = b'', bytes((0,1,0,0))
    for i in range(6):
        state = (d[i][0],d[i-1][1] if i else 0)
        slots = output_length(state,prefix,cycle,slots)
        prefix,cycle = periodic_marks(state,prefix,cycle)
    period = len(cycle)
    marks = [i for i,b in enumerate(cycle,1) if b]
    assert (prefix,period,marks) == (b'',28,[3,7,14,23])
    print(f'cut 6: {slots} slots, period {period}, marked at {marks}')
    for i in range(6,59):
        period, marks, slots = lift_period(period,marks,slots)
    assert (period,len(marks)) == (3146280,393280)
    print(f'cut 59: at most {slots} slots, {len(marks)} marks per period of {period}')
    slots, marked, (events, depth, carry) = deep_prefix(period,marks,slots,403-59)
    assert marked == [5,11,17,23] and slots == 24
    print(f'cut 403: at most {slots} slots; possible marks {marked}')
    print(f'cut-59 marks tested {events}; depth bound {depth}; signed coefficient {carry}')
    word = bytes(int(i in marked) for i in range(1,slots+1))
    lengths = []
    for i in range(403,len(d)):
        _, word = marks_on_word((d[i][0],d[i-1][1]),word)
        lengths.append(len(word))
    assert lengths[:6] == [23,18,13,5,1,0] and not any(lengths[6:])
    print('slot bounds at cuts 404 through 409:', lengths[:6])
    print(f'{epochs} complete header epochs; more than 10^36 defined elementary steps from blank.')


if __name__ == '__main__':
    literal_audit()
    blank_bound()
