# Certifying the gaps after the doubled powers at exponents 32 and 33

The even-reset worker certifies the same crossing statement as the ordinary window checker. Every reset in the 5,001-seed incoming window visits a reset in the 5,001-seed outgoing window. The selected outgoing resets are all even. A receipt gives the lower input cut, the output cut, the minimum and maximum possible output, the number of symbolic blocks, and the number of exact even-to-even calls. The last four fields can differ from the ordinary checker's receipt.

## The paired return

Write $P=3^m$ and take $m=32$ or $33$. Throughout the supported interval the odd return is $N(s)=s+2m+5+2[s\equiv3\pmod4]$. On an even input define $N(s)=s$. The odd word and its corridor follow from the ordered endpoint proof in [the power gates](POWER_GATES_758.md).

An even reset first takes $I J^m$ to $(4P-1,s-2P+2m+5)$. At an odd-left state put $u=(a+2c-1)/2$ and $d=(c-1)/2$. The launch point is

$$
(u,d)=(s+2m+4,\ s/2-P+m+2).
$$

Write $j=u-3d$, $t=2u-9d$, and $r=d\bmod4$. If $u-2d=1$ the current state is already a reset at $2d+1$. Otherwise $j\le1$ gives a single J, sending $(u,d)$ to $(u+2,3d-u+1)$. For $j>1$ the following constants give the two-bulk guard $t\ge T_r$ and its update $(u+g_r,(9d+b_r)/4)$.

| $r$ | $T_r$ | $g_r$ | $b_r$ |
|---:|---:|---:|---:|
| 0 | 11 | 5 | 20 |
| 1 | 18 | 9 | 35 |
| 2 | 13 | 7 | 26 |
| 3 | 16 | 7 | 29 |

If those cases do not apply, $j=2$ with $d$ odd takes E to $(u+4,0)$. Otherwise $t\le 9+5(d\bmod2)$ takes LR to the reset at $u+5+2(d\bmod2)$. The remaining case halts. These disjoint guards follow by substituting $a=2u-4d-1$ and $c=2d+1$ into the ordinary single-step rules and separating $d$ modulo four. After finding a reset the worker applies $N$ to obtain an even successor.

## Exact residue tables

In each region of $2^{19}$ consecutive seed integers, the checker takes both even endpoints forward through their common J/LL prefix. On a shared ordinary branch the left counter decreases weakly with the seed and the right counter increases weakly with the seed. Thus equal endpoint choices of J, LL or LR establish that same ordinary branch or branch pair for the whole cell. Before each pair the right endpoint must have $a>1$ to exclude an earlier reset. An intermediate L leaves an even first counter and so cannot be a reset.

For a fixed word of Js and $k$ pairs of Ls, put $D=4^k$. The output has the form

$$
u'=u+g,\qquad Dd'=A d+B u+e,
$$

where $e$ and $g$ depend on the single residue $A d+B u\bmod D$. Starting with $A=1,B=0,D=1$, appending J sends $(A,B)$ to $(3A,3B-D)$. Appending LL sends $(A,B,D)$ to $(9A,9B,4D)$.

To prove the single-residue claim, consider the suffix after the first symbol, with coefficients $A_1,B_1,D_1$. If the first symbol is J, its affine substitution makes the suffix projection the full initial projection plus a constant modulo $D=D_1$. If the first symbol is LL, the full projection is $9A_1d+4B_1u$ modulo $D=4D_1$. Since $A_1$ is odd, this determines $r=d\bmod4$. After LL, four times the suffix projection is the full projection plus $A_1 b_r+4B_1g_r$. Consequently the suffix residue modulo $D_1$ and all its corrections are determined. Induction finishes the proof. Setting $u=0$ and ranging $d$ over $0,\ldots,D-1$ visits every residue because $A$ is odd.

Each shared word is divided into blocks of at most 16 operations and five LL pairs. The checker precomputes $e,g$ from the $D$ representatives for each block. At the first block the initial projection follows directly from the affine launch in the half-seed.

The computed numerator is an unsigned 64-bit residue. Because $0\le d'\le u'/2$ and $u'\le3P+50,000$, even the largest $D=1024$ gives $Dd'<2^{63}$ at both supported exponents. Its residue therefore reconstructs the exact quotient after shifting. The implementation checks at most 256 shared operations and 5,000 subsequent paired operations. With each paired move adding at most nine to $u$, a returned odd seed is less than 50,000 above its source. The ordinary symbolic bound is also less than 50,000 from its 10,000-step limit and maximum mass gain nine. The worker rejects input windows too close to the end of the proved odd corridor.

## Symbolic crossing

The worker initially puts $N(s)$ in its frontier for every incoming seed. On an interval, [the existing same-parity checker](reset_cover_758.hpp) first tries to prove a return for each even input using a coarse common word. Its integer upper bound on the reset gain also determines its parity. Each L adds either five or nine to $a+2c$, and all other increments in the word are fixed. The actual final mass gain therefore differs from the upper mass gain by a multiple of four, and the corresponding reset gains differ by a multiple of two.

For an odd gain bound, add $2m+7$ to allow the following odd return. Every even input in the block can now progress to a strictly larger even reset within this combined bound. Consequently all entries to the block eventually leave it at even seeds between one above its upper end and that end plus the bound. Any previously accumulated exits above that range are retained in the frontier enclosure. If the symbolic test fails, the checker bisects, switching to exact frontier propagation when the interval width is at most 250,000. It reports a crossing only after every remaining point lies in the requested outgoing window.

## Reproduction

Place the two sources and audit beside the repository's reset-cover header. The default evaluates $2\cdot3^{33}$ to $3^{34}$. Pass `-DPOWER_EXPONENT=32` to target the preceding doubled-to-single gap.

```sh
g++ -O3 -std=c++17 cross_even_power_758.cpp -o cross_even
g++ -O3 -std=c++17 audit_even_power_758.cpp -o audit_even
./audit_even
./cross_even 16484121133201395 16484970113975417
```

On each supported exponent the independent audit checks all six local phase types in 75,100 small odd-left states. It compares 1,179,648 even inputs and the adjacent odd inputs with individual ordinary transitions and verifies the complete 5,001-seed incoming frontier in 20 separate small windows.
