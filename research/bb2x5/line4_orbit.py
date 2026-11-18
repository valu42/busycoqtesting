"""Time the exact line-4 blank orbit using the local rules in line4_cert."""
from functools import lru_cache
from hashlib import sha256

@lru_cache(maxsize=512)
def three_power(n):
    return 3**n


def complete_rounds(b):
    # 3^n <= (b+n+8)/8. Bracket and binary search the monotone threshold.
    lo, hi = 0, b.bit_length()
    while lo < hi:
        mid = (lo + hi + 1)//2
        if 8*(three_power(mid)-1)-mid <= b:
            lo = mid
        else:
            hi = mid-1
    return lo


def a_epoch(b):
    """From A(6,b) until B or halt, processing any complete A-to-A rounds."""
    rounds = complete_rounds(b)
    power = three_power(rounds)
    a = 8*power - 2
    b -= 8*(power-1) - rounds
    steps = 48*(power*power-1) - 16*(power-1) + 3*rounds
    pairs = min(a,b//2)
    steps += 6*pairs*pairs + 14*pairs
    a -= pairs
    b -= 2*pairs
    k = 3+3*pairs
    if a == 0:
        if b == 2:
            return ('B', k+1, 2), steps + 2*k+12
        if b == 1:
            return None, steps + 2*k+5
        assert b == 0
        return ('B', k-2, 7), steps + 2*k+60
    if b == 1:
        return ('B', a-1, k+2), steps + 4*k+7
    assert b == 0
    if a == 1:
        return ('B', k+1, 5), steps + 6*k+46
    return ('B', a-2, k+4), steps + 8*k+22


def b_epoch(a,b):
    q, r = divmod(a,3)
    steps = q*(42*q + 12*b + 14)
    k = b+7*q
    if r == 1:
        return ('B', k+1, 7), steps+6*k+76
    if r == 2:
        return ('B', k+4, 5), steps+10*k+74
    if k >= 4:
        return ('A', 6, k-4), steps+3*k+57
    target,cost = [(('B',0,4),33),(('B',3,7),107),(None,55),(('B',6,2),65)][k]
    return target,steps+cost


def blank_returns(count):
    """Yield actual A(6,b) entries separated by at least one B-phase state."""
    state = 'B', 2, 7
    steps = 93
    while count:
        tag,a,b = state
        if tag == 'A':
            assert a == 6
            yield b,steps
            count -= 1
            if count == 0:
                return
            state,elapsed = a_epoch(b)
        else:
            state,elapsed = b_epoch(a,b)
        steps += elapsed
        if state is None:
            raise ValueError(f"Reached halt at {steps} defined instructions")


def check_inverse_family():
    for n in range(30):
        power = 3**n
        halt = 24*power-n-11
        assert a_epoch(halt)[0] is None
        before = halt
        j = 1
        while (3**j-1)*(3*n+11)//2 <= 16*power-3:
            start = halt-(3**j-1)*(3*n+11)//2
            (tag,a,b),_ = a_epoch(start)
            assert tag == "B"
            assert b_epoch(a,b)[0] == ("A",6,before)
            before = start
            j += 1


def check_excluded_classes():
    # Test the modular arithmetic used by the all-width proof in line4.md.
    excluded = {1:4, 15:6, 22:0, 36:5}
    for n in range(3, 250):
        residue = excluded.get(n%42)
        if residue is None:
            continue
        power = 3**n
        low = 8*power-8-n
        h = 24*power-n-11
        value = h
        while value >= low:
            assert value%7 == residue
            assert value > 8*power-8
            assert 3*value < 56*3*power-19
            if value != h:
                (tag,a,b),_ = a_epoch(value)
                assert tag == "B" and a%3 == 0
                assert b_epoch(a,b)[0] == ("A",6,next_value)
            next_value = value
            value = 3*value-(48*power+n-11)


def fingerprint(x):
    return sha256(x.to_bytes((x.bit_length()+7)//8,"big")).hexdigest()


if __name__ == "__main__":
    from line4_cert import verify
    verify()
    check_inverse_family()
    check_excluded_classes()
    results = list(blank_returns(1024))
    assert results[:3] == [(71,6393),(393,172248),(3081,10139877)]
    for i,(b,steps) in enumerate(results[:3],1):
        print(i,b,steps)
    b,steps = results[-1]
    assert fingerprint(b) == "823aeb9c0850ba39b1dd241c1d224243e4a69241bf547138f10d9e61c562fb6f"
    assert fingerprint(steps) == "f1fef71e717dbd6d460dc8df5382d2cd09a548ec4e582f8935a26255cf1122e6"
    assert steps > 10**1802
    for label,x in [('b',b),('defined steps',steps)]:
        print(f'{label}: {len(str(x))} digits, {x.bit_length()} bits, SHA256 {fingerprint(x)}')
