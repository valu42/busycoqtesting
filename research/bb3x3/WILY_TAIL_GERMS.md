# What a periodic Wily reference can induce on the high bits

Call a virtual sweep singular when its carry never stops on the infinite
binary word. On a periodic orbit of the scalar map $F=s_0$, **every nontrivial
action induced sufficiently high on the tail has one of two forms**. On an
eventually zero reference it is a power of $s_2$. On an eventually alternating
reference it fixes the matching alternating tail. At the first differing bit
it acts on the rest as a power of $F$, possibly conjugated by a first-bit
flip. All other reference periods act as the identity sufficiently high.
This gives a test for proposed periodic-reference reductions and leaves
the forward sign question of the actual blank checkpoint open.

## Two successive singular sweeps

Take any two consecutive singular sweeps in chronological order. All sweeps
between them stop after finitely many bits. Above the largest of those
positions, their two active carries operate successively on the same column.
Only $s_0,s_1,s_2$ can remain active forever. Writing $ij$ for the ordered
pair $(s_i,s_j)$, the following are all transitions that retain two such
carries. An entry gives the next pair. The columns refer to the original
input bit.

| Pair | 0 | 1 |
|---|---:|---:|
| 00 | 12 | 21 |
| 01 | 10 | — |
| 02 | 11 | 22 |
| 10 | — | 01 |
| 11 | — | — |
| 12 | — | 02 |
| 20 | 21 | 12 |
| 21 | — | 10 |
| 22 | 22 | 11 |

The only recurrent components are the loop at 22 on zero and the
01–10 cycle on alternating bits. An infinite path enters one of them
after at most three transitions. Its successive input and final output
bits there are identical. On the alternating component the intermediate
bits are the opposite phase. These facts follow directly from the
[original carry table](check_bb33.py).

Consequently a ray whose tail is neither eventually zero nor eventually
alternating has at most one singular sweep in its forward orbit. Before
its first singular sweep, each update changes a finite prefix. A second
would force the starting tail to have one of the two forms above.
In particular, on a periodic orbit with any other tail, every sweep is
regular, since a single singular sweep would recur one period later.

## The return action in a neighborhood of a periodic reference

For a reference of finite period $P$, choose a cutoff above all stops
of its regular sweeps and all transients of its singular sweeps over one
period. If there are no singular sweeps, $F^P$ fixes the entire cylinder
of points sharing the reference prefix. With an eventually zero tail,
the only indefinitely continuing state on sufficiently high zero bits is
$s_2$, so the return on the tail is $s_2^c$, where $c$ is the number of
singular sweeps. Its odometer is described in the [shell calculation](WILY_SHELL_CONE.md).

With an alternating tail each singular sweep swaps the two phases. In a
full period their number is even, say $2m$, and the high carries alternate
between $s_0$ and $s_1$. Put $U=(s_0,s_1)$ and $V=(s_1,s_0)$, with the first
listed carry applied first, and $J=s_3$. Both $U$ and $V$ fix the bit they
read. Their sections on the remaining suffix are

| Pair | After reading 0 | After reading 1 |
|---|---|---|
| $U$ | $V$ | $JFJ$ |
| $V$ | $F$ | $U$ |

For the off-diagonal cases, the literal sections are respectively
$(s_2,s_3)$ and $(s_3,s_2)$. The identities follow because $J$ is an
involution and consecutive $s_3,s_0$ equal $s_2$ on infinite words.
Thus $U^m$ or $V^m$ fixes every matching alternating bit as well as the
first mismatch. Beyond that mismatch its exact action is $F^m$ or
$JF^mJ$. A sufficiently high alternating-periodic reference therefore
recovers the original scalar problem on a shorter tail. The reference's
finite intermediate phases still matter to a physical safety proof.

