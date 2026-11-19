# A smaller search space for two hard launch parities

For the ordinary direction set $K$ of machine 758, the single-phase exponent is $\delta=0.73177394\ldots$, defined by $3^{-\delta}+(4/9)^\delta=1$. With both phases required to survive, an **upper box exponent of $0.65$** is certified for the portion of $K\cap(3/2)K$ with bounded difference in bulk-pair counts as defined below. The same covering argument works, without any restriction on the words, down to geometric resolution $3^{-292}$. A padded version applies to simultaneous long prefixes of actual neighboring odd and even seeds. The unrestricted infinite-scale upper box dimension remains open; the balance bound is automatic only through the stated finite scale.

At resolution $3^{-35}$, exact subdivision leaves **67,856,170 of the 2,466,287,855,329 odd cylinders** as candidates when both ideal phases have to survive. Each selected cylinder actually contains a common survivor. This count concerns all normalized directions on $[0,1]$. It does not count actual blank resets or decide what happens at a difficult direction.

| Resolution | All odd cylinders | Odd cylinders containing a joint survivor | Positive overlapping pairs |
|---:|---:|---:|---:|
| $3^{-12}$ | 23,058 | 551 | 606 |
| $3^{-20}$ | 13,643,734 | 31,745 | 35,782 |
| $3^{-26}$ | 1,665,376,507 | 666,149 | 770,011 |
| $3^{-30}$ | 42,467,340,908 | 5,173,188 | 5,927,547 |
| $3^{-34}$ | 1,096,294,154,557 | 40,585,745 | 45,686,165 |
| $3^{-35}$ | 2,466,287,855,329 | 67,856,170 | 76,077,049 |

## The scale comparison

Write $J(z)=z/3$ and $P(z)=(4z+5)/9$, where $P$ represents two bulks. A cylinder has elementary depth $d$ (one per $J$, two per $P$), pair count $p$ and width $4^p/3^d$. An even cylinder is rescaled by $3/2$. For an odd cylinder $C$ of width $w\le1/4$, stop each even branch at its first cylinder $D$ of width at most $5w$. These stopped widths are strictly greater than $5w/3$. Distinct stopped even cylinders are separated by a gap greater than $10w/9$, since their least common ancestor was wider than $5w$. The odd cylinder, even enlarged by $10^{-9}w$ on either side, can therefore meet at most one.

For a surviving point compare the pair counts $p_C,p_D$ at each such prefix $C$ containing it. Call the point bounded at 400 if $|p_D-p_C|\le400$ at all these prefixes. With $b=p_D-p_C$, the ratio $r=|D|/w$ is $(3/2)4^b3^j$ for some integer $j$. There is exactly one such ratio in $(5/3,5]$ for each $b$. This gives 801 rational slopes. For any $w\ge3^{-292}$ both counts are automatically less than 400: $(3/2)(4/9)^{400}<3^{-292}$, and both parent widths are at least $w$.

## Exact simultaneous pruning

Rescale $C$ to $[0,1]$ and write $D=t+r[0,1]$. Let $\eta=10^{-9}$. For **every** listed $r$ and real translation $t$, there is a grouped depth $1\le n\le12$ such that
$$
\sum_{I:\ \operatorname{dist}(I,\ t+rE)\le\eta\ \text{for some }E} |I|^{13/20}\ \le 1 .
$$
Here $I,E$ range over ordinary depth-$n$ cylinders. A grouped depth counts $J$ and $P$ once apiece. The exponent pertains to spatial resolution, not to the number of two-counter calls.

The [Python checker](joint_dimension_758.py) proves the inequality entirely with integers. It upper bounds the two single-symbol weights by $489634/10^6$ and $590312/10^6$, checking the required powers exactly. At depth $n$ each cylinder has integer endpoints on the grid $9^{-n}$. For a source $I=[a,b]$ and an even descendant $E=[c,d]$, compatibility is the closed translation interval $[a-rd-\eta,b-rc+\eta]$. Merge the intervals for each source before adding its weight. Sweep endpoint events to obtain precisely the translations where their summed upper weights exceed one. Retain only translations exceeding one at every level tried. For every slope the retained set is empty by level 12. The largest required depth has the following distribution.

