# Extending the guarded recurrence search to five more inputs

**No new machine is classified.** The guarded-block idea from [entry 26](CUBIC26.md) also applies to four existing doubling recurrences. A different, asymmetric construction handles entry 35. All counts below are iterations of the existing CubicCap certificates, not ordinary TM transitions.

## Existing models and exact input mapping

The starting definitions are BusyCoq's existing [CubicCap.v](../../verify/CubicCap.v), at branch base `cfa10a0be34ed9404dadc59b95cc5737a423807d`. The recurrence definitions, configurations, and original proof tactics are credited to its authors. This work adds native batching and checks its arithmetic arguments; it does not claim to have discovered the underlying recurrences.

| Supplied entry | Existing certificate | Orientation used by simulator | Initial `(a,b,c)` |
| --- | --- | --- | --- |
| 35 | `WF17` | supplied table | `(3,0,0)` |
| 138 | `WF35` | reflected supplied table | `(0,1,1)` |
| 269 | `WF32` | reflected supplied table | `(0,1,0)` |
| 409 | `WF36` | reflected supplied table | `(0,0,1)` |
| 494 | `WF33` | reflected supplied table | `(2,2,1)` |

The exact tables are embedded in the simulator and each checkpoint. [ResearchCubicModels.v](../../verify/ResearchCubicModels.v) checks the four reflected mappings in both directions. Entry numbers refer to the user's 623-machine ordering.

The optimized original `WF` proofs depend on `Uint63` specifications. `ResearchCubicModels.v` extracts only their **definitions**, and rechecks the five natural-number models using the original execution tactics. Its `completed_run` theorem gives a blank-start execution bridge for every finite recurrence run, or a halting conclusion when that run returns `None`. The ten printed reports have closed assumptions. This is a reuse of existing local TM arguments, not a new blank-run classification, and no converse termination theorem is claimed here.

## Four doubling models

One scalar certificate iteration first bounces

```text
i = min(a div 2,c)
(a,b,c) -> (a-2i,b+2i,c-i)
```

and then applies its model's finite boundary cases. The native scalar function preserves every exceptional case, including halting. In the regular region, let `N=a+2b+2c`. The two composite branches are

```text
L: a' = 2a+2b+ell,     b'=bl,  N'=N+2-(a mod 2)
R: a' = 2a-N+2b-4,     b'=2,   N'=N+2.
```

The parameter pairs `(bl,ell)` are `(1,2)`, `(2,2)`, `(0,4)`, and `(0,2)` for `WF32`, `WF33`, `WF35`, and `WF36`. A fixed-`N` ideal doubling orbit supplies a branch word and final residue `r=(2^k*a) mod N`. Corrections depend only on the starting `b`, parity of `a`, and branch word. The six correction tables contain `6*2^k` signed 32-bit entries.

The accepted-batch guard is

```text
r >= 6*2^k  and  N-r >= 8*2^k.
```

Writing real coordinates as `(x+C,N+D)`, every prefix satisfies

```text
i <= D_i <= 2i
-6*2^i+2i+6 <= C_i <= 8*(2^i-1).
```

These inequalities justify the true regular branch at every prefix. An unsuccessful guard executes one scalar iteration. The abstract argument is proved in `CubicFamilyDoubling` in [ResearchCubicFamilyJump.v](../../verify/ResearchCubicFamilyJump.v).

An informative common form is `A=a+b+v`, `M=N+v+2`, with `v=ell+bl`. On the even regular region, the maps become `A'=2A` or `A'=2A-M`, with `M'=M+2`. This does **not** identify the exceptional cases or the blank orbits of the four machines.

## Entry 35: mixed slopes instead of doubling

Here the bouncer removes three units from `a` for one from `c`. Normalize `b` to 0 or 1 and put `N=a+2b+c`, `a=3q+r`. The regular left events are:

| `r` | `a'` | `b'` | `c'` | Increase in `N` | Certificate iterations |
| --- | --- | --- | --- | --- | --- |
| 0 | `4q+2b+1` | 0 | `c-q-1` | 0 | 1 |
| 1 | `4q+2b+5` | 0 | `c-q-2` | 2 | 1 |
| 2 | `4q+2b+7` | 0 | `c-q-2` | 3 | 2 |

These rows hold when `q>=1` and `c-q>=2`. The right event, valid for `a-3c>=3`, is

```text
(a,b,c) -> (a-3c-2, 1, 3+2b+4c),   N'=N+3.
```

The boundary `a-3c=2` halts after two certificate iterations. [ResearchCubicFamily.v](../../verify/ResearchCubicFamily.v) checks the bouncer, all four normalized events, and this boundary directly against the natural-number definitions; its seven printed reports are closed.

The ideal branches now have slopes **4/3 and 4**, meeting at `a=3N/4`. For a word of `k` events containing `L` left branches, its ideal map is

```text
x = (4^k*a-B*N)/P,  where P=3^L.
```

Starting with `(B,P)=(0,1)`, a left branch sends `(B,P)` to `(4B,3P)` and a right branch to `(4B+3P,P)`. Thus that word's interval is `[B/4^k,(B+P)/4^k)`. A `4^k`-entry directory chooses the word from `floor(4^k*a/N)`.

