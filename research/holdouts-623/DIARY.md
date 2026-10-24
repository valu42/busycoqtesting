# BB6 research diary

This diary records ongoing research in the owner's copy of busycoq. It contains method notes and aggregate status; input attachments and detailed run data are not included.

## 2026-10-24 — First research pass

**Outcome: no new complete classification or equivalence proof.** No classification PR was opened.

Reviewed the proof styles in the upstream BB6 branch and audited existing upstream and owner PRs before selecting candidates. Existing work was excluded from new-result claims. Useful references include [upstream PR #38](https://github.com/ccz181078/busycoq/pull/38), [upstream PR #39](https://github.com/ccz181078/busycoq/pull/39), and [the owner's existing proof PR](https://github.com/valu42/busycoqtesting/pull/1).

Approaches explored:

- Local simulation equivalences, state renaming and reflection.
- Finite-window and finite-automaton invariants.
- Convergence of blank runs with a common transition table.
- Extensions of the repository's counter and chaotic-bell acceleration rules.

Some local rule extensions compiled in Coq 8.20.1 and passed a separate kernel check. These are partial lemmas, not resolutions of new blank runs. Long exploratory executions did not produce a complete certificate. A proposed extension that failed a transition lemma was rejected rather than used as evidence.

## 2026-10-24 — Second research pass

The initial direction was to seek a common process after grouping tape cells into blocks. The experiment computed finite block-exit behavior, refines state and symbol partitions, and compares the resulting transition graphs. Any matching graph would still require an explicit isomorphism and a Rocq proof connecting both machines to that process.

Individual counter examples were also studied through their short tape transformations. The aim is to derive a closed invariant or recurrence instead of increasing the previous simulation budgets.

## 2026-10-24 — Block search and individual return maps

The block-process comparison finished through block width 6, including offsets and reflection. It produced no candidate equivalences. This is a bounded search result, not a proof of inequivalence.

The individual analysis now includes a Bell-like return map. Six general local tape-transformation lemmas compile in Coq 8.20.1 (Rocq's former name) and pass a separate `coqchk` kernel check. `Print Assumptions` reports each as closed under the global context. These lemmas concern finite progress between parameterized configurations; none establishes nonhalting from the blank tape.

The main obstacle is the exceptional transition that creates another stored block. Several proposed global invariants were rejected by explicit counterexamples. In particular, a sufficiently large leading counter does not make every finite suffix safe. Accelerated exploration helps identify the missing cases, but is not being counted as a classification certificate.

The upstream PR audit was refreshed. No new complete classification or equivalence has been obtained, and no new-result PR has been opened. A subsequent literature check changes the priority of this candidate; see below.

## 2026-10-24 — Literature correction and partial proof checkpoint

The candidate is a starting-state variant of a family whose [public analysis](https://wiki.bbchallenge.org/wiki/1RB1RD_1LC0LE_1RA0LB_1RA1RF_0RA0RC_1RE---) describes very rare halting paths. A [pre-existing Lean proof by -d](https://github.com/int-y1/proofs/blob/1929f57df4dd7afcc11c3f458e20526fd1f991e0/BusyLean/Individual/1RB0RE_1LC0RA_1LA1LD_1LC1LF_0LC0LB_1LE---.lean) establishes halting from a parameterized family of configurations for a related start. Reaching that family from the relevant blank start remains the difficult part. This makes attempts to prove nonhalting from a simple tape-language invariant a lower priority. The earlier "could be solvable" annotation was insufficient for candidate selection.

[ResearchBellFrontier.v](../../verify/ResearchBellFrontier.v) preserves the six checked local lemmas for the publicly documented table. It contains no blank-run halting, nonhalting, or equivalence theorem. The statements quantify over arbitrary untouched tape tails and repetition counts. They were verified using Coq 8.20.1 with native compilation disabled; each assumption report is closed under the global context.

After building the usual BusyCoq dependencies, from the repository root:

```sh
coqc -native-compiler no -Q verify BusyCoq verify/ResearchBellFrontier.v
coqchk -silent -bytecode-compiler yes -Q verify BusyCoq BusyCoq.ResearchBellFrontier
```

The module is a reproducible research checkpoint. No novelty or solved-holdout claim is made for these local transformations.

## 2026-10-24 — Counter phase acceleration and broader decider searches

**Outcome: two additional general phase transformations are proved; no new complete holdout classification or equivalence.**

[ResearchCounterBatch.v](../../verify/ResearchCounterBatch.v) contains a generalized version of the existing `P0_n` rule from [CounterClass3v1.v](../../verify/CounterClass3v1.v), two whole-phase rules (`frontier` and `back_sweep`), and a strict-progress corollary for a nonempty forward phase. All four theorems quantify over an arbitrary D0 transition and arbitrary untouched tape tails. The phases avoid D0, which lets the same acceleration apply to multiple variants. The original core induction and BusyCoq execution/shift tactics remain credited to the repository authors.

The forward rule replaces a whole counter phase by a repeated three-cell output block. The backward rule consumes repeated left-hand blocks and transfers their counts into two right-hand blocks. Neither establishes an invariant covering every configuration of a blank run. All four statements compile in Coq 8.20.1, pass an independent `coqchk`, and report `Closed under the global context` with `Print Assumptions`.

```sh
coqc -native-compiler no -Q verify BusyCoq verify/ResearchCounterBatch.v
coqchk -silent -bytecode-compiler yes -Q verify BusyCoq BusyCoq.ResearchCounterBatch
```

Exploratory implementation and measurements:

- A native simulator first applied the core counter rule and constant-symbol sweeps. Three related starts each reached 100 million accelerated iterations without a halt.
- Packing runs of three-cell words reduced a representative tape from more than two million stored runs to a few dozen. Each start then reached one billion iterations with the original acceleration schedule.
- The two new phase rules skip entire phases, so their iteration counts are not comparable to the earlier schedule. Small-case comparisons against ordinary simulation passed 912 macro cases. An independent Python implementation using unbounded integers matched the complete native configuration after one million iterations on one start.
- With the new schedule, all three starts completed at least 20 million iterations without a halt. The largest recorded counter used 74 bits. These are exploratory executions, not Rocq-certified lower bounds on blank-run runtime; the simulator itself has not been verified.
- For two starts with a common transition table, a further orbit comparison sampled 470,280 frontier configurations across ten million iterations per start. It found no shared configuration hash. This supplies no proof of inequivalence.

The automatic search also broadened beyond the earlier checks:

- A run-length/block decider sweep tested all 623 inputs at widths 3, 4, 5, 6, 8, 10, 12, and 16: 4,984 bounded runs, no certificate. Transition memoization helped some benchmarks and slowed others, so the small-block runs retained the uncached implementation.
- Native extraction of the repository's `RWL_mod_FAR`, `CPS_LRU_FAR`, and `RNGS_mod_QSym_FAR` deciders was checked against 29 existing positive examples. Across three searches, 85,153 bounded attempts produced no certificate. The largest parameter sweep included reflection and completed 102 full parameter/orientation settings over all 623 inputs before its budget was stopped; a separate larger-budget sweep had 1,103 timeouts. These counts include overlapping settings.
- A targeted follow-up on the 88 informally unknown inputs tried block widths 7, 9, and 11, allowing up to 20 million iterations and two seconds per run. All 264 runs reached their time limit without a certificate.
- An attempt to prove equivalence by avoiding the single differing transition was abandoned: all 176 candidate pairs actually reached that transition within the tested prefix. This only rejects that particular strategy.

The upstream open-PR audit was refreshed: #39 remains a result to exclude from duplicate claims; #3 and #4 concern assumption audits. No complete result PR was opened. The counter rules above are a partial proof checkpoint in this owner's repository.

The next useful counter work is to characterize the remaining nested tape patterns and derive a closed recurrence or invariant. Further simulation alone would not establish nonhalting.

## 2026-10-24 — Fourth pass: return rules, falsification, and induction search

**Outcome: thirteen further local theorems checked; no new complete holdout classification or equivalence.**

[ResearchCounterRecurrence.v](../../verify/ResearchCounterRecurrence.v) complements the previous phase rules. It adds five general positive-progress rules and a general halting-pattern rule, two D0-specific return rules, three bridges from blank starting configurations, and two checked counterexamples. The general rules preserve arbitrary untouched tape tails and allow an arbitrary D0 transition. The specialized rules cover the `1LF` and `1LB` choices for D0.

For the `1LF` choice, the bridges include blank A to an A/0 configuration with one right-hand block of four ones, and blank F to A/0 with blocks of lengths 12 and 5 separated by a zero. These are entry points for a future invariant; they do not establish one.

The counterexamples explain why two tempting arguments cannot be used:

- A/0 on a blank left side with right-hand blocks of lengths 2 and 2 halts, regardless of the untouched suffix after the next separator. Merely requiring positive or at-least-two block sizes does not prove nonhalting.
- A/0 with one block of length 19 returns to A/0 with block lengths 7, 15, and 5. Consequently, decreasing block lengths are not preserved at every such return. Weaker order conditions, including a separate leading marker case, also failed exploratory checks.

All thirteen statements compile in Coq 8.20.1, pass a separate `coqchk`, and report `Closed under the global context`. No `Admitted`, new axiom, native-computation axiom, blank-run classification, or explicit raw-step bound is introduced. After building the normal dependencies and `ResearchCounterBatch.v`:

```sh
coqc -native-compiler no -Q verify BusyCoq verify/ResearchCounterRecurrence.v
coqchk -silent -bytecode-compiler yes -Q verify BusyCoq BusyCoq.ResearchCounterRecurrence
```

The exploratory simulator now uses these return rules as well as the earlier batches. New-rule comparisons against ordinary execution passed 9,931 applicable cases, in addition to the earlier 912 batch cases. Independent native and unbounded-integer Python implementations matched their complete configurations after 100,000 iterations on one start. A scheduling experiment also found that applying a short return rule too early could bypass a much stronger P0 batch; the final schedule preserves that opportunity.

The companion [counter_explore.py](counter_explore.py) makes this exploration reproducible without any input attachment. It contains the public parameterized table, a small-case `--selftest`, time/iteration budgets, and JSON checkpoint/resume support. Its standalone return-rule self-test passed 990 applicable cases. It is deliberately labeled as an unverified explorer, not a certificate generator.

With the revised schedule and unbounded integers, all three counter starts completed 50 million accelerated iterations without a halt. Each run took about two minutes; the largest sampled stored run counts used 81–84 bits. These iteration counts are specific to the revised schedule. The simulator is exploratory, and these measurements are not Rocq-certified runtime bounds or nonhalting proofs.

Other directions were deliberately tested rather than repeatedly increasing the same decider budgets:

- Extracted the repository's inductive decider, including arithmetic-sequence and exponential-loop configurations. An existing positive example succeeded. A targeted grid of 84 bounded runs over 28 candidates produced 54 unknown results and 30 timeouts, with no certificate.
- Tried adapting individual proofs for one Skelet-class candidate and two cubic candidates. Necessary transition lemmas failed, so none of those adaptations was accepted.
- Revisited pairs whose observed executions rejoin after their differing transition. A common-model attempt exposed an uncovered three-one pattern. Backward searches for the required guards on 14 pairs, both directly and with pattern subsumption, exhausted their budgets without a certificate. Observed rejoining is not being promoted to equivalence.

The upstream open-PR audit was refreshed again. Upstream #39 remains excluded from new-result claims; #3 and #4 concern assumption audits. This checkpoint updates only the owner's research PR.

The next mathematical task is to characterize the nested counter tape language strongly enough to prove closure and continued progress, or to derive a shared process for a pair with all exceptional cases covered. The checked counterexamples rule out using a simple sorted-block condition as that invariant.

## 2026-10-24 — Fifth pass: total fractal recurrence and modular automata

**Outcome: a complete halting reduction to a word recurrence and general block-transfer rules; no new blank-run classification.** These directions differ from the counter extensions, local-window automata, and block-equivalence searches in the earlier passes. No priority claim over other researchers' work is intended.

The individual target is the public chaotic-fractal table
`1RB1LE_0RC1RC_0RD0RB_1RE0RF_1LA0LE_---1RB`
(entry 7 in the supplied 623-machine ordering).
[ResearchFractalSweep.v](../../verify/ResearchFractalSweep.v) defines one complete right-and-left sweep on **every** pair of finite binary words. Missing cells are zero, words are nearest-cell first, and the right word includes the scanned cell. The right scan consumes a prefix code; the left scan consumes its finite left word. Both functions terminate structurally, without a simulation budget or an assumed tape grammar.

`turn_spec` proves that every successful recurrence step makes positive TM progress, and every failed step reaches a halt. `halts_iff_turns` proves the two-way halting equivalence for any finite starting pair. `blank_halts_iff_turns` includes the blank-start bridge to `([1], [])`. This covers all exceptional patterns and the finite-word boundaries; the remaining problem is to classify the orbit of that initial pair.

[ResearchFractalTransfer.v](../../verify/ResearchFractalTransfer.v) supplies an arithmetic acceleration inside that recurrence. At B, for a left run of length A following a zero and a right prefix `10 1^(2B) 0 1^(2C) 00 1^M`, one transfer changes the four run lengths by

```text
(A, 2B, 2C, M) -> (A+2, 2B-2, 2C+2, M-2),  A >= 1, B >= 1, M >= 2.
```

The theorem preserves arbitrary untouched tails. `transfers` proves arbitrary repetition, and `reset` covers a boundary case when the first right-hand run is exhausted. These do not yet form a closed invariant for the blank orbit.

Two checked counterexamples narrow the next invariant search:

- Starting at B with left word `1` and right word `10011` halts. The first sweep produces right word `1011001`, so excluding isolated ones after the leading cell is not preserved.
- The analogous transfer-family configuration with left word `1` and right word `1011010011` halts. Its middle run is odd; the block layout alone is insufficient as a nonhalting invariant.

The sweep and transfer statements compile with Coq 8.20.1, pass a separate `coqchk`, and report closed assumptions. No axiom or admitted proof was introduced. After building the usual dependencies, from the repository root:

```sh
coqc -native-compiler no -Q verify BusyCoq verify/ResearchFractalSweep.v
coqc -native-compiler no -Q verify BusyCoq verify/ResearchFractalTransfer.v
coqchk -silent -bytecode-compiler yes -Q verify BusyCoq BusyCoq.ResearchFractalSweep BusyCoq.ResearchFractalTransfer
```

[fractal_sweep.py](fractal_sweep.py) implements the recurrence and optional transfers with unbounded integers. It is explicitly unverified. Its independent coordinate-tape interpreter checked 6,096 sweep cases and 448 batch cases, comparing the entire tape and state. A split 500+500-iteration checkpoint run matched an uninterrupted 1,000-iteration run. A 25-second exploratory run completed 145,239 calls, including 73 batches, with no halt; the final left/right words used 127,803/237,971 bits. Calls mix sweeps and batches and are **not** raw-step counts or certified runtime bounds. Time and space budgets are checked between calls.

```sh
python3 research/holdouts-623/fractal_sweep.py --selftest
python3 research/holdouts-623/fractal_sweep.py --iterations 1000000 --seconds 25 --max-bits 1000000 --output /path/to/checkpoint.json
python3 research/holdouts-623/fractal_sweep.py --resume /path/to/checkpoint.json --seconds 25
```

The second direction changes the information retained by the existing FAR procedure. [ResearchAlgebraicFAR.v](../../verify/ResearchAlgebraicFAR.v) records a polynomial residue of the entire scanned word together with a short suffix. A bit `b` updates the residue to `(multiplier * residue + b) mod modulus`, and shifts `b` into the suffix. This can distinguish words with the same recent suffix but different earlier contents. The arbitrary-generator soundness theorem comes from the existing FAR engine; no numerical interpretation of the TM tape is assumed.

The bounded grid used moduli `{3,5,7,11,31,127}`, distinct multipliers `{1,2,modulus-1}`, and suffix widths `{0,4,8}`. There are 51 distinct settings. Each used both orientations of all 623 inputs, capacity 8,192, event budgets 100,000, and 0.10 seconds per case: **63,546 attempts, 61,641 unknown results, 1,905 timeouts, zero positive candidates**. The grid used four worker processes; timeout counts depend on the host and scheduling. Separate controls (two nonhalting and two halting machines, both orientations) returned the expected four positives and four unknowns. A pilot at modulus 3, multiplier 2, suffix width 3 also returned no candidate in 1,246 attempts; it is excluded from the grid total.

The new wrapper introduces no axiom, but **its soundness theorem does not have closed assumptions**: it inherits FAR's primitive integer/array specifications and `LibTactics.inj_pair2`. This is separate from the closed fractal proofs above. Native extraction is used only for candidate search; any future positive must be replayed inside Coq and its assumptions audited before claiming a result.

The extraction entry point and native driver are included. With the usual Coq/OCaml dependencies installed, from `verify/`:

```sh
coqc -native-compiler no -Q . BusyCoq ResearchAlgebraicFAR.v
coqchk -silent -bytecode-compiler yes -Q . BusyCoq BusyCoq.ResearchAlgebraicFAR
coqc -native-compiler no -Q . BusyCoq ../research/holdouts-623/ExtractAlgebraicFAR.v
ocamlfind ocamlopt -w -a -O2 -package coq-core.kernel,unix -linkpkg algebraic_far.mli algebraic_far.ml ../research/holdouts-623/algebraic_far_driver.ml -o algebraic_far
```

The driver accepts `INPUT MODULUS MULTIPLIER SUFFIX_BITS EVENTS SECONDS`, checks both orientations, and prints JSON summaries. The following reproduces the grid's parameter set; the input file remains external:

```sh
python3 - ./algebraic_far /path/to/BB6_holdouts_623.txt <<'PY'
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
jobs = [(p, m, k) for p in (3, 5, 7, 11, 31, 127)
        for m in sorted({1, 2, p-1}) for k in (0, 4, 8)]
def run(job):
    return subprocess.run([sys.argv[1], sys.argv[2], *map(str, job), '100000', '0.10'],
                          check=True, text=True, capture_output=True).stdout
with ThreadPoolExecutor(max_workers=4) as pool:
    for result in pool.map(run, jobs):
        print(result, end='')
PY
```

The upstream open-PR audit was refreshed: #39 remains excluded from new-result claims; #3 and #4 concern assumptions. The next focused mathematical task is a recursive description of the reachable words at reset boundaries, proved closed under the total recurrence. Merely extending the simulation or dropping parity guards would not settle it.

## Proof status

No new complete blank-run halting/nonhalting classification, machine-to-machine equivalence, or explicit raw-step bound has been established in this work. The fractal machine's halting equivalence to its total recurrence is proved; classification of the initial recurrence orbit remains open. Search failures are not proofs of nonhalting or inequivalence.

A result will be submitted only after the exact theorem is checked by Rocq and the current PRs are checked again for duplication. Research and proof PRs from this work target this repository, not upstream.

This is AI-assisted research by Codex. Existing proof methods remain credited to their upstream authors.

