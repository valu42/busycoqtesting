# Wily Coyote: exact language and finite-memory obstructions

These results concern the transducer in `BusyBeaver/BB33/WilyCoyote.lean`.
Write `P_i(w)` for `wilyPass s_i w`, interpreting `false` as 0 and `true` as 1,
and write `F(w)=0P_0(w)` when defined. The initial word is `00`.
No result below decides this initial orbit.

## 1. The exact halting language

**Theorem 1.** A sweep halts exactly on

\[
 B=(01\mid10^*11)^*(0\mid10^*1).
\]

**Proof.** Ignore output bits and follow the input-mode graph. Once state `s3`
is reached, no continuation can halt: either the boundary supplies `00`, or
one bit is flipped and the remainder copied. Thus a halting input stays in
`{s0,s1,s2}` and ends in `s1`. The first-return paths from `s0` to `s0` without
an intermediate visit to `s0` are exactly `01` and `10^j11`, for `j>=0`.
After the last visit to `s0`, the paths ending in `s1` are exactly `0` and
`10^j1`. Concatenating these paths gives the expression; every such path
ends in `s1` and hence halts. This proves both inclusions. ∎

The minimal deterministic recognizer has four states. Its initial state is
0, its only accepting state is 1, and its table is

| State | Read 0 | Read 1 |
|---|---:|---:|
| 0 | 1 | 2 |
| 1 | 3 | 0 |
| 2 | 2 | 1 |
| 3 | 3 | 3 |

Here state 3 combines `s3` and the final copy mode. It is minimal: state 1
is separated from every other state by the empty suffix; suffix `0`
separates 0 from both 2 and 3, and suffix `1` separates 2 from 3.

## 2. Removing the inert alternating prefix

**Theorem 2.** For every `k>=0` and every word `x`,

\[
 F((01)^k x)=(01)^k F(x),
\]

including equivalence of definedness. For every nonempty `x`,

\[
 F^2(00x)=0100P_0(x),
\]

again including equivalence of definedness; the first sweep is always
defined. The exceptional empty case is `F^2(00)=0100·001100`.

**Proof.** `P_0(01x)=10P_0(x)`, so `0(10)^k=(01)^k0` proves the first identity.
If `x=bu`, then `F(00bu)=011(!b)u`. Removing its initial inert `01` in the
second sweep gives

\[
 F^2(00bu)=01F(1(!b)u)=0100P_0(bu).
\]

For `b=0`, both sides continue as `01001P_1(u)`; for `b=1`, both continue
as `01000P_2(u)`. The empty case follows directly from the boundary rules. ∎

Consequently, set `v_1=001100` and, when defined, `v_{n+1}=P_0(v_n)`. Then

\[
 F^{2n}(00)=(01)^n00v_n \qquad(n\ge1).
\]

Every odd sweep from these words is safe; the following even sweep exists
if and only if the corresponding `P_0(v_n)` exists. Also `|P_0(v)|>=|v|`
whenever defined, so these reduced words never become empty. This is an
exact reduction of the entire orbit, not a finite simulation observation.
It removes a deterministic growing prefix but does **not** by itself
provide an invariant of the remaining words.

## 3. Controlled passes can change any suffix

This lemma concerns **a freely chosen sequence of modes** `s1,s2,s3`.
It does not claim that the blank orbit can freely choose those modes.

**Theorem 3 (safe fixed-length controllability).** For every `l>=1` and
any words `u,v` of length `l`, there is a finite sequence of passes from
`{P_1,P_2,P_3}` taking `u` to `v`, each defined and preserving length.

**Proof.** It suffices to construct, for each position `j` (numbered from
0), a sequence that flips exactly position `j` and preserves every other
position. Induct on `j`.

* For `j=0`, use `P_3(bx)=(!b)x`.
* For `j=1`, use the previously constructed flips to make position 0 equal
  to 0. Then `P_1(0bx)=1(!b)x`. Restore position 0 using a lower-position
  flip. Only position 1 remains changed.
* For `j>=2`, use the previously constructed flips to arrange the first
  `j` bits as `0^(j-2)10`. Then

  \[
  P_2(0^{j-2}10bx)=0^{j-2}11(!b)x.
  \]

  Restore the first `j` bits to their original values using the lower
  flips. Only position `j` remains changed.

