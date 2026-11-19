# Finite binary word counts at two crossings

Write one bit per elementary counter update, 1 for J and 0 otherwise. The following are requirements on a **single actual passage** that survives to the far edge without a reset in the indicated interval.

| Reset interval passed without entry | Binary word length | Number of distinct words required |
|---|---:|---:|
| [Scale-10 halting corridor](LOWER_SCALE_GATES_758.md), from $H-905{,}416{,}090{,}650{,}670$ through $H-543{,}249{,}654{,}390{,}404$ | 44 | At least 45 |
| [Post-target checkpoint corridor](AFTER_TARGET_758.md), from $H+1$ through $E+647$ | 1,085 | More than 300,000,000 |

For the first interval there are at least $n+1$ words of every length $1\le n\le44$. The second interval feeds a single later checkpoint, whose halting status remains open. These bounds count only the jump bit and do not assume that different starting configurations are sampled randomly.

In both cases the [785-bulk exceptional annulus](CUT_758.md) includes the entire mass span. An E gives a reset within 787 calls and 5,458 mass units. Trim this allowance from the high end and at most eight units of overshoot from the low end. The surviving passage contains only ordinary moves, after discarding up to one elementary call at each endpoint for alignment.

## The post-target passage

Here are explicit constants for the [two-stage line argument](COARSE_ENTROPY_758.md). The trimmed span contains more than $T+4N$ complete blocks for $T=10^{135}$, $U=2H$ and $N=1085$. Reserve $N$ blocks at each end so all histories and binary encodings stay in the passage. At the outer stage take the least $m,l$ with $3^m>144T$, $(3/2)^l\ge U+1$, giving $N=m+l+4$. Suppose there are at most $K=300{,}000{,}000$ different length-$N$ binary words in the passage. Then the outer edge count is bounded by $F=2^{m+4}K$. The longest run of repeated edges has length at least $\lfloor(T-F)/(F+1)\rfloor$.

For explicit endpoint allowances put $Q=9T$, $a=1+\lceil\log_3 Q\rceil$, $b=1+\lceil\log_4 Q\rceil$, $j=1+\lceil\log_3(U+1)\rceil$ and $g=3+\lceil\log_{9/4}(2Q(U+7))\rceil$. Discard at most $a+(b+1)(j+1)+2g+10$ more positions. These terms bound the initial three-divisible denominators, the even-denominator tail with at most $b$ pairs and $b+1$ runs of jumps, and both possible escapes from the bounded slope or deviation interval. Endpoint rounding is included. Call the remaining lower bound $D$.

For a denominator $q$ supporting that central interval, let $d$ be the least exponent with $3^d>7q$. There are at most $d+2+f_d+4f_{d-1}$ central positions, where $f_0=f_1=1$ and $f_n=f_{n-1}+4f_{n-2}$. Beyond $d$ blocks each phase has a suffix of elementary length $d$, or one P followed by a suffix of length $d-1$. It determines the bounded $(k,e)$ pair, which cannot recur. The bound increases weakly with $q$. The checker finds the first $q_0$ for which it reaches $D$ and selects
$$
s=\min(\lfloor D/2\rfloor,\lfloor(q_0-1)/9\rfloor).
$$
The selected $s$ positions have $9s<q$.

For the inner stage choose the least $m'$ with $3^{m'}>144s$, and $r=\max(m',\lceil\log_3(Q+1)\rceil)$. Discard $r+2$ positions for the past. As $r+3\le N$, the inner encoding can use a complete length-$N$ binary extension in the original passage, again bounded by $K$. The inner edge count is at most $2^{m'+4}K$. This forces at least **1,126** successive repeated edges. The slope discrepancy starting at $1/(9sQ)$ grows by at least $9/4$ per block and must remain at most $U+1$. Even allowing rounding, at most **897** such edges are possible.

## The scale-10 passage

