# Timed left sweeps on line 9

The machine `1RB---4RB2RB4LA_2LB3LA3LB0RA0RB` reaches its first left extension after three defined steps. At extension $n=1$, A scans coordinate −1, and cells 0 and 1 contain `32`. The simulator records later extensions when the head is in A on the virgin blank at −n, the next cell contains 3, and the n cells after it through coordinate 1 all contain 2. The record stores the remaining word starting at coordinate 2. Cells outside the header and the stored suffix are blank.

## One sweep

A0 writes a guard 1. B3 on the next cell leaves 0 and sends A to the twos. For each pair `22`, the instructions A2, B2, B4, B3 leave `00` and send A right. Define a suffix request as the run beginning at coordinate 2 and ending on its first exit back to coordinate 1.

| Length of the twos | Requests to the suffix, in order |
|---|---|
| Even | A |
| Odd | B, B |

For even n the last full pair sends A directly to the suffix. For odd n, A2 on the unpaired two leaves 4 and sends B to the suffix. On a B reply, B4 changes that 4 to 0 and sends the second B. If every requested reply is B, the return crosses n+1 zeros using B0, then B1 changes the guard to 3 and sends A onto the next blank. This establishes the same header at extension n+1.

There are $3n+4$ instructions outside the suffix in either case. They consist of two startup steps, four per full pair, two extra steps if n is odd, and n+2 return steps. The first odd sweep followed by the first even sweep therefore supplies BBA to the suffix. After k such two-sweep cycles, startup and the physical left sweeps have cost $3+6k^2+11k$. Raw time also includes every defined step in the suffix.

## Batching at coordinate 2

An ordinary cell receives A or B from its left. Conditional on B replies to every child request it sends to its right, the following table gives its ordered requests and final digit. Each listed row exits to the left in B. These paths are direct applications of the machine instructions.

| Digit | Incoming | Requests to the next cell | Final digit |
|---:|---|---|---:|
| 2 | A | BB | 2 |
| 3 | A | B | 3 |
| 2 | B | empty | 3 |
| 3 | B | A | 2 |
| 0 | B | empty | 2 |

The simulator passes an entire finite word through each cell, preserving the order and the digit changes between requests. It stops once the emitted word is empty. At that point all replies assumed at the deepest cell are accounted for, and induction back to coordinate 2 accounts for every reply at the other cells. If a cell emits j requests, it takes j steps to send them and one to exit left per incoming request. Summing across cells gives the suffix clock as the root request count plus twice the sum of all emitted word lengths.

BBA repeated a power of two times has a short representation by concatenation. Equal subwords share a node, and the ordered image of a node in each starting digit can be reused. Encountering A on a virgin zero or reaching the node limit discards the provisional batch. The simulator then halves the batch. At one cycle it can execute all three root requests with the elementary suffix interpreter, which follows the actual states returned by deeper calls. Both a wrong-state return across coordinate 2 and a literal work limit stop the calculation. Only completed cycles enter a checkpoint.

## Reproduction

From `research/bb2x5`, the following commands recreate the finite run and compare with elementary execution and the saved ten-billion-step simulation.

```sh
python3 frontiers/line9.py --cycles 33554432 --checkpoint /tmp/line9-sweeps.json
cmp /tmp/line9-sweeps.json frontiers/runs/line9-sweeps.json
python3 frontiers/test_line9.py
```

Pass `--resume frontiers/runs/line9-sweeps.json` and a larger absolute cycle count to continue. One cycle completes two left extensions. The test starts an independent elementary interpreter at the old moving-window checkpoint and meets the new calculation at cycle 40,822, comparing every cell, the head, state and raw time. Smaller checks compare the cell table, the first hundred cycles from blank, and different batch partitions. The recorded 33,554,432 cycles reach 6,755,400,984,549,769 defined steps. The head is in A at −67,108,865, and the word from coordinate 2 has 133 digits. The blank-tape halting question remains open.
