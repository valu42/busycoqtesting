# Dyadic directions in the ordinary return map for machine 758

Consider the exact normalized direction $x=N/4^p$ for an odd positive multiple $N$ of five below $4^p$. A jump $J$ sends $x$ to $3x$ for $x<1/3$. A pair $P$ sends it to $(9x-5)/4$ for $x>5/9$. In the middle interval the ordinary word ends. The table measures its length in elementary moves, counting one for $J$ and two for $P$. A final returning bulk is excluded. The denominator is a power of two and the numerator stays odd, so none of the four endpoints $0,1/3,5/9,1$ can occur.

Exactly **224** eligible dyadic directions with $p\le27$ have a tail of at least 189 elementary moves. At $p=28$ the two-sided search found 748 more, giving 972 in total. It tested 15,211,551,150 interval matches and replayed 1,568,831,850 candidates exactly. The [complete ledger](dyadic_long_tails_758.tsv) gives each numerator and its exit length.

The table certifies the maximum over every direction in each row, including directions that need not arise from the blank orbit. For $p=1$ there is no eligible numerator. For a cusp header, suppose $x=D h_d/3^e$ with $h_d$ even. The first normalized pair produces an odd numerator divisible by five. Reading to the first grouped boundary at elementary depth $e$ or $e+1$ removes the factors of three and gives the reduced denominator $4^p$, where $p$ is the number of pairs read. The remaining normalized word then satisfies the corresponding bound. [Why these dyadics occur](RATIONAL_HEADERS_758.md)

| $p$ | Maximum elementary moves | Smallest maximizing $N$ | Number of maxima |
|---:|---:|---:|---:|
| 2 | 24 | 5 | 1 |
| 3 | 21 | 55 | 1 |
| 4 | 22 | 145 | 1 |
| 5 | 30 | 935 | 1 |
| 6 | 37 | 35 | 1 |
| 7 | 43 | 13,505 | 1 |
| 8 | 60 | 60,305 | 1 |
| 9 | 60 | 17,165 | 3 |
| 10 | 59 | 349,505 | 1 |
| 11 | 86 | 2,530,055 | 1 |
| 12 | 103 | 15,461,755 | 1 |
| 13 | 105 | 64,681,495 | 1 |
| 14 | 106 | 28,057,115 | 1 |
| 15 | 116 | 234,966,355 | 1 |
| 16 | 133 | 3,642,299,795 | 1 |
| 17 | 133 | 1,907,721,085 | 1 |
| 18 | 138 | 19,832,464,355 | 1 |
| 19 | 156 | 85,415,752,025 | 1 |
| 20 | 167 | 1,034,958,816,055 | 1 |
| 21 | 170 | 3,074,610,587,485 | 1 |
| 22 | 176 | 14,925,759,124,445 | 1 |
| 23 | 187 | 47,672,032,283,785 | 1 |
| 24 | 213 | 61,089,283,523,705 | 1 |
| 25 | 210 | 242,035,771,586,755 | 1 |
| 26 | 207 | 905,466,298,629,265 | 2 |
| 27 | 235 | 16,596,468,157,584,215 | 1 |
| 28 | 243 | 62,420,325,085,947,185 | 1 |

## Exhaustion of the search

A node stores the exact images of the surviving grid points as $(a+is)/q$ for $i\ge0$ with $a+is\le q$. The original numerators at this node are $N_0+10i$. At the root $(a,s,q,N_0)=(5,10,4^p,5)$. For the left child replace $(a,s)$ by $(3a,3s)$. For the right child take the first index $i_0\ge0$ for which $9(a+i_0s)\ge5q$ and use
$$
(a',s',q',N'_0)=(9(a+i_0s)-5q,9s,4q,N_0+10i_0).
$$
The requirement that numerator be at most the new denominator selects precisely the branch interval. The gap between the children has already ended its word at the node's current depth. Empty nodes are discarded. At a node with at most eight grid points the program evaluates each surviving point to its first gap or the supplied ceiling. It checks that the deepest split is strictly shallower than the reported maximum, so an earlier discarded gap cannot affect either the maximum or its multiplicity. It also checks that every such split occurs before depth 189.

For a finite search to depth $T>\log_{3/2}Q$, the grid cutoff always occurs first. A word of elementary length $n$ contracts by at most $(2/3)^n$. In the original direction a split requires the cylinder width to be at least $80/Q$, where $Q=4^p$. Each final child then has width at least $80/(3Q)$. With $3^{-\delta}+(4/9)^\delta=1$, the sum of the $\delta$ powers of those disjoint final cylinder widths is at most one. There are $O(Q^\delta)$ leaves, each with at most eight grid points in the arbitrary-precision algorithm. Its cost is $O((T+1)Q^\delta)$ integer operations. For $T>(e+1)\log_{3/2}2$, collecting the dyadic classes after depletion of a ternary denominator $3^e$ costs $O((T+1)2^{\delta e})$, since the first boundary has $p\le(e+1)/2$. This bounds a finite-horizon search on the enlarged dyadic class. Header ancestry and a bound on physical shadowing are separate requirements for the machine.

