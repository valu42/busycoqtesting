# Matching an ordinary past and future at a selectable mass cut

Let $H$ be the known halting reset, $u=(a+2c-1)/2$, and $d=(c-1)/2$. At **every integer $T$ with $|T-H|\le10^{100}$**, the exact slice $u=T$ contains more than $2.1\times10^{61}$ distinct physical states with 300 ordinary bulk calls in their past and 300 ordinary calls in their future. This includes every possible choice of a cut in the verified halting interval. Each witness arrives at $T$ from a smaller mass, so it also qualifies as a first crossing with zero overshoot.

Write $J$ for one ordinary jump and $P$ for two ordinary bulks. A fine past specifies the input residue modulo four of each $P$. A future word in the table specifies the $J$ and $P$ positions and allows every legal bulk residue. All counts apply separately at each cut. [Exact constructors and integer checks](cut_word_matching_758.py)

| Incoming history | Future words covered, in every order | Number of future words | Lower bound on states per word at each cut |
|---|---|---:|---:|
| 300 consecutive bulk calls | 100 $J$, 100 $P$ | $\binom{200}{100}$ | 234 |
| 360 consecutive bulk calls | 36 $J$, 162 $P$ | $\binom{198}{36}$ | 3 |
| Any prescribed complete fine word of 200 elementary calls | 10 $J$, 95 $P$ | $\binom{105}{10}$ | 119,261 |
| Any prescribed complete fine word of 110 elementary calls | 100 $J$, 100 $P$ | $\binom{200}{100}$ | 2,068 |

Consequently choosing special ternary digits for the cut and imposing the corresponding past congruences cannot exclude every one of these finite integer histories. Blank ancestry remains the constraint. A bypass of the halting interval would require an ordinary excursion extending much farther in both directions. [Earlier density bounds](CUT_DENSITY_758.md) · [Physical fine words through 291 calls](LOCAL_WORDS_758.md) · [Finite ancestral searches](CUT_ANCESTRY_758.md)

## An interval realizing an arbitrary coarse future

For a future word with $j$ jumps and $p$ pairs set $R=3^j(9/4)^p$. In the normalized coordinate $d/u$, the inverse direction maps are $f_J(x)=(x+1)/3$ and $f_P(x)=4x/9$. Pull the terminal midpoint $1/4$ back through each suffix, obtaining $x_i$ at each phase. If $R_i$ is the product of the forward slopes through the first $i$ blocks, then
$$
\min(x_i,1/2-x_i)\ \ge\ R_i/(4R).
$$
Indeed the suffix inverse maps $[0,1/2]$ inside $[0,1/2]$, has slope $R_i/R$, and sends the midpoint to $x_i$.

Evaluate the prescribed steps algebraically, following each actual pair residue. Write $e_i=d_i-u_i x_i$. A jump gives $e_{i+1}=3e_i+1-2x_{i+1}$. A pair of charge $v$ and correction $b$, with $d'=(9d+b)/4$, gives $e_{i+1}=9e_i/4+b/4-vx_{i+1}$. The added terms lie in $[0,1]$ and $[0,35/4]$, respectively. Dividing by the growing product and summing a geometric series yields $|e_i|\le R_i(|e_0|+7)$. Thus every integer
$$
|d_0-Tx_0|\le T/(4R)-9
$$
follows the prescribed word when the radius is positive. Both physical gaps at each group boundary exceed one, since $u_i\ge T$. Nonnegative output $d$ verifies each jump guard. A pair has two positive left-counter decrements, and its positive final left counter verifies both bulk guards and excludes an intermediate reset. [Exact angular rules](MIXED_TERMINALS_758.md)

## An incoming all-bulk history at the same exact mass

The right coordinate after one pair is $F(d)=(9d+b_{d\bmod4})/4$ with $b=(20,35,26,29)$. This is nondecreasing and unbounded on the nonnegative integers. For $y\ge x$, $F(y)-F(x)\le(9/4)(y-x)+15/4$. Consequently after $k$ pairs, with $A=(9/4)^k$, consecutive candidates $F^k(d)$ differ by less than $4A$, while $F^k(0)<7A$ for $k\ge1$.

For each candidate, compute its actual total charge $g$ and start it at $u=T-g$. This places the final state at exactly $T$ independently of its bulk labels. Every candidate inside the future interval has a legal past: in reverse, $h=(a+1)/2$ satisfies $h_{\rm old}=(4h_{\rm new}+5u_{\rm old}-4v+2b)/9$. Here $2b>4v$, all masses are at least $T-9k>10$, and $h_{\rm new}\ge2$ implies $h_{\rm old}\ge2$. The right counters are nonnegative by construction. Every half-open interval of width $8A$ within the future interval therefore contributes a distinct integer witness. Taking the integer part of $(T/(2R)-18)/(8A)$ gives the first two rows. Distinct future words at a fixed cut give disjoint witness sets by determinism.

## A prescribed fine past

A prescribed fine past of $n$ elementary calls ending at $T$ fixes its earlier mass, every pair charge, and one residue $d\bmod 3^n$. An integral path is obtained for every representative, before checking the guards. For a jump, the forward coefficient is three. For a pair it is $9/4$, with four invertible modulo every power of three; the inverse also forces the prescribed input modulo four. [Fine-word inversion](COARSE_RECONSTRUCTION_758.md)

Restrict the future interval to $|d-Tx_0|\le T/(8R)-9$. Both cut gaps then exceed $T/(8R)$. In the last two rows this exceeds $100\cdot3^n$. Inverting one jump or pair reduces either gap by at most a factor of three as long as the current gaps exceed 35. For the lower gap of a reverse pair this follows from $(4d-b)/9\ge d/3$; the upper gap follows from the formula for $h_{\rm old}$. The inverse jump sends $h$ to $h/3$ and $d$ to $(d+u_{\rm old}-1)/3$. Thus every representative in the smaller interval gives a guarded physical history all the way to the prescribed beginning. The interval contains at least $\lfloor(T/(4R)-18)/3^n\rfloor$ representatives. The checker evaluates the bounds at $T=H-10^{100}$ and replays sample witnesses against the original counter rules at both extremes and at $H$.

~~~sh
python3 cut_word_matching_758.py
~~~
