"""Find windows admitting a symbolic certificate on the next doubled-power link."""
import argparse
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from after_fourth_758 import CHECKPOINT
from power_gates_758 import coarse_return, coalesce, gate_exits

HERE = Path(__file__).resolve().parent
END = 30_018_927_059_399_750
STRIDE = 2*10**12


def survey(exe, window):
    lo, hi = window
    result = subprocess.run([str(exe), str(lo), str(hi)], text=True, capture_output=True)
    if result.returncode:
        if result.returncode == 1 and result.stderr.strip() == "direct trace requested":
            return False
        raise RuntimeError(result.stderr)
    start, cut, first, last, blocks, calls = map(int, result.stdout.split())
    assert (start, cut) == window and cut <= first <= last <= cut+5_000
    assert blocks >= 0 and calls == 0
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk", type=int, help="survey one zero-based window")
    parser.add_argument("--list-hard", action="store_true", help="print unresolved window indices")
    args = parser.parse_args()
    if not __debug__:
        parser.error("run without -O")
    for first in (20_012_618_039_599_810, END+1):
        assert coarse_return(34, first, 2) > first
        try:
            coarse_return(34, first-2, 2)
        except AssertionError:
            pass
        else:
            raise AssertionError("the preceding seed still has this word")
    assert END+5_000 < 2*3**34-2*34-6-34*(4*34+40)
    assert coalesce(gate_exits(34, 2), 693) == (2*3**34+32_211, 693)
    cuts = list(range(CHECKPOINT, END, STRIDE)) + [END]
    pairs = list(zip(cuts, cuts[1:]))
    assert len(pairs) == 5_820
    if args.chunk is not None and not 0 <= args.chunk < len(pairs):
        parser.error(f"--chunk must be between 0 and {len(pairs)-1}")
    with TemporaryDirectory() as temp:
        exe = Path(temp)/"symbolic"
        subprocess.run(["c++", "-std=c++17", "-O3", "-DBB758_SYMBOLIC_ONLY",
                        str(HERE/"cross_758_fast.cpp"), "-o", str(exe)], check=True)
        if args.chunk is not None:
            pair = pairs[args.chunk]
            print(pair, "certified" if survey(exe, pair) else "requires direct tracing")
            return
        hard = [i for i, pair in enumerate(pairs) if not survey(exe, pair)]
    assert len(hard) == 1_043
    print(f"{len(pairs)-len(hard):,} windows certified symbolically; {len(hard):,} need more work.")
    if args.list_hard:
        print(*hard)


if __name__ == "__main__":
    main()
