# Line 34: how much unmatched tape reaches the guard?

**Machine** `1RB2LA4RA1LA3LA_0LA2RB3RB2LB---`. **Outlook: Unknown.** Six unmatched closings in a sweep halt this machine. The new results isolate a necessary event in a particular suffix and measure it in the blank run. The exact clock now reaches **33,919,375,494 defined instructions**. An all-time nonhalting proof remains open.

At a sweep boundary A is on the blank just before a word of opening (1), neutral (2) and closing (3) cells. Each closing matches the nearest available opening to its left. The **debt** of a word is the largest excess of closings over openings in any prefix, including the empty prefix. Write $d(j)$ for the debt of the portion strictly after its first $j$ cells, and $H=d(0)$. The inherited [sweep reduction and literal interpreter](../prior_sweeps.py) show that $H\ge6$ reaches the undefined instruction B4. When $H<6$ the sweep finishes in finite time.

## Proof target

From the actual seed the left prefix has only 65 possibilities in the nine-cell calculation that allows arriving debts zero through five. The prefix is safe on every edge. **If line 34 ever halts, then at some earlier or current sweep the suffix after cell nine has debt at least six.** The [left-boundary report](line34_left.md) also gives a sharper test at cell twelve on the failing sweep itself. The [right-boundary report](line34_right.md) proves a timing law for successive extensions at that end of the tape. All new proofs here are on paper with executable checks. The transfer from the interior to the left cut is the missing step.

## Exact clock for one successful sweep

Index the old data from 1 to $w$ and the original left guard by 0. Let $S$ be the number of surviving openings. A closing at $i$ matched at $j$ consumes $2(i-j)$ extra instructions on the outward traversal: B moves left over processed cells to the match, then retraces them to resume the rightward scan. Assign unmatched closings temporarily to guard 0. Summing these distances counts each intervening cut once per active match and gives $D=\sum_{j=0}^{w-1} d(j)$. The baseline outward cost is $w+2$, including A0 and the far B0 turn.

A third unmatched closing triggers the reset. B scans the processed part back to the old guard. Compared with reflection at position 0, it enters the blank on its left; the short wall-building path adds 16 instructions. Any fourth or fifth closing matches one cell beyond the original guard and adds two further instructions. In the guard's coordinates the third reflection starts B at 0 on symbol 3, with blanks to the left. The first return to coordinate 1 in B takes 17 instructions: B3, B0, A0, B0, A1, A0, B2, B0, A3, A1, A0, B2, B1, B0, A2, A0, B2. Ordinary reflection there takes one. The new guard is at −1. Thus the outward subtotal is

$$w+2+2D+16[H\ge3]+2\max(H-3,0).$$

The return visits the processed data and a guard header of length $h$, one or five cells according as $H<3$ or $H\ge3$. Before conversion the header is $g$, or $(1,3,4,g,3)$, with $g=1,2,3$ for $H\bmod3=0,1,2$. The ternary order is $(3,1,2)$. Add the carry from the previous cell to the cell's one-based index in this order (base zero for the wall 4), output the digit at that residue modulo three (zero-based), and pass the quotient. Let $K$ count outgoing header carries. Each surviving old opening sends one further carry. In physical return order every such carry uses an extra right/left pair. A final carry into blank uses one additional pair to append a cell, recorded by $e=1$; otherwise $e=0$. The return subtotal is

$$w+h+2(S+K+e).$$

The new head coordinate is the old one minus $h$. The code constructs both symbol masks of the entire new word and stops on $H\ge6$ before issuing any successful-sweep shortcut.

## Blank-orbit measurement

| Completed sweeps | Width | Cumulative raw instructions | Raw length of last sweep | Largest $d(9)$ so far |
| ---: | ---: | ---: | ---: | ---: |
| 1,000 | 1,216 | 2,165,440 | 4,365 | 2 |
| 10,000 | 12,174 | 217,034,068 | 43,467 | 2 |
| 50,000 | 61,003 | 5,430,974,000 | 217,461 | 2 |
| 100,000 | 121,869 | 21,709,277,756 | 434,937 | 2 |
| 125,000 | 152,334 | 33,919,375,494 | 543,007 | 2 |

All successful input epochs from 52 through 124,999 followed the same 13-phase guard pattern. The largest debts at cuts nine and twelve were both two. The smallest gap between the true cut-twelve debt and its exact halting threshold was four, first reached at epoch 51. Greater debt occurs elsewhere. At epoch 14,117 at least one cut carried six units; that tape completed its sweep. Both extrema persisted on the later portion of the run. A halting hazard inferred from the frequency of large debts anywhere would count safe events. The data provide no probability of a future sufficiently large debt at the guard.

## Reproduction

From the repository root:

```sh
cd research/bb2x5/halting-outlook
python3 target34_orbit.py --epochs 125000 --output /tmp/line34-replay.json
cmp /tmp/line34-replay.json target34_checkpoint.json
```

[Timed sweep and literal audit](target34_orbit.py) · [Complete checkpoint and cumulative histograms](target34_checkpoint.json). The bit-parallel matching borrows the [line 37 slot construction](../line37_orbit.py), with a new clock, header and digit maps. A slot stores one unmatched closing while reading from the right. The occupancy masks at all slots count $D$ by population count across the $w$ cuts. The audit checks all 3,280 words through width seven, including ten halting words, and the full state, head, complete tape and raw count at 180 successive blank boundaries. The counter agrees there at step 71,630. The machine at the saved endpoint is in A at −125,000. The checkpoint encodes the entire finite word by its width and two hexadecimal masks, with the remainder of the tape blank.

A next step is to use relations between the phases of nearby cuts to bound debt reaching cells nine or twelve. A proof must allow large interior debts and explain why they cannot travel far enough to exhaust the left prefix.
