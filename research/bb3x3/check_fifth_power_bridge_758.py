"""Check and optionally reproduce the indexed bridge after 2*3**34."""
import argparse
import concurrent.futures
import subprocess
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIRST = 2*3**34 + 32_211
LAST = 39_752_584_607_270_532
CUTS = (*range(FIRST, LAST, 10**13), LAST)


def read_rows(path):
    rows = {}
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        index, worker, *columns = line.split()
        index = int(index)
        receipt = tuple(map(int, columns))
        if not (0 <= index < len(CUTS)-1) or index in rows:
            raise ValueError(f"invalid or duplicate index {index}")
        if worker not in ("ordinary", "paired"):
            raise ValueError(f"unknown worker {worker}")
        lo, cut, minimum, maximum, blocks, calls = receipt
        if (lo, cut) != CUTS[index:index+2] or not cut <= minimum <= maximum <= cut+5000:
            raise ValueError(f"invalid endpoints at index {index}")
        if min(blocks, calls) < 0:
            raise ValueError(f"negative operation count at index {index}")
        rows[index] = worker, receipt
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--table", type=Path, default=HERE/"fifth_power_bridge_758.tsv")
    parser.add_argument("--ordinary", type=Path, help="compiled cross_758_fast.cpp")
    parser.add_argument("--paired", type=Path, help="compiled cross_even_power_758.cpp, exponent 34")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--start", type=int, default=0, help="first index for optional replay")
    parser.add_argument("--stop", type=int, default=len(CUTS)-1, help="exclusive index for replay")
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--fill", action="store_true", help="compute missing windows with the paired worker")
    args = parser.parse_args()
    if not 0 <= args.start <= args.stop <= len(CUTS)-1 or args.jobs < 1:
        parser.error("invalid range or number of workers")
    rows = read_rows(args.table)
    if args.fill:
        if args.paired is None:
            parser.error("--fill requires --paired")
        pending = [i for i in range(args.start, args.stop) if i not in rows]

        def fill(index):
            lo, cut = CUTS[index:index+2]
            raw = subprocess.run([args.paired.resolve(), str(lo), str(cut)], check=True,
                                 capture_output=True, text=True).stdout
            receipt = tuple(map(int, raw.split()))
            a, b, mn, mx, blocks, calls = receipt
            if not ((a, b) == (lo, cut) and cut <= mn <= mx <= cut+5000
                    and min(blocks, calls) >= 0):
                raise ValueError(f"invalid computed receipt at index {index}")
            return index, receipt

        with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
            futures = [pool.submit(fill, i) for i in pending]
            for future in concurrent.futures.as_completed(futures):
                i, receipt = future.result()
                rows[i] = ("paired", receipt)
                tmp = args.table.with_suffix(".tmp")
                with tmp.open("w") as out:
                    print("# index worker lo cut minimum maximum blocks exact_calls", file=out)
                    for k, (worker, row) in sorted(rows.items()):
                        print(k, worker, *row, file=out)
                tmp.replace(args.table)
    missing = sorted(set(range(len(CUTS)-1)) - rows.keys())
    count = missing[0] if missing else len(CUTS)-1
    print(f"{len(rows)}/{len(CUTS)-1} windows; first {count} continuous through {CUTS[count]:,}.")
    if args.require_complete and missing:
        raise SystemExit(f"Missing {len(missing)} windows, starting at index {missing[0]}.")
    if args.fill:
        return
    programs = {"ordinary": args.ordinary, "paired": args.paired}

    def replay(index):
        worker, receipt = rows[index]
        path = programs[worker].resolve()
        result = subprocess.run([path, *map(str, receipt[:2])], check=True,
                                capture_output=True, text=True)
        if tuple(map(int, result.stdout.split())) != receipt:
            raise ValueError(f"{worker} receipt mismatch at index {index}")

    selected = [i for i in range(args.start, args.stop)
                if i in rows and programs[rows[i][0]] is not None]
    if selected:
        with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
            for _ in pool.map(replay, selected):
                pass
        print(f"Reproduced {len(selected)} complete receipts.")


if __name__ == "__main__":
    main()
