# Line 34 · a delayed source of guard debt

For `1RB2LA4RA1LA3LA_0LA2RB3RB2LB---`, a change confined to the interior of the epoch-52 tape can produce **2,989 successful sweeps with the same guard history as blank, followed by B4**. In an explicit infinite family of such tapes the exact time to B4 is $2,258,780,781 + 498,942k$ defined instructions from the modified checkpoint. The blank machine survives this sweep. The two runs also agree at cuts 9 and 12 throughout those 2,989 sweeps. This gives a test for proposed finite-history proofs and a way to recognize a dangerous periodic region. The blank-tape outlook remains **Unknown**.

## A transfer rule for arbitrary surroundings

Use the physical digits 1 (opening), 3 (closing), and 2 (neutral). Write `b(P)` for openings minus closings in a word P, and `h(P)` for the maximum excess of closings over openings among its prefixes, including the empty prefix. The suffix to the right of a cut supplies a nonnegative debt d. Greedy matching in P leaves exactly

$$f_P(d)=\max(h(P),d-b(P))$$

units to its left. This follows by splitting the prefixes of P followed by the exterior at the end of P. It applies to an arbitrary finite exterior and has no time-history assumption.

If a period P has positive balance B, the map has the unique stationary value H = h(P). With d = H on the right, mark an opening as surviving precisely when its immediate right-hand debt is zero, carrying the debt backwards through the period. One pass produces exactly B surviving openings and returns debt H to the left. The next ordinary word has digit 1 for equal neighboring survivor bits, 3 for a rise and 2 for a fall. Wrapping the last bit around to the first defines the next periodic word. [Physical sweep and clock](target34.md)

There is a quantitative bound on influence from the edge of a repeated region. If the actual exterior sends d, let s = 0 when d = H, and otherwise take

$$s=\max\left(1,\left\lceil(d-H)/B\right\rceil\right).$$

For every positive j, the j-fold map gives $f_P^j(d)=\max(H,d-jB)$. Hence after s copies the debt equals H. In a region consisting of q copies, the other q−s copies have the stationary survivor mask when q ≥ s. The derivative at the leftmost cell still depends on the bit from its left neighbor. If the sweep succeeds, at least $\max(0,q-s-1)$ complete copies therefore update to the periodic successor in their ordinary physical positions. This bound uses no assumptions on the word to the left. Earlier halting already ends the calculation.

A sharper test can permit every copy to update. At each of the two ends of a period, record the pair consisting of the suffix debt and the survivor bit immediately to the left of that cut. If both pairs equal the stationary pair, all copies supply the same returning debt and entering bit. Inserting any number of further copies then preserves every other digit, the guard and the terminal action, and inserts exactly as many copies of the next period. This step can be iterated even as the period changes.

## An infinite family with a finite failing sweep

The blank prefix of 5,924 instructions gives epoch 52 with A at −52 and a 65-cell word. Preserve its first 50 and last 15 cells and insert **3,600 + k** copies of

```text
21112212211221111212121112211122211121112111112
```

between these two pieces, for any integer $k\ge0$. This defines a family of deliberately modified tapes. It does not describe how blank could acquire such an insertion. The base case uses k = 0. Take its central cuts immediately before and after copy 1,801.

For each of the next 2,989 successful sweeps, the physical period between the central cuts agrees with the circular calculation. Its balance is at least eight. At both central cuts the actual debt and preceding survivor bit agree with the stationary pair. All four quantities are checked afresh at each epoch. Induction using the transfer rule proves the same successful history for every k. The cut indices increase by the length of the new header to keep following the same physical cells. At every one of those epochs the true blank continuation has identical guard, cut-9 and cut-12 debts. At least its first 19 digits agree with the altered tape, including at the start of the failing sweep.

The period then equals

```text
31232131232132321312321312321312321312321312321
```

and its balance is −1. On the base altered tape the whole-word debt is **480**. On the genuine tape it is **2**. Inserting k more copies cannot reduce the maximum prefix excess. Prefixes ending before the insertion keep their excess, and corresponding prefixes extending past it gain k. The pre-existing 480 already exceeds the physical halt threshold of six. Thus every member of the modified family first fails on sweep 2,990 from the altered checkpoint. The current record does not establish any of those tapes on blank. The literal way a sixth unpaired closing reaches B4 is the same as in the [left-guard calculation](line34_left.md).

The exact number of defined instructions **through the 2,989 successes** is

$$1,816,430,783 + 498,942k$$

