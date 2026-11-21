# Periodic tails, canonical padding, and record-width repairs

## Status and purpose

This note gives an exact reduction of the finite-word `a = wilyPass(s0)`
dynamics to a total periodic-tail map plus a running width record. It does
**not** decide the blank orbit. It removes the separate unbounded padding
counter, identifies the only finite-boundary repair, and specifies a new
reset section on which a further theorem could act.

The blank-core initial word is `001100`, by the previously proved two-sweep
normal form for `F`. The definitions and statements below apply to arbitrary
finite binary inputs, not just to this core.

Write `a,b,c,d` for modes `s0,s1,s2,s3`, and `e` for the identity mode after
an early exit. Read words left to right. A scan of a finite prefix `u`,
without applying its terminal boundary rule, emits a word `p` of the same
length and leaves one residual mode `q`.

## 1. Canonical representatives of the alternating tail

Let `t=(10)^omega`, interpreted as the 2-adic number `-1/3`. For a finite
word `w=w_0...w_(n-1)`, put

```
V(w) = sum_i w_i 2^i,
N(w) = 3 V(w) - 2^n.
```

Then the infinite word `wt` represents `N(w)/3`. Every such numerator is
nonzero modulo 3.

### Lemma: uniqueness up to trailing `10`

Two finite words represent the same `wt` precisely when one is obtained
from the other by appending a power of `10`.

To prove the nontrivial direction, suppose `N(u)=N(v)` and `|v|>=|u|`.
Reduction modulo 3 forces `|v|-|u|=2k`. The equality of numerators gives

```
V(v) = V(u) + 2^|u| (4^k-1)/3.
```

The high-bit factor `(4^k-1)/3 = 1+4+...+4^(k-1)` has least-significant-first
binary word `(10)^k`. Thus `v=u(10)^k`.

Consequently every finite word has a unique decomposition

```
w = v(10)^k,    k>=0,    v does not end in 10.
```

Call `v` canonical, and write `h(N)=|v|` for the canonical width. Conversely,
every integer not divisible by 3 has a finite representative: choose a
sufficiently large width of the parity required by `N+2^n = 0 mod 3`, then
use the integer `(N+2^n)/3` as its binary content. Removing trailing `10`
pairs gives the unique canonical representative.

## 2. The exact, all-parameter padding table

Suppose scanning `u` from mode `a` emits `p` and leaves mode `q`. For every
integer `k>=0`, the **finite** pass on `u(10)^k` is given exactly by:

| Residual mode q | Finite result |
|---|---|
| a, k=0 | `p0` |
| a, k>=1 | `p001100 (10)^max(k-3,0)` |
| b | undefined, for every k |
| c | `p1100 (10)^max(k-2,0)` |
| d | `p00 (10)^max(k-1,0)` |
| e | `p(10)^k` |

These are identities of partial functions, including their domains. They
hold even for `u=epsilon`.

**Proof.** Across an input pair `10`, the residual-mode/output transitions
needed here are

```
a -> c, output 00
b -> b, output 01
c -> d, output 11
d -> e, output 00
e -> e, output 10.
```

Use the known finite boundary extensions `a:0`, `b:HALT`, `c:1100`,
`d:00`, `e:epsilon`. This gives the displayed formulas for `k=0,1,2,3`.
After reaching `e`, every further pair is copied, proving the formulas for
arbitrary `k`.

In particular, appending `(10)^k` never changes whether the **next pass**
halts. The finite output can change, so this is not a claim of equivalence
of eventual halting behavior. The most consequential exception is

```
a(epsilon)=0,       a(10)=001100.
```

The first word then halts; the second is the still-undecided blank core.

The table also proves exact confluences: when `q=a`, the three inputs with
`k=1,2,3` have identical next outputs; when `q=c`, the three inputs with
`k=0,1,2` have identical next outputs; when `q=d`, the inputs with `k=0,1`
have identical next outputs. This is a uniform parameter theorem, not a
claim inferred from a finite run.

## 3. A total virtual map

On infinite words the finite-state pass is total, and direct substitution
of `t` gives

```
a(t)=001100t
b(t)=0t
c(t)=1100t
d(t)=00t
e(t)=t.
```

