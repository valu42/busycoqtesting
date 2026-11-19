"""Verify a #758 corridor with a single common forward checkpoint.

Place this file beside check_bb33.py and run python3 check_confluence.py.
Only integer arithmetic and the standard library are used.
"""
from check_bb33 import champion_step, first_return

LOW = 1_059_491_543_272_883
HIGH = 1_079_817_520_122_229
CHECKPOINT = 1_079_817_520_208_950


def itinerary(seed):
    """Coarse branch word up to an h-return or halt; bound growth in a+2c."""
    assert seed >= 3
    a, c = champion_step(1, seed)
    mass_gain = (a + 2*c) - (1 + 2*seed)
    word = []
    while True:
        q = (c + 1) // 4
        result = champion_step(a, c)
        if a >= 4*q + 3:
            # Both low-residue branches have this exact successor. The
            # contribution to a+2c is either 5 or 9.
            assert result == (a - 4*q - 3, 6*q + 5)
            letter, cost = 'L', 9
        elif a % 2 == 0:
            if a <= c:
                assert result == (1, a // 2 + c + 2)
                return ''.join(word) + 'R', mass_gain + 5
            assert result is None
            return ''.join(word) + 'H', mass_gain
        elif a <= c:
            assert result == (3*a + 2, c - a + 1)
            letter, cost = 'J', 4
        else:
            assert c % 4 == 3 and a == c + 2 and result == (3*c + 8, 1)
            letter, cost = 'E', 8
        a, c = result
        word.append(letter)
        mass_gain += cost


def verify():
    # For each seed parity the first step has fixed a and increasing c.
    # Common L/J branches preserve a nonincreasing and c nondecreasing with
    # seed. L eligibility decreases; J eligibility increases. R requires even
    # a <= c and therefore persists with increasing seed at this phase. Thus
    # matching endpoint itineraries with no E certify the entire parity class.
    # The argument only uses words ending in R and containing no E here.
    jump = 0
    for parity in (0, 1):
        lo = LOW + (parity - LOW) % 2
        hi = HIGH - (HIGH - parity) % 2
        word, growth = itinerary(lo)
        assert (word, growth) == itinerary(hi) and word.endswith('R') and 'E' not in word
        jump = max(jump, growth // 2)
    assert jump == 82
    # All surviving returns increase c because the mass increases at every
    # step. Every first return costs at most the growth bound through R, even
    # if the orbit has already hit a=1 internally. Hence all starts must exit.
    exits = set()
    for c in range(HIGH - jump + 1, HIGH + 1):
        nxt = first_return(c)
        assert nxt is not None and c < nxt <= c + jump
        if nxt > HIGH:
            exits.add(nxt)
    assert len(exits) == 23
    linked = {CHECKPOINT}
    for c in sorted(exits):
        history = []
        while c not in linked:
            history.append(c)
            nxt = first_return(c)
            assert nxt is not None and c < nxt <= CHECKPOINT
            c = nxt
        linked.update(history)
    assert len(linked)-1 == 1_216
    print(f"{HIGH - LOW + 1:,} seeds, {len(exits)} exits, common checkpoint {CHECKPOINT:,}")

    # Bridge the open interval between the two confluence certificates.
    # Descending induction puts each start into the second interval, since
    # its return either stays in this gap at a larger c, or crosses its top.
    top = 1_080_000_000_000_000
    greatest = 0
    for c in range(HIGH + 1, CHECKPOINT):
        nxt = first_return(c)
        assert nxt is not None and c < nxt <= top
        greatest = max(greatest, nxt)
    assert (CHECKPOINT-HIGH-1, greatest) == (86_720, 1_079_817_520_209_214)
    print(f"All {CHECKPOINT-HIGH-1:,} intervening seeds feed the second interval.")


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    verify()
