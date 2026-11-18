# Line 34 has a variable right-edge clock

The machine is `1RB2LA4RA1LA3LA_0LA2RB3RB2LB---`. Its blank-tape outcome remains **Unknown**. Two results of this pass are an exact interval between right-boundary growth events and a finite counterexample to deciding guard safety from short observed substrings. The latter uses an explicitly altered tape. Neither gives a halting-time distribution. These are mathematical arguments with executable checks. They have no formal verification.

## The next append

Use the repository's normalized epoch, with A on the blank immediately left of the occupied word. In left-to-right order, write O for 1, C for 3 and N for 2. In the outward sweep, each C pairs with the nearest available O to its left. A sixth unpaired C reaches B4. If the sweep succeeds, write 1 for each unpaired O, and 0 elsewhere. The ordinary return digit for an old cell with previous and current bits $(p,s)$ is

| $(p,s)$ | New digit |
| --- | --- |
| (0,0) or (1,1) | O |
| (0,1) | C |
| (1,0) | N |

This follows from the inherited sweep rules. Their ternary return order is 3,1,2. An unpaired opening leaves 2 and supplies a carry. Every other old digit leaves 3 and supplies zero. The left header has length one or five. The return appends N precisely when the last old bit is 1. In particular this happens exactly when the last old digit is O. [Inherited matching model and literal interpreter](../prior_sweeps.py)

**Clock theorem.** Suppose epoch `e` ends in a maximal run of `r ≥ 1` openings. On a continuing run, the next two appending sweeps start at `e` and `e+r+1`. After the first append the suffix is `C O^(r−1) N`. All those old openings survive. The cell before them supplies a zero bit, including the left guard when the entire old word consists of openings. Next, any suffix `C O^k N` with positive `k` becomes `C O^(k−1) N` with no append. The C cannot survive and the k openings all survive. When k reaches zero, both cells of the final CN have zero bits. The last digit then becomes O, at epoch `e+r+1`. The argument applies to each successful sweep individually. A guard failure terminates it.

Once the word has at least three ordinary digits, a CN also forces the third bit from the right to be zero. An opening there would be paired with the C. Consequently the next word ends in at least two O's. From the literal epoch-4 seed (width five), every further append interval has at least three sweeps. Each successful sweep on width `w` travels to its right edge and back to a new left checkpoint. It costs at least `2w` defined instructions. Thus there are at least `2w(r+1)` raw instructions between these successive append epochs. The exact raw interval is the sum of the r+1 sweep costs, each determined by the interior matches and guard in the [raw clock derivation](target34.md#exact-clock-for-one-successful-sweep).

| Blank epoch at start of appending sweep | Old width | Old terminal run | Raw step |
| --- | ---: | ---: | ---: |
| 2 | 2 | 1 | 8 |
| 4 | 5 | 4 | 32 |
| 9 | 11 | 2 | 171 |
| 12 | 15 | 5 | 302 |
| 18 | 22 | 3 | 692 |

**Residue restriction.** Consider the CN checkpoint immediately before the terminal O's reappear. Let Z be the suffix after the last surviving opening. Suppose that opening is at the last header cell or to its right in the current word. The C's in Z all have partners inside Z, since no unmatched debt can cross this surviving opening. Z has no surviving opening of its own, so its O and C counts are equal. Each ordinary C is a rise and each N is a fall in the previous sweep's bits. Their difference telescopes. The final N is a fall to zero, including an appended N represented by adding a terminal virtual zero bit. This gives `#N − #C ∈ {0,1}` on Z. Its length `z` is therefore 0 or 1 modulo 3. Its first digit becomes N and its remaining digits become O, so the new maximal run is exactly `z−1`, congruent to 2 or 0 modulo 3. The following append interval is accordingly 0 or 1 modulo 3.

If the hypothesis fails, all old bits strictly to the right of the header are zero. The next run then has length at least `width − header_length − 1`. This includes the case of no surviving opening anywhere. The blank run through epoch 1,500 included 326 appending sweeps. The residue hypothesis held for 324 of 325 observed renewals from a terminal CN. Its single exception leads to the run of four openings at epoch 4. Finite sampling gives no all-time assertion about the hypothesis. In particular there is no fixed Pascal boundary of the kind proved for line 35. [Line 35 right-edge theorem](../line35-pascal.md)

## A local proof obstruction at the cut after nine digits

A bound of five on all incoming debts at this cut would suffice for nonhalting by the [left guard calculation](line34_left.md). The following altered orbit shows how a sixth unpaired closing can evade a proof based on local factors or short interface histories.

At blank epoch 839, take the 1,025-cell word and replace its segment `[856,879)`, in zero-based left-origin coordinates, by 493 consecutive copies of that segment. It is `11112113232111111131211`. At each of the next 15 sweeps, the two bounding cuts of the **original** segment have equal outgoing matching debt and equal survivor bits on the immediately preceding cells. Thus copies can be inserted without changing either exterior. Right-to-left matching sees identical initial debt and sends out the same debt for each copy. The bit at each join also agrees, so the return digit across each join is correct. The same guard decision gives the same left header. The segment shifts in left-origin coordinates by that header length. This is an application of the repository's line 37 splicing argument to a different string and a new physical witness. [Original splicing method](../line37-splice.md)

At epoch 854 the segment is at `[871,894)` and reads `23213232131232131232131`. It has one more C than O. The blank word sends zero debt across cut 9 and survives. The altered word sends ten across that cut and delivers six to the guard. A separate literal run from the altered epoch-839 tape halts at B4 after **6,685,289** defined instructions, with final head −17 relative to the initial head at zero. The closed-form splice and literal run both start from the specified altered checkpoint.

Every 17-digit factor at **every** position of the failing word occurs in a genuine blank epoch with index congruent to 854 modulo 13. Factors outside a join occur in the original epoch-854 tape. Those crossing a new join occur in the periodic repetition of the 23-digit segment. Its 23 offsets yield 22 distinct 17-digit factors. The verifier finds all 22 by epoch 704 without a phase restriction, and all 22 in phase 9 by epoch 3,181. In particular any interior constraint admitting all real 17-digit factors of this phase also admits the entire failing interior. The failing word has the genuine left and right exteriors. A proof that uses additional long-range correlations, position labels or histories can distinguish the two orbits.

## Reproduction and next step

Run `python3 halting-outlook/line34_right.py` from `research/bb2x5` with assertions enabled. The code checks the complete transition string, the first 80 literal blank epochs, and every normalized input through length seven (3,280 words, ten reaching B4). The full state, absolute head and tape are compared on each successful one-sweep test. The raw endpoints in the clock table come directly from the literal interpreter. For the 15 safe altered sweeps, the separate [timed accelerator](target34_orbit.py) agrees with the literal raw count, absolute head, state and every tape cell at every checkpoint. Its next call detects the failing guard and debt ten at the cut. The literal run continues through B4. The larger genuine epochs use the inherited single-sweep matcher; every application checks the guard. Its raw instruction clock is not used for the factor claims. [Checker](line34_right.py) · [Verification output](line34_right-verification.txt)

The immediate proof target is to control debt from the middle across the cut on the unique blank orbit. A next finite search can carry the exact signed balance of a material interval through more than 15 sweeps, with its terminal-run countdown and cut debts, and test whether it excludes this particular splice before attempting a global induction. A count of append events alone cannot distinguish the two equal right exteriors.
