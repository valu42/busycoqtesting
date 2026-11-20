# Complete decision of the isolated Wily `s2` iterates

This note proves a theorem about **every finite binary word** under repeated
application of `c = wilyPass(s2)`. It does **not** decide the blank-tape Wily
Coyote orbit, whose complete sweep is `F(w) = 0 wilyPass(s0,w)`.

The distinction matters: `0` belongs to the nonhalting language for repeated
`c`, but `wilyPass(s0,0)` is undefined. Consequently the language proved here
is not an invariant satisfying the user's three obligations for `F`.

## 1. Notation and exact boundary rules

Write `a,b,c,d` for `wilyPass` in modes `s0,s1,s2,s3`, respectively. Words are
read left to right, `epsilon` denotes the empty word, and concatenation is
implicit. Function composition below is ordinary right-to-left composition.

For all finite words `x`, the published reduction says

```
a(0x) = 1 b(x)       a(1x) = 0 c(x)       a(epsilon) = 0
b(0x) = 1 d(x)       b(1x) = 0 a(x)       b(epsilon) = undefined
c(0x) = 0 c(x)       c(1x) = 1 b(x)       c(epsilon) = 1100
d(0x) = 1x           d(1x) = 0x           d(epsilon) = 00.
```

An expression with an undefined inner value is undefined. In particular,
identities of partial functions include agreement of their domains.

Two useful identities are

1. `a(d(x)) = c(x)` for **all** finite `x`.
2. `c(d(x)) = a(x)` for **nonempty** finite `x`.

Both follow by cases on the first bit. The empty case of the first identity
is `a(00)=1100=c(epsilon)`. The second identity deliberately excludes the
empty word: `c(d(epsilon))=001100`, whereas `a(epsilon)=0`.

It follows that

```
c(10x)   = 11 d(x),
c(11x)   = 10 a(x),
c^2(10x) = 10 c(x).
```

The first formula is always defined. The third includes equality of the
domains: the second `c` call fails precisely when `c(x)` fails.

## 2. A constructive infinite orbit from epsilon

Define finite words `q_n` by recursion on the nonnegative integer `n`:

```
q_0       = epsilon
q_(2n)    = 10 q_n       (n >= 1)
q_(2n+1)  = 11 d(q_n)    (n >= 0).
```

Every recursive call has a strictly smaller argument. Thus every `q_n`
exists as a finite word. We claim `c(q_n)=q_(n+1)` for every `n`.

For `n=0`, the assertion is `c(epsilon)=1100=11d(epsilon)`. For an even
positive index `2k`, use `c(10q_k)=11d(q_k)`. For an odd index `2k+1`, use

```
c(11d(q_k)) = 10a(d(q_k)) = 10c(q_k) = 10q_(k+1),
```

where the inductive hypothesis applies to `k < 2k+1`. This proves the claim
and gives an explicit infinite `c` orbit. Its first terms are

```
epsilon, 1100, 101100, 110100, 10101100, 11001100, 10110100, 11010100, ...
```

This proof does not infer infinity from a finite observed run.

## 3. Exact halting clock for arbitrary input

Let `H(w)` be the number of **successful `c` calls** before the first
undefined call. Put `H(w)=infinity` if every iterate is defined. These are
accelerated `s2` pass counts, not raw Turing-machine transition counts.

### Theorem

For every finite binary word, `H` is completely determined by

```
H(epsilon) = infinity
H(1)       = 0
H(11)      = infinity

H(0x)      = H(x)
H(10x)     = 2 H(x) + 1
H(110x)    = 2 H(1x)
H(111x)    = 2 H(x).
```

We use the usual conventions `2 infinity = infinity` and
`infinity + 1 = infinity`. Every nonbase rule strictly decreases word
length, so the equations are a terminating exact decision procedure.

### Proof

The empty-word case was proved constructively above. `c(1)` is undefined.
Also `c(11)=100`, and the identities for `0x` and `10x` below show that
`100` has the same infinite `c` safety as the empty word, so `H(11)=infinity`.

The equation for `0x` follows from `c(0x)=0c(x)` at every iteration. For
`10x`, the first `c` call always succeeds, and every pair of calls performs
one `c` call on the suffix while restoring the prefix `10`. Thus a suffix
that survives exactly `k` calls yields exactly `2k+1` successful calls on
`10x`, proving its equation, including the infinite case.

For nonempty `y`, let `z=d(y)`. The partial-function identity
`a(y)=c(d(y))` gives

```
c(11y) = 10 c(z).
```

If `H(z)=0`, this first call is undefined. If `0 < H(z) = k < infinity`,
that call succeeds, the new suffix `c(z)` survives `k-1` calls, and the
`10x` equation gives total clock

```
1 + (2(k-1)+1) = 2k.
```

If `H(z)=infinity`, the same identities produce an infinite orbit.
Therefore `H(11y)=2H(d(y))`. Substitute `y=0x` and `y=1x`, and use the
`0x` equation, to obtain the last two displayed rules. This proves all
cases without an unproved termination or safety assumption.

### Sharp bound

If a length-`n` word halts under repeated `c`, where `n >= 1`, then

```
H(w) <= 2^floor((n-1)/2) - 1.
```

Induction on the shortening rules proves the bound. Each multiplication
by two removes at least two bits; the only additive term is the `+1` in
the `10x` rule. The bound is sharp: `(10)^k 1` has length `2k+1` and clock
`2^k-1`; prepend a zero to attain the corresponding bound at even length.

