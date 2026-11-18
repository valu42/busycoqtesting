# Baseline and research provenance

The original pass on this outlook branch began on **2026-11-18** at [master 01b0a10](https://github.com/valu42/busycoqtesting/commit/01b0a10592b3bf843c0fd5bb1718625c65632830). The [original simulation table](https://github.com/valu42/busycoqtesting/blob/01b0a10592b3bf843c0fd5bb1718625c65632830/research/bb2x5/SIMULATION_TABLE.md) and [37-machine roster](../BB2x5_Rocq_holdouts_37.txt) define machine identity and order. [baseline.json](baseline.json) records the two SHA-256 hashes and every source endpoint, additional lower bound and external report at intake.

The earlier outlook, [680c696](https://github.com/valu42/busycoqtesting/commit/680c69635d58a26ad2d33814ac16df4f72a86975), began at [2ab106f](https://github.com/valu42/busycoqtesting/commit/2ab106f706cb1715d494c7f67464e9222092058f). Its machine reports, programs and checkpoints are inherited here. Their original dates and starting commits identify their provenance. The current table marks those contributions **I**. Reports below record where later evidence supersedes those experiments.

## Line 34 proof pass on 18 November

From [outlook c970885](https://github.com/valu42/busycoqtesting/commit/c970885c2e6dce20b0a712d310ba16982660e2f5), two finite certificates reduce blank nonhalting to a condition after digit 100. The spatial test allows any debt attained in the first eight suffix cells, and always permits zero or one. A separate test permits all streams bounded by two with doubles at least 42 sweeps apart. The blank run attained 135,652,670,312 instructions. The all-time source bound and the blank outcome remain open. [Proof, controls, and complete trace](cut100.md)

## Continuation on 18 November

This continuation starts from [outlook 6e9f4ea](https://github.com/valu42/busycoqtesting/commit/6e9f4ea27600c34026e8d1c4eb795a7b040a6d5f) and the then-current [master 04b5213](https://github.com/valu42/busycoqtesting/commit/04b52137b2de1784986655cb9014c486de4dfd22). The [claim board registration](https://github.com/valu42/busycoqtesting/commit/b5f832e10857b90a9d9f643407421e69f12832ac) separated the new work on 13, 33 and 34 from concurrent return investigations on 15 and 18. The outlook keeps a byte-identical [intake table](simulation-table-at-intake.txt) for offline checks. Other researchers can update the live simulation table. The generator checks the intake hash and matches every current line and string against the intake roster.

* **13.** A nonhalting execution must face infinitely many odd-cell parity tests. For cell 155 there is both a genuine blank checkpoint still awaiting the test and an absolute deadline for settling it. Later phases and their probabilities remain open. [Proof and trace](pair13.md) · [Clock by coordinate](timing13.md)
* **33.** An aligned terminal block protects every finite request batch on a shifted canonical register. The actual source determines when blocks are consumed. Two disjoint observed stretches each contain fewer losses than gains, and the proposed probabilistic interpretation needs assumptions about the state and penultimate trit. [Protection theorem](reserve33.md) · [Extension 41 and independent replay](compress33.md) · [Complete checkpoint](compress33-41.json) · [Model and its limits](reserve33-outlook.md)
* **34.** A fixed material cut must return to zero debt on an infinite run. The moving guard admits a 52-phase sufficient condition. An explicit altered family shadows the real guard for 2,989 sweeps before halting. The difference between a fixed material cut and the guard's moving position is central to the remaining proof. [Research summary](target34.md)

No blank-outcome classification changes in this continuation. Master’s newer checkpoints on lines 3, 18, 26 and 30 also appear as inherited evidence. The handoff included a [new line 26 raw clock](https://github.com/valu42/busycoqtesting/blob/53418ee1a3cb8cd316cdcb4e2617a4cd3f29de43/research/bb2x5/column-time.md), [first-visit data for 17](https://github.com/valu42/busycoqtesting/blob/91f5cde3f22ec17fd2dd7c895899fa2755449ee2/research/bb2x5/line17-edge-time.md), [a sharp synchronization bound for 35](https://github.com/valu42/busycoqtesting/blob/85ecc03c3e49bce92d2c5958dc398b7879b26429/research/bb2x5/line35-pascal.md#exact-waiting-time-for-a-neutral-center) and the [owner’s correction of the line 37 proof attribution](https://github.com/valu42/busycoqtesting/commit/126961c1be4d1bec9bfa8316d2a604068b297c9e). During handoff a concurrent [line 17 accelerator](https://github.com/valu42/busycoqtesting/commit/599a6640a7c0010c3b10e622bcd5c28d22ee3efe) on this same branch reached 10³⁰ sweeps and tightened the first-visit deadline to 2.871 × 10³³². Its two width extrapolations describe that overflow only. The linked machine reports distinguish checkable implications, numerical observations and the unresolved blank-reachability questions.

## Changes at the opening baseline

| Line | Evidence added since the earlier outlook |
| --- | --- |
| 13 | Seventy-seven odd cells have received their first A safely. At coordinate 155 only the leading B has arrived. [Exact trace and raw clock](../line13-edge.md) |
| 17 | Six times 10²⁸ normal sweeps give the current exact raw clock. The first +12 visit must precede 3.176 × 10³⁴⁴ raw steps. Two bits distinguish three possible returns. [Timed checkpoint](../frontiers/runs/line17-epochs.json) · [Bound and branches](../line17-edge-time.md) |
| 26 | The first possible halting width exceeds 173. The cut-84 timing proves survival through 377,503,392,604,154,203,337,765 raw steps. [Calculation](../column-phases.md#extension-through-cut-84) |
| 35 | Right-hand triples follow Pascal mod 2. A finite left graph proves that a halt requires debt of at least five beyond the first eight cells at some sweep. [Guard calculation](../line35-pascal.md) |
| 36 | The reference prefix and suffix potential protect every real sweep. Rocq formalizes the blank-start induction and the repository documents kernel replay. [Theorem and verification scope](../line36-rocq.md) |
| 37 | Line 37 remains open. The owner corrected the original proof attribution to line 36. The published criterion for 37 leaves an all-time bound to prove. [Owner clarification](https://github.com/valu42/busycoqtesting/commit/126961c1be4d1bec9bfa8316d2a604068b297c9e) · [Public argument](../line37-header.md) · [Merged PR](https://github.com/valu42/busycoqtesting/pull/4) |

We matched all 37 full strings against the [November 17 wiki revision](https://wiki.bbchallenge.org/w/index.php?title=BB(2,5)&oldid=10980). The domain page still lists both 36 and 37 among its historical holdouts. For line 36 the repository contains a later proof of the identical machine. For line 37 the table records the open fixed-cut bound. [Source audit](sources-audit.md)

## Verification repeated in this pass

The table checker verified 37 original line/string pairs, both baseline hashes, label spelling and report links. The original scoreboard agreed with its 37 run files. All 18 existing arithmetic and block-simulator unit tests passed. Re-running the fresh-cell controls below reproduced the inherited JSON byte-for-byte on lines 8, 11, 12 and 31. The line 35 Pascal checker reproduced the 355 literal eight-cell guard checks. The line 17 first-visit checker reproduced the pair-173 visit, and the Python edge bound reproduced the 81,526,541-slot deadline at cut 403. The stronger cut-95 raw clock quoted in the table is inherited. We inspected the line 36 theorem and reported verification scope without rebuilding its large kernel proof in this pass.

From `research/bb2x5` run:

```sh
python3 halting-outlook/update_table.py --check
python3 frontiers/scoreboard.py --check
python3 -m unittest test_arithmetic5 test_exact_blocks -q
python3 halting-outlook/remaining-stream-triggers.py
python3 line35_pascal.py
python3 frontiers/line17_visit.py check frontiers/runs/line17-first-173.json
python3 frontiers/line17_edge.py bound
```

## Additional results of this research pass

The table keeps the reviewed earlier outlooks for the open machines. On line 36, the later formal theorem changes the earlier table’s **Unknown** to **Proven nonhalting**. The following results narrow specific open questions.

| Line | New result |
| --- | --- |
| [6](probe6.md) | Exact literal floor 10,087,506,894. Reordering a real checkpoint preserves all factor counts through length seven but can produce A1. |
| [21, 22](target21_22.md) | Four possible input prefixes at a fresh parent cause the child's BB on 21. Only BAAAAA does so on 22. The sampled streams contain dangerous words at safe internal offsets. |
| [31](edge31.md) | Odd cells are permanently safe. Two input prefixes decide a halt at the even grandchild. The earliest open candidate coordinate is 142. |
| [33](neglected33.md) | A timed word recurrence reaches the 33rd left extension after about 6.00151 × 10^12573 raw instructions. A nested 21 that receives a B reply halts. An outer B return would enter a proven infinite family of sweeps. |
| [34](target34.md) | All 352 possible twelve-cell prefixes in the finite proof have nonnegative balance. A halt would require at least six units of debt from the remaining suffix on that sweep. Exact blank clock 33,919,375,494. |

The next proof target is **34**. Its unresolved claim is a single inequality on the actual tape at a fixed cut. The public branches and recent commits at intake included active work on 13, 17, 26 and 35–37. This pass used a separate research branch and left the simulation table intact. The search identifies public work only.

## Concurrent results checked at handoff

Master advanced to [12c4acd](https://github.com/valu42/busycoqtesting/blob/12c4acdce3310d435190895136f65826a702f1c8/research/bb2x5/ROADMAP.md) during this pass. Another agent published [nine targeted simulations](https://github.com/valu42/busycoqtesting/blob/f8aad726409eb538d288f079898ee56197ef794f/research/bb2x5/SIMULATION_TABLE.md). We matched both revisions against all 37 complete strings and inspected their checkpoint tables and derivations. Their new floors on 9, 14, 16, 17, 20, 24, 28 and 29 appear as inherited evidence. The stronger existing outlook bounds on 3 and 30 continue to take precedence. The table also incorporates the updated line 26 clock and independent line 36 kernel replay. The starting simulation table and its intake hashes remain pinned at 01b0a10. The master [research board](https://github.com/valu42/busycoqtesting/blob/master/research/bb2x5/ROADMAP.md) indexes this page and its open line 34 proof obligation.

## Historical intake at 2ab106f

The following sections describe the **earlier** outlook pass at 680c696. In these historical sections, “new”, “this pass” and the transcript results refer to that work. Current labels and bounds are in the [outlook table](../HALTING_OUTLOOK.md).

All 37 machines were unresolved in this repository at intake. No blank-tape
decision or new Rocq/Lean theorem is inherited from these research notes.
Exact integer simulation, finite exhaustive checking, informal mathematical
arguments, and community heuristics are different kinds of evidence.

The baseline includes much more than ordinary direct simulation:

* Lines 3–5 have counter reductions and exact arithmetic rules. Line 3 has a
  proved finite survival bound, line 4 has a million-return scalar computation,
  and line 5 has a timed 100,000-return checkpoint. Those are finite results.
* Lines 7 and 17 have exact suffix-call and register accelerators. The community
  suggests eventual halting for both; only line 17's accessible machine page
  supplies an explicit per-overflow probability model. The reports below audit
  what can be justified for the actual blank orbit.
* Lines 8, 10–13, 21, 22 and 31 have exact left response streams and saved raw
  clocks. Stream phase at fresh cells is part of the problem, not a free choice.
* Lines 2, 6, 26 and 34–37 have more specialized return, fixed-point or matching
  descriptions. The [remaining-machine report](remaining.md) records the
  individual questions for all machines outside the focused investigations.
* Lines 29 and 30 are the two known Hydra-family cryptids. Their community
  arithmetic heuristics must be evaluated separately from a finite local run.

Source attribution is attached to the machine-specific reports. Repository
material predating this pass is always **inherited**, even when this pass
reruns its checker. The [current source audit](sources-audit.md) matches community
entries by complete transition string, rather than list position or a similar
machine's name. Linked Discord pages that returned only a JavaScript shell
were not treated as inspected derivations. This is a documented source-access
limit, not evidence that their underlying results are false.

## Floor convention used in the historical pass

The earlier table favored an exact repository endpoint or mathematically justified
repository bound. `I` marks inherited evidence, `N` marks this pass, and `E`
marks a community-reported run not independently reproduced here. External
reports are kept visibly separate in the evidence cells/reports.

An abbreviated exact endpoint is not rounded into a new strict inequality:
`≈ 5.69 × 10^3872` denotes the exact integer in its linked record. It means
the computation survives through that exact integer, not through every number
rounding to that display. A displayed `≥` or `>` is an actual lower-bound
claim. No undefined transition is counted as a defined raw instruction.

Particularly easy mistakes are avoided here: line 4's millionth-return bound
is much larger than its separately timed 1,024th return; line 5's recurrence
event count is not its raw clock; line 17's epoch count is not its raw clock;
and line 37's bound sums necessary traversals rather than claiming an exact
total duration. Every baseline floor can be traced to [baseline.json](baseline.json)
and then the original source. A checksum verifies record integrity, not
mathematical correctness or reachability from blank.

## Investigations inherited from 680c696

The individual reports distinguish established arguments, experimental
observations, conjectures, and missing assumptions. They address the halting
opportunity, its exact local condition, blank reachability, restrictions,
probabilistic assumptions, and raw timing. See:

* [Arithmetic lines 3–5](arithmetic.md).
* [Line 7: exceptional returns](line7.md).
* [Line 17: the next overflow and its heuristic](line17.md).
* [Lines 13, 21 and 22: actual generated streams](streams.md).
* [Hydra and Bonus Cryptid](hydra.md).
* [All remaining machines and fresh-cell tests](remaining.md).

Auxiliary starting tapes are positive or negative controls, never evidence
of their reachability from blank. A local rule tested on finitely many inputs
is labeled accordingly unless a general derivation is supplied. An allowed
path in an enlarged stream model is not an actual execution. None of the new
computations has been checked by a proof-assistant kernel.

## Classification decisions in the earlier pass

No blank-tape halting status was resolved. The earlier outlook contained **32
Unknown, two Possible halting, one Probable halting, and two Probable
nonhalting** rows. These labels assess evidence; they do not change the formal
37-machine holdout roster.

* **Line 7:** use Possible halting rather than adopting the community's stronger
  expectation. Exact guard filters show why abundant internal tests are not
  independent chances to halt; outer and residual tests remain uncalibrated.
* **Line 13:** retain Possible halting. Its newly derived positive-even-B-run
  trigger sharpens the question, without proving that blank reaches it.
* **Line 17:** retain the inherited Probable halting heuristic with explicit
  reset-mixing assumptions. The new bound puts its next overflow before
  `10^405` raw steps, but does not put halting before that bound.
* **Lines 29/30:** include the accessible positive-drift heuristic as Probable
  nonhalting. This adds an outlook to the old finite-simulation “Unknown” label;
  it is not a new nonhalting theorem. The new timed Hydra replay survives beyond
  `10^7045` instructions.
* **Lines 3 and 26:** keep Unknown despite external directional suggestions.
  Line 3's external probabilistic approximation is explicitly invalidated by
  its own source; line 26's original heuristic could not be audited. Line 3 now
  has a new exact clock and survival beyond `10^287` instructions.

Other substantive additions are the line-5 inverse exclusion of 20,000 specific
target exponents, exact fresh-cell triggers on lines 8/11/12/31, and phased
stream/correlation studies plus extended endpoints on lines 21/22. All changes
to a floor are finite survival results. No raw stopping-time percentile was
invented from these large endpoints.

Independent cross-reviews checked the line-3 timing/no-hidden-halt argument,
the line-17 slot and raw-cost upper bound, and the stream-trigger/phase/timing
arguments. The lead pass additionally replayed the complete new Hydra result
and obtained byte-identical JSON. These reviews and literal comparisons do not
constitute formal verification.

The most concrete next investigations are the actual suspended return word at
line 17's next overflow, line 13's initial-B parity invariant, the true fresh
phases on lines 21/22, and an inverse-reachability search for line 5. Each report
specifies a reproducible starting point and the exact missing implication.

## Reproduction and consistency checks

Python 3.10+ and the standard library suffice for Python checks. Native
experiments specify compiler and GMP requirements in their reports. Run from
`research/bb2x5` unless a report says otherwise:

```sh
python3 frontiers/scoreboard.py --check
python3 -m unittest test_arithmetic5 test_exact_blocks -v
python3 halting-outlook/update_table.py --check
```

The first command checks all inherited table rows against indexed runs,
including machine identity and raw-clock records. In the earlier pass the second command passed all 18
test groups, including complete-configuration comparisons of block simulation
against literal execution on all 37 machines and arithmetic halting controls.
The transcript is [baseline-tests.txt](baseline-tests.txt).

The earlier pass also reran the moving-window test independently:

```sh
c++ -O3 -std=c++17 frontiers/window.cpp -o /path/to/bb25-window
BB25_WINDOW=/path/to/bb25-window python3 frontiers/test_window.py
```

Its transcript is [baseline-window-tests.txt](baseline-window-tests.txt).
New experiment validation and retained checkpoints are linked from each report.
The final table checker enforces the exact original 37 strings in order,
unchanged baseline hashes, valid outlook labels, and existing report anchors.
`rows.json` is the reviewed table data; `update_table.py` renders it and never
infers a research classification from a runtime.
