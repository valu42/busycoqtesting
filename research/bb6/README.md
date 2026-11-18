# BB(6) holdout research

[Machine table](MACHINES.csv) · [Claim board and handoffs](ROADMAP.md) · [Original 608 entries](BB6_holdouts_608.txt)

Each row is a six-state, two-symbol machine started in state A at coordinate zero on an all-zero, two-way infinite tape. The six blocks of its transition string are states A–F. Each block gives the instructions for reading 0 and 1 in that order. Reaching `---` halts.

**Use the one-based line in the October 30, 2026 list as the permanent research index.** Keep the row, numeric machine ID and full transition string when its status changes. The [published list](https://wiki.bbchallenge.org/w/images/5/5e/BB6_holdouts_608.txt) groups machines by known equivalences. The local baseline records its ID and transition string on each line with LF line endings.

## Starting position

On November 18 the 608 rows gave **523 targets for a fresh decision**. Open BusyCoq PRs claimed 49 nonhalting and 28 halting results. Seven further machines had reported simulation halts. One proposed equivalence joins lines 117 and 405, with line 117 retained in the queue. The table links the evidence on every affected row. These figures describe the initial import. Run the summary for the current counts.

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
| `HALT_PR`, `NONHALT_PR` | An upstream PR proposes this outcome. Its link is in `source`. |
| `SIMULATED_HALT` | A source reports a halt by simulation. The run record is in `simulation_log`. |
| `EQUIVALENCE_PR`, `EQUIVALENT` | A proposed or verified equivalence points to the representative in `same_as_line`. Follow that line for the decision. |
| `HALTS`, `NONHALTS` | A verified decision from blank. The row links the witness or proof and its verification. |

Edit [MACHINES.csv](MACHINES.csv) when evidence changes. Set `status`, date the evidence as `YYYY-MM-DD`, and link a source or repository path. Use `notes` for the replay command, theorem or handoff as needed. For an equivalence, keep the lower line as the representative and point the higher line to it. If a pending result is withdrawn, record that in the evidence and return the affected row to the appropriate status. The blank-tape decision criteria and claim workflow are on the [roadmap](ROADMAP.md).

The [community tracker](https://denniskoshta.com/bbchallenge/bb6/) and [upstream BusyCoq PRs](https://github.com/ccz181078/busycoq/pulls) are useful places to check before opening a campaign.