## 4. The complete nonhalting language is regular

A three-state deterministic automaton recognizes exactly the words with
`H(w)=infinity`. Start in `C`; accept `C` and `E`; reject `D`.

| State | On `0` | On `1` | Accepting? |
|---|---|---|---|
| C | C | D | yes |
| D | C | E | no |
| E | D | C | yes |

To prove equivalence with the clock theorem, call its accepted-word
predicate `L`. The transition table gives

```
L(0x) = L(x)
L(10x) = L(x)
L(110x) = L(1x)
L(111x) = L(x),
```

with accepted bases `epsilon,11` and rejected base `1`. These are exactly
the shortening equations for the predicate `H(w)=infinity`. Induction on
word length proves the claimed equality of languages. It includes both
safety and the converse assertion that every rejected word eventually
halts.

For fixed length `n`, the number of accepted words is

```
(2^(n+1) + (-1)^n) / 3.
```

Indeed, if `D_n` counts words ending in automaton state `D`, the table gives
`D_(n+1)=2^n-D_n` and `D_0=0`; solve this recurrence and subtract from `2^n`.
The counting formula is a consequence of the theorem, not evidence for it.

## 5. Independently checkable finite safety certificate

The companion `c_safety.py` also checks closure of this language under `c`
by an exact product construction. Add identity mode `e` after `d` consumes
its first bit. A product state consists of

```
(pass mode, input-DFA state, output-DFA state).
```

Starting in `(c,C,C)`, exactly these seven states are reachable:

| Pass mode | Input state | Output state |
|---|---|---|
| c | C | C |
| b | D | D |
| d | C | E |
| a | E | C |
| e | C | C |
| e | D | D |
| e | E | E |

Checking both bit transitions of every row establishes closure of this
finite set, hence covers words of arbitrary length. At a right boundary,
all rows whose input state is accepting have a defined extension and an
accepting completed output. The only undefined extension appears in
`(b,D,D)`, whose input is rejected.

This is a finite certificate of an unbounded invariant, not a simulation
cutoff. The code separately compares its exact clock formula with literal
passes on all 32,767 binary words of length at most 14. That latter check
validates implementation, while Sections 2--4 prove the all-length result.

Run with Python 3, without `-O`:

```
python c_safety.py
```

No third-party packages are required.

## 6. Complete decision of isolated `s1` iterates, too

Let `H_b(w)` count successful iterates of `b = wilyPass(s1)` before its first
undefined call, again using infinity for a nonhalting orbit. Then

```
H_b(epsilon) = 0
H_b(0x)      = 2 H(x) + 1
H_b(1x)      = 2 H(d(x)).
```

The last equation includes the empty suffix: `b(1)=00` is nonhalting, and
`H(d(epsilon))=H(00)=infinity`.

To prove these identities, observe

```
b(0x)   = 1d(x),
b^2(0x) = 0a(d(x)) = 0c(x).
```

The first call always succeeds, and each pair performs one `c` call on
`x`, giving the formula for `0x`. For nonempty `x`, use
`b(1x)=0a(x)=0c(d(x))` and the same counting argument as in Section 3. If
`x` is empty, `b(1)=00` and the already proved `0x` case apply directly.

The **same three-state DFA** from Section 4 recognizes all nonhalting
`b` inputs if its initial state is changed from `C` to `D`. Indeed,
reading an initial zero from `D` enters `C`, while reading an initial one
enters `E`. Starting at `E` recognizes the predicate `H(d(x))=infinity`:
its zero and one transitions are respectively the states obtained from
`C` after reading one and zero, and it accepts the empty word, matching
`d(epsilon)=00`.

Thus the three residual predicates have exact infinite-orbit meanings:

| Initial DFA state | Meaning of acceptance on `w` |
|---|---|
| C | Every iterate of `c` on `w` is defined. |
| D | Every iterate of `b` on `w` is defined. |
| E | `a(w)` is defined and every subsequent iterate of `c` on `a(w)` is defined. |

For the last row, use `a(w)=c(d(w))` for nonempty `w`; for the empty word,
`a(epsilon)=0` is `c`-safe. The code checks the `b` clock independently by
literal passes on every word of length at most 14, as well as the `c`
checks described above.

For `n >= 2`, a halting `b` input of length `n` has at most
`2^floor(n/2)-1` successful calls. This is sharp at `0(10)^k1` for even
length and `00(10)^k1` for odd length. Both one-bit words are `b`-safe;
the empty word halts immediately. The `d` iteration is also trivially
nonhalting on every finite word: nonempty words alternate with their
first-bit flips, while `epsilon` enters the cycle `00,10`.

## 7. What this establishes for the research problem

The `s2` component is now completely understood on arbitrary finite inputs,
including an exact halt clock and a regular description of the entire
nonhalting basin. A section/return-map proof reducing the actual blank
orbit to repeated `s2` on an accepted word would finish that branch of the
argument immediately.

That implication has not been established. Complete Wily sweeps restart
in `s0`; actual boundary streams contain `s0,s1,s2,s3`, and preserving the
`s2` nonhalting predicate through those interleavings remains a separate
obligation. For example, `0` is accepted by the three-state automaton,
while `a(0)` is already undefined. This result genuinely removes an
unbounded subproblem for `s2`, but it does not supply the missing invariant
for `F` or decide machines #531/#532.
