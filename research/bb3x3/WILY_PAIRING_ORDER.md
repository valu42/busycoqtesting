# Exact signs of Wily odometer excursions and their endpoint order

For a negative Wily integer $e$ with $F(e)>0$, write $P(e)$ for its first
positive predecessor under $G=F^{-1}$. On the entire
[punctured cone at 3](WILY_SHELL_CONE.md) the sign test and the computation
of $P$ reduce to a single comparison of odometer digits. Every exit in this
cone satisfies $P(e)>(18/7)|e|$. There are nevertheless crossings in the
pairing both in ordinary signed order and on the actual blank's 32-bit
prefix cycle. The blank's all-time outcome remains open.

## Four intervals determine every coefficient sign

Use the integer odometer track $m$ and fixed decorations $d_i$ for an odd
coefficient $a$, so $H(a)=G(a)+3$ decreases $m$ by one. Discard trailing
zero decorations. This leaves the track unchanged because zero decorations
are precisely the ordinary high pairs $(b,1-b)$. Let $s$ be the remaining
number of decorations. If $s=0$, or the highest decoration $d=d_{s-1}$ is
at least 3, then $a(m)>0$ exactly when $m<0$. If $d$ is 1 or 2, put
$h=2^{s-1}$. Then
$$
 a(m)>0 \quad\Longleftrightarrow\quad m<0\quad\text{or}\quad h\le m<2h.
$$

To prove this, write $M=\lfloor m/2^s\rfloor$. For $M\ge1$ the coefficient
is negative, and for $M\le-2$ it is positive, by the high-digit numerator
formula. For $M=-1$ and $M=0$ the upper numerators are respectively
$-1$ and $-2$. Appending $\ell$ low physical digits of value $z$ therefore
tests $z/2^\ell>1/3$ or $z/2^\ell>2/3$, respectively. If $s=0$ the only
low digit is 1 and the claim follows. Otherwise the highest decorated block,
read from its *most* significant end, is $1,0^{d-1},b,b$, where $b$ is
the highest retained track digit. Its first bit exceeds the first bit of
$1/3=(0.0101\ldots)_2$. Against $2/3=(0.1010\ldots)_2$, the block is
strictly greater exactly when $d\in\{1,2\}$ and $b=1$. The comparison is
settled within this block independently of all lower digits.

Hence for a negative coefficient the first positive forward track occurs at
$h$ if $0\le m<h$ and a finite positive interval exists. In all other
cases the coefficient remains negative forward. In the inverse direction
the nearest positive track is $2h-1$ if that interval exists and
$m\ge2h$. Otherwise it is $-1$. This gives the exact number of singular
reference contacts and the positive coefficient without iterating $H$.

## Every finite coefficient excursion enlarges the paired magnitude

Suppose $a<0$ and $H^{-1}(a)>0$. The sign classification forces
$d\in\{1,2\}$, $m=h-1$ and the preceding positive track $-1$. Exactly
$h=2^{s-1}$ applications of $H$ reach its positive coefficient $q$.
Let $u=1+\sum_{i<s-1}(d_i+2)$ count the physical bits below the highest
decoration and let $z$ be their common value. The two endpoints have
identical lower track digits, all ones. The highest physical block goes
from $1,0^{d-1},0,0$ to $1,0^{d-1},1,1$ in most-significant-first order.
Using the high numerators $-2,-1$ gives
$$
 a=3z-2^u2^{d+1},\qquad q=3z+2^u(9+2^{d+1}).
$$
The fraction $r=z/2^u$ exceeds $1/3$. It starts at $1/2$ on the initial
physical bit 1. Each zero decoration with track bit 1 updates $r$ to
$(1+r)/4$; each positive decoration appends a highest bit 1. Thus
$$
 \frac{q}{|a|}=\frac{9+2^{d+1}+3r}{2^{d+1}-3r}>
 \begin{cases}14/3&d=1,\\18/7&d=2.\end{cases}
$$
The two lower bounds are limiting values when every lower decoration is
zero and their number tends to infinity.

For an escaping $e=3+2^j a$ with $a$ odd and $j\ge30$, the forward step
from the center 3 undoes the last singular reference step from 0. Therefore
$H^{-1}(a)>0$. The previous positive is $P(e)=b+2^j q$ with $b\ge0$,
so the lower bound above implies $P(e)>(18/7)|e|$. The reference return
has 96 singular slots. The positive predecessor occurs in slot
$2^{s-1}\pmod {96}$, which gives only seven possible residues $P(e)\bmod2^j$:
18, 318, 2,595, 96,462, 20,988,222, 90,835,491 and 25,138,494.
The blank cycle omits 3 modulo 128, so this particular estimate does not
cover a possible blank exit.

