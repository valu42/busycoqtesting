# Line 33 · When the mixed-digit counter can first return in B

`1RB2LA0RB4LB1RA_1LA3RA1RA---0LA` · **Unknown** · 2026-11-18

The blank execution reaches its 33rd left extension after approximately **6.0015102 × 10^12573 defined instructions**. The checkpoint contains the exact clock and all 178,032 nonzero cells. A timed recurrence reduces each successful left extension to a single request on a finite word. The first possible departure from the recurrence is an A request on a lone final 2. Every completed B reply leaves a pure (421)^k suffix. A B reply to 21 triggers B3, and a B reply at the outer extension enters a proved infinite sweep pattern. These derivations and the native replay have no formal verification.

**Attribution.** The [starting simulation](../SIMULATION_TABLE.md) records 10^10 instructions. The [community list](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved) attributes the mixed-digit shift-overflow description for this exact string to [hipparcos](https://discord.com/channels/960643023006490684/1436181033992327333/1436181033992327333) and [mxdys](https://discord.com/channels/960643023006490684/1259770421046411285/1436151075450130443). Those Discord posts required JavaScript and their underlying arguments could not be inspected here. The derivation, timings and checks below were obtained independently for this pass.

## Established return rules

A word denotes cells from left to right, followed by virgin zeroes. A request starts in A on its first cell and ends on the first move across its left edge. Let F(w) denote the output of the ordinary rules below, all of which return A. Outside that domain the actual machine still has a well-defined execution. The table gives the local cost in addition to all listed child costs. A power of F means successive requests on the evolving suffix.

| Input | Output | Local cost | Instructions responsible |
| --- | --- | ---: | --- |
| empty | 21 | 3 | A0, B0, A1 |
| 1w | 2w | 1 | A1 |
| 4w | 2 F(w) | 2 | A4 calls right, A1 exits after reply |
| 21w | 14 F(w) | 4 | A2, B1 suspend 03, then A3, B0 |
| 22w | 22 F²(w) | 7 | A2, B2 suspend 01. A1, A0, B2 launch the second request, then A1, A1 exit |
| 24w | 21w | 5 | A2, B4, A0, B0, A1 |

The formulas follow by reading these instructions in chronological order with the child execution inserted at each call. Induction over a finite successful evaluation composes the physical paths, including the clock. The `21 → 14 → 24 → 21` cycle uses ten local instructions and one child request per three inputs. Each request on 22 passes two requests to the child and restores 22. When a child is never requested its tape stays in place. These are the batching rules in [neglected33.py](neglected33.py).

**Connecting the recurrence to blank.** At step 3 the head in A is on the first fresh left cell, coordinate −1, followed by `21`. Write an extension as A on fresh −j, with exactly `2y` to its right and blank exterior. A0, B2 turn the first two cells into 11 and send A into y. If the request returns ordinarily, A1, A1 turn those two cells into 22 and enter fresh −j−1. Consequently **y₁ = 1** and **yⱼ₊₁ = 2 F(yⱼ)**. The interval between these specific opportunities is exactly four instructions plus the full cost of F(yⱼ).

**First exception.** The cases exhaust any finite word over 1, 2, 4 except a solitary 2. A request on that word exits left in B in precisely 19 steps and leaves `421421`. A successful evaluation cannot conceal a halt. The batch evaluator stops when it demands this exceptional rule. A native batch can evaluate disjoint costs in a different order, so it reports the affected epoch without assigning an exception clock. For example, an exceptional B reply to the first child of 21 immediately scans the suspended 3. A request on the artificial word `212` therefore encounters B3 after 21 defined instructions. Whether any exceptional request occurs on blank, and what its caller is if one occurs, remain open.

The local traces also give a necessary condition for a finite blank halt. Follow the chronological depth-first interpretation of the return rules. Before the first exceptional demand, each local instruction is defined and every completed child replies in A. An infinite descent of requests would itself be an infinite execution. Thus every finite halt requires the solitary-2 demand somewhere on its path. Its occurrence alone leaves the caller's fate open.

## A replaceable suffix and its cost

Let C = 421. The substitution w ↦ w C^k has an exact effect on **every ordinary finite calculation**. If F^n(w) = v ordinarily, then F^n(w C^k) = v C^k and the extra cost is **3k (|v| − |w|)**. The proof starts at a virgin suffix. The 4 and 21 rules give F(421u) = 214 F(u) at six local instructions. Thus F(C^k) = (214)^k 21 = 21 C^k in 6k + 3 instructions. Substitute this for each base case F(empty) in the finite derivation. All other local actions and child requests persist. Each base case grows the word by two, which counts exactly how many substitutions were made. Also, F^n(empty) exists ordinarily for every finite n. The first call builds 21, and the pair cycle reduces the remaining batch to strictly fewer requests on its virgin suffix.

This gives a way to measure the number of protective terminal blocks actually needed. Write y = p C^k with k maximal. Add C blocks to p until F(p C^m) first succeeds, producing u. The measured next reserve is k − m plus the number of terminal C blocks in 2u. Both the resulting word and the extra clock can be cross-checked against a full evaluation. On the blank execution the reserve falls from 8 to 7 across extension 12. It falls on **three consecutive stages** from 11 to 10 to 9 to 7 across extensions 17–19. Each of those last three stages requires two supplied blocks. The prefix cannot be discarded on the strength of a large reserve alone. For instance F²(42421) and F⁵(42142421421) demand the exceptional branch, despite one and two terminal C blocks respectively. These two examples use freely chosen input tapes.

The order of the left actions also matters. Start from the **actual** extension-3 word y = 2221421. Let P prepend a 2. The free sequence P,P,F,F,P,F,P yields 2222222222221242421, whose next F needs the exceptional branch. Blank uses F followed by P at every stage. An invariant that grants arbitrary interleaving of these two operations and requires every evaluation to be ordinary already fails from this real checkpoint.

## All exceptional replies and an infinite sweep pattern

**Theorem.** For an A request on *any* finite word over 1, 2, 4 with virgin zeroes to its right, every finite left exit in B leaves exactly C^k, where C = 421 and k ≥ 2. The part to the left of the entry is untouched. Every finite halt in such a request occurs at a 21 prefix receiving B from its child, possibly within nested calls. This describes finite outcomes and does not require an assumption that every request exits.

Prove both statements together by induction on the elapsed physical instructions in a completed or halting request. The direct solitary-2 trace exits B and leaves C². The cases empty, 1 and 24 exit A. For 4, 21 and 22, use the ordinary table until a child halts or returns B. A child halt propagates immediately. A returning child has a shorter execution than the parent, so its B reply leaves C^k by induction. Subsequent A calls on that suffix return A as long as required: the first gives 21 C^k in 6k+3 instructions and the second gives 14 21 C^k in 6k+7. The only additional paths at the parent are the following. The cost column excludes the first B-producing child and any earlier children, but includes the known later calls.

| Parent | Replies through the first B | Subsequent local actions | Final outcome | Remaining cost including earlier local instructions |
| --- | --- | --- | --- | ---: |
| 4 | B | B1 calls right, A3 exits left | B, C^(k+1) | 6k+6 |
| 21 | B | B on suspended 3 | Halt | 2 |
| 22 | B | B1 calls right, then A3, B0 exit | A, 1 C^(k+1) | 6k+8 |
| 22 | A,B | B1 calls right, A3, B1, A4 call again, then A1, A3 exit | B, C^(k+2) | 12k+21 |

In the last row the first ordinary child leaves 01 under the suspended calls; A1, A0, B2 turn that into 11 and launch the second call. After its B reply, the six listed local instructions turn 11 into 42. The final suffix is 14 21 C^k and the combined word is C^(k+2). The other rows follow by reading the suspended cells 1, 03 and 01 respectively. These cases exhaust every route because the known calls after an exceptional reply terminate in A. The [scalar evaluator](neglected33.py) implements this full table separately from the ordinary batched evaluator.

**Blank-extension consequence.** At an outer extension a finite A exit still gives the next y by prepending 2 to the output, including after an internal recovery. A finite halt still identifies the nested 21 whose child returned B. If the *outer* request returns B on C^k, its left context is precisely the suspended 11, with virgin zeroes farther left. The last-row six-instruction handler turns the context and suffix into C^(k+2) and exits left in B. Thus the head scans a virgin zero in B with a pure C-power to its right.

For every r ≥ 2 this last configuration advances to another of the same shape, two cells farther left with exponent r+2, in **12r+18 instructions**. In order the local instructions are B0, A0, B1; an A request on C^r; A3, B1, A4; an A request on 21 C^r; A1, A3. The two request costs are 6r+3 and 6r+7, and the eight local instructions give the stated clock. Induction proves nonhalting for this family. A literal illustration starts with the artificial tape containing only a 2 at coordinate zero and A scanning it:

| Raw clock | Head | State | Nonzero word, starting one cell right of head |
| ---: | ---: | --- | --- |
| 19 | −1 | B | 421421 |
| 61 | −3 | B | 421421421421 |
| 127 | −5 | B | 421421421421421421 |

The blank execution reached the extension-33 checkpoint without any exceptional demand or entry into this family. The artificial solitary-2 run and the halting 212 run illustrate two distinct reachable outcomes from other initial tapes.

## Reproduction and open problem

Run from this directory with Python 3.10 or later. The second command checks the exact integer, state, head position and complete decoded tape, including the known blank exterior.

```sh
python3 neglected33.py --verify
python3 neglected33.py --epoch 33 --check neglected33-checkpoint.json
python3 neglected33.py --epoch 24 --reserve
```

The independent literal interpreter compared 1,256 complete request results, including elapsed instructions, over every input word of length at most five and up to six successive calls. It stopped 222 of these input series at the first exceptional demand. For the full exceptional evaluator a separate exhaustive single-request comparison over all 1,093 words of length at most six found 1,037 A returns, 24 B returns and 32 halts. Every return matched the entire tape and clock and every halt matched the exact B3 clock. Another 31 comparisons checked complete infinite-family periods for r = 2 through 32. Two further literal controls verify the solitary-2 B return and the 212 halt. Ten full blank checkpoints through step 272,898 matched the interpreter. The larger [checkpoint](neglected33-checkpoint.json) is at coordinate −33, with its first nonzero cell at −32. Its exact clock has 12,574 decimal digits. This finite result supplies no calibrated stopping distribution.

**Next proof step.** Relate the number of blocks a prefix can demand *after the one-cell shift* to the number it can produce in later stages. The timed substitution permits a proof to track that balance on a shorter prefix while preserving the omitted suffix exactly. The observed three-stage loss rules out a stepwise monotonicity argument. A closed invariant guaranteeing that the reserve always covers demand would prove nonhalting. If this test exhausts the reserve on blank, continue with the full exceptional rules until a 21 halt, an outer B escape or a recovered A exit is found.