For this narrower interval a direct coarse-period argument gives a finite test. Assume that for some $n\le44$ there are at most $K\le n$ binary words of length $n$. Make a finite directed graph on these words using every observed one-bit transition. Every strongly connected component containing a directed cycle must be a single simple cycle. Otherwise two outgoing choices within a component yield a non-eventually-periodic infinite walk: repeat a cycle an increasing number of times and take an alternative edge between runs. Overlap of successive windows produces a non-eventually-periodic binary word with at most $n$ length-$n$ factors. This is impossible: an infinite word with two symbols and at most $n$ length-$n$ factors must have some length $j<n$ for which its factor counts stop increasing. Every length-$j$ factor then has a unique right extension, and the finite deterministic sequence of factors is eventually periodic. A single-symbol sequence is already periodic.

The finite passage therefore traverses simple periodic components in order, with at most $K$ transitions between components. Their cycle lengths $p$ sum to at most $K$. A pure run has fewer than 1,000 calls at $u\le H$: J triples $a+1$, and consecutive ordinary bulks grow the right counter by at least $3/2$ per call. On a mixed component, align the period at a J. If there are at least two complete periods, the zeros between jumps occur in pairs. Write $p=j+2b$, where $j,b\ge1$ count jumps and bulk pairs. The [periodic slope formula](EXCURSION_POWERS_758.md) gives one reduced denominator $q\le3^p-4^b<3^p$ at every phase. Its normalized directions $k/q$ lie in $[0,1/2]$. The integer $e=qd-ku$ must stay in $[-7q,0]$ until the last 1,000 elementary calls: outside it distance grows at least $3/2$ per call until it exceeds $q(H+7)$. Endpoints of incomplete periods can be discarded.

Among reference visits just before the chosen J with another 100 complete blocks after that J still in the bounded part, all values of $e$ have span at most $q$. Indeed, fold an interval of width $7q$ backwards through the 100 common coarse blocks, allowing every fine residue at P. At J a normalized width $W$ becomes $W/3$. At P it becomes at most $4W/9+5/3$, by the [four inverse offsets](FINITE_AFFINE_PERIODS_758.md). Thus it is at most $3+4(4/9)^{100}$ in normalized units before the final inverse J. That J divides by three, giving integer span at most $q$ since $4q(4/9)^{100}<3$.

Given the preceding complete period, its fine labels determine the final $e$ modulo $3^p$. At the earliest P, the label pairs $0,3$ and $2,1$ give equal final residues within each pair. This follows from the first-pair congruence in the [denominator proof](FINITE_AFFINE_PERIODS_758.md); it applies also with leading jumps. There are thus at most $4^b/2$ classes. As $q<3^p$, the span bound permits at most one actual integer $e$ per class. A repeated $e$ at the reference phase would yield a legal invariant-line repetition on the observed trajectory, which the [periodicity theorem](FINITE_AFFINE_PERIODS_758.md) excludes.

To bound the *total mass-coordinate increase* of the retained complete periods, charge each class the larger gain in its pair. Across the four labels the average P gain in $u$ is seven. Each merged pair has a gain difference of two, so taking the larger adds one to the average for that P. The total is bounded by
$$
(4^b/2)(2j+7b+1).
$$
All discarded ends of any one component cost fewer than 20,000 units of $u$: at most 1,000 elementary calls for deviation escape, 202 for the width estimate, and at most four periods of at most 44 calls for alignment and the initial past. Each call adds at most $9/2$ to half the mass. The same allowance covers a pure run or short component. Allow 20,000 each for all transitions and the final readout padding together. With $K\le44$, summing the largest ratio of the displayed charge to $p$ against the total cycle length gives a bound below **337,524,500,610,000** units. The trimmed crossing requires more than **362,166,436,245,266**. This contradicts the assumed binary complexity.

Run the [exact finite checker](binary_passages_758.py) beside the post-target verifier with Python 3.10 or later.

```sh
python3 binary_passages_758.py
```
