"""Certify the first #758 reset beyond the second candidate pair."""
from argparse import ArgumentParser
from pathlib import Path
from subprocess import PIPE, run
from tempfile import TemporaryDirectory

from check_bb33 import champion_step, first_return


K = 2_031_355_966_425_479
KNOWN_CUT = 1_927_938_094_216_160
GATE = 1_928_257_804_717_083
JOIN = 1_928_257_804_761_237


def scalar(seed):
    target = first_return(seed, batch=False)
    assert target is not None and target > seed
    return target


def confluence():
    # Every intermediate edge is a first positive return, and all roots
    # reach JOIN. Equal later resets share their remaining path.
    known = {JOIN}
    for seed in range(GATE, GATE+5001):
        path = []
        while seed not in known:
            assert seed < JOIN
            path.append(seed)
            seed = scalar(seed)
        known.update(path)
    return len(known)-1


def label(a,c):
    # Each nonterminal branch is specified by linear guards and residues.
    if a <= c:
        if a%2 == 0:
            return "R" if c%2 else "halt"
        return "J" if c%2 else "I"
    if c%2 == 0:
        return "A"
    if a == c+1:
        return "halt"
    if c%4 == 1:
        return "B"
    if a == c+2:
        return "E"
    return "halt" if a == c+3 else "C"


def lifted_return(seed, shift, count):
    """Certify every first return from seed+i*shift for 0 <= i < count."""
    assert shift > 0 and count >= 2
    last = count-1
    states = [(1,seed+i*shift) for i in (0,1,last)]
    for _ in range(5000):
        (a,c),(near_a,near_c),(far_a,far_c) = states
        da, dc = near_a-a, near_c-c
        assert (far_a,far_c) == (a+last*da,c+last*dc)
        op = label(a,c)
        assert op != "halt" and all(label(*s) == op for s in states)
        # Residues repeat for every i. The ordinary inequalities and the
        # equality in E hold between the two extremal affine configurations.
        assert da%2 == dc%2 == 0
        if op in ("B","C","E"):
            assert dc%4 == 0
        states = [champion_step(*s) for s in states]
        assert all(s is not None for s in states)
        (a,c),(near_a,near_c),(far_a,far_c) = states
        if a == 1:
            assert near_a == far_a == 1
            assert near_c == c+shift and far_c == c+last*shift
            assert c > seed
            return c
        # No translated run can visit a=1 earlier.
        assert (a > 1 and far_a > 1) or (a == far_a == 0)
    raise AssertionError("lifted first return exceeded its check budget")


def cycle(seed, shift, count, returns):
    start = seed
    for _ in range(returns):
        seed = lifted_return(seed, shift, count)
    assert seed == start+shift
    return start+count*shift


def bridge(seed, returns, endpoint):
    for _ in range(returns):
        seed = scalar(seed)
    assert seed == endpoint
    return seed


def exact_second():
    edges = confluence()
    assert edges == 6_249
    seed = bridge(JOIN,64,1_928_257_804_768_921)
    seed = cycle(seed,1536,26_013_946_962,17)
    seed = bridge(seed,20,1_968_215_227_304_800)
    seed = cycle(seed,80,789_259_239_008,1)
    assert seed == K-39 and scalar(seed) == K+41
    returns = 64+17*26_013_946_962+20+789_259_239_008+1
    assert returns == 1_231_496_337_447
    return edges, returns


def check_gate(executable):
    output = run([executable, str(KNOWN_CUT), str(GATE)],
                 text=True, stdout=PIPE, check=True)
    a,b,lo,hi,_,_ = map(int, output.stdout.split())
    assert (a,b) == (KNOWN_CUT,GATE) and GATE <= lo <= hi <= GATE+5000


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O so all verification checks execute.")
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--checker", type=Path, help="use an already compiled crossing checker")
    parser.add_argument("--arithmetic-only", action="store_true", help="check the result from the 5,001 gate resets")
    args = parser.parse_args()
    if not args.arithmetic_only:
        if args.checker:
            check_gate(args.checker.resolve())
        else:
            with TemporaryDirectory() as tmp:
                exe = Path(tmp)/"cross_758_fast"
                source = Path(__file__).with_name("cross_758_fast.cpp")
                run(["c++","-O3","-std=c++17",source,"-o",exe],check=True)
                check_gate(exe)
    edges, returns = exact_second()
    print(f"{edges:,} gate edges coalesce. The join reaches the exit in {returns:,} first returns.")
    print(f"The pair lies between consecutive resets {K-39:,} and {K+41:,} (K+41).")