| Required depth | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Number of slopes | 133 | 293 | 188 | 80 | 67 | 16 | 8 | 8 | 8 |

For the bound on covering numbers, start at the finitely many odd cylinders first crossing width $1/4$. At an admissible parent use its certified depth, discard the incompatible odd children and repeat. Each replacement has total $13/20$-weight at most its parent's. Stop once a cylinder reaches width $\rho$. Each stopped width exceeds $3^{-12}\rho$, giving $O(\rho^{-13/20})$ stopped cylinders. This proves the upper box bound for the fixed bounded-imbalance set and the finite-scale bound whenever $\rho\ge3^{-292}$. The argument also works starting at any other fixed scale. If the starting scale varies arbitrarily by point, countable stability gives the Hausdorff bound.

## Padded physical comparisons

Let $Q=3^m$, $m\le292$, and consider a neighboring odd seed $s$ and even seed $s+1$ in the launch range where the odd opening has $m$ jumps, the even opening has one initial even instruction and $m-1$ jumps, and $s+2m\ge Q$. Their directions in common units are $Q/(s+2m)$ and $Q/(s+2m+3)$, differing by at most $3/Q$. Every physically completed ordinary prefix puts its true direction within $14/Q$ of its ideal cylinder, or $21/Q$ for the rescaled even phase. Thus any completed pair of prefixes has nominal interval distance at most $38/Q$. [Guard identity](LOCAL_RETURN_WINDOWS_758.md) · [Simultaneous long examples](SIMULTANEOUS_PARITY_758.md)

For $\rho\ge 40\cdot10^9/Q$, a parent of width $w\ge\rho$ absorbs this discrepancy into $\eta w$. If both neighboring suffixes continue to width at most $3^{-12}\rho$ in common units, then all comparison descendants used before stopping are available: after at most 12 grouped symbols a width is still at least $3^{-12}$ times its parent width. Apply the same pruning and enlarge each resulting odd interval by $14/Q$ to cover the actual odd directions. This localizes those two-phase difficult locations in $O(\rho^{-13/20})$ intervals of length $O(\rho)$. Seed gain, reachability from blank, and the later fate of each candidate require separate arguments.

## Exact counts at power 35

The [C++ enumerator](joint_cover_758.cpp) refines the longer interval, discards disjoint children and stops when both widths reach $3^{-m}$. The widths stay within a factor of three, larger than the relative $2/9$ middle gap. Thus every positive overlap extends to a joint survivor by the nested construction in the [simultaneous-prefix proof](SIMULTANEOUS_PARITY_758.md). Distinct positive endpoints across phases have different reduced denominator parity. The only common endpoint of both grids is zero, and the two cylinders with left endpoint zero have positive overlap. Descending the two children from left to right gives the distinct odd and even counts in one pass. The table uses the unpadded ideal geometry.

The worker accepts $m\le35$. Since $(3/2)(4/9)^{48}<3^{-35}$, neither side uses more than 48 grouped letters. Each working integer uses units of $1/(2\cdot3^{\max(d_C,d_D)})$. The deeper cylinder has width at most $3\cdot4^{48}$ units. The other width is at most three times this, and, in a retained pair, the endpoint offset is bounded by their larger width. A child rescales these quantities by at most nine, within signed 128 bits; the 48-letter path IDs fit in unsigned 64 bits. The single-parity totals use the exact two-branch recurrence depending only on elementary depth and pair count.

```sh
python3 joint_dimension_758.py
c++ -O3 -std=c++17 joint_cover_758.cpp -o /tmp/joint-cover758
python3 joint_dimension_758.py --worker /tmp/joint-cover758
```
