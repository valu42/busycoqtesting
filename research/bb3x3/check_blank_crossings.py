"""Reproduce the blank-tape crossings, or check one independent section."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from check_bb33 import champion_step, first_return
from check_candidate_exits import CASES, trace
from check_confluence import LOW as PUBLISHED

HERE = Path(__file__).resolve().parent
FIRST_FORWARD = 1_080_000_000_055_450
SPAN = 500_000_000_000
WIDTH = 5_000
FIRST_CUT = 100_003
NAMES = ("prefix", "bridge", "first", "second", "third")


def prefix_entry():
    # First two raw steps enter A(0,1). Check the next map call and the
    # unique blank trajectory before using a window of possible states.
    assert champion_step(0, 1) == (1, 3)
    seed = 3
    while seed < FIRST_CUT:
        nxt = first_return(seed, batch=False)
        assert nxt is not None and nxt > seed
        seed = nxt
    assert seed == 100_008 and FIRST_CUT <= seed <= FIRST_CUT + WIDTH


def cuts(section):
    if section == "prefix":
        result = [FIRST_CUT]
        while result[-1] < PUBLISHED:
            last = result[-1]
            span = min(SPAN, max(100_000, last // 20))
            result.append(min(PUBLISHED, last + span))
        return result
    k1, k2, k3 = (case[0] for case in CASES)
    windows = {
        "bridge": (PUBLISHED, FIRST_FORWARD),
        "first": (FIRST_FORWARD, k1 - 199_000),
        "second": (k1 + 50, k2 - 199_000),
        "third": (k2 + 3, k3 - 199_000),
    }
    start, limit = windows[section]
    return list(range(start, limit, SPAN)) + [limit]


def run_window(exe, pair):
    lo, hi = pair
    proc = subprocess.run([str(exe), str(lo), str(hi)], capture_output=True, text=True)
    if proc.returncode:
        raise RuntimeError(f"Window {lo}..{hi} failed: {proc.stderr.strip()}")
    start, cut, first, last, blocks, calls = map(int, proc.stdout.split())
    assert (start, cut) == (lo, hi) and hi <= first <= last <= hi + WIDTH
    assert blocks >= 0 and calls >= 0
    return last-hi


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--section", choices=("all", *NAMES), default="all")
    parser.add_argument("--jobs", type=int, default=4, help="parallel C++ workers")
    parser.add_argument("--chunk", type=int, help="verify only this zero-based window index")
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error("run without -O and use at least one worker")
    if args.chunk is not None and args.section == "all":
        parser.error("--chunk needs an individual --section")

    sections = NAMES if args.section == "all" else (args.section,)
    with TemporaryDirectory() as temp, ThreadPoolExecutor(max_workers=args.jobs) as pool:
        exe = Path(temp) / "cross_758"
        subprocess.run(["c++", "-std=c++17", "-O3", str(HERE / "cross_758.cpp"),
                        "-o", str(exe)], check=True)
        for section in sections:
            if section == "prefix":
                prefix_entry()
            grid = cuts(section)
            windows = list(zip(grid, grid[1:]))
            if args.chunk is not None:
                if not 0 <= args.chunk < len(windows):
                    parser.error(f"{section} has {len(windows)} windows")
                windows = [windows[args.chunk]]
            largest = max(pool.map(lambda pair: run_window(exe, pair), windows))
            print(f"{section}: {len(windows)} windows passed, maximum excess {largest}.", flush=True)
            if section in NAMES[2:] and args.chunk is None:
                candidate, expected, edges = CASES[NAMES.index(section) - 2]
                assert trace(candidate) == (expected, edges)
                print(f"Local exits above {candidate}: {expected}", flush=True)


if __name__ == "__main__":
    main()
