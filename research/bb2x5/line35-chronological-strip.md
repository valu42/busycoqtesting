# Where a first halt can originate on line 35

**On every reached blank epoch from epoch 15 onward, the first 28 cells contain at most five unmatched closings.** If the machine ever halts, the closing that triggers its guard must occur farther right. On any sufficiently old interval of at least 46 cells, at most one of five consecutive sweeps can have at least as many closings as openings. For debt five to appear at the same old cut five sweeps in a row, the witnesses must extend at least 230,304 cells to its right. These statements hold beyond the simulated epochs. The exact sweep now locates the sixth closing. A single exceptional reading can halt only on its arrival, and a first fatal pulse after quiet readings must reach cell 65 or farther right. The remaining question is how much debt the blank-generated tape can send. [Isolated-sweep proof and replay](line35-isolated-sweep.md) [Checker](line35_chronological_strip.py) · [Verification transcript](line35-chronological-strip-verification.txt)

The machine is `1RB2LA4RA1LA3LA_0LA3RB3LB2RB---`. At each epoch, A scans the blank immediately left of the finite word. An opening is physical digit 1, a closing is 2, and 3 is neutral. Write $b(I)$ for openings minus closings and $h(I)$ for the largest excess of closings over openings in a prefix, including the empty prefix. A scan of $I$ with incoming debt $d$ at its right end sends $\max(h(I),d-b(I))$ to its left. B4 follows when the sixth unmatched closing is processed. [Literal sweep rule](line35-pascal.md) · [Eight-cell proof](line35-guard-stream.md)

## The first 28 cells

Literal execution from blank reaches `13111231121113111111112113112` at epoch 15. Start with its first 28 cells. For any prefix $P$, match it with zero exterior debt. Its $s=b(P)+h(P)$ surviving openings disappear from right to left as exterior debt increases. At incoming debt $d$ the guard therefore reads $h(P)+\max(0,d-s)$. For each $0\le d\le s+5-h(P)$, write the actual header and ordinary successor digits and retain the first 28. These are all the successful inputs, whatever the rest of the word. Their successors depend only on $P,d$.

The closure contains **711,940 prefixes and 12,856,742 successful prefix/debt inputs**. Counts by internal deficit zero through five are 343,615, 231,841, 135,257, 1,083, 135 and 9. The seed belongs to the closure and every successful transition stays in it. Induction includes the word at a possible first failing epoch. Thus **at cut 28 the exact halting threshold for exterior debt is $6+b(P)$**. Earlier blank epochs were executed directly.

At width 29, the same computation that permits a fresh exterior at each sweep already admits an internally failing prefix. From the full epoch-15 word the ten successive debts `19 0 25 0 19 0 10 0 4 0` give a sixth unmatched closing at position 29. Each transition has its own literal tape realization. Following this path on blank would require a consistent evolving suffix. In particular, the true epoch-15 word ends at cell 29.

## Five ordinary sweeps on the same interval

Fix an interval $I$ of $L$ cells by distance from the rightmost digit. Use indices at least one that already existed five sweeps before the observation. Let $b_i$ be its physical balance $i$ sweeps after that older row, for $0\le i\le5$. The following are integer bounds on **every** such interval.

| Quantities on the interval | Bound |
|---|---|
| Current balance | $19b_5\ge-2L-59$ |
| One sweep apart | $19(b_4+b_5)\ge5L-71$ |
| Two apart | $19(b_3+b_5)\ge5L-65$ |
| Three apart | $11(b_2+b_5)\ge L-45$ |
| Four apart | $11(b_1+b_5)\ge4L-83$ |
| Four consecutive balances | $b_2+b_3+b_4+b_5\ge L-5$ |

For $L\ge46$ all four pair bounds are strictly positive. Sliding the five-sweep calculation to each pair proves that at most one of five consecutive balances is nonpositive, provided the indices had the stated ancestry throughout. One isolated negative balance can still trigger the guard.

