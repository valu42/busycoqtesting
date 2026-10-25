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

## 2026-10-25 — Sixth pass: symbolic frontiers, different starts, and invariant synthesis

**Outcome: 22 more checked statements and three reproducible search tools; no new complete blank-run classification.** The new directions were symbolic input exploration, synthesis of both side automata, and memoization across recursively nested tape blocks. These are additions to this research branch, not claims that the methods are new to the literature.

### Monotone-list frontier and falsification

The individual target is entry 144,
`1RB0LE_0RC---_1RD0LA_1RE0RA_1LC0LF_0RC1LC`.
At a frontier, the head is in B with an entirely blank right side; the finite left word is written nearest-cell first.
[ResearchMonotoneFrontier.v](../../verify/ResearchMonotoneFrontier.v) contains 13 statements: entry and local scanning rules, two general frontier returns, a further concrete return, two blank-state bridges, and a checked halting counterexample with its word property. The general rules preserve arbitrary untouched tails. In particular, `root_fours` covers an arbitrary repetition count, not a fixed simulation prefix.

An initially plausible grammar forbade adjacent zeros in the finite word. Ordinary exploration returned safely on every word below `2^20` and on 10,000 sampled 256-bit words. This was misleading: [monotone_frontier.py](monotone_frontier.py) found a halting word after exploring 58,900 symbolic work states:

```text
11111101011010110111111011
```

This is the 26-bit nearest-first word `0x37ed6bf`. The independent coordinate-tape replay halts after 434 transitions. Coq proves both that the finite word has no adjacent zeros and that the corresponding B/frontier configuration halts; **the exact count 434 is an explorer measurement, not a separate Coq runtime theorem**. This is not a configuration claimed reachable from the blank A start.

The symbolic search assigns a bit only when execution first reaches unread input, and merges equal control/work-word/grammar states. It avoids enumerating all complete words of a given length. Every reported counterexample is completed to a finite admissible word and independently replayed. A bounded search that finds nothing still reports unknown.

A stricter hypothesis bounded the leading one-run by five, allowed interior one-runs congruent to 1 or 2 modulo four, capped the number of the latter, and constrained the final run after the head to residue 0 or 1. Closure fails immediately: `11111` returns to `11010111101`, which contains an interior run of four. `five_ones_return` checks this transition in Coq. Separate halting searches with marker caps 0, 1, and 2 each exhausted 500,000 symbolic states without a halt; they do not repair the failed closure condition.

```sh
python3 research/holdouts-623/monotone_frontier.py --selftest
python3 research/holdouts-623/monotone_frontier.py --seconds 30
python3 research/holdouts-623/monotone_frontier.py --grammar residues --check-closure
```

### Common programs with distinct blank starts

Ignoring the initial-state label reveals two useful pairs. [ResearchStartVariants.v](../../verify/ResearchStartVariants.v) checks both directions of each reflected state map and records the actual different initial configurations:

| Supplied entry | Shared program | Blank start reduces to |
| --- | --- | --- |
| 7 | `FractalSweep.tm` | recurrence pair `([1], [])`, proved in the previous pass |
| 549 | `FractalSweep.tm` | recurrence pair `([1], [1])` |
| 144 | `MonotoneFrontier.tm` | B/frontier left word `1` |
| 321 | `MonotoneFrontier.tm` | B/frontier left word `101` |

The new file contains nine statements. Both halting reductions are two-way. They **do not** assert that the two blank runs in a pair have the same outcome. The proofs check the inverse state map directly, avoiding the functional-extensionality dependency of the general double-reflection lemma. All nine report closed assumptions.

An exploratory comparison of the first 100,000 unbatched recurrence pairs from each fractal start found no shared configuration hash. This is neither an inequivalence proof nor a classification. The explorer now accepts `--start E`; checkpoints record the start, retain compatibility with old A checkpoints, and reject an explicitly mismatched start. A split 500+500-call E run matched an uninterrupted 1,000-call run.

