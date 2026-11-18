# Baseline, scope and evidence policy

Research pass: **2026-11-18**. Starting commit:
[`2ab106f706cb1715d494c7f67464e9222092058f`](https://github.com/valu42/busycoqtesting/commit/2ab106f706cb1715d494c7f67464e9222092058f).
The commit was read through the GitHub connector and independently matched by
the checkout. The untouched [original table](../SIMULATION_TABLE.md) and
[37-string list](../BB2x5_Rocq_holdouts_37.txt) define membership and order.
The machine list SHA-256 is
`89ea92fd4643166b92fca4ae80e37a699ab8615ac1dd375dae777e6b3e45ecc6`.
[baseline.json](baseline.json) freezes every original endpoint, extra bound,
external report and source, together with both file hashes. There are exactly
37 rows in the [new outlook table](../HALTING_OUTLOOK.md).

## Stage 1: inherited findings

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

## Reading the floor column

The table favors an exact repository endpoint or mathematically justified
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

## Stage 2: new investigations

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

## Classification decisions and strongest additions

No blank-tape halting status was resolved. The final outlook contains **32
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
including machine identity and raw-clock records. The second passed all 18
test groups, including complete-configuration comparisons of block simulation
against literal execution on all 37 machines and arithmetic halting controls.
The transcript is [baseline-tests.txt](baseline-tests.txt).

The moving-window test was also rerun independently:

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
