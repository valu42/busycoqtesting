# BB(2,5) holdout research

**[Machine decision roadmap and agent claim board](ROADMAP.md)** · [Simulation table for all 37 holdouts](SIMULATION_TABLE.md) · [Run and resume the simulators](frontiers/README.md)

These notes record results on the November 3, 2026 list of 37 formal holdouts. Each machine is identified by its full transition string. All line numbers here are **one-based positions in that exact file**. The scripts use an initially blank, two-way infinite tape, state A and head coordinate zero. An undefined instruction halts on arrival. Line 36 has a kernel-checked Rocq proof of blank-tape nonhalting. [Formal theorem and build instructions](line36-rocq.md) · [Proof and reproduction](line36-nonhalting.md) · [Reduced certificates and verification](line36-cap-blocks.md)

| Formal line | Machine | Result to continue from |
|---:|---|---|
| 17 | `1RB2RA3LB---2LB_2LA0LA4RB0RB1LA` | The first visit to coordinate +12 occurs after 1.4 × 10⁵⁹ and before 3.176 × 10³⁴⁴ elementary steps. At 10²⁹ sweeps the deepest pair reached is 175. The return depends on whether cut 418 marks slot 9 or 10. [Two-bit decision and bounds](line17-edge-time.md) · [First-visit tapes](frontiers/README.md#line-17-first-arrivals-inside-a-sweep) |
| 13 | `1RB3RA3RB4LA1LA_1LB2LA1LA---1RB` | A halt requires an odd coordinate to receive an initial positive even number of B entries followed by A. Every odd coordinate below 155 is permanently clear. [Edge test and blank-orbit traces](line13-edge.md) |
| 26 | `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA` | The blank machine halts exactly at the least fixed point of a monotone integer function. All widths through 204 are excluded. The [record-gap criterion and exact checkpoint](column-records.md) reach 204 pairs after 181,912,616,417,007,775,091,148,375 instructions. [Bounds and calendar](column-phases.md) · [Halting permutations](column-traps.md) · [Exact carry accounting](column-reserve.md) |
| 2 | `1RB---4LB0LA4RA_2LB2LA3RA4LB0RB` | A fixed-cut protocol replaces the growing left half. The negative prefix is exact through 2,400 extensions from blank. |
| 10 | `1RB2RB3LA4LA1LA_2LB3RA---4RA1RB` | Three leading A entries at the fresh edge halt. Cyclic period counts are known. The starting position matters. |
| 3 | `1RB---0RB0LA2RA_2LB2LA3RA4LB0LB` | The 320th zero-counter checkpoint is at about 3.09717 × 10³¹² defined steps from blank. Higher reset branches remain open. [Exact mixed-counter clock](frontiers/line3-timing.md) |
| 35 | `1RB2LA4RA1LA3LA_0LA3RB3LB2RB---` | Adding one opening transfers the line 37 right edge. A growing suffix follows Pascal's recurrence with constant boundary bit one. The left guard remains open. [Proof and checks](line35-pascal.md) |
| 36 | `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---` | **Runs forever from blank.** Two integer certificates keep every sweep away from B4. [Rocq theorem](../../verify/Line36Nonhalting.v) · [Proof](line36-nonhalting.md) |

The first four rows are developed in [the research log](research-log.md). The earlier [frontier derivations](frontier-background.md) give the raw pair tables and the initial blank checkpoint. The [mixed-counter and sweep notes](mixed-and-sweeps.md) also record results on lines 12, 21 and 22 and list the exact identities used for the left-half certificates.

The [integer-register derivation](marked-register.md) proves the line-17 running-time bound and describes the remaining branch question. The [column-frontier derivation](column-frontier.md) gives the line-26 fixed-point criterion and a safety bound between width increases. The [parity-sweep derivation](parity-bulk.md) proves eventual global parity uniformity for the boundary-free line-36 data dynamics.

The [line-4 scalar return map](line4-scalar.md) verifies one million returns from blank and a lower bound of $10^{1,719,137}$ defined steps. The [six-phase line-36 tilings](line36-tiles.md) describe a growing prefix observed on blank, and the [right-boundary bound](line36-right-cap.md) controls part of the matching debt. The [line-37 stream recurrence](line37-stream.md) gives an exact blank halting test, with [a finite splicing example](line37-splice.md) showing how an altered tape can shadow the same cuts. On line 6, the [word recurrence](line6.md) gives a halting test on successive left extensions.

From the repository root, run these checks with Python 3.10 or later, with assertions enabled. They use only the standard library.

```sh
cd research/bb2x5
python3 verify.py
python3 mixed_and_sweeps.py
python3 marked_register.py
python3 column_frontier.py
python3 column_phases.py
python3 parity_bulk.py
```

The [C++20 gap check](column-frontier.md#computing-p71-without-replaying-the-root-clock) independently evaluates the next fixed-point iterate from two cuts.

Expected output is in [verification.txt](verification.txt), [mixed-verification.txt](mixed-verification.txt), [marked-verification.txt](marked-verification.txt), [column-verification.txt](column-verification.txt) and [parity-verification.txt](parity-verification.txt). The direct interpreters and word rules live in `prior_sweeps.py` and `prior_frontier.py`. The tests distinguish the actual blank orbit, exact implications for auxiliary configurations, and experiments with freely chosen inputs. In particular the 242-step line-17 halting continuation agrees with a long prefix of the blank stream, then diverges from its fixed period.

The data file is [BB2x5_Rocq_holdouts_37.txt](BB2x5_Rocq_holdouts_37.txt). Its SHA-256 is `89ea92fd4643166b92fca4ae80e37a699ab8615ac1dd375dae777e6b3e45ecc6`. The notes credit the original community analyses at the relevant derivations. [Published list](https://wiki.bbchallenge.org/w/images/c/cc/BB2x5_Rocq_holdouts_37.txt) · [Community status](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved)
