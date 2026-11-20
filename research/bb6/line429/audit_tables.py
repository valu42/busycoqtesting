"""Find explicit encodings of the line-429 table in Lean and Rocq files at local Git refs."""
import argparse
from itertools import permutations
from pathlib import Path
import re
import subprocess

TARGET = "1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA0RF"
STATES = "ABCDEF"
CELL = rb"(?:[01][LR][A-FHZ]|HHH|---)"
ROW = CELL * 2
SEPARATOR = rb"[_ \t]+"
TABLE = re.compile(rb"(?<![A-Z0-9])(" + ROW + rb"(?:" + SEPARATOR + ROW + rb"){5})(?![A-Z0-9])")


def encodings():
    forms = {}
    for perm in permutations(STATES):
        renamed = dict(zip(STATES, perm))
        for mirror in (False, True):
            rows = [""] * 6
            for state, row in zip(STATES, TARGET.split("_")):
                actions = []
                for move in (row[:3], row[3:]):
                    if move == "---":
                        actions.append(move)
                    else:
                        written, direction, dest = move
                        if mirror:
                            direction = {"L": "R", "R": "L"}[direction]
                        actions.append(written + direction + renamed[dest])
                rows[STATES.index(renamed[state])] = "".join(actions)
            forms["_".join(rows).encode()] = renamed["A"]
    assert len(forms) == 1440
    return forms


def git(repo, *args):
    return subprocess.check_output(["git", "-C", repo, *args])


def sources(repo, refs):
    blobs = {}
    for ref in refs:
        for line in git(repo, "ls-tree", "-r", ref).splitlines():
            entry, name = line.split(b"\t", 1)
            if name.endswith((b".v", b".lean")):
                blobs.setdefault(entry.split()[-1], (ref, name.decode()))
    return blobs


def audit(repo, refs, forms):
    blobs = sources(repo, refs)
    count = 0
    with subprocess.Popen(["git", "-C", repo, "cat-file", "--batch"],
                          stdin=subprocess.PIPE, stdout=subprocess.PIPE) as proc:
        for oid, (ref, path) in blobs.items():
            proc.stdin.write(oid + b"\n")
            proc.stdin.flush()
            size = int(proc.stdout.readline().split()[-1])
            data = proc.stdout.read(size)
            assert len(data) == size and proc.stdout.read(1) == b"\n"
            for match in TABLE.finditer(data):
                text = re.sub(SEPARATOR, b"_", match[1])
                text = re.sub(rb"HHH|[01][LR][HZ]", b"---", text)
                start = forms.get(text)
                if start:
                    line = data.count(b"\n", 0, match.start()) + 1
                    print(f"{ref} {path}:{line}  target start maps to {start}")
                    count += 1
        proc.stdin.close()
        assert proc.wait() == 0
    print(f"{repo}: {len(blobs)} distinct source blobs, {count} explicit table occurrences")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", type=Path)
    parser.add_argument("refs", nargs="*", help="defaults to all locally available remote tips")
    args = parser.parse_args()
    refs = args.refs or git(args.repo, "for-each-ref", "--format=%(refname)",
                            "refs/remotes").decode().splitlines() or ["HEAD"]
    audit(args.repo, refs, encodings())
