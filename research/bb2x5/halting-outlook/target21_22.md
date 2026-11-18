# Lines 21 and 22: which input at the parent would halt its child?

On line 22, the first five A entries following an initial B at a new cell would halt its right neighbor. On line 21 there are four dangerous prefixes. This gives a short test on the actual upstream stream. Both outlooks remain **Unknown**.

| Line | Exact machine | Dangerous prefixes at a fresh parent |
| --- | --- | --- |
| 21 | `1RB2RA3LA4LA2RB_2LA3RB---0RA1LA` | `BAAAAA`, `BAAAABB`, `BAABBA`, `BAABBBB` |
| 22 | `1RB2RA3LA4LA2RB_2LA3RA---0RA1LA` | `BAAAAA` |

## Argument

The inherited [one-cell table and negative-half return proof](../mixed-and-sweeps.md#2-two-machines-with-the-same-exact-blank-half-input) reduce halting to a fresh cell receiving BB first. Here we pull that event back through one fresh cell. Cell 0 begins with A, so a halt anywhere on blank must have a parent at some nonnegative coordinate. The table uses actual entries in chronological order. A successful entry finishes before the next one is supplied.

An initial A emits BA, which clears the child's BB test. An initial BB halts the parent itself. An initial BA emits nothing and leaves the parent on symbol 3. From 3, input B first emits A (in the word ABA). Input AA first emits B and restores 3. Input ABA first emits A. Input ABB emits B and leaves 4 on line 21, and emits A on line 22. These four alternatives exhaust the first emission after BA. From state 4 on line 21, A emits B, BA emits A, and BB emits B. Combining the first and second emissions gives exactly the prefixes in the table. No later inputs can change a child's first two calls. An offending child needs no grandchild return. Its first B turns on the blank and its second reaches B2 immediately. This is an elementary proof from the transitions, without formal verification.

## Comparison with the blank run

We read the first up to 128 entries at each cut of the previously saved blank executions. These runs and their exact clocks, pair-frequency statistics, and left-half timing formulas are in the [stream report](streams.md#new-experiments-on-actual-blank-execution).

| Line | Parent cuts already excluding all listed prefixes | Still too short | Occurrences strictly inside the saved prefixes, cuts 0–99 / later |
| --- | ---: | ---: | ---: |
| 21 | 224 of 225 | Cut 224 | 43 / 45 |
| 22 | 202 of 203 | Cut 202 | 38 / 28 |

Each exclusion permanently clears the **child at that parent** of the fresh BB trigger. The last column counts overlapping occurrences at offsets greater than zero within each saved prefix. Those occurrences are safe in that position. The early and later cuts on both machines exhibit the same distinction between internal factors and the leading phase. There is no justified stochastic law for a fresh parent's position. We have no raw halting-time estimate.

Driving a fresh physical suffix with the listed controls took 8 or 9 local instructions through B2. These counts exclude the time spent to the left supplying successive entries. The [exact clock](streams.md#exact-timing-formulas-and-what-they-do-not-estimate) accounts for actual source periods and every crossing. It requires the period index at which the target prefix arrives.

Run `python3 research/bb2x5/halting-outlook/target21_22.py` from the repository root. It checks every binary input through length eight against the inherited cell interpreter, checks every dangerous word on the literal TM, and recomputes the two disjoint portions of the saved traces. The next proof target on line 22 is particularly concrete: determine whether the distinguished stream can **start** with BAAAAA at any later cut. A language allowing it in the body can still exclude it at the beginning.
