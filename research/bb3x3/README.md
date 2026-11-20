# BB(3,3) holdouts and the #758 blank-tape proof

## Proof status and mathematical priority

**The decision is still missing a uniform excursion or transport theorem.** The connected blank trajectory and the remote halting basin are established separately. To join them, it suffices to prove a closed family of reset seeds containing the current blank checkpoint whose excursions terminate and cannot jump past the basin. No such invariant has been proved, and the finite counts below do not give a proof ETA or a percentage complete.

The research priority is a mathematical argument retaining the correlation between the real direction, integer divisibility and physical guards. The existing joint real and binary-adic formulation now has an explicit finite-prefix version, including the unique compatible reset residue selected by each fine prefix. It is a formulation of the obstruction, not a decision. The strategy note gives the precise closing implication, an interior counterexample to a universal angular-separation shortcut, and criteria for the next family lemma. Large enumerations should serve an explicit closing theorem. [Proof strategy and obligations](PROOF_STRATEGY_758.md) · [Exact ordinary-excursion coding](SEPARATED_FACTORS_758.md)

## Established finite and structural results

**The blank-tape fate of #758 and its twin #153 remains open.** Both blank tapes now reach the exact common reset **150,124,733,170,248,900 = $3^{36}+30,097,873,249,779$**. The completed 4,831-window power-36 bridge is followed by two adaptive connections and exact gate mergers. These new connections use 240,440 locally verified return intervals and do not require a fixed input grid. Both encodings have already taken more than **3.9169625267 × 10⁴⁹ raw transitions** at the earlier power-36 checkpoint. A separate proof rules out every eventually periodic sequence of counter rules, from any physical starting configuration. An infinite orbit could still have aperiodic ordinary excursions or continue through infinitely many resets. A halt anywhere on the common orbit would settle both encodings. [New blank continuation and replay](post36_ladder_758.md) · [Completed power-36 bridge](power36_final_758.md) · [Raw-clock bounds](power36_clock_758.md) · [Global periodicity theorem](FINITE_AFFINE_PERIODS_758.md) · [Four-holdout rankings](RANKINGS.md)

**The halting corridors are joined through scale 21.** Every one of **160,391,744,210,490,562,488 consecutive reset seeds** below the large target halts. The latest extension checks 1,385,824 additional prefix cylinders; two directions outlast the common cutoff and are resolved separately by exact physical replay and guard clearances. A reset within **35,642,609,824,553,458,330 counter calls** before the specified mass crossing would settle blank. A bypass would require at least 4,221,528,741 distinct length-336 fine words on that passage. [Enlarged basin, proof and commands](TARGET_GAP_21_758.md) · [Earlier joined basin](TARGET_BASIN_758.md) · [Finite word-count condition](FACTOR_COMPLEXITY_758.md)

Ordinary states can also enter directly. Across the enlarged, trimmed scale-21 mass band, every odd/odd state with even $h=(a+1)/2$ between 2 and **3,036,773,634,391,198,935,066**, and even $u=(a+2c-1)/2$, reaches a basin reset within 553 counter calls. The full rectangle now contains 121,768,354,998,108,739,585,604,304,504,361,494,240,000 states. It reuses the completed angular exhaustion, including the direction whose separately checked return takes 508 calls, and verifies the larger physical perturbation. No reset-header ancestry is assumed. [Entry theorem across the wider band](scale21_entry_758.md) · [Complete angular rectangle](wider_even_entry_758.md) · [Earlier rectangle and inverse-jump criterion](NONRESET_ENTRY_758.md)

An exact membership test extends the even-coordinate range to **69,471,640,166,665,074,144,382,279,320,672,514** using at most 89 elementary angular updates per input. The new backward arithmetic check excludes every possible guard ambiguity through aligned depth 277 across the wider scale-21 mass band; its final depth has 764,815,183,667,524 candidate integer distances and no cut ancestors. The test leaves fewer than 8.496 in ten million of the specified even coordinates inconclusive, uniformly across that band. Every accepted state reaches a basin reset within 553 counter calls. This population bound does not establish which state the blank machine reaches. [Wider-band criterion and callable predicate](scale21_entry_758.md) · [Earlier angular classifier](entry_transport_758.md) · [Exact examples identifying the reachability gap](entry_transport_gap_758.md) · [Mixed inverse certificates and their scope](inverse_entry_758.md)

