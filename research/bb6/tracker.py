"""Check and display the BB(6) register using only the Python standard library."""

import argparse
import csv
import hashlib
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BASELINE_SHA256 = "a5229ff6abd03dd30c59784c0d4e1465754991d197878c139951860ddcab556a"
FIELDS = "line machine_id machine status same_as_line evidence_date source simulation_log notes".split()
STATUSES = (
    "OPEN", "HALT_PR", "NONHALT_PR", "PARTIAL_PR", "SIMULATED_HALT",
    "EQUIVALENCE_PR", "EQUIVALENT", "HALTS", "NONHALTS",
)


def load_register():
    # Normalize newlines for checkouts using Git's core.autocrlf.
    baseline = (ROOT / "BB6_holdouts_608.txt").read_text(encoding="utf-8")
    if hashlib.sha256(baseline.encode("utf-8")).hexdigest() != BASELINE_SHA256:
        raise ValueError("the frozen October 30 baseline has changed")
    identities = baseline.splitlines()
    with (ROOT / "MACHINES.csv").open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        if reader.fieldnames != FIELDS:
            raise ValueError("unexpected MACHINES.csv columns")
        rows = list(reader)
    if len(rows) != len(identities):
        raise ValueError(f"expected {len(identities)} rows, found {len(rows)}")

    for line, (identity, row) in enumerate(zip(identities, rows), 1):
        if None in row or None in row.values():
            raise ValueError(f"line {line}: incorrect field count")
        if row["line"] != str(line) or [row["machine_id"], row["machine"]] != identity.split():
            raise ValueError(f"line {line}: index, machine ID or transition string differs from baseline")
        status = row["status"]
        if status not in STATUSES:
            raise ValueError(f"line {line}: unknown status {status!r}")
        if status != "OPEN" and not (row["source"].strip() and row["evidence_date"]):
            raise ValueError(f"line {line}: record a source and evidence date for {status}")
        if row["evidence_date"]:
            try:
                date.fromisoformat(row["evidence_date"])
            except ValueError as exc:
                raise ValueError(f"line {line}: invalid evidence date") from exc
        peer = row["same_as_line"]
        if status in ("EQUIVALENCE_PR", "EQUIVALENT"):
            if not peer.isascii() or not peer.isdecimal() or not 1 <= int(peer) < line:
                raise ValueError(f"line {line}: equivalence must point to an earlier line")
        elif peer:
            raise ValueError(f"line {line}: only an equivalence row can point to another line")
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--open", action="store_true", help="list targets for a fresh decision")
    group.add_argument("--line", type=int, help="show one permanent one-based line")
    args = parser.parse_args()
    try:
        rows = load_register()
    except (OSError, ValueError, csv.Error) as exc:
        parser.exit(1, f"Register check failed: {exc}\n")
    if args.line is not None:
        if not 1 <= args.line <= len(rows):
            parser.error(f"--line must be between 1 and {len(rows)}")
        for name, value in rows[args.line - 1].items():
            if value:
                print(f"{name}: {value}")
    elif args.open:
        print("line\tmachine_id\tmachine")
        for row in rows:
            if row["status"] == "OPEN":
                print(row["line"], row["machine_id"], row["machine"], sep="\t")
    else:
        counts = Counter(row["status"] for row in rows)
        print(f"{len(rows)} indexed machines")
        for status in STATUSES:
            print(f"{status:16} {counts[status]:3}")


if __name__ == "__main__":
    main()
