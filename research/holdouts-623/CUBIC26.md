# Accelerated halting search for entry 26

Target: `1RB1LC_1LC1RD_1LA0LB_0RB1RE_1RF0RA_---0RC`, entry 26 in the supplied ordering, sometimes called Cubic Mess. This pass follows the request to concentrate on a potentially probviously halting machine and accelerate its simulation.

**No halt has been found.** The new guarded block simulator is about **13 times faster** than a compiled scalar implementation of the published recurrence in the benchmark below. This is a constant-factor improvement, **not an exponential improvement over existing recurrence simulation**, and no claim of a literature-first algorithm or simulation record is made.

## Starting point and attribution

[Racheline's analysis, as recorded on BusyBeaverWiki](https://wiki.bbchallenge.org/w/index.php?title=1RB1LC_1LC1RD_1LA0LB_0RB1RE_1RF0RA_---0RC&oldid=6856), supplies the two-counter recurrence. The page calls the machine potentially probviously halting with exponential runtime and reports that Bricks simulated these rules for `8e11` iterations. That reported run is the comparison point, not a verified upper bound on all previous work. The source was checked on 2026-10-25.

Write `A(a,b)` for the configuration with tape `0^inf 1^a 0 C> 1^b 0^inf`. The blank start reaches `A(2,9)`. The following domain is invariant:

```text
a >= 1, b >= 2, a+b >= 11.
```

Within it, the rules are:

| Condition | Next pair |
| --- | --- |
| a even, b >= a+3 | (2a+4, b-a-1) |
| a odd, b >= a+4 | (2a+3, b-a) |
| a odd, b = a+3 | (2a+1, 9) |
| b = a+2 | (1, 2a+7) |
| b = a+1 | (4, 2a+4) |
| a >= b >= 4 | (a-b+1, 2b+3) |
| b = 3 | halt |
| b = 2 | (a-3, 7) |

The domain supplies the additional lower bounds needed by the small-boundary cases. Rules are not asserted for arbitrary tiny configurations outside it. The original recurrence already replaces long ordinary TM computations; that acceleration is credited to the existing analysis.

## New acceleration: compose regular branches using a guarded doubling word

Let `N=a+b`. Away from the exceptional cases, there are only two forms:

```text
L: a' = 2a + 4 - (a mod 2),  N' = N+3
R: a' = 2a - N + 1,          N' = N+4
```

Temporarily hold `N` fixed and double `a` modulo `N`. In `k` such ideal steps, the binary branch word and final residue are

```text
B = 2^k
word = floor(B*a/N), written with exactly k bits, most significant first
r = (B*a) mod N.
```

The real run differs from this ideal run by additive corrections. After a prefix, write the real coordinates as `(x+C,N+D)`, where `x` is the ideal residue. Starting at `C=D=0`, update the corrections as follows:

```text
L: C' = 2C + 4 - pa,  D' = D+3
R: C' = 2C - D + 1,   D' = D+4
```

Only two parity bits are needed. Here `pa` and `pn` are the parities of the current real first counter and real sum:

```text
L: pa' = pa,    pn' = 1-pn
R: pa' = 1-pn,  pn' = pn.
```

Thus all `2^k` words can be tabulated for each of the four starting parity states. The final increment is `D=3k+popcount(word)`. A lookup supplies `C`.

An ideal word is **not automatically the real itinerary**. Accept the entire batch only when

```text
r >= 3B  and  N-r >= 4B.
```

Then the result is exactly

```text
a' = r+C,  N' = N+D,  b' = N'-a'.
```

Otherwise execute one scalar recurrence iteration, checking all exceptional and halting cases. The guard concerns every intermediate step, so checking only the endpoints for a halt is not being substituted for a sound batch condition.

### Why the guard works

For every prefix of length `i`, the correction recurrence gives

```text
3i <= D_i <= 4i
-3*2^i + 4i + 3 <= C_i <= 4*(2^i-1).
```

These bounds hold for every branch word. Pulling the final guard backwards through ideal doubling yields `x_i >= 3*2^i` and `N-x_i >= 4*2^i` at every prefix. Consequently `a_i=x_i+C_i >= 4i+3`.

On an ideal L branch, the upper margin at the following prefix gives `N-2x_i >= 8*2^i`. The bound on `C_i` then gives `N_i-2a_i >= D_i+8 >= 4`, so the true rule is regular L for either parity.

On an ideal R branch, the lower margin at the following prefix gives `2x_i-N >= 6*2^i`. The lower correction bound gives `2a_i-N_i >= 8i+6-D_i >= 0`. The current upper margin also gives `b_i=N_i-a_i >= D_i+4 >= 4`, so the true rule is regular R. None of the exceptional rules, including halting, occurs inside an accepted batch.

Table construction costs `O(2^k)` time and space. A batch uses exact integer division, one correction lookup, and a population count. Fixed `k` gives a constant-factor speedup. The correction bounds grow as `2^k`; this argument does not permit skipping an arbitrary exponentially large number of recurrence iterations with a small fixed table.

## Formal scope

[ResearchCubic26.v](../../verify/ResearchCubic26.v) proves the blank-start bridge, all eight recurrence cases, preservation of the stated domain, and a two-way equivalence between TM halting from blank and eventual termination of the recurrence. It uses BusyCoq's existing semantics and execution tactics. The nine public local rules and the two complete recurrence statements report closed assumptions.

[ResearchCubic26Jump.v](../../verify/ResearchCubic26Jump.v) separately proves the abstract integer-arithmetic guard theorem. `guarded_jump` says that an ideal doubling trace with its correction recurrence and the final margins represents exactly `k` regular steps. `shadow_remainder` identifies the ideal final residue with modular doubling; `parity_rules` checks the four-state parity update. These statements also report closed assumptions.

The native lookup-table generator, integer implementation, checkpoint provenance, and the connection of its entire long execution to a Coq proof term are **not verified**. The abstract guard proof is not a claim that the native executable was extracted or fully certified. No certified raw-TM-step bound or blank-run classification is asserted. Every native result includes `"verified": false`; a native halt would be a candidate requiring proof replay.

After building the usual dependencies, from the repository root:

```sh
coqc -native-compiler no -Q verify BusyCoq verify/ResearchCubic26.v
coqc -native-compiler no -Q verify BusyCoq verify/ResearchCubic26Jump.v
coqchk -silent -bytecode-compiler yes -Q verify BusyCoq BusyCoq.ResearchCubic26 BusyCoq.ResearchCubic26Jump
```

## Implementation and validation

```sh
g++ -O3 -march=native -std=c++17 -Wall -Wextra -Wconversion research/holdouts-623/cubic26_accel.cpp -o /path/to/cubic26_accel
python3 research/holdouts-623/cubic26_validate.py /path/to/cubic26_accel
/path/to/cubic26_accel --bits 11 --iterations 1000000000000 --seconds 900 --checkpoint /path/to/run.checkpoint
/path/to/cubic26_accel --bits 11 --resume /path/to/run.checkpoint --iterations 1000000000000 --seconds 900 --checkpoint /path/to/run.checkpoint
```

`--iterations` is an **additional** recurrence-iteration budget; it never means ordinary TM steps. `--scalar` disables batching. `--bits` accepts 1 through 24; the default is 14, while 11 performed better at the later checkpoint on this host. Four 32-bit correction tables require `16*2^k` bytes. All branch decisions use exact integer arithmetic, including 128-bit division when the shifted numerator exceeds 64 bits. No floating estimate decides a branch.

Checkpoints are atomically replaced approximately every 30 seconds and at exit. They contain a format tag, the exact machine table, `a`, `b`, total iterations, jump counts, scalar counts, and elapsed time. Resume checks identity, the supported domain, counter consistency, integer syntax, and trailing input. This is format validation, not a reachability certificate. Time checks are periodic and may slightly overshoot the requested wall-clock budget; table construction is outside the measured simulation time.

The implementation deliberately stops before the sum approaches `UINT64_MAX/8`, leaving room for the largest possible next update and preserving a resumable checkpoint. It is not an arbitrary-precision simulator. Exhausted iteration, time, or integer limits remain unknown results.

Validation completed:

- 2,806 independent ordinary-TM comparisons covering small configurations in the domain, including 42 halting cases; full tape and state comparisons, with up to 5,429 ordinary transitions per case. The blank-entry bridge took 52 transitions in this test.
- 12,030,650 accepted local jumps compared against scalar execution, including exhaustive small domains for widths 1 through 8 and sampled large integers exercising the 128-bit path.
- One million blank-orbit iterations compared with an independently ordered Python recurrence using unbounded integers.
- A split 100-million plus 100-million run, changing block width between segments, matched an uninterrupted 200-million run. Zero-iteration resume, malformed checkpoints, identity mismatches, terminal reporting, time exhaustion, and resumable integer exhaustion were checked.
- The full native/integration validation suite passed under the undefined-behavior sanitizer. Both Coq files compile with Coq 8.20.1 and pass independent kernel checking; all 15 printed assumption reports are closed.

## Measurements and continuation

For the first billion recurrence iterations, both backends ended at `(990401271,2509600633)`:

| Backend | Measured simulation seconds |
| --- | ---: |
| Compiled scalar recurrence | 8.094683135 |
| Guarded table, k=14 | 0.620498821 |

The ratio is 13.05. These are measurements on this host, not a comparison against the speed of Bricks' implementation. Later block-width tests favored `k=11`. Bigger flat tables, composed eight-bit tables for longer words, and two reciprocal-estimate implementations were tested; they were slower and are not retained. The final implementation uses ordinary exact division.

The first trillion iterations completed in 628.657 cumulative simulation seconds. Two trillion completed in 1202.745 seconds. The final run reached **four trillion recurrence iterations**, at `(7354046713435,6645952891241)`, without a halt. Cumulative simulation time was 2348.694 seconds, about 39 minutes. This is five times the wiki's reported `8e11` recurrence iterations, but has not established eventual halting or nonhalting.

[cubic26.checkpoint](cubic26.checkpoint) preserves the final counter state for `--resume`; [cubic26_results.json](cubic26_results.json) records the benchmarks, milestones, and validation summaries. The checkpoint is a native experimental result, not a Coq certificate.

The remaining challenge is a way to compose substantially longer itineraries without an exponentially sized table, or a structural argument determining the blank orbit. No random-orbit heuristic is used as a proof.

AI-assisted research and implementation by Codex; the underlying recurrence is credited to Racheline and the prior reported simulation to Bricks.