```sh
python3 research/holdouts-623/fractal_sweep.py --start E --iterations 100000 --seconds 30 --max-bits 1000000 --output /path/to/twin.json
python3 research/holdouts-623/fractal_sweep.py --resume /path/to/twin.json --seconds 30
```

A wider transition-graph comparison also allowed the initial state to move. It compared 240,489 distinct tables appearing in non-research proof sources, finding 935 matching occurrences across 363 supplied inputs. Most were in equivalence catalogues; a table occurrence is not a blank-run theorem. No existing classification was transferred merely from this graph match. The monotone entries 116/375/387 form another common-program group with different starts.

### Synthesizing both side automata

[synthesize_invariant.py](synthesize_invariant.py) uses Z3 to choose both DFA transition tables and an allowed relation on `(left state, TM state, scanned bit, right state)`. Both automata read from blank infinity toward the head and loop at state zero on zero. Constraints include the blank start, forbid all halting configurations, and require closure under every possible predecessor when popping a side. This searches transition tables directly instead of choosing a residue or suffix generator in advance.

The selection was the 88 inputs labelled Unknown in the working taxonomy plus the ten fractal/monotone targets, giving 98 distinct machines. A four-worker grid tried:

- sizes `(4,4)`, `(2,8)`, `(8,2)` with two solver seconds each: 294 UNSAT results;
- sizes `(8,8)`, `(16,4)`, `(4,16)` with five solver seconds each: 115 UNSAT and 179 timeout/unknown results.

Thus **588 bounded attempts produced no candidate**. UNSAT is only a result for the stated finite template and sizes, not evidence that a machine halts. Two nonhalting and two halting controls produced the expected SAT/SAT/UNSAT/UNSAT results. For SAT, an independent Python least-fixed-point traversal checks the proposed DFA tables without using the solver's allowed relation. This is still unverified code: any positive on a holdout requires Coq replay before acceptance.

Install `z3-solver` in an isolated environment (tested version 5.3.1.0), then for example:

```sh
python3 research/holdouts-623/synthesize_invariant.py --selftest
python3 research/holdouts-623/synthesize_invariant.py --input /path/to/BB6_holdouts_623.txt --index 144 --left 8 --right 8 --seconds 5
```

A separate exploratory generator that tracked run residues and a capped number of exceptional runs was tested with the existing FAR engine: 108 bounded orientation/settings attempts on entries 7/144/321, all unknown. No certificate was obtained.

### Recursively memoized blocks

[hierarchical_sim.py](hierarchical_sim.py) stores binary tape blocks in shared binary trees and caches execution from a block boundary until exit or halt. Parent calls compose child calls; a repeated complete configuration inside a finite block produces a cycle candidate. This differs from comparing fixed-width block transition graphs: it reuses execution at every represented block size. It is an unverified simulator, not a proof checker.

Validation compared 13,416 finite-block cases with ordinary execution, including 168 cycles, and checked 276 complete global snapshots while crossing block boundaries and expanding into blank space. The default ten fractal/monotone targets were tried at levels 8 and 16. All 20 runs stopped at budgets. At level 16, with 800,000 cache misses allowed, the last completed snapshot for entry 7 represented 187,774,600,009 simulated raw steps; entry 549 represented 178,044,727,628. These are unverified execution counts, not certified bounds or nonhalting evidence. Interrupted inner calls contribute no count to the reported completed snapshot.

Another 88 runs on the Unknown selection used level 10, a 300,000-cache-miss limit, a billion top-level calls, and ten seconds each, with two worker processes. All were unknown: 64 hit the entry limit and 24 the time limit. No halt or cycle candidate was found. Timeouts depend on host load.

```sh
python3 research/holdouts-623/hierarchical_sim.py /path/to/BB6_holdouts_623.txt --selftest
python3 research/holdouts-623/hierarchical_sim.py /path/to/BB6_holdouts_623.txt --level 16 --entries 800000 --blocks 1000000000 --seconds 20
```