The blank orbit has a [verified singular sweep in its past](WILY_INTEGER_MAP.md#an-obstruction-to-a-bounded-zero-tail-reference-for-the-blank-orbit).
It cannot be captured by a regular-reference cylinder on which *all*
sweeps over the period stop before the cutoff. Such a cylinder returns to
itself, and all its phases also have regular sweeps. The existing
zero-reference obstruction also applies on the blank orbit. Any new
periodic capture using this method must use the alternating case and
control the induced shorter-tail orbit.

## The actual finite path excludes alternating sections through width 763

At every cutoff from 1 through 68, the full cyclic stream from $n_*$ contains
a 2 or 3. At width zero it is a single 0. At each odd scalar width 69 through
765 the first arrival is 3 by the [blank edge replay](WILY_INTEGER_MAP.md#checking-the-sign-along-the-blank-run).
For each such width through 763 the next arrival is 0. Scalar widths count
the suffix after its two fixed low bits have been removed.

At an intervening even width, the first arrival must be 1: the 3 at the
previous odd width flips the untouched 1 to 0 and stops, and the following
0 reads that 0, writes 1, and emits 1. A pure alternating period at this
even width would therefore start 10. Its initial untouched bit is 0.
Reading these two events produces 3 followed by 2 at the next odd width.
That contradicts the actual 3 followed by 0 whenever the latter pair is
certified. Thus no full return stream is a power of 01 or 10 at widths
0 through 763, or at width 765. The argument uses the chronological
stream; it does not exclude other words inducing the same action after
algebraic simplification.

Run `python3 wily_tail_germs.py`. The [checker](wily_tail_germs.py) verifies
the finite pair graph and compares both first-mismatch formulas against
literal products for all nonmultiples of three from −1024 through 1024
and exponents zero through eight.

## Two additive invariants of positive carry products

For any positive (no inverses) word $W$ of carries, write
$A(W)=\#s_0+\#s_2$ and $B(W)=\#s_1$. If two such words act identically
on the binary tree, both counts agree. In particular, any positive word
with $A+B>0$ has infinite order as a tree automorphism. Its action on an
individual point can have finite order.

To prove this, call an automorphism *finitary* when all its sections at
some finite level are the identity. Finitary automorphisms form a subgroup.
Let $N_k(W)$ count the length-$k$ prefixes on which the section of $W$ is
not finitary. The individual nonfinitary carries are exactly 0, 1, 2.
From the carry table, with Fibonacci numbers $F_0=0,F_1=1$,

$$
N_k(s_0)=N_k(s_2)=F_{k+2},\qquad N_k(s_1)=F_{k+1},\qquad N_k(s_3)=0.
$$

Indeed, 0 and 2 each have one section of type 1 and one of type 0 or 2.
Type 1 has one nonfinitary section of type 0. Every preceding factor
permutes length-$k$ prefixes, so the sum of the individual nonfinitary
section counts in the product is $A(W)F_{k+2}+B(W)F_{k+1}$.
When exactly one factor has a nonfinitary section, its product section is
nonfinitary by the subgroup property. All-finitary sections give a
finitary product. A discrepancy can occur only when at least two factors
remain in states 0, 1, 2 at level $k$.

For a fixed word $W$ the number of these exceptions is polynomially
bounded in $k$. Process the binary input with a finite graph storing all
factor states, discarding paths once fewer than two remain in 0, 1, 2.
States can leave this set, pass through 3, and stop. None reenters. On
any infinite path of the retained graph, select a cutoff above every
factor that eventually stops. The first two surviving factors are then
adjacent active carries, and the table above forces the input eventually
to be zero or alternating. Thus this finite graph accepts only countably
many infinite paths. A reachable recurrent component must be a simple
directed cycle, counting parallel edges separately: two choices of
return loops within a component would give uncountably many paths.
The acyclic graph of components bounds the number of cycle visits, so
choosing the number of turns on each cycle gives a polynomial bound on
paths of length $k$. Each exceptional prefix contributes at most $|W|$
to the discrepancy. It follows that for some polynomial $p_W$,

$$
N_k(W)=A(W)F_{k+2}+B(W)F_{k+1}+O(p_W(k)).
$$

Equal automorphisms have equal $N_k$. Divide their difference by
$F_{k+1}$ and take $k$ to infinity. The limit gives
$(A-A')\varphi+(B-B')=0$ with irrational $\varphi$, hence the two
integer differences vanish separately.

In particular, either alternating power $U^m,V^m$ has $A=B=m$. The
[checker](wily_tail_germs.py), run with `--counts`, constructs the exact
return words of the blank checkpoint at cutoffs 0 through 350 using the
[run-length recurrence](wily_edge_stream.py). Equality of the two counts
holds only at widths 1, 14 and 34, with $m=1,20,15$ respectively. At each
of those widths an explicit integer input distinguishes the product from
each candidate alternating power. Thus algebraic simplification cannot
produce either alternating power at any of these 351 cutoffs.

## A sublinear bound for finding the positive predecessor of any exit

For every virtual $F$ orbit and every binary prefix of width $r\ge1$,
its period divides $2^{1+\lfloor 2r/3\rfloor}$. If $e<0<F(e)$ and its
canonical bucket is $B(e)=2^r$, its first positive predecessor $P(e)$
therefore occurs within $2^{1+\lfloor 2r/3\rfloor}=O(|e|^{2/3})$ inverse
updates. The [known lower-bound family](WILY_INTEGER_MAP.md#a-family-with-a-long-wait-for-the-preceding-positive-state)
requires order $\sqrt{|e|}$ updates.

At each prefix let $W$ be the chronological word emitted over its least
return period. For this argument take all counts modulo two. Set
$R=\#s_0+\#s_1+\#s_3$, the parity of bit flips, and keep
$A=\#s_0+\#s_2$ and $B=\#s_1$. When the next bit is adjoined, its
prefix period doubles exactly when $R=1$. For either choice of incoming
bit, let $R_i,A_i,B_i$ describe the emitted section during one reading
of $W$. Then

$$R_i+B_i=B.$$

Indeed, $R_i+B_i$ counts the outgoing 0 and 3. Only an incoming 1 emits
one of these, and it does so on either bit value. When $R=0$, the new
return word is this one section. When $R=1$, the second reading starts
with the opposite bit, and together the two readings feed both bit
values to each occurrence of a carry. The combined counts are therefore

$$ (R',A',B')=(A,A+B,A). $$

In particular, the first doubling establishes $R'=B'$. This equality
persists at all later cutoffs. Another doubling gives it directly from
the displayed formula. At a fixed bit, $R=B=0$ gives it from the
one-section equation. After the first doubling no three consecutive
extensions can double. For the first two to double requires
$R=B=A=1$ at the first. At the next cutoff $A'=A+B=0$, so the second
doubling gives $R''=A'=0$ at the third cutoff.

From $F$ the first bit always doubles. Among its next $r-1$ bits at most
$(r-1)-\lfloor(r-1)/3\rfloor$ can double by splitting off triples. The
total exponent is at most $r-\lfloor(r-1)/3\rfloor=1+\lfloor2r/3\rfloor$.
The empty prefix has period one. In particular the set of prefixes visited
by a single orbit has zero limiting proportion among all binary words.

By the [canonical-bucket order](WILY_INTEGER_MAP.md#a-negative-escape-always-has-a-positive-predecessor),
until reaching a positive state the inverse iterates of $e$ lie in
$[-B(e),-1]$. All exits have $B(e)\ge8$, so even the exceptional negative
transition through $-1,-2$ fits in this interval. It contains exactly one
integer of each residue modulo $B(e)$. If the first $p$ inverse steps
remained negative, for $p$ the prefix period at width $r$, the $p$th
iterate would equal $e$. Its preceding iterate (the $(p-1)$st) would
then equal $F(e)>0$, a contradiction. Congruences of the digit integer
and its numerator are equivalent because 3 is odd. Canonical negative
buckets in one residue class differ by a factor of four, hence
$B(e)<4|e|$. The checker verifies both one-bit parity rules, the
period bound on every prefix through width 14, and the positive-predecessor
bound on every exit down to −4096. A finite forward excursion could still
extend arbitrarily far before this backward estimate applies.

A finite prefix can have substantially larger period than the square root
of the bucket size. Take the 63 little-endian bits of the ordinary binary
integer $1\,317\,624\,506\,749\,325\,312$. Its exact prefix period is
$2^{43}$: the first three bits all double the period, then every successive
triple fixes it at the first bit and doubles it at the next two. The
`--counts` checker verifies all 63 applications of the literal one-bit
rule. This single prefix gives no asymptotic lower exponent.

The same three-step pattern cannot be proved to persist by finding a
cycle of bounded positive return words whose counts recur. If the fixed
step gives a section with counts $(a,b)$, then $a+b$ is at least the old
$A$, since every 0 or 2 has a nonfinitary section on either bit. Each
doubling gives both sections in succession, hence changes counts by
$(a,b)\mapsto(a+b,a)$. Two doublings give new first count $2a+b$.
For both doublings to occur, $a$ is odd: the second flip counts the
root swaps of the first child's two sections, namely $a\bmod2$ by the doubling formula.
Consequently the new first count is strictly larger than the old $A$.
This rules out a bounded positive-word cycle for this pattern, even
allowing equal group elements or cyclic rotations of the chronological
word. Growing sections can still realize the pattern.
