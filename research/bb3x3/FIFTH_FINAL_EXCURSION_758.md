# The last excursion into the fifth terminal basin

Let $K=40{,}486{,}323{,}621{,}582{,}648$. Suppose an orbit coming from a reset below $K-10^{11}$ eventually halts at this specific terminal. Its first reset at or above $K-10^{11}$ must belong to
$$
S=\{K-73,\ K-71,\ K,\ K+2\}.
$$
Indeed the first two seeds lead directly to $K+2$, and every other reset from $K-10^{11}$ through $K+2$ bypasses the pair. This uses the existing local basin certificate and is independent of the forward grids connecting this neighborhood to blank. [Local basin and fifth terminal](MIXED_TERMINALS_758.md)

**At least 22,222,222,206 consecutive counter updates lead from the lower mass crossing into this first root.** Each update before the final reset is an ordinary bulk or jump. The last two calls are a bulk and the even-left reset. Immediately before those two calls the mass coordinate $u=(a+2c-1)/2$ lies in the six-element set
$$
u-K\in\{-80,-78,-76,-7,-5,-3\}.
$$
These give explicit reverse-search slices at the end of the required long excursion. The [earlier ordinary-passage bound](FIFTH_CROSSING_758.md) concerns a different mass interval preceding these slices.

## The exceptional rule misses every root

Write $W=a+2c$ for the input mass of E. It satisfies $W\equiv11\pmod{12}$, and E gives $(W+6,1)$. Throughout $2(K-10^{11})+1\le W\le 2(K+2)+1$, the first return after E has word $L^{88}JL^3R$. The [verifier](fifth_final_excursion_758.py) checks its guards and the absence of an earlier reset at the two ends of each admissible residue class modulo 48. As $W$ increases, the left coordinate is nondecreasing and the right coordinate nonincreasing, so the endpoint checks cover each entire class.

During the first 88 bulks the right coordinate is independent of $W$. Increasing $W$ by 48 increases the left coordinate by 48 through those moves. Following J, the input right-coordinate differences at the final three bulks are successively $-48,-72,-108$. All are divisible by four, so the same fine branches are selected. Consequently the entire word has the same mass gain, and its output reset $s$ increases by 24. A single checked representative per class gives the exact formulas below.

| $W\bmod48$ | $s-(W-1)/2$ | $s\bmod24$ |
|---:|---:|---:|
| 11 | 326 | 19 |
| 23 | 328 | 3 |
| 35 | 324 | 5 |
| 47 | 326 | 13 |

The four roots have residues $23,1,0,2$ modulo 24. Thus E returns to a seed outside $S$. If that seed overshoots the region, monotone mass growth prevents a later visit to $S$. If it is inside, the local basin proof excludes the terminal. An E at any state after the lower mass crossing and before the first root is therefore impossible on the hypothesized path. There is also no reset there by the choice of the first root. The first crossing of mass $2(K-10^{11})+1$ overshoots by at most eight. Each live call adds at most nine, which gives the displayed call count.

## The final two calls

A non-R entry to a reset could be a bulk landing at $a=1$. This requires $s\equiv5\pmod6$ and has the two possible parents $(4q+4,4q\pm1)$, $q=(s-5)/6$. Among the four roots only $K-73$ has this residue. Both its candidate parents have even left counter, so they can have entered only by a bulk. Their right counters are respectively 1 and 3 modulo six, whereas a bulk always outputs a right counter congruent to 5. The parents have no predecessors. In general this also excludes every hidden bulk entry to a reset with $s\equiv17\pmod{18}$ on an orbit from blank.

The last call into the first root is consequently R. Its even-left input must itself follow a bulk. The two gains in $W$ are 5 or 9 for that bulk and exactly 5 for R, giving $u=s-5$ or $s-7$. Removal of the two overlaps gives the stated six slices.

There is also an origin restriction independent of the last $10^{11}$ seeds. On the entire odd-seed corridor from $30{,}018{,}927{,}059{,}399{,}751$ through $K+1$, the first return gains exactly $73+2\mathbf 1_{s\equiv3\pmod4}$. The ordered endpoints certify the word of 34 Js followed by LR. Hence the only odd starts in this corridor mapping to an element of $S$ are $K-73,K-71$, both already roots. A preceding reset in this corridor before the *first* root must therefore be even. [Odd power-gate formula](POWER_GATES_758.md)