from the modified checkpoint. This excludes the failing sweep. Per extra period of width p and positive balance B, let $D_P$ be the sum of its stationary debts over the p cuts immediately before its cells. The outward and return traversals contribute 2p instructions, the matched excursions contribute $2D_P$, and the B surviving openings contribute $2B$ return moves. The unchanged header and terminal actions add no difference. Applying the exact sweep clock and summing gives the stated coefficient. The final failing sweep costs exactly **442,349,998** further defined instructions for every k. A separately implemented literal interpreter executed the entire base tape through B4. It compared all 172,923 cells, state, absolute head and time at the last successful checkpoint. In the failing sweep it reached no coordinate greater than 143,739. The insertion cut at this checkpoint is at physical coordinate 84,599. From there through coordinate 166,062 inclusive, the base tape agrees with an infinite repetition of the final period. Inserting k whole copies thus preserves the initial contents of **every** tape cell the base terminal trace reads. Determinism gives the same complete terminal trace up to B4 at head −3,043. A second literal run with k = 1 checks the whole predicted intermediate tape and final time as well.

Consequently the exact halting time from each altered checkpoint is **$2,258,780,781 + 498,942k$**. All these clocks start after the intervention. They supply no numerical probability or stopping-time estimate for blank.

## A backward search using finite windows

I also tried to prove that a deficit of six has no arbitrarily deep predecessors among ordinary interior factors. For a width $w$, begin with all $2^w$ possible survivor masks. An old mask and a left boundary bit determine $w$ ordinary digits. Match those digits first with zero debt at the right, then admit every entering debt by deleting rightmost surviving openings in succession. Keep all masks produced and repeat until the set stays fixed. This is an exact calculation for the abstraction that chooses the two exterior inputs freely at each sweep. The rule covers every actual interval that has been ordinary data over the generations in question.

| Width | Masks at closure | First pass identical to preceding pass |
| ---: | ---: | ---: |
| 12 | 2,235 | 3 |
| 15 | 12,604 | 3 |
| 18 | 68,999 | 4 |
| 21 | 369,956 | 5 |

At each width, the limit admits every cyclic factor of the survivor sequence producing the negative 47-cell period above. A tape repeating this sequence passes every such local membership test, yet its derivative has one excess closing per period. Hence this abstraction cannot give a uniform bound on the debt of the ordinary middle. A proof using selected histories from the blank seed, boundary correlations, or restrictions on the order of larger intervals has different information available. [Independent finite checker](back34_windows.cpp)

## Checking the actual tape

The screen checked every 47-cell interval at genuine epochs 52 through 3,041 inclusive, and every rotation of each of the 2,990 successive periodic words. It found 71 matches of a full period. The longest single stretch was **52 cells**, at zero-based offset 296 of epoch 977. It agreed with phase 2,974 rotated by 28 cells. A separate screen of the saved epoch-125,000 blank checkpoint found three 47-cell matches. The longest was 48 cells. All these stretches are shorter than two complete periods. Local resemblance alone does not supply the repeated region needed by the transfer theorem. [Epoch-125,000 checkpoint](target34_checkpoint.json)

## Replay and next step

Run from the repository root with Python 3.10 or later and assertions enabled.

```sh
c++ -O3 -std=c++17 research/bb2x5/halting-outlook/back34_literal.cpp -o /tmp/bb34-literal
python3 research/bb2x5/halting-outlook/back34.py --literal /tmp/bb34-literal
c++ -O3 -std=c++17 research/bb2x5/halting-outlook/back34_windows.cpp -o /tmp/bb34-windows
/tmp/bb34-windows
```

[Transfer and checkpoint checker](back34.py) · [Independent literal interpreter](back34_literal.cpp) · [Verification output](back34-verification.txt). The script checks the epoch-52 seed against the literal interpreter with its absolute head, entire tape and raw time. Two independent small controls insert 50 and 51 copies of an 11-cell period. At each of ten successful sweeps it compares the complete physical configuration and raw clock to the literal interpreter, then follows literal execution to B4. Their halting times from the modified checkpoint are 38,830 and 39,216. The measured difference of 386 agrees with the per-copy clock. The larger certificate uses the previously [literal-tested sweep](target34_orbit.py) and a separate scalar circular matching rule. Each step checks the real guard before advancing. No proof assistant has checked the new transfer calculation.

A proof using guard history alone must account for two executions with 2,989 identical observed debts and differing next outcomes. A more discriminating next step is to bound the total length of segments on the actual tape that can maintain the stationary debt and bit across multiple cuts, relative to the openings available to their left. The transfer formula gives the exact right-hand debt and the minimum number of copies shielded at one step. The evidence above tests one family and leaves that all-time bound open.
