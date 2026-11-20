# An exact odometer and a two-sided sign test for Wily

Let $F$ be the [single Wily map](WILY_INTEGER_MAP.md) and $G=F^{-1}$.
For **every negative** $n=3+2^j a$, where $j\ge30$ and $a$ is odd and
prime to three, an exact finite test decides whether *all* forward virtual
iterates stay negative. The first positive backward iterate also has an
exact formula. For example, every $n=3-2^j$, $j\ge30$, stays negative
forever under $F$ and gives a nonhalting Wily suffix in its canonical
bucket. The actual blank orbit lies outside this class: at level seven its
cycle of residues omits 3 modulo 128.

## Reading the $s_1$ orbit as an ordinary binary counter

Write $g=s_1$, $h=s_2$, and $J=s_3$ on infinite binary words.
$J$ flips just the first bit. The map $h$ reads zeros without writing
and, at the first one, passes $g$ to its remaining suffix. In chronological
order $J,h$ act as $s_0$. These identities follow from the four
[carry rules](check_bb33.py).

Parse a word with infinitely many ones into digits $b_i$ and nonnegative
integers $d_i$. Take its first bit $b_i$, flip the first bit of the
remaining suffix if $b_i=1$, read $0^{d_i}1$, and repeat on the rest.
The $d_i$ are **invariant under $g$**. The bits $b_i$, read little-endian,
are incremented by exactly one. Indeed, $g$ flips the first bit. When it
reads 0 it sends $J$, so normalization at the new first bit 1 restores the
old normalized suffix. When it reads 1 it sends $s_0$, which applies $J$
then $h$. This sends $h$ to the old normalized suffix; $h$ preserves its
leading $0^{d_i}1$ and passes $g$ further. This is binary addition with a
carry. The identities hold at every finite depth, including the case of an
infinite carry.

For an eventually alternating word, all sufficiently late $d_i$ are zero:
as soon as parsing starts in the alternating tail each block is a pair of
unequal bits. All sufficiently late $b_i$ are then the same. Its digit
track $m=\sum_i b_i2^i$ is an ordinary signed integer.

On odd numerators put $H(a)=G(a)+3$. On the bits of $a/3$, $G$ reads
the initial 1, writes 0 and passes $g^{-1}$ to the tail. Adding one to
the resulting binary value restores the initial 1 without a carry.
Therefore on the tail digit track **$H$ subtracts one and $H^{-1}$ adds one**.

Write $s$ for the number of blocks parsed before the remaining tail is
purely alternating and retain the first $s$ decorations. At any other
track value $m'$ the remaining high track integer is $M=\lfloor m'/2^s\rfloor$.
There the physical pairs are $(b_i,1-b_i)$. Put
$D(q)=\sum_i q_i4^i$ for the binary digits of $q\ge0$. The high
numerator equals $-2-3D(M)$ for $M\ge0$, or $-1+3D(-1-M)$ for $M<0$.
These formulas follow by summing the pair digits $2-b_i$ in base four,
using $1+4+4^2+\cdots=-1/3$ in the binary integers. The lower decorations
and leading 1 reconstruct $a$ exactly. Appending them as the low $\ell$ bits gives the full numerator
$3z+2^\ell c$, where $0\le z<2^\ell$ and $c$ is the high numerator. Hence $M\ge1$
forces $a<0$, and $M\le-2$ forces $a>0$. To decide forward sign it is
enough to classify the two remaining high digits $M=-1,0$. The
[exact sign intervals](WILY_PAIRING_ORDER.md) depend only on the last
nonzero decoration and the track, so the checker computes both the first
sign crossing and its coefficient directly.

## A return map on an entire congruence class

For the reference center only, extend $G$ to nonnegative multiples of three
by the same inverse action on the bits of $b/3$. Here $G(0)=3$: the inverse
of $s_0$ on all zeros writes one and passes $h^{-1}$, which fixes all zeros.
Use the integer inverse recurrence from the [scalar checker](wily_integer_map.py).
A reference step is called singular if its recursion reaches 0. All its other
leaves are the translation cases $b\equiv1,5\pmod8$. Starting from 3 gives
an exact cycle with 8,192 distinct reference numerators. Its minimum is 0,
its maximum is 94,370,751, and exactly 96 of its steps are singular.

At any reference point $b$, add $2^j a$ with $j\ge30$. The reference
recursion consumes at most 27 low bits before reaching a leaf. All branch
tests agree up to that leaf. At a translation leaf the lifted successor is
$G(b)+2^j a$. At a zero leaf use, for every odd unit $u$ and $k\ge1$,
$$
G(2^k u)=3+2^k(G(u)+3).
$$
For $k=1$ the inverse has the form $2G(u)+9$; later doublings apply
$y\mapsto2y-3$. Restoring the same number of binary places that the
recursion removed gives $G(b)+2^j H(a)$ at the singular step. Since
$H(a)$ remains an odd unit, the description iterates indefinitely in
both directions. In particular,
$$
G^{8192}(3+2^j a)=3+2^j H^{96}(a).
$$
Throughout the reference cycle $0\le b<2^j$, so the lifted numerator has
the sign of its coefficient. In forward time the coefficient successively
takes $H^{-1}$ steps at the reversed singular contacts. Every positive
track value sufficiently far forward corresponds to a negative coefficient.
For $a=-1$ its tail track is zero with no decorations; every larger track
value has negative coefficient. The resulting negative orbits cannot meet
$-2$, since $b$ is smaller than $2^j-2$, or require a positive-input
edge correction. The scalar sign criterion gives the stated nonhalting
family.

For the first positive predecessor, let $k$ be the first positive integer
such that $H^k(a)>0$. Existence follows from the negative end of the digit
track. The $k$th singular reference contact gives the exact step and the
coefficient $H^k(a)$. A second bound explains the cost of computing $k$.
Let $B=2^r$ be the canonical bucket of $a$. While $H(a)$ is negative,
$G(a)$ is also negative and the backward bucket bound applies; the exceptional
step from $-1$ already gives $H(-1)=1$. Adding three preserves the residue
and can only reduce the required bucket. The period of $g$ on a length-$t$
prefix is at most $2^{\lceil t/2\rceil}$: its square removes the first
digit block of length at least two, or already fixes the prefix. Thus the
period of $H$ on the low $r$ bits divides $2^{\lfloor r/2\rfloor}$. If
the first full such period stayed in $[-B,-1]$, its endpoint would equal
$a$ by the congruence, contradicting translation by a nonzero number on its
integer track. Therefore $k\le2^{\lfloor r/2\rfloor}$.

Run `python3 wily_shell_cone.py`. The [checker](wily_shell_cone.py)
replays the reference cycle, compares both coefficient signs at every
phase with the true inverse, checks the odometer in both directions on
thousands of odd inputs, and compares predicted positive predecessors
against individual inverse steps.
