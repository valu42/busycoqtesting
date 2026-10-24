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

## Proof status

No new halting, nonhalting, equivalence, or explicit raw-step-bound theorem has been established in this work. Search failures are not proofs of nonhalting or inequivalence.

A result will be submitted only after the exact theorem is checked by Rocq and the current PRs are checked again for duplication. Research and proof PRs from this work target this repository, not upstream.

This is AI-assisted research by Codex. Existing proof methods remain credited to their upstream authors.

