# Closing the 264 odd primitive guard contacts at two target crossings

Let $H=(3^{307}-8,282,708,212)/13,959,275$ and $T=H-10,000,000$. At **every** odd/odd state of #758 or #153 with $T\le u\le T+8$, write $h=(a+1)/2=3^j v$, $3\nmid v$, and $u=(a+2c-1)/2$. The state halts if either of the following holds.

| Primitive left coordinate | Inclusive limit |
|---|---:|
| Odd $v$ | 211,637,975,937,205 |
| Even $v$ | 1,012,257,878,130,399,645,022 |

The same two criteria hold for every mass in the second interval

$$H-61,410,570,681,246,030,618+584\ \le u\le H-61,410,569,303,845,097,640.$$

This gives **1,377,400,932,395 consecutive mass levels**. An ordinary block increases $u$ by at most nine, so the nine-mass test suffices at an ordinary crossing of $T$. The blank trajectory has yet to be connected to either crossing. The limits describe the primitive coordinate $v$, even when $h$ itself has 140 digits.

## The nine-mass check

Write $F=61,410,570,681,246,030,619$ and $L=3,403,055$. At a primitive predecessor $A(2v-1,w-v+1)$, where $w=u-2j$, the $j$ regular jumps to the given state are legal. Each inverse step divides $h$ by three and subtracts two from $u$. The forward guard at each step is exactly $h_{\rm out}\le u_{\rm out}$, inherited by its predecessor. Since $h\le u<H<3^{293}$, $j\le292$ and $u-584\le w\le u$. All these primitive masses at the stated crossings lie in $[H-F,H-L-2488]$. The [ordinary header proof](ORDINARY_HEADER_COVER_758.md) already settles every even $v$ up to its limit and every odd $v$ up to its limit except for 263 guard contacts. Its [264-row ledger](odd_header_ties_758.tsv) includes the basin reset $v=1$.

The [checker](odd_tie_crossing_758.py) follows the original counter map from every distinct primitive predecessor, including the initial reset for $v=1$. Odd $v$ requires odd $u$, so the possible offsets are $0,2,4,6,8$. All allowed powers $3^jv\le u$ are included. Among the 350,095 states, 175,123 have $c\equiv1\pmod4$ and 174,972 have $c\equiv3\pmod4$. There are 71,075 distinct primitive predecessors. Each reaches a reset with seed in the [proved halting interval](HALTING_COLLAR_758.md). The largest return time is 617 counter calls and the largest seed gain is 1,341, both measured from the primitive predecessor with $v=14,041,887,462,289$, $u=T+8$ and $j=227$.

## An interval at the outer edge

At both ends of the even distance interval

$$61,410,569,303,845,097,640\le H-w\le61,410,570,681,246,030,618$$

the checker reads the same complete $J,L,R$ word for each nonreset contact $v$. To see why this covers every interior odd $w$, at the two ends the smaller mass has a larger or equal left counter and a smaller or equal right counter. A jump maps $(a,c)$ to $(3a+2,c-a+1)$. A strong bulk maps it to $(a-4q-3,6q+5)$ with $q=\lfloor(c+1)/4\rfloor$. Both preserve the opposite endpoint orders. The conditions for another jump or bulk, or for the final ordinary reset, are one-sided comparisons in these orders. The left parity is determined by the word. Together the two verified endpoint trajectories enclose every intermediate trajectory up to the final reset.

For a word comprising $j'$ jumps, $p$ pairs, and the final bulk and reset, the seed gain is positive and at most $2j'+9p+7$. Across all 263 words the greatest upper bound is 1,243, which puts every return inside the collar. The remaining $v=1$ starts inside the collar. Trimming 584 from the outer side permits all inverse jump counts in the displayed state criterion. The first smaller even distance changes the word for $v=120,423,828,604,033$.

## Why a full-collar calculation needs to combine different words

For the single contact $v=14,365,291$, at least **3,544,067,762,102 distinct complete physical first-return words** occur as the odd primitive mass $H-d$ varies through the wide collar. An endpoint calculation requiring a common word on each interval therefore needs at least this many intervals for this coordinate alone.

Here is a direct count. Set $D=13,959,275$, $U=3^{307}/D$, $C=8,282,708,212$ and $\lambda=Dv/3^{30}$. The primary launch takes $k=277$ jumps. From the alignment the ideal orbit reaches $5/9$ at depth 28, having taken 13 pairs. At this contact the signed initial discrepancy is $\lambda(U-u_*)$, where $u_*=H-d+2k$. It is positive by millions of aligned units throughout the collar. Every earlier guard has the nonzero margin from the [odd header proof](ORDINARY_HEADER_COVER_758.md). The physical contact consequently takes a pair. Immediately after this fourteenth pair denote the new coordinate by $h'$. The [physical pullback](TARGET_SHADOW_758.md) of zero gives the exact relation

$$\lambda(d+C/D-2k)=Rh'+B,\qquad R=4^{14}/3^{30},\quad 0\le B\le14.$$

With $G=\lambda/R$, choose a target direction $x\in(5/9,1)$ for a second launch of $s=239$ jumps. Round $Ux/(3^sG)-C/D+2k$ to the nearest even integer $d$. Every such distance is within the collar, between $1.48\cdot10^{19}$ and $2.67\cdot10^{19}$. The normalized error of $3^s h'/U$ from $x$ is at most $E=(G+14/R)3^s/U<5.77\cdot10^{-19}$. When $x$ has margin greater than $E+(F+2600)/U$ from the relevant guards, all $s$ jumps are legal and the next jump is illegal. Earlier jump guards follow from the last legal one by monotonicity. The same margin to each subsequent pulled-back guard ensures the prescribed physical continuation. The mass during these two launches is within $F+594$ of $U$.

Given any grouped word $w$ with $j'$ jumps and $p$ pairs, prescribe a direction whose next instructions are $P w$ followed by the middle return. Obtain $x$ by pulling the center $4/9$ of the middle interval back through $P w$. All group-boundary guards, including the final return, have initial clearance at least

$$M=\tfrac4{81}(1/3)^{j'}(4/9)^p.$$

Indeed the final gap boundaries are $1/9$ from its center and the inverse contraction of the complete word is $(4/9)(1/3)^{j'}(4/9)^p$. Every earlier continuing branch interval contains this final cylinder, so its guard boundaries are at least as far away. Whenever $M>E+(F+2600)/U$ a distinct physical full word occurs, ending in an ordinary reset inside the collar. Words of different lengths are distinct because the prescribed return takes place at the end of the chosen word. Summing $\binom{j'+p}{p}$ over all qualifying counts gives the stated integer. No grouped length beyond 48 passes this particular lower bound. This leaves the all-mass halting claim for these contacts open.

From this directory, run the following command for all 350,095 ancestry cases, both outer endpoints for all contacts, the exact binomial count, and literal checks of selected prescribed words.

```sh
python3 odd_tie_crossing_758.py
```
