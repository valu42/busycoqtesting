# Wily Coyote: record boundaries and a clipped linear inverse

**The blank-tape behavior of #531/#532 remains undecided.** This continuation
adds general structural theorems, constructive obstructions, and two further
nonblank nonhalting certificates. It does not add a survival checkpoint.

The most useful new description is exact: the finite system follows a total
infinite-word map with a running length record, interrupted by one specified
boundary repair. The inverse of that total map is a linear cellular automaton
until the first `11`, with an explicit correction after that position. Halting
and repair can both be characterized using the same no-`11` subshift.

## 1. Starting point and proof status

Write `a,b,c,d` for the four partial passes. The earlier normal form proves
that the two blank machines run forever if and only if every iterate

\[
 v_0=001100,\qquad v_{n+1}=a(v_n)
\]

exists. The already verified next-pass halting language remains

\[
 B=(01\mid10^*11)^*(0\mid10^*1).
\]

The present results use that reduction and the completely decided auxiliary
`c`-language from [AUXILIARY_MODES.md](AUXILIARY_MODES.md).

| New result | Quantified scope | What it changes |
|---|---|---|
| Canonical padding and record theorem | Every finite word and arbitrary padding | Separates the virtual dynamics from the exact finite-boundary exception |
| Clipped linear inverse and boundary identities | Every infinite output and every finite boundary | Identifies a linear part and the precise nonlinear suffix correction |
| Fixed polynomial-quotient obstruction | Every truncation depth and length modulus | Rules out an entire proposed arithmetic invariant class |
| Full contextual-clock obstruction | Arbitrary prefix/suffix contexts and arbitrary predicates on the stated features | Shows that even exact auxiliary clock information loses needed order information |
| Nonhalting of two Fibonacci power seeds | Entire orbits, with arbitrary-tail return identities | Falsifies a tempting uniform halting extrapolation to the blank reset |
| Return-section suffix certificate | A regular family of branches at all depths | Excludes fixed-length cycles on those branches, while allowing either growth or halting |
| Noncontraction of the full automaton group | The full automaton group | Excludes a global finite contracting nucleus, without excluding a branch-specific invariant |

All universal statements have mathematical proofs in the linked notes.
Executable checks validate implementations and discharge the stated finite
certificate obligations. These results have not been formalized in Lean.

## 2. The finite boundary becomes a running-record condition

Put `t=(10)^omega`. Every finite word has a unique form

\[
 w=v(10)^k,\qquad k\ge0,
\]

where `v` does not end in `10`. Its completed infinite word `vt` depends only
on `v`. In ordinary 2-adic integer coordinates it is

\[
 vt=\frac{N(v)}3,\qquad
 N(v)=3\sum_i v_i2^i-2^{|v|}.
\]

Let `A(v)` be the canonical finite representative of the infinite action
`a(vt)`. Unlike the original finite pass, this map is total. Directly from
the transducer,

\[
 a(t)=001100t,\quad b(t)=0t,\quad
 c(t)=1100t,\quad d(t)=00t.
\]

Suppose scanning `v` emits `p` and ends in mode `q`. Let `L=|w|` be the
physical finite length. The following is an exact theorem:

* If `q=b`, the finite pass halts, for every amount of padding.
* If `q=a` and `L=|v|`, the next actual word is `p0`, of length `L+1`.
  Call this event a **repair**.
* Otherwise the next canonical word is `A(v)` and
  \[
  L'=\max(L,|A(v)|).
  \]

Thus between repairs, the padding is determined by the virtual orbit and its
running maximum length. The record remains an unbounded state variable; no
width information has been discarded.

There is also a sharp bound on each virtual canonical-length change:

| Terminal mode | Change in canonical length |
|---|---:|
| a | +6 |
| c | +4 |
| d | +2 |
| Copy | 0 or -2 |
| b | -1 |

In particular, the halting singularity is exactly a one-bit downward change
of canonical length. A successful repair replaces a virtual six-bit increase
with an actual one-bit increase.

The full padding formulas and proofs, including empty inputs, are in
[TAIL_RENORMALIZATION.md](TAIL_RENORMALIZATION.md). This theorem genuinely
isolates the exceptional boundary behavior. It does not prove that a future
singularity is avoided.

## 3. A linear inverse, stopped at the first `11`

For this section use formal bit series over the field `F_2`, where addition
is XOR. This is different from ordinary 2-adic integer arithmetic. Set

\[
 P=1+z+z^2,\qquad D=z+z^2,\qquad
 t=\frac1{1+z^2}.
\]

