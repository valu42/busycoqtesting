# Line 7: exceptional replies, forced-safe guards, and an uncalibrated halting heuristic

Machine: `1RB---3RA2LA2RB_2LB3LA4LB4RA0RA`.
Starting repository commit: `2ab106f706cb1715d494c7f67464e9222092058f`.
Research pass: 2026-11-18. Blank two-way infinite tape; defined instructions are the raw clock. No result in this report has been formally verified in Rocq or Lean.

**Outlook: Possible halting.** The community's probable-halting claim remains an attributed conjecture. This pass makes its main missing ingredient more precise: most superficially plausible halt trials are forced safe, and the remaining trials have no justified probability law. No numerical halting-time median or percentile is warranted.

## Inherited baseline and source access

The full machine string matches the [current community holdout entry](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved). It attributes a doubly exponential halting heuristic to LegionMammal978. The [October report](https://wiki.bbchallenge.org/wiki/TMBR:_October_2026#Holdouts) attributes a simulation beyond `10^1,140,000,000` instructions to the same researcher on October 17. These are external reports, not a replay performed here. Both pages were read on the research date.

The linked original messages ([heuristic](https://discord.com/channels/960643023006490684/1259770421046411285/1559400536690794496), [continuation](https://discord.com/channels/960643023006490684/1259770421046411285/1559690798490980384), [run](https://discord.com/channels/960643023006490684/1259770421046411285/1561033327190872226)) returned a JavaScript shell without message text. Consequently the original heuristic's random variables, assumptions and parameter `n` in the wiki's `exp(exp(O(n)))` were not verified. The reported huge survival time does not itself support halting.

The repository already supplied [an exact suffix-call accelerator and its derivation](../frontiers/README.md#line-7-and-exceptional-returns), [implementation](../frontiers/line7.py), [tests](../frontiers/test_line7.py), and a [complete checkpoint after 8,192 epochs](../frontiers/runs/line7-calls.json) at approximately `5.69453 × 10^3872` instructions. These are inherited results; the table's original simulation baseline is unchanged.

## Exact trigger and the opportunities actually being counted

The only undefined instruction is A1. Only A0 writes a 1. Its next action is a B call into the suffix on its right, with the new 1 suspended as a guard. A B return consumes the guard through B1 and is safe. An A return reaches A1 and halts without executing another defined instruction. A halt inside that suffix is, of course, already a halt of the machine.

Thus **a completed B suffix call returning A to an A0 guard is the exact trigger**. This includes both the fresh left guard of each epoch and temporary guards created internally. On an old cell the guard is usually created after a previous A call has returned A to a suspended zero, so it is an ordered, correlated response test, not an arbitrary random tape sample.

An epoch starts in A on the fresh zero left of the saved word. If its outer B suffix call returns B, two local instructions complete the epoch, add a leading 3, and shift the fresh head left by one. All epochs in this report complete. The internal guard statistics below deliberately exclude this one outer guard per epoch; the outer guards remain another possible halting route. The finite executions establish reachability of the tested calls from blank, **not** reachability of their halting responses.

### New safe filters for internal tests

The following are exact sufficient safety conditions for a guard's B call. They are not proposed as a complete invariant of the blank orbit.

* Child starts with 0: B0 returns B in one instruction.
* Child starts with 2: B2 returns B in one instruction.
* Entire nonblank child suffix is `32`: literal execution returns B in nine instructions, leaving `4432` on that suffix and its new cells.
* Child starts with `3w`, where `w` consists of 2s and 4s, and the following request-count calculation reaches zero within `w`: the call returns B without touching the remaining suffix.

For the last filter, B3 initially sends two A requests to its child, provided both return B; it then leaves 2 and returns B. Start with `(q,N)=(A,2)` and scan `w`:

| Entry and digit | Next entry and request count |
|---|---|
| A, 2 | A, `3N` |
| A, 4 | B, `N` |
| B, 2 | A, `floor(N/2)` |
| B, 4 | A, `floor((N+1)/2)` |

These are the inherited one-cell identities. If N becomes zero, the deepest cell asks nothing of the unexamined tail. Its return is B, and backward composition justifies each enclosing assumed B return. All skipped paths use only defined instructions; they cannot contain A1. For example, `34242` is a sufficient prefix regardless of its tail: its counts are `2 → 2 → 1 → 1 → 0`. This proves the filter for arbitrary finite prefixes, not merely those tested.

## New experiments on the actual execution

[The instrumented script](line7_probe.py) reuses the inherited accelerator and only adds observations to its literal exception handler. It does not replace exception handling with a probabilistic or overapproximate rule. Results include every sampled epoch and the residual suffixes. Full physical endpoint checkpoints are included.

| Actual execution interval | Internal guard tests | Forced safe by the above filters | Residual internal tests | Leading 2-run at final epoch |
|---|---:|---:|---:|---:|
| Epochs 1–1,024, replayed from blank | 427,138 | 427,136 | 2, both return B | 973 |
| Epochs 8,193–8,256, resumed from inherited checkpoint | 466,170 | 466,170 | 0 | 8,178 |

In the first interval the forced-safe partition is: 1,547 child-0 cases, 424,358 child-2 cases, 773 terminal-32 cases and 458 ordinary-prefix cases. The two residual calls occur in epochs 415 and 827. Their complete suffixes are stored in [the first interval's data](line7-blank-1024.json); independent literal execution returns B in respectively **129 and 21 instructions**, matching the accelerator's complete resulting tape and raw count. They are residual only with respect to these simple filters; neither is evidence of a positive halt probability.

The held-out interval has 102 child-0, 465,984 child-2, 51 terminal-32 and 33 ordinary-prefix cases. Its entire guard population is locally forced safe, rather than merely fortunate under random outcomes. These observations reject using the raw count of guards as the number of exchangeable trials with a fixed positive hazard. They do not disprove all more selective probabilistic models.

The full [8,256-epoch checkpoint](line7-8192-8256-checkpoint.json) survives to approximately **`1.955320 × 10^3903` raw instructions**. `steps_hex` stores the exact integer; [the interval data](line7-8192-8256.json) record growth and timing summaries. A further bounded continuation through epoch **9,216** reaches approximately **`6.304411 × 10^4360`** instructions; its [complete checkpoint](line7-8192-9216-checkpoint.json) is the largest new endpoint in this pass. The [longer interval log](line7-8192-9216.json) was recorded before the guard filters were added, so it records total internal tests but not their safe-filter partition. Its 1,024-epoch growth sample has 1,022 changes of +1, one zero, and one decrease of one. These improve the reproducible repository endpoint, but remain far below the externally reported run and are not stopping-time estimates.

At 1,024 epochs the 2-run changed by +1 in 1,005 epochs, by 0 in seven, and decreased in twelve, with maximum decrease six. All 64 held-out epochs increase it by one. This counter therefore has long regular stretches interrupted by exceptions; a permanent +1 recurrence is already false. This finite observation is not an all-time positive-drift theorem.

## Raw timing and what a runtime estimate would require

For N calls in A through k consecutive 2s, the exact child request count is `3^k N` and the local cost is `2N(3^k−1)`, **conditional on every descendant returning B**. Exceptions must resume their chronological suspended instructions; the accelerator does so. More generally each ordinary cell costs N plus its emitted child count. These identities give exact times for a known future event history.

They do not give a constant separation between meaningful halting opportunities. Within epochs 8,193–8,256, `log10` of the raw epoch increment ranges from about 3,873.0565 to 3,903.1151, while each measured internal guard is forced safe. The inherited large leading block makes time approximately exponential in epoch number over this interval. That is different from a prediction of a doubly exponential eventual stopping time.

To convert a heuristic to conditional quantiles, one would need:

1. A justified definition of residual opportunities including the outer guards, after removing forced-safe cases.
2. Their actual deterministic recurrence or a defensible conditional probability model, accounting for inherited tape states, request-count residues and the changes in width.
3. Evidence that cumulative hazard does not converge: a sequence of probabilities merely being positive is insufficient if it decreases too rapidly.
4. A clock bound or timing recurrence up to the predicted event quantiles, including exceptional excursions.

For a hypothetical uncertainty model, let `p_j = P(H=j | H≥j)`, where H is the index of the halting opportunity. The chain rule gives survival through m as the product of `(1−p_j)` without an independence assumption; all correlations must be incorporated in those conditional hazards. Neither those hazards nor a reliable opportunity schedule have been established for this execution. Therefore no median or percentile range is quoted; the community's doubly exponential scale remains an uncalibrated conjecture.

## Verification and reproduction

From the repository root, with Python 3.10 or later and assertions enabled:

```sh
python3 research/bb2x5/halting-outlook/line7_probe.py --epochs 1024 \
  --out research/bb2x5/halting-outlook/line7-blank-1024.json
python3 research/bb2x5/halting-outlook/line7_probe.py \
  --resume research/bb2x5/frontiers/runs/line7-calls.json --epochs 8256 \
  --out research/bb2x5/halting-outlook/line7-8192-8256.json
python3 research/bb2x5/halting-outlook/line7_check.py --deep
# Reproduce the deepest raw endpoint without observational overhead:
python3 research/bb2x5/frontiers/line7.py \
  --resume research/bb2x5/frontiers/runs/line7-calls.json --epochs 9216 \
  --checkpoint research/bb2x5/halting-outlook/line7-8192-9216-checkpoint.json
```

[The verification transcript](line7-probe-verification.txt) records full tape, state, head and raw-count agreement with the independent literal interpreter for the first 18 blank epochs, ending at 84,412 instructions. It also records 2,250 complete-configuration comparisons for the ordinary-prefix filter with arbitrary two-cell tails, the exact terminal-32 identity, and the two actual residual suffixes. The proof above, rather than finite testing alone, supports arbitrary ordinary-prefix lengths. No newly accelerated transition is introduced. The [inherited accelerator test suite also passed](line7-verification.txt), including its comparison to the independent moving-window checkpoint at 100 billion raw instructions. The latter checks the full physical configuration, not only a step total. A separate uninstrumented continuation from epoch 8,256 to 9,216 exactly matches the instrumented continuation from 8,192, including the complete tape and raw clock; `--deep` reproduces this split-checkpoint comparison.

To repeat that inherited suite, compile `frontiers/window.cpp` with `c++ -O3 -std=c++17`, then set `BB25_WINDOW` to the resulting executable when running `python3 research/bb2x5/frontiers/test_line7.py`.

## Next concrete step

Extend the safe-return recognizer to nested 3s and apply it to the **outer** epoch calls as well as internal calls. Record the smallest unproved residual suffix transformation, preserving its actual phase and history. The concrete residual words from epochs 415 and 827 provide reproducible seeds. Only after finding an unbounded family of genuinely distinct residual tests should one attempt to recover or replace the community hazard model and translate its conditional quantiles through the exact raw timing rules.
