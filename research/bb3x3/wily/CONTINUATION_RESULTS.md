# Wily Coyote: return sections, branch certificates, and failed refinements

This continuation does not decide the blank orbit. It proves an all-depth
statement about a regular family of prefix branches, strengthens an explicit
abstraction obstruction, excludes a natural proposed conjugacy by a finite
permutation certificate, and proves that the global self-similar group is
noncontracting. It also records the exact return systems that were investigated
and the specific failures of several candidate families.

Throughout, `a,b,c,d` denote the four partial passes. Mode words are written in
**temporal order**: `cb` means apply `c` first and then `b`. A separate copy
state is omitted from such words. Prefix actions ignore finite-boundary
extensions; when the tail is finally empty the genuine boundary rules are
applied.

## 1. Exact return map for the actual six-bit initial prefix

The length-six prefix `001100` has period 32 under the infinite binary-word
automorphism induced by `a`. Its raw sequence of noncopy sections is

```
ccbadcdbbcdaba
```

Using `da -> c`, `dc -> a`, and `dd -> identity` gives

```
R = ccbaadbbccba.
```

Consequently

\[
 a^{32}(001100x)=001100R(x).
\]

This equality includes the domain of the entire 32-pass composition. It is
valid for every nonempty tail. It is also valid for the empty tail here:
the first raw section is `c`, so either the input tail is already nonempty,
the first `c` call is undefined, or that first call creates a nonempty tail.
All subsequent uses of the reductions are therefore within their valid domain.
The empty-tail base is

\[
 R(\epsilon)=10000010101100.
\]

This gives an exact alternative formulation of the remaining initial-orbit
problem: iterate `R` from the empty word. It is useful only if its invariant or
return structure can be simplified further; the reformulation alone is not a
decision.

The two-bit prefix `10` is preserved by `R`. Its section is
`cbacbcba`. Therefore after the first `R` pass the constant `10` can also be
removed, leaving this eight-letter driver on initial tail `000010101100`.
No closed safe family for that system was established.

## 2. A finite suffix certificate for return sections at all depths

Let `N` reduce temporal words by

```
da -> c,   dc -> a,   dd -> empty.
```

The reductions strictly shorten words and represent exact identities of
infinite-word automorphisms. They also preserve the partial finite-word maps
on nonempty tails. They are not claimed to solve the entire group word problem.

For a prefix return word `r`, define its child return word `L_i(r)` at bit
`i` as follows. Take the section of `r` at `i`; if `r` flips the root bit,
append its section at `1-i` as well. Reduce the result by `N`. In the latter
case the prefix period doubles. This is the standard direct lifting of a
cycle in a binary prefix permutation and follows immediately by following the
first bit through one or two returns.

Consider the following five predicates on reduced nonempty temporal words:

| Class | Required suffix |
|---|---|
| A | `ba` |
| B | `ab` or `cb` |
| C | `ad` or `cd` |
| D | `a` or `c` |
| E | `b` |

They satisfy these **universal** lifting implications:

| Current class | Child bit 0 | Child bit 1 |
|---|---|---|
| A | D | B |
| B | A | C |
| C | E | D |
| D | D | E |
| E | D | no assertion |

### Proof of the table

A completed child return finishes with its selected bit unchanged. If the last
suffix `s` has root permutation parity `chi(s)`, its input bit on the last
copy of the parent return must therefore be `i xor chi(s)`. This determines
the section of that suffix without knowing anything about the earlier word.
For example, a parent ending in `ba` has root-even final suffix. At child bit
1 its suffix section is `ab`. The preceding section may end in `d`, changing
this to `cb`; otherwise it remains `ab`. Either result is in class B.
Conversely, at child bit 0 the suffix sections of both `ab` and `cb` are
`ba`. Its leading `b` cannot be cancelled by the chosen reductions, so the
result is in A.

The other rows follow in exactly the same way. The complete finite check must
consider both possible suffixes in each class, both child bits, and an empty
preceding section or each of its four possible last letters. This is 75
cases for the asserted transitions. `section_suffix_certificate.py` checks
all of them. This finite table is an exhaustive proof obligation for arbitrary
preceding words: only their final letter can interact with the displayed
suffix, and the one problematic cancellation from E at bit 1 is deliberately
left without an assertion.

The initial return word `R` from Section 1 ends in `ba`, so it is in A.
Induction on prefix length now gives a finite certificate of a nonempty
return word for every extension accepted by this five-state partial automaton.

In particular, for every `k>=0`, extensions `(10)^k` end in A and
`(10)^k1` end in B. For every `k>=0`, `(10)^k11` ends in C. After this single
`11` insertion, every subsequent complete `10` pair ends in D; the
intermediate bits stay in D or E. Hence every finite prefix of each ray

