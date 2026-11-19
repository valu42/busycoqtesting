"""Lower-bound the #758 raw clock from any attained two-counter mass."""
from check_bb33 import HALTING_TARGET, champion_step
from timing_758 import branch_cost


def block_size(target):
    """Multiple of five long enough for a balanced input at this mass scale."""
    limit = (target + 8) // 5
    exponent, numerator, denominator = 0, 1, 1
    while numerator < limit * denominator:
        exponent += 1
        numerator *= 3
        denominator *= 2
    return 5 * ((exponent + 3 + 4) // 5)


def raw_lower_bound(target):
    """Given that a+2*c reaches target from #758 blank, lower-bound raw time."""
    if target < 2:
        raise ValueError("target mass must be at least two")
    size = block_size(target)
    initial_threshold = (target - 2) // 5
    decrement = 9 * size // 5
    blocks = initial_threshold // decrement
    # Sum 3*(initial_threshold - decrement*j)^2 for j from 1 to blocks.
    squares = blocks * (blocks + 1) * (2 * blocks + 1) // 6
    return 3 * (blocks * initial_threshold**2
                - initial_threshold * decrement * blocks * (blocks + 1)
                + decrement**2 * squares)


def check_block(a, c):
    """Literal replay of the balanced-input lemma on one seeded block."""
    start = a + 2*c
    threshold = (start - 2) // 5
    # The time to balance uses only the starting threshold.
    for _ in range(block_size(start)):
        if min(a, c) >= threshold:
            return
        state = champion_step(a, c)
        if state is None:
            return
        a, c = state
    raise AssertionError("unbalanced complete block")


def conditional_target_clock():
    """Clock bounds only if the blank orbit reaches A(1,H)."""
    mass = 2*HALTING_TARGET + 1
    a, c, suffix = 1, HALTING_TARGET, 0
    for call in range(1, 308):
        suffix += branch_cost(a, c)
        state = champion_step(a, c)
        if state is None:
            assert call == 307
            break
        a, c = state
    else:
        raise AssertionError("target did not halt on call 307")
    upper_prefix = 2 + (mass**3 + 45*mass**2 + 585*mass) // 36
    return raw_lower_bound(mass) + suffix, upper_prefix + suffix


def audit():
    for a in range(48):
        for c in range(1, 48):
            if a == 1 or c % 2:
                mass = a + 2*c
                clock = branch_cost(a, c)
                assert 3*min(a, c)**2 <= clock
                assert 3*clock <= mass**2 + 30*mass + 195
                state = champion_step(a, c)
                if state is not None:
                    na, nc = state
                    assert 4 <= na + 2*nc - mass <= 9
                check_block(a, c)
    for base in (10**4, 10**9, 10**15, 10**139):
        for small in (0, 1, 2, 3, 7, 19):
            check_block(small, base + 1)
            check_block(base + small, 1)
        check_block(1, base)

    a, c, raw = 0, 1, 2
    for i in range(1, 100_001):
        raw += branch_cost(a, c)
        a, c = champion_step(a, c)
        if i % 1000 == 0:
            assert raw_lower_bound(a + 2*c) <= raw
    for target in range(2, 12000, 17):
        size = block_size(target)
        count = (target - 2) // (9*size)
        direct = sum(3*((target - 9*size*j - 2)//5)**2
                     for j in range(1, count + 1))
        assert raw_lower_bound(target) == direct


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to keep verification enabled.")
    audit()
    for c in (1_326_438_094_216_160, 2_031_355_966_425_482, 3_335_436_339_933_383):
        target = 2*c + 1
        print(f"A(1,{c}): mass {target}, block {block_size(target)}, "
              f"lower bound {raw_lower_bound(target):,} raw steps")
    low, high = conditional_target_clock()
    assert low > 441*10**411 and high < 220*10**415
    print("If blank reaches A(1,H), the halting time is between "
          "4.41e413 and 2.20e417 raw steps.")
