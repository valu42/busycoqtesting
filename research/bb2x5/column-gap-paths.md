# Line 26: what part of a record gap can fund the safety margin?

The real blank run of `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA` reaches record depth 99 with 207 allocated pairs. The all-depth decision is open. A sufficient target from the [record-gap criterion](column-records.md) is a prefix average of six safe tokens per new record. The following reduction isolates tokens that pass in complete local cycles. Their prefix average alone would suffice, and their exact smallest prefix average on the first 63 transitions is 20/3. The comparison examples below explain why simply putting more safe tokens into the root cannot justify the induction.

## A phase-preserving comparison

Consider a fixed nonempty block of h pairs starting in the digits (uᵢ,eᵢ), low pair first. In an input made up of g safe tokens followed by one dangerous token, put

* m = 1 + the number of set e bits **below the last pair**;
* r = the number of set e bits in the **whole block**;
* g = 2ᵐa + d, with 0≤d<2ᵐ.

Replacing g by d leaves every digit at the dangerous-token arrival unchanged, including the decision to pass that token. The original input sends exactly **a·2ᵐ⁻ʳ more safe tokens** through the block. This weight is either one or two per complete cycle.

For a proof, safe subtraction toggles the selected u bits as an ordinary binary counter. In h pairs the selector is the low h bits of 2e+1, with exactly m set bits. The least positive number of safe inputs restoring the selected counter is 2ᵐ. Over a restoring cycle the first pair sends its input count divided by $2^{e_0}$, since it alternates between sending 2−e₀ and sending zero. The same reasoning applies at every subsequent pair because all u bits return. The output of one cycle is 2ᵐ⁻ʳ. Removing whole cycles before each dangerous arrival preserves every later state **in this block**, so these positive contributions add over the intervening arrivals. The lower and upper cut must be specified when using this comparison.

## Exactly 28 cases between records

At a new record j, take the small block from the *preceding record index* up to, but excluding, j. Its digits D are determined by the preceding record gap modulo four. Start from D and read the subsequent lower-cut gaps until the first Q passes the block. The total safe output in this interval is exactly the new record gap b. At each incoming Q choose the residue d as above and update the block using only d. Let L be the sum of the complete-cycle outputs, and ρ the safe output on the residue path. Then **b=L+ρ**.

| Preceding gap mod 4 | Initial block D | Number of residue paths | Most lower Qs needed | Possible ρ |
|---:|---|---:|---:|---|
| 0 | 0 | 3 | 2 | 0, 1, 2 |
| 1 | 3, 2 | 11 | 3 | 0, 1 |
| 2 | 0, 2 | 12 | 4 | 0, 1, 2 |
| 3 | 3 | 2 | 1 | 0 |
| Initial seed | 2 | 3 | 2 | 0, 1 |

The 28 regular paths (and three seed paths) enumerate at most four residues apiece because the block contains at most two pairs. To reproduce any entry, branch on d from 0 through 2ᵐ−1, perform one ordinary column transfer across D, and end the path if Q passes. Otherwise recurse on the new digits. For example, in the single digit 3 the first Q always passes and every emitted safe token comes from a complete cycle. The [checker](column_gap_paths.py) generates every leaf and independently cross-checks the affine formula on unrounded inputs.

For every transition, L≥max(0,b−max ρ), with the cap chosen from its row. On the 63 true transitions these computable lower bounds sum to at least **632**. The first three blocks consume lower gap lists (9,9), (4), and (7). They emit record gaps 13, 2, and 8. Their exact complete-cycle contributions are 12, 2, and 6. From the fourth prefix onward even the conservative lower bounds have average at least 37/5. Thus the least actual prefix average of L is **20/3**, attained at the third prefix. The empirical statement is finite. To prove nonhalting it suffices to show **Σ Lᵢ≥6n** for every prefix of n transitions on the anchored root stream; the residue outputs are nonnegative. The formulas reduce one such reward to at most four gaps at the preceding record cut. They do not yet bound how often each path occurs.