If the blank tape reaches the leading halting target, the estimated runtime is about **$2\times10^{415}$ original machine transitions**. The proved bounds under this condition are $2.10448\times10^{414}$ and $8.206\times10^{416}$. [Halting-time estimate, checks and alternatives](HALTING_TIME_758.md)

There are now exact simulation skips near every power of three and its double for exponents $m\ge20$. An [elementary-depth cutoff](ELEMENTARY_SKIP_758.md) computes an exact annular exit with $O(X^{0.856184})$ individual first-return queries. One skip below $3^{292}$ recovers about $4.03\times10^{134}$ first returns in 25 return-word evaluations. The difficult step is transporting the actual blank orbit across changes of word into the halting basin. Near the far end of the power-to-target gap there are more than $10^{41}$ distinct complete return words even on a single class of reset starts. A proof that assigns one case to each word would require at least that many cases. [Word-count obstruction and integer witnesses](HEADER_WORD_LOWER_BOUND_758.md) [Exact skipping rules and the proof strategy](EXPONENTIAL_SKIPS_758.md)

The reduction uses A(a,c) for a tape configuration carrying two nonnegative integer counters. One map update represents a variable number of raw machine transitions. A reset here means any visit to a = 1. The map and the equivalence of the encodings have published formalizations. This directory contains integer verification programs and their mathematical arguments. [Formal machine specifications](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB33/README.md) · [Counter transitions, timings and published checkpoint](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA)

The 8,006-window blank crossing ends with a 128,286,013,074,958-return flight. At the remote target scale, every reset in one interval of about $2.3997\times10^{136}$ seeds reaches the same specified checkpoint $Y+158{,}145{,}479{,}878$. The path from that checkpoint to the halting basin remains open. [Exact blank flight](DOUBLED_POWER35_758.md) · [Target-side common checkpoint](CHECKPOINT_Y_758.md) · [Return words actually taken from blank](BLANK_WORD_SPECTRUM_758.md)

One change of return word can be crossed uniformly for all 273 tested powers, from $3^{20}$ to $3^{292}$. The interval at exponent 35 is on the blank orbit. [Parity transfer across a word change](POWER_PARITY_TRANSPORT_758.md) · [Completed power-36 crossing](power36_final_758.md)

## Current proof and replay

| Part of the argument | Current result |
|---|---|
| Actual blank orbit | The complete power-36 bridge is followed by two adaptive singleton connections and exact outward gates. Both blank tapes reach the exact reset 150,124,733,170,248,900. The previous lower clock bound of $3.9169625267\times10^{49}$ raw transitions still applies. [New continuation and replay](post36_ladder_758.md) · [Inherited bridge](power36_final_758.md) · [Raw-clock bounds](power36_clock_758.md) |
| The halting target | All 160,391,744,210,490,562,488 reset seeds in the joined scale-21 interval below $H$ halt. The proof covers every reset origin, including two new directions with separately verified physical returns. [Scale-21 basin and verifier](TARGET_GAP_21_758.md) · [Inherited basin](TARGET_BASIN_758.md) · [Dyadic arithmetic](DYADIC_SURVIVAL_758.md) |
| The approach from $3^{292}$, conditional on entry | All starting seeds in each of eleven intervals have one exact later reset for their respective interval. The last of those checkpoints still has no proven connection to the halting basin. Another set of 381 intervals resolves the range close to the power into independent crossing problems. [Eleven exact mergers](ANNULAR_MERGERS_292_758.md) · [Power gates and connected portion](POWER_CUSP_758.md) · [Direct-halting words in this gap](POWER_CUSP_TERMINALS_758.md) |
| A long excursion with no intervening reset | Arbitrary ordinary motion can be simulated to a **finite mass cutoff** with an exact clock. Distinct directions give a practical limit on checking each word separately. [Finite simulation](ORDINARY_ATLAS_758.md) · [Lower bound for word enumeration](HEADER_WORD_LOWER_BOUND_758.md) · [Recovering a state from its directions](COARSE_RECONSTRUCTION_758.md) · [Terminal-free mass intervals](SIGNED_TERMINAL_STRIPS_758.md) · [Power-gate terminal sieve](BULK_TERMINAL_SIEVE_758.md) |