**Finite proof.** Read the strip from right to left. At each cut keep five chronological letters. Letters 0 and 1 mean zero debt with survivor bit 0 and 1 respectively, letter 2 means unit debt, and letter 3 includes every debt of at least two. Choose the physical symbol at the oldest row of the next column. At a sample, with incoming debt $d$ and right survivor $r$, its own survivor is $s=[q=1\text{ and }d=0]$. It emits debt $\max(0,d+[q=2]-[q=1])$ and survivor $s$, then changes to $D(s,r)$ at the same right index. Here equal bits give 1, $(0,1)$ gives 2, and $(1,0)$ gives 3. An opening with high incoming debt may emit either unit or high debt. All other emitted classes are determined. The genuine history therefore traces a path in the resulting graph with $4^5=1024$ vertices and 6,818 labelled edges. Every edge records the six physical digits at that column. [Derivation of the right-index rule](line35-pascal.md#the-extra-opening)

For each bound the checker constructs an integer potential $p$. For every edge $u\to v$ it verifies $p(v)-p(u)\le w$, where $w$ is the asserted left side minus the length term on one cell. The potential maxima are zero and the minima are minus the constants displayed above. Summing along a path gives each result for arbitrary $L$.

The length refinement uses the minimum newest-row balance $v_L(j)$ over paths of exactly $L$ edges ending at $j$, with $v_0(j)=0$. The min-plus recurrence gives $v_{86}(j)=v_{67}(j)-2$ at **every** vertex. Translation of all entries commutes with that recurrence, so $v_{L+19}=v_L-2$ for all $L\ge67$. In this graph the minimum widths capable of deficits 1 through 12 are respectively **1, 3, 8, 13, 18, 29, 37, 48, 56, 67, 75, 86**. These give necessary widths on the machine. The graph permits independent high-debt choices.

## Consecutive debt readings must reach farther right

Fix a cut by its distance from the right end. At a sweep where it receives debt $d>0$, take the shortest prefix of the suffix on its right with balance $-d$. Let its length be $l$. **The next sweep starts that same interval with $l-1$ consecutive openings.** To see this, let $e$ be the debt entering the far end of the witness interval. Its number of surviving openings equals its balance plus its outgoing debt minus its incoming debt, or $-d+d-e=-e$. Thus $e=0$ and all its survivor bits are zero. At each cell except the rightmost, both bits in the ordinary successor rule are zero. Each of those cells becomes an opening.

Let $w(d)$ be the minimum graph width for deficit $d$ in the length calculation above. For $d\ge11$ it satisfies $w(d+2)=w(d)+19$. If the next sweep sends debt $d'>0$ at the same cut, its witness must first cross those $l-1$ openings. Its remaining part must lose at least $d'+l-1$ openings. Hence its length is at least

$$
(l-1)+w(d'+l-1).
$$

The interval on the right must have five ordinary ancestors for these width estimates. If a fixed cut farther right sends zero debt, all witnesses fit between the two cuts. With the terminal pair `12` the same argument uses the cells before that pair. Iteration gives the following **necessary** available widths for readings at or above the indicated debt on every one of the consecutive sweeps.

| Debt each time | One sweep | Two sweeps | Three sweeps | Four sweeps | Five sweeps |
|---|---:|---:|---:|---:|---:|
| 2 | 3 | 15 | 138 | 1,428 | 14,973 |
| 3 | 8 | 74 | 767 | 8,042 | 84,431 |
| 4 | 13 | 136 | 1,426 | 14,971 | 157,195 |
| 5 | 18 | 198 | 2,088 | 21,933 | 230,304 |
| 6 | 29 | 323 | 3,410 | 35,822 | 376,148 |

For example, even at arbitrarily late times a fixed, old cut with only 200,000 cells before a permanent zero-debt cut cannot send five units on five consecutive sweeps. A single pulse remains possible. The examples below show how one can arrive after a sequence of small readings.

## A sufficient blank induction

Let $n$ be the width and choose $25\le x\le n-2$. Put $S=W[0,x)$. Every cell of $W[x,n-2)$ existed five sweeps earlier because the width grows by at most five per successful sweep. The final two cells are the permanent pair `12`, with zero outgoing debt. Apply the single-row bound to every prefix of the interval beyond $x$. The entire sweep is safe if

$$
 h(S)\le5,\qquad 2x+19b(S)\ge2n-58 .
$$

Indeed the exterior debt is at most $\lfloor(2(n-2-x)+59)/19\rfloor$, and the second inequality is exactly the integer condition that this bound be at most $b(S)+5$. For $x=\lceil n/5\rceil$ both inequalities hold on every blank epoch **594 through 40,000** in the replay. The last miss was 593. The subsequent least margin was 111 at epoch 597. An induction from 594 would settle line 35. A complementary campaign has tested a smaller prefix at odd epochs by also using the synchronized right suffix. [Paired test through epoch 300,001](https://github.com/valu42/busycoqtesting/blob/1bcfb761d57825838ebeb1b4587235fa918928f3/research/bb2x5/line35-band.md)

The same proof uses $2x+19b(S)\ge2m-54$ if a known zero-debt suffix leaves $m$ cells to its left. At epoch 300,001 a complementary proof gives such a cut with $m=257{,}890$, and the cut remains at zero debt throughout its virtual future. In the saved 610,114-cell word the first prefix satisfying the displayed linear test ends at cell **41,707**. Its balance is 22,754, its internal deficit is one, and its margin is 14. At later epochs use the current width to the left of that cut. [Permanent zero-debt cut](https://github.com/valu42/busycoqtesting/blob/d6f72418c0056b47948fb2a4b5182810e586c57d/research/bb2x5/line35-seam.md)

## Why five earlier balances do not close the induction

The slope $-2/19$ is attained by actual ordinary cells. Take $B=$ `3313333333133111111` and $R=$ `1211212`. At the left of $R$ the exact first five chronological letters are `0 0 1 0 1`. Passing them through $B$ returns the same letters. Consequently each copy in $B^mR$ has the same six successive balances **8, 10, 13, 7, 7, −2**. At the sixth observation its digits are `3123231232312323112`. This also attains the one- and two-sweep pair slopes $5/19$.

For every $m\ge2$ the first five sweeps succeed. Each prefix $P$ of each of those five words even satisfies $3b(P)\ge |P|-8$. To check the constant, the left boundary and foot are common to all multiplicities. Each full copy has $3b(B_i)-19\ge0$ on those rows, so the smallest value occurs in the first copy, in the shared left part, or no later than with two copies at the foot. The checker evaluates the five floors as $-7,-8,0,-7,0$. On the next sweep each copy costs two openings. The 45-cell tape with two copies reaches B4 after **1,233 defined instructions**. Every extra copy can only increase the entering debt at that observation.

## A repeated piece of the genuine blank tape

A proof can also be tested using only material already present in a reached word. At blank epoch **83**, take the ten digits at zero-based positions $[14,24)$, namely `1231111112`. At both cuts the first four chronological letters, at their original distances from the right end, are `0 1 0 1`. Repeating the block any number of times therefore preserves the next four guard readings. At epoch 87 the block is `3123231232`, with balance $-2$. The part to its left has balance two and internal deficit two. The single original copy sends debt two. Two **extra** copies send six and the guard reads four. Three extra copies send eight and the guard reaches six. The unmodified blank sweep succeeds.

There is a longer instance at epoch **903**. The 23 digits at $[115,138)$ are 22 openings followed by a neutral. Both cuts send letter 1 for 15 sweeps. At epoch 918 the block has balance $-1$, its left prefix has balance 88 and internal deficit zero, and the original copy sends unit debt. **92 extra copies** give guard debt five. **93 extra copies** reach B4. The checker replays both sides of each threshold on the literal transition table.

For either example, if the critical block has balance $-a<0$ and its original outgoing debt is $e$, $m$ extra copies send exactly $e+ma$. This follows by composing the matching formula and using $e\ge h(B)$. Equal earlier letters at the two cuts ensure that the copies have evolved to the same critical digits. A blank-orbit induction must bound how much such material the actual sequence of births can place together. The 28-cell theorem supplies a fixed target for that bound. [Live machine claims](ROADMAP.md#claim-board)

Run `python3 research/bb2x5/line35_chronological_strip.py` from the repository root.

To replay the checkpoint calculation as well, extract the paired campaign's published input and pass its path to the same checker.

```sh
git show 1bcfb761d57825838ebeb1b4587235fa918928f3:research/bb2x5/frontiers/runs/line35-band.json > /tmp/line35-band-300001.json
python3 research/bb2x5/line35_chronological_strip.py --odd-checkpoint /tmp/line35-band-300001.json
```