Each displayed pass reaches the copy mode before the boundary, so it is
safe and preserves length. Lower flips have the same property by
induction. Composing the required individual flips changes `u` to `v`. ∎

`certificates.py` implements this induction constructively, producing the
actual sequence of modes. Its correctness is not based on a search bound.

## 4. No bounded-end/modular-length inductive invariant

The following is a restriction on a substantial class of simple regular
abstractions. It is **not** an impossibility theorem for all regular
languages.

**Definition.** A language has a *bounded-end/modular-length description*
if there exist finite integers `k,l,N>=0`, `M>=1`, and a Boolean table `A`
such that, for every sufficiently long word `w` (say `|w|>=N`),

\[
 w\in I\iff A(\operatorname{prefix}_k(w),
                 \operatorname{suffix}_l(w),|w|\bmod M)=1.
\]

The behavior on shorter words is unrestricted. Prefix-only, suffix-only,
length-modulus, and arbitrary Boolean combinations of these tests are
special cases. We may enlarge `l` to at least 1 and enlarge `N` as needed.

**Theorem 4.** There is no language with such a description satisfying
all three conditions

1. `00` belongs to `I`;
2. every member of `I` has a defined sweep;
3. `F(I)` is contained in `I`.

**Proof.** Suppose such an invariant exists. Its closure and safety imply
that every blank-orbit iterate exists. By Theorem 2, arbitrarily late
iterates have an arbitrarily long initial block `(01)^n`. Let `alpha` be
the length-`k` prefix of the infinite alternating word. For residue `r`,
let

\[
 S_r=\{u\in\{0,1\}^l:A(\alpha,u,r)=1\}.
\]

At least one `S_r` is nonempty, by taking a sufficiently long blank-orbit
word with prefix `alpha`.

We need the freedom to choose the input mode at the start of `u`. Every
streaming mode, including the identity/copy mode, can be reached from
`s0` by a word of any prescribed sufficiently large length. Indeed, use
one of the base words

| Desired mode | Base word |
|---|---|
| `s0` | empty |
| `s1` | `0` |
| `s2` | `1` |
| `s3` | `00` |
| copy | `000` |

and pad on the left with the `s0` loops `01` (length 2) and `111` (length
3). Every integer at least 2 is a nonnegative combination of 2 and 3.
No boundary action is applied while this middle word is being read.

Fix `u in S_r`. Choose an input `(01)^m p u` with `2m>=k`, total length
at least `N`, total length congruent to `r` modulo `M`, and `p` ending in
the copy mode. Such a `p` exists by the preceding padding argument.
This input belongs to `I`. Its image preserves both its initial
`(01)^m` and suffix `u`, and its length increases by exactly 1. Hence
`u in S_(r+1)`. Thus

\[
 S_0\subseteq S_1\subseteq\cdots\subseteq S_{M-1}\subseteq S_0,
\]

so all these sets are one common nonempty set `S`.

The same construction, with `p` ending in any chosen mode `q`, shows:
if `u in S` and `P_q(u)` is defined with length `l`, then `P_q(u) in S`.
The image still begins with `(01)^m`; its suffix is precisely `P_q(u)`;
and its total length increases by 1. Theorem 3 now forces
`S={0,1}^l`.

In particular `u=0^(l-1)1` belongs to `S`. Construct a sufficiently long
accepted input `(01)^m p u` with `p` ending in `s2`. But `P_2(u)` halts:
`s2` loops over the zeros, the last 1 enters `s1`, and the right boundary
is reached in `s1`. This contradicts safety. ∎

The conclusion identifies information that any successful regular
invariant must retain: the middle of the word cannot be forgotten after
recording only fixed end windows and length residue. Correlations through
the interior remain necessary. Theorem 3 is deliberately used only
inside this abstraction argument, where arbitrary middle words really
are admitted; it would be invalid to use controllability directly as a
claim about the actual orbit.

## 5. Two further exact obstructions

**Proposition 5 (piecewise-testable languages).** No piecewise-testable
language is a safe inductive invariant containing `00`.

Here a piecewise-testable language is a finite Boolean combination of
tests that a fixed finite word is a scattered subsequence. Let `d` bound
the lengths of all tested words. The word `(01)^d` contains every binary
word of length at most `d` as a scattered subsequence: use at most one
pair for each requested bit. Under the assumed inductive invariant,
Theorem 2 supplies an orbit word beginning with `(01)^d`; all the tests
therefore hold. They also all hold on `(01)^d0`, which is in `B`.
The two words cannot be distinguished by the language, a contradiction. ∎

