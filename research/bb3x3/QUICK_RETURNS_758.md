# How often a reset starts a long excursion

For an interval of $L$ consecutive reset origins at arbitrary height, the number of difficult origins is $O(L^{0.731774})$. [Local proof and common-word construction](LOCAL_RETURN_WINDOWS_758.md)

Let $H=(3^{307}-8\,282\,708\,212)/13\,959\,275$. Among all $H$ reset configurations $A(1,s)$ for $1\le s\le H$, **fewer than two in $10^{36}$ can avoid both a halt and another reset for 1,086 counter calls**. This is a finite count over the entire interval. Each seed is counted once. Including direct halts among the exceptions, **fewer than three in $10^{36}$ fail to reach a positive-time reset within the same budget**. The blank orbit selects its own successive reset seeds, and paths from different starting seeds can merge.

An infinite blank orbit must cross the known [scale-10 halting corridor](LOWER_SCALE_GATES_758.md). Its last reset before the upper mass crossing would have to go at least 80,481,430,280,060 calls without a reset or a halt. This forces that particular reset into the exceptional set bounded here. A proof excluding this set from the relevant part of the blank orbit would decide the machine.

## Counting the exceptional resets

Write $u=(a+2c-1)/2$ and $h=(a+1)/2$ at odd/odd states. An even seed first takes one opening call. Set $b=1$ for odd entry and $b=2$ for even. After the maximal run of $k$ initial jumps, $h=b3^k$ and $u=t=s+4(b-1)+2k$. The first call after the run cannot be another jump, so $h\le t\le3h-3$. In particular $b3^k\le H+4(b-1)+2k$. These bounds give 584 parity/exponent groups in the verifier. Counting extra possible starts in a group preserves the upper bound.

Use $P$ for two successive ordinary bulk calls and $J$ for a jump. A path that continues ordinarily past its initial run must begin with $P$, or exit during the attempted pair. For each group put $T=\min(H+4(b-1)+2k,3h-3)$. Choose the first $n\ge1$ satisfying $9(T+9n)(4/9)^n<5$ and set $U=T+9n$. This bounds $u$ during the next $n$ complete ordinary blocks because every block adds at most nine. A finite binary tree starts with $P$ and appends $J$ or $P$. For a word containing $j$ jumps and $p$ pairs let $R=4^p/3^{j+2p}$. Stop at the first word with $9UR<5$. Every branch stops by depth $n$.

The [reset-origin identity](RESET_WORDS_758.md) puts all same-parity starts for a word into an interval of width at most $6+(9/5)UR$. Briefly, undoing the word gives $h=S t+B+R h_{\rm end}$. Its initial pair gives $S\ge5/9$. Across bulk residues the range of $B/S$ has width at most six, and $0\le h_{\rm end}\le U$. At a leaf the width is strictly below seven, giving at most four integers of fixed parity.

An exceptional update $E$ before reaching a leaf must be accounted for even when its subsequent trajectory is unknown. Its odd/odd input satisfies $a=c+2$. At launch, $a$ is constant and $c$ strictly increases with $s$, giving at most one seed. After the first bulk, equal images can group at most two adjacent seeds of one parity because the image depends on $\lfloor(c+1)/4\rfloor$. For distinct images, increasing the original seed strictly decreases the left coordinate and strictly increases the right. These orders persist on a common ordinary word. At a bulk the right gap, initially at least six, stays at least six, and at a jump the gap can only increase. Thus each internal word admits at most two original seeds at the exceptional equality. The midpoint of a bulk pair has even left coordinate and cannot take $E$.

A tree with $L$ leaves has $L-1$ internal vertices after its first pair. At most $4L+2(L-1)+1\le6L$ starts can reach a leaf or an earlier $E$. Every other start returns or halts within the possible opening, the leading $k$ jumps and $2n$ more calls, including a final single bulk followed by its decision. The checker groups words by length and number of pairs to count the leaves exactly. Summing $6L$ over the groups gives an upper bound $B$ with
$$
\left\lfloor H/B\right\rfloor=621353992137306222688330968369786851.
$$
The maximum total call budget is 1,086. Counts are upper bounds on exceptional seeds. Some counted seeds return quickly.

For the stronger claim about reaching a reset, also count direct halts before a leaf. The right counter stays odd following the possible opening. Such a halt must occur at an even-left phase, after the first individual bulk of an attempted pair. It requires $a-c$ equal to one or three. The same strict ordering after that bulk gives at most two seeds for each equality. Include the launch and the $L-1$ internal vertices as possible starts of that final pair. This adds at most $4L$ seeds per group. Replacing $6L$ by $10L$ gives the three-in-$10^{36}$ bound.

## Typical length beyond the leading jumps

