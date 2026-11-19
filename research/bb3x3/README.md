# BB(3,3) holdouts and the #758 blank-tape proof

**The blank-tape fate of #758 and its twin #153 remains open.** From blank, both machines skip the fourth candidate halting pair, reach the exact common reset **18,378,934,934,402,308**, and have executed more than **1.48 × 10⁴⁶ raw transitions** each. A separate proof rules out every eventually periodic sequence of counter rules, from any physical starting configuration. An infinite orbit could still have aperiodic ordinary excursions or continue through infinitely many resets. A halt anywhere on the common orbit would settle both encodings. [Four exact blank crossings](POWER_CROSSINGS_758.md) · [Raw clock](FOURTH_GATEWAY_758.md) · [Global periodicity theorem](FINITE_AFFINE_PERIODS_758.md) · [Four-holdout rankings](RANKINGS.md)

The reduction uses A(a,c) for a tape configuration carrying two nonnegative integer counters. One map update represents a variable number of raw machine transitions. A reset here means any visit to a = 1. The map and the equivalence of the encodings have published formalizations. This directory contains integer verification programs and their mathematical arguments. [Formal machine specifications](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB33/README.md) · [Counter transitions, timings and published checkpoint](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA)

## Continuing the blank proof

* **Scale 74.** A sufficiently early reset in the gate determines the exact midpoint configuration $A(2\cdot3^{36}-1,T-3^{36}+1)$, where $T=H-5G/4$ and $G=10^{10}3^{74}$. More generally, membership in a checked set of 701 states at the first midpoint crossing is equivalent to an actual gate visit by then. Starting from the gate's unique exit, the proof traverses the first change of word and reconverges a trillion reset values farther on. The connection to scale 73 remains open. [Midpoint and ancestry](SCALE74_ANCESTRY.md) · [Exact continuation from the exit](SCALE74_BRIDGE_758.md)
* **An alternative at the same crossing.** Missing the scale-74 gate altogether requires at least $10^{22}$ different length-401 fine words on that single passage. Missing the joined halting interval requires at least 1,900,000 different length-322 words. The argument uses collinearity of repeated words and applies even to aperiodic trajectories. [Finite word-count theorem](FACTOR_COMPLEXITY_758.md) · [Entropy on an infinite orbit, including resets](ALL_ORBIT_ENTROPY_758.md) · [Recovering the integer state from a two-sided word](SEPARATED_FACTORS_758.md) · [Why modular survival alone admits false states](MODULAR_GATE_LIMIT.md)
* **Starting much closer to blank.** At 546 gates of the form $3^m$ or $2\cdot3^m$, every sufficiently deep entry leads to one specific checkpoint. At scales 7 through 10 below the large target, four more verified intervals lead to a halt. The largest contains 362,166,436,260,267 consecutive reset seeds. [Halting intervals and transfer receipts](LOWER_SCALE_GATES_758.md) The first 29 power checkpoints are joined to blank through $3^{34}$. A fifth candidate at 40,486,323,621,582,648 has known halting ancestors and an incoming interval of 633,739,014,317,117 seeds that all pass it alive. [Fifth candidate and earlier halting intervals](MIXED_TERMINALS_758.md) [Power-gate checkpoints](POWER_GATES_758.md) · [Fourth candidate](FOURTH_GATEWAY_758.md) · [Exceptional halting branches](EXCEPTION_TERMINALS_758.md)

* **Halting seeds at arbitrarily large scales.** Under the hypothesis that ordinary stretches become short relative to their starting mass, the actual orbit visits every fixed relative neighborhood of an infinite family of halting pairs with exponents $m=597+1200j$. The unresolved step is reaching a seed that leads to a halt inside such a neighborhood. [Exact family and proof](CUSP_TERMINALS_758.md) · [Actual returning trajectories with every fixed target congruence](TERMINAL_CONGRUENCES_758.md)

## Where the two calculations stand

Let $H=(3^{307}-8\,282\,708\,212)/13\,959\,275$. The following statements use inclusive endpoints.