**Proposition 6 (counts alone).** No language whose membership depends
only on the numbers of zeros and ones is a safe inductive invariant
containing `00`, even if the condition on those numbers is not regular.

Indeed, closure gives `F(00)=01100 in I`. The word `10001` has the same
three zeros and two ones, so it also belongs to `I`. But
`10001=10^3 1` is in `B`. ∎

## 6. Exact DFA certificates and explicit failed candidates

`dfa.py` accepts any complete binary DFA and verifies the three desired
conditions for `F`. It checks initial-word acceptance directly. Safety
is a reachability computation on the product with the four-state DFA
for `B`. Closure is reachability on triples

`(input DFA state, output DFA state, streaming transducer state)`.

The output state starts after the leading 0 of `F`. Reading an input bit
advances the input DFA, the streaming state, and the output DFA by the
emitted bit. At end of input, the verifier processes the relevant
boundary suffix (`0`, `1100`, `00`, or empty), rejects the halting mode,
and tests output acceptance. The graph has at most `5*n*n` vertices for
an `n`-state candidate, so absence of a violating reachable vertex proves
closure for **every** finite input, not merely a length cutoff. A breadth
first traversal gives shortest, lexicographically first counterexamples.

Two natural candidates contain `00` and exclude `B`, but both fail
closure at the same shortest word:

\[
 000\longmapsto 0111\in B.
\]

They are the language of all words ending in `00`, and the language of
all words safe for their next sweep, namely the complement of `B`.

`preimages.py` constructs exact DFAs for survival of a bounded number of
sweeps using transducer preimages and DFA minimization. These are finite
horizon languages, **not** inductive invariants. The first 25 horizons
did not stabilize; their counterexamples are computed exactly. No claim
about impossibility of general regular invariants follows from this
finite observation.

## Reproduction and scope

Run `python certificates.py` and `python dfa.py` from this directory.
The former checks the regex/DFA agreement and identities on all 8,191
binary words through length 12, constructs 1,538 single-bit control
certificates through length 7, and validates the arbitrary-length incoming
mode constructor on several finite lengths. These checks detect code or
algebra mistakes; the universal statements above rest on their proofs.

The blank-generated reduced orbit remains undecided. The remaining
problem is to find a safe invariant for repeated `P_0` from `001100`, or
a finite halting certificate. The obstruction theorems give a reason to
retain recursive or finite-state information about the interior, rather
than repeatedly enlarging a prefix/suffix window.

## 7. Obstruction to a more informed auxiliary-DFA abstraction

A separate part of this investigation classified nonhalting under `P_2`
using a three-state DFA with states `C,D,E`, initial state `C`, accepting
states `C,E`, and transitions

| State | Read 0 | Read 1 |
|---|---|---|
| C | C | D |
| D | C | E |
| E | D | C |

The obstruction below only uses this transition table; it does not depend
on the auxiliary classification theorem. For a DFA `A`, let `tau_A(w)`
be the **entire transformation of its state set** induced by reading `w`,
not only the state reached from its initial state. Thus this feature
retains the answer from every possible starting state simultaneously.

**Proposition 7.** No language containing `001100`, closed under `P_0`,
and disjoint from `B` can have membership determined solely by

* the exact numbers of zeros and ones;
* the full transformation induced on the displayed three-state DFA;
* the full transformation induced on the four-state DFA for `B`.

This permits an arbitrary condition on the counts; it is not limited to
modular or regular conditions.

**Proof by an explicit certificate.** The two words `001100` and `001010`
both contain four zeros and two ones. Both send all three states of the
auxiliary DFA to `C`, and all four states of the halting DFA to its safe
sink. Therefore such a language must either admit both or neither. But

\[
 001010\xrightarrow{P_0}110010
        \xrightarrow{P_0}011110
        \xrightarrow{P_0}\text{HALT}.
\]

The last word has the halting parse `01 · 111 · 0` in Theorem 1. An
inductive language admitting the reduced seed would admit this halting
word, a contradiction. ∎

