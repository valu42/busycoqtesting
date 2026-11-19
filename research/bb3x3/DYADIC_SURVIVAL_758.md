# Dyadic directions in the ordinary return map for machine 758

Consider the exact normalized direction $x=N/4^p$ for an odd positive multiple $N$ of five below $4^p$. A jump $J$ sends $x$ to $3x$ for $x<1/3$. A pair $P$ sends it to $(9x-5)/4$ for $x>5/9$. In the middle interval the ordinary word ends. The table measures its length in elementary moves, counting one for $J$ and two for $P$. A final returning bulk is excluded. The denominator is a power of two and the numerator stays odd, so none of the four endpoints $0,1/3,5/9,1$ can occur.

The table certifies the maximum over every direction in each row, including directions that need not arise from the blank orbit. For $p=1$ there is no eligible numerator. The link to a cusp header is exact: if $x=D h_d/3^e$ with $h_d$ even, the first normalized pair produces an odd numerator divisible by five. Reading to the first grouped boundary at elementary depth $e$ or $e+1$ removes the factors of three and gives the reduced denominator $4^p$, where $p$ is the number of pairs read. The remaining normalized word then satisfies the corresponding bound. [Why these dyadics occur](RATIONAL_HEADERS_758.md)

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

## Exhaustion of the search

A node stores the exact images of the surviving grid points as $(a+is)/q$ for $i\ge0$ with $a+is\le q$. The original numerators at this node are $N_0+10i$. At the root $(a,s,q,N_0)=(5,10,4^p,5)$. For the left child replace $(a,s)$ by $(3a,3s)$. For the right child take the first index $i_0\ge0$ for which $9(a+i_0s)\ge5q$ and use
\[
(a',s',q',N'_0)=(9(a+i_0s)-5q,9s,4q,N_0+10i_0).
\]
The requirement that numerator be at most the new denominator selects precisely the branch interval. The gap between the children has already ended its word at the node's current depth. Empty nodes are discarded. At a node with at most eight grid points the program evaluates each surviving point to its first gap or the supplied ceiling. It checks that the deepest split is strictly shallower than the reported maximum, so an earlier discarded gap cannot affect either the maximum or its multiplicity.

All comparisons use integers. The verifier checks bounds for the 128-bit prefix arithmetic and promotes long individual tails to GMP. Compiling with OpenMP parallelizes disjoint depth-nine prefix subtrees; the same source also runs serially. The following commands exhaust the reported range, then independently traverse every numerator through $p=10$ without prefix pruning. No start reached the 240-move ceiling. [C++ verifier](dyadic_survival_758.cpp)

```sh
g++ -O3 -std=c++17 -fopenmp dyadic_survival_758.cpp -lgmpxx -lgmp -o dyadic_survival_758
./dyadic_survival_758 1 24 240
./dyadic_survival_758 1 10 240 --brute
```
