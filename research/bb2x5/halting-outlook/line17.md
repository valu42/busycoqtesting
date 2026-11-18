# Line 17: a guaranteed next overflow, but no calibrated halting clock

Machine: `1RB2RA3LB---2LB_2LA0LA4RB0RB1LA`.

Starting repository commit: `2ab106f706cb1715d494c7f67464e9222092058f`.
Research pass: **2026-11-18**. No formal proof assistant verification was performed.

## Accelerator update

The fused simulator reached 337,241,228,953,203,465,014,813,971,709,954 ordinary sweeps and pair 202 at ≈ 1.59224 × 10^66 raw instructions from blank. Two extrapolations from 21 shortened registers put the first +12 visit around 4 × 10^149 or 3 × 10^158 instructions. The rigorous upper bound is 3.545 × 10^331. The first five genuine marks at cut 403 occupy slots 5, 11, 17, 23 and 29. The blank trajectory still has two previously observed overflow resets and no calibrated raw halting clock.

[Simulator, experiments, and reproduction](../line17-accelerator.md) · [Exact blank-tape checkpoint](../frontiers/runs/line17-epochs.json)

## Earlier repository results

**Handoff update.** The active simulation reached 10^29 normal sweeps and pair 175 at ≈ 1.40000 × 10^59 raw steps. The upper bound on visiting +12 still applies. [Exact checkpoint](https://github.com/valu42/busycoqtesting/blob/12c4acdce3310d435190895136f65826a702f1c8/research/bb2x5/frontiers/runs/line17-epochs.json) · [First-visit analysis](https://github.com/valu42/busycoqtesting/blob/12c4acdce3310d435190895136f65826a702f1c8/research/bb2x5/line17-edge-time.md)

A later replay locates the actual first arrival at pair 175 after 122,738,729,699,760,992,018,224,200,752,726,973,004,558,037,906,774,074,004,819 instructions. At the later checkpoint of 10²⁹ sweeps the first four marked slots have reached pairs 173, 169, 165 and 161. The return from coordinate +12 remains open. [First visits and source marks](https://github.com/valu42/busycoqtesting/blob/91f5cde3f22ec17fd2dd7c895899fa2755449ee2/research/bb2x5/line17-edge-time.md)

At the opening intake the repository had completed **6 × 10²⁸ ordinary sweeps**, at approximately 5.04000 × 10⁵⁸ defined instructions. The later cut-rank calculation puts the next visit to +12 before **3.176 × 10³⁴⁴** defined instructions. The actual marks at slots 9 and 10 of cut 418 select the branch. Finite continuations with the same initial period can give three distinct outcomes at this cut. The repeating blank-source period therefore matters. These bounds supersede the older continuation below and constrain the next opportunity only. [Earlier checkpoint](https://github.com/valu42/busycoqtesting/blob/6e9f4ea27600c34026e8d1c4eb795a7b040a6d5f/research/bb2x5/frontiers/runs/line17-epochs.json) · [Return test and proof of clock bound](../line17-edge-time.md)

The remainder documents the experiment inherited from [680c696](https://github.com/valu42/busycoqtesting/commit/680c69635d58a26ad2d33814ac16df4f72a86975).

## Outlook and provenance

**Probable halting, retaining an inherited overflow heuristic; not a new classification.**
The structural case is that a finite counting register must eventually overflow,
and its exceptional return can encounter the sole undefined instruction, **A3**.
The additional heuristic is that later reset registers continue to expose halting
return patterns with a probability bounded away from zero. It is a conjecture
about the deterministic reset sequence, not a conclusion from a large runtime.
Neither equidistribution nor independence of overflow patterns has been established.

The [full-string community page](https://wiki.bbchallenge.org/w/index.php?title=1RB2RA3LB---2LB_2LA0LA4RB0RB1LA&oldid=8484)
attributes to Racheline a halting probability of 0.2–0.35 per overflow and describes
tetrational growth. The current page was checked by its complete machine string;
its displayed revision date is 2026-09-13. Its linked
[Discord analysis](https://discord.com/channels/960643023006490684/1259770421046411285/1329809402378719273)
was not accessible through the source reader. Consequently the sampling procedure
behind those probabilities could not be audited. They remain an attributed model,
not measured probabilities established by this pass.

The inherited repository results are much more precise about the next counting
phase: [two-cell and header derivation](../frontier-background.md),
[integer mark register](../marked-register.md),
[exceptional-return branches](../research-log.md#line-17--the-next-branch-reads-two-bits),
and [exact sweep clock](../frontiers/README.md#line-17-and-the-exact-cost-of-a-header-sweep).
Their finite proofs and software checks are not Rocq/Lean certificates.

## Established facts and the new result

The literal blank execution reaches header registers of 7, 20 and 424 pairs at
raw times 252, 2,889 and 2,308,940. The first two complete 9 and 400 ordinary epochs
before exceptional epochs. For the 424-pair register, inherited mark-separation
and initial-pending checks exclude all internal A3 conflicts until the first call
to its terminal singleton. That call is guaranteed eventually; it enters the
singleton at coordinate 11 in B, and one further B2 instruction reaches virgin
coordinate 12. The subsequent return can halt, reset, or require more analysis.

The inherited exact checkpoint has completed `10^23` normal epochs, at
`140000000000000000000014538939220573301021838248` raw instructions.
This pass continued the actual saved register for **1,000,000,001 further epochs**
without a terminal call. The resulting full checkpoint is
[line17-continuation.json](line17-continuation.json), at exactly

```text
140000000000002800000017338953220573474411231282
```

defined instructions. One batch and a split into 317,801 and 999,682,200 epochs
produce identical registers, physical heads, states and raw clocks. The increase
is modest relative to the inherited floor and supplies no new overflow sample.

**New mathematical bound:** from this actual checkpoint the first visit to virgin
cell 12 occurs before **`10^405` raw instructions from blank**. Together with the
checkpoint, its time lies strictly after the displayed ~`1.4 × 10^47` floor and
below `10^405`. This is an upper bound for the **next overflow**, not an upper
bound or estimate for halting. The tighter integer computed below is approximately
`2.01792 × 10^404`.

### A slot-potential identity

For one trit, let `n` be the number of input slots, `m` the emitted slots, `C` the
number of compound pulses actually consumed, and `v,v' ∈ {0,1,2}` the initial and
final trits. The existing exact pair table gives, for every legal pulse,

```text
3m = n + v − v' + 4C.
```

For example a plain pulse at trit 2 emits one slot and changes 2 to 0; a compound
pulse at trit 1 emits two slots and changes 1 to 0. Summing the one-pulse identity
proves it for every legal finite input, including a prefix ending inside a marked
burst. Therefore

```text
m ≥ floor((n+v)/3).
```

This bound requires no probabilistic assumption, no independent residues and no
assumption that the marks are uniformly placed. It applies also with an initially
pending compound pulse. Internal-conflict exclusion for the actual register is
inherited from the source proof above; the inequality does not assert that arbitrary
registers are conflict-free.

Let `w=424` and `v_i` be the actual checkpoint's trits, ordered left to right.
Set `q_w=1` and work backwards with `q_i=3q_(i+1)−v_i`. Then `q_0` root slots
suffice for a terminal call. Equivalently,

```text
q_0 = 3^w − Σ(v_i 3^i),      D = ceil(q_0/4).
```

The header supplies exactly four root slots per epoch. Thus the first terminal
call occurs no later than epoch `K+D`, where `K` is the saved pile length. This
improves the coarse inherited `3^424` root-slot bound by using the actual trits.
The full integers are saved in [line17-results.json](line17-results.json).

### Converting that bound to raw instructions

For `D` additional successful normal epochs starting with pile length `K`, the
header and pile contribute

```text
58D + 14D(2K+D−1).
```

For the upper bound, consider a virtual completion with normal replies at the
terminal cut. An ideal responder can return A to B probes and B to A probes;
this prevents an outgoing flag conflict and completes the local calls. The real
execution and this virtual execution agree up to the first terminal call, which
is all that the bound needs. No claim of actual reachability after that call is
made.

Write `n_i` for slots entering pair `i`, `R_i` for raw probes into it and `I_i`
for its internal moves. Every slot emits at most two slots, so `n_i ≤ 4D·2^i`.
The exact local tables give `R_i ≤ 4n_i` and `I_i ≤ 6n_i`. Summing local crossings
gives `Σ(2R_i+I_i)+R_w`; the **extra final-cut term `R_w`** must be retained when
the terminal receives calls. Consequently the fixed data and cut cost at most

```text
56D(2^w−1) + 16D·2^w.
```

Adding the starting raw time `T_0` and one final real B2 move to virgin cell 12
gives the conservative upper bound

```text
T_12 ≤ T_0 + 58D + 14D(2K+D−1)
             + 56D(2^424−1) + 16D·2^424 + 1 < 10^405.
```

The individual slot identity was exhaustively checked on all 9 legal control
cases and on 1,686 valid length-12 input words. Those checks audit the algebra;
the proof is the local identity and its telescoping sum, not extrapolation from
the samples. A fresh literal blank run also checked the bound chronologically
on the earlier 7- and 20-pair registers: their next virgin-cell visits occur at
raw times **2,628** and **2,306,191**, below the corresponding conservative bounds
6,911,767 and 8,056,633,188,332,046,426. The looseness is intentional: the bound
permits far fewer propagated slots than the true marked stream often produces.

## What the actual input stream says about probability

The source at the first data cut is exactly `(0100)` repeated. This pass propagated
its complete distinguished period through the actual initial trits, retaining
the pending state and period phase. Selected complete periods were:

| Cut | Period slots | Marks | Observation |
|---:|---:|---:|---|
| 0 | 4 | 1 | Root mark is at slot 2 |
| 6 | 28 | 4 | Marks at 3, 7, 14, 23 |
| 20 | 20 | 3 | Cyclic gaps 6, 7, 7 |
| 35 | 72 | 7 | No gap divisible by 3 |
| 53 | 147,740 | 18,468 | Cyclic gaps 4–43; highly nonuniform |

These are exact period representatives, not independent random observations.
The cut-53 first marks are `5,11,17,23,27,43,49,53,62,67,75,82`. Its gap histogram
includes 4,070 gaps of length 6, 2,111 of length 4, and **no** gap of length 3.
The marginal counts of gap residues modulo three are 6,623, 6,483 and 5,362;
the full adjacent-residue matrix is recorded in the JSON. These restrictions
invalidate a Bernoulli-per-slot model of the mark stream. They do not alone
disprove a separate mixing heuristic across future *overflows*.

The important inherited obstruction remains: several artificial continuations
agree with the genuine cut-53 stream for 32 whole periods (4,727,680 slots) and
then give different exceptional returns, including a halt. The genuine stream
repeats its period forever and excludes those altered continuations. Thus finite
prefix agreement and successful halting from an auxiliary tape do not identify
the blank-tape branch.

## Conditional count quantiles and limits of the runtime model

If, **as an extra model assumption**, each future overflow halts independently
with a constant probability `p`, the number `J` of future overflows up to and
including the halting one has `P(J≤j)=1−(1−p)^j`. Applying the attributed endpoints:

| Assumed p | Median J | Central 90% interval for J |
|---:|---:|---:|
| 0.20 | 4 | 1–14 |
| 0.35 | 2 | 1–7 |

These are **conditional overflow-count quantiles**, not fitted estimates and not
raw-step quantiles. Independence is stronger than needed for eventual halting:
if every history conditional on survival has halt probability at least `ε>0`,
then survival for `j` more overflows is at most `(1−ε)^j`. No such uniform bound
has been proved for the deterministic sequence. If the relevant chance shrinks
as the register grows, even the eventual-halting prediction needs reconsideration.

For the current phase the exact raw clock has an explicit quadratic header/pile
term, with phase-dependent fixed-data work separately counted (and at most linear
for fixed width). Across successive exceptional resets,
however, neither the actual new widths nor a universal width-growth recurrence
has been established here. The community's tetrational scale is therefore an
**inherited growth conjecture**. There is no justified mapping from the count
quantiles above to raw halting-time percentiles. A mean halting time is not
reported; exponentiating random numbers of growth stages can make it misleading
or divergent even in a model that halts almost surely.

## The six investigation questions

- **Opportunity:** a terminal call ends a finite normal counting phase and
  launches the exceptional return. The many ordinary header epochs are not
  separate halting trials for this register.
- **Exact trigger:** the physical head scans symbol 3 in state A. At one studied
  suffix cut, the inherited 242- and 288-step halting continuations are exact
  local witnesses, conditional on particular suspended words.
- **Blank reachability:** the next terminal call is guaranteed and now has the
  raw-time bracket above. Reachability of a *halting return word* on blank is
  still unresolved.
- **Restrictions:** marked starts are separated; pending bursts have precise
  phases; the source is a fixed periodic stream; arbitrary admissible inputs
  include impossible continuations.
- **Probability:** the overflow-mixing hypothesis supports the inherited outlook,
  but the accessible source does not provide an auditable probability dataset.
  Exact period correlations prevent replacing the actual stream with iid slots.
- **Timing:** normal-epoch times are exact; the next overflow has an upper bound.
  Timings between *later* overflow opportunities require the unresolved reset map.

## Reproduction and next step

From the repository root, using Python 3 with assertions enabled and C++17:

```sh
c++ -O3 -std=c++17 research/bb2x5/frontiers/line17_marks.cpp -o /tmp/line17-marks
c++ -O3 -std=c++17 research/bb2x5/frontiers/window.cpp -o /tmp/line17-window
BB25_MARK17=/tmp/line17-marks BB25_WINDOW=/tmp/line17-window \
  python3 research/bb2x5/frontiers/test_line17.py
python3 research/bb2x5/halting-outlook/line17-investigate.py --engine /tmp/line17-marks
```

The inherited test suite was rerun: **7 tests passed**
([transcript](line17-tests.txt)). It checks every local pulse case, complete
literal tapes through 425 epochs, the independent 100-million-raw-step window
checkpoint, partial bursts, Python/native agreement, and stop-on-terminal
controls. The new experiment adds the actual continuation with full split
equality; [script](line17-investigate.py), [output](line17-experiment.txt),
[results](line17-results.json), and [checkpoint](line17-continuation.json) are saved.
No new accelerated transition rule was introduced. Skipped ordinary stretches
use the existing verified local paths and stop if any terminal call is detected.

The next concrete step is to compute the genuine fifth and subsequent mark
times through the long homogeneous band far enough to select the suspended word
at the first overflow. An exact event-select/rank method for the packed ternary
register would be more decisive than more small increments of the already huge
epoch count. Only after obtaining several genuine overflow resets should a
hazard model be fitted or a raw percentile estimate proposed.
