"""Classify the scale-74 midpoint crossings that certify genuine reset entry."""
from check_bb33 import HALTING_TARGET as H, champion_step, first_return
from scale_clauses_758 import BASE, check_corridor, cycle_exits
from terminal_forest_758 import exhaust


G = BASE*3**74
DISTANCE = 5*G//4
T = H-DISTANCE
MASS = 2*T+1
GAIN_BOUND = 1184


def crossing(seed):
    """Find first crossing in this single excursion, or None on an earlier reset."""
    s = (1,seed)
    for steps in range(1,2001):
        s = champion_step(*s)
        assert s is not None
        if s[0]+2*s[1] >= MASS:
            return s,steps
        if s[0] == 1:
            return None
    raise AssertionError("local crossing budget exhausted")


def verify():
    check_corridor(74)
    image = {}
    for seed in range(T-GAIN_BOUND,T):
        result = crossing(seed)
        if result:
            target, depth = result
            image.setdefault(target,{})[seed] = depth
    assert (len(image),sum(map(len,image.values()))) == (700,815)
    assert {c-T for a,c in image if a == 1} == {0,2}

    nodes = starts = longest = oldest = 0
    for target, origins in image.items():
        if target[0] == 1:
            continue
        resets, visited, depth = exhaust(target,5000)
        assert set(origins.items()) <= set(resets.items())
        assert all(T-1018 <= seed < T for seed in resets)
        nodes += visited
        starts += len(resets)
        longest = max(longest,depth)
        oldest = max(oldest,max(T-seed for seed in resets))
    assert (starts,nodes,longest,oldest) == (811,750444,507,1018)

    # A reset first crossing can only be T..T+4. For T+3 the output is even
    # and the only reset-producing branch is R, whose gain 5 is too small.
    # For T+4, only the larger-charge bulk parent can cross, and it is dead.
    assert T%6 == 1
    q = (T+4-5)//6
    parent = (4*q+4,4*q-1)
    assert parent[0]+2*parent[1] == MASS-1
    assert champion_step(*parent) == (1,T+4)
    assert exhaust(parent,10) == ({},3,1)

    cycles, exits = cycle_exits(74,lower=DISTANCE+4000)
    assert (cycles,exits) == ([(64,1)],[858])
    seed = T-4000+858
    while True:
        result = crossing(seed)
        if result:
            break
        new = first_return(seed,batch=False)
        assert new is not None and seed < new < T
        seed = new
    target, depth = result
    assert (seed-T,depth) == (-72,36)
    assert target == (2*3**36-1,T-3**36+1)
    assert exhaust(target,5000)[0] == {T-72:36}
    return 700,698,750444


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so verification remains active.")
    verify()
    print("815 reset seeds give 700 first crossing states, 698 of them nonresets.")
    print("All nonreset inverse queues exhaust. Deep entry gives the sole last reset T-72.")
