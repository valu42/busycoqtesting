# Complete first-return words actually used from blank

The blank orbit uses at least **48,798,505 distinct complete ordinary first-return words** over two published crossings. A complete exponent-35 grid raises the combined count to **118,391,094**.

On the certified blank crossing from $3^{34}$ to $2\cdot3^{34}$, #758 and #153 execute at least **30,968,802 distinct complete ordinary first-return words from odd reset seeds**. After one fixed opening they realize every one of the $2^{21}$ possible 21-block suffixes, each followed immediately by a bulk and reset. The same calculation on a complete $3^{35}$ to $2\cdot3^{35}$ grid gives 69,592,589 distinct words and every 22-block suffix. The optional checker accepts that second count as an actual blank result only with a complete archive. [Actual exponent-34 crossing](FIFTH_BLANK_CROSSING_758.md) · [Checker](blank_word_spectrum_758.py)

## Forcing a chosen return word onto the actual path

Write $S=3^m$, $h=(a+1)/2$, $t=(a+2c-1)/2$. An odd reset with seed $s$ makes $m$ initial jumps in the intervals below, giving $h=S$, $t=s+2m$ and $x=S/t$. An ordinary jump $J$ has inverse direction $x\mapsto x/3$. Two consecutive ordinary bulks form a block $P$ with inverse $x\mapsto(4x+5)/9$. A single bulk followed by a reset occupies the open gap $(1/3,5/9)$.

Prescribe the grouping $PJw$ after the launch, where $w$ has $n$ blocks and $p$ pairs. The root cylinder for $PJ$ is $[5/9,19/27]$. The return gap after $PJw$ has length $(2/9)(4/27)4^p/3^{n+p}$. Trim $20/S$ off each end of this gap in the $x$ coordinate. Every remaining odd seed executes the entire prescribed first-return word. Indeed the exact inverse comparison after any realized prefix is
$$
h-\lambda t = R(h'-\mu t')+B,\qquad 0<R\le1,\quad 0\le B\le14
$$
for each guard $\mu$ and its inverse image $\lambda$. All inverse guards of those prefixes are outside the open final gap. The trimmed starting margin $t|x-\lambda|>20$ preserves their signs with more than four units of physical clearance. This excludes exceptional or terminal edges and premature resets. The initial $m$ jumps are legal since $S<t$ after the proposed launch, and $x>5/9$ excludes a further jump. [Physical guard identity](TARGET_SHADOW_758.md)

The absolute derivative $|ds/dx|=S/x^2$ is at least $S(27/19)^2$ on this cylinder. Thus the extent of the trimmed seed interval is at least
$$
(27/19)^2\left((8S/243)4^p/3^{n+p}-40\right).
$$
All of these intervals lie within the archived grid. The window checkers' budgets prove that at any integer cut $z$ within it the actual path has a reset in $[z,z+100000]$. Every admissible even seed there has the word $IJ^{m-1}LR$ and therefore advances to an odd seed in at most $2m+9$ more seed units. The checker verifies its same-parity extremes; the intervening inputs obey the same guards by counter order. A trimmed interval of real span greater than 100,090 therefore contains an odd reset on the actual trajectory. [Interior-cut budget](CROSSING_CLOCK_758.md) · [Power-35 packed engine](double35_prefix_758.hpp)

For each $(n,p)$ whose displayed lower bound exceeds 100,090, add $\binom np$. The sum counts distinct complete ordinary words since group parsing is unique. Once the all-pair word at a given length fails the bound, all later lengths fail it too. Literal counter replay in the checker tests both sides of four representative word intervals.

## A disjoint set from even resets

On the [certified passage above the doubled power](FIFTH_BLANK_CROSSING_758.md), apply the same calculation at even launches, now with $h=2\cdot3^{34}$, $t=s+72$. The initial opening is $IJ^{34}$. Two disjoint initial words $P^3J$ and $P^2JP^2$ give complete cylinders within the archived passage. Throughout either cylinder odd starts execute $J^{34}LR$ and arrive at an even reset with gain 73 or 75. The same interior-cut budget and 100,090 width threshold therefore force the corresponding even words onto blank. Summing binomial multiplicities gives respectively 11,154,004 and 6,675,699 further words. Their openings distinguish them from odd-start words, and the two fixed prefixes differ before either finishes. The power-34 and power-35 odd words differ at their first post-launch pair.

## What previous resets can exclude at the target scale

Let $S=3^{292}$. There are **more than $10^{80}$ different possible complete odd first-return words below $H$ even when each must occur after $10^{21}$ consecutive genuine first returns on a compatible trajectory**. Different words may have different launch trajectories. The proof gives no connection from blank to these target-scale examples.

Take the cylinder $P^8$, with width $r=(4/9)^8$ and upper endpoint 1. The corresponding seed positions are wholly below the scale-20 halting basin. All their even seeds take $IJ^{291}L^2JL^3R$ and land at odd seeds with gains at most 615. Grow a binary tree of suffix cylinders, stopping as soon as its width is at most $\epsilon=10^{-110}$. For $3^{-\delta}+(4/9)^\delta=1$ the sum of widths to the power $\delta$ stays one. There are at least $\epsilon^{-\delta}>10^{80}$ leaves, since $\delta>8/11$. Each leaf has width greater than $\epsilon/3$; appending its returning middle gap inside the initial $P^8$ cylinder and trimming both ends gives a true seed interval of span greater than $2Sr\epsilon/27-40>2.35\times10^{25}$.

Start at the first integer in this interval. Each odd seed in it has the prescribed complete ordinary word, and each even one has the short word above. The maximum suffix block count is bounded by the least $n$ with $(4/9)^n\le\epsilon$. Every first return increases the seed by at most $\lfloor9(292+16+2n+2)/2\rfloor$. The interval is wide enough that, after $10^{21}$ consecutive first returns, the trajectory and one further return are still inside. If the reached seed is even, its next reset is odd. This constructs the claimed recent reset history for every one of the different returning words. This also gives a dichotomy on a *single* infinite blank trajectory. Before mass reaches $2H+1$, the trajectory must either use more than $10^{80}$ distinct complete odd-reset words or spend **more than $5\times10^{24}$ consecutive elementary calls without a reset** near $3^{292}$. Indeed, if any constructed word is absent, the corresponding seed interval contains no odd reset. Removing 615 units at its upper end leaves an interval with no reset of either parity, since any even reset there would reach an odd one inside the original interval. The trajectory traverses that mass range by monotone increments of $W=a+2c$ of at most nine. Even discarding two upper/lower crossing increments and 630 seed units in total for rounding leaves more than $5\times10^{24}$ reset-free calls. If every constructed word is present the word-count alternative holds. Either alternative remains possible for this machine.

```sh
python3 blank_word_spectrum_758.py
python3 blank_word_spectrum_758.py --power35-table double35_frontier_758.tsv.gz
```