\[
 001100(10)^\omega
 \quad\hbox{or}\quad
 001100(10)^k11(10)^\omega \quad(k\ge0)
\]

has a nonempty raw return word once its length is at least six.

### Dynamical consequence and limit

**Theorem.** For every such finite prefix `p`, repeated finite `a` passes
must either halt or increase word length within one period of its prefix
permutation. In particular, its orbit cannot remain forever in a fixed-length
cycle.

Indeed, a nonempty raw return word contains an occurrence of `a,b,c`, or `d`
at the right boundary. Modes `a,c,d` extend the word, while mode `b` halts.
A length-preserving pass has only the copy mode at its boundary. Thus an
entire fixed-length prefix period would require the raw return word to be
empty, contradicting the certificate.

This theorem does **not** exclude halting. It also does not prove that all
future repaired completions of the blank orbit remain in this branch language.
It is a parameterized no-fixed-length-cycle theorem for the stated family,
not a nonhalting certificate.

## 3. Equal final bits do not repair the earlier whole-word summary

Let `tau_C(w)` and `tau_B(w)` be the entire transformations induced by `w`
on the three-state auxiliary-safety DFA and the four-state next-sweep-halting
DFA, respectively, as defined in the first automata note.

The reduced initial word `001100` and the word `100100` have:

* the same four zeros and two ones;
* identical `tau_C` transformations, namely constant C;
* identical `tau_B` transformations, namely constant safe sink;
* the same final two bits `00`.

But the latter has the exact halting trace

```
100100 -> 000111 -> 111111 -> 0100100 -> 1011000
       -> 0010111 -> 1100111 -> 0111111 -> HALT.
```

Every word displayed before halting ends in `00` or `11`.

**Corollary.** No safe `a`-invariant containing `001100` can have membership
determined solely by the two full DFA transformations, exact counts, and the
final two bits. Even the additional requirement that all subsequent defined
iterates have equal final bits does not separate this explicit counterexample
from the intended safety property.

The last sentence is a limitation of that proposed property, not an assertion
that the entire blank orbit has been proved to have equal final bits.

There is a similar obstruction directly in the 32-step tail system. The first
tail `10000010101100` has the same exact counts and full DFA transformations
as `10011010001000`, and both start `10` and end `00`. The latter halts in
component 11 of `R`. Thus moving this same summary to the actual prefix
return map does not make it inductive.

## 4. Fibonacci repair coordinates: verified value and a conjugacy obstruction

For an integer `z>0`, let `R_F(z)` be its least-significant-digit-first
Zeckendorf representation with weights `1,2,3,5,...`, followed by two zeros.
The observed first blank-orbit repair word is exactly

\[
 r=10100101010100010010101000100=R_F(390625)=R_F(5^8).
\]

This arithmetic equality is independently checked by `fibonacci_records.py`.
It does not establish a power-of-five recurrence. For example

\[
 R_F(25)=101000100
\]

halts on its seventh `a` call, after six successful calls. Its last word is
`111010111`. It is a genuine repair destination:

\[
 a(01011011)=101000100.
\]

Both the source and destination have their first six bits in the same
32-cycle as the blank reduced prefix `001100`. Thus even restricting the
no-`11` repair language to that prefix cycle cannot establish safety.

The larger example has the exact factorization

\[
 R_F(3125)=0101010000\,R_F(25).
\]

Let `p=0101010000`. It has prefix period 128, with reduced temporal return
section

```
cbadbccdbbaacccbbac.
```

One might hope this section were a power of `a`, or conjugate to a power of
`a,b`, or `c`, giving a uniform deflation to the smaller example. The natural
unrestricted version of that proposal is false.

**Proposition.** The return automorphism at `p` is not conjugate by any
binary-tree automorphism to any power of `a`, `b`, or `c`.

**Finite proof.** On seven-bit tails its permutation has cycle type

\[
 4^4\,8^6\,16^4.
\]

On that level, `a,b,c` have respective orders `32,16,8`. Exhausting their
finitely many powers gives no permutation with the displayed cycle type.
Any binary-tree conjugacy would restrict to a conjugacy on that level, which
must preserve cycle type. This contradiction excludes every integer power,
not merely a bounded list of exponents. `continuation_certificates.py`
reconstructs these permutations and checks the assertion independently.

A conjugacy on a specially restricted tail family is not excluded by this
argument. No such restricted deflation was found.

## 5. The return section at the actual first repair

At the full 29-bit prefix `r=R_F(5^8)`, the prefix period is 8192. Its raw
noncopy section stream is

```
cccadabbbbabbdadcbdababc
```

and its reduced temporal word is

```
H = cccacbbbbabbcabcbabc.
```

The empty-tail base is

