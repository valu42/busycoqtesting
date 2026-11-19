"""Replay the four links from the doubled power-32 gate to the fourth terminal."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from after_fourth_758 import verify as after_fourth
from check_bb33 import first_return
from exact_fourth_758 import ENTRY, NEXT, verify_fourth
from exception_power_phases_758 import SIDE_WINDOWS, middle_crossing, power_phase, verify_candidates
from power_gates_758 import coarse_return, coalesce, gate_exits

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "power_crossings_758.tsv.gz"
WIDTH = 5_000
LEGS = {
    "power33": (2*3**32+41_023, 5_558_504_660_484_436, 10**12),
    "double33": (3**33+87_239, 10_006_309_019_799_870, 2*10**12),
    "power34": (2*3**33+90_349, 16_484_970_113_975_417, 2*10**12),
    "fourth": (3**34+9_103, ENTRY, 2*10**12),
}
GATES = {
    # exponent, multiple, merger edges, resulting offset
    "power33": (33, 1, 1_332, 87_239),
    "double33": (33, 2, 1_123, 90_349),
    "power34": (34, 1, 107, 9_103),
}


def windows(leg):
    lo, end, stride = LEGS[leg]
    cuts = list(range(lo, end, stride)) + [end]
    return list(zip(cuts, cuts[1:]))


def check_gate(leg):
    if leg == "fourth":
        assert verify_fourth()[1] == NEXT
        after_fourth()
        return NEXT
    m, multiple, edges, offset = GATES[leg]
    p = 3**m
    low = LEGS[leg][1]
    boundary = multiple*p-2*m-(4 if multiple == 1 else 6)
    high = ((boundary+2*m+7, boundary) if multiple == 1 else
            (boundary, boundary+2*m+11))
    assert low+WIDTH <= boundary-34*(4*m+40)
    for parity, ceiling in enumerate(high):
        for seed in (low+(parity-low)%2, ceiling-(ceiling-parity)%2):
            assert coarse_return(m, seed, multiple) > seed
    checkpoint, steps = coalesce(gate_exits(m, multiple), edges)
    assert (checkpoint, steps) == (multiple*p+offset, edges)
    return checkpoint


def read_report():
    report = {leg: [] for leg in LEGS}
    with gzip.open(MANIFEST, "rt") as handle:
        assert next(handle).split() == ["leg", "engine", "start", "end", "min", "max", "blocks", "calls"]
        for row in handle:
            leg, engine, *numbers = row.split()
            start, end, first, last, blocks, calls = map(int, numbers)
            assert engine in ("general", "fast", "plain", "even")
            assert engine != "even" or leg in ("power33", "power34")
            assert end <= first <= last <= end+WIDTH and min(blocks, calls) >= 0
            report[leg].append((start, end, first, last, blocks, calls, engine))
    for leg, rows in report.items():
        assert [(s, e) for s, e, *_ in rows] == windows(leg)
    return report


def replay(executables, row):
    lo, end, *_ = row
    errors = []
    for executable in executables:
        result = subprocess.run([str(executable), str(lo), str(end)], capture_output=True, text=True)
        if result.returncode == 0:
            break
        errors.append(f"{executable.name}: {result.stderr.strip()}")
    else:
        raise RuntimeError(f"Window {lo} to {end} failed: {' | '.join(errors)}")
    start, cut, first, last, blocks, calls = map(int, result.stdout.split())
    assert (start, cut) == (lo, end)
    assert end <= first <= last <= end+WIDTH and min(blocks, calls) >= 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--leg", choices=(*LEGS, "all"), default="all")
    parser.add_argument("--chunk", type=int, help="zero-based window on the selected leg")
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--engine", choices=("recorded", "general", "reference"), default="recorded")
    parser.add_argument("--report-only", action="store_true",
                        help="validate archived row coverage and replay gate algebra without rerunning C++")
    parser.add_argument("--exception-phases", action="store_true",
                        help="also check two side windows used to identify exceptional-branch candidates")
    args = parser.parse_args()
    if not __debug__ or args.jobs < 1:
        parser.error("run without -O and select a positive worker count")
    if args.chunk is not None and (args.chunk < 0 or args.leg == "all"):
        parser.error("--chunk requires a nonnegative index and an individual --leg")
    if args.exception_phases and args.chunk is not None:
        parser.error("--exception-phases needs a full leg")
    report = read_report()
    selected = tuple(LEGS) if args.leg == "all" else (args.leg,)
    # Anchor the first link at the published exact reset after the third pair.
    exits = gate_exits(32, 2)
    seed = 2*3**32-20
    assert seed in exits
    assert coalesce(exits, 857) == (LEGS["power33"][0], 857)
    for _ in range(167):
        seed = first_return(seed, batch=False)
        assert seed is not None
    assert seed == LEGS["power33"][0]
    with TemporaryDirectory() as temp, ThreadPoolExecutor(args.jobs) as workers:
        compiled = {}
        for leg in selected:
            rows = report[leg]
            if args.exception_phases and leg in SIDE_WINDOWS:
                side = SIDE_WINDOWS[leg]
                lo, end, first, last, blocks, calls = side
                assert any(a == lo and end < b for a,b in windows(leg))
                assert lo < end <= first <= last <= end+WIDTH and min(blocks, calls) >= 0
                rows = rows + [(*side, "fast")]
            if args.chunk is not None:
                if args.chunk >= len(rows):
                    parser.error(f"{leg} has only {len(rows)} windows")
                rows = [rows[args.chunk]]
            if not args.report_only:
                jobs = []
                for row in rows:
                    engine = ({"general": "general", "reference": "plain"}.get(args.engine)
                              or row[-1])
                    executables = []
                    for solver in (("fast", "plain") if engine == "general" else (engine,)):
                        exp = (32 if leg == "power33" else 33) if solver == "even" else 0
                        key = solver, exp
                        if key not in compiled:
                            source = {"fast": "cross_758_fast.cpp", "plain": "cross_758.cpp",
                                      "even": "cross_even_power_758.cpp"}[solver]
                            exe = Path(temp)/f"{solver}{exp}"
                            flags = [f"-DPOWER_EXPONENT={exp}"] if exp else []
                            subprocess.run(["c++", "-O3", "-std=c++17", *flags,
                                            str(HERE/source), "-o", str(exe)], check=True)
                            compiled[key] = exe
                        executables.append(compiled[key])
                    jobs.append(workers.submit(replay, executables, row))
                for job in jobs:
                    job.result()
            largest = max(row[3]-row[1] for row in rows)
            mode = "archived" if args.report_only else "replayed"
            print(f"{leg}: {len(rows)} windows {mode}, largest archived excess {largest:,}.", flush=True)
            if args.chunk is None:
                print(f"Gate checkpoint {check_gate(leg):,}.", flush=True)
                if args.exception_phases and leg == "power33":
                    power_phase()
                if args.exception_phases and leg == "power34":
                    middle_crossing()
        if args.exception_phases:
            print("Candidate reset-to-E families:", verify_candidates())


if __name__ == "__main__":
    main()