Even without the count feature, an even shorter obstruction is
`001100 ~ 000010 -> 111010 -> HALT`, where `~` means equality of both full
DFA transformations. For the three-state transformation alone,
`001100 ~ 0000 -> 1110 -> HALT` suffices.

`feature_analysis.py` constructs the finite transition monoid of one or
more supplied DFAs and computes the exact abstract image relation under
`P_0` by a finite product. The combined two-automaton monoid has 87
reachable transformations; its transducer product has 309 reachable
states. These counts are reproducible implementation results. The short
word certificate above is enough to independently verify the mathematical
obstruction without trusting either count or the graph exploration.

This failure is informative: knowing every auxiliary-mode classification
of the *whole word*, even together with exact counts, loses the
positional relationship needed after a pass. A successful refinement
must encode additional order information or correlations through a
recursive decomposition. Merely adding counts to this particular
auxiliary-DFA summary cannot repair it.

## 8. The reduced search loses no regular invariant certificates

Let `a=P_0`, let `v=001100`, and let `d(bx)=(!b)x` on nonempty words.

**Theorem 8.** The following statements are equivalent:

1. There is a regular language `I` containing `00`, disjoint from `B`,
   and closed under `F`.
2. There is a regular language `J` of nonempty words containing `v`,
   disjoint from `B`, and closed under `a`.

The same constructions give an equivalence without the word “regular.”

**Proof, forward direction.** Given `I`, put

\[
 J=\{x\ne\epsilon:\exists k\ge1, (01)^k00x\in I\}.
\]

It contains `v` because `F^2(00)=01·00v`. If `x in J`, select a witnessing
`k`. Two applications of safety and closure of `I`, followed by Theorem 2,
show that `a(x)` is defined and

\[
 F^2((01)^k00x)=(01)^{k+1}00a(x)\in I.
\]

A defined pass never decreases word length, so `a(x)` is nonempty and
belongs to `J`. This proves the two required obligations.

For regularity, take a DFA recognizing `I`. There are only finitely many
states reached after words `(01)^k00`, `k>=1`. The language `J` is the
union of the languages recognized from those states, restricted to
nonempty inputs. This is a direct finite-automaton construction.

**Proof, reverse direction.** Given `J`, define

\[
 I=\{00,01100\}
   \ \cup\ (01)^+00J
   \ \cup\ (01)^{\ge2}1d(J).
\]

The first two exceptional words cover the initial two iterates. Let
`K=(01)^+00J`. For `x=bu in J`, the direct transducer identity is

\[
 F((01)^k00x)=(01)^{k+1}1d(x),\qquad k\ge1.
\]

Thus the last component of `I` is exactly `F(K)`. Its next image lies in
`K`, since Theorem 2 gives

\[
 F^2((01)^k00x)=(01)^{k+1}00a(x)
\]

and `a(x) in J`. These identities also establish that all sweeps in
these components are defined. Finally,
`F(00)=01100` and `F(01100)=01·00v in K`.
All three invariant obligations follow.

For regularity, prefix concatenation and finite union preserve regular
languages, and

\[
 d(J)=0(1^{-1}J)\ \cup\ 1(0^{-1}J),
\]

where the two left quotients are obtained by starting a DFA after one
input bit. Hence the displayed `I` is regular. ∎

This equivalence gives a substantive reason to focus subsequent regular
invariant searches on `a` from `001100`: removing the inert prefix is
not a restriction of the possible regular certificates. It neither
proves a certificate exists nor excludes one.

## 9. A complete regular certificate for a different infinite family

The preceding failures do not mean regular invariants never work for the
transducer. They do work on an explicit separate family. Let `L_c` be
the language accepted by the three-state DFA in Section 7 from state `C`
with accepting states `C,E`. The auxiliary result proves `P_2` is defined
on `L_c` and preserves it; the exact finite certificate below also checks
the resulting `P_0` invariant independently.

For every finite tail `x`, the following table is a parameterized identity
`P_0(px)=p'Q(x)`. The copy action is the identity, and `c=P_2`.

| Prefix `p` | Next prefix `p'` | Tail action `Q` |
|---|---|---|
| `000100` | `111100` | identity |
| `111100` | `010000` | c |
| `010000` | `101110` | identity |
| `101110` | `001000` | c |
| `001000` | `110000` | identity |
| `110000` | `011100` | identity |
| `011100` | `100111` | identity |
| `100111` | `000100` | c |

