# BB(2,5) machine decisions

**Verified decisions from blank: 1 of 37.** Line 36 runs forever. Lines 1–35 and 37 remain open here. The owner clarified that the reported proof was for line 36. [Line 36 theorem](line36-rocq.md) · [Machine list](BB2x5_Rocq_holdouts_37.txt)

## Pick a research direction

**Give the next free agent a machine with an unclaimed route to a decision.** For an arithmetic argument, check `26-RESERVE`. For a sweep invariant, check `35-GUARD`. For a stream argument, check `22-PHASE`. In each case a specific statement about the blank orbit would settle the machine. The board below records who has dibs. If your first choice is staffed, take the next available machine or name a genuinely independent approach.

## Claim board

Edit your row on `master` before starting. A claim covers a continuing investigation, with its next question visible to other agents. `OPEN` is available. `SEEN` points to prior work with no registered owner. Check its branch before claiming it. [Claim and handoff rules](#how-to-call-dibs-and-keep-a-campaign)

| Work ID | State | Agent / branch | Decision route or handoff | Renew by (UTC) |
|---|---|---|---|---|
| 26-RESERVE | CLAIMED | Codex/reserve-26 / [draft PR 7](https://github.com/valu42/busycoqtesting/pull/7) | Width 207 and record depth 99. The 28 local residue paths give a sufficient target: prove that complete safe cycles emit at least 6n tokens over the first n records. The least actual prefix average through 63 transitions is 20/3. Three literal counterexamples rule out monotonicity in the safe supply. | 2026-11-20 18:15Z |
| 35-GUARD | RELEASED | Codex/guard-stream / [proof and replay](line35-chronological-strip.md) | A first halt needs debt from beyond cell 28. Five successive debt-five readings at one old cut require 230,304 cells. Couple an isolated incoming pulse to the 28-cell prefix and its birth history. A ten-cell piece of blank epoch 83 costs two openings per extra copy four sweeps later. The left-fifth test passes at epochs 594–40,000. Replay `python3 research/bb2x5/line35_chronological_strip.py`. | — |
| 35-COLUMNS | RELEASED | Codex/guard-stream / [work branch](https://github.com/valu42/busycoqtesting/tree/research/bb2x5-line35-guard-stream) | From the constant stream of 2s, exclude the seven forbidden anchored pairs under the exact birth rule. Preserve the origin of each column through its transient. Right extensions can shadow arbitrarily long boundary histories. Replay `python3 research/bb2x5/line35_guard_stream.py`. [Recurrence and witnesses](line35-guard-stream.md#what-a-chronological-invariant-must-distinguish) · [Delayed-debt theorem](line35-delayed-debt.md) | — |
| 35-MIDDLE | RELEASED | Codex/middle-35 / [proof and checker](https://github.com/valu42/busycoqtesting/blob/1a47b45f468aa296f57255a7a127ce137464c69d/research/bb2x5/line35-middle.md) | After five ordinary sweeps, eight times the excess of closings is at most the interval length plus 25. The resulting left-quarter test succeeds at every blank epoch 524–150,000 (73,421,002,000 raw steps). Prove the two quarter inequalities at all subsequent epochs, or follow their first failure. Replay `python3 line35_middle.py --epochs 150000` on the linked commit in `research/bb2x5`. | — |
| 35-QUARTER | CLAIMED | Codex/middle-35 / [draft PR 10](https://github.com/valu42/busycoqtesting/pull/10) · [zero-debt cut and blank witnesses](https://github.com/valu42/busycoqtesting/blob/d6f72418c0056b47948fb2a4b5182810e586c57d/research/bb2x5/line35-seam.md) | The 352,224-cell right cut at epoch 300,001 has zero debt forever. The paired test covers odd epochs 26,351–300,001 at 293,713,845,976 raw steps. Even arbitrarily large margins can fail on altered tapes. Blank epoch 2022 contains the negative 47-cell factor in the uncovered strip and absorbs its debt two cells later. Bound the total debt from successive such intervals on the blank orbit. Replay `python3 line35_seam.py --literal` in the research directory. | 2026-11-20 20:00Z |
| 31-PHASE | CLAIMED | Codex / [work branch](https://github.com/valu42/busycoqtesting/tree/research/bb2x5-line31-phase) | Decide line 31 by constructing arbitrarily late single-request edits whose drivers enter the safe fixed stream. Test whether a safe edit can be lifted through the true input period, or identify the exact obstruction. | 2026-11-20 18:32Z |
| 21-PHASE | RELEASED | Codex/phase-22 / [proof and replays](https://github.com/valu42/busycoqtesting/blob/afe22505b751e6d04d35e55d0d5127a8aaedf7e4/research/bb2x5/anchored-phase.md) | The blank run permanently clears 0–285. At 216,603,790,802,953 groups, cell 285 has received BAA. A halt at 286 requires one of AAA, AABB, BBA or BBBB next at 285. Determine the actual continuation or exclude all later fresh BBs. Replay `bb25-phase 21 66 394` as documented. | — |
| 22-PHASE | RELEASED | Codex/phase-22 / [proof and replays](https://github.com/valu42/busycoqtesting/blob/afe22505b751e6d04d35e55d0d5127a8aaedf7e4/research/bb2x5/anchored-phase.md) | The blank run permanently clears 0–274. At 2,251,799,815,782,533 groups, cell 274 has received BAA. A halt at 275 requires the next three entries there to be AAA. The actual 269-to-274 advance reproduced the same five-cell block. Control its subsequent inputs. Replay `bb25-phase 22 74 256` as documented. | — |
| 33-REPLY | RELEASED | Codex/outlook-continuation / [result](https://github.com/valu42/busycoqtesting/blob/c970885c2e6dce20b0a712d310ba16982660e2f5/research/bb2x5/halting-outlook/reserve33.md) | One aligned 421 block protects a whole shifted request batch. Two evaluators match at extension 41 with 20 aligned blocks. Bound cumulative losses across actual stages. Replay `python3 reserve33.py` in the report directory. | — |
| 34-CUT12 | CLAIMED | Codex/line34-proof / [line 34 report](https://github.com/valu42/busycoqtesting/blob/32341e94c020e7ec929694ca024cf89a270a3880/research/bb2x5/halting-outlook/cut100.md) | Blank survived 250,000 sweeps. At cut 100, eight local digits suffice if they realize every debt above one. Three generations rule out five consecutive positive groups. Bound the cumulative contribution of groups separated by zero or negative charge on the actual blank orbit. Replay `python3 cut100_ancestry.py` from `halting-outlook/`. | 2026-11-20 17:35Z |
| 19-23-INTERFACE | RELEASED | Codex / [paired guard study](frontiers/spaghetti-guards.md) | A reflection gives two distinct seeds for the same rules. Both reached 100 billion steps. All 58,488 line 23 launches begin with a prefix proved safe. Establish whether these prefixes exhaust its blank orbit. Line 19 has reachable `3233` launches and a third call exceeding 354 million steps. [Checked prefixes](frontiers/line19-guard-filter.md) · [Physical controls](frontiers/line19-pair.md) | — |
| 18-ROOT-RETURN | RELEASED | Codex / [record and traces](frontiers/line18.md) | The first completed odd record with edge ≥ +30,000 is 9,333. A suffix beginning `13` excludes a root A under the record requests. The protected prefix covers 366 conditional attempts. The remaining question is whether a deeper call can encounter A4, including the tested `133313` with ABB, or interrupt the protected regime. [Guard proof](frontiers/line18-interfaces.md) | — |
| 13-PARITY | CLAIMED | Codex/edge-13 / `research/bb2x5-line13-edge` | Determine the actual first A at odd cell 155, then follow the same anchored two-cell test toward B3. Use exact compressed source words and search for an invariant of the pair inputs. Compare initial prefixes against the published blank trace. [Earlier deadline](https://github.com/valu42/busycoqtesting/blob/c970885c2e6dce20b0a712d310ba16982660e2f5/research/bb2x5/halting-outlook/timing13.md) | 2026-11-20 20:35Z |
| 15-RETURN | RELEASED | Codex / [seven-cell strip study](frontiers/line15.md) | The 245,000-period checkpoint reaches 20,331,546,024,060 raw steps. The window and strip simulators agree on the full physical tape. Every audited nonroot strip with five calls starts `AAABB`. The four-cell fringe admits a controlled halt. Determine whether the actual parent can send A on the fifth call to a virgin strip. [Source and continuation](frontiers/line15.md) | — |
| 17-CLOCK | CLAIMED | Codex / `line17-frontiers` on `master` | Trace the marked inputs that control the first return from +12. The [10²⁹-sweep checkpoint](frontiers/runs/line17-epochs.json) reached pair 175. Two replays located its first entry between 9 × 10²⁸ and 10²⁹ sweeps. Next, determine which times of the fifth mark at cut 403 alone force either decisive bit at cut 418. | 2026-11-20 15:42 |
| 06-WORD | CLAIMED | Codex/word-06 / `research/bb2x5-line6-prefix` | Search the true blank epochs for a repeated residual after certified prefix removal. Characterize the prefixes by their calls and returns; test through the inherited extension 16,310. | 2026-11-20 21:00Z |
| 34-SWEEP | SEEN | | From epoch 10, a blank sweep halts exactly when suffix debt at cut 12 reaches six plus the prefix balance (openings minus closings). The altered tape that shadows 15 sweeps is a test for any invariant. Coordinate this work through `34-CUT12`. [Prefix proof][left34] · [Splice][right34] | — |
| FORMAL-04 | OPEN | | Line 4 physical rewrite for an identified step in a blank-orbit proof. [Rewrite](line4.md) | — |
| PORT-07 | CLAIMED | Codex / [machine 7 guard search](https://github.com/valu42/busycoqtesting/pull/9) | Epoch 16,384, fixed suffix at cell −89. Its first A after 218 modulo 486 B replies forces A1 at −94 in 26 more steps. The permanent 42/44 pair and 19 local certificates give 71 halting residues modulo 6,561. Determine the first exceptional rank on that suffix or detect an earlier halt inside it. [Proof, clocks and replay](frontiers/line7-guards.md) · [Earlier baseline][out-seven] | 2026-11-20 17:30Z |
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
