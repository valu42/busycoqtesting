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

**In progress.** The current direction is to seek a common process after grouping tape cells into blocks. The experiment computes finite block-exit behavior, refines state and symbol partitions, and compares the resulting transition graphs. Any matching graph would still require an explicit isomorphism and a Rocq proof connecting both machines to that process.

In parallel, individual counter examples are being studied through their short tape transformations. The aim is to derive a closed invariant or recurrence instead of increasing the previous simulation budgets.

## Proof status

No new halting, nonhalting, equivalence, or explicit raw-step-bound theorem has been established in this work. Search failures are not proofs of nonhalting or inequivalence.

A result will be submitted only after the exact theorem is checked by Rocq and the current PRs are checked again for duplication. Research and proof PRs from this work target this repository, not upstream.

This is AI-assisted research by Codex. Existing proof methods remain credited to their upstream authors.
