# Nonhalting of the BB(2,5) machine 1RB2LA1LA4RA2LA_0LA3RB3LB2RB---

Starting in state A on the all-zero tape, this machine never reaches B on symbol 4, its only undefined transition. It is entry 36 in the November 3 list of 37 machines and entry 58 in the website's list of 60. The public theorem uses the machine string parsed by `Individual25.TM_from_str` and BusyCoq's blank configuration. [Theorem](../../verify/BB25_Line36.v) · [Machine viewer](https://bbchallenge.org/1RB2LA1LA4RA2LA_0LA3RB3LB2RB---)

## Argument

After 612,729 elementary steps the machine reaches a checkpoint with 1,035 data cells. Each subsequent sweep returns to a checkpoint in a positive number of steps. The induction protects the left part of the tape from the unmatched closings in its right part. Two finite calculations bound how far the cut can move and how much cancellation the rightmost 50 cells force. Together the bounds guarantee enough surviving openings to complete another sweep. [Mathematical proof](https://github.com/valu42/busycoqtesting/blob/113d896813afdb99b69a6a6010b5ff98738a6398/research/bb2x5/line36-nonhalting.md)

| What to review | Where |
|---|---|
| Parsed transition table, blank seed, and progress in elementary steps | [Machine](../../verify/Line36Machine.v) and [physical sweep](../../verify/Line36Physical.v) |
| How the invariant implies infinitely many checkpoints | [Induction](../../verify/Line36Nonhalt.v) and [final theorem](../../verify/BB25_Line36.v) |
| How every debt is covered | [Finite-debt proof](../../verify/Line36LowBranch.v) and [large-debt proof](../../verify/Line36HighBranch.v) |
| The two exhaustive computations | [Left certificate](../../verify/Line36LeftCertificate.v) and [right certificate](../../verify/Line36CapCertificate.v) |

## Build

From the repository root, with Coq 8.20.1, GNU Make and a C++17 compiler, run:

```sh
make -C verify -j6 line36
coqtop -quiet -Q verify BusyCoq <<'EOF'
From Coq Require Import Strings.String.
From BusyCoq Require Import Individual25 BB25_Line36.
Open Scope string_scope.
Check BB25_Line36.nonhalt.
Print Assumptions BB25_Line36.nonhalt.
EOF
```

The explicit `line36` target builds this individual proof. The six phases collectively check 14,877,696 concrete transitions. The C++ generator rebuilds the packed table for 16,939,461 reachable right suffixes. Rocq checks the table's transitions and proves that the physical tape follows them. [Generator](line36_right_cap.cpp) · [Original formalization](https://github.com/valu42/busycoqtesting/blob/113d896813afdb99b69a6a6010b5ff98738a6398/research/bb2x5/line36-rocq.md)

To independently replay the theorem and all its compiled dependencies, run:

```sh
coqchk -bytecode-compiler yes -Q verify BusyCoq BusyCoq.BB25_Line36
```