## How strong is the evidence for halting?

Halting is the leading conjecture for this pair. There is no calibrated probability for the blank tape. Three comparisons locate the uncertainty.

| Starting population | Proven outcome |
|---|---|
| The actual blank orbit, over 11,538,952,370,487 consecutive first returns | The longest gap was 134 counter calls. All but 753 returns followed two fixed patterns. [Exact profile](BLANK_RETURN_PROFILE_758.md) |
| Every reset seed from 1 through the 140-digit target $H$ | Fewer than three seeds per $10^{36}$ can fail to reach another reset within 1,086 calls. Any infinite blank orbit crossing the scale-10 halting interval must have selected an exceptional seed. [Whole-population bound and typical increment](QUICK_RETURNS_758.md) |
| Identical windows of 5,000,003 reset seeds around each of 257 direct terminal pairs | The large pair captures 3,837,489 starts before a live reset above it. The next-highest count is 29,620. In the much wider verified interval ending at $H$, 33,533,928,120,845 of 33,533,929,283,359 starts halt before returning above $H$. [Matched comparisons](TERMINAL_NEIGHBORHOODS_758.md) · [Boundary and all bypasses](AFTER_TARGET_758.md) |

At the midpoint of the scale-10 halting interval, almost every state sampled under several precise rules would halt. Even fixing an admissible 200-call incoming ordinary word gives an upper fraction of $2.966\times 10^{-12}$ for escaping under uniform sampling from the states realizing that word. The blank machine can select very rare states: at one known mass it executes 33 consecutive jumps from the only one of 9,189,467,467,201,156 physical states where that is possible. [Conditioned crossing counts and blank replay](CUT_DENSITY_758.md)

Every reset in an interval extending about $1.26\times10^{136}$ seeds above $H$ eventually reaches the same explicit checkpoint. Each of the 1,162,514 near-target overshoots joins it too. Its subsequent fate remains open. Repeating the original direct terminal word at the next admissible exponent changes the result completely: an offset interval whose 8,596,946 starts all halt at the original target passes the next target alive from every start. [Post-target checkpoint](AFTER_TARGET_758.md) · [Exact comparison at all lifted targets](LIFTED_BASINS_758.md)

## Continuing the blank proof

* **Scale 74.** A sufficiently early reset in the gate determines the exact midpoint configuration $A(2\cdot3^{36}-1,T-3^{36}+1)$, where $T=H-5G/4$ and $G=10^{10}3^{74}$. More generally, membership in a checked set of 701 states at the first midpoint crossing is equivalent to an actual gate visit by then. Starting from the gate's unique exit, the proof traverses the first change of word and reconverges a trillion reset values farther on. The connection to scale 73 remains open. [Midpoint and ancestry](SCALE74_ANCESTRY.md) · [Exact continuation from the exit](SCALE74_BRIDGE_758.md)
* **An alternative at the same crossing.** Missing the scale-74 gate altogether requires at least $10^{22}$ different length-401 fine words on that single passage. Missing the scale-21 halting interval requires at least 4,221,528,741 different length-336 fine words. The argument uses collinearity of repeated words and applies even to aperiodic trajectories. [Finite word-count theorem](FACTOR_COMPLEXITY_758.md) · [Entropy on an infinite orbit, including resets](ALL_ORBIT_ENTROPY_758.md) · [Recovering the integer state from a two-sided word](SEPARATED_FACTORS_758.md) · [Why modular survival alone admits false states](MODULAR_GATE_LIMIT.md)
* **Starting much closer to blank.** At 546 gates of the form $3^m$ or $2\cdot3^m$, every sufficiently deep entry leads to one specific checkpoint. At scales 7 through 10 below the large target, four more verified intervals lead to a halt. The original scale-10 interval contained 362,166,436,260,267 seeds. The [joined basin](TARGET_BASIN_758.md) now includes these intervals and every intervening gap through scale 21. [Scale-21 extension](TARGET_GAP_21_758.md) · [Halting intervals and transfer receipts](LOWER_SCALE_GATES_758.md) The blank chain reaches $2\cdot3^{35}+155{,}534$ across 8,006 windows, then the completed 4,831-window bridge reaches $3^{36}+112,032$. The adaptive continuation reaches $3^{36}+30,097,873,249,779$. [Adaptive connections](post36_ladder_758.md) · [Complete doubled-power flight](DOUBLED_POWER35_758.md) · [Complete power-36 bridge](power36_final_758.md) An earlier passage enters a verified interval of 633,739,014,317,117 seeds and crosses the fifth pair by the exact jump $K-98\to K+118$. [Fifth blank crossing](FIFTH_BLANK_CROSSING_758.md) · [Power-35 checkpoint and next gate](POWER35_BLANK_758.md) · [Power-gate checkpoints](POWER_GATES_758.md) · [Exceptional halting branches](EXCEPTION_TERMINALS_758.md)

