# Line 18 · two left extensions and a batch of suffix calls

The machine is `1RB2RA3LB4LA---_2LA0RB1LA2RB0RA`. Record k starts in A at coordinate −2k−1, scanning a blank. The word immediately to its right is `134 (313)^k`, followed by the saved suffix at coordinate k+3. All exterior cells are blank. Literal execution reaches record 1 after 47 defined instructions with suffix `13`. The community holdout list credits dyuan and Legion with earlier analysis. [Community holdout notes](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved)

## What one record asks of the suffix

The prefix sends one A request, then exactly $2^{k-1}$ B requests into the suffix. Each request starts at its first cell and finishes on the first move to the left of it. If all requests return B, the prefix takes exactly $17+24k+29\cdot 2^{k-1}$ local instructions, including both left extensions. The last B return leaves a 3 in the first suffix cell because A2 → 3LB is the only such exit. That 3 joins the next prefix and the suffix cut advances by one. Seven finite traces establish the prefix calculation under the stated reply condition. [Header derivation and executable traces](line18_header.py)

The suffix simulator executes the first A request literally. On B requests it uses the following finite paths, reverting to the physical instructions wherever no listed rule applies. Each row assumes that every emitted child request also returns B. Costs count instructions on the displayed cells.

| Initial cells | Emitted child requests | Final cells | Local cost |
|---|---|---|---:|
| `31` | B | `32` | 4 |
| `32` | none | `31` | 3 |
| `313` | BB | `313` | 11 |
| `323` | none | `313` | 3 |

In n consecutive B calls, the two-cell rule sends one child request for every two calls, rounding up for an initial `31` and down for `32`. The three-cell `313` rule sends two requests per call. Both widths are valid whenever their child replies match. The implementation uses the three-cell rule where its third cell and the following cell are both 3. This groups repeated doublings on the left of the suffix and binary digits farther right.

A child batch returns the number of leading B replies and the first different reply. For a pair, if j children have returned B before an A, then 2j parent calls have completed for an initial `31`, or 2j+1 for `32`. The current B3 and B1 have written `20` and sent the outstanding child request. For `313`, divide j by two. The quotient counts complete parent calls. Remainder zero puts the current parent on `202` after three local instructions, and remainder one puts it on `210` after six. In both cases the child has already updated its own suffix, and A resumes on the last cell of the suspended tile. The simulator then follows the actual instructions to the first left exit. This accounts for exceptional returns inside nested batches in time order.

A changed reply at the outer cut invalidates the header hypothesis. An undefined instruction within the suffix or exhaustion of the work budget also stops the run. Only completed records advance the table clock.

At record **3,136** the rightmost nonzero cell is at **+10,005**. Among the odd left records, this is the first with a nonzero cell at or beyond +10,000. The largest right edge across records 1 through 3,135 was +9,997. At record k the right edge is k+2 plus the length of the suffix trimmed of trailing zeros. The checkpoint has 6,867 suffix cells, head −6,273, and a 3,166-bit raw clock. [Physical record](runs/line18-returns.json)

## Reproduction

An independent suffix replay groups up to three tiles into a strip. It traces the literal instructions until the full strip state repeats, counts the child requests, and resolves the first exceptional reply in chronological order. This reconstructs the saved suffix and raw clock using the same verified left header. The command below checks any saved odd-record checkpoint.

From `research/bb2x5`, replay the endpoint from the initial blank tape.

```sh
python3 frontiers/line18.py --record 3136 --checkpoint /tmp/line18.json
cmp /tmp/line18.json frontiers/runs/line18-returns.json
python3 frontiers/check_line18_strips.py frontiers/runs/line18-returns.json
c++ -O3 -std=c++17 frontiers/window.cpp -o /tmp/bb25-window
BB25_WINDOW=/tmp/bb25-window python3 frontiers/test_line18.py
```

Add `--resume frontiers/runs/line18-returns.json` and increase `--record` to continue. The decimal record index and stored hexadecimal clock are absolute. From record 27 at step 9,306,778,039 the independent moving-window simulator reproduces the complete tape, head and state in the original 10-billion-step checkpoint.