For each word, the exact correction, increase of `N`, and number of certificate iterations depend only on `b`, `a mod P`, and `N mod max(1,P/3)`. The five-event default stores 66,668 correction records, about 533 KB, plus its directory. Odd-denominator modular inversion gives the exact division by `P`; quotient/remainder decisions use integer arithmetic.

The batch is accepted only if

```text
3*4^k <= x  and  4^k <= N-x.
```

The rational shadow argument bounds the errors by `0<=D_i<=3i` and `-3*4^i+3i+3<=e_i<=3*(4^i-1)`. Pulling the margins backward proves the required regular branch at every prefix. `CubicFamilyAsymmetric` in `ResearchCubicFamilyJump.v` proves this argument. Together the two arithmetic modules have four closed printed reports. Their hypotheses explicitly describe the shadow trace; they do not verify the C++ table generator.

Larger blocks were not automatically faster. Pilot tests favored five events over three, four, six, and seven. Batching only consecutive sweeps was also slower. Fixed block sizes give constant-factor improvements over recurrence simulation, not an exponential shortcut through these recurrences.

## Validation and measurements

[cubic_family_validate.py](cubic_family_validate.py) independently translates the original natural-number pattern matches using Python integers and compares configurations with an ordinary coordinate-tape TM interpreter.

- 5,915 small triple comparisons, all checked against ordinary TM execution, including 191 halting cases. Blank-entry checks require 8, 7, 5, 5, and 27 raw transitions for the table order above.
- One million Python recurrence iterations for each of the five starts, with complete triple comparisons against both native modes.
- One million accepted doubling blocks and 657,456 accepted asymmetric blocks checked against scalar execution, plus four million-step doubling orbits.
- Extra block-width checks at three, six, and eight asymmetric events; a three-to-six-event checkpoint resume; and four artificial large-counter orbits checked against Python through the 128-bit division path. These artificial configurations are not claimed reachable from blank.
- Split checkpoint runs, changed block widths, malformed inputs, terminal controls, and integer/time limits. The native/Python suite also passes with undefined-behavior sanitization.

[cubic_family_results.json](cubic_family_results.json) records measured scalar/accelerated billion-iteration comparisons and longer runs. Both backends reach the same complete triple in every benchmark. Timings are measurements on this host, include simulation only, and vary with other running jobs; they are not comparisons against another author's implementation. Checkpoints preserve all five long-run states for continuation.

The long searches completed without a halt:

| Entry | Certificate iterations | Final `(a,b,c)` | Cumulative simulation seconds |
| --- | ---: | --- | ---: |
| 35 | 1,000,000,000,000 | `(1456783997093,0,143215903080)` | 3674.270 |
| 138 | 100,000,000,000 | `(48338543900,0,75830728075)` | 139.338 |
| 269 | 100,000,000,000 | `(159466687122,1,20266656441)` | 139.458 |
| 409 | 100,000,000,000 | `(192643925654,0,3678037175)` | 138.473 |
| 494 | 100,000,000,000 | `(174667235660,2,12666382201)` | 138.295 |

These native results leave every target unknown. The entry-35 run used the first billion scalar iterations as its seed, then the asymmetric table for the remaining 999 billion.

## Reproduction and scope

```sh
g++ -O3 -march=native -std=c++17 -Wall -Wextra -Wconversion research/holdouts-623/cubic_family.cpp -o /path/to/cubic_family
python3 research/holdouts-623/cubic_family_validate.py /path/to/cubic_family
/path/to/cubic_family --entry 269 --iterations 100000000000 --seconds 300 --checkpoint /path/to/269.checkpoint
/path/to/cubic_family --entry 35 --events 5 --iterations 1000000000000 --seconds 5000 --checkpoint /path/to/35.checkpoint
/path/to/cubic_family --entry 35 --resume /path/to/35.checkpoint --iterations 1000000000 --seconds 30 --checkpoint /path/to/35.checkpoint
```

`--iterations` is an **additional** certificate-iteration budget. `--bits` selects 1–24 doubling steps; `--events` selects 1–8 asymmetric events; `--scalar` disables blocks. A two-iteration event is never counted as one iteration. Checkpoints are atomically written about every 30 seconds and at exit. Their identities, ranges, and count consistency are checked on reload; this does not prove reachability. Native counters have explicit conservative 64-bit limits and are not arbitrary precision.

With the usual BusyCoq dependencies built:

```sh
coqc -native-compiler no -Q verify BusyCoq verify/ResearchCubicModels.v
coqc -native-compiler no -Q verify BusyCoq verify/ResearchCubicFamily.v
coqc -native-compiler no -Q verify BusyCoq verify/ResearchCubicFamilyJump.v
coqchk -silent -bytecode-compiler yes -Q verify BusyCoq BusyCoq.ResearchCubicModels BusyCoq.ResearchCubicFamily BusyCoq.ResearchCubicFamilyJump
```

The native tables, integer implementation, and long runs remain **unverified**, with `"verified": false` in every result. A native halt needs proof replay. Time, iteration, or integer exhaustion is an unknown result, and no certified raw-step bound is asserted. AI-assisted implementation and additional arithmetic proofs by Codex.
