# Lines 29 and 30: drift away from halting, with a timed Hydra replay

Research pass: **2026-11-18**. Repository baseline:
`2ab106f706cb1715d494c7f67464e9222092058f`.

| Line | Exact encoding | Outlook in this pass |
|---:|---|---|
| 29 | `1RB3RB---3LA1RA_2LA3RA4LB0LB1LB` | Probable nonhalting; heuristic |
| 30 | `1RB3RB---3LA1RA_2LA3RA4LB0LB0LA` | Probable nonhalting; heuristic |

Neither is proved nonhalting. Their **different final instructions matter**.
The repository's old accelerator table labels the finite simulations “Unknown”;
the outlook above additionally incorporates the published drift arguments.

## Inherited facts and attribution

Daniel Yuan identified Hydra and the Bonus Cryptid. Shawn Ligocki's
[primary analysis](https://www.sligocki.com/2024/05/10/bb-2-5-is-hard.html)
gives the reductions and the biased-walk interpretation. The
[Hydra wiki, revision 5250](https://wiki.bbchallenge.org/w/index.php?title=Hydra&oldid=5250)
includes timed rules and reports four million arithmetic events without a halt,
ending at counter value 2,005,373. The
[Bonus Cryptid wiki, revision 9314](https://wiki.bbchallenge.org/w/index.php?title=Bonus_Cryptid&oldid=9314)
reports at least `10^13634` raw steps, plus a later 100-million-event run from a
reported large normal form. These external endpoints were **not replayed here**.
All three sources identify the complete strings above; they still describe open
problems on this research date. No formal proof of either eventual outcome was
found in these sources.

<a id="line-30"></a>

## Line 30: exact opportunities and timing

Use `C(a,b)=0^∞ [A on 0] 2 0^a 3^b 2 0^∞`, with the head on the blank
immediately left of the first 2. This is the wiki's C convention; it differs by
one instruction from the primary article's B-head convention. Literal execution
reaches `C(3,0)` after **20** defined instructions, with first 2 at coordinate −3.

The inherited timed rules, independently checked below, are:

| Condition | Result | Defined instructions |
|---|---|---:|
| `a=2n, b=0` | physical `A2`, halt | `6n²+20n+4` |
| `a=2n, b>0` | `C(3n+3,b−1)` | `6n²+23n+10` |
| `a=2n+1` | `C(3n+3,b+2)` | `6n²+23n+4b+26` |

Each nonhalting return shifts the first 2 left by `n+2` cells. These rules cover
every nonnegative parameter pair; their published sweep derivation accounts
for all intermediate instructions. The new program checks the halt guard before
each return. It never replaces a sequence by a guessed recurrence fit.

Each return tests a new opportunity, but halting is possible only when `b=0`
and `a` is even. With `O_N,E_N` the odd/even branch counts, the running counter
is exactly `b_N=2O_N−E_N`. The actual orbit visits zero early (including after
three rules), but all observed zero states have the safe odd parity. An even
zero state is realizable on other starting tapes; this alone says nothing about
its reachability from blank. Resolving the blank orbit requires controlling the
cumulative parity imbalance, not just individual residue classes.

For the raw clock, `a_{j+1}=3a_j/2+c_j`, with `c_j` either 3 or 3/2.
Consequently `3(3/2)^j ≤ a_j ≤ 9(3/2)^j−6`, and `0≤b_j≤2j` on a surviving
prefix. The timed rules imply that the accumulated raw time through `N` returns
is `Θ((9/4)^N)`. This is a proved growth scale **conditional on the number of
surviving returns**, not a prediction of the halting event count.

## New bounded computation and verification

Run from repository root:

```sh
python3 research/bb2x5/halting-outlook/hydra_check.py --events 20000
```

[Program](hydra_check.py), [full exact checkpoint and statistics](hydra-results.json),
[verification output](hydra-verification.txt). Integer fields use hexadecimal.
The checkpoint records both counters, the absolute first-2 and head coordinates,
state, and exact raw time, so it specifies the entire finite nonzero tape.

* Every rule for `0≤a<40, 0≤b<8` was compared with the literal interpreter:
  **320 complete tape/head/state/raw-time comparisons**, including 20 physical
  halting positive controls. No skipped interval in these checks hides a halt.
* Blank execution was compared at all first **12** returns, through
  **1,069,506** literal instructions, including absolute positions.
* The timed recurrence from blank completed **20,000** returns with `b=9,889`,
  an 11,703-bit `a`, and an exact raw time strictly between `10^7045` and
  `10^7046`. Thus **`≥10^7045` raw instructions** is a new reproducible repository
  floor for line 30. It is much shallower in event count than the community run.

The old exact repository endpoint was only 4,121,120,989 raw steps. The new floor
depends on the published all-parameter recurrence argument plus this checked
implementation; it is **not kernel-verified in Rocq or Lean**.

Actual branch observations, rather than synthetic tapes, give:

| Event block | Odd | Even | Counter after block |
|---|---:|---:|---:|
| 1–10,000 | 4,942 | 5,058 | 4,826 |
| 10,001–20,000 | 5,021 | 4,979 | 9,889 |

Across all 19,999 adjacent pairs, counts `(EE,EO,OE,OO)` are
`(5040,4996,4997,4966)`. All 16 length-four patterns occur (counts 1,209–1,290).
Pearson correlations at lags 1,2,3,4,8,16,32 are respectively approximately
`0.00064, −0.00051, −0.00456, −0.00982, −0.00161, −0.00412, 0.00239`.
The second block checks the same qualitative prediction on a subsequent part
of the actual execution. This small early sample cannot establish independence
or exclude a rare future coherent block.

## Why the heuristic is substantive, and why it is not a theorem

Assume future parities act as independent fair bits, even conditional on survival
and the current counter. Then `b` takes steps −1 and +2 with equal probabilities,
so its mean increment is +1/2. The chance of ever reaching −1 from `b` is
`r^(b+1)`, where `r=(sqrt(5)−1)/2`: substituting `q(b)=r^(b+1)` into
`q(b)=(q(b−1)+q(b+2))/2` yields the formula. It is a model probability about
unknown deterministic digits, not randomness physically present in the machine.
Positive drift and the large actual counter explain “Probable nonhalting.”

There is an exact finite arithmetic reason to consider this model: the first
`k` parities under `F(a)=3 floor(a/2)+3` depend only on `a mod 2^k`, and each
binary word occurs for exactly one residue. Indeed the first parity chooses one
of two lifts, and after fixing it, the next iterate acts on the remaining bits
by an affine map with odd multiplier 3, hence a permutation. Induction proves
the assertion. Restricting the starting `a` to a multiple of 3 does not change
the uniform residue ensemble, since 3 is invertible modulo powers of 2.
The script exhaustively checks `k=1,…,12` as a check of the implementation.

This theorem concerns **varying seeds**, not the single seed `a=3` on blank.
It proves there are no universally forbidden finite parity words in that ensemble,
but does not prove the seed's later words are uniformly distributed or independent.
Long-range correlations or deterministic residue restrictions specific to this
orbit remain the main mathematical obstacle. No unconditional finite halting-time
median exists under the model once its nonhalting probability exceeds 1/2, and no
conditional halting-time percentile is calibrated here.

<a id="line-29"></a>

## Line 29: related drift with an exceptional branch

In the primary article's form `D(a,b)=0^∞ [B on 0] 0^a 3^b 2 0^∞`, the
published ordinary transitions are
`(3n,b>0)→(4n+3,b−1)`, `(3n+1,b)→(4n+3,b+3)`, and
`(3n+2,b>0)→(4n+5,b−1)`. The `b=0,a≡0 (mod 3)` case halts;
`b=0,a≡2 (mod 3)` leaves this simple ordinary description and must not be
silently declared a halt. Such exceptional branches occurred in the actual
early run. The reported later start is `D(1287547464911049659,10)`.

If future ternary branches are independent and uniform, counter increments are
−1 with probability 2/3 and +3 with probability 1/3, giving positive drift +1/3.
This corrects a possible misreading of the phrase “biased towards traveling away”:
downward steps are more frequent, but upward steps are larger. The probability
of ever returning to zero from counter `b` in that model is `r^b`, where `r` is
the unique root in `(0,1)` of `r^4−3r+2=0`. Reaching zero is only a prerequisite
to a possible halt, so that return probability bounds the modeled halt probability.
The reported large counter supports a probable-nonhalting heuristic; its uniform,
independent ternary-branch assumption has **not** been verified for the actual
long orbit here. No new line-29 floor or timed recurrence is claimed.

## Next concrete steps

For line 30, extend parity diagnostics using the published divide-and-conquer
integer method while retaining the **minimum prefix counter**, not only the final
counter; endpoint-only acceleration could conceal a halt. Develop a joint summary
for exact raw cost and prefix deficit, and compare it with this scalar program.
For line 29, independently replay the published large-start certificate and derive
complete timed rules for its exceptional zero-counter branches before estimating
any conditional raw stopping-time distribution.