Each row follows by reading exactly six bits through the transducer. It
is valid including equivalence of definedness when `c` is the tail
action, and including an empty tail. Therefore

\[
 P_0^8(000100x)=000100\,c^3(x)
\]

with equivalence of existence of all intermediate passes. More strongly,
the complete `P_0` orbit of `000100x` is nonhalting if and only if the
complete `c` orbit of `x` is nonhalting: the eight-step block performs
exactly three `c` actions, and the intervening tail actions are identities.

**Theorem 9.** Let `S` be the set of eight prefixes in the first column.
Then

\[
 K=\bigcup_{p\in S}pL_c
\]

is a regular safe `P_0`-invariant containing `000100`.

**Proof of all three obligations.** First, the empty tail belongs to
`L_c`, so `000100 in K`. Second, on an input `px` with `x in L_c`, each
row's tail action is either identity or `c`; both are defined. Thus the
pass does not halt. Third, the output prefix is another member of `S`,
and its tail is either `x in L_c` or `c(x) in L_c`. Hence the image is in
`K`. ∎

`regular_family.py` constructs the language and minimizes its DFA to 19
states. `dfa.py` verifies the three obligations globally by finite product
reachability, with seed `000100` and `prepend=False`. It finds 32 reachable
states in the safety product and 37 in the closure product, with no
violation. The complete certificate is:

```json
{
  "initial": 0,
  "accepting": [15, 17],
  "transitions": [
    [1,2], [3,4], [5,4], [6,7], [7,6], [8,9],
    [18,10], [10,18], [18,11], [18,12], [13,18],
    [18,14], [18,13], [15,18], [18,15],
    [15,16], [15,17], [16,15], [18,18]
  ]
}
```

**Limit of this result.** The reduced blank seed is `001100`, which this
DFA rejects. Its first six bits lie in a different 32-cycle of the
length-six prefix permutation. Boundary extensions never change these
existing six bits, so the blank orbit cannot later enter `K`. The theorem
classifies an infinite family and supplies a genuine regular certificate,
but it does not narrow the blank orbit to that family.

There are related families deeper inside the initial cylinder `001100`:
for example, the prefix `0011000001001010` has return period 256 and a
return section reducing to `c^9` on nonempty tails. Consequently it would
be false to claim that every descendant of the initial cylinder is
excluded from a pure-`c` return family. Determining which descendants the
finite-boundary dynamics actually creates is a separate obligation.

## 10. A precise periodic-tail representation and its obstruction

Here the actions are extended to infinite binary sequences by ignoring
finite-boundary rules. Let `t=(10)^omega`. Direct substitution gives

\[
 c(t)=1100t,\qquad d(t)=00t,\qquad
 b(t)=0t=(01)^\omega,\qquad a(t)=001100t.
\]

For example, `c(10t)=1b(0t)=11d(t)=1100t`, and
`b(10t)=01b(t)`, which uniquely specifies `(01)^omega`.
Also

\[
 a(11t)=0t.
\]

Therefore the `c` and `d` finite-boundary extensions are exactly compatible
with completing a finite word by `t`. The `a` boundary is not: its finite
extension is `0`, while `a(t)=001100t`. Its actual finite-boundary output
can instead be represented by inserting `11` immediately before the
virtual tail and then applying the infinite action, because `a(11t)=0t`.
The `b` finite boundary halts; its infinite action is defined, so simply
completing all words by `t` erases precisely the halting information.

These identities are exact, but the periodic-tail representation is not
a proof of nonhalting. One must still control all exceptional `a` boundary
insertions and prove that a `b` boundary is never exposed. It may be a
useful recursive representation of the missing information; it does not
discharge that unbounded obligation.

`return_sections.py` implements exact recursive lifting of prefix return
maps, without iterating through an exponentially long prefix period. A
return section is a word of pass modes in temporal order. The reductions
`d,a -> c`, `d,c -> a`, and `d,d -> identity` are valid as partial finite
maps **on nonempty tails**. They must not silently be applied to an empty
tail, where boundary extensions differ. The section derivation itself
concerns infinite-word automorphisms; using it for a finite-word safety
argument requires checking that the tail is nonempty or separately
checking the empty case, as the eight-row table above does.
