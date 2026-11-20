# Arithmetic partial results for the Wily Coyote pass

These results do **not** decide Wily Coyote. The precise new arithmetic results
are sixteen universally quantified return identities, an independently checked
counterexample to a natural residue invariant, and an explicit obstruction to
ignoring the finite boundary when using binary counter encodings.

The companion `arithmetic_certificates.py` is standard-library Python. Run:

```sh
python arithmetic_certificates.py
```

The program finishes in well under a second on the research environment. It
checks finite certificates for universal identities; the logical bridge from
those certificates to the universal statements is given below. This is not a
Lean formalization.

## 1. Notation and composition identities

Write `a,b,c,d` for the finite-word passes starting in modes `s0,s1,s2,s3`.
Composition is ordinary function composition, with the rightmost function
applied first. Equality of partial transformations includes equality of domains.

For every finite word `x`,

\[
a(d(x))=c(x).
\]

For a nonempty word `x`, also

\[
c(d(x))=a(x),\qquad d(d(x))=x.
\]

**Proof.** For nonempty words, split on the first bit and use the defining
transducer rules. At the empty word the first identity remains valid:
`d(ε)=00`, `a(00)=1100=c(ε)`. The other two identities fail at the empty word:
`c(d(ε))=001100` but `a(ε)=0`, and `d(d(ε))=10`, not `ε`.

All four passes preserve nonemptiness whenever defined on a nonempty input.
Consequently the nonempty identities can be composed freely while a nonempty
tail is being transformed. The executable certificates never apply these
identities to an empty tail.

## 2. A literal binary odometer inside the transducer

Let the two-letter digit code be

\[
\rho(0)=01,\qquad \rho(1)=10.
\]

Extend `rho` by concatenation. If `u(n)` is the ordinary binary expansion of `n`
written least significant bit first, with `u(0)=ε`, define

\[
R(n)=\rho(u(n))0,\qquad E(n)=0R(n).
\]

Then the following exact theorem holds:

\[
\boxed{b(R(n))=R(n+1)\quad\text{for every }n\ge0.}
\]

This is a general theorem, not an observation about a simulated prefix. The
proof is the usual carry induction using the three exact identities

\[
b(0)=100,\qquad b(01x)=10x,\qquad b(10x)=01b(x).
\]

The last identity includes partial definedness. It changes a low counter digit
`1` to `0` and propagates the carry. The middle identity changes a low digit `0`
to `1` and stops. The first supplies the new most significant digit at overflow.

More generally, the regular language

\[
J=(01\mid10)^*0
\]

is closed under `b`, and `b` is defined on every member. Leading zero counter
digits may be retained in this larger language. Therefore `1J` is closed under
`c`, because `c(1x)=1b(x)`. In particular,

\[
c^n(10)=1R(n)\quad(n\ge0),
\]

and `c(ε)=1100=1R(1)`, so both auxiliary orbits are nonhalting.

These auxiliary safe families do not establish safety of the blank-generated
`a` orbit. That orbit begins at `E(2)=001100`, but `a` does not preserve `0J`.
For example `00 in 0J` and

\[
a(00)=1100,\quad a^2(00)=0111,\quad a^3(00)=\text{HALT}.
\]

## 3. A symbolic prefix certificate proves an infinite arithmetic family

For a fixed prefix `p`, one application of `a` gives an exact identity

\[
a(px)=p' q(x),\qquad q\in\{a,b,c,d,\mathrm{id}\},
\]

where `p'` has the same length as `p`. This is a single finite transducer walk,
and holds for **every** tail `x`, with partial definedness.

Iterating this fixed prefix walk `t` times gives

\[
a^t(px)=p_t q_t\cdots q_1(x).
\]

On nonempty tails replace every `a` by `c d`, then cancel adjacent `d d`.
The certificate succeeds only when the remaining composition is `b^j`. Thus it
proves the exact universal statement

\[
\boxed{a^t(px)=p_t b^j(x)\quad\text{for every nonempty }x.}
\]

If `p=0 rho(u_k(r))` and `p_t=0 rho(u_k(s))`, where `u_k` denotes exactly `k`
binary digits, substitute `x=R(m)` for `m>=1`. The odometer theorem gives

\[
a^t(E(2^k m+r))=E(2^k(m+j)+s).
\]

No intermediate halt is possible: equality of the composite partial functions
and totality of `b^j` on `J` establish definedness of the entire `a` excursion.

### The finite-boundary caveat

