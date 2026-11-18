# BB(6) holdout research

[Machine table](MACHINES.csv) · [Claim board and handoffs](ROADMAP.md) · [Research overview and proof queue](PROOF-QUEUE.md) · [Original 608 entries](BB6_holdouts_608.txt)

Each row is a six-state, two-symbol machine started in state A at coordinate zero on an all-zero, two-way infinite tape. The six blocks of its transition string are states A–F. Each block gives the instructions for reading 0 and 1 in that order. Reaching `---` halts.

**Use the one-based line in the October 30, 2026 list as the permanent research index.** Keep the row, numeric machine ID and full transition string when its status changes. The [published list](https://wiki.bbchallenge.org/w/images/5/5e/BB6_holdouts_608.txt) groups machines by known equivalences. The local baseline records its ID and transition string on each line with LF line endings.

## Recorded outcomes

On November 18 the register records **30 proven halters and 50 proven nonhalters**. Seven machines have reported simulation halts. Line 405 has a proved equivalence to line 117. Of the 520 unresolved representatives, four have open upstream PRs for partial results and 516 appear in the fresh-work queue. The original import listed 523 open rows and linked 77 decisions as pending PRs. Run the summary below for the latest counts.

## Use the register

From `research/bb6/`, run any of the following with Python 3. Each command checks the table against the frozen ID and transition string on every line.

```sh
python3 tracker.py             # counts by status
python3 tracker.py --open      # candidate lines, IDs and machines in original order
python3 tracker.py --line 117  # one row, including evidence and notes
```

| Status | Meaning |
|---|---|
| `OPEN` | Candidate for a blank-tape decision. Check the claim board for an owner. |
| `HALT_PR`, `NONHALT_PR` | An upstream PR proposes an outcome whose complete blank-start proof has yet to be identified. Its link is in `source`. |
| `PARTIAL_PR` | An open upstream PR proves a reduction or covers this representative in an equivalence. Its blank-tape outcome is undecided. |
| `SIMULATED_HALT` | A source reports a halt by simulation. The run record is in `simulation_log`. |
| `EQUIVALENCE_PR`, `EQUIVALENT` | A proposed or verified equivalence points to the representative in `same_as_line`. Follow that line for the decision. |
| `HALTS`, `NONHALTS` | A proved decision from blank. The row links the published proof or witness. The notes identify the theorem and its source. |

Edit [MACHINES.csv](MACHINES.csv) when evidence changes. Set `status`, date the evidence as `YYYY-MM-DD`, and link a source or repository path. Use `notes` for the replay command, theorem or handoff as needed. For an equivalence, keep the lower line as the representative and point the higher line to it. Use `PARTIAL_PR` for the representative while an upstream PR covers it and the blank outcome is undecided. If a pending result is withdrawn, record that in the evidence and return the affected row to the appropriate status. The blank-tape decision criteria and claim workflow are on the [roadmap](ROADMAP.md).

The [community tracker](https://denniskoshta.com/bbchallenge/bb6/) and [upstream BusyCoq PRs](https://github.com/ccz181078/busycoq/pulls) are useful places to check before opening a campaign.
