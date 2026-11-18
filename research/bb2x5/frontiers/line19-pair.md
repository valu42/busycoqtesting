# Lines 19 and 23 share a transition table after reflection

Reflect the tape about the origin, exchange A and B, and relabel the digits as follows.

| Original | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| Reflected | 0 | 2 | 1 | 4 | 3 |

Each of line 19's ten instructions becomes the corresponding instruction of line 23 under this transformation, including the missing A3 instruction, which becomes B4. For example, line 19 A0 writes 1 and moves right in B. Line 23 B0 writes 2 and moves left in A. The transformation commutes with every defined step. It preserves the clock, negates the head position and maps an occupied interval $[l,r]$ to $[-r,-l]$. Applying it twice recovers the original configuration. The [checker](line19_pair.py) verifies each instruction against the pinned list.

Both listed machines start in A. **Simulate line 19 from blank A for line 19, and from blank B for line 23.** Reflect the second result back before recording its physical tape. Each seed has its own guard counts. The [paired runs](spaghetti-guards.md) use this correspondence.

## A family of halting and returning controls

Use line 19 coordinates. Let A scan the 0 of a tape beginning `03` followed by $m\ge1$ copies of 2, then a suffix $U$. No restriction is needed on the tape to the left. The guard sends exactly one B request into $U$. If the request returns to its caller, the two possible outcomes are as follows. Local steps in the table exclude the steps spent in $U$ and count only defined instructions.

| Response from $U$ | $m$ | Guard outcome | Local steps |
|---|---|---|---:|
| A | even | Halt on A3, one cell right of the initial 0 | $2m+8$ |
| B | odd | Halt on the same A3 | $2m+8$ |
| A | odd | Exit one cell left of the initial 0 in A | $2m+6$ |
| B | even | Exit to the left in A | $2m+6$ |

To verify this, keep the first 2 with the outer `03`. Each additional 2 receives B, sends one B to its right, flips the reply and exits left. The two local instructions leave a 2 on an A reply and a 0 on a B reply. The outer `032` has just two paths. A child reply of A leaves `332` and exits left in eight local steps. A child reply of B leaves `233` and encounters A3 in ten. Composing $m-1$ flips gives the table. A request into $U$ that halts or runs forever stops the caller there.

For example, B on a 0 returns A in one instruction, so `03220` halts after 13 defined steps. B on `20` returns B in three instructions and exercises the other response. The guard-predecessor proof excludes `032` at the launch of a genuine blank-orbit guard, for both seeds. These manufactured configurations give positive and negative tests for the simulator. [Blank-orbit guard analysis](spaghetti-guards.md)

## A surviving prefix can hide the deciding digit arbitrarily far away

At a blank-orbit launch with `03` under and to the right of the head, the suffix beginning two cells farther right satisfies additional [prefix restrictions](line19-guard-filter.md). Consider the surviving four-digit prefix `3022`. On any tape beginning **`0330` followed by $m$ twos and a 0**, with $m \ge 4$, the guard has the following two literal outcomes. All cells beyond the final 0 can have arbitrary values.

| Number $m$ of twos | Outcome | Defined steps |
|---|---|---:|
| Even | Returns left in A | $2m+15$ |
| Odd | Halts at the original guard's A3 | $2m+37$ |

Keep the first seven cells `0330222` together. They first request B on the remaining $n=m-3$ twos and the 0. The 0 answers A, and each 2 flips its child's answer. This costs $2n+1$ instructions. For odd $n$ the seven cells receive B and exit left after 20 local instructions. For even $n$, which is at least two, the outermost remaining 2 receives B, writes 0 and exits in A. The seven cells call again in B. The newly written 0 returns A in one step. These two A replies make the seven cells halt after 41 local instructions. All local paths are checked against the literal rules.

For any fixed number of visible cells, choose consecutive even and odd values of $m$ larger than that number. The two launch tapes agree throughout the visible region but only one halts at this guard. This explains why a universal decision for `3022` needs more information than a bounded launch prefix. Neither seed produced a `3022` launch through 100 billion steps. Reachability of these artificial tails on the blank orbit remains open.

### The same obstruction for the common `3233` class

Line 19 actually launched on `3233` **31,531 times** through 100 billion steps. There is a family with this prefix that agrees for arbitrarily many cells before the deciding digit. Let $P=$ `033233202332020030`. Start in A on the first 0 of $P$, followed by $m \ge 11$ twos and a 0. Everything past that 0 is arbitrary.

| Number $m$ of twos | Outcome | Defined steps |
|---|---|---:|
| Even | Returns one cell left of $P$ in A | $2m+471$ |
| Odd | Halts on A3 at the original guard | $2m+205$ |

After 140 steps the first B call enters the run of twos, leaving $P$ rewritten to `121444441444444414`. This call takes $2m+1$ instructions. When $m$ is even it returns A and leaves an alternating word starting `02`. When $m$ is odd it returns B and the alternating word starts `20`. This follows from the single-cell flip rule applied from the rightmost 2 to the leftmost. In each case the first eleven of these symbols suffice to finish: literal replay stays within them and takes 330 further instructions for the left exit or 64 for the halt. The checker verifies the three finite parts separately. The observed `3233` launches establish reachability of the four-symbol prefix. Reachability of the full artificial tails remains open.

## One-cell controls from both real blank runs

These controls first execute the original table from blank to a guard, then fork its configuration. The fork changes exactly one cell and leaves both of the guard's first two reply states and their clocks intact. In the original the third reply is B. In each altered tape it is A and A3 is reached two instructions later. Coordinates in this table are normalized to line 19, including the B seed for physical line 23. Reply clocks are relative to the unaltered launch configuration.

| Physical line | Launch clock and head | Alteration | Three original reply clocks | Three altered reply clocks | Halt on the altered tape |
|---|---|---|---|---|---|
| 19 | 716,152 at −168 | Cell −137 changes from 2 to 0 | 49, 55, 235 | 49, 55, 295 | A3 at −167, 297 steps after launch |
| 23 | 52 at −4 | Cell 0 changes from 2 to 3 | 3, 13, 21 | 3, 13, 51 | Normalized A3 at −3, physical B4 at +3, 53 steps after launch |

In the line 19 control the deciding perturbation is 31 cells from the head. In the line 23 control it occurs four cells away. The literal tests reconstruct the starting tapes from their respective seeds before changing a digit.

From `research/bb2x5`, run the rule checks and the literal replay tests. The tests cover both blank seeds, both 10-billion-step window checkpoints, 20,000 more instructions from each transformed window, and both parity outcomes through $m=20$.

```sh
python3 frontiers/line19_pair.py
python3 frontiers/test_line19_pair.py
```
