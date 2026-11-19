# Testing angular transport from the secondary-cusp checkpoint

Let $Y=\lfloor3^{301}/19171\rfloor+4,510,976$ and $R=Y+158,145,479,878$. The [connected secondary-cusp interval](CHECKPOINT_Y_758.md) reaches $R$. Three direct ways to transport its orbit to a simpler one encounter distinct obstructions.

1. An invertible affine change of the physical counters intertwining both repeated ordinary instructions can change the mass coordinate $u$ by at most six, even allowing different finite words on the target side.
2. The order-reversing symbolic map of the normalized survivor set would send the representative's 358 consecutive pair blocks to 358 jumps. A machine state supporting those jumps requires more than $3.0064\times10^{31}H$ in its mass coordinate, where $H$ is the known halting reset.
3. On the first 100 actual excursions from $R$, the smallest denominator of any strict rational direction within the published 18-unit physical guard allowance at a postlaunch odd phase exceeds $7.33\times10^{66}$.

These tests concern the specified transports and finite histories. The eventual fate of $R$ remains open.

## Affine changes of the physical counters

Use $h=(a+1)/2$ and $u=(a+2c-1)/2$ at odd/odd states. A jump is $(h,u)\mapsto(3h,u+2)$. A bulk pair has linear part $(h,u)\mapsto((9h-5u)/4,u)$; its additive constants depend on the fine residue. Suppose an invertible affine $F$ intertwines a positive jump iterate $J^i$ and a positive pair iterate $Q^j$ with finite words of fine $J,Q$ branches. The identities may be restricted to full-dimensional affine branches. The words and the two positive lengths need not agree in advance.

The determinant of a word with $s$ jumps and $p$ pairs is $3^{s+2p}/4^p$. Similarity preserves determinants. Comparing prime powers forces the image word for $J^i$ to be exactly $J^i$, and that for $Q^j$ to consist of precisely $j$ pairs. The linear part of $F$ must commute with $\operatorname{diag}(3^i,1)$, so it is diagonal. The exact jump law $J^i(h,u)=(3^i h,u+2i)$ then forces the $h$-translation to vanish and the coefficient of $u$ to be one. Since the linear part of $Q^j$ has a nonzero off-diagonal entry, the coefficient of $h$ is also one. Thus $F(h,u)=(h,u+c)$.

Put $d=(u-h)/2$. Each fine pair is $d\mapsto(9d+e)/4$ for $e\in\{20,35,26,29\}$. Two $j$-pair words can differ in their additive constants by at most $3((9/4)^j-1)$, by summing the one-pair difference $15/4$ geometrically. Translating $d$ by $c/2$ requires an additive difference of $|(9/4)^j-1||c|/2$. Hence $|c|\le6$. If the same map works on all sufficiently large integer inputs for pure pairs, it is the identity: the projection on $d$ is defined for arbitrarily long strings of translated inputs by choosing $u$ sufficiently large, whereas a $j$-pair iterate has growth factor $(9/4)^j>1$ and bounded rounding error.

## Exchanging the two cusp endpoints

The ideal launch direction at the secondary cusp is $19171/3^9$. Four pair blocks and one jump send it to the right endpoint 1. At the primary target the ideal launch direction is $13959275/3^{15}$. Four pairs and one jump give $665/729$, and three further pair formulas give the left endpoint 0. The physical halting trajectory reaches the boundary on the last attempted pair. The inverse-angle contractions at the right and left endpoints are $4/9$ and $1/3$.

There is no fixed nonconstant algebraic endpoint correspondence exchanging periodically grouped levels of these pure branches. An elementary proof works even for an alleged correspondence only on a geometric sequence. Distances to the two endpoints at such levels are $x_n=x_0(4/9)^{bn}$ and $y_n=y_0(1/3)^{an}$, with $a,b$ positive integers and nonzero $x_0,y_0$. For any polynomial in $x,y$, its nonzero monomials give distinct positive exponential bases in $n$: equality first forces equal $x$ exponents by the prime 2 and then equal $y$ exponents by the prime 3. The Vandermonde determinant therefore prevents the polynomial from vanishing at all levels. This also proves that a polynomial with $t$ nonzero monomials cannot describe $t$ consecutive such levels.