The 22 new statements compile in Coq 8.20.1 with native compilation disabled and pass a separate `coqchk`. All 22 assumption reports are closed. No axiom or admitted proof was added:

```sh
coqc -native-compiler no -Q verify BusyCoq verify/ResearchMonotoneFrontier.v
coqc -native-compiler no -Q verify BusyCoq verify/ResearchStartVariants.v
coqchk -silent -bytecode-compiler yes -Q verify BusyCoq BusyCoq.ResearchMonotoneFrontier BusyCoq.ResearchStartVariants
```

The upstream and owner open-PR audits were refreshed. Upstream #39 and owner #1 remain excluded from new-result claims; upstream #3/#4 concern assumptions. The useful remaining mathematical task is a reachable-word invariant stronger than the rejected grammars, or a terminating recurrence analysis. None of the negative bounded searches supplies that missing argument.

## 2026-10-25 — Seventh pass: accelerated search on Cubic Mess

The focused target is supplied entry 26, `1RB1LC_1LC1RD_1LA0LB_0RB1RE_1RF0RA_---0RC`, a potentially probviously halting machine. [CUBIC26.md](CUBIC26.md) gives the derivation, source attribution, commands, exact proof scope, and benchmark data.

Racheline's published two-counter rules were independently checked in Coq, including every exceptional case on the invariant domain `a>=1, b>=2, a+b>=11`. `ResearchCubic26.v` proves a two-way reduction from blank-run halting to termination of that recurrence. `ResearchCubic26Jump.v` proves an abstract guarded-doubling composition theorem, the correction bounds, the ideal modular residue, and the four-state parity update. The 15 printed assumption reports are closed, and both files pass independent kernel checking. These are recurrence and arithmetic theorems, not a certification of the native executable.

The new [cubic26_accel.cpp](cubic26_accel.cpp) predicts a block of regular branches by doubling modulo the original counter sum, then applies a precomputed affine correction. A two-sided margin guard excludes every exceptional/halting branch inside an accepted block; a rejected guard falls back to one ordinary recurrence iteration. It runs **13.05 times faster** than the compiled scalar recurrence over the first billion iterations on this host. This is a constant-factor gain, not the requested exponential shortcut. Larger tables, composed byte tables, and reciprocal approximations were also tried and were slower.

The search reached **4,000,000,000,000 recurrence iterations**, ending at `(7354046713435,6645952891241)` without halting, in 2348.694 cumulative simulation seconds. This is five times the `8e11` recurrence iterations reported on the checked wiki page, not a claim about all previous simulations. [cubic26.checkpoint](cubic26.checkpoint) preserves that native state for continuation; [cubic26_results.json](cubic26_results.json) records the milestones and checks. Counts are not raw TM steps or certified bounds.

Validation includes 2,806 ordinary-TM configuration comparisons, 12,030,650 accepted jumps compared with scalar execution, a million-round Python comparison, cross-width checkpoint/resume checks, terminal and integer-limit controls, and the full suite under the undefined-behavior sanitizer. The checkpoint was reloaded without advancing and retained the exact final counters.

## 2026-10-25 — Eighth pass: avoid copying growing binary counters

