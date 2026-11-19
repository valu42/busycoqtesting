"""Identify exact common checkpoints of ordinary cells below the target H at power 292."""
from annular_skip_758 import evaluate, openings, partition, skip_cell
from check_bb33 import HALTING_TARGET, first_return
from power_gates_758 import coalesce
from power35_inner_skip_758 import certify_word

POWER = 3**292
# Depth-eight cells, numbered in increasing seed order, with a local merger.
# (number, number of exits, distinct first-return edges, checkpoint minus exclusive end)
MERGERS = (
    (1,222,7_760,2_834_641), (2,284,8_919,4_819_571), (3,280,14_661,8_328_137),
    (5,273,12_625,7_835_441), (7,218,8_199,3_687_890), (8,282,8_248,2_930_770),
    (9,218,8_715,6_810_540), (10,214,6_376,2_681_696), (11,280,9_249,4_511_571),
)


# Two further cells first traverse an odd-only word and then an even-only word.
# The endpoints are the first excluded seeds of their respective parities.
EXTENDED = {
    4: (
        21108458269789582760414409787128336147519516284411166167310864894236762767305781689402027231472489377339465558890375382817519482034013819663,
        21108467747695834076222243215821423538605419377771908728895011199056664291649291940993568339023931469093608942591153226262017156966179245598,
        224, 18, 29, 5, 'LLJLLJLLLLLLLLJJJJLLL', 7_925, 7_530_151,
    ),
    6: (
        21191076913182172264633870715374809303569733235328366330733351418441103129442053791020750538674329530392392990122174179917963591624678417787,
        21192478722331885855941711159944607864601080587609347557169640906097871913860002966041506947066682198583479144717698079194231041723218030102,
        209, 11, 18, 9, 'LLJLLJLLLLJLLJL', 5_438, 963_359,
    ),
}


def closed_skip(seeds, end, word):
    lo = min(seeds)
    assert max(seeds) < end and all((s-lo)%2 == 0 for s in seeds) and (end-lo)%2 == 0
    certify_word(lo,end-2,word)  # Also proves all successors keep this parity.
    rule = openings(lo),word
    return {skip_cell(s,end,(rule,rule))[0] for s in seeds}


def extended_merger(i, rules, seeds):
    a,b,n,m,switches,k,even,edges,delta = EXTENDED[i]
    assert len(seeds) == n and all(s%2 for s in seeds)
    seeds = closed_skip(seeds,a,rules[1][1])
    assert len(seeds) == m
    even_seeds = set()
    count = 0
    for s in seeds:
        while s%2:
            t = first_return(s)
            assert t is not None and t > s
            s = t
            count += 1
            assert count <= switches
        even_seeds.add(s)
    assert count == switches
    seeds = closed_skip(even_seeds,b,even)
    assert len(seeds) == k and coalesce(seeds,edges) == (b+delta,edges)
    return b+delta


def audit_cycle(low,end,rules):
    # Both parity words send their seed to an even reset. A fixed even
    # word has seven bulks, so the gain depends only on the seed mod 256.
    assert low%2 == end%2 == 0
    assert tuple(word for _,word in rules) == ('LLJLLJLLL','LLLLLLLLL')
    for parity,(launch,word) in enumerate(rules):
        mass = 8*launch.even + 4*(launch.k+word.count('J')) + 5*word.count('L') + 5
        assert (parity+mass//2)%2 == 0
    graph = {}
    for i in range(128):
        nxt = evaluate(rules[0],low+2*i)
        assert nxt%2 == 0
        graph[i] = ((nxt-low)//2)%128
    active = set(graph)
    for _ in range(7):
        active = {graph[i] for i in active}
    assert len(active) == 27 and active == {graph[i] for i in active}
    i = min(active)
    path = []
    while i not in path:
        path.append(i)
        i = graph[i]
    assert i == path[0] and set(path) == active
    assert sum(evaluate(rules[0],low+2*i)-(low+2*i) for i in path) == 16_640
    possible = {evaluate(rules[0],s) for s in range(end-628,end,2) if (s-low)//2%128 in active}
    exits = {s for s in possible if s >= end}
    assert len(exits) == 65 and (min(exits)-end,max(exits)-end) == (4,604)
    assert coalesce(exits,6_929) == (end+3_687_890,6_929)


def check_onward(checkpoint):
    from check_confluence import itinerary
    from check_scale74_bridge_758 import formal_gain
    from scale_clauses_758 import EVEN_WORD, check_word
    # Every even seed through H returns in 615 seed units by endpoint order.
    for s in (checkpoint+1,HALTING_TARGET-1):
        assert s%2 == 0 and 0 < check_word(s,EVEN_WORD) <= 615
    suffix = 'L'*8+'J'+'L'*742+'J'+'L'*4+'JL'
    word = 'J'*292+suffix+'R'
    assert certify_word(checkpoint-726,checkpoint+29_812,suffix) == 2**756
    for s in (checkpoint-728,checkpoint+29_814):
        assert 'J'+itinerary(s)[0] != word
    assert word.count('L') == 755 and 2**756 > HALTING_TARGET
    assert (formal_gain(checkpoint,word),formal_gain(checkpoint+2**755,word)) == (3216,3218)
    s = checkpoint
    for _ in range(10):
        assert s <= checkpoint+29_812
        s = first_return(s)
    assert s == checkpoint+32_308 and first_return(s) == checkpoint+35_577
    far = HALTING_TARGET-(153*10**10*3**264)//100
    gap = far-checkpoint
    assert 1118*10**133 < gap < 1119*10**133
    print('From the last checkpoint to the published far edge of scale 264:',gap)


def verify():
    cells = [(lo,hi,rules) for lo,hi,*rules in partition(POWER,8)
             if lo < HALTING_TARGET and None not in rules]
    assert len(cells) == 11 and all(hi < HALTING_TARGET for _,hi,_ in cells)
    short = {i:(n,e,d) for i,n,e,d in MERGERS}
    for i,(lo,hi,rules) in enumerate(cells,1):
        # Every seed in [lo,hi) must escape alive in positive first returns.
        # The last seed sits no farther below hi than the maximum return gain.
        gain = max((8*launch.even + 4*(launch.k+word.count('J')) + 9*word.count('L') + 5)//2
                   for launch,word in rules)
        assert lo < hi-gain
        exits = {evaluate(rules[s%2],s) for s in range(hi-gain,hi)}
        exits = {s for s in exits if s >= hi}
        if i in EXTENDED:
            checkpoint = extended_merger(i,rules,exits)
        else:
            count,edges,delta = short[i]
            checkpoint = hi+delta
            assert len(exits) == count and coalesce(exits,edges) == (checkpoint,edges)
        if i == 7:
            assert gain == 627
            audit_cycle(lo,hi,rules)
        if i == 11:
            check_onward(checkpoint)
        print(i,'end',hi,'checkpoint',checkpoint,flush=True)
    width = sum(hi-lo for lo,hi,_ in cells)
    assert 439_813_660*(HALTING_TARGET-POWER) < width*10**9 < 439_813_662*(HALTING_TARGET-POWER)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    verify()
