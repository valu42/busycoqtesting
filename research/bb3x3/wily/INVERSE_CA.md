# A clipped linear cellular automaton for Wily's inverse pass

This note gives exact, unbounded structural results. It **does not decide the
blank orbit**. The finite checker is `inverse_ca.py`; the proofs below do not
depend on its enumeration depth. The companion `TAIL_RENORMALIZATION.md`
specifies the exact bridge between infinite completions and finite boundaries.

Write `a,b,c,d` for the four transducer modes. On infinite words,

\[
\begin{array}{c|cc}
 &0x&1x\\\hline
a&1b(x)&0c(x)\\
b&1d(x)&0a(x)\\
c&0c(x)&1b(x)\\
d&1x&0x.
\end{array}
\]

All four maps are automorphisms of the rooted binary tree. Identify an infinite
word with its coefficient series in \(\mathbb F_2[[z]]\), in scan order. Put

\[
 P=1+z+z^2,\qquad D=z+z^2=P+1,
 \qquad t=(10)^\omega=\frac1{1+z^2}.
\]

Addition in this note is XOR. These series identities must not be interpreted
as ordinary integer identities by substituting \(z=2\).

## 1. Exact inverse, with a stopping position

Let \(Y=y_0y_1\ldots\) be any output word. If its first adjacent pair `11` is
at positions \(j,j+1\), define

\[
 Q(Y)=\sum_{i=0}^{j}y_i z^i.
\]

If no `11` occurs, define \(Q(Y)=Y\). Then

\[
 \boxed{a^{-1}(Y)=Y+1+D Q(Y).}\tag{1}
\]

In particular, on the Fibonacci subshift

\[
 \mathcal S=\{Y:\text{no adjacent pair `11` occurs}\},
\]

the inverse is the affine linear cellular automaton

\[
 \boxed{a^{-1}(Y)=P Y+1\qquad(Y\in\mathcal S).}\tag{2}
\]

**Proof.** Before copy mode is reached, the active state records the last two
output bits, with fictitious initial memory `10`:

\[
 a\leftrightarrow10,\quad b\leftrightarrow01,
 \quad c\leftrightarrow00,\quad d\leftrightarrow11.
\]

This assertion follows directly from all six transitions out of `a,b,c`.
While the previous output memory is not `11`, the incoming bit therefore is

\[
 x_i=y_i+y_{i-1}+y_{i-2},\qquad y_{-2}=1,
 \quad y_{-1}=0.
\]

The first output `11` enters `d`. Its next incoming bit is the complement of the
next output bit, after which all subsequent bits are copied. Formula (1) gives
exactly these three phases: the linear rule through position \(j+1\), a flip at
position \(j+2\), and identity afterwards. If there is no `11`, the linear rule
continues forever and gives (2). This also proves that reaching copy is
equivalent to the output containing `11`. ∎

A useful affine change of coordinates is

\[
 Z(X)=1+D X.
\]

Equation (1) becomes

\[
 \boxed{Z(a^{-1}Y)=P Z(Y)+D^2\bigl(Y+Q(Y)\bigr).}\tag{3}
\]

The second term is a suffix defect. When the first `11` is at \(j,j+1\), its
first potentially nonzero coefficient is at position \(j+3\); indeed
\(Y+Q(Y)\) starts with its second `1`, at \(j+1\), and \(D^2\) starts at degree
two. On \(\mathcal S\) the defect is zero. The identity
\(P^{2^k}=1+z^{2^k}+z^{2^{k+1}}\) consequently describes the *unclipped* linear
rule, but does not by itself describe iterates of `a`.

## 2. All finite boundary terms

Let `u` have length \(n\), polynomial \(U\), and let scanning it from `a` emit
the same-length prefix `p`, polynomial \(V\), without yet applying the finite
boundary rule. If its terminal mode is one of `a,b,c,d`, then

| Terminal mode | Exact polynomial identity |
|---|---|
| `a` | \(PV=U+1+z^n\) |
| `b` | \(PV=U+1+z^n+z^{n+1}\) |
| `c` | \(PV=U+1\) |
| `d` | \(PV=U+1+z^{n+1}\) |

**Proof.** The low \(n\) coefficients are the same inverse linear rule. The
omitted two coefficients of \(PV\) are
\((y_{n-2}+y_{n-1})z^n+y_{n-1}z^{n+1}\). Substitute the four output-memory
states above. The empty word is included: its mode is `a`, and
\(0=0+1+z^0\). ∎

For terminal copy mode, if \(Q\) cuts the emitted prefix at its first `11` as in
(1), the exact finite polynomial formula instead is
\(U=V+1+DQ\), with no high boundary terms.

The actual finite boundary rules append `0`, halt, append `1100`, and append
`00`, respectively. Thus the identity for a boundary-`a` repair output `r=p0`
is

\[
 \boxed{P R=U+1+z^n.}\tag{4}
\]

The boundary-`c` and boundary-`d` full outputs have polynomials \(R\) satisfying
\(PR=U+1+z^n+z^{n+3}\) and \(PR=U+1+z^{n+1}\), respectively.

## 3. Halting and repair are opposite ways to reach the same subshift

For every finite word `w`, append the infinite alternating tail `t`. Then

\[
 \boxed{a(w)\text{ is undefined}\iff a(wt)\in\mathcal S.}\tag{5}
\]

If the finite pass is defined, then

\[
 \boxed{a(w)t\in\mathcal S
 \iff\text{the finite pass ends in mode `a`}.}\tag{6}
\]

**Proof.** If scanning `w` has already reached `d` or copy, the output already
contains `11`. Otherwise examine the three active tail actions:

\[
 a(t)=001100t,\qquad b(t)=0t,\qquad c(t)=1100t.
\]

