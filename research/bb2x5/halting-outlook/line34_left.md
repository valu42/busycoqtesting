# Line 34 · the left guard of a potential halting sweep

The full string is `1RB2LA4RA1LA3LA_0LA2RB3RB2LB---`. On **the halting sweep itself**, the suffix following cell 12 would have to supply at least six unmatched closings. The exact threshold is six plus the balance of the first twelve cells. This follows from a finite graph of 352 prefixes starting on the blank orbit. No assumption about earlier suffix debts is needed. The remaining proof obligation is to rule out that much debt from the true suffix. No formal proof assistant was used.

## Inherited sweep and notation

At an epoch, A scans the blank immediately left of a finite word. Label its digits from 1 at the left. Symbol 1 is an opening, 3 a closing, and 2 neutral. A closing consumes the most recent unmatched opening to its left. The sixth closing with no available opening reaches B4. Every successful sweep reaches the next epoch in finite positive time. The physical derivation and literal interpreter are inherited. [Sweep model](../prior_sweeps.py) · [Original research log](../research-log.md)

For a word $P$, let $b(P)$ count openings minus closings. Its intrinsic debt is $h(P)=\max_U(-b(U))$ over its prefixes, including the empty one. Let $d(j)$ be the intrinsic debt of the suffix strictly after cell $j$. Splitting a word at $j$ gives whole-word debt $\max(h(P),d(j)-b(P))$. The argument below determines which values of $h(P)$ and $b(P)$ are possible at the guard.

## New finite guard certificates

Set $D(0,0)=D(1,1)=1$, $D(0,1)=3$, $D(1,0)=2$. For a prefix $P$ and candidate exterior debt $d$, match $P$ from right to left with starting debt $d$. Mark uncanceled openings by a survivor bit 1 and other cells by 0. The outgoing debt at the left is the guard debt $H$. If $H\ge6$ the sweep halts. Otherwise the physical output starts with the following header. The virtual bit is the left argument of $D$ at the first old cell.

| $H$ | Header | Virtual bit |
|---:|---|---:|
| 0 | 2 | 0 |
| 1 | 3 | 1 |
| 2 | 1 | 0 |
| 3 | 21321 | 0 |
| 4 | 21332 | 0 |
| 5 | 21311 | 0 |

To recover the header, take $g=1,2,3$ for $H\bmod3=0,1,2$. The outward sweep leaves raw guard $g$ when $H<3$, otherwise $1,3,4,g,3$. Applying the ternary return in order $3,1,2$ gives the six rows and the outgoing carry. Each old cell then produces $D(s_{i-1},s_i)$. All choices further right with the same $d$ have the same effect on the guard and the first $|P|$ output digits. An exterior of $d$ copies of 3 realizes the local calculation. These completions support enumeration of necessary conditions on blank execution.

| Cut | Blank seed | Exterior choices | Reachable prefixes | Consequence |
|---:|---|---|---:|---|
| 9 | Epoch 7, step 109 | $0\ldots5$ | 65 | If $d(9)\le5$ at all epochs from 7, the machine runs forever. |
| 12 | Epoch 10, step 210 | Every nonnegative debt | 352 | Every reachable prefix has $h(P)\le2$ and $b(P)\ge0$. Any halt in this epoch occurs exactly when $d(12)\ge6+b(P)$. |
| 16 | Epoch 13, step 361 | Every nonnegative debt | 2,149 | Every reachable prefix has $h(P)\le2$ and has a prefix of positive balance. A halt requires $d(j)\ge7$ at some cut $1\le j\le16$ in that same epoch. |

For the unrestricted graphs, increase $d$ until the first halting edge. Raising $d$ by one erases the rightmost survivor if there is one, and otherwise raises $H$ by one, so every larger choice also halts. Every *successful* continuation from any actual prefix therefore has its next prefix in the graph. Induction begins with the literal seeds. The width-16 implication follows by splitting at the positive-balance prefix, whose intrinsic debt is at most two. All epochs before the three seeds were checked literally. The bounds at widths 12 and 16 apply even after an earlier epoch with large exterior debt.

## New restriction on the size of a dangerous interval

A halt needs a contiguous interval after cell 12 with at least six more closings than openings. It must contain **at least ten closings in at least 23 cells**. More generally, a deficit of $E\ge2$ in that region needs at least $2E-2$ closings and $5E-7$ cells.

Trim the interval to the first and last closing. This can only increase its deficit. Suppose $g$ closings remain. In ordinary output every closing is a $0\to1$ boundary of the previous survivor bits and every neutral is a $1\to0$ boundary. Hence the trimmed interval has $g-1$ neutrals, and its deficit is $3g-1-L$ for length $L$. Its $g$ starts of one-runs in the *previous* survivor mask are separated by $g-1$ nonempty zero-runs. Each such gap contains some old closing or neutral. Its length equals twice its number of closings plus its number of neutrals, since its endpoints are separated from other gaps by surviving openings and all its other openings are paired. All old closings and neutrals between the first and last starts are in those gaps. They alternate, since that prior interval was also ordinary derivative output. The current interval lies after the first 12 cells and each of the two headers has length at most five. A terminal appended neutral may be dropped when trimming, and the last survivor in the preceding word is an opening. This keeps both uses of the ordinary rule inside data.

Thus the gaps together contain at least $g-1$ old closing-or-neutral cells and at least $\lfloor(g-1)/2\rfloor$ old closings. Including the $g$ survivors gives $L\ge2g-1+\lfloor(g-1)/2\rfloor$. Combining the two inequalities yields the claimed counts. The estimate concerns the width of a dangerous region, with no assumption about a random input or a stopping-time distribution.

## Replay and next step

Run from `research/bb2x5` with Python 3.10 or later and assertions enabled.

```sh
python3 halting-outlook/line34_left.py
```

The checker replays the complete physical configurations at the seeds, compares all 4,489 canonical choices at widths 9 and 12 to the literal interpreter, and checks 29,111 width-16 choices against the existing sweep implementation. The word graph deliberately allows independently chosen successive exteriors. A halting edge within that graph has no established realization on the blank orbit. [Checker](line34_left.py) · [Verification transcript](line34_left-verification.txt)

The next target is an upper bound on the actual exterior debt relative to $b(P)$ at cell 12. A proof could combine a bound on the balance lost across consecutive middle blocks with the charge absorbed by the ordinary prefix. A uniform bound of five would suffice, and the exact criterion also allows larger debts when the left balance pays for them. The altered-tape experiment in the accompanying right-boundary analysis shows why any proposed bound needs information beyond a finite run of matching boundary histories. [Right-boundary counterexample](line34_right.md) · [Timed blank orbit and proof target](target34.md)
