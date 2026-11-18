# BB(2,5) machine decisions

**Verified decisions from blank: 1 of 37.** Line 36 runs forever. Lines 1–35 and 37 remain open here. The owner clarified that the reported proof was for line 36. [Line 36 theorem](line36-rocq.md) · [Machine list](BB2x5_Rocq_holdouts_37.txt)

## Pick a research direction

**Give the next free agent a machine with an unclaimed route to a decision.** For an arithmetic argument, check `26-RESERVE`. For a sweep invariant, check `35-GUARD`. For a stream argument, check `22-PHASE`. In each case a specific statement about the blank orbit would settle the machine. The board below records who has dibs. If your first choice is staffed, take the next available machine or name a genuinely independent approach.

## Claim board

Edit your row on `master` before starting. A claim covers a continuing investigation, with its next question visible to other agents. `OPEN` is available. `SEEN` points to prior work with no registered owner. Check its branch before claiming it. [Claim and handoff rules](#how-to-call-dibs-and-keep-a-campaign)

| Work ID | State | Agent / branch | Decision route or handoff | Renew by (UTC) |
|---|---|---|---|---|
| 26-RESERVE | CLAIMED | Codex/reserve-26 / [draft PR 7](https://github.com/valu42/busycoqtesting/pull/7) | Width 205 and the next 108 records are safe. Bound the prefix sums of floor((b+1)/4)−1 for the second gaps of the blank-start calendars at record depths. All 56 observed six-record windows gain, while shifting the starting phase can lose four. | 2026-11-20 16:50Z |
| 35-GUARD | SEEN | | **Decide line 35.** From epoch 5 a sweep halts exactly when cut-8 debt reaches six plus the prefix balance. Together with the five-sweep interior bound, it suffices to maintain two left-quarter inequalities from epoch 444. Coordinate the spatial route with `35-MIDDLE`. [Exact test and quarter inequalities](line35-guard-stream.md#a-sufficient-test-using-the-left-quarter) | — |
| 35-COLUMNS | RELEASED | Codex/guard-stream / [work branch](https://github.com/valu42/busycoqtesting/tree/research/bb2x5-line35-guard-stream) | From the constant stream of 2s, exclude the seven forbidden anchored pairs under the exact birth rule. Preserve the origin of each column through its transient. Right extensions can shadow arbitrarily long boundary histories. Replay `python3 research/bb2x5/line35_guard_stream.py`. [Recurrence and witnesses](line35-guard-stream.md#what-a-chronological-invariant-must-distinguish) · [Delayed-debt theorem](line35-delayed-debt.md) | — |
| 35-MIDDLE | RELEASED | Codex/middle-35 / [proof and checker](https://github.com/valu42/busycoqtesting/blob/1a47b45f468aa296f57255a7a127ce137464c69d/research/bb2x5/line35-middle.md) | After five ordinary sweeps, eight times the excess of closings is at most the interval length plus 25. The resulting left-quarter test succeeds at every blank epoch 524–150,000 (73,421,002,000 raw steps). Prove the two quarter inequalities at all subsequent epochs, or follow their first failure. Replay `python3 line35_middle.py --epochs 150000` on the linked commit in `research/bb2x5`. | — |
| 31-PHASE | CLAIMED | Codex / `research/bb2x5-line31-phase` | Decide line 31 by retaining the start of the periodic even-cell input through the paired transducer. Search for the first fatal entry, or certify its exclusion. | 2026-11-20 16:15Z |
| 21-PHASE | CLAIMED | Codex/phase-22 / [proof and checker](https://github.com/valu42/busycoqtesting/blob/089c13f78183d617b6f91aa033afdbad857517b7/research/bb2x5/anchored-phase.md) | The 84 grandparent triggers are exact. Replay cut 66 through 256 cycle copies from blank. A BB decides the machine. At a surviving endpoint compute the first still possible B2 from its complete positive tape. | 2026-11-20 17:03Z |
| 22-PHASE | CLAIMED | Codex/phase-22 / [proof and checker](https://github.com/valu42/busycoqtesting/blob/089c13f78183d617b6f91aa033afdbad857517b7/research/bb2x5/anchored-phase.md) | The 36 grandparent triggers are exact. At 70,368,746,274,949 groups, the tape protects five unvisited cells. Replay 64 cycles at cut 74 and test the forced future for a halt or a closed safe cycle. | 2026-11-20 17:03Z |
| 33-REPLY | RELEASED | Codex/outlook-continuation / [result](https://github.com/valu42/busycoqtesting/blob/c970885c2e6dce20b0a712d310ba16982660e2f5/research/bb2x5/halting-outlook/reserve33.md) | One aligned 421 block protects a whole shifted request batch. Two evaluators match at extension 41 with 20 aligned blocks. Bound cumulative losses across actual stages. Replay `python3 reserve33.py` in the report directory. | — |
| 34-CUT12 | CLAIMED | Codex/line34-proof / [research branch](https://github.com/valu42/busycoqtesting/tree/research/bb2x5-next-proof-34) | Decide line 34 by proving or refuting the residual allowances on the 52-phase blank prefix. Start at the literal epoch-1300 seed. Test a phase-coupled certificate at the four zero-debt cuts and check any obstruction on the genuine orbit. | 2026-11-20 16:25Z |
| 19-23-INTERFACE | RELEASED | Codex / [paired guard study](frontiers/spaghetti-guards.md) | A reflection gives two distinct seeds for the same rules. Both reached 100 billion steps. All 58,488 line 23 launches begin with a prefix proved safe. Establish whether these prefixes exhaust its blank orbit. Line 19 has reachable `3233` launches and a third call exceeding 354 million steps. [Checked prefixes](frontiers/line19-guard-filter.md) · [Physical controls](frontiers/line19-pair.md) | — |
| 18-ROOT-RETURN | RELEASED | Codex / [record and traces](frontiers/line18.md) | The first completed odd record with edge ≥ +30,000 is 9,333. A suffix beginning `13` excludes a root A under the record requests. The protected prefix covers 366 conditional attempts. The remaining question is whether a deeper call can encounter A4, including the tested `133313` with ABB, or interrupt the protected regime. [Guard proof](frontiers/line18-interfaces.md) | — |
| 13-PARITY | RELEASED | Codex/outlook-continuation / [result](https://github.com/valu42/busycoqtesting/blob/c970885c2e6dce20b0a712d310ba16982660e2f5/research/bb2x5/halting-outlook/timing13.md) | An infinite blank run must face infinitely many fresh odd-cell tests. Cell 155 must settle before 1.1 × 10^93 raw instructions. Determine the first-A parity from its actual parent stream. Replay `python3 timing13.py` in the report directory. | — |
| 15-RETURN | RELEASED | Codex / [seven-cell strip study](frontiers/line15.md) | The 245,000-period checkpoint reaches 20,331,546,024,060 raw steps. The window and strip simulators agree on the full physical tape. Every audited nonroot strip with five calls starts `AAABB`. The four-cell fringe admits a controlled halt. Determine whether the actual parent can send A on the fifth call to a virgin strip. [Source and continuation](frontiers/line15.md) | — |
| 17-CLOCK | CLAIMED | Codex / `line17-frontiers` on `master` | Trace the marked inputs that control the first return from +12. The [10²⁹-sweep checkpoint](frontiers/runs/line17-epochs.json) reached pair 175. Two replays located its first entry between 9 × 10²⁸ and 10²⁹ sweeps. Next, determine which times of the fifth mark at cut 403 alone force either decisive bit at cut 418. | 2026-11-20 15:42 |
| 06-WORD | OPEN | | Prove that every reachable unary probe returns B, or find the first failing probe and replay the halt. A viable residual grammar must distinguish words sharing the same short-factor counts. [Recurrence](line6.md) · [Counterexample][probe6] | — |
| 34-SWEEP | SEEN | | From epoch 10, a blank sweep halts exactly when suffix debt at cut 12 reaches six plus the prefix balance (openings minus closings). The altered tape that shadows 15 sweeps is a test for any invariant. Coordinate this work through `34-CUT12`. [Prefix proof][left34] · [Splice][right34] | — |
| FORMAL-04 | OPEN | | Line 4 physical rewrite for an identified step in a blank-orbit proof. [Rewrite](line4.md) | — |
| PORT-07 | CLAIMED | Codex / [machine 7 guard search](https://github.com/valu42/busycoqtesting/tree/research/bb2x5-line7-guards/research/bb2x5) | Starting at the checked epoch 9,216, search the next 512 left extensions for guard calls outside the current safe filters. Independently replay reachable residuals or prove a stronger return condition if none occur. The target is A1 on the actual blank orbit. [Earlier guard results][out-seven] | 2026-11-20 16:30Z |
| 13-TRACE | SEEN | | Lifetime entry traces for the line 13 proof. Cell 155 has only Bs at the saved cutoff. [Trace](line13-edge.md) | — |
| 26-CALENDAR | SEEN | | Exact calendars exclude fixed points through width 173. The new physical checkpoint fixes p(85)=173. Test a proposed record-time inequality against its incoming carry. [Tape, raw clock and replay](column-time.md) | — |
| 37-CUT | OPEN | | Bound the debt reaching cut 45 on the actual blank orbit, or follow its first violation. The owner clarified that the completed proof was for line 36. [Cut certificate](line37-header.md) · [Exact stream recurrence](line37-stream.md) | — |

<details>
<summary>Completed work and earlier handoffs</summary>

| Work ID | State | Agent / branch | Decision route or handoff | Renew by (UTC) |
|---|---|---|---|---|
| 36-REPLAY | SEEN | | Independent replay of solved line 36. [Build transcript](line36-kernel-replay.txt) · [Workflow][replay] | — |
| 36-BLANK | DONE | | [Blank-tape nonhalting theorem](../../verify/Line36Nonhalting.v) and [verification instructions](line36-rocq.md). | — |
| SIM-TARGETED-10 | DONE | Codex / [targeted simulations](https://github.com/valu42/busycoqtesting/tree/research/bb2x5-targeted-simulations/research/bb2x5) | Indexed exact runs for 3, 9, 14, 16, 18, 20, 24, 28, 29 and 30. Line 3 matches the outlook branch at record 300 and extends it to 320. Line 30 reproduces its 20,000th return. Line 18 reaches +10,005 at odd record 3,136. From this directory run `python3 frontiers/scoreboard.py --check`. [Per-machine replay and continuation](frontiers/README.md#replaying-the-targeted-simulations) | — |
| OUTLOOK-37-PAGE | DONE | Codex / [37-machine outlook](https://github.com/valu42/busycoqtesting/blob/research/bb2x5-next-proof-34/research/bb2x5/HALTING_OUTLOOK.md) | Published the full-string outlook from `01b0a10` and [proof reductions and checkpoints](https://github.com/valu42/busycoqtesting/commit/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb) for 6, 21, 22, 31, 33 and 34. On the outlook branch run `python3 research/bb2x5/halting-outlook/update_table.py --check`. | — |

</details>

### How to call dibs and keep a campaign

1. **Claim.** Check [branches][branches], [open PRs][prs] and the live rows for an equivalent approach. Put `CLAIMED`, your session handle, branch, scope, next question and a 48-hour UTC expiry in one row. The first compatible claim visible on `master` wins. Publish by fast-forward push or merged claim PR. Recheck ownership if the base moves. A second agent on the same machine should name the distinct proof obligation or method they own.
2. **Continue or redirect.** Keep the same ID across milestones. Renew with evidence and the next question. Before a long run, record its starting checkpoint, budget, what event would change the proof, and what you would do if the event never occurs within budget. If both outcomes would leave the same proof obligation untouched, try another method or take a different machine.
3. **Hand off.** Link the commit, replay command, last reachable state or proved lemma, and next unresolved case. Use `BLOCKED` for a named dependency, `RELEASED` when giving up the scope, or `DONE` when its stated outcome has landed. After expiry, check the old branch for unpublished-to-master progress and record the transfer. A refuted invariant deserves its smallest known counterexample.

## Other machines

Agents can claim any open line, including line 37. The catalogue gives a decision question, evidence and optional entry assignments for each. Register a new row when taking an unlisted route.

| Approach | Lines | Where to start |
|---|---|---|
| Bound the debt in successive sweeps | 34, 35. Use 36 as a solved example. | [Sweep guards and matching debt](STARTERS.md#sweep-guards-and-matching-debt) |
| Decide whether an arithmetic orbit reaches a halting target | 3, 4, 5, 17, 26, 29, 30 | [Arithmetic and counter orbits](STARTERS.md#arithmetic-and-counter-orbits) |
| Classify the replies that can reach a guard | 1, 2, 6, 7, 9, 15, 18, 20, 24, 33 | [Recursive requests and suffix returns](STARTERS.md#recursive-requests-and-suffix-returns) |
| Prove or exhibit a dangerous prefix at a fresh cell | 8, 10, 11, 12, 13, 21, 22, 31 | [Anchored streams at fresh cells](STARTERS.md#anchored-streams-at-fresh-cells) |
| Derive a closed tape description from the literal transition rules | 14, 16, 19, 23, 25, 27, 28, 32 | [Finding a reduction](STARTERS.md#finding-a-reduction) |

<a id="work-on-other-branches"></a>

The [simulation table](SIMULATION_TABLE.md) indexes the exact checkpoints on master, including the [ten targeted runs](frontiers/README.md#replaying-the-targeted-simulations). The [branch outlook][outlook-current] contains additional machine-specific derivations. Check both before repeating a run.

## When a machine counts as resolved

**HALTS** requires a reproducible path from the two-way blank tape, state A at coordinate zero, to the literal undefined instruction. Justify any accelerated transitions. **NONHALTS** requires a proof from that seed covering every reachable case and establishing infinite progress in elementary instructions. An exact reachable loop suffices.

Record the full transition string, witness or proof, revision, independent check and verification status. Update the tally once per machine and release its other claims. A finite run, a sufficient condition with an open premise, or a halt from an altered tape leaves the blank decision open. [Verification example](line36-rocq.md)

[branches]: https://github.com/valu42/busycoqtesting/branches
[left34]: https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/line34_left.md
[out-seven]: https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/halting-outlook/line7.md
[outlook-current]: https://github.com/valu42/busycoqtesting/blob/6e9f4ea27600c34026e8d1c4eb795a7b040a6d5f/research/bb2x5/HALTING_OUTLOOK.md
[parent21]: https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/target21_22.md
[probe6]: https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/probe6.md
[prs]: https://github.com/valu42/busycoqtesting/pulls
[replay]: https://github.com/valu42/busycoqtesting/actions/runs/44316962368
[right34]: https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/line34_right.md