There is also an exact recursion for the whole rooted stream. At the seed use the constant lower gap stream 9,9,… and block 2. Consume the first residue path to obtain b. Push the unconsumed lower stream through the **updated** block to obtain the future gap stream at the current record, and select the new block using b mod 4. Repeating this rule generates the actual record sequence and its complete-cycle rewards without choosing a phase. The checker implements this recursion independently and agrees with the first twelve timestamped transitions.

## Three comparisons that fail even from the common blank seed

In all three experiments the first tick is exactly the true blank tick, and every Q remains in place. The modified safe arrivals are inputs to the reduced upper machine. Once the nine-token schedule resumes, the indicated upper word, the usual three low pairs, and the guard specify an actual nonblank tape for the original ten-entry machine.

| Alteration at cut 3 | Resume after tick | Upper digits at resumption | First undefined instruction |
|---|---:|---|---|
| Move one P from tick 7 to 6, from 11 to 10, and from 15 to 14 | 15 | `223233233210` | B3 at coordinate 35 during tick 41, after 287,750 defined instructions from resumption |
| Add one P at each of ticks 6, 9 and 18 | 18 | `301203111200` | B3 at coordinate 43 during tick 224, after 9,638,408 defined instructions from resumption |
| Add four P at each of ticks 4, 6, 7 and 34 | 34 | `11112331322012` | B3 at coordinate 37 during tick 55, after 365,400 defined instructions from resumption |

The first comparison is never below the genuine cumulative supply and never exceeds it by more than one. At tick 15 it has the exact genuine cumulative supply again, yet its width is 15 versus the genuine 21. In the second comparison **every single input gap** is at least nine and its width at tick 18 is 15 versus the genuine 24. In the third comparison adding four preserves both low upper pairs (indices 3 and 4) at every Q, since their complete-cycle lengths divide four. The entire Q schedule at cut 5 is unchanged and every corresponding safe gap there is at least the genuine one. The upper continuation still fails. All three standard-tape continuations were checked from their specified tapes by literal defined instructions. All three modified inputs differ from the physical blank orbit. They rule out proving blank safety by a comparison that assumes extra or advanced safe tokens can only help at all later times.

## The next two blank records

| Tick | Old record | Gap | New record | Allocated width | Margin |
|---:|---:|---:|---:|---:|---:|
| 1,216,542,934,121 | 96 | 6 | 98 | 206 | 108 |
| 2,179,060,843,052 | 98 | 4 | 99 | 207 | 108 |

The width-205 checkpoint had already accumulated four P at pair 96. Two more precede its next Q. The next complete gap measured at pair 98 is four. The first-arrival gap recurrence gives g₉₆=408, g₉₇=411, g₉₈=412 and g₉₉=414, hence p(99)=207. The [plateau bound](column-phases.md#the-first-dangerous-arrival-and-a-bound-on-its-plateaux) with R₁₅=4 gives 3R₉₉<2⁵³, so p(152)>p(99) and therefore p(207)>207. All potential halting widths through 207 are excluded.

The exact raw checkpoint at depth 99 is **911,674,782,283,459,532,199,683,101 defined instructions**. Its head scans the blank at -17,432,486,744,417 in state A. Its weighted physical visit sum is 252,771,055,003,771. Replays using calendar cuts 17 and 18 reproduce the entire tape and clock by restarting at the preceding checked tape. With margin 108 the next 107 records are safe. Their earliest possible danger is bounded by counting Q arrivals at cut 60: all ticks through its 107th subsequent Q at tick 2,180,358,927,799 succeed. The [raw-clock inequality](column-time.md#bounds-that-hold-beyond-the-computed-checkpoint) therefore gives **at least 912,761,290,374,298,539,837,004,992 defined instructions**. [Record 98 tape](frontiers/runs/line26-record98.json) · [Record 99 tape](frontiers/runs/line26-record99.json)

For the local proofs, the literal comparisons and the two checkpoint checks, run from this directory:

```sh
c++ -O3 -std=c++17 column_records.cpp -o /tmp/line26-records
c++ -O3 -std=c++17 column_raw_time.cpp -o /tmp/line26-clock
python3 column_gap_paths.py
python3 check_column_followup.py --records /tmp/line26-records --clock /tmp/line26-clock
python3 frontiers/scoreboard.py --check
```