* **Halting seeds at arbitrarily large scales.** Under the hypothesis that ordinary stretches become short relative to their starting mass, the actual orbit visits every fixed relative neighborhood of an infinite family of halting pairs with exponents $m=597+1200j$. The unresolved step is reaching a seed that leads to a halt inside such a neighborhood. [Exact family and proof](CUSP_TERMINALS_758.md) · [Actual returning trajectories with every fixed target congruence](TERMINAL_CONGRUENCES_758.md)

## Earlier checkpoints and their proofs

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

The forward proof starts at A(0,1) after two raw steps. Direct execution takes the reset seed 3 to 100,008, and 2,435 independently checked windows place the orbit in [1,059,491,543,272,883, 1,059,491,543,277,883]. This need not select its lower endpoint. The previously verified confluence applies everywhere in the window. A separate 42-window bridge also feeds the first candidate calculation directly. Those crossings excluded the first three specified terminals. The [subsequent crossing](POWER_CROSSINGS_758.md) excludes the fourth and reaches another exact checkpoint on the later connected chain. [Exact crossings, algorithms and commands](BLANK_CROSSINGS.md) · [Raw-time lower bound](MASS_CLOCK_758.md)

At the central cut near H, a complete backward search excludes all five previously exhibited 98-copy paths from blank. More generally, the first 395 surviving blocks at the crossing cannot repeat a pattern of period at most 13. The verifier checks ancestry back to any possible reset, permitting earlier exceptional branches. Longer and nonperiodic words remain possible. [Inverse searches](CUT_ANCESTRY_758.md)

A specified 397-block itinerary from a reset determines at most four candidate reset seeds once its parity and initial jump count are known. Even reset origins in a macroscopic interval below H return within 300 calls. The case of an old odd reset still requires a reachability argument. A concrete state visited on the earlier orbit also shows why exact mass, the indicated finite residues and 1,024 angular bins alone allow a false infinite continuation. [Reconstructing reset origins](RESET_WORDS_758.md) · [Blank-reachable counterexample to the finite description](ANGULAR_758.md)

An earlier test looked for an ordinary affine period. The first 8,192 returns after the checkpoint at 3,706,040,377,703,662 reached **3,706,040,379,351,922**. None contained a qualifying word. The subsequent [periodicity proof](FINITE_AFFINE_PERIODS_758.md) excludes every ordinary affine period from any starting state. [Certificate and blank-tape replay](EXCURSION_POWERS_758.md)

## What would decide both machines

A new route uses a single bit per counter update. Record 1 for the ordinary odd/odd jump and 0 for every other rule. If the blank trajectory is infinite, the exponential growth rate of its distinct length-$n$ binary words, measured with natural logarithms, is at least 0.06316617 per update. Proving a smaller upper bound for this one sequence would settle both machines as halting, without predicting the terminal. That upper bound remains open. [Binary-word theorem](COARSE_ENTROPY_758.md) · [Finite binary tests at two crossings](BINARY_PASSAGES_758.md) · [Earlier fine-rule theorem](ALL_ORBIT_ENTROPY_758.md)

