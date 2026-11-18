# BB(6) machine decisions and claims

Start with an `OPEN` line in the [machine table](MACHINES.csv). From this directory, `python3 tracker.py --open` lists candidates and `python3 tracker.py --line 1` shows the record for line 1. The aim of each campaign is a decision from the blank tape for one identified machine.

Use the [machine approach rankings](RANKINGS.md) to choose a fresh campaign or find a proof, simulation or equivalence ready for review.

## Claim board

Use the [BB(2,5) claim and handoff workflow](../bb2x5/ROADMAP.md#how-to-call-dibs-and-keep-a-campaign). Check [branches](https://github.com/valu42/busycoqtesting/branches), [open PRs](https://github.com/valu42/busycoqtesting/pulls), and existing claims. Add a row on `master` with the stable line, a work ID such as `BB6-001-SWEEP`, your handle and branch, the next decision question, and the 48-hour UTC renewal time. For a complementary claim on the same line, describe the separate proof obligation.

| Line | Work ID | Claim state | Agent / branch | Next question, evidence or handoff | Renew by (UTC) |
|---:|---|---|---|---|---|
| 110 | BB6-110-VISIT | CLAIMED | Codex / `research/bb6-line110-visits` | Decide ID 28035 from blank. Derive its rightward visit rules from its own table and compare them with the three halters in [upstream PR 59](https://github.com/ccz181078/busycoq/pull/59). Determine which input first reaches F1 or find a closed set of safe returns. | 2026-11-20 19:14Z |
| 133 | BB6-133-ODOMETER | CLAIMED | Codex/odometer-133 / [`research/bb6-line133-odometer`](https://github.com/valu42/busycoqtesting/tree/research/bb6-line133-odometer) | ID 35069. Match the reflected table to line 581, identify the actual blank-start entry and test whether its odometer reaches F0 or a closed return family. [Sibling proof](https://github.com/ccz181078/busycoq/pull/76) | 2026-11-20 19:14Z |
| 173 | BB6-173-REPLAY | CLAIMED | Codex / `research/bb6-line173-replay` | Check whether the merged upstream `FIBv7.v` theorem applies to ID 45924 from blank A. Match all twelve instructions, replay the kernel proof, and record the proven outcome and attribution. | 2026-11-20 19:10Z |

Renew a `CLAIMED` row with a reachable checkpoint, proved lemma or reproducible result and the remaining obstacle. On release, link the work and record what the next agent should try. Use `BLOCKED`, `RELEASED` or `DONE` as appropriate. Claim state lives here. Machine evidence lives in the machine table.

## Record a decision

- **HALTS** requires a reproducible path from the blank start to the undefined instruction. Justify accelerated steps and link the witness and replay.
- **NONHALTS** requires a proof from blank that covers every reachable case and establishes infinite progress in elementary instructions. An exact reachable loop suffices.
- **EQUIVALENT** requires a proof that the two specified machines have the same blank-tape halting outcome. Link the proof and the representative's stable line.

Record the full machine, revision, independent check and verification status with the result. Put machine-specific notes in a file such as `line001-sweeps.md` and link it from the table or claim. A finite run without a halt is a lower bound. Keep partial results with the claim so another agent can continue from them. Once a decision is verified, update the existing table row and close or redirect its claims. [Example of a kernel-checked decision in this repository](../bb2x5/line36-rocq.md)
