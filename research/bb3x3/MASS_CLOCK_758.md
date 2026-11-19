# A raw-time lower bound from an attained #758 mass

Let W = a + 2c. If #758 reaches a mass of **6,670,872,679,866,767** from blank, it has run for at least **14,659,627,256,375,446,994,648,609,755,050,506,701,497,558 raw steps**. This is the mass at A(1,3,335,436,339,933,383). The implication needs only attainment of the mass. Connecting a particular checkpoint to blank requires the forward certificates. The two raw clocks differ by 50,707 steps after the proved join, so the same threshold implies more than 1.46 × 10⁴³ steps in each encoding. [Ranking and raw join](RANKINGS.md) · [Ten branch costs](timing_758.py)

## A costly transition in every sufficiently long block

The blank #758 reaches A(0,1) after two raw steps. On the continuing orbit, c ≥ 1 and an even c occurs only at a reset with a = 1. Direct substitution into the two-counter rules gives a positive increase of at most nine in W per map call. Every branch costs at least 3 min(a,c)² raw steps by the published quadratic timings. [Transition rules and timing table](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA#A(a,_c)_Rules_and_Timings)

Consider a block of continuing calls starting at mass W₀ and set m = ⌊(W₀−2)/5⌋. Throughout the block W ≥ 5m+2. A state with a,c ≥ m supplies a transition costing at least 3m². For m ≤ 0 the bound is immediate. Otherwise the following cases cover an input with a small coordinate.

* If a < m, then a ≤ c. An even a takes the return to a = 1. At a reset with even c, one more call gives a = 3 and odd c. With odd a and c the J update sends a to 3a+2 and preserves odd c. Thus after at most two preparatory calls the first counter grows at least threefold until it reaches m. On the crossing call its new value is at most 3m−1, so the new second counter is at least m. A preparatory call that already reaches m obeys the same upper bound.
* If c < m, then a ≥ 3m+4. Here c is odd and the ordinary bulk rule applies. For q = ⌊(c+1)/4⌋ it gives c′ = 6q+5 ≥ 3c/2 and a′ = a−4q−3 ≥ a−c−4 ≥ 2m+1. This repeats until c reaches m, with the other coordinate still at least m.

Fix a target mass V ≥ 2 and stop at its first crossing. The endpoint mass is at most V+8. Choose n as the least nonnegative integer with (3/2)ⁿ ≥ ⌊(V+8)/5⌋. Let B be the smallest multiple of five at least n+3. In any completed block of B calls before this crossing, the preceding cases reach a state with both coordinates at least m in at most n+2 updates. Its outgoing costly transition is inside the block.

## Sum over completed blocks

Count backwards from the crossing. The start of the jth preceding block has mass at least V−9Bj. At least N = ⌊(V−2)/(9B)⌋ complete blocks exist since the initial mass is two. Define P = ⌊(V−2)/5⌋ and D = 9B/5. Adding one transition per disjoint block gives the lower bound

$$
3\sum_{j=1}^{N} (P-Dj)^2.
$$

For V = 6,670,872,679,866,767, the verifier gives B = 90 and N = 8,235,645,283,786. It evaluates the sum exactly in constant time after finding B. Run `python3 mass_clock_758.py` beside [check_bb33.py](check_bb33.py) and [timing_758.py](timing_758.py). The checks compare the formula against direct summation at small masses, compare one hundred blank-orbit masses with their exact clocks, and replay the balanced-state argument at small and large seeded configurations. [Verifier](mass_clock_758.py)

## Conditional clock at the known halting seed

**If the blank orbit reaches A(1,H), #758 halts after more than 4.41 × 10⁴¹³ and fewer than 2.20 × 10⁴¹⁷ raw steps.** The lower bound above uses V = 2H+1 and B = 795. For the upper bound, every branch costs at most W²/3 + 10W + 65 since min(a,c) ≤ W/3. Each continuing blank-domain mass increment is at least four. Integrating this increasing cost bound over the disjoint mass intervals of those calls bounds the prefix clock by 2 + V³/36 + 5V²/4 + 65V/4. The verifier adds the exact cost of the 307-call halting suffix. Blank-tape reachability of A(1,H) remains open.