A proof that the blank orbit reaches **any** state in the larger halting interval suffices. An earlier halt also settles both. At 265 additional scales, sufficiently deep reset entry in a specified interval restricts the eventual exit to at most 20 candidates. There are 1,722 candidates in total and eight scales have exactly one. A proof connecting those exits across the gaps could give a route to the halting intervals. [Scaled reset intervals](SCALED_GATES_758.md) One way to make the entry question precise uses the integer mass $W=a+2c$. It grows by at least 3 and at most 9 at each continuing map update. An infinite trajectory must therefore cross the middle of the halting interval in mass. The value of the first counter at that crossing matters.

For the latest basin set $B=H-160,391,744,210,493,965,542$ and $U=H-3,403,055$. On a hypothetical infinite blank orbit, take the first state with $W>2U+1$. The most recent preceding reset has parameter at most $U$. Avoiding the halting interval would require that reset to have parameter at most $B-1$. The resulting minimum mass gain, $2(U-B)+3$, exceeds nine times **35,642,609,824,553,458,330**. Therefore a reset within that many counter calls forces a halt. Whether the actual blank orbit has a sufficiently recent reset there remains open. [Scale-21 proof and certificate](TARGET_GAP_21_758.md)

* An orbit escaping the joined halting interval must switch between the ordinary bulk move and the odd/odd jump at least **5,689,983,720 times**. At the central crossing, its right counter must exceed 16,777,215. The part of its left counter plus one remaining after all factors of three are removed must exceed 67,108,864. These restrictions apply to the actual blank orbit if it continues indefinitely. [Counter bounds and switch proof](AXES_758.md)
* At the threshold $W=2(H-10\,000\,000)+1$, every crossing with a reset in the preceding 4,000 updates leads to a known halt. Exhausting the possible recent resets gives 745 distinct crossing states. A proof that the actual crossing has such a recent reset would close the problem. The same calculation identifies an exceptional branch that forces a return into the halting interval in 787 updates when it occurs with enough room before the upper edge. [Cut argument and checker](CUT_758.md)
* A general bound that prevents a single excursion from skipping the entire interval would also suffice, provided it covers an excursion that never returns. Merely bounding jumps **between** returns leaves that case open. At one fixed mass near H all $2^{144}$ words of length 144 built from two specific nonreturn blocks occur from some starting state. A proof may be able to exploit the fact that only one trajectory is reachable from blank. [Construction and limits of a cut search](CUT_758.md)
* Neighboring reset seeds can often be identified exactly. Every pair A(1,4q−1), A(1,4q+1) for q ≥ 1 merges. There is a corresponding rule for even seeds with explicit boundary cases. These rules can reduce a backward reachability search. [Identities and proof](reset_pairs.md) · [Checker](check_reset_pairs.py)
* Exhausting all incoming paths to the exact terminal reached from H gives just two possible last resets, H−2 and H. Analogous searches for the three published smaller candidate pairs also terminate. The nearest pair can be skipped in one excursion. Its exact 93-update bypass is a test case for any proposed crossing theorem. [Complete reverse graphs and bypass](TERMINALS_758.md)
* The fine terminal word for H recurs at all exponents $m=292+242660k$ for integers $k\ge0$. Allowing all bulk residues in its coarser terminal word gives exactly two halting seeds through H, namely H−2 and H. A search for a smaller halter must allow a different terminal itinerary, or a preceding return. [Proof and exhaustive search](LIFTS758.md)
* Each exponent in that family has two or four explicit even reset seeds that lead to its halt. At sufficiently high exponents, every even seed in the translated twelve-million-wide strip overshoots its target on its first return. [Moving preimages and uniform return formula](MOVING_SEEDS758.md)

## Running the checks

Use Python 3.10 or later, with assertions enabled, from this directory. The Python scripts use only the standard library. The forward window check uses C++17. The verifier for the large halting intervals also uses GMP.

The latest proof checks are:

```sh
python3 power36_final_758.py
python3 power36_clock_758.py
python3 wider_even_entry_758.py
python3 entry_transport_758.py
python3 entry_transport_gap_758.py
```

These validate the archived crossing and angular-exhaustion receipts and rerun the new gate, clock, guard, margin and boundary arguments. The exponent-88 reverse-guard check takes several minutes. The linked proof notes give the separate commands for regenerating the exhaustive receipts.

The earlier checks remain available:

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
