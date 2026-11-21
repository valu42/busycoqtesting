# Second-stage arithmetic research: exact limits and Fibonacci reset tests

The blank orbit is still undecided. This note records new universal obstruction
and nonhalting certificates, and separates them from promising but unsuccessful
attempts to use the first repair's Fibonacci value.

## 1. The full affine auxiliary-clock transformation still loses information

Define a finite integer-valued extension `K` of the auxiliary `c` halting clock
by the shortening rules

\[
\begin{aligned}
 K(\epsilon)&=-1,&K(1)&=0,&K(11)&=0,\\
 K(0x)&=K(x),&K(10x)&=2K(x)+1,\\
 K(110x)&=2K(1x),&K(111x)&=2K(x).
\end{aligned}
\]

On inputs whose `c` orbit halts, these are the same recurrence and terminal
value as the exact finite clock, so `K` equals that clock. On safe inputs it is
merely a finite extension; its value must not be mistaken for a finite halting
time.

Let

\[
 V(w)=(K(w),K(1w),K(11w)).
\]

Then, with `(A,B,C)=V(w)`, the rules give

\[
 V(0w)=T_0(A,B,C)=(A,2A+1,2B),
\]

\[
 V(1w)=T_1(A,B,C)=(B,C,2A),
\]

and `V(epsilon)=(-1,0,0)`. A word therefore induces an affine transformation
`T_w`, defined on an **arbitrary** triple, not only on this initial vector.
Each of its three rows has the form `2^e X_i + o`.

Keeping the entire transformation is much stronger than keeping the three
clock values. In particular, `T_u=T_v` implies

\[
 K(puq)=K(pvq)
\]

for every pair of finite contexts `p,q`. This follows from
`T_(puq)=T_p T_u T_q`.

There is also an exact statement for the actual halting clocks, including
infinity. The source coordinate of each affine row is precisely the state
reached in the auxiliary three-state DFA. Thus equality of the full affine
maps preserves both the safe/unsafe classification and the finite clock
value. It follows that

\[
 H_c(puq)=H_c(pvq)
\]

for all contexts, with infinity included. Repeated `b` clocks agree as well,
since `c(1x)=1b(x)` gives `H_b(x)=H_c(1x)`. Therefore keeping every such
contextual auxiliary halting-clock test still does not distinguish the
counterexample below.

### Exact obstruction theorem

There is no safe `a`-invariant containing `001100` whose membership depends
only on all of the following features together:

* the full affine transformation `T_w`;
* exact word length and exact zero and one counts;
* the last two bits;
* the full state transformation induced on the one-sweep halting DFA.

An arbitrary, possibly nonregular predicate on these features is allowed.

**Proof.** Seven actual `a` passes from the blank core give

\[
 u=a^7(001100)=1010010100001100.
\]

Put

\[
 v=1010000101011000.
\]

Both words have length 16, ten zeros, six ones, and suffix `00`. Both induce
constant-sink transformations on the four-state halting DFA. Their full affine
transformations coincide:

\[
 T_u(A,B,C)=T_v(A,B,C)
 =(64A+47,\ 128A+92,\ 64A+46).
\]

Nevertheless `v` halts on its twentieth `a` call. Its first nineteen calls are
successful; the last word is

\[
 0110111111110111,
\]

whose next call is undefined. Every word in this finite counterexample's trace
ends in `00` or `11`.

An invariant containing the blank core must contain `u`, must therefore contain
`v`, and by closure must contain the final halting word. This contradicts
safety. The exact equality, initial seven-step trace, and twenty-call halting
certificate are checked by `clock_obstruction.py`. ∎

This is not an impossibility theorem for all arithmetic invariants. Literal
prefix information, correlations between internal positions, or a recursive
representation can distinguish these words. It does dispose of the proposed
full weighted-clock transformation abstraction even with width, counts,
right-edge equality, and the one-sweep DFA added.

## 2. Repair states have a canonical Fibonacci coordinate

The record-width analysis establishes that a physical `a`-boundary repair
produces either `0` or a word in

\[
 (0^*10)^+0.
\]