The refreshed upstream audit found [PR #40](https://github.com/ccz181078/busycoq/pull/40), which supplies a complete reset-round map for the SOC25 family. Its pinned main source was compiled and kernel-checked independently; its eight `eqv_F` statements and `F_G` report closed assumptions. These are the upstream author's results. The separate wrappers involving `Eqv_v3` were not part of this audit, and no upstream proof source was copied into this branch.

This suggested an additional representation-based acceleration. [soc25_deque.cpp](soc25_deque.cpp) stores the binary counter in a deque of machine words with a moving low-bit origin. Consuming low blocks leaves the remaining words in place. The auxiliary counter is kept as signed powers of two, so only the necessary carry and borrow regions are touched. [SOC25_DEQUE.md](SOC25_DEQUE.md) explains the construction and limitations. The initial audit checked only the three representative tables. The ninth pass below corrects that incomplete coverage statement: existing equivalences connect supplied entries 535, 572, and 573 to the same three starts.

Against an independent **compiled C++ big-integer** implementation of the same upstream map, full 100,000-round comparisons give speedups of **456.70x, 438.59x, and 415.14x** for the three starts. This avoids a mandatory full-counter copy per round; it is not a proof of an exponential improvement or constant worst-case round cost.

Each start completed **one billion reset rounds without a halt**, a thousand times the round count reported in the pinned upstream PR. Simulation times were 153.811, 156.502, and 153.763 seconds. Final counter widths are about 8.56 billion bits each. The small result records are in [soc25_results.json](soc25_results.json); the roughly one-GiB counter payloads are not included in Git. This tool currently replays from a selected start rather than resuming saved large states.

The independent checks cover 18,056 round cases, including 6,033 halting cases; 100,000 arithmetic-operation comparisons; complete Python orbit comparisons; complete 100,000-round comparisons against Boost `cpp_int`; and budget/error controls. The native/Python suite also passed under the undefined-behavior sanitizer. The native implementation and long orbit remain unverified, so no classification or certified raw-step count is claimed.

The final open-PR audit covers upstream #40 (related recurrence work, explicitly credited), #39 (previously excluded halting result), #3/#4 (assumptions), and owner #1 (previously excluded halting result). No new complete result is claimed from these searches.

## 2026-10-25 — Ninth pass: reuse the accelerators and investigate a new packet frontier

**No new complete blank-run classification.** The focused continuation applies the tools to seven further targets and establishes that three additional supplied variants share the already searched SOC25 starts. It also continues entry 26 to **five trillion** recurrence iterations, at `(2009061144720,15490938245740)`, with no halt. That is 6.25 times the wiki's reported `8e11` iterations; it is not a literature-wide simulation-record claim.

### Five more cubic models

[CUBIC_FAMILY.md](CUBIC_FAMILY.md) gives the exact mapping to existing `CubicCap.WF17/32/33/35/36`, derivations, measurements, and continuation commands. Entries **138, 269, 409, and 494** each reached **100 billion certificate iterations** with guarded doubling blocks. Entry **35** reached **one trillion certificate iterations** using a new mixed-slope construction: regular events have ideal slopes 4/3 and 4, and their corrections depend on small residues modulo powers of three. One normalized event can represent two certificate iterations; the simulator counts that explicitly.

The existing optimized CubicCap wrappers depend on `Uint63` specifications. [ResearchCubicModels.v](../../verify/ResearchCubicModels.v) rechecks their natural-number definitions, blank-start bridges, and four reflected input mappings without those wrappers. Its ten printed reports are closed. [ResearchCubicFamily.v](../../verify/ResearchCubicFamily.v) checks seven normalized identities for entry 35. [ResearchCubicFamilyJump.v](../../verify/ResearchCubicFamilyJump.v) contains four printed abstract guard/correction theorems covering the doubling and asymmetric maps. These files pass separate kernel checking. This is reuse of the existing TM recurrence arguments plus additional batching arithmetic, not verification of the C++ implementation.

Native checks include 5,915 ordinary-TM comparisons, 191 halting cases, a million Python iterations per model, accepted block/scalar comparisons, checkpoint/error controls, and undefined-behavior sanitization. Exact full states agree between the accelerated and compiled scalar billion-iteration benchmarks. [cubic_family_results.json](cubic_family_results.json) records the measurements and five preserved checkpoints.

### Two packet streams and an actual catalogue failure

[PACKET_STREAM.md](PACKET_STREAM.md) applies the longitudinal packet/cycle method from valu42's work and upstream PR #39 to entries **405 and 482**. Finite packets were learned independently. Both contain a four-cell packet that doubles the right-tail call count. [ResearchPacketCoverage.v](../../verify/ResearchPacketCoverage.v) checks that `m` copies transform `n` calls into `n*2^m` calls, along with 34 finite rules, blank/round entry bridges, and local halting packets. All twelve printed reports are closed. The method's exponential call-count compression is credited to the existing packet work.

The new evaluator reuses SOC25's sliding words for the tape and call count. A 16-bit tape window plus four counter residue bits composes several exact packet operations, measuring 2.90–3.37x over the single-packet/deque path at 10,000 rounds. Skipping an unchanged repeated-packet prefix gives complete default-mode speedups of 3.12x and 6.96x in full-state comparisons. A further exact `2^e+d` call-counter representation, with dense fallback, improves entry 405 in a separate benchmark. Its gain on entry 482 is small; no general constant-space claim is made.

The first catalogue failed at **161,210 completed rounds of entry 405**, encountering a six-cell word it could not handle. An independent finite learner supplied a new preperiod/cycle. Six additional laws were checked in Coq, and a complete million-bit next tape matched the independent Python evaluator before the native search resumed. The failing boundary is retained as a compressed regression fixture. An unrecognized packet was not silently treated as nonhalting or halting.

The validation includes independent Python orbits, ordinary-TM boundary snapshots, full 100,000-round comparisons between the original single-packet path and composed windows, random field/counter arithmetic, exhaustive window-key samples, the large frontier regression, rollback/error/halting-detector controls, and undefined-behavior sanitization. Entry 405 reached **500,000 complete rounds** and entry 482 reached **300,000**, without halting. A transient single-call rule and a directly checked artificial halting boundary also test paths that a cycle-only catalogue omits. The latest search endpoints and compressed complete checkpoints are recorded in [packet_results.json](packet_results.json). No raw-step bound or classification is inferred from these native runs.

### Corrected SOC25 input coverage

[ResearchSOC25Coverage.v](../../verify/ResearchSOC25Coverage.v) connects entries **535, 572, and 573** to existing `Eqv_WordPairs` representatives for starts `(2,4)`, `(1,3)`, and `(1,2)`, respectively. Its three reports are closed and kernel-checked. Thus the already recorded billion-round searches cover those supplied variants too. The underlying equivalences and upstream PR #40's integer map are existing results; this corrects the earlier representative-only audit and does not claim three new resolutions.

The final audit retains owner #1 and upstream #38/#39 as excluded previous halting results. It also checks the six commits from the branch base to upstream BB6 tip `0bd6d3890fa9cdf502904847a42c1004d1291db4`: the eight changed proof files contain 49 distinct-per-file literal six-state tables, with no match to the eleven continuation targets under any state renaming or tape reflection. This is a table/relevant-source audit, not a universal claim about every possible implicit theorem application; details are in [continuation_audit.json](continuation_audit.json). Upstream #40 remains the explicitly credited SOC25 source, at unchanged head `069dc1eb72df69dfa595f491b5c315c3ce424ac6`; upstream #3/#4 concern assumptions. The branch remains a draft research continuation, with all native outcomes marked unverified.

## Proof status

No new complete blank-run halting/nonhalting classification or explicit certified raw-step bound has been established in this work. Existing equivalences and checked reflection maps are reused to connect supplied inputs to the searched models. Two fractal blank starts are reduced to distinct initial pairs of the same total recurrence; their classification remains open. A monotone start is similarly reduced to a different frontier of its partner's program. Cubic Mess now has a checked complete recurrence reduction and a separate abstract jump theorem, while the accelerated native searches remain unverified. Search failures are not proofs of nonhalting or inequivalence.

A result will be submitted only after the exact theorem is checked by Rocq and the current PRs are checked again for duplication. Research and proof PRs from this work target this repository, not upstream.

This is AI-assisted research by Codex. Existing proof methods remain credited to their upstream authors.

