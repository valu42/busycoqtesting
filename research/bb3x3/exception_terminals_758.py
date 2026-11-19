"""Search both sides of the exceptional #758 rule up through the known wall."""
from check_bb33 import HALTING_TARGET, champion_step
from terminal_forest_758 import exhaust

DEPTH = 17
JUMP, GAP, BULK = 0, 1, 2


def region(a, c):
    if a <= c:
        return JUMP
    if a >= 4*((c+1)//4) + 3:
        return BULK
    return GAP


def move(a, c, branch):
    if branch == BULK:
        q = (c+1)//4
        return a-4*q-3, 6*q+5
    return 3*a+2, c-a+1


def narrow_states(first, last, initial, depth, pattern=()):
    """All narrow guard intervals within depth ordinary calls, in key order.

    Initially a is nondecreasing and c nonincreasing in the key, and a has
    constant parity. Both ordinary updates preserve these properties.
    """
    results = []
    word = []
    offsets = [(bool(pattern), 0)]

    def sample(key):
        a, c = initial(key)
        for branch in word:
            a, c = move(a, c, branch)
        return a, c

    def boundary(i, left, j, right, target):
        # The secant is optional. Every chosen integer is strictly internal,
        # and each branch classification is checked with the exact full word.
        attempts = 0
        while j-i > 1:
            x = (i+j)//2
            low_gap, high_gap = left[0]-left[1], right[0]-right[1]
            if attempts < 3 and high_gap > low_gap:
                centre = 1 if target == GAP else 3
                step = (j-i)*(centre-low_gap)//(high_gap-low_gap)
                x = i+max(1, min(j-i-1, step))
            state = sample(x)
            if region(*state) < target:
                i, left = x, state
            else:
                j, right = x, state
            attempts += 1
        return i, left, j, right

    def piece(i, left, j, right, branch):
        assert left[0]%2 == right[0]%2
        if branch == GAP:
            results.append((i, j, tuple(word), left, right))
            return
        if branch == JUMP and left[0]%2 == 0:
            return  # The entire piece resets.
        matching, tail = offsets[-1]
        # A complete copy of the optional ordinary pattern resets the tail
        # length; the first mismatch fixes the end of the repeated prefix.
        next_match = matching and branch == pattern[tail]
        next_tail = (tail+1) % len(pattern) if next_match else tail+1
        if next_tail > depth:
            return
        if len(word) >= 1_500:
            raise RuntimeError("ordinary path budget exhausted")
        offsets.append((next_match, next_tail))
        word.append(branch)
        visit(i, move(*left, branch), j, move(*right, branch))
        word.pop()
        offsets.pop()

    def visit(i, left, j, right):
        low, high = region(*left), region(*right)
        assert low <= high
        if low == high:
            piece(i, left, j, right, low)
            return
        x, sx, y, sy = boundary(i, left, j, right, low+1)
        piece(i, left, x, sx, low)
        if region(*sy) == high:
            piece(y, sy, j, right, high)
            return
        z, sz, e, se = boundary(y, sy, j, right, high)
        piece(y, sy, z, sz, GAP)
        piece(e, se, j, right, high)

    visit(first, initial(first), last, initial(last))
    return results


def after_exception(limit, depth=DEPTH, pattern=()):
    """Every last E of input mass <= 2H whose post-bulk tail has <= DEPTH calls."""
    q_max = (2*limit-11)//12
    spent, right, count = 0, 1, 0
    hits = compatible = further = 0
    while spent <= 12*q_max+17:
        decrement = 4*((right+1)//4)+3
        next_spent = spent+decrement
        lo = max(0, (spent-17+11)//12)
        hi = min(q_max, (next_spent-18)//12)
        if lo <= hi:
            initial = lambda q: (12*q+17-spent, right)
            for q, q2, word, state, _ in narrow_states(lo, hi, initial, depth, pattern):
                # A unit q increases a by 12 initially, a gap preserved or
                # enlarged by every common word. A narrow gap is at most three.
                assert q == q2
                source = 4*q+5, 4*q+3
                actual = champion_step(*source)
                for _ in range(count+len(word)):
                    assert actual is not None and actual[0] != 1
                    actual = champion_step(*actual)
                assert actual == state
                resets, _, _ = exhaust(source, 200_000)
                if state[0]%2:
                    # A second E before any reset. Check that none of these
                    # first E states has a reset ancestor in the blank domain.
                    assert state[0] == state[1]+2 and state[1]%4 == 3
                    assert not resets
                    further += 1
                    continue
                assert champion_step(*actual) is None
                hits += 1
                if resets:
                    assert source == (53,51) and set(resets) == {71}
                    compatible += 1
        spent, right = next_spent, 6*((right+1)//4)+5
        count += 1
    return hits, compatible, further


def before_exception(limit, depth=DEPTH, pattern=(), *, matching_ranges=None):
    """All reset seeds <= H reaching E within DEPTH calls after the leading J run."""
    families = seeds = halts = largest_post = largest_gain = 0
    first_future = None
    checkpoint = 3_706_040_377_703_662
    for parity in (0, 1):
        m, p = 0, (1 if parity else 2)
        while True:
            lift = 2*m + (0 if parity else 4)
            low, high = max(3, p-lift), min(limit, 3*p-3-lift)
            if low > limit:
                break
            low += (parity-low)%2
            high -= (high-parity)%2
            if low <= high:
                # Larger keys mean smaller reset seeds and smaller right counters.
                initial = lambda k: (2*p-1, parity-2*k+lift-p+1)
                rows = narrow_states((parity-high)//2, (parity-low)//2, initial, depth, pattern)
                for i,j,word,state,other in rows:
                    if state[0]%2 == 0:
                        continue  # A direct halt without E is outside this search.
                    assert state == other and state[0] == state[1]+2 and state[1]%4 == 3
                    left, right = parity-2*j, parity-2*i
                    if matching_ranges is not None:
                        matching_ranges.append((left, right))
                    families += 1
                    seeds += (right-left)//2+1
                    for seed in range(left, right+1, 2):
                        actual = (1,seed) if parity else champion_step(1, seed)
                        for _ in range(m+len(word)):
                            actual = champion_step(*actual)
                            assert actual is not None and actual[0] != 1
                        assert actual == state
                    candidate = max(left, checkpoint+1)
                    candidate += (left-candidate)%2
                    if candidate <= right and (first_future is None or candidate < first_future):
                        first_future = candidate
                    actual = champion_step(*state)
                    for calls in range(1, 5001):
                        if actual is None:
                            assert left == right == 71
                            halts += 1
                            break
                        if actual[0] == 1:
                            largest_post = max(largest_post, calls)
                            largest_gain = max(largest_gain, actual[1]-left)
                            break
                        actual = champion_step(*actual)
                    else:
                        raise RuntimeError("post-exception path not classified")
            m, p = m+1, 3*p
    return families, seeds, halts, largest_post, largest_gain, first_future


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable verification.")
    after = after_exception(HALTING_TARGET)
    assert after == (169, 1, 71)
    print("Halting E launches, count with a reset ancestor, and double-E launches", after, flush=True)
    before = before_exception(HALTING_TARGET)
    assert before == (399, 507, 1, 795, 3376, 5_559_060_566_555_455)
    print("First-E families, seeds, halts, largest call count, largest gain, "
          "and first future seed", before)
    # Also allow arbitrarily many complete PJ or JP coarse blocks near the
    # forward checkpoint. Six more ordinary calls may follow the last copy.
    periodic_after = after_exception(10**18, 6, (JUMP, BULK, BULK))
    periodic_before = before_exception(10**18, 6, (BULK, BULK, JUMP))
    assert periodic_after == (25, 1, 8)
    assert periodic_before == (45, 54, 1, 123, 516, 5_559_060_566_555_455)
    print("Repeated JP and PJ families through 10^18", periodic_after, periodic_before)
