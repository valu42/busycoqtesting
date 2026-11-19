# Which resets can reach a specific #758 terminal?

For the specific terminal state reached from A(1,H), the **only possible last resets** on a blank-compatible orbit are A(1,H−2) and A(1,H). The exhaustive reverse search contains 2,723 states. The same test identifies the exact last-reset pairs for three smaller terminals. The [blank crossings](BLANK_CROSSINGS.md) now exclude the three smaller pairs. Reachability of the pair at $H$ remains open. H and the two-counter conventions are given in the [ranking](RANKINGS.md). [Published candidate pairs and transition rules](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA)

| Exact last reset parameters | Map calls from either reset, including the halting call | States in reverse search | Maximum reverse depth |
|---|---:|---:|---:|
| 1,326,438,094,216,110 and that value + 2 | 62 | 617 | 99 |
| 2,031,355,966,425,479 and that value + 2 | 38 | 265 | 37 |
| 3,335,436,339,933,243 and that value + 2 | 34 | 213 | 36 |
| H − 2 and H | 307 | 2,723 | 313 |

## Exhaustive inverse check

From the blank entry A(0,1), every live state has c ≥ 1, and an even c occurs only at a reset (a = 1). This follows by inspecting the two-counter rules. On this domain, each nonreset target A(a,c) has odd c. The table lists every possible predecessor on the domain. The symbols J, L and E refer to the [grouped transition rules](COVER_758.md).

| Predecessor branch | Condition on target | Predecessor coordinates |
|---|---|---|
| L | c ≡ 5 mod 6, q = (c − 5)/6 | (a + 4q + 3, 4q − 1) or (a + 4q + 3, 4q + 1), keeping positive second coordinates |
| J | a ≡ 5 mod 6, b = (a − 2)/3 | (b, c + b − 1) |
| Even reset entry | a = 3 and c ≥ 5 | (1, c − 3) |
| E | c = 1, a ≥ 17 and a ≡ 5 mod 12, b = (a − 8)/3 | (b + 2, b) |

The checker runs forward from both reset candidates to identify the exact terminal state. It then traverses the entire inverse graph, stopping a branch as soon as it reaches a reset or has no predecessor. It checks every reconstructed edge against the forward map. The mass a + 2c decreases on each reverse edge. Every queue empties within the reported size. Thus the table includes all last resets leading to **each listed terminal** while permitting every trajectory on the stated domain. An individual reverse state may be unreachable from blank.

For the smallest pair let K = 1,326,438,094,216,110. Its exact terminal is A(884,292,062,810,856, 884,292,062,810,855). The universal claim that all trajectories must encounter one of this pair when crossing the nearby mass range has a counterexample. A(1,K−252) first returns at A(1,K+8) after 93 calls, passing both candidate masses. Subsequent resets have strictly larger parameters. The inverse check therefore also rules out that particular terminal for this crossing trajectory.

The obstruction to extending the literal inverse search through a reset is already visible at K. A(1,K) has **221,073,015,702,685** predecessors of the form A(2b,K−b−2) from the return rule alone. Here b ranges through the odd integers with 0 ≤ 3b ≤ K−2. These are algebraic predecessors; reachability from blank requires a further argument. A proof going farther backward would need to handle this family symbolically or use information specific to the blank orbit.

## Reproduction

Run [terminal_forest_758.py](terminal_forest_758.py) beside [check_bb33.py](check_bb33.py) using Python 3.10 or later.

```sh
python3 terminal_forest_758.py
```
