# Lines 3–5: arithmetic opportunities and obstructions

Research pass: **2026-11-18**. Starting repository commit:
`2ab106f706cb1715d494c7f67464e9222092058f`.
All runs start on the two-way blank tape, A at coordinate zero. Raw time counts
defined instructions; reaching the undefined entry takes no additional step.

**Outlook: Unknown for all three machines.** There are exact halting triggers,
but no argument that the blank orbit reaches one. New work here adds an exact
clock and a longer checked execution for line 3, an inverse-target exclusion
test for line 5, and actual-orbit distribution checks for lines 4 and 5. None
of these is a blank-tape halting or nonhalting proof.

## Baseline and current sources

| Line | Exact identity | Inherited result |
|---:|---|---|
| 3 | `1RB---0RB0LA2RA_2LB2LA3RA4LB0LB` | Mixed binary/ternary counter; lower bound ≥10^151; higher resets unresolved. |
| 4 | `1RB3LA1LA1RA3RA_2LB2RA---4RB1LB` | Exact A/B returns; raw floor >10^1,719,137; four forbidden exponent classes modulo 42. |
| 5 | `1RB3LA1LA1RA1RA_2LB2RA---4RB1LB` | Exact A/B returns and timed replay; endpoint approximately 1.99499×10^104610. |