Thus, for canonical input `v` with emitted prefix `p` and residual mode `q`,
define `A(v)` to be the canonical representative of

```
p E_q t,
```

where `E_a=001100`, `E_b=0`, `E_c=1100`, `E_d=00`, `E_e=epsilon`.
Equivalently, `A` is a total map on integer numerators not divisible by 3.
This virtual map is explicitly different from the finite pass at an empty
`a` or `b` boundary.

The outputs in the `a,c,d` rows end in `00`, so they are already canonical.
Their widths are respectively `h+6,h+4,h+2`. The `e` row has width `h-2r`
for the number `r` of trailing `10` pairs removed from its emitted prefix.
In fact `r` is either zero or one. If the copied suffix had length at least
two, an output ending in `10` would force the canonical input to end in
`10`, impossible. Consequently the single bit flipped by `d` must be last
or penultimate. The two preceding output bits are `11`, so an output ending
in `10` has suffix `110` or `1110`, respectively, and cannot end in `1010`.
Thus at most one pair is removed.

For a canonical input, the `b` row decreases canonical width **exactly one**.
Use the boundary-`b` language `L*(0|10*1)`, where
`L=(01|10*11)`. A canonical input of the first form must be just `0`, since
any nonempty `L*` prefix ends in `1` and would make the input end in `10`.
This input virtually maps to `t`, decreasing canonical width from one to
zero. An input of the second form is `l 10^j1`, with `l` in `L*` and `j>=0`.
Its scan output is `p 0^(j+1)1`, where `p` is the output of `l`. Appending
the virtual extension `0` and stripping a single final `10` leaves
`p 0^(j+1)`. This is canonical: `p` is empty or ends in `10`, and at least
one zero follows it. No further pair is removed.

In summary, the virtual canonical-width increments are

| Residual mode | Change of canonical width |
|---|---|
| a | +6 |
| c | +4 |
| d | +2 |
| e | 0 or -2 |
| b | -1 |

These observations give the exact singularity criterion

```
finite a halts on v(10)^k  iff  A(N(v)) = -N(v) (mod 3).
```

This is a one-step test expressed in terms of the virtual map, not a
closed autonomous map on residue classes. No claim that `A` is determined
by `N mod 3`, or by any other fixed modulus, is being made.

## 4. The padding counter is a running maximum

Represent an actual finite word by its canonical word `v` and its physical
length `L`:

```
w = v(10)^((L-|v|)/2),
L>=|v|,   L=|v| (mod 2).
```

Call a step a **repair** if the canonical scan ends in mode `a` and there
is zero padding, that is, `L=|v|`.

### Record-width theorem

For every finite input represented in these coordinates:

1. If the canonical scan ends in `b`, the actual pass halts, independently
   of `L`.
2. If the step is a repair, with scan output `p`, the actual next state is
   canonical `p0`, with new physical length `L+1`.
3. Otherwise the actual canonical next word is the virtual output `A(v)`,
   and its new physical length is exactly

   ```
   L' = max(L, |A(v)|).
   ```

Consequently, throughout any actual orbit before it halts,

```
L_t = max(L_0, |v_1|, ..., |v_t|).
```

In particular, between repairs the actual word follows a single virtual
`A` orbit, and the separate padding counter is given explicitly by

```
k_t = (max(L_start, max_{s<=t}|A^s(v_start)|) - |A^t(v_start)|)/2.
```

### Proof

The halting and repair cases follow immediately from the padding table.
In the repair case `p0` is canonical: if the scanned word is nonempty,
entry into final mode `a` emits a last zero, so `p0` ends in `00`; the empty
input gives canonical word `0`.

For a nonrepair `a` step, the padding is positive and the table gives
canonical output of width `h+6` and residual padding `max(k-3,0)`. Its total
length is `h+6+2 max(k-3,0)=max(h+2k,h+6)`. The same calculation gives the
claim for `c` and `d`, with decrements 2 and 1. For `e`, canonicalization
removes `r` trailing pairs from `p`, so its canonical width is `h-2r` and
its new padding is `k+r`; the physical length stays `L`.