Let `Y` be an infinite output. If its first `11` occurs at positions `j,j+1`,
let `Q(Y)` retain the coefficients only through position `j`, including the
first of these two ones. If there is no `11`, set `Q(Y)=Y`. Then the exact
inverse of the infinite-word action is

\[
 \boxed{\widehat a^{-1}(Y)=Y+1+D Q(Y).}
\]

The proof is a small state-memory identity. Before copying, the modes are the
last two emitted bits:

\[
 a\leftrightarrow10,\quad b\leftrightarrow01,\quad
 c\leftrightarrow00,\quad d\leftrightarrow11.
\]

With initial virtual history `10`, the inverse bit rule is

\[
 x_i=y_i\oplus y_{i-1}\oplus y_{i-2}.
\]

It applies through the first `11`; the next bit is flipped and all remaining
bits are copied. This proves the formula for arbitrary words, rather than
only for a sampled orbit.

Let `S` be the infinite no-`11` subshift. On it,

\[
 \widehat a^{-1}(Y)=PY+1.
\]

More importantly, its relation to the finite problem is exact:

\[
 \boxed{a(w)\text{ halts}\iff\widehat a(wt)\in S.}
\]

For a successful finite pass, `a(w)t` belongs to `S` exactly at a repair.
A natural virtual visit to `S` therefore means halting; a finite repair
creates an earlier visit to `S` instead.

The correction cannot be ignored. Under `Z(X)=1+DX`,

\[
 Z(\widehat a^{-1}Y)
 =PZ(Y)+D^2\bigl(Y+Q(Y)\bigr).
\]

The second term begins at the position determined by the first `11`. A
renormalization must control these positions and suffixes.

### Exact boundary defects

If a length-`n` word `u` reaches boundary mode `a` and repairs to `r`, then

\[
 P\operatorname{poly}(r)=\operatorname{poly}(u)+1+z^n,
\]

\[
 \widehat a^{-1}(rt)=ut+z^{n+1},
 \qquad
 rt+\widehat a(ut)=\frac{z^{n+1}P^2}{1+z}.
\]

A repair is one flipped input bit, and its output defect has exactly
`P`-adic valuation two. This congruence is not propagated by the next sweep:
`0t` and `001100t` agree modulo `P^2`, but their virtual images `t` and
`110100t` differ even modulo `P`.

### Why the bare linear rule does not decide the problem

There is a sharp classification:

\[
 S\cap\widehat a(S)=\{0^\omega,t\}.
\]

Thus no three consecutive states of an orbit belong to `S`. An exact
five-state productive graph certifies the intersection. Also, on three-bit
prefixes, `a` has one 8-cycle while the unclipped affine rule has two 4-cycles,
so they cannot be globally conjugate as binary-tree automorphisms.

These facts prevent replacing the actual dynamics with repeated powers of
`P`. Proofs and all boundary formulas are in [INVERSE_CA.md](INVERSE_CA.md).

## 4. Two stronger invariant obstructions

### Every fixed `P`-adic depth still admits a halting word

For a finite word `w` of length `n`, define its completed bit series

\[
 X_w=\operatorname{poly}(w)+\frac{z^n}{1+z^2}.
\]

The reachable word

\[
 u=a^{90}(001100)=01101011100010010111
\]

has the following property. **For every pair of integers `k,M>=1`**, there is
an immediately halting word `v` such that

\[
 X_v\equiv X_u\pmod{P^k},\qquad
 |v|\equiv20\pmod M,
\]

and `v` has the same final two bits `11`.

Consequently no safe invariant containing the blank core can depend only on
any fixed polynomial truncation, final two bits, and fixed length modulus.
The proof is constructive: monomials can be moved arbitrarily far apart by
multiples of the finite order of `z` in a quotient, preserving the residue
while enforcing no adjacent ones. The linear inverse turns the resulting
no-`11` output into a halting input with the required boundary phase.

This rules out every fixed depth at once. It does not exclude recursive
coefficient information or unbounded valuations. See
[P_ADIC_OBSTRUCTION.md](P_ADIC_OBSTRUCTION.md).

### Even all contextual auxiliary clocks are insufficient

The reachable word and counterexample

```
u = a^7(001100) = 1010010100001100
v               = 1010000101011000
```

have identical length, exact counts, final two bits, full halting-DFA
transformations, and the entire affine action on the three auxiliary clock
coordinates. That affine action is

\[
 (A,B,C)\longmapsto(64A+47,128A+92,64A+46).
\]

