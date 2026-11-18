# BB(2,5) simulation table

Each row follows one machine from the all-zero, two-way-infinite tape. The step counter advances once per defined instruction. The linked result contains the complete checkpoint or its run record. All 37 blank-tape outcomes remain open in these runs.

The exact endpoint column gives the largest counted run in the sources indexed here. Values marked ≈ abbreviate the exact integer in the linked file. The lower-bound column also credits longer runs where only a minimum raw duration is known.

| Line | Machine in the November 3 list | Raw steps at exact endpoint | Additional raw lower bound | Endpoint source |
|---:|---|---:|---:|---|
| 1 | `1RB---4LB1RA4RA_2LB2LA3RA4LB0RB` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-01.json) |
| 2 | `1RB---4LB0LA4RA_2LB2LA3RA4LB0RB` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-02.json) |
| 3 | `1RB---0RB0LA2RA_2LB2LA3RA4LB0LB` | 100,000,000 | [≥ 10^151](mixed-verification.txt) | [Moving window](frontiers/runs/window-03.json) |
| 4 | `1RB3LA1LA1RA3RA_2LB2RA---4RB1LB` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-04.json) |
| 5 | `1RB3LA1LA1RA1RA_2LB2RA---4RB1LB` | 100,000,000 | [≥ 2^173,753](accelerator-results/arithmetic5-100k.json) | [Moving window](frontiers/runs/window-05.json) |
| 6 | `1RB---3LB4RB0LA_2LB3LA3RB4RA0RA` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-06.json) |
| 7 | `1RB---3RA2LA2RB_2LB3LA4LB4RA0RA` | 100,000,000,000 | — | [Moving window](frontiers/runs/window-07.json) |
| 8 | `1RB4LA1RA1RB1LA_2LB3LA---4RA2RB` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-08.json) |
| 9 | `1RB---4RB2RB4LA_2LB3LA3LB0RA0RB` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-09.json) |
| 10 | `1RB2RB3LA4LA1LA_2LB3RA---4RA1RB` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-10.json) |
| 11 | `1RB2LA4LA1RA1LA_2LB3RB4RB---2RA` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-11.json) |
| 12 | `1RB4RB4RA1LA3LA_1LB2LA3RB2RB---` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-12.json) |
| 13 | `1RB3RA3RB4LA1LA_1LB2LA1LA---1RB` | 100,000,000,000 | — | [Moving window](frontiers/runs/window-13.json) |
| 14 | `1RB2RA4LA1RB4RB_1LB2LA3RA---0LB` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-14.json) |
| 15 | `1RB3RB1LA2LA3RA_1LB2RA4RB0LA---` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-15.json) |
| 16 | `1RB2LA0RB0LB3LB_2LA4RB3RA0RA---` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-16.json) |
| 17 | `1RB2RA3LB---2LB_2LA0LA4RB0RB1LA` | 100,000,000 | [> 10^36](marked-register.md) | [Moving window](frontiers/runs/window-17.json) |
| 18 | `1RB2RA3LB4LA---_2LA0RB1LA2RB0RA` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-18.json) |
| 19 | `1RB2RA3LA---2LB_2LA4RA4RB0RB0LA` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-19.json) |
| 20 | `1RB2RA3LA4LA2RB_2LA---3LB1RA3RA` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-20.json) |
| 21 | `1RB2RA3LA4LA2RB_2LA3RB---0RA1LA` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-21.json) |
| 22 | `1RB2RA3LA4LA2RB_2LA3RA---0RA1LA` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-22.json) |
| 23 | `1RB3LA3LB0RB0LA_2LA4RB1LB1RA---` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-23.json) |
| 24 | `1RB3LA1LA2RB2RA_2LA4RA3LB1RA---` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-24.json) |
| 25 | `1RB2LB3LA0RA1LB_2LA4RA3RB3LA---` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-25.json) |
| 26 | `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA` | 100,000,000 | — | [Moving window](frontiers/runs/window-26.json) |
| 27 | `1RB3LB---4LA1RB_2LA4LA4LB3RB1RA` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-27.json) |
| 28 | `1RB3LB4LA0LB---_2LA0LA1RB0RA3RA` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-28.json) |
| 29 | `1RB3RB---3LA1RA_2LA3RA4LB0LB1LB` | 4,124,222,829 | — | [Block simulator](accelerator-results/line-29-level-12.json) |
| 30 | `1RB3RB---3LA1RA_2LA3RA4LB0LB0LA` | 4,121,120,989 | — | [Block simulator](accelerator-results/line-30-level-12.json) |
| 31 | `1RB3RB---4RA2RA_2LA2RA3LB4LB1LB` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-31.json) |
| 32 | `1RB3RB1LB2RA---_2LA2RB1LA4LB0RA` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-32.json) |
| 33 | `1RB2LA0RB4LB1RA_1LA3RA1RA---0LA` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-33.json) |
| 34 | `1RB2LA4RA1LA3LA_0LA2RB3RB2LB---` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-34.json) |
| 35 | `1RB2LA4RA1LA3LA_0LA3RB3LB2RB---` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-35.json) |
| 36 | `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-36.json) |
| 37 | `1RB2LA3LA4RA1LA_0LA3LB3RB1RB---` | 10,000,000,000 | — | [Moving window](frontiers/runs/window-37.json) |

Line 5’s A(4,b) checkpoint contains b consecutive nonzero cells. Starting on blank takes at least one write per such cell, so its 173,754-bit b gives the displayed raw lower bound. Its 8,684,421,216 recurrence events have a separate count. Line 3’s exact lower-bound integer is in its transcript. Line 17’s bound follows from its verified count of header epochs and the distance travelled in each.

The table tracks this repository. For comparison, Andrew Ducharme reported about 10^17.50888 raw steps for line 13, and LegionMammal978 reported more than 10^1,140,000,000 on line 7. The community lists line 17 as likely to halt, line 13 as a possible halter, and line 26 as likely nonhalting. [Community holdout notes](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved) · [October research report](https://wiki.bbchallenge.org/wiki/TMBR:_October_2026#Holdouts)

Run `python3 frontiers/scoreboard.py --check` from this directory to check the table against the saved files. [Simulation and continuation commands](frontiers/README.md)