| Starting point | Verified consequence | Reproduction or argument |
|---|---|---|
| #758 on a blank tape | Reaches A(0,1) at step 2, then A(1,3). At exactly 3,251,620,479,139,366,879 raw transitions the counters are a = 107 and c = 5,090,319. | [Raw clocks and 400 raw-tape checks](timing_758.py) |
| Published blank checkpoint with a = 1 and c = 1,059,491,543,272,883 | The next 254,074,710,617 returns reach c = 1,079,817,520,122,241, with exactly 1,138,748,236,895,051,391,487,973,286,265,103,628,580,163 raw transitions between checkpoints. | [Affine return and exact clock](jump_758.py) |
| Every reset seed 1,059,491,543,272,883 ≤ c ≤ 1,079,817,520,122,229 | All 20,325,976,849,347 reach the identical reset at c = 1,079,817,520,208,950. The independent blank prefix reaches this interval, which suffices to prove the common endpoint from blank. | [Proof and verifier](CONFLUENCE.md) |
| Every reset seed 1,059,491,543,272,883 ≤ c ≤ 1,080,000,000,000,000 | All **20,508,456,727,118** reach a = 1, c = **1,080,000,000,055,450**. A second interval check and an exact bridge over 86,720 intervening seeds extend the previous row. | [Second interval and exit check](FRONTIER.md) · [Bridge](check_confluence.py) |
| #758 on a blank tape, through the three smaller candidate pairs | The crossing resets are exactly K−17 → K+50, K−39 → K+41, and K−96 → K+140 for the three increasing values of K. Another 5,147,278,302,365 first returns reach 3,706,040,377,703,662. Both machines have taken more than $1.28\times10^{44}$ raw transitions by this point. | [Cut certificates](BLANK_CROSSINGS.md) · [Exact second crossing](EXACT_SECOND_758.md) · [Final jump and timing](JUMP_AFTER_THIRD.md) |
| #758 / #153 on blank through the fourth pair | The consecutive reset seeds are $K-35$ and $K+65$ for $K=17,430,344,744,167,562$. After precisely 10,747,030,481,905 more returns both reach 18,378,934,934,402,308. | [7,100 grid windows and exact crossing](POWER_CROSSINGS_758.md) · [Raw timing](FOURTH_GATEWAY_758.md) |
| A(1,c) with H − 12,000,000 ≤ c ≤ H − 3,403,055 | All 8,596,946 reach A(1,H), which halts on macro call 307. The next larger seed skips H. | [Basin and boundary check](RANKINGS.md) |
| A(1,c) with H − 64,000,000 ≤ c ≤ H − 3,403,055 | All 60,596,946 halt. The extension also allows trajectories that halt on the way. | [Descending induction and resumable verifier](COVER_758.md) |
| A(1,c) with H − 11,177,976,427,786 ≤ c ≤ H − 3,403,055 | All **11,177,973,024,732** reset seeds halt. A cover of every seed through distance 10 trillion overlaps the outer halting interval. | [Universal proof and replay](UNIVERSAL_758.md) · [Outer interval](GATEWAYS_758.md) |
| A(1,c) with H − 33,533,929,283,358 ≤ c ≤ H − 3,403,055 | All **33,533,925,880,304** reset seeds halt. The 36-band universal calculation joins the earlier basin to the scale-7 corridor. | [Proof, four further corridors and replay](LOWER_SCALE_GATES_758.md) |

## Following the actual blank trajectory

The forward proof starts at A(0,1) after two raw steps. Direct execution takes the reset seed 3 to 100,008, and 2,435 independently checked windows place the orbit in [1,059,491,543,272,883, 1,059,491,543,277,883]. This need not select its lower endpoint. The previously verified confluence applies everywhere in the window. A separate 42-window bridge also feeds the first candidate calculation directly. Those crossings excluded the first three specified terminals. The [subsequent crossing](POWER_CROSSINGS_758.md) excludes the fourth and reaches the current blank checkpoint. [Exact crossings, algorithms and commands](BLANK_CROSSINGS.md) · [Raw-time lower bound](MASS_CLOCK_758.md)

At the central cut near H, a complete backward search excludes all five previously exhibited 98-copy paths from blank. More generally, the first 395 surviving blocks at the crossing cannot repeat a pattern of period at most 13. The verifier checks ancestry back to any possible reset, permitting earlier exceptional branches. Longer and nonperiodic words remain possible. [Inverse searches](CUT_ANCESTRY_758.md)

A specified 397-block itinerary from a reset determines at most four candidate reset seeds once its parity and initial jump count are known. Even reset origins in a macroscopic interval below H return within 300 calls. The case of an old odd reset still requires a reachability argument. A concrete state visited on the earlier orbit also shows why exact mass, the indicated finite residues and 1,024 angular bins alone allow a false infinite continuation. [Reconstructing reset origins](RESET_WORDS_758.md) · [Blank-reachable counterexample to the finite description](ANGULAR_758.md)

An earlier test looked for an ordinary affine period. The first 8,192 returns after the checkpoint at 3,706,040,377,703,662 reached **3,706,040,379,351,922**. None contained a qualifying word. The subsequent [periodicity proof](FINITE_AFFINE_PERIODS_758.md) excludes every ordinary affine period from any starting state. [Certificate and blank-tape replay](EXCURSION_POWERS_758.md)

## What would decide both machines

A new route would settle the full machine without predicting which terminal it hits. If the actual blank trajectory had fewer than exponentially many length-$n$ fine rule words, an infinite continuation would contradict the [positive entropy theorem](ALL_ORBIT_ENTROPY_758.md). An upper bound strictly below $(\log3)/8$ per individual counter call would already suffice. Proving such a bound for the blank orbit remains open.

