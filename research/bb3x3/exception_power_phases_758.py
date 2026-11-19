"""Check the actual blank exclusions for short reset-to-E words after the third pair."""
from check_bb33 import first_return
from exception_terminals_758 import before_exception
from power_gates_758 import coarse_return, coalesce, gate_exits

P = 3**33
B = 5_494_990_037_991_759
MIDDLE = 15_799_435_294_420_882

# Six fields from the generic C++ checker. Each extra window begins on the
# specified leg's main grid and ends at the cut used below.
SIDE_WINDOWS = {
    "power33": (5_494_040_377_744_705, B-100_000, 5_494_990_037_891_878,
                5_494_990_037_891_878, 61_658, 216_700_462),
    "power34": (15_798_121_133_201_395, MIDDLE-10_000, MIDDLE-10_000,
                MIDDLE-9_916, 1, 0),
}


def power_phase():
    seed, edges = coalesce(range(B-100_000, B-95_000+1), 7_525)
    assert (seed, edges) == (5_494_990_037_941_749, 7_525)
    for _ in range(381):
        assert seed < B
        seed = first_return(seed, batch=False)
    assert seed == B+103
    gains = {}
    for r in range(64):
        s = B+(r-B)%64
        gains[r] = coarse_return(33, s, 1)-s
        assert gains[r]%2 == 1
    # Extend the gate's common two words down to the cut where we enter.
    for parity in (0, 1):
        assert coarse_return(33, B+(parity-B)%2, 1) > B
    odd = seed+gains[seed%64]
    assert odd == B+190
    boundary = P-70

    def pair(s):
        even = s+gains[s%64]
        return even+gains[even%64]

    q = pair(pair(odd))
    assert q == odd+320 and q%64 == odd%64
    # The simple odd word holds through boundary. Every even member of a
    # pair starting at or below it is in the simple even corridor.
    assert gate_exits(33, 1) and max(gains[r] for r in range(1,64,2)) <= 73
    repeats = (boundary-odd)//320
    odd += 320*repeats
    while odd <= boundary:
        previous = odd
        odd = pair(odd)
    assert (previous-P, previous+gains[previous%64]-P, odd-P) == (-216, -145, -54)
    for _ in range(379):
        odd = first_return(odd, batch=False)
    assert odd == P+87_239


def middle_crossing():
    exits = {}
    for start in range(MIDDLE-10_000, MIDDLE-4_999):
        s = start
        history = []
        while s <= MIDDLE+2 and s not in exits:
            assert s not in (MIDDLE, MIDDLE+2)
            history.append(s)
            following = first_return(s, batch=False)
            assert following is not None and following > s
            s = following
        out = (history[-1], s) if s > MIDDLE+2 else exits[s]
        for seed in history:
            exits[seed] = out
    assert {(x-MIDDLE,y-MIDDLE) for x,y in exits.values()} == {
        (-74,6), (-58,22), (-42,38), (-26,54), (-10,70),
    }
    assert min(gate_exits(34, 1)) == 3**34-40


def verify_candidates():
    low = 3_706_040_377_703_662
    high = 18_378_934_934_402_308
    families = []
    before_exception(high, matching_ranges=families)
    in_range = sorted((max(a,low),b) for a,b in families if low <= b <= high)
    assert in_range == [(P-68, P-68), (MIDDLE, MIDDLE+2), (3**34-70, 3**34-70)]
    return in_range


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable verification.")
    power_phase()
    middle_crossing()
    print("Excluded the following three reset-to-E families:", verify_candidates())