These prove `L'=max(L,|v'|)` in all nonrepair cases. A repair has
`|v'|=L+1`, so this same running-maximum relation also holds through a
repair when `v'` denotes the actual repaired canonical word. Induction
proves the global formula.

The padding is determined by the canonical word and the running width record.
The record remains an unbounded state variable; this is not an autonomous
one-dimensional reduction. The theorem also shows
precisely where that removal does not permit the finite dynamics to be
replaced by the virtual map: a mode-`a` event at the current width record
uses the repair instead.

## 5. The repair in integer coordinates

The virtual `a` boundary constant has numerator `N(001100)=-28`, whereas
the actual extension `0` has numerator `N(0)=-2`. Therefore a repair at
canonical width `h` replaces the virtual numerator by

```
N' = A(N) + 26 * 2^h,
L' = h+1.
```

The exact arithmetic reduction is therefore:

```
if the residual mode is b: halt
else if the residual mode is a and h(N)=L:
    (N,L) -> (A(N)+26*2^h(N), L+1)
else:
    (N,L) -> (A(N), max(L,h(A(N)))).
```

The blank core starts at `(N,L)=(-28,6)`. The defect term vanishes modulo
13, but that observation alone gives no invariant: the virtual map is not
known to descend to that residue quotient.

## 6. A sparse reset section

Every repair destination belongs to the exact language

```
R = (0*10)*0
  = {0} union {words with no 11 that end in 100}.
```

Conversely every member of this language is the output of some boundary-`a`
repair.

**Proof.** The scan inputs ending in `a` without an early exit are exactly

```
(01 | 10*11)*.
```

The two types of first-return block have outputs

```
01       -> 10,
10^j11   -> 0^(j+1)10.
```

Their output-block set is exactly `0*10`. Appending the actual final zero
gives `(0*10)*0`, and reversing the block correspondence proves the converse.

Every repair therefore restarts a virtual-orbit segment in this section,
at zero padding and at a new physical-width record. Apart from `0`, these
words are precisely canonical Zeckendorf representations of positive
integers, written least-significant first with Fibonacci weights
`1,2,3,5,...`, followed by `00`.

This is a structural section, not a safe family. It contains the immediately
halting input `0`, and it also contains `000100`, whose nonhalting was proved
in the earlier section-cycle certificate. The sparse shape alone cannot
replace a proof about the particular reset sequence.

For example, the first repair reached from the blank core is a finite,
independently reproducible event. It occurs on the 583rd reduced pass, after
582 completed passes. Its input and output are

```
0101111010101101111101011011
    -> 10100101010100010010101000100.
```

The latter word has Fibonacci value `390625=5^8`. This is an exact finite
observation, not a proved rule for the next reset. Powers of 5 are not a
uniform safe family: the reset word representing `25`, namely `101000100`,
halts on its seventh reduced pass. Its terminal input is `111010111`.

## 7. What remains to prove

One can now formulate the remaining obligation as competition along virtual
orbits. Starting at a reset word with record `L=h(N)`, follow the total
virtual map until either

* a `b` singularity is reached, which gives an actual halt;
* an `a` event occurs at the current running width record, which produces
  the explicit sparse reset above; or
* neither event occurs, in which case the actual orbit is nonhalting.

A sufficient nonhalting theorem would give a recursively described subset
of reachable reset words and prove, for every member, either the third
alternative or a next reset in the same subset before any `b` singularity.
The initial blank-core segment would also have to enter that subset. A
halting theorem could instead force an eventual `b` singularity before the
next protective repair.

Neither alternative is proved here. The advance is the exact elimination
of the padding counter, the identification of the exceptional event as a
width-record condition, and the sparse reset section. The virtual bulk
still contains an unbounded orbit problem, so this note does not treat the
new notation as a solution.

## Reproduction

Run `python padding.py` with Python 3 and assertions enabled. The checker
validates numerator/canonical conversion, the all-parameter formulas on
representative finite instances, the record-width step against literal
finite passes on all 2,047 words of length at most 10, the modular singularity
criterion, and the first blank-core repair.

Those finite checks validate the implementation. The statements for arbitrary
padding, arbitrary words, and arbitrary times rest on the proofs above.