A proof that the blank orbit reaches **any** state in the larger halting interval suffices. An earlier halt also settles both. At 265 additional scales, sufficiently deep reset entry in a specified interval restricts the eventual exit to at most 20 candidates. There are 1,722 candidates in total and eight scales have exactly one. A proof connecting those exits across the gaps could give a route to the halting intervals. [Scaled reset intervals](SCALED_GATES_758.md) One way to make the entry question precise uses the integer mass $W=a+2c$. It grows by at least 3 and at most 9 at each continuing map update. An infinite trajectory must therefore cross the middle of the halting interval in mass. The value of the first counter at that crossing matters.

**A reset in the preceding 7,451,983,528,956 map calls at the upper crossing would decide both machines.** Set $B=H-33,533,929,283,358$ and $U=H-3,403,055$. On a hypothetical infinite blank orbit, take the first state with $W>2U+1$. The most recent preceding reset has parameter at most $U$. Avoiding the halting interval would require that reset to have parameter at most $B-1$. The resulting minimum mass gain, $2(U-B)+3$, exceeds nine times 7,451,983,528,956. Whether the blank orbit has a sufficiently recent reset there remains open. [Interval proof and certificate](LOWER_SCALE_GATES_758.md)

* An orbit escaping the joined halting interval must switch between the ordinary bulk move and the odd/odd jump at least **5,689,983,720 times**. At the central crossing, its right counter must exceed 16,777,215. The part of its left counter plus one remaining after all factors of three are removed must exceed 67,108,864. These restrictions apply to the actual blank orbit if it continues indefinitely. [Counter bounds and switch proof](AXES_758.md)
* At the threshold $W=2(H-10\,000\,000)+1$, every crossing with a reset in the preceding 4,000 updates leads to a known halt. Exhausting the possible recent resets gives 745 distinct crossing states. A proof that the actual crossing has such a recent reset would close the problem. The same calculation identifies an exceptional branch that forces a return into the halting interval in 787 updates when it occurs with enough room before the upper edge. [Cut argument and checker](CUT_758.md)
* A general bound that prevents a single excursion from skipping the entire interval would also suffice, provided it covers an excursion that never returns. Merely bounding jumps **between** returns leaves that case open. At one fixed mass near H all $2^{144}$ words of length 144 built from two specific nonreturn blocks occur from some starting state. A proof may be able to exploit the fact that only one trajectory is reachable from blank. [Construction and limits of a cut search](CUT_758.md)
* Neighboring reset seeds can often be identified exactly. Every pair A(1,4q−1), A(1,4q+1) for q ≥ 1 merges. There is a corresponding rule for even seeds with explicit boundary cases. These rules can reduce a backward reachability search. [Identities and proof](reset_pairs.md) · [Checker](check_reset_pairs.py)
* Exhausting all incoming paths to the exact terminal reached from H gives just two possible last resets, H−2 and H. Analogous searches for the three published smaller candidate pairs also terminate. The nearest pair can be skipped in one excursion. Its exact 93-update bypass is a test case for any proposed crossing theorem. [Complete reverse graphs and bypass](TERMINALS_758.md)
* The fine terminal word for H recurs at all exponents $m=292+242660k$ for integers $k\ge0$. Allowing all bulk residues in its coarser terminal word gives exactly two halting seeds through H, namely H−2 and H. A search for a smaller halter must allow a different terminal itinerary, or a preceding return. [Proof and exhaustive search](LIFTS758.md)
* Each exponent in that family has two or four explicit even reset seeds that lead to its halt. At sufficiently high exponents, every even seed in the translated twelve-million-wide strip overshoots its target on its first return. [Moving preimages and uniform return formula](MOVING_SEEDS758.md)

## Running the checks

Use Python 3.10 or later, with assertions enabled, from this directory. The Python scripts use only the standard library. The forward window check uses C++17. The verifier for the large halting intervals also uses GMP.

```sh
python3 check_bb33.py
python3 timing_758.py
python3 jump_758.py
python3 check_confluence.py
python3 check_frontier_exit.py
python3 check_reset_pairs.py
python3 check_758_lifts.py
python3 check_758_moving_seeds.py
python3 verify_cut.py
python3 check_cut_residues.py
python3 terminal_forest_758.py
```

The following commands replay the second forward interval, the full four-holdout checks and the extended halting interval. Allow several minutes and roughly 1–2 GiB of memory for the full Python checks. The last command prints the covered halting interval for both parities. To extend it, use the bounds and continuation instructions in [COVER_758.md](COVER_758.md).

```sh
c++ -O3 -std=c++17 cover_frontier.cpp -o /tmp/bb33-cover-frontier
/tmp/bb33-cover-frontier
python3 check_bb33.py --full
python3 cover_758.py --far 64000000 --node-limit 2000000
```

For a complete replay of the forward crossings run `python3 check_blank_crossings.py --jobs 4`. The large-integer compilation and resumption commands are in [GATEWAYS_758.md](GATEWAYS_758.md). A separately checked 26-digit candidate has two 53-seed halting intervals, but 20,000 consecutive earlier seeds bypass its terminal. [Alternate target check](check_alternate_wall_758.py)
