# BB(2,5) simulation table

Each row starts on the all-zero, two-way-infinite tape. One raw step is one defined Turing-machine instruction. Line 36 runs forever by the [blank-tape proof](line36-nonhalting.md).

The endpoint column gives the largest exact raw count indexed in this repository. Follow its source for the full integer and configuration or run record. ≈ marks a shortened display. Bounds, externally reported simulations and exact repository counts have separate columns.

| Line | Machine in the November 3 list | Raw steps at exact endpoint | Additional raw lower bound | Other reported raw steps | Endpoint source |
|---:|---|---:|---:|---:|---|
| 1 | `1RB---4LB1RA4RA_2LB2LA3RA4LB0RB` | 10,000,000,000 | — | — | [Moving window](frontiers/runs/window-01.json) |
| 2 | `1RB---4LB0LA4RA_2LB2LA3RA4LB0RB` | 10,000,000,000 | — | — | [Moving window](frontiers/runs/window-02.json) |
| 3 | `1RB---0RB0LA2RA_2LB2LA3RA4LB0LB` | ≈ 3.09717 × 10^312 | [≥ 10^151](mixed-verification.txt) | — | [Timed mixed-counter probes](frontiers/runs/line3-timed.json) |
| 4 | `1RB3LA1LA1RA3RA_2LB2RA---4RB1LB` | ≈ 5.35561 × 10^1802 | [> 10^1,719,137](line4-scalar.md) | — | [Timed A(6,b) returns](frontiers/runs/line4-return.json) |
| 5 | `1RB3LA1LA1RA1RA_2LB2RA---4RB1LB` | ≈ 1.99499 × 10^104610 | [≥ 2^173,753](accelerator-results/arithmetic5-100k.json) | — | [Timed A/B returns](frontiers/runs/line5-timed.json) |
| 6 | `1RB---3LB4RB0LA_2LB3LA3RB4RA0RA` | 10,000,000,000 | — | — | [Moving window](frontiers/runs/window-06.json) |
| 7 | `1RB---3RA2LA2RB_2LB3LA4LB4RA0RA` | ≈ 5.69453 × 10^3872 | — | [> 10^1,140,000,000](https://wiki.bbchallenge.org/wiki/TMBR:_October_2026#Holdouts) | [Batched suffix calls](frontiers/runs/line7-calls.json) |
| 8 | `1RB4LA1RA1RB1LA_2LB3LA---4RA2RB` | ≈ 1.50000 × 10^57 | — | — | [Boundary streams](frontiers/runs/stream-08.json) |
| 9 | `1RB---4RB2RB4LA_2LB3LA3LB0RA0RB` | 6,755,400,984,549,769 | — | — | [Batched BBA sweeps](frontiers/runs/line9-sweeps.json) |
| 10 | `1RB2RB3LA4LA1LA_2LB3RA---4RA1RB` | ≈ 2.10250 × 10^22 | — | — | [Boundary streams](frontiers/runs/stream-10.json) |
| 11 | `1RB2LA4LA1RA1LA_2LB3RB4RB---2RA` | ≈ 2.81543 × 10^50 | — | — | [Boundary streams](frontiers/runs/stream-11.json) |
| 12 | `1RB4RB4RA1LA3LA_1LB2LA3RB2RB---` | ≈ 2.67029 × 10^82 | — | — | [Boundary streams](frontiers/runs/stream-12.json) |
| 13 | `1RB3RA3RB4LA1LA_1LB2LA1LA---1RB` | ≈ 1.50000 × 10^35 | — | [≈ 10^17.50888](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved) | [Boundary streams](frontiers/runs/stream-13.json) |
| 14 | `1RB2RA4LA1RB4RB_1LB2LA3RA---0LB` | 1,000,000,000,000,000 | — | [≥ 5 × 10^13](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved) | [Six-cell strides](frontiers/runs/stride-14.json) |
| 15 | `1RB3RB1LA2LA3RA_1LB2RA4RB0LA---` | 10,000,000,000 | — | [≥ 2 × 10^13](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved) | [Moving window](frontiers/runs/window-15.json) |
| 16 | `1RB2LA0RB0LB3LB_2LA4RB3RA0RA---` | 1,000,000,000,000,000 | — | — | [Six-cell strides](frontiers/runs/stride-16.json) |
| 17 | `1RB2RA3LB---2LB_2LA0LA4RB0RB1LA` | ≈ 1.40000 × 10^59 | [> 10^36](marked-register.md) | — | [Timed register sweeps](frontiers/runs/line17-epochs.json) |
| 18 | `1RB2RA3LB4LA---_2LA0RB1LA2RB0RA` | ≈ 9.24569 × 10^952 | — | — | [Timed prefix and suffix calls](frontiers/runs/line18-returns.json) |
| 19 | `1RB2RA3LA---2LB_2LA4RA4RB0RB0LA` | 10,000,000,000 | — | [≥ 4 × 10^13](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved) | [Moving window](frontiers/runs/window-19.json) |
| 20 | `1RB2RA3LA4LA2RB_2LA---3LB1RA3RA` | ≈ 6.00000 × 10^22 | — | — | [Guarded boundary streams](frontiers/runs/stream-20.json) |
| 21 | `1RB2RA3LA4LA2RB_2LA3RB---0RA1LA` | ≈ 5.20000 × 10^23 | — | — | [Boundary streams](frontiers/runs/stream-21.json) |
| 22 | `1RB2RA3LA4LA2RB_2LA3RA---0RA1LA` | ≈ 5.20000 × 10^23 | — | — | [Boundary streams](frontiers/runs/stream-22.json) |
| 23 | `1RB3LA3LB0RB0LA_2LA4RB1LB1RA---` | 10,000,000,000 | — | — | [Moving window](frontiers/runs/window-23.json) |
| 24 | `1RB3LA1LA2RB2RA_2LA4RA3LB1RA---` | ≈ 1.77089 × 10^21 | — | — | [Guarded AB sweeps](frontiers/runs/line24-sweeps.json) |
| 25 | `1RB2LB3LA0RA1LB_2LA4RA3RB3LA---` | 10,000,000,000 | — | — | [Moving window](frontiers/runs/window-25.json) |
| 26 | `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA` | 566,255,088,944,246,173,560,939 | [≥ 377,503,392,604,154,203,337,765](column-phases.md#extension-through-cut-84) | — | [Timed pair checkpoint](column-time.md) |
| 27 | `1RB3LB---4LA1RB_2LA4LA4LB3RB1RA` | 10,000,000,000 | — | — | [Moving window](frontiers/runs/window-27.json) |
| 28 | `1RB3LB4LA0LB---_2LA0LA1RB0RA3RA` | 1,000,000,000,000,000 | — | — | [Six-cell strides](frontiers/runs/stride-28.json) |
| 29 | `1RB3RB---3LA1RA_2LA3RA4LB0LB1LB` | ≈ 1.09706 × 10^1030 | — | [≥ 10^13,634](https://wiki.bbchallenge.org/wiki/Bonus_Cryptid) | [Timed cryptid sweeps](frontiers/runs/hydra-29.json) |
| 30 | `1RB3RB---3LA1RA_2LA3RA4LB0LB0LA` | ≈ 2.85901 × 10^7045 | — | — | [Timed cryptid sweeps](frontiers/runs/hydra-30.json) |
| 31 | `1RB3RB---4RA2RA_2LA2RA3LB4LB1LB` | ≈ 5.00000 × 10^27 | — | — | [Boundary streams](frontiers/runs/stream-31.json) |
| 32 | `1RB3RB1LB2RA---_2LA2RB1LA4LB0RA` | 10,000,000,000 | — | — | [Moving window](frontiers/runs/window-32.json) |
| 33 | `1RB2LA0RB4LB1RA_1LA3RA1RA---0LA` | 10,000,000,000 | — | — | [Moving window](frontiers/runs/window-33.json) |
| 34 | `1RB2LA4RA1LA3LA_0LA2RB3RB2LB---` | 10,000,000,000 | — | — | [Moving window](frontiers/runs/window-34.json) |
| 35 | `1RB2LA4RA1LA3LA_0LA3RB3LB2RB---` | 10,000,000,000 | — | — | [Moving window](frontiers/runs/window-35.json) |
| 36 | `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---` | 10,000,000,000 | [Unbounded (proved nonhalting)](line36-nonhalting.md) | — | [Moving window](frontiers/runs/window-36.json) |
| 37 | `1RB2LA3LA4RA1LA_0LA3LB3RB1RB---` | 10,000,000,000 | [≥ 39,999,600,001](line37-header.md) | — | [Moving window](frontiers/runs/window-37.json) |

Line 3’s transcript gives its lower bound in full. Line 4’s lower bound uses the millionth return, while its saved raw clock is at return 1,024. Line 5’s timed replay reaches the same A(4,b) and recurrence count as the earlier checkpoint, which contains b consecutive nonzero cells. Each required a write, so its 173,754-bit b gives the displayed bound. The 8,684,421,216 recurrence events have a separate count. Line 17’s bound uses the distance travelled in its verified header epochs. On line 37 the successful sweeps from epochs 1 through 199,999 each traverse the old word, whose width starts at one and grows by at least two per sweep. Summing the minimum widths gives 199,999² raw steps.

The [line 17 first-visit records](frontiers/README.md#line-17-first-arrivals-inside-a-sweep) give exact clocks inside a header sweep. Two input slots determine the first return from coordinate +12. [Decision rule and time bounds](line17-edge-time.md#the-return-depends-on-two-bits)

The community describes line 7 as expected to halt, line 13 as a possible halter, line 17 as likely to halt and line 26 as likely nonhalting. [Community holdout notes](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved) · [October research report](https://wiki.bbchallenge.org/wiki/TMBR:_October_2026#Holdouts)

Run `python3 frontiers/scoreboard.py --check` from this directory to verify the table. [Simulation and continuation commands](frontiers/README.md)