The full strings were matched against the current individual wiki pages:
[line 3, revision 7282](https://wiki.bbchallenge.org/w/index.php?title=1RB---0RB0LA2RA_2LB2LA3RA4LB0LB&oldid=7282),
[line 4, revision 6814](https://wiki.bbchallenge.org/w/index.php?title=1RB3LA1LA1RA3RA_2LB2RA---4RB1LB&oldid=6814),
and [line 5, revision 6815](https://wiki.bbchallenge.org/w/index.php?title=1RB3LA1LA1RA1RA_2LB2RA---4RB1LB&oldid=6815),
read on the pass date. The line-3 counter rules are credited to mxdys; line-4
normal forms to Racheline; line-5 normal forms to mxdys and Racheline. Discord
attribution is inherited from these public pages, not independently inspected.

Repository baseline derivations are [mixed-and-sweeps.md](../mixed-and-sweeps.md),
[line4.md](../line4.md), [line4-scalar.md](../line4-scalar.md),
[ACCELERATORS.md](../ACCELERATORS.md), and
[the line-5 timed rules](../frontiers/line5_timed.py).

**Important source limitation, checked this pass:** the external line-3
[TODO](https://github.com/rwst/bbchallenge/blob/main/1RB---0RB0LA2RA_2LB2LA3RA4LB0LB/TODO.md)
(blob `4b7a02d27a36fd4dd13398065d1253576d74480c`) says its outstanding Lean
`sorry` relies on a false parity invariant. Its
[Probabilistic.lean](https://github.com/rwst/bbchallenge/blob/main/1RB---0RB0LA2RA_2LB2LA3RA4LB0LB/Probabilistic.lean)
(blob `9c5a3d1ecb090cf53a13ab3bbc1603764839a0b8`) explicitly warns that an
overflow branch is disproved and that its arithmetic era sequence after era
2 is not reliable as the TM trajectory. We therefore do **not** transfer its
very small numerical risk estimate or its nonhalting conclusion to this
machine. Partial Lean results are not a formally verified blank nonhalting
proof. No Lean or Rocq kernel verification was performed in this pass.

<a id="line-3"></a>

## Line 3: an exact clock for mixed counter probes

### Established structure and halt trigger

Use the inherited `C(X,d,p,v)` representation: `P(X)` is `13` followed by the
binary digits of X with the leading 1 omitted, encoding 0/1 as symbols 2/3.
An A head scans the pivot 2, followed by d ternary pairs, pad p∈{0,1}, and
blank exterior. Pairs 22,02,42 encode ternary digits 0,1,2. `E(X,d)` and
`O(X,d)` have zero counter and pad 0 or 1.

Ordinary counter exhaustion creates reset opportunities. In an odd reset,
the leftward A pass erases trailing binary ones. If it reaches the marker
1, the undefined entry A1 halts. In particular `O(2^m−1,d)` halts; inherited
reset rules also give `O(2^(m+3)−13,d)` and `O(2^(m+4)−25,d)` halting
families for m≥2. These are sufficient auxiliary conditions, **not an
exhaustive description of all cascaded resets or a blank reachability claim**.
The actual blank orbit reaches O(6947,8) at step 59,171; its next reset is a
known longer branch, already refuting indefinite extrapolation of the short
even-reset formula.

### New exact raw-time lemma

The inherited token-capacity shortcut processes a string of pairs `(2,c)`,
c∈{2,0,4}, and singleton 4s. Pair values are v=0,1,2. Starting from the far
cut, capacity is transformed by `N↦3N+v` at a pair and `N↦floor(N/2)` at a
singleton. Every n up to that capacity gives a safe batch of completed
probes without touching the cut.

Here is the new clock. If n probes enter one token:

* A pair receives n probes, sends `q=floor((n+2−v)/3)` child probes, and
  contributes exactly `3n+q` local instructions.
* A singleton 4 sends 2n child probes and contributes exactly 3n local
  instructions.

For a nonzero pair value the local path takes three instructions; a zero
value takes four plus the child call. A singleton executes A4, a child call,
B2, a second child call, B3. These paths are all defined. Iterate the child
request counts through the token list and sum local costs. The capacity
guard makes the final child count zero, so no omitted excursion can reach a
halting cut.

The interleaved binary increment has an exact aggregate cost. Write
`s₂(z)` for popcount and `ℓ(z)` for binary length. For a complete P(X), n
increments cost

\[
3n+2(s_2(X)-s_2(X+n))+2(\ell(X+n)-\ell(X)).
\]

An ordinary increment j−1→j costs `2v₂(j)+1`; crossing a power of two costs
two more instructions to recreate the marker. Summing valuations gives
`Σv₂(j)=n+s₂(X)−s₂(X+n)`. This proves the formula. With only t available
binary cells of value x, cap n at `2^t−1−x`; the same formula without the
length term applies, and the carry never touches the unknown left context.
Adding the binary and token costs supplies the exact clock. Literal steps
handle everything outside the shortcut's guard.

### New blank run and checks

[arithmetic_checks.py](arithmetic_checks.py) compares **1,173** full and
partial-prefix shortcut cases against a literal interpreter, including whole
tapes, state, head and exact raw count. A separate blank comparison agrees
at every operation through **200,086** instructions, including 785 jumps.
The longer blank run reaches its 300th zero-counter checkpoint in exactly

`474785757405757851752355817601200608407144651560821563445304885079334485637979920986464882357386623678040746754713618753835663984965017921683919103082992312131632781857409102685280265155053788988249700415776883642264190264516215501043361454023433456339916801603286861491809139427911164449`

defined steps, approximately **4.74786×10^287**, without halting. Its d=601,
p=1. The complete nonzero tape, head, state, exact X, exact raw count and all
300 zero checkpoints are in
[arithmetic_line3_checkpoint.json](arithmetic_line3_checkpoint.json). The
derivation plus differential tests justify this endpoint; it is not
kernel-certified. This replaces the row's inherited floor, not its outlook.

There are 198 odd zero-counter checkpoints. Splitting them into two groups
of 99, their trailing-one counts are:

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 9 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| First 99 | 47 | 25 | 19 | 3 | 2 | 1 | 1 | 1 |
| Next 99 | 53 | 28 | 9 | 2 | 7 | 0 | 0 | 0 |

Both halves sample longer resets. These small histograms do not establish
independence, uniform binary tails, or an asymptotic distribution. The saved
transition matrix exposes correlations for further analysis. A model that
randomizes every counter reset also discards exact inherited relations such
as `D↦D/2` along consecutive even resets, where `D=17X−2·3^(d+2)`.

**Estimate:** none. The exact clock now converts any reproduced probe/reset
sequence to raw instructions, but there is no justified distribution of
future reset types, no exhaustive higher-reset rule, and no proof of eventual
contact with the marker. **Next step:** derive all cascades indexed by the
trailing-one count k, retaining the true binary residue and the token word,
then analyze their reachable invariant set.

<a id="line-4"></a>

## Line 4: sparse ternary-exponential targets

Inherited normal forms use physical state A in both configuration families.
Blank reaches B(2,7) at raw step 93 and A(6,71) at 6,393. For a return
A(6,b), choose maximal n with `L_n=8(3^n−1)−n≤b`. Its next A phase halts
**iff** `b=H_n=24·3^n−n−11`. Otherwise the exact B recurrence either returns
to another A(6,b), or continues forever without halting. Each finite B macro
is safe. Thus A returns are precisely the halting opportunities.

The actual return values strictly increase. The inherited inverse argument
excludes `n≡1,15,22,36 (mod 42)` from blank, and a million exact scalar
returns pass all smaller target levels up to width 1,801,571. Its rigorously
derived raw floor is **>10^1,719,137**; this is not an expected stopping time.
The larger floor is inherited, not reproduced in full here.

The elementary timing rules are inherited and exact: an A-to-A round
at parameter a costs `6a²+20a+19`; consuming j residual pairs costs
`6j²+14j`; q B triple reductions cost `q(42q+12b+14)`, followed by the
specified boundary cost. Hence an n-wide A phase already has a cost on
the scale `9^n`, and the B excursion adds its own parameter-dependent cost.
One cannot multiply an unproved trial count by a constant time.

New [actual-orbit checks](arithmetic_orbit_results.json) inspect 4,000
successive returns in four disjoint windows. Mean B-excursion lengths are
3.053, 2.920, 2.904, 2.946; adjacent-length correlations range from −0.042
to +0.014. This superficially resembles a geometric return law but does not
test rare exact halting targets. Within-width positions are visibly biased:
the bottom decile contains 302 returns and the top 617. Residue exclusions
also rule out an unrestricted uniform model. Small linear correlation does
not establish independent deterministic trials.

**Estimate:** none. A toy uniform model would give one target among roughly
`16·3^n` integers at width n, a *decreasing* hazard; it would not justify
inevitable halting. We do not adopt it. Auxiliary tapes can halt after
arbitrarily many returns, but no chain back to the actual seed 71 is known.
**Next step:** combine the exact inverse B residues with the distinguished
seed to extend the reachable-target obstruction beyond modulo 42.

<a id="line-5"></a>

## Line 5: a new inverse-target exclusion certificate

### Inherited exact recurrence

Blank reaches A(4,4) at raw step 136. The A(4,b) return halts in its next A
phase iff

\[
b=H_n=16\,2^n-n-11,
\qquad L_n=8\,2^n-8-n\le b<L_{n+1}.
\]

Otherwise it returns through B, or stays safely in B forever. Return values
strictly increase. The saved 100,000-return endpoint has width **173,750**
and raw time approximately **1.99499×10^104610**. That is the established
floor; it supplies no halting prediction.

### New obstruction, proved conditionally on an explicit integer test

Fix n≡13 or 18 modulo 20. Set `p=2^n`, `C=3n+11`, and
`K=32p+n−11`. If there is **no** nonnegative j satisfying

\[
16p+n+5\le C3^j\le16p+3n+5, \tag{1}
\]

then the blank orbit cannot reach H_n at any A(4,b) return.

Proof: an ordinary residual A state has `a=8·2^m−4`, `0≤u≤a`.
Its first B state is B(a−u,2u). A direct return requires a−u≡1 modulo 3,
and gives

\[
y=(5a+u+1)/3=(x+32\,2^m+m-11)/3.
\]

Its possible image lies between `(40·2^m−19)/3` and `16·2^m−8`.
Any return after at least one B-to-B event has y≡2 or 4 modulo 5, because
that event sets the second B parameter to 0 or 2. The exceptional A endpoint
u=a+2 can return directly only for even m, with image
`(80·2^m−26)/3`, of residue zero modulo 5.

Suppose H_n occurred. Forced same-width predecessors would be

\[
y_j=(K-C3^j)/2,\quad y_0=H_n.
\]

Since C is a multiple of five, their residue modulo five is constant: 3 for
n≡13 and 0 for n≡18 modulo 20. Neither permits a B-to-B excursion. For the
first class, residue 3 also excludes the exceptional endpoint. For the
second class, a special image in `[L_n,H_n]` could only come from m=n−1:
smaller m gives an image below L_n and larger m above H_n (n≥18 suffices).
But n−1 is odd, so that direct special return is impossible.

Every predecessor must therefore be ordinary. The image interval rules
out m>n. A smaller width has y≤8p−8; combined with y_j≥L_n, this requires
exactly (1). If (1) fails, each predecessor must have width n. The inverse
formula is then forced at every step. It strictly decreases and eventually
drops below L_n, a contradiction. No such y_j can be the initial seed 4
while it has width n. This proves the claimed exclusion.

The supplied integer test checks the least j with C3^j at least the lower
endpoint of (1), then compares to the upper endpoint. A floating-point
logarithm only provides an initial guess; exact integer adjustments and
guards establish the final j, so rounding cannot affect the certificate.
It finds **no escape for any of the 20,000 selected exponents through
n=200,000**. Therefore all these targets are excluded. **2,626** are at or
above the inherited endpoint width, so this is more than a recount of
already-passed targets. The finite test does **not** prove that both entire
residue classes are impossible for every n. The ordinary direct-return
formula is independently checked on 16,659 tractable inputs; 192 full
configuration/clock checks and the inherited universal symbolic timing
checker also pass.

### Correlations and runtime outlook

New actual-orbit samples cover 4,000 returns in four disjoint windows. Mean
B-excursion lengths are 3.022, 3.053, 3.039, 3.007; lag-one correlations
range from −0.020 to +0.046. The within-width bottom decile has 248 samples
versus 643 in the top decile. These observations do not license independent
uniform target draws. The new inverse obstruction identifies exact
restrictions that such a model would miss.

Exact raw clocks are already available: at A with x=a+4, k full doubling
rounds cost `2x²(4^k−1)/3−3x(2^k−1)+3k`; residual j single consumptions
cost `j(2j+9)` plus a boundary cost. Grouped B reductions cost
`q(15q+6b+27)` plus their boundary cost. The run length between successive
opportunities changes with the current parameters; no constant conversion
from event count is valid. A phase at width n has an exponential-in-n raw
cost, but a halting width distribution has not been established.

**Estimate:** none, including no conditional median. A toy one-hit-in-`8·2^n`
model has a shrinking hazard and needs a distribution of widths and their
correlations; the data and inverse obstruction do not supply that model.
**Next step:** prove or disprove (1) for the two complete exponent classes,
or use its rare possible near-equalities to branch a full inverse search.

## Reproduction and artifacts

From the repository root, with Python 3.10+ and assertions enabled:

```sh
python3 research/bb2x5/halting-outlook/arithmetic_checks.py --zeros 300 --max-n 200000
python3 research/bb2x5/halting-outlook/arithmetic_orbit_checks.py
```

Results: [exact checks](arithmetic_results.json),
[check transcript](arithmetic_verification.txt),
[line-3 full checkpoint and trace](arithmetic_line3_checkpoint.json),
[orbit statistics and exact endpoints](arithmetic_orbit_results.json),
[orbit transcript](arithmetic_orbit_verification.txt).
The scripts use the repository's literal transition interpreter for
differential checks. Every newly batched line-3 stretch has the local
no-halt argument above; checks compare complete configurations and clocks.
Line-4/5 orbit sampling reuses existing timed reductions rather than adding
an unvalidated accelerator. The probabilistic discussion is explicitly
diagnostic, not an empirical proof or a runtime forecast.
