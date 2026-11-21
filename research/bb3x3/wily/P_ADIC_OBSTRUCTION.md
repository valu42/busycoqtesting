# A constructive obstruction at every fixed P-adic depth

This theorem concerns **formal bit series over F₂**, where addition is XOR.
It is distinct from ordinary 2-adic integer arithmetic. Write

\[
 P=1+z+z^2,\quad E=1+z^2,\quad t=E^{-1}=(10)^\infty.
\]

For a finite word `w` of length `n`, let `W` be its bit polynomial, with the
leftmost bit as the constant coefficient. Its periodic completion is

\[
 X_w=W+z^n/E.
\]

Because `gcd(P,E)=1`, its residue modulo every `P^k` is well-defined.

The argument below is a theorem for **all** positive integers `k,M`, not a
finite failure to find an invariant. The companion `p_adic_obstruction.py`
implements its witness construction and checks sample parameters.

## 1. The linear inverse and the critical language

Let `S` be the set of infinite binary sequences with no adjacent ones. The
inverse of the infinite-word action `a` satisfies

\[
 a^{-1}(Y)=P Y+1\qquad(Y\in S).
\]

One can check this directly from the three active modes. As long as the output
has no `11`, the previous two output bits identify the current mode:

| Previous two output bits | Forward mode |
|---|---|
| 10 | a |
| 01 | b |
| 00 | c |

The virtual initial pair is `10`. The inverse input bit is the XOR of the
current output bit and these two previous bits. A first output `11` is exactly
the event that leaves this linear regime for mode `d`.

Consequently, a completed finite input `X_w` is a physical next-pass halting
input if and only if `a(X_w)` belongs to `S`. To see the boundary direction,
only the continuation from mode `b` remains forever in the active linear
regime on the periodic tail `t`; the continuations from `a,c` produce `11` and then exit, while reaching
`d` or the copy mode has already produced `11` in the emitted finite prefix.
Thus the completed halting set is

\[
 P S+1
\]

restricted to the ultimately alternating sequences under discussion. In
particular every halting completion is `1 mod P`. This is necessary, not
sufficient, for an arbitrary finite input.

## 2. The obstruction theorem

A reachable blank-core word is

\[
 u=a^{90}(001100)=01101011100010010111.
\]

It has length 20 and suffix `11`. Direct polynomial division gives

\[
 X_u\equiv1\pmod P.
\]

**Theorem.** For every `k>=1` and `M>=1`, there exists a finite word `v` such
that

1. `a(v)` is undefined;
2. `X_v = X_u mod P^k`;
3. `v` has the same last two bits, namely `11`;
4. `|v| = 20 mod M`.

Therefore there is **no** safe `a`-invariant containing `001100` whose
membership depends only on a fixed `P`-adic residue, the last two bits, and
length modulo a fixed integer. This allows an arbitrary membership predicate
on those features. In particular increasing a fixed `P`-adic truncation
cannot repair the approach.

The statement does not exclude invariants using unbounded valuations,
recursive coefficient information, literal prefix information, or a different
arithmetic representation.

## 3. Explicit proof and construction

Put

\[
 N_*=E U+z^{20},\qquad Q_*=(N_*+E)/P.
\]

The latter is a polynomial because `X_u=1 mod P`. Let `H=P^(k-1)`.
For `k=1`, all congruences modulo `H=1` below are vacuous.

Choose an even positive integer `L` divisible by `M` for which

\[
 z^L\equiv1\pmod H.
\]

Such an integer is explicit: if `2^e>=k-1`, then

\[
 (z^3+1)^{2^e}=(z+1)^{2^e}P^{2^e},
\]

so any multiple of `3*2^e` works. Taking the least common multiple with `M`
and 2 meets the other requirements.

Let `R` be the polynomial residue

\[
 R\equiv E^{-1}(Q_*+z^{19})+z^{16}\pmod H,
 \qquad \deg R<\deg H.
\]

Replace each nonzero monomial `z^i` of `R` by

\[
 z^{i+(i+1)L}.
\]

Their sum `A` has the same residue as `R`, but all its ones are separated by
at least `L` zeros. Choose an odd integer

\[
 N\equiv19\pmod L,\qquad N>\deg A+7,
\]

and put

\[
 Q=A+z^{N-3},\qquad Y=Q+z^N/E.
\]

The ones of `A` are separated. The added one at `N-3` is separated from `A`
and from the alternating tail starting at `N`. Hence `Y` has no adjacent
ones: `Y in S`.

The congruence calculation is

\[
\begin{aligned}
 DY&=DQ+z^N\\
   &\equiv E(R+z^{16})+z^{19}\\
   &\equiv Q_*\pmod H.
\end{aligned}
\]

Therefore

\[
 P Y+1\equiv N_*/E=X_u\pmod{P^k}.
\]

Now use `P=E+z` to write the same sequence exactly as

\[
 P Y+1
 =\underbrace{(P Q+1+z^N)}_{V}+z^{N+1}/E.
\]

Let `v` be the `N+1` low bits of the polynomial `V`. This is its full width:
its coefficient at `N` is 1. Its coefficient at `N-1` is also 1, contributed
by `P z^(N-3)`. Thus `v` ends in `11`. Also `N+1=20 mod M`.

Finally, the inverse linear identity proves that the infinite `a` image of
this completion is `Y`. More concretely, the first `N+1` output bits have no
`11` and end in `01`: the output at `N-1` is 0 and the output at `N` is the
first 1 of the alternating tail. The finite sweep is therefore in mode `b`
at its right boundary and halts. This proves all four requirements. ∎

## 4. Consequence for the invariant search

If an invariant based on the stated features contained the blank reduced
seed, closure would force it to contain `u`. For its chosen fixed `k,M`, the
constructed `v` has identical recorded features, so it too would be admitted.
But it halts immediately. This contradicts safety without any further orbit
simulation.

The proof explains the loss of information: the Fibonacci subshift is
surjective onto every finite `P`-adic quotient. Its monomials can be moved far
apart by multiples of the finite order of `z`, preserving the quotient while
changing the global adjacency structure. That freedom is exactly what a
successful recursive invariant must retain rather than quotient away.
