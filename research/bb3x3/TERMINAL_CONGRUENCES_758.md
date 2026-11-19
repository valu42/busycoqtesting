# Actual reset congruences arbitrarily close to both cusp halters

Assume an infinite blank-compatible orbit has ordinary stretches sublinear
in their starting mass, the [reset-dense alternative](ALL_ORBIT_ENTROPY_758.md).
Let $b_m$ be either member of the [fifteen-bulk halting pair](CUSP_TERMINALS_758.md)
at exponent $m=597\pmod{1200}$. For **every** fixed $\epsilon>0$ and positive
integer $M$, infinitely many exponents admit an actual odd reset $s$ with
$$
 0<s-b_m<\epsilon 3^m,\qquad s\equiv b_m\pmod M.
$$
Moreover, the two seeds execute identical fine instructions throughout
their $m$ jumps and fifteen ordinary bulks. At the next instruction
$b_m$ halts and $s$ returns alive. Increasing the requested modulus to
$2^{16}M$ also makes both counters agree modulo $M$ after every common
instruction, since each bulk consumes at most one binary digit.
Thus arbitrarily accurate fixed relative and modular conditions on the
actual orbit can all hold together strictly above the target. Whether
the orbit enters either halting basin remains open.

## First returns on the upper side

Put $t=s/3^m$ and $t_*=1+65536/42981185$, the common limiting position
of the halting pair. After the initial jumps the normalized counters
tend to $(2,t-1)$. Each ordinary bulk sends a normalized pair to
$(a-c,3c/2)$ up to terms tending uniformly to zero. After $i$ bulks
the limiting gap is
$$
 2-\big(3(3/2)^i-2\big)(t-1).
$$
For $0\le i<15$ this is strictly positive throughout
$[t_*,t_*+10^{-4}]$. At $i=15$ it vanishes at $t_*$ and is negative
above it, with both counters still positive. Therefore on any fixed
closed subinterval strictly inside this upper interval every odd seed
has complete first return $J^m L^{15}R$ for large $m$. The final left
counter is divisible by four, because it starts at one modulo four
and each bulk adds one modulo four. The return is odd. Even seeds in
this cusp return to odd seeds with an $O(m)$ increment by the five-letter
theorem. Choose the closed subinterval inside the requested neighborhood
with positive clearance on both sides.

## Exact cycles and absolute lifts

Write $z=(s-1)/2$, $D=32768$, and
$y=z+m-(3^m-1)/2\pmod D$. This is the low residue of the right coordinate
$d=(c-1)/2$ after the initial jumps. The fifteen bulks consist of
seven pairs and a final single bulk. If $B(y)$ of those bulks have
input right counter three modulo four, the exact mass charges give
$$
 z'-z=m+20+B(y).
$$
The seven pairs each consume two low bits and the last bulk reads the
remaining bit. Thus this is a deterministic map on $y\bmod D$ at
each exponent. At a terminal seed the two possible initial right
counters are $4i-1,4i+1$, with $i\equiv28826\pmod D$. The corresponding
target phases are $24883,24884$ respectively.

The following [32,768-state enumeration](check_terminal_congruences_758.py)
checks every phase, including transient phases. Each row has **one**
cycle, and that cycle contains the target phase. For
$m=m_0+Tj$, the last column is the increase in the integer $z$ across
one whole cycle, divided by $D$.

| Target | $m_0$ | $T$ | Target $y$ | Cycle length | Integer winding |
|---|---:|---:|---:|---:|---|
| Lower cusp sibling | 350,997 | 19,660,800 | 24,883 | 153 | $1639+91800j$ |
| Upper cusp sibling | 36,597 | 19,660,800 | 24,884 | 1,368 | $1529+820800j$ |
| Lifted $H_m$ | 242,417,632 | 15,902,965,760 | 28,726 | 3,879 | $28696843+1882556280j$ |

In each row the constant and slope of the winding are coprime.
For every prime dividing $M$, either the slope vanishes and the
constant is nonzero, or at most one residue of $j$ makes the winding
zero modulo that prime. The Chinese remainder theorem permits a fixed
progression of $j$ on which the winding is coprime to $M$.

The cusp density theorem supplies an actual reset in a smaller interval
at every sufficiently large favorable exponent of that progression.
After a possible even-to-odd return, $(M+2)D+1$ successive odd starts
remain in the larger interval. This count is fixed while each gain is
$O(m)$ and the available width is proportional to $3^m$. The orbit
reaches the unique cycle and then the target phase. At that phase the
seed already equals $b_m$ modulo $2D$. Successive full cycles add
$2D$ times the integer winding to the seed. Within $M$ cycles one
start equals $b_m$ modulo $M$, even when $M$ has a binary factor.
It also equals $b_m$ modulo $2D$ there, which preserves all fifteen
fine bulk labels. Its final gap is exactly
$1-(42981185/32768)(s-b_m)<0$ by the common affine trace.

## The lifted 140-digit family

The third row uses the [lifted halting seed](LIFTS758.md) on
$m\equiv292\pmod{242660}$. It gives an actual cusp reset congruent to
$H_m$ modulo any fixed $M$. Its neighborhood is a fixed interval
inside $1<s/3^m<251/250$. The narrower-neighborhood assertion above applies to the two cusp siblings.
For this row the cusp construction uses the complete odd return
$J^mP^7J^{13}LR$. Inverting the thirteen jumps and seven pairs
from limiting direction $4/9$ produces a strict open corridor in
the cusp. The gain in $z$ is $m+33+B(y)$. The final bulk high flag
flips relative to the unpadded graph since the seven pairs leave
$u=(a+2c-1)/2$ even and each padding jump flips the low bit of $d$.
The published formula for $H_m$ gives seed residue $57901\pmod{65536}$
at every exponent in this row, which corresponds to $y=28726$.
The same winding argument proves the claimed congruence.

Run the checker beside the existing cusp and lift verifiers with
Python 3.10 or later.
