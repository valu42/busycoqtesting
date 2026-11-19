# Which #758 cut witnesses can come from a reset?

**None of the five sharp 98-copy witnesses can be reached from blank.** More generally, consider the first odd/odd state on or immediately after the central mass crossing, provided the trajectory has avoided the halting basin. The next **395** blocks cannot match a periodic sequence of period at most **13**. A block is either one odd/odd jump $J$ or a consecutive pair $P$ of ordinary bulk updates, allowing all four bulk residue combinations. This leaves longer-period and nonperiodic sequences open.

## The five witnesses

For each [98-copy witness](cut_residues.md), the verifier explores all its predecessors until reaching a reset or exhausting the search. It uses the [exact inverse rules](TERMINALS_758.md) and checks every reverse edge against the forward counter map. The blank trajectory passes through the reset $A(1,3)$, so absence of a reset in a complete inverse search rules out blank reachability.

| Copies before the cut | Copies after the cut | Distinct states in inverse search | Maximum reverse depth | Reset ancestors |
|---:|---:|---:|---:|---:|
| 0 | 98 | 2 | 1 | 0 |
| 23 | 75 | 463 | 85 | 0 |
| 46 | 52 | 885 | 147 | 0 |
| 69 | 29 | 1,183 | 209 | 0 |
| 92 | 6 | 1,853 | 278 | 0 |

As a separate check, the verifier constructs 1,028 representative two-sided paths with 72 prescribed blocks before and 72 after the central cut using the [mixed-word construction](CUT_758.md). All 1,028 inverse searches exhaust without a reset. Their largest search has 1,316 states and their greatest depth is 152.

## Every period up to 13

Write $u_c=H-10{,}000{,}000$, $u=(a+2c-1)/2$ and $d=(c-1)/2$. After the optional compulsory bulk move from an even mass, every surviving first crossing gives an odd/odd state with $u_c\le u\le u_c+8$. The [central cut estimate](CUT_758.md) encloses the possible $d$ for a given $n$-block prefix in the frozen inverse image of $[0,u/2]$, padded by 14 at each end. In units of $u$ the two frozen inverse maps are $f_J(x)=(x+1)/3$ and $f_P(x)=4x/9$.

For a mixed period word $w$, the composition $f_w$ has a unique fixed point $\theta_w$ in $[0,1/2]$. This point lies in the inverse image for every finite prefix of the infinite repetition of $w$, including prefixes ending partway through a copy. This follows by composing the maps for the omitted suffix up to a whole number of copies and using $f_w(\theta_w)=\theta_w$. Both maps send $[0,1/2]$ into itself. At $n=395$ the unpadded interval has diameter at most $(u_c+8)(4/9)^{395}/2<1$. Therefore each candidate integer $d$ lies strictly between $u\theta_w-15$ and $u\theta_w+15$.

The checker enumerates the 16,220 distinct mixed directions from all period words of length at most 13, including all phases. At each of the nine possible masses it checks 30 integers around each direction, covering this entire open interval. All 4,379,400 inverse searches exhaust without encountering a reset. They examine 32,925,469 states counted with multiplicity across searches. The largest individual search has 658 states, and none extends beyond 93 inverse steps. The two constant words are already excluded by the bounds of 292 consecutive jumps and 786 consecutive ordinary bulk steps in the [halting strip](CUT_758.md). A constant $P$ prefix of length 395 would require 790 consecutive ordinary bulk steps.

Run the following in this directory. The checker uses only the existing counter and inverse rules and Python's standard library.

~~~sh
python3 cut_ancestry_758.py
~~~