The `a` and `c` tails introduce `11`. The `b` tail does not: its emitted finite
prefix has no `11` and ends with memory `01`, so joining `0t` preserves that
property. Its finite boundary is exactly the halting boundary. This proves
(5). For the actual finite output, a boundary-`a` pass appends only `0`; its
prefix has memory `10`, so appending `0t` leaves no `11`. The other successful
boundary cases retain or introduce `11`. This proves (6). ∎

Thus following the total infinite-word dynamics until its next visit to
\(\mathcal S\) detects a finite halt. The actual finite system can instead make
an earlier repair, deliberately creating a visit to \(\mathcal S\). Controlling
this competition is an unproved global problem.

## 4. A repair is a single input defect, or an exactly quadratic output defect

Suppose the finite input `u` has length \(n\), ends in mode `a`, and its actual
output is `r=p0`. Then

\[
 \boxed{a^{-1}(rt)=ut+z^{n+1}.}\tag{7}
\]

Equivalently, `rt` is the image of `u11t`: the two inputs `ut` and `u11t` differ
in exactly their coefficient at position \(n+1\).

The output difference between the repaired and virtual maps is

\[
 \boxed{rt+a(ut)=\frac{z^{n+1}P^2}{1+z}.}\tag{8}
\]

**Proof.** The repaired output belongs to \(\mathcal S\), so (7) follows by
substituting (4) in \(a^{-1}(rt)=P(rt)+1\), or directly from
\(a(11t)=0t\). For (8), the common emitted prefix cancels. The actual and
virtual tails are `0t` and `001100t`, whose sum is
\(zP^2/(1+z)\); shift this by \(n\). ∎

All completions have denominator \(1+z^2\). If

\[
 W_w=(1+z^2)\operatorname{poly}(w)+z^{|w|},
 \qquad wt=\frac{W_w}{1+z^2},
\]

then (8) has the equivalent polynomial certificate

\[
 W_r+W_{\mathrm{virtual}}=z^{n+1}(1+z)P^2.
\]

In particular the repair defect has **exactly** \(P\)-adic valuation two,
since neither \(z\) nor \(1+z\) is divisible by \(P\). This finite polynomial
identity is checked without truncating an infinite series.

This invisibility modulo \(P^2\) does **not** propagate through an arbitrary
next sweep. A minimal useful illustration is

\[
 X=0t,\qquad X'=001100t.
\]

Their difference has valuation two, but
\(a(X)=t\), \(a(X')=110100t\), and the difference of their completion
numerators is \(z+z^2+z^5+z^6\), which is not divisible by \(P\). Moreover
the finite representative `0` halts immediately, whereas `001100` is the open
blank core. Therefore congruence modulo \(P^2\) cannot identify their full
dynamics or decide their safety.

## 5. The unclipped subshift has only two double visits

There is a sharp obstruction to applying the linear rule for long successive
rows:

\[
 \boxed{\mathcal S\cap a(\mathcal S)=\{0^\omega,t\}.}\tag{9}
\]

The two preimages are

\[
 a^{-1}(0^\omega)=10^\omega,
 \qquad a^{-1}(t)=0t.
\]

**Proof.** Suppose both \(Y\) and \(X=PY+1\) have no `11`.

If `Y` starts `01`, `X` starts `11`, impossible. If `Y` starts `00` and its
first `1` is at position \(j\ge2\), then its next bit is zero, so
\(x_j=x_{j+1}=1\), also impossible. Therefore this branch is exactly
\(Y=0^\omega\).

If `Y` starts `1`, it must start `10`. Until the first departure from
alternation it equals `t`. Such a departure must be a second consecutive zero,
at some even position \(2k+2\); then
\(x_{2k+1}=x_{2k+2}=1\). Hence no departure is allowed and \(Y=t\).
Both listed series directly satisfy the condition. ∎

The checker also gives an exact finite graph certificate. Store
\((y_{i-2},y_{i-1},x_{i-1})\), initially \((1,0,0)\). For each candidate bit
\(y_i\), compute \(x_i=y_i+y_{i-1}+y_{i-2}\), reject `11` in either series,
and update the memory. Removing states without an infinite continuation leaves
five states and exactly the two paths labelled \(0^\omega\) and \(t\).

Consequently **no three consecutive states of an `a` orbit belong to
\(\mathcal S\)**. A third visit would require one of the displayed preimages
to belong to \(\{0^\omega,t\}\), which neither does. On the class of eventually
alternating completions, only the double-visit pair \(0t\mapsto t\) remains.

There is also no global binary-tree conjugacy that replaces `a` by the
unclipped affine rule \(T(Y)=PY+1\). On level three, `a` has one 8-cycle:

`000 → 111 → 010 → 101 → 001 → 110 → 011 → 100 → 000`.

The map `T` has two 4-cycles:

`000 → 100 → 011 → 110 → 000`,

`010 → 111 → 001 → 101 → 010`.

Conjugate permutations have the same cycle lengths, so this finite discrepancy
is an exact obstruction, valid independently of any simulation horizon.

## 6. What these theorems reduce, and what is still missing

The inverse is now a linear CA plus a precisely located suffix defect. Actual
finite boundary repairs are single input-bit flips, and their exact output
defect is divisible by \(P^2\). Combined with the record-width theorem, the
blank problem is an exact interaction between clipping positions and record
events, rather than an unspecified finite-word boundary effect.

These are structural simplifications, not a proof of safety. An adequate next
theorem would control the clipping suffixes in (3) under arbitrarily many
sweeps, or prove an inductive family of record states that always repairs
before the virtual orbit enters \(\mathcal S\). Neither has been proved here.
The double-visit classification and the explicit congruence counterexample
show why neither a long block of bare Frobenius powers nor \(P^2\)-congruence
alone supplies the missing induction.