All comparisons use integers. The verifier checks bounds for the 128-bit prefix arithmetic and promotes long individual tails to GMP. Compiling with OpenMP parallelizes disjoint depth-nine prefix subtrees. The same source also runs serially. The following commands exhaust the one-sided portion through $p=25$, then independently traverse every numerator through $p=10$ without prefix pruning. No start reached the 240-move ceiling. [C++ verifier](dyadic_survival_758.cpp)

```sh
g++ -O3 -std=c++17 -fopenmp dyadic_survival_758.cpp -lgmpxx -lgmp -o dyadic_survival_758
./dyadic_survival_758 1 25 240
./dyadic_survival_758 1 10 240 --brute
```

## Exact search for long dyadic tails

The second verifier finds every eligible numerator that survives at least a chosen elementary depth. It joins two lists of ordinary intervals, then checks the tail after the join. [Two-sided verifier](dyadic_tail_join_758.cpp)

Choose a grouped length $b$ with $4b$ smaller than the requested depth, $Q=4^p$, $g=2^{b_g}$, and $G=Qg$. For a grouped prefix $u$ of length $b$ with $j$ pairs, let $[\alpha_u,\alpha_u+L_j]$ be its cylinder, where $L_j=4^j/3^{b+j}$. For any second word $v$ of the same length with $k$ pairs, its cylinder inside $u$ is
$$
[\alpha_u+L_j\alpha_v,\ \alpha_u+L_j(\alpha_v+L_k)].
$$
A point surviving to the requested depth lies in one of these intervals.

Compute lower fixed-point endpoints by prepending each inverse branch, rounding down after each operation. On a grid of size $T$, the last rounded integer understates the true scaled endpoint by less than $1/(1-4/9)<2$ at every depth. In particular the stored $a$ for a first prefix satisfies $a\le G\alpha_u<a+2$. For the second interval use $T=\lfloor GL_j\rfloor$ and store the lower approximations $l,h$ to both scaled endpoints, starting from zero and $T$. In units of $G$, each true scaled endpoint within that first prefix lies between its respective $a+l$ or $a+h$ and that quantity plus five.

Therefore a dyadic numerator $N\equiv5\pmod{10}$ in this exact cylinder satisfies $Ng-a\in[l,h+5]$. Within each $j$, sort the first words by $(5g-a)\bmod 10g$. The second words specify short circular ranges of these residues. Each match gives its original integer $N$ by division and remainder modulo $10g$. The search includes every such match even when the rounded intervals overlap.

For a match let $z=Ng-a-l$ and $W=h-l$. If its unrounded direction truly has the indicated two prefixes, the residual numerator differs from $z$ by at most five and the true residual width from $W$ by at most three. Since the residual direction $x$ lies in $[0,1]$, $|Wx-z|\le8$. With $W\ge64$, the code uses the wider interval $[\max(0,z-20),\min(W,z+20)]/W$. Exact propagation of both endpoints can exclude a candidate by showing that its entire interval reaches the hole before the requested depth. A small width, ambiguous guard or impending overflow triggers a replay from the original $N/4^p$ using wide integers and GMP. Replays also remove matches introduced by outward rounding. Results are deduplicated by original numerator.

The first list has $2^b$ entries. The search generates $(b+1)2^b$ second intervals plus the actual angular matches. To select $b$, one can average over all phase shifts of the numerator grid. A cylinder then contains its length times $Q/10$ points on average. The sum of the lengths of the $2b$-letter cylinders is $(7/9)^{2b}$, giving an average of $(Q/10)(7/9)^{2b}$ matches before rounding. The actual residue class is fixed and the search counts its matches directly.

With a 110-move threshold at $p=18$, the two independently implemented enumeration schemes return the same 180 numerators and exact exit lengths.

The following commands check all reported long tails beyond the one-sided portion and test both a fine and a deliberately coarse rounding grid against exhaustive direct iteration on three small examples. The first two arguments select the denominator exponent and the number of grouped letters in each half. The final argument selects $b_g$. [Independent small-grid test](check_dyadic_join_758.py)

```sh
g++ -O3 -std=c++17 -fopenmp dyadic_tail_join_758.cpp -lgmpxx -lgmp -o dyadic_tail_join
python3 check_dyadic_join_758.py ./dyadic_tail_join
./dyadic_tail_join 26 23 189 32
./dyadic_tail_join 27 25 189 36
./dyadic_tail_join 28 26 189 35
```