A symbolic exchange of branch addresses can be defined without an algebraic formula. At the actual $R$ the complete word is $J^{292}Q^4J\,Q^{358}JQ^{10}JLR$. Exchanging the postheader pairs for jumps would require $J^{358}$. Every physical launch has $h\ge1$. After $n$ jumps it needs $3^n\le3^n h\le u+2n$, since the right counter cannot be negative. Thus the target state needs $u\ge3^{358}-716$. Even $J^{293}$ is impossible at $u\le H+10^4$. The same obstruction applies to all 78 primary corridors with odd $587\le k\le741$, since they start their postheader words with at least 293 complete pairs.

## Lower-height directions at actual states

An angular direction $h/u$ in lowest terms requires an integer coordinate $u'$ at least its denominator for any exact match. An odd reset launch at exponent $m$ has numerator $3^m$ before reduction; an even launch has numerator $2\cdot3^m$. Both give a pure power of three after reducing the measured launches here. A reduced numerator $3^e$ rules out either parity at every smaller opening exponent $m<e$. At $R$, $R+584$ is coprime to three, so $e=292$. Across the 368 primary and 364 secondary merger checkpoints the minimum is 285.

For a rounded match, choose any strict rational direction $0<p/q<1$ with $q\le10^{18}$ and measure $|h-u p/q|$. The [physical pullback identity](TARGET_SHADOW_758.md) motivates this choice of units. The first ordinary bulk after the maximal opening jump run begins the postlaunch part. At each measured state the checker finds the two adjacent bounded-denominator Farey fractions bracketing $h/u$. Their determinant is one; a strict intermediate fraction has denominator at least the sum of their denominators. This proves that one of the two endpoints gives the smallest error. When the direction is within $1/10^{18}$ of 0 or 1, the nearest strict boundary-side fraction is handled directly.

| Starts and return budget | Counter calls | Odd/odd states | Postlaunch odd/odd states | Smallest exact denominator across all odd phases | Least postlaunch error for $q\le10^{18}$ |
|---|---:|---:|---:|---:|---:|
| $R$, 100 returns | 67,050 | 48,200 | 19,050 | 136 digits | $224584707220898/2187>10^{11}$ |
| 732 catalog starts, four returns each | 2,510,806 | 1,687,303 | 833,068 | 133 digits | $695182660215218/387420489>1,794,387$ |

The same adjacent-fraction search can minimize the denominator over *all* strict directions satisfying $|h-u p/q|\le18$. Start with bounds 0 and 1 and test their mediant, skipping a run of mediants only when each lies strictly on the same side of the allowed interval. The first accepted mediant has the smallest possible denominator by the determinant-one property. Across the representative histories the minimum is $7.3384994785\times10^{66}$ (rounded); across all catalog histories it is $1.9744998189\times10^{66}$. At each of $H-2$ and $H$, the final odd phase instead has $9h-5u=34$ after 305 counter calls: the actual terminal is detected at denominator nine and error $34/9$. Thus neither catalog provides a comparably low-height lift at this clearance. More widely separated directions can still share a finite word whose individual guards have larger margins.

Run [angular_lift_obstruction_758.py](angular_lift_obstruction_758.py) beside the [secondary-cusp](SECONDARY_CUSP_758.md) and [edge-merger](Y_EDGE_BANDS_758.md) checkers.

## Searching the terminal boundaries of observed words

A second test searches for genuine halting origins next to the return patterns seen on these trajectories. Start at the 732 merger checkpoints, $Y$, $R$ and the known target $H$; follow up to 32 positive-time returns from each, stopping at a halt. The 17,399 odd excursions give 3,918 distinct postlaunch words. Use every prefix after the compulsory $Q^4J$, and append each possible suffix of up to three $J,Q$ blocks to every observed complete word. Interpret each resulting word as a possible path followed by a final individual bulk and halt.

The [direct-terminal strip inversion](MIXED_TERMINALS_758.md) gives a short interval of candidate reset seeds for each word. The checker intersects this interval with $[Y,H]$, tests all odd candidates, and requires the exact same prefix with a literal halting decision. There are 121,480 word classes, including 52,950 with at least three separate postlaunch jump runs. The necessary strips give 338,709 candidate occurrences and 313,475 distinct seeds. The only exact matches are the two known direct halters $H-2,H$. Other words and later excursions are still possible. [Terminal-boundary checker](checkpoint_terminal_neighbors_758.py)