Nevertheless `v` halts on its twentieth `a` call. Equality of the full affine
maps implies equality of the auxiliary `b` and `c` halting clocks in every
finite prefix/suffix context, including infinite clock values. Therefore
those contextual clocks, even combined with the other features, cannot
support a safe invariant containing the blank orbit.

The precise scope and trace are in
[SECOND_STAGE_ARITHMETIC.md](SECOND_STAGE_ARITHMETIC.md).

## 5. The actual reset and the failed power-of-five lead

All possible repair destinations form the exact language

\[
 (0^*10)^*0
 =\{0\}\cup\{w:\text{no `11`, and }w\text{ ends in `100`}\}.
\]

Apart from `0`, each is a unique least-significant-first Zeckendorf expansion,
with weights `1,2,3,5,...`, followed by two zeros. Denote this code by `R_F(N)`.

The first actual blank-core repair is the finite base fact

\[
 a^{583}(001100)=r
 =10100101010100010010101000100
 =R_F(390625)=R_F(5^8).
\]

The arithmetic pattern was tested in both directions, with decisive results:

| Reset seed | Rigorous outcome |
|---|---|
| `R_F(5)` | Nonhalting, by the earlier `c^3` return family |
| `R_F(5^2)` | Halts on call 7 |
| `R_F(5^5)` | Halts on call 4,528 |
| `R_F(5^8)` | Unresolved; this is the actual first blank reset |
| `R_F(5^11)` | Nonhalting |
| `R_F(5^14)` | Nonhalting |

The last two are unbounded proofs. For their respective prefixes `u`,

\[
 a^{8192}(ux)=u\,c^3(x),
 \qquad
 a^{65536}(ux)=u\,c^3(x)
 \quad(x\ne\epsilon).
\]

Each empty-tail base cycle is separately verified and produces tail `110100`,
which is nonempty and `c`-safe. The identities then prove safety of every
subsequent block. Thus the two early halting exponents cannot be extrapolated
to every exponent `2 mod 3`.

A literal recurrence from the `5^8` seed to a word beginning with the `5^5`
seed is also impossible: their relevant 19-bit prefix orbits are disjoint.
The natural factorization of the `5^5` seed through the `5^2` seed has a
return section not even conjugate to any power of `a,b,c`, by an exact
seven-bit permutation certificate.

The actual repair prefix has return period 8192 and chronological tail driver

```
H = cccacbbbbabbcabcbabc.
```

For every finite tail `x`, including the empty word, the exact identity of
partial maps (with the same domain) gives

\[
 a^{8192}(rx)=rH(x),\qquad
 H(\epsilon)=00011010001100.
\]

A safe invariant for `H` containing the empty word would solve the blank
problem. Merely replacing `a` by this longer driver does not reduce the
mathematical difficulty; no such invariant has been established.

See [SECOND_STAGE_ARITHMETIC.md](SECOND_STAGE_ARITHMETIC.md) and
[CONTINUATION_RESULTS.md](CONTINUATION_RESULTS.md) for the proofs and further
all-depth return-section results.

## 6. The precise next theorem

The strongest structural route now has a concrete target. Find a recursively
described family `C` of repair words containing `R_F(5^8)`, and prove for every
member that its record-controlled virtual excursion either:

1. continues forever without a halting singularity; or
2. reaches a record-`a` repair before any halting singularity, with the next
   repaired word again in `C`.

The first 583 passes are already a verified finite entry certificate. The
clipped inverse identifies exactly which suffix corrections such a theorem
must control. The fixed-quotient and contextual-clock obstructions identify
information that cannot be discarded.

No family satisfying this obligation is currently proved. A proof forcing a
natural visit to `S` before the next repair would instead establish halting.
The nonlinear stopping positions and their interaction with the length record
remain the unresolved implication, not a missing finite simulation horizon.

## Reproduction and formalization boundary

From this directory, run:

```sh
python verify.py
```

The runner checks the original and continuation certificates using only the
Python standard library. The archived output is [VERIFICATION.txt](VERIFICATION.txt).
The continuation-only runner is `python verify_continuation.py`.

The finite certificates include symbolic section identities, complete finite
products, finite graph languages, and permutation obstructions. The exhaustive
short-word checks separately validate formulas and boundary implementations.
They are not used as substitutes for the general proofs.

The Lean bridge remains the existing `wilyPass` reduction and the two machine
halting equivalences. A formal port can add the padding lemmas by induction
on the padding exponent, the inverse-memory lemma by induction on the emitted
prefix, and the finite product certificates as independently checked tables.
No new raw Turing-machine simulation is required. The present contribution is
mathematical documentation and executable certificates, not a Lean proof of
the blank decision.