\[
 H(\epsilon)=00011010001100.
\]

The first raw section is `c`, so the same nonempty-tail justification as in
Section 1 makes the reduced identity valid also for the empty initial tail.
A proper safe invariant for `H` containing the empty word would therefore
settle the blank orbit after its certified first repair.

The three auxiliary residual safety classes do not individually work. Exact
Moore-machine preimages give these counterexamples:

* The full `c`-safe class contains `01101`, on which `H` halts.
* Restricting the auxiliary DFA's final state to C still contains `10100`,
  on which `H` halts.
* Adding even length to the latter predicate still contains `010100`, on
  which `H` halts.

These are failures of particular proposed abstractions, not an impossibility
result for regular `H`-invariants.

## 6. The global self-similar group is noncontracting

This section concerns the total actions on **infinite** binary words, not the
partial finite-word boundary rules. Let

\[
 G=\langle a,b,c,d\rangle\le\operatorname{Aut}(\{0,1\}^*).
\]

Its generators are closed under taking sections, so this is a self-similar
group. A self-similar group is contracting if there is a single finite set
\(\mathcal N\subset G\) such that, for each \(g\in G\), all sufficiently
deep sections of \(g\) belong to \(\mathcal N\). The depth may depend on
\(g\), but the finite set must work for every group element.

**Theorem.** The element `c` has infinite order, and `G` is noncontracting.

**Proof.** Write \(g=(g_0,g_1)\pi\) for the root permutation and the two
sections of a binary-tree automorphism. Directly from the transducer,

\[
 c=(c,b),\qquad b=(d,a)\sigma,\qquad d^2=1,
 \qquad a=c\circ d.
\]

Here \(\sigma\) interchanges the two root edges, and \(\circ\) uses the
usual functional convention rather than temporal word order. Squaring `b`
therefore gives

\[
 b^2=(a\circ d,d\circ a)=(c,d\circ c\circ d).
\]

Suppose `c` had finite order \(m\). Since `c` fixes the root and has section
`b`, the identity \(c^m=1\) implies \(b^m=1\). Thus `b` has some finite
order \(k\) dividing \(m\). Its root permutation is a transposition, so
\(k\) is even. But the two sections of \(b^2\) are conjugate to `c`, hence
\(b^2\) has order exactly \(m\). On the other hand its order is
\(k/2\), giving \(k=2m\), a contradiction to \(k\mid m\). This proves
that `c` has infinite order.

Because `c` fixes the root and its section at 0 is itself, for every integer
\(j\ge0\) and every depth \(n\ge1\),

\[
 (c^j)|_{0^n}=c^j.
\]

Consequently any contracting set \(\mathcal N\) would have to contain every
power \(c^j\): apply its defining property to that fixed group element and
then take a sufficiently deep all-zero section. These powers are all
distinct, contradicting finiteness. ∎

This excludes a **global finite contracting nucleus** as a general solution
method for this particular automaton group. It does not exclude a finite
description of return sections along the actual blank-generated branch, a
regular invariant for `a` or `H`, a contracting subgroup, or a useful
noncontracting recursive representation. No conclusion about halting follows
from noncontraction alone.

`group_recursion_certificate()` in `continuation_certificates.py` checks the
exact symbolic root and section identities used in the proof. The infinite
order and noncontraction arguments then require no finite-depth assumption.

## 7. Executable tools and unsuccessful synthesis

`return_abstraction.py` constructs a Moore machine that classifies every
finite input by the exact `R` output's chosen DFA feature, or by an undefined
intermediate pass. It composes exact transducer preimages and minimizes the
result. For the 87-state combined transition-monoid feature, the `R`
classifier has 517 states. These are exact finite automata over all words,
not length-bounded simulation data.

`learn_return.py` performs a limited state-merging experiment with this exact
checker. Candidate languages were required to contain the initial tail and
were tested for all-word safety and closure. Proven fixed-prefix information,
the observed equal-final-bits filter, and implication counterexamples were
incorporated. No invariant was found. This failed synthesis run provides no
proof that a regular invariant does not exist; no larger state limit was
presented as mathematical progress.

The main reproducible checks are

```
python section_suffix_certificate.py
python continuation_certificates.py
```

These commands run from the integrated research directory. All imports are
ordinary local module imports; the required `certificates.py`, `dfa.py`,
`feature_analysis.py`, and `return_sections.py` come from the first
investigation and belong in the same directory. No scratch-directory paths or
third-party libraries are required.

The strongest unresolved opportunity from this part is a structurally closed
family for the actual repair-aligned driver `H`, or a proved induced map on
the no-`11` repair cross-section that retains the physical record condition.
The auxiliary classes, numeric coincidence `5^8`, and simple homogeneous
section conjectures do not supply that missing implication.
