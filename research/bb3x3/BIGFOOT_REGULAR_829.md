# A restriction on inductive proofs for Bigfoot

Let $B(a,x)=A(a,2x+1,2)$ be the state at a four-step boundary. An inductive
safety set contains $B(2,0)$ and, from every member, all four macro-steps
must be live and their endpoint must be another member. **No finite automaton
reading the aligned digits of $(a,x)$ recognizes such a set, in any integer
base $k\ge2$.** This leaves proofs that use other representations or
additional unbounded information open.

There is a separate result about individual fibers. **Every infinite regular
language of nonnegative integer lengths in a base coprime to three contains
arbitrarily large lengths that halt at any fixed starting counter $a$.**
For example, from $B(2,2^j)$ every
$j\equiv7\pmod{4374}$ takes the halting branch on macro-step eight. This
follows by replaying $x=128$ and checking $2^{4374}\equiv1\pmod{3^8}$.
These statements concern blank-tape proof methods. They do not establish
that the blank tape halts or runs forever.

## Forcing a halt in a ternary residue class

Fix $a$, a representative $x_0\ge0$, and any prescribed initial precision
$3^v$. Follow $n=\lceil v/4\rceil$ four-step groups from $x_0$. All lifts
$x_0+81^n t$ take the same branches. If one of those branches halts, this is
already a halting residue class. Otherwise, if the representative ends at
$B(h,y)$, the lift ends at $B(h,y+256^n t)$. This is the [four-step lift
identity](BIGFOOT_BLANK_829.md).

Put $m=\lfloor h/2\rfloor+1$. Choose $t$ to solve
$175(y+256^nt)+502\equiv0\pmod{81^m}$, possible since the coefficient of
$t$ is invertible. The lifted endpoint is then $5\pmod{81}$ and its next
group loses two if it survives. Its length update $F$ satisfies
$175F(y')+502=256(175y'+502)/81$, so the loss repeats until it halts.
Thus the original class contains a whole halting subclass. Its precision is
at most $81^{n+m}$. [Losing group](RANKINGS.md#bigfoot--why-a-finite-residue-test-can-be-misleading)

## Pumping an infinite regular language

Use base-$k$ strings with no leading zeros. An arbitrarily long accepted word
contains a nonempty digit loop after its first digit, by the pigeonhole
principle on automaton states. Pump it $j$ times between the same prefix and
suffix. Let $p\ge1$ be the prefix value, $w$ the loop value, $f=k^{\ell}$
for its positive length $\ell$, and $d$ the suffix length. Denote by $x_0$
the value when the loop is omitted. These accepted lengths satisfy
$$
x_{2h}=x_0+D\,U_h,\qquad D=k^d(p(f-1)+w)(f+1),\quad
U_h=\frac{Q^h-1}{Q-1},\quad Q=f^2.
$$

Since $Q\equiv1\pmod3$, the numbers $U_h$ for $0\le h<3^t$ permute all
residues modulo $3^t$, for every $t$. Indeed $U_b-U_a=Q^a U_{b-a}$ when
$b>a$. If $3\nmid j$, then $U_j\equiv j\pmod3$. Multiplying $j$ by three
multiplies $U_j$ by $1+Q^j+Q^{2j}\equiv3\pmod9$. Consequently
$v_3(U_b-U_a)=v_3(b-a)$. As $D>0$, the pumped lengths therefore represent
every residue in the class $x_0\bmod 3^{v_3(D)}$ at every finer precision.
They enter the halting subclass just constructed for an entire arithmetic
progression of $h$. Those lengths are unbounded.

## Why every integer base fails for a blank invariant

Represent $(a,x)$ by padding the shorter canonical digit string on the left
with zeros and reading the two strings together from the most significant end.
Reversing the reading order leaves the class of regular languages unchanged.
Take a deterministic automaton for the regular set. Suppose that this
set is inductively safe and contains the blank. Its orbit must then survive forever. All the following lengths occur.

Write $x_n$ for the length after $n$ groups and $\theta=256/81$. The 81
residue cases give $x_{n+1}=\theta x_n+e_n/81$ with $126\le e_n\le518$.
Consequently $x_n/\theta^n$ converges to a positive constant $C$, by summing
the geometric series of bounded increments. For every integer $k\ge2$ the
ratio $\log_k\theta$ is irrational: no positive power of $256/81$ is an
integer. Hence $\log_k x_n=n\log_k\theta+\log_k C+o(1)$ visits the
interior of every fractional-part interval infinitely often, by density of
irrational rotations. **Every nonzero canonical base-$k$ digit string
therefore occurs as a leading prefix of arbitrarily large $x_n$.** The
counter satisfies $0\le a_n\le2+4n$, so, for a fixed prefix, all its
corresponding counter digits are zero at sufficiently large occurrences.

For each positive integer $p$, reading the digits of $p$ against counter
zeros thus reaches a state with some accepting continuation. For each such
state $s$ choose one accepting suffix seen on a true blank orbit, of length
$d_s$. Reading that suffix completes *any* prefix reaching $s$ to a member
of the set with a fixed counter $a_s$ and length $k^{d_s}p+c_s$ for a fixed
$c_s$. Leading zero padding is valid since $p$ starts with a nonzero digit.

It is possible to choose one $p$ for which **all** of these putatively
accepting suffixes instead lead to halting configurations. Begin with all
positive $p$ and refine a ternary residue class once for each of the finitely
many suffixes. If the current class is $p_0\bmod3^t$, put
$K=k^{d_s}$ and $w=v_3(K)$. Its possible $Kp+c_s$ cover all refinements
of $Kp_0+c_s\bmod3^{t+w}$ in ternary precision, since $K/3^w$ is a unit
modulo three. Use the halting-cylinder construction at $a_s$ to obtain a
halting subclass, then pull that subclass back to a finer class of $p$.
Earlier halts persist. A positive representative after the last refinement
must reach some productive state, yet its chosen accepting suffix halts.
This contradiction proves the all-base obstruction.

A parallel argument excludes any predicate built from finitely many
integer polynomial inequalities in $a,x$ and congruences with fixed moduli
using Boolean operations. At fixed $a$, every polynomial has constant sign
beyond a polynomial bound in $a+1$: regard it as a polynomial in $x$, bound
its coefficients by a polynomial in $a+1$, and use the ordinary root bound
$1+\max_{i<d}|c_i|/|c_d|$ when its degree is positive. A nonzero integer
leading coefficient has magnitude at least one, including when the degree
drops after substitution. Membership beyond the bound therefore depends only
on $x$ modulo a fixed integer. Every full arithmetic progression there
contains a halting seed, by the ternary construction and the Chinese remainder
theorem on the factors coprime to three. A safe inductive set in this class
would bound $x$ by a polynomial in $a+1$, again contradicted by the blank
path's growth.

Run `python3 bigfoot_regular_829.py` in this directory. The [checker](bigfoot_regular_829.py)
constructs halting residue classes for 72 pumped families in eight bases,
tests their macro-steps against the original rules, replays the explicit
power-of-two example, and constructs simultaneous counterexamples to suffix
lists in bases 2, 3, 6, 9 and 10.
