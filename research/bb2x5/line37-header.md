# A fixed-cut condition for nonhalting on line 37

The exact machine is `1RB2LA3LA4RA1LA_0LA3LB3RB1RB---`. A normalized sweep starts with A on the blank immediately left of a word over 1, 2 and 3. The next undefined instruction is reached precisely when at least two closings remain unmatched in this word. Symbol 2 is an opening, 1 a closing, and 3 is neutral.

**If the suffix to the right of the first 45 digits always has at most four unmatched closings, the machine runs forever from blank.** The largest value through 200,000 epochs is two. Establishing an all-time bound at this cut remains open.

For a cut immediately after the first L digits, let d(L) be the number of unmatched closings in the suffix to its right. Equivalently, d(L) is the largest number by which closings exceed openings in a prefix of that suffix, including the empty prefix. If the blank machine ever halts, each row of the following table gives a necessary earlier-or-current event in an epoch numbered at least 91.

| Event required by a halt | Distinct reachable safe prefixes in the bounded model |
|---|---:|
| d(45) ≥ 5 | 58,302 |
| d(j) ≥ 6 at some j from 0 through 40 | 26,007 |
| d(j) ≥ 7 at some j from 0 through 48 | 196,262 |

Equivalently, an all-epoch upper bound excluding any one row's event would prove nonhalting. These are conditional implications. A large matching debt far to the right need not reach any of the cuts in the table.

With d(45) ≤ 4 the finite graph proves more. Every reachable prefix has a unique phase modulo 11 corresponding to its input epoch number. Every edge out of phase 1 uses one guard reset, and every edge out of any other phase uses none. An ordinary sweep grows the word by two cells and one reset adds three more, giving exactly 25 cells of growth per 11 sweeps under this condition.

## Exact finite calculation

Use the digit map D and survivor bits of [the right-suffix derivation](line37-pascal.md). For a prefix P and candidate debt d arriving from its right, scan P right-to-left with this debt, canceling 1 against 2 and marking every surviving 2. The final debt H is the number of unmatched closings in the entire word. With H≥2 the machine halts. With H=0 the returned word starts with `2`. With H=1 the single guard reset makes the returned word start with `2122`. In both cases these header digits are followed by D(sᵢ₋₁,sᵢ) for each digit of P, taken left to right, with the initial bit zero. This follows directly from the outward sweep: a reset adds the wall (1,4), the new guard 1, and the consumed old guard rewritten as 1. These four old symbols yield `2122` on the ternary return. The initial header supplies no carry into the first old data digit in either case. Thus P and d determine the new prefix of the same length and whether this epoch halts.

Start from the true prefix at epoch 91, reached by 91 successful word sweeps from blank. Enumerate the finite reachable graph, trying every integer d from zero to the listed cap at the exterior cut. For the two rows imposing an interior cap, discard a choice only when the exact scan exceeds the cap at a listed cut. Every actual run satisfying the cap appears in this graph by induction. The search exhausts the reachable prefixes and has no halting edge. A run violating the cap can first leave the graph at the epoch of that violation.

The checker computes once the survivor mask for d=0. Increasing d by one removes the rightmost surviving opening if any, then increases H after those openings run out. To check every interior cap efficiently, at each intermediate position the debt from d is the maximum of (i) the debt there from starting at zero and (ii) d plus the excess of closings over openings scanned so far. This follows by induction from the one-digit reflected update. It suffices to track the peaks of those two quantities.

Run `python3 line37_header.py`. The finite graph search is preceded by a comparison against `word_sweep` for all prefixes of widths four through six, initial debt caps zero through three, and both versions of the interior cap. Each candidate d is realized by appending d closings and one terminal opening.


## Checking the cut on the blank orbit

At epoch 200,000 the word has 454,542 digits. There were 18,181 guard resets in the sweeps that produced it. Over every word long enough to contain cut 45 up to and including this epoch, the maximum debt at that cut was two. Epochs count completed sweeps from blank. The following command reproduces the finite run with Python 3.10 or later.

```sh
python3 line37_orbit.py --epochs 200000
```

The runner represents openings and closings by two integer bit masks, with the rightmost cell at bit zero. One matching pass uses a slot that holds one pending closing. At a closing the slot fills, at an opening it empties, and at a neutral it keeps its state. A closing that meets a full slot and an opening that meets an empty slot pass to the next slot. A closing enters some empty slot, and an opening consumes a closing if any slot holds one. The number of occupied slots at any cut is therefore the usual matching debt. Openings that pass every slot are exactly the survivors. Each pass removes at least the first remaining closing, so the calculation terminates on every finite word.

For opening and closing masks O and C the incoming carries of the binary addition C + (~O) are the occupancies just before each cell. At a closing both addend bits are one, at an opening both are zero, and at a neutral their sum is one. XORing the addition result with both addends extracts the incoming carries, including the carry just beyond the last cell. This also gives the debt at cut 45 without materializing the individual digits. The runner checks its digit masks, all cut debts and the next complete word against the existing sweep on every word of length at most seven ending in 2, including words that halt.
