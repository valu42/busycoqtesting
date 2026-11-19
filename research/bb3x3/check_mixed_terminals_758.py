"""Independently check the fifth candidate pair and the direct-terminal survey."""
import argparse
from pathlib import Path

from check_bb33 import HALTING_TARGET, champion_step, first_return
from check_confluence import itinerary
from terminal_forest_758 import exhaust, terminal


K = 40_486_323_621_582_648


def check_fifth():
    target = terminal(K, 69)
    assert terminal(K+2, 69) == target == (26_990_882_414_388_552, 26_990_882_414_388_551)
    assert exhaust(target, 585) == ({K: 68, K+2: 68}, 585, 92)
    hits = {}
    max_gain = 0
    for seed in range(K+2, K-10_001, -1):
        out = first_return(seed, batch=False)
        if out is None or hits.get(out, False):
            hits[seed] = True
        if out is not None:
            assert out > seed
            max_gain = max(max_gain, out-seed)
    assert sorted(s-K for s in hits) == [-73, -71, 0, 2]
    assert max_gain == 362
    assert all(first_return(K-d, batch=False) == K+2 for d in (71, 73))
    assert (2*(10**11-74+2)+8)//9 == 22_222_222_207
    lower = 39_752_584_607_270_532
    cut = K-10**14
    assert itinerary(lower) == itinerary(cut+5000) == ('J'*34+'LLLLJLR', 198)
    assert itinerary(lower+1) == itinerary(cut+4999) == ('J'*33+'LR', 150)
    assert itinerary(lower-2)[0] != itinerary(lower)[0]
    assert cut+5000-lower+1 == 633_739_014_317_117
    assert (2*(cut+5000-lower+2)+8)//9 == 140_830_892_070_471
    print("The fifth candidate's terminal has exactly two last resets.")


def check_fifth_shape():
    word = 'PPJJPPPPJPPPPPJPPP'
    a, den, low, high = 2, 9, -17, -10
    for op in reversed(word):
        if op == 'J':
            a, den, low, high = a+den, 3*den, low+2*a-den, high+2*a-den
        else:
            a, den, low, high = 4*a, 9*den, 4*low+36*a-35*den, 4*high+20*a-20*den
    launch_den = den-2*a
    assert (den,launch_den,low,high) == (16_677_181_699_666_569, 13_739_374_908_094_985,
                                         -70_279_322_567_176_159, -40_889_613_571_793_860)
    # itinerary omits the first update, J for an odd seed and I for an even one.
    tail = word.replace('P', 'LL')+'LH'
    hits = []
    for m in range(293):
        for even in (0, 1):
            h = (1+even)*3**m
            first = max(h,-((-h*den-2*low)//launch_den))
            last = min(3*h-3,(h*den+2*high)//launch_den)
            for t in range(first+(h-first)%2,last+1,2):
                seed = t-2*m-4*even
                if seed < 3:
                    continue
                if itinerary(seed)[0] == 'J'*(m-1+even)+tail and first_return(seed) is None:
                    hits.append(seed)
    assert hits == [K, K+2]
    assert 3**293-2*293 > HALTING_TARGET


def incoming_window(k):
    """Number halting, number of distinct edges, distinct overshoots among 5001 seeds."""
    cache = {}
    reached = set()
    halting = 0
    for start in range(k-199_000, k-194_000+1):
        seed = start
        path = []
        while seed is not None and seed <= k+2 and seed not in cache:
            path.append(seed)
            nxt = first_return(seed)
            assert nxt is None or nxt > seed
            seed = nxt
        outcome = cache.get(seed, seed)
        for item in path:
            cache[item] = outcome
        if outcome is None:
            halting += 1
        else:
            reached.add(outcome-k)
    return halting, len(cache), tuple(sorted(reached))


def check_earlier_walls():
    cases = (
        (4_581_767_045_681_768_136, 3602, 9, 2, 66, 66, 70),
        (12_966_580_636_926_693_791_014_052, 25997, 53, 2, 6, 50, 620),
        (67031973341757228314446197656042783060587885387371250178974638183578180826471990549767534077392348,
         170405, 64, 0, 712, 143, 1057),
    )
    for k, distance, width, target, left_exit, right_exit, edges in cases:
        known = {}
        ends = []
        for start in range(k-distance-1, k-distance+width+1):
            s = start
            path = []
            while s <= k+2 and s not in known:
                path.append(s)
                nxt = first_return(s)
                if nxt is None:
                    assert s in (k, k+2)
                    outcome = ('halt', s-k)
                    break
                assert nxt > s
                s = nxt
            else:
                outcome = known.get(s, ('exit', s-k))
            for previous in path:
                known[previous] = outcome
            ends.append(outcome)
        assert ends == [('exit',left_exit)] + [('halt',target)]*width + [('exit',right_exit)]
        assert len(known) == edges


def check_exception_rows(path):
    seeds = set()
    for line in path.read_text().splitlines():
        seed, m, even, blocks, left, right = map(int, line.split())
        assert seed not in seeds and seed%2 == 1-even
        seeds.add(seed)
        assert left == right+2 and right%4 == 3
        state = (1, seed)
        for _ in range(even+m+2*blocks+1):
            if state == (left, right):
                break
            state = champion_step(*state)
            assert state is not None and state[0] != 1
        else:
            raise AssertionError("predicted exceptional input was never reached")
        assert first_return(seed, batch=False) is not None
    print(f"Checked {len(seeds)} exceptional seeds against the elementary transition.")


def check_survey():
    halting_counts = []
    previous = 0
    with Path(__file__).with_name("mixed_terminal_windows_758.tsv").open() as stream:
        assert stream.readline().split() == ["seed", "halting", "edges", "exits", "offsets"]
        for line in stream:
            k, halting, edges, exits, *offsets = map(int, line.split())
            assert previous < k and first_return(k) is None and first_return(k+2) is None
            previous = k
            assert exits == len(offsets) and incoming_window(k) == (halting, edges, tuple(offsets))
            halting_counts.append((k, halting))
    assert len(halting_counts) == 257
    assert sorted(count for _, count in halting_counts if count) == [120, 150, 875, 951]
    assert (HALTING_TARGET-2, 951) in halting_counts
    print("Checked all 257 candidate pairs and their 5,001 incoming resets each.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable checks.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--survey", action="store_true", help="also replay all listed incoming windows")
    parser.add_argument("--exceptions", type=Path, help="replay the rows from a --exception search")
    args = parser.parse_args()
    check_fifth()
    check_fifth_shape()
    check_earlier_walls()
    assert incoming_window(K) == (0, 6_704, (118,))
    if args.exceptions:
        check_exception_rows(args.exceptions)
    if args.survey:
        check_survey()