At a fixed depth $n$, the $2^{n-1}$ words beginning with $P$ have total $R$ equal to $(4/9)(7/9)^{n-1}$. For each such word the interval bound permits at most $4+(9/10)(T+9n)R$ same-parity seeds. Including possible earlier exceptional branches, the number still alive without a reset after $2n$ calls beyond the launch is at most
$$
6\cdot2^{n-1}+\tfrac25(T+9n)(7/9)^{n-1}
$$
per group. Summing this expression over the 584 groups and dividing by $H$ gives the following upper bounds for a uniform reset seed. The opening and leading jump count are measured separately on each seed.

| Further counter calls after the leading run | Fraction that can still be live without a new reset |
|---:|---:|
| 44 | below 1 in 100 |
| 62 | below 1 in 1,000 |
| 118 | below 1 in 1,000,000 |
| 172 | below 1 in 1,000,000,000 |

## Typical reset increments as the cutoff grows

The argument works with an arbitrary integer cutoff $X$ in place of $H$. Fix $n$ first and let $X$ grow. There are $O(\log X)$ groups and $\sum T=O(X)$ because the power $b3^k$ grows geometrically and the last power is $O(X)$. Including direct halts in the exceptional set costs at most four seeds per internal/launch word. Thus the upper fraction that fails to make a genuine return within $2n$ post-launch calls has limiting upper bound $C(7/9)^{n-1}$ for an absolute constant $C$. In particular the fraction with no return at all tends to zero.

At a return $A(1,s')$, the opening costs eight in mass when present and each of the $k$ leading jumps adds four. The remaining $D$ calls add at most $9D$. Hence $s'-s=2k+O(1+D)$. The launch inequalities give $k=\log_3 s+O(1)$. For a seed sampled uniformly from $1,\ldots,X$, the deviations $s'-s-2\log_3 s$ are therefore **bounded in probability**: given any error fraction, a fixed finite bound works outside that fraction for all sufficiently large $X$. Seeds without a return count as exceptions. This proves a typical logarithmic increment in the published counter convention, including its leading coefficient two. No bound on the untruncated mathematical expectation is needed.

The number of exceptional origins also has a uniform power bound. Let $\delta=0.73177394\ldots$ solve $3^{-\delta}+(4/9)^\delta=1$. In a group's stopped tree, $\sum_{\rm leaves}R^\delta=(4/9)^\delta$, because splitting a word preserves this sum. Every leaf satisfies $R\ge5/(27U)$: its parent failed the stopping test, and the last contraction is at least $1/3$. The root leaf also satisfies this bound. Hence $L=O(U^\delta)$. One may use $T=3b3^k-3$ throughout a group; then $n=O(k+1)$, $U=O(b3^k)$ and the group's total call budget is $O(k+1)$. Summing the geometric powers through $X$ proves that, for some absolute constant $A$, at most $O(X^\delta)$ reset seeds $s\le X$ fail to make a positive-time reset within $A\log(s+2)$ calls. This count includes halts and indefinitely long first excursions. The result constrains exceptional origins; it does not control how many earlier reset chains coalesce at any one of them.

There is an explicit limiting distribution inside a complete launch group. Fix the parity and let $k$ tend to infinity. Sample the reset seed uniformly among those of that parity with this maximal leading jump count. The ratio $t/h$ is asymptotically uniform on $[1,3]$, so $x=h/t$ has density $1/(2x^2)$ on $[1/3,1]$. For any fixed number of blocks the exact normalized rules converge off their guard boundaries to the branches with inverses $f_J(x)=x/3$ and $f_P(x)=(4x+5)/9$. The finitely many boundaries have limiting measure zero. Passing a boundary by taking an earlier $E$ or an immediate direct halt also has zero limiting weight at every fixed depth. The underlying guards and normalized maps are derived in the [ordinary-word proof](ALL_ORBIT_ENTROPY_758.md).

The limiting probability of completing at least $n$ ordinary blocks after the launch is the integral of that density over the intervals $f_w([0,1])$ for words $w$ starting with $P$ and containing $n$ blocks. For $n=1$ it is exactly $2/5$. These intervals have total length $(4/9)(7/9)^{n-1}$ and lie in $[5/9,1]$. Thus the probability for every $n$ is between $(2/9)(7/9)^{n-1}$ and $(18/25)(7/9)^{n-1}$. This derives the geometric decay for one specified population of resets directly from the counter rules.

The frequently used small-gap heuristic concerns the resets actually selected by forward iteration. The table proves a related claim under a specified sampling rule. It supplies neither independence of successive excursions nor a distribution on the unique blank trajectory. [Community discussion of the heuristic](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA)

Run the [integer and rational verifier](quick_returns_758.py) locally.

```sh
python3 quick_returns_758.py --small-check
```
