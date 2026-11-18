# BB(2,5) holdout research

These notes record partial results on the November 3, 2026 list of 37 formal holdouts. Each machine is identified by its full transition string. All line numbers here are **one-based positions in that exact file**. The scripts use an initially blank, two-way infinite tape, state A and head coordinate zero. An undefined instruction halts on arrival. No blank-tape decision or Rocq theorem is claimed in this directory.

| Formal line | Machine | Result to continue from |
|---:|---|---|
| 17 | `1RB2RA3LB---2LB_2LA0LA4RB0RB1LA` | A 424-digit blank checkpoint reaches coordinate 12. Two exact suspended words halt at −4 before the head returns to −10. The unresolved step selects the suspended word from the true periodic stream. |
| 26 | `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA` | Blank halting is equivalent to a three-integer recurrence crossing its threshold. Both the counter and its width are unbounded in the total arithmetic model. |
| 2 | `1RB---4LB0LA4RA_2LB2LA3RA4LB0RB` | A fixed-cut protocol replaces the growing left half. The negative prefix is exact through 2,400 extensions from blank. |
| 10 | `1RB2RB3LA4LA1LA_2LB3RA---4RA1RB` | Three leading A entries at the fresh edge halt. Cyclic period counts are known. The starting position matters. |
| 3 | `1RB---0RB0LA2RA_2LB2LA3RA4LB0LB` | Mixed binary/ternary macros give a lower bound exceeding 10¹⁵⁰ defined steps from blank. Higher reset branches remain open. |
| 36 | `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---` | A prefix with six excess closing symbols halts. Repeated blank sweeps exhibit a common prefix six epochs apart. |

The first four rows are developed in [the research log](research-log.md). The earlier [frontier derivations](frontier-background.md) give the raw pair tables and the initial blank checkpoint. The [mixed-counter and sweep notes](mixed-and-sweeps.md) also record results on lines 12, 21 and 22 and list the exact identities used for the left-half certificates.

From the repository root, run these checks with Python 3.10 or later, with assertions enabled. They use only the standard library.

```sh
cd research/bb2x5
python3 verify.py
python3 mixed_and_sweeps.py
```

Expected output is in [verification.txt](verification.txt) and [mixed-verification.txt](mixed-verification.txt). The direct interpreters and word rules live in `prior_sweeps.py` and `prior_frontier.py`. The tests distinguish the actual blank orbit, exact implications for auxiliary configurations, and experiments with freely chosen inputs. In particular the 242-step line-17 halting continuation agrees with a long prefix of the blank stream, then diverges from its fixed period.

The data file is [BB2x5_Rocq_holdouts_37.txt](BB2x5_Rocq_holdouts_37.txt). Its SHA-256 is `89ea92fd4643166b92fca4ae80e37a699ab8615ac1dd375dae777e6b3e45ecc6`. The notes credit the original community analyses at the relevant derivations. [Published list](https://wiki.bbchallenge.org/w/images/c/cc/BB2x5_Rocq_holdouts_37.txt) · [Community status](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved)