Thus a nonzero repair word has no adjacent ones and ends in exactly two zeros.
Use Fibonacci weights `1,2,3,5,8,...`, least significant digit first. Removing
the final two zeros gives a canonical Zeckendorf representation, so every
nonzero repair word has a unique positive integer coordinate `N`. Denote its
code, including the two final zeros, by `R_F(N)`. Put `R_F(0)=0` separately.

This is an appropriate cross-section because the encoding has no arbitrary
width padding. It does not by itself say that every repair orbit returns to
another repair or survives.

The first actual repair, after 583 reduced passes from `001100`, is

\[
 r=10100101010100010010101000100=R_F(390625)=R_F(5^8).
\]

The equality is checked directly by `fibonacci_repairs.py`.

## 3. Powers of five: exact positive and negative results

The first repair's round Fibonacci value is an interesting lead, but several
natural extrapolations are false.

### Known halting powers

The exact finite certificates are

* `R_F(5^2)` halts on its seventh `a` call; its final word is `111010111`.
* `R_F(5^5)` halts on its 4,528th `a` call; its final word is
  `11101101111110001101011110101101111`.

The second computation has no intervening physical `a` repair. Its six earlier
boundary extensions are, in temporal order, `c,d,d,c,d,d`. Thus it cannot be
explained by an observed reset to the first power seed.

These two exponents, and the blank repair exponent 8, are all `2 mod 3`. That
suggested a possible halting renormalization. The next theorem falsifies a
uniform halting claim for that exponent class.

### Proven nonhalting powers in the same exponent class

Both `R_F(5^11)` and `R_F(5^14)` are nonhalting.

For `u=R_F(5^11)`, the exact prefix return identity is

\[
 a^{8192}(ux)=u\,c^3(x)\qquad(x\ne\epsilon).
\]

For `u=R_F(5^14)`, the corresponding identity has period `65536` and the same
section `c^3`. These identities include equivalence of definedness of every
intermediate call. They are obtained by following the finite prefix
permutation and reducing its temporal section word with identities valid on
nonempty tails.

The empty-tail initial condition must be checked separately. In each case the
first whole return cycle is defined and gives

\[
 a^P(u)=u\,110100.
\]

The suffix `110100` is nonempty and belongs to the completely decided safe
language for repeated `c`. Every subsequent `P`-call block is consequently
safe and again has a nonempty `c`-safe suffix. This proves nonhalting.

The certificate verifies the prefix cycle both recursively and by its explicit
finite permutation, and checks the empty-tail base cycle independently.
It does not apply a nonempty-tail identity blindly to the empty word.

More generally these section identities certify infinite families of tails,
not only the two displayed words. They do not apply to `R_F(5^8)`, whose return
section is genuinely mixed.

### An obstruction to the most literal power recurrence

`R_F(5^5)` has length 19 and belongs to a 2,048-cycle of the 19-bit prefix
permutation of `a`. The first 19 bits of `R_F(5^8)` are not in that cycle.
Since the prefix action is a permutation and finite boundary extensions never
alter its existing bits, for **every** `t` for which the iterate exists,

\[
 a^t(R_F(5^8))\ne R_F(5^5)x
\]

for every suffix `x`.

Thus a literal return of the `5^8` seed to the `5^5` seed as a left prefix is
impossible. A more indirect conjugacy or renormalization is not excluded.

## 4. The remaining mixed section

For the actual first repair prefix `r=R_F(5^8)`, the return period is 8,192.
Its temporal section word, using letters for the passes in order of
application, reduces to

```
cccacbbbbabbcabcbabc
```

It has twenty letters. The first finite tail output from the empty tail is
`00011010001100`; neither this nor subsequent elementary tails land in the
simple binary-odometer languages from the first investigation.

This mixed section is not conjugate to an odd power of `c o b` in the full
binary-tree automorphism group. Their cycle profiles agree through depth four
but disagree at depth five: the displayed section has three 8-cycles and two
4-cycles, while `c o b` has one 16-cycle and four 4-cycles. Odd powers preserve
those cycle lengths.

These observations locate a real obstruction to a simple recurrence; they do
not decide the mixed section's finite-boundary orbit. The exact missing theorem
is still a safe recursive family for this mixed section, or a rigorous
reduction of its complete finite-boundary dynamics to a decided component.
