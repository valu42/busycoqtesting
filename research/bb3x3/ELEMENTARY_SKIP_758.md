# Exact traversal with an elementary-depth cutoff

For a reset chain crossing the seed annulus $[X,3X]$, its exact exit seed and number of first returns can be obtained with $O(X^\eta)$ individual first-return evaluations, where
$$
\eta=\log_3\!\left((1+\sqrt{17})/2\right)=0.8561834341\ldots .
$$
The previous proved exponent for the same exact outputs was 0.880614. Use the [existing exact simulator](annular_skip_758.py) with depth $n=\lceil\log_3 X\rceil$ and weights $(1,2)$ for jumps and bulk pairs. A halt during an evaluation ends the run. The bound counts evaluations conditional on their completion. The duration of a long or infinite excursion is still uncontrolled. At the target scale even this exponent gives a power of $X$ far beyond direct computation.

## What costs a first-return evaluation?

Following the maximal launch jumps, an ordinary word with $j$ more jumps and $p$ bulk pairs has elementary length $m=j+2p$ and inverse contraction $R=4^p/3^m$. The ordinary middle branch then makes one final bulk and a reset. For each parity the partition stores the whole interval of seed indices returning by that word. There are a bounded number of launch groups on an annulus. A returned-word interval $I$ spans $W=O(1+XR)$ full seed positions, by the [inverse physical bounds](LOCAL_RETURN_WINDOWS_758.md). Pairing adjacent even and odd seeds changes this width by at most a constant. The word has $2p+1$ individual bulks, so $M_w=4^{p+1}$ is a period of its reset increment.

Intersect the two parity partitions. In a common cell $C$ where both words return, the larger of their periods is a period for both. Positive gains and the [residue-cycle skip](ANNULAR_SKIP_758.md) give at most $2\min(|C|,\max(M_0,M_1))$ evaluations. Charge at most $2\min(|C|,M_b)$ to each parity $b$; the sum of the two allowances covers the cost.

## How much can the other parity split a word?

Within one launch group, let $K$ be the survivor set of the two inverse branches with ratios $1/3$ and $4/9$. In the direction variable $x=h/t$, losing a specific branch at a physical word boundary can happen only within $O(1/X)$ of $K$. Indeed the components of the complement are the distinct open return gaps. If $x$ is more than $18/t$ from the ends of its gap, the whole word up to the return agrees with the ideal one. Its prefix up to our stopping depth also agrees. This holds for every seed in the connected interior of that gap after this padding is removed. The partition makes no internal subdivision there. With $|dx/ds|$ bounded above and below by constants times $1/X$, adjacent integer seeds and the even/odd pairing enlarge the padding by only a constant in seed units. The ends of launch groups add a bounded number of cuts.

For an interval of width $W$ in seed units, consider the $M$-neighborhood of these cut locations, $M\ge1$. Its intersection with the interval has length
$$
O\bigl(M(1+W/M)^\delta\bigr), \qquad 3^{-\delta}+(4/9)^\delta=1.
$$
For $W<M$ the bound is immediate. For $W\ge M$, cover $K$ first by disjoint cylinders stopped when their widths reach $W/X$ (the root suffices above width one). Each has width greater than $W/(3X)$ whenever the stop occurs below the root. Only $O(1)$ of them meet the window enlarged at both ends by $O(M/X)$. In each, stop again at widths $M/X$; preservation of the sum of the $\delta$ powers of the widths gives $O((W/M)^\delta)$ smaller cylinders. Each and its padded neighborhood cost $O(M)$ seed positions. Scaling the two stopping widths by fixed constants covers the distortion of the launch coordinate. [Local stopping argument](LOCAL_RETURN_WINDOWS_758.md)

For a fixed word interval $I$, charge the first $\min(M_w,|C|)$ seed positions of each common cell $C$ in $I$. They are disjoint and lie within $M_w$ of a cut of the other parity or the left endpoint of $I$. Therefore the total charge to this word is $O(M_w(1+W/M_w)^\delta)$. This accounts for many intervals of one parity subdividing a single high-period interval of the other.

## Summing the costs

Before depth $n$, $X/3^m\ge1$ for integer $m<n$. A word at depth $m$ costs at most $O(4^p (X/3^m)^\delta)$. Let $F_m$ be the sum of $4^p$ over all words of elementary length $m$. Removing the last block gives $F_0=F_1=1$ and $F_m=F_{m-1}+4F_{m-2}$. Thus $F_m=O(\alpha^m)$ with $\alpha=(1+\sqrt{17})/2$. Since $3^\delta<\alpha$, summing through depth $n-1$ costs
$$
O\left(X^\delta\sum_{m<n}(\alpha/3^\delta)^m\right)=O(\alpha^n).
$$

A surviving prefix at the cutoff has $m=n$ or $n+1$. Its physical interval has width $O(1+X4^p/3^m)=O(4^p)$. Summing both lengths costs $O(F_n+F_{n+1})$ seed positions. Earlier exceptional, immediate-reset or halting equalities cost a bounded number per word. Doubling those sets to admit the neighboring opposite-parity seed changes only a constant. The simulator can query each of those positions at most once. This proves the stated bound. The partition itself has $O(\varphi^n)$ nodes per parity, where $\varphi^2=\varphi+1$; its bisections and word replays use $O(\varphi^n\operatorname{polylog}X)$ arithmetic operations. Other skip bookkeeping uses a bounded number of dictionary operations per evaluation.

The [checker](elementary_skip_758.py) verifies the exponent inequalities using rationals and compares the exact exit and return count with literal iteration from 15 starting seeds on five annuli.

```sh
python3 elementary_skip_758.py
```