When `r` has fewer than `k` binary digits, the word `pR(0)` is a **padded**
encoding of `r`, not the canonical `E(r)`. Therefore the representative `n=r`
has to be checked separately. All rows in the following table include that
check. They consequently hold for **every** nonnegative `n` in the stated
residue class, including the short representative.

| Condition on n | Number t of a passes | Exact output |
|---|---:|---|
| n ≡ 1 (mod 2) | 2 | E(n+3) |
| n ≡ 4 (mod 16) | 6 | E(n+21) |
| n ≡ 8 (mod 32) | 14 | E(n+69) |
| n ≡ 2 (mod 64) | 62 | E(n+429) |
| n ≡ 16 (mod 64) | 14 | E(n+69) |
| n ≡ 24 (mod 64) | 14 | E(n+69) |
| n ≡ 14 (mod 128) | 126 | E(n+1053) |
| n ≡ 34 (mod 128) | 62 | E(n+429) |
| n ≡ 44 (mod 128) | 22 | E(n+165) |
| n ≡ 48 (mod 128) | 30 | E(n+141) |
| n ≡ 118 (mod 128) | 94 | E(n+1221) |
| n ≡ 64 (mod 256) | 78 | E(n+741) |
| n ≡ 76 (mod 256) | 54 | E(n+549) |
| n ≡ 78 (mod 256) | 126 | E(n+1053) |
| n ≡ 120 (mod 256) | 126 | E(n+573) |
| n ≡ 174 (mod 256) | 126 | E(n+1245) |

For instance, the row `n ≡ 2 mod 64` has output residue `47` and tail action
`b^6`, because `2+429=64*6+47`. Its universal prefix certificate reads

\[
a^{62}\bigl(0\rho(010000)x\bigr)
 =0\rho(111101)b^6(x)
\]

for every nonempty `x`, with both fixed binary strings displayed least
significant bit first. The exceptional short input `E(2)` is checked directly.

These are return identities; no claim is made that the displayed time is the
first return time for every member of a parameter family.

The first row also has a short pencil-and-paper derivation. For `n=2m+1`,

\[
\begin{aligned}
a^2(E(n))
 &=0c(b(R(n)))\\
 &=0c(R(2m+2))\\
 &=0c(01R(m+1))\\
 &=001b(R(m+1))\\
 &=001R(m+2)=E(2m+4).
\end{aligned}
\]

## 4. What fails, and why it matters

### 4.1 A residue conjecture fails inside an excursion

Every even-to-odd row above, followed by the odd row, has a combined increment
divisible by 24. The blank cross-section starts

\[
E(2)\xrightarrow{62}E(431)\xrightarrow{2}E(434).
\]

This suggests the tempting conjecture that all `E(24m+2)` are safe. It is false.
The concrete counterexample is

\[
E(146)=001100101100101100,
\]

which halts on its 135th `a` pass. Its state after 134 passes is

\[
010111101010110110111111.
\]

The next pass is undefined. None of the 134 intervening words belongs to the
larger padded cross-section `0(01|10)*0`.

Thus even a conserved residue on established returns cannot justify the
existence or safety of the next return. Any viable invariant must constrain the
excursion itself or supply a complete certified return map.

### 4.2 Erasing width gives false universal statements

A symbolic prefix certificate exists with

\[
k=19,\quad r=434,\quad t=13694,\quad \Delta=1994205.
\]

It proves

\[
a^{13694}(E(n))=E(n+1994205)
\]

for `n ≡ 434 mod 2^19` with `n>=2^19`. It does **not** hold for the short
canonical representative `E(434)`: direct execution of the finite certificate's
short base case yields a different word. The companion verifier checks this
failure explicitly.

A still more severe example is the canonical `E(10)`, which halts in 254 passes.
Sufficiently padded words with the same counter value can have symbolic safe
prefix certificates. These are different finite words and must not be identified.

## 5. Exact scope and remaining obligation

The odometer lemma and all sixteen arithmetic families are exact, parameterized
mathematical results. The symbolic certificates discharge finite obligations
for arbitrary tails; they do not merely increase a simulation horizon.

They do not furnish an inductive family containing the blank orbit. The covered
arithmetic classes take the blank core from `E(2)` to `E(434)`, and then the
established return families stop applying. Neither perpetual return to `E`, nor
safety of excursions from arbitrary members of a residue class, has been proved.

A next theorem that would complete this strategy would be a width-sensitive
recursive description of the excursions, with a proved return-or-nonhalting
alternative, whose reachable parameter family is closed and excludes a
halting exit. Merely adding more isolated residue rules does not discharge that
obligation. The counterexample `E(146)` shows exactly why.
