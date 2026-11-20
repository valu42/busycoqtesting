# Wily Coyote #531/#532: structural research and exact certificates

**Status, 2026-11-21: the blank-tape pair remains undecided.** This directory
contains mathematical partial results, exact finite certificates for several
unbounded claims, and explicit counterexamples to proposed abstractions. It
does not contain a proof that either blank machine halts or runs forever.

The investigation starts from the existing Lean reduction, rather than a new
raw-machine simulation. Both machines have the same accelerated orbit. The
repository's previous `2^96`-sweep checkpoint is finite evidence; this work
does not claim a longer checkpoint or infer a decision from that checkpoint.

## Sources and conventions

* [Shared Lean reduction](https://github.com/google-deepmind/cryptids/blob/0661f4e9b011de8d92d30f44dc6c2a5532656f72/BusyBeaver/BB33/WilyCoyote.lean).
  The inspected file has Git blob SHA
  `74e3c6e69a24d079de9c839d9da7ab099da2b2b9`.
* [Formal BB(3,3) documentation](https://github.com/google-deepmind/cryptids/tree/main/BusyBeaver/BB33).
  Each machine's `isHalt_iff_acceleration` connects the common word dynamics to
  its raw blank-tape behavior.
* [Community Wily Coyote page](https://wiki.bbchallenge.org/wiki/Wily_Coyote),
  which still described the question as unsolved when inspected.
* [Existing repository analysis](../RANKINGS.md) and [implementation](../check_bb33.py),
  inspected at repository commit `03b4cbce1d6ae6ec116c95e016444d6014644e69`.

Bits are the Lean booleans: `0=false` represents tape symbol 2, and `1=true`
represents tape symbol 1. Words are read from left to right. Write `a,b,c,d`
for passes starting in `s0,s1,s2,s3`, respectively, and write `epsilon` for
the empty word. Composition is right to left. The complete sweep is
`F(w)=0a(w)`, with initial word `00`.

| Mode | Input `0x` | Input `1x` | Empty input |
|---|---|---|---|
| a | `1b(x)` | `0c(x)` | `0` |
| b | `1d(x)` | `0a(x)` | HALT |
| c | `0c(x)` | `1b(x)` | `1100` |
| d | `1x` | `0x` | `00` |

Every pass consumes a finite word and terminates. The question is whether an
unbounded sequence of passes remains defined. Equality of partial functions
below always includes equality of domains.

## What was proved

| Result | Scope | Effect on the remaining problem |
|---|---|---|
| Exact next-sweep halting language | All finite words | Verifies the proposed target language independently |
| Two-sweep reduction to repeated `a` from `001100` | Entire blank orbit, including failures | Removes the inert growing prefix without losing any regular invariant certificates |
| Complete decision of repeated `c`, and repeated `b` | All finite inputs | Resolves these auxiliary components, including exact halting clocks |
| A regular inductive family for repeated `a` | Infinitely many other seeds, including `000100` | Demonstrates an exact section-based proof; explicitly excludes `001100` |
| Impossibility of several invariant classes | Arbitrary window sizes and moduli in the stated classes | Shows that fixed end windows and several stronger summaries lose essential interior information |
| Sixteen arithmetic return identities | Infinite congruence families, with finite boundaries checked | Compresses whole excursions for those families; does not cover the blank continuation |
| Counterexamples to residue-only and width-erasing reasoning | Explicit finite certificates | Identifies the missing excursion and boundary obligations |

The arguments below are mathematical proofs with executable checks. The new
results have not been formalized or checked in Lean. No literature-wide
priority claim is made.

## 1. Exact halting language and reduced orbit

The proposed expression is correct:

\[
 B=(01\mid10^*11)^*(0\mid10^*1).
\]

A halting input never enters `d`, which always finishes safely. In the remaining
mode graph, the first-return loops from `a` back to `a` are exactly `01` and
`10^j11`; the final paths from `a` to the halting boundary mode `b` are `0`
and `10^j1`. This proves both directions of the expression. Its minimal DFA
has four states.

There is an exact simplification of the full orbit:

\[
 F((01)^k x)=(01)^kF(x),
 \qquad F^2(00x)=0100a(x)\quad(x\ne\epsilon).
\]

The first sweep from `00x` is always defined. The second is defined precisely
when `a(x)` is. The exceptional empty case is

\[
 F^2(00)=0100\,001100.
\]

Consequently, putting `v_0=001100` and `v_(n+1)=a(v_n)` when defined gives

\[
 F^{2n+2}(00)=(01)^{n+1}00v_n\qquad(n\ge0).
\]

This includes the failure correspondence: both original blank machines run
forever if and only if every iterate of `a` from `001100` exists. All reduced
words remain nonempty because a defined pass never decreases word length.

This reduction also preserves the existence of a regular invariant. If `I`
is an `F`-invariant containing `00`, then

\[
 J=\{x\ne\epsilon:\exists k\ge1,\ (01)^k00x\in I\}
\]

is a regular `a`-invariant containing `001100`. Conversely, a nonempty-word
regular `a`-invariant `J` containing that seed gives the regular `F`-invariant

\[
 \{00,01100\}\ \cup\ (01)^+00J\ \cup\ (01)^{\ge2}1d(J).
\]

The three invariant obligations are checked by the displayed two-sweep
identity and the initial two sweeps. See
[LANGUAGE_OBSTRUCTIONS.md](LANGUAGE_OBSTRUCTIONS.md) for the full proofs and
the explicit quotient-DFA construction.

## 2. Complete auxiliary decisions

The repeated-`c` nonhalting language is recognized by this three-state DFA:

| State | Read 0 | Read 1 | Accept? |
|---|---|---|---|
| C | C | D | yes |
| D | C | E | no |
| E | D | C | yes |

Start in C. This is a complete classification, including the assertion that
every rejected finite word eventually halts under repeated `c`. Starting
the same DFA in D instead classifies repeated `b`.

For a quantitative statement, let `H(w)` count successful `c` calls before
the first undefined call, with infinity for a nonhalting orbit. Then

\[
\begin{aligned}
 H(\epsilon)&=\infty,& H(1)&=0,& H(11)&=\infty,\\
 H(0x)&=H(x),& H(10x)&=2H(x)+1,\\
 H(110x)&=2H(1x),& H(111x)&=2H(x).
\end{aligned}
\]

Every rule shortens the word. Thus the theorem gives a terminating exact
decision and clock algorithm. Among length-`n` inputs that halt, for `n>=1`, the largest
clock is `2^floor((n-1)/2)-1`, attained by `(10)^k1` and by its zero-prefixed
even-length version. There is no simulation horizon in this theorem.

The main identity behind the proof is

\[
 c^2(10x)=10c(x).
\]

Its boundary cases are essential: `a(d(x))=c(x)` holds for every finite word,
but `c(d(x))=a(x)` holds only for nonempty words. An explicit recursively
defined infinite orbit proves the base `H(epsilon)=infinity`.

The safety half also has a particularly small certificate: just seven
reachable states in the product of the pass transducer, the input DFA, and
the output DFA. Checking their transitions and boundary outputs proves
closure for words of every length. The mathematical proof and exact clocks
are in [AUXILIARY_MODES.md](AUXILIARY_MODES.md); the certificate and decider
are in [c_safety.py](c_safety.py).

### An actual `a`-invariant, for different seeds

Let `L_c` be the accepted language above. Let `P` be the following set of
six-bit prefixes, in their cyclic order:

```
000100, 111100, 010000, 101110,
001000, 110000, 011100, 100111.
```

Reading one of these prefixes with `a` yields the next prefix, with tail
action either identity or `c`. The eight tail actions are respectively
`id,c,id,c,id,id,id,c`. Hence

\[
 a^8(000100x)=000100c^3(x)
\]

for every finite `x`, including exact definedness. Therefore `P L_c` is
an inductive safe family for `a`: it contains `000100`, excludes the
halting language, and is closed under every `a` call.

The minimal DFA constructed for this family has 19 states. The exact
invariant checker verifies all three obligations, and also verifies that
it does **not** accept the blank reduced seed `001100`. The executable
certificate is [regular_family.py](regular_family.py).

This is useful progress in proof technique, but it is not a blank-tape
decision or an invariant that can be substituted for the missing `J`.

## 3. Rigorous obstructions and explicit failures

The following impossibility statements concern the specified classes, not
all regular languages.

* No `F`-invariant containing `00` can, on sufficiently long words, depend
  only on a fixed-length prefix, a fixed-length suffix, and length modulo
  a fixed integer. This holds for every choice of the windows and modulus.
* No piecewise-testable language can be such an invariant. Here this means
  any finite Boolean combination of fixed scattered-subsequence tests.
* No counts-only language can be such an invariant, even with an arbitrary
  nonregular predicate on the two counts.
* For reduced `a`, even the full transition transformations of both the
  three-state auxiliary DFA and the four-state halting DFA, augmented with
  the exact zero and one counts, do not suffice.

The last obstruction has a short certificate. The blank core `001100` and
the word `001010` have the same counts and induce the same entire
transformations on both DFAs. Nevertheless,

\[
 001010\ \longmapsto\ 110010\ \longmapsto\ 011110
 \ \longmapsto\ \mathrm{HALT}.
\]

Any invariant based only on those features would have to accept the latter
word as well and therefore cannot be safe and inductive.

The arbitrary-window theorem uses a constructive controllability lemma:
freely chosen safe, length-preserving passes from `b,c,d` can change any
fixed-length suffix to any other suffix. In a bounded-end abstraction,
arbitrary middle words can present any incoming mode to that suffix. This
forces an accepted suffix class to contain an input ending in the halting
mode. The proof carefully uses the freedom provided by the abstraction;
it does not assert that the actual orbit can freely choose modes.

Two simpler candidates fail at the same shortest word:

\[
 000\xrightarrow{F}0111\in B.
\]

Thus neither ending in `00` nor being safe for one sweep is an inductive
condition. Full proofs, the exact DFA verifier, and the witnesses are in
[LANGUAGE_OBSTRUCTIONS.md](LANGUAGE_OBSTRUCTIONS.md), [dfa.py](dfa.py),
and [feature_analysis.py](feature_analysis.py).

## 4. Parameterized arithmetic returns, and their boundary

Define `rho(0)=01`, `rho(1)=10`, with the digits of integers written least
significant first. Put

\[
 R(n)=\rho(\operatorname{bin}(n))0,\qquad E(n)=0R(n),
 \qquad \operatorname{bin}(0)=\epsilon.
\]

The auxiliary pass is exactly a binary odometer:

\[
 b(R(n))=R(n+1)\quad(n\ge0).
\]

This follows from `b(0)=100`, `b(01x)=10x`, and `b(10x)=01b(x)`.
The blank reduced seed is `E(2)`. Symbolic prefix sections and the odometer
prove sixteen infinite return families, including:

| Condition | Proven return |
|---|---|
| n odd | `a^2(E(n))=E(n+3)` |
| n = 4 mod 16 | `a^6(E(n))=E(n+21)` |
| n = 8 mod 32 | `a^14(E(n))=E(n+69)` |
| n = 2 mod 64 | `a^62(E(n))=E(n+429)` |

These identities guarantee definedness of every intermediate pass and hold
for all parameters in their classes. They are return identities, not claims
that the displayed return is always the first one. Each certificate computes
on a fixed prefix, leaving an arbitrary nonempty tail; it reduces the tail
action exactly to a power of `b`. The short canonical representative of each
class is checked separately, so leading zero padding is not silently erased.

These rules take the blank core through `E(2) -> E(431) -> E(434)`. They do
not establish the next return. Two counterexamples limit the interpretation:

1. The residue candidate `E(24m+2)` is unsafe. `E(146)` halts on its 135th
   reduced pass, without an intermediate visit to `0(01|10)*0`. A congruence
   conserved by known completed returns does not ensure a safe excursion.
2. A symbolic rule with 19 low digits gives an exact 13,694-pass return for
   all `n=434 mod 2^19` with `n>=2^19`. That rule fails on the shorter canonical
   word `E(434)`. Finite boundary creation is mathematical information, not
   dispensable padding.

All sixteen families, their proofs, and both failed conjectures are documented
in [ARITHMETIC_RETURNS.md](ARITHMETIC_RETURNS.md), with exact executable
certificates in [arithmetic_certificates.py](arithmetic_certificates.py).

## 5. Recursive direction and the exact remaining implication

On infinite words, the passes become binary-tree automorphisms with sections

\[
 a=(b,c)\sigma,\quad b=(d,a)\sigma,\quad c=(c,b),
 \quad d=(\mathrm{id},\mathrm{id})\sigma,
\]

where `sigma` swaps the first bit. Return sections of powers of `a` can be
computed recursively, so a proof can analyze a whole finite-prefix cycle
without enumerating its time steps. The successful nonblank family above is
one example: the remaining section is `c^3`, whose finite-word safety has
now been completely decided.

Infinite-word identities must retain their finite-boundary exceptions. A
particularly useful way to see the exception is to append the infinite tail
`t=(10)^infinity`. Directly from the rules,

\[
 d(t)=00t,\quad c(t)=1100t,\quad b(t)=0t,\quad a(t)=001100t.
\]

The `c` and `d` identities agree with the finite boundary extensions. The
`a` identity does not: its finite extension is only `0`. The finite `b`
boundary halts even though its infinite-word image exists. Therefore an
infinite-tree automorphism argument alone does not decide the machine. It
must control these exceptional finite boundary events.

The most justified next target is an inductively closed recursive class of
the actual mixed return sections, together with their finite suffix states,
that reduces their safety obligations to the decided `b` and `c` components.
A theorem that every return section generated from `001100` stays in such
a class and has no halting boundary would settle both machines. Equally,
a reachable boundary-`b` certificate would settle them as halting. Neither
implication has been established here.

The obstacle is specific: the actual sections mix the generators, the known
regular features identify the seed with halting words, and the arithmetic
excursions need not reach the next proposed return section. Increasing a
simulation horizon or a fixed end window does not discharge that obligation.

## 6. Reproduction, certificate strength, and Lean connection

Run Python 3.10 or later, with assertions enabled, from this directory:

```sh
python verify.py
```

No third-party packages are required. The runner checks equality with the
repository's pre-existing `WILY` table; the exact auxiliary-language product
certificate; the 19-state nonblank invariant; all sixteen arbitrary-tail
return certificates; and the reported counterexamples. Exhaustive small-word
checks are kept separate from the finite certificates proving unbounded
closure. The runner prints the unresolved status explicitly.

`preimages.py` also provides exact transducer preimages and DFA minimization.
Its optional horizon exploration is not a proof of an inductive invariant,
and is not needed by the main verification run.

For a Lean port, the first useful lemmas are the finite-boundary identities
`a(d(x))=c(x)` and `c(d(x))=a(x)` under the nonempty hypothesis, followed by
the two-sweep identity and its iteration. These use the upstream `wilyPass`
definition directly. The auxiliary classifier can then be proved by the
length-decreasing clock rules, or its safety half by the seven product states.
A future blank-core invariant would combine with the normal form and the
existing `isHalt_iff_acceleration` for each of the two machines. No changes
to the established raw-machine reduction are needed.