## Discontinuity and crossings

For $j\ge30$, two explicit families of escape inputs are
$$
 e_j=S^j(-8)=3-5\cdot2^j,\qquad
 f_j=S^j(L(S(-8)))=3-19\cdot2^j.
$$
The inverse reference from 3 visits $18,33,36,63,318$ in that order.
Steps 1 and 5 are singular. The first sends coefficient $-5$ to 29.
For $-19$ the two singular steps give $-37,253$. Thus
$$
 P(e_j)=18+29\cdot2^j,\qquad P(f_j)=318+253\cdot2^j.
$$
The inputs agree through $j$ low bits, while the outputs differ modulo 8.
Consequently $P$ has no continuous extension to the center 3.
There is also no deterministic subsequential finite-state transducer from
little-endian signed binary inputs to little-endian binary values of $P$.
On these two inputs it can emit at most two bits while reading their
common prefix. Only boundedly many input bits remain, and each transition
and final state emits a bounded string, whereas the output lengths grow
with $j$. The same argument applies if the input alphabet gives the forest
lifts from outermost to innermost, since the shared prefix is then $S^j$.
This excludes that specific reading direction and output representation.

The endpoints interleave in ordinary order:
$$
 e_{j+2}<f_j<0<P(e_{j+2})<P(f_j).
$$
They also cross on a complete modular cycle that contains the blank.
Let $w=\text{SSSSLLSSSSSSSLSLSLLSSLSL}$ and
$v=\text{LLLLLLLLSLSSLSLLLLLSS}$, applying the rightmost lift first.
Their total binary weights are 32 and 36. For $j\ge43$ set
$$
 A_j=w(3)-79\cdot2^j,\qquad B_j=v(3)-19\cdot2^j.
$$
Both are escapes. In fact $A_j=w(S^{j-32}(-82))$ with
$-82=L(L(S(-8)))$, and $B_j=v(S^{j-36}(-22))$. When $j$ is odd
both inputs have the blank checkpoint's residue 1 modulo 3.

| Exit family | Reference center | Singular steps through first positive | $P$ |
|---|---:|---|---|
| $A_j$ | 25,543,214,355 | 1,376, 2,398, 2,414, 4,209 | $12,683,447,586+1009\cdot2^j$ |
| $B_j$ | 85,963,243,518 | 513, 4,609 | $350,576,705,541+253\cdot2^j$ |

The displayed paths have all reference centers below $2^{40}$. The inverse
recursion decreases its input by at least a factor two until a translation
or zero leaf, so $j\ge43$ suffices for every low branch test before a
leaf. A translation leaves the coefficient fixed; a zero leaf applies $H$.
The coefficient sequences at the singular steps are
$(-79,-73,-151,-145,1009)$ and $(-19,-37,253)$. Their signs give the
claimed first positive predecessors.

The full blank cycle modulo $2^{32}$ has 32,768 phases, starting at $n_*$.
Its order is $P(A_j)$ at phase 13,702, $P(B_j)$ at 15,513,
$A_j$ at 17,911 and $B_j$ at 20,122. Thus preserving noncrossing chords
on a modular blank cycle is not an invariant of the true signed pairing.
A longer prefix can distinguish these particular families.

The crossing persists after imposing the [dihedral invariant](WILY_DIHEDRAL.md).
Take $A_{43+12t}$ and $B_{51+12t}$ for any $t\ge0$. Both have residue 1
and the identity invariant, just as the blank does. To verify all $t$,
compute the labels at $t=0$. An extra twelve short lifts inside either
outer word preserve the raw label and residue since a single short lift
cycles through all twelve possible states.

The failure of low-first transduction persists on this filtered set.
Compare $A_{43+12t}$ with $C_{44+12t}$, where
$C_j=w(3)-5\cdot2^j=w(S^{j-32}(-8))$. Both exits match the blank's
32-bit orbit, residue class, and dihedral invariant. The first singular
step gives $P(C_j)=44,897,140,755+29\cdot2^j$, which is odd, whereas
$P(A_j)$ is even. The two inputs share arbitrarily long low prefixes
and also arbitrarily long outer lift words with bounded suffixes. Hence
even the first output bit can depend on the very end of either encoding.

Run the two independent certificates:
```sh
python3 wily_shell_cone.py
python3 wily_pairing_order.py
```
