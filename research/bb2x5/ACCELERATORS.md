# Exact simulation tools for the BB(2,5) swarm

These tools extend the research at commit
`f895ccb5921c41545796f9f4edd6ae0831ee1e5b`. They add separate files so that an
agent pursuing the frontier, mixed-counter or sweep arguments need not merge
changes to its working code. The visible research concentrates on formal lines
17, 26, 2, 10, 3 and 36; the machine-specific runner here targets **line 5**.
Unpushed work by other agents is not visible. Line numbers refer only to the
checked-in `BB2x5_Rocq_holdouts_37.txt` (SHA-256
`89ea92fd4643166b92fca4ae80e37a699ab8615ac1dd375dae777e6b3e45ecc6`).

**No new holdout decision or Rocq theorem is claimed.** These are exact integer
simulation algorithms with differential tests, not kernel-checked proofs. A
finite safe prefix remains an unknown blank-tape classification. A checkpoint
contains a state from which to continue; loading a supplied checkpoint does not
independently establish that it is reachable from blank.

## Line 5: arithmetic instead of materializing unary tape

The exact machine is `1RB3LA1LA1RA1RA_2LB2RA---4RB1LB`.
The underlying two-counter normal forms and seven return rules are credited to
mxdys and Racheline in the [published analysis, revision 6815](https://wiki.bbchallenge.org/w/index.php?title=1RB3LA1LA1RA1RA_2LB2RA---4RB1LB&oldid=6815).
The repository already implements them as `published_return` and tests finite
instances in `prior_sweeps.py`. The repeated-A formula and the thin halting
family are also already published. The contribution here is a bounded,
resumable implementation, exact B-phase batching, and reusable validation.

Both normal-form tags A and B have the **concrete head state A**. Up to a tape
translation, they denote

```
A(a,b): 0^inf 1 4^a 1^4 [A>] 1^b 2 0^inf
B(a,b): 0^inf 1 4^a 1^(3+b) [A>] 11 0^inf
```

Blank reaches A(4,4) after 136 defined TM transitions. Exponents are stored as
arbitrary-precision integers. The unary tape need not be allocated.

For a run of k repeated A-to-A rules,

```
a' = 2^k (a+4) - 4
b' = b - (a+4)(2^k-1) + k.
```

The allowed k is the largest for which the total subtraction does not exceed
b. The subtraction is strictly increasing for a >= 0, so this checks all
intermediate guards, rather than guessing that an observed pattern continues.
From A(4,b), the next A phase halts exactly at the known values
`b = 16*2^k - 11 - k`, k >= 0. These are synthetic positive controls; finding
one in an arbitrary input is not a blank-tape result.

For consecutive B(a,0) updates through a divisible by 3, put x=2a+9. One
update sends x to 5x/3. Exactly v_3(x) such updates are possible, giving

```
a' = (5^k (x/3^k) - 9)/2, b'=0.
```

For consecutive B(a,2) updates through a congruent to 2 modulo 3, use x=2a+11
and replace 9 by 11. Mixed branches can also be composed: the low k ternary
digits determine up to k successive B branches. Fixing `a = r + 3^k q`
therefore yields an affine output in q. Composition stops at the first return
to normal form A, so it never skips an A-phase halting test.

The specialized tool counts applications of these published return rules and
completed returns to A(4,b). **Neither count is a raw TM step count.** An
unbounded B phase is not assumed to return; resource limits leave an exact
intermediate B checkpoint.

## General block-exit memoization

The general tool works directly from a transition table and does not assume a
normal form. A finite block is stored as a shared immutable binary tree. The
cache key includes the complete block, control state and entry side. Its value
is the exact rewritten block, exit state and side, and number of defined TM
transitions. A larger block is evaluated by composing exits from its two
halves. Equal subtrees and equal local computations are reused, so large
repeated regions and repeated excursions can be processed without enumerating
their individual cells or transitions.

Each base case executes the literal transition table. Each composed result
stops at the first exit from its block, so it is independent of the exterior
tape. An internal undefined instruction propagates immediately. Repetition of
a complete local configuration can establish a confined loop, but resource
exhaustion cannot. This is a general acceleration mechanism, not a promise of
exponential speedup on every machine; irregular tapes can defeat sharing.

## Reproduction and handoff

Python 3.10 or later and its standard library suffice. From the repository root:

```sh
cd research/bb2x5
python3 -m unittest test_arithmetic5 test_exact_blocks -v
python3 verify_accelerator_results.py --replay-line5
```

The 18 test groups include 432 literal-TM checks of arithmetic return rules,
exhaustive B-block quotient lifting through width five, guarded A skips,
synthetic halting controls, 7,400 local block replays, all 37 blank trajectories,
budget exhaustion, large integers, corrupted checkpoints and interrupted
checkpoint writes. An artificial uniform sweep checks an exact `2**60`-step
block computation using fewer than 400 work units; this demonstrates sharing
on a controlled input, not the performance of a holdout.

`verify_accelerator_results.py` reloads the complete saved states and compares
100 further block exits against a literal interpreter. Its optional
`--replay-line5` independently reconstructs all 100,000 saved line-5 rounds
using the pre-existing A formula and one B rule at a time, then compares the
entire counter and event count. Neither that reconstruction nor the large
block runs have been checked in Rocq.

### Saved finite results

| Target | Exact progress from blank | Saved state | Classification |
|---|---:|---|---|
| Line 5 | 100,000 A(4,b) returns; 8,684,421,216 macro events | A(4,b), b has 173,754 bits | Unknown |
| Line 29 | 4,124,222,829 defined TM steps | Full compressed tape, head and state | Unknown |
| Line 30 | 4,121,120,989 defined TM steps | Full compressed tape, head and state | Unknown |
| Line 31 | 3,913,364,635 defined TM steps | Full compressed tape, head and state | Unknown |

The line-5 run takes 380,120 accelerated operations. Its full counters are in
[`accelerator-results/arithmetic5-100k.json`](accelerator-results/arithmetic5-100k.json),
with counts in [`arithmetic5-results.json`](accelerator-results/arithmetic5-results.json).
The three general-simulator checkpoints and their checksums are indexed in
[`deep.json`](accelerator-results/deep.json). No previous search record or new
mathematical decision is claimed. Lines 29 and 30 belong to the already-studied
Hydra family; they are useful implementation benchmarks, not a new reduction.

Continue line 5 or reproduce its saved checkpoint:

```sh
python3 arithmetic5.py --rounds 100000 --max-operations 1000000 \
  --checkpoint arithmetic5-reproduced.json
python3 arithmetic5.py --resume accelerator-results/arithmetic5-100k.json \
  --rounds 10000 --seconds 60 --checkpoint arithmetic5-next.json
```

The canonical checkpoint integer fields use hexadecimal strings, avoiding
Python's decimal conversion limit. The state tag describes a normal form, not
the physical control state. A reported arithmetic halt identifies a halting
macro guard; it does not contain the final literal tape or an exact raw runtime.

Continue a general simulator checkpoint, or try another machine:

```sh
python3 exact_blocks.py --resume accelerator-results/line-31-level-12.json \
  --macros 1000000 --work 2000000 --seconds 60 --checkpoint line31-next.json
python3 exact_blocks.py --line 14 --level 10 --work 1000000 \
  --seconds 30 --checkpoint line14.json
```

The block level fixes the width at `2**level`; results depend on that choice.
Work counts summary invocations (including hits) and child-composition
iterations. Node and cache bounds are separate. On exhaustion the last
completed outer-block configuration is retained, even if some internal work
was performed. The exact raw-step counter includes only committed execution.
Checkpoints store reachable tape nodes, not the cache: resuming starts with a
cold cache. General integer strings are decimal for small values and hexadecimal
for very large ones. Both writers use a same-directory atomic replacement.

In Python, use `arithmetic5.Accelerator.step(State(...))` for auxiliary integer
states, or `exact_blocks.Engine.exit(node, state, side)` for exact finite block
queries. Numeric states are A=0, B=1; entry side 0 means the left edge and 1 the
right edge. A returned `exit` stops before consulting the neighboring cell.
`halt` means an undefined instruction inside the queried block; `loop` means a
repeated complete local configuration with a positive period. For continued
global execution use `Run.blank` / `Run.restore` and `Run.advance`. Stored loop
claims are trusted input on reload, not independently checked proof objects.

### Measured speed and pilot coverage

The committed [`benchmarks.json`](accelerator-results/benchmarks.json) compares
full tape, head, state and raw-step endpoint against `prior_sweeps.TapeMachine`:

| Line | Raw steps at common endpoint | Accelerator seconds | Python literal seconds | Ratio |
|---|---:|---:|---:|---:|
| 29 | 6,030,217 | 0.0480 | 2.1733 | 45.2x |
| 30 | 5,847,870 | 0.0477 | 2.5629 | 53.7x |
| 31 | 3,635,811 | 0.0601 | 1.2780 | 21.3x |

These timings are environment-specific Python 3.12.14 measurements, not a
comparison with the fastest available simulator. The line-5 benchmark compares
3,000 rounds against its scalar recurrence, with complete counter and event
equality. Its roughly 320x measured ratio **includes the already-known A
doubling shortcut**, so it is not a speedup claim over `largest_repeat`.

[`pilot.json`](accelerator-results/pilot.json) records 99 bounded runs: block
levels 6, 10 and 14 across the 33 lines other than 2, 10, 17 and 26. Every result
was unknown. This small pilot helps agents choose block sizes; it does not
rank mathematical solvability. Reproduce the three general experiments with:

```sh
python3 benchmark_blocks.py pilot --output pilot-reproduced.json
python3 benchmark_blocks.py benchmark --output benchmarks-reproduced.json
python3 benchmark_blocks.py deep --levels 12 --work 2000000 --macros 1000000 \
  --output deep-reproduced.json
```

AI-assisted implementation and validation by Codex. Existing mathematical
analyses remain credited above and in the earlier research notes.
