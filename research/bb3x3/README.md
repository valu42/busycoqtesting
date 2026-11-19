# BB(3,3) holdouts and the #758 blank-tape proof

**The blank-tape fate of #758 and its twin #153 remains open.** They reach identical configurations after reflection and relabeling. A decision for one decides both. Our strongest halting result is a contiguous interval of 60,596,946 reset seeds. Our forward calculation starts at the community's reported blank-orbit checkpoint and proves that more than 20 trillion neighboring starts all reach a single later state. Connecting the blank orbit to a halt remains the goal. The other three holdout classes, their encodings, and their expected behavior appear in [RANKINGS.md](RANKINGS.md).

The reduction uses A(a,c) for a tape configuration carrying two nonnegative integer counters. One map update represents a variable number of raw machine transitions. A reset here means any visit to a = 1. The map and the equivalence of the encodings have published formalizations. This directory contains integer verification programs and their mathematical arguments. [Formal machine specifications](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB33/README.md) · [Counter transitions, timings and published checkpoint](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA)

## Where the two calculations stand

Let $H=(3^{307}-8\,282\,708\,212)/13\,959\,275$. The following statements use inclusive endpoints.

| Starting point | Verified consequence | Reproduction or argument |
|---|---|---|
| #758 on a blank tape | Reaches A(0,1) at step 2, then A(1,3). At exactly 3,251,620,479,139,366,879 raw transitions the counters are a = 107 and c = 5,090,319. | [Raw clocks and 400 raw-tape checks](timing_758.py) |
| Published blank checkpoint with a = 1 and c = 1,059,491,543,272,883 | The next 254,074,710,617 returns reach c = 1,079,817,520,122,241, with exactly 1,138,748,236,895,051,391,487,973,286,265,103,628,580,163 raw transitions between checkpoints. | [Affine return and exact clock](jump_758.py) |
| Every reset seed 1,059,491,543,272,883 ≤ c ≤ 1,079,817,520,122,229 | All 20,325,976,849,347 reach the identical reset at c = 1,079,817,520,208,950. This also advances the published checkpoint. Its blank-to-checkpoint prefix comes from the community run. | [Proof and verifier](CONFLUENCE.md) |
| Every reset seed 1,059,491,543,272,883 ≤ c ≤ 1,080,000,000,000,000 | All **20,508,456,727,118** reach a = 1, c = **1,080,000,000,055,450**. A second interval check and an exact bridge over 86,720 intervening seeds extend the previous row. | [Second interval and exit check](FRONTIER.md) · [Bridge](check_confluence.py) |
| A(1,c) with H − 12,000,000 ≤ c ≤ H − 3,403,055 | All 8,596,946 reach A(1,H), which halts on macro call 307. The next larger seed skips H. | [Basin and boundary check](RANKINGS.md) |
| A(1,c) with H − 64,000,000 ≤ c ≤ H − 3,403,055 | All 60,596,946 halt. The extension also allows trajectories that halt on the way. | [Descending induction and resumable verifier](COVER_758.md) |

## The obligation that would decide both machines

A proof that the blank orbit reaches **any** state in the larger halting interval suffices. An earlier halt also settles both. One way to make the entry question precise uses the integer mass $W=a+2c$. It grows by at least 3 and at most 9 at each continuing map update. An infinite trajectory must therefore cross the middle of the halting interval in mass. The value of the first counter at that crossing matters.

**A sufficient bound on the single excursion that crosses the upper edge is 13,465,988 map updates.** Set $B=H-64,000,000$ and $U=H-3,403,055$. On an infinite blank orbit, consider the first state with $W>2U+1$. A reset exists strictly before it because the orbit starts through A(1,3). If the most recent such reset was A(1,r), then $r\le U$. To have missed the halting interval it must satisfy $r\le B-1$. From that reset to the crossing the required gain in mass is at least $2(U-B)+3=121,193,893$. Even 13,465,988 updates gain at most 121,193,892. Thus a proof that this particular crossing has a reset in its preceding 13,465,988 updates rules out an infinite blank orbit. This bound on the actual trajectory remains unproved.

* Within the trimmed halting interval, an infinite orbit must switch between the ordinary bulk move and the odd/odd jump at least **24,982 times** without resetting. Bounds from both directions exclude 99 consecutive copies of one particular three-move word at the central cut. There are actual integer examples with 98 copies, and congruence tests alone admit that word indefinitely. A bound that works across changing words would address the remaining case. [Switch count](CUT_758.md) · [Two-sided test and sharp example](cut_residues.md)
* At the threshold $W=2(H-10\,000\,000)+1$, every crossing with a reset in the preceding 4,000 updates leads to a known halt. Exhausting the possible recent resets gives 745 distinct crossing states. A proof that the actual crossing has such a recent reset would close the problem. The same calculation identifies an exceptional branch that forces a return into the halting interval in 787 updates when it occurs with enough room before the upper edge. [Cut argument and checker](CUT_758.md)
* A general bound that prevents a single excursion from skipping the entire interval would also suffice, provided it covers an excursion that never returns. Merely bounding jumps **between** returns leaves that case open. At one fixed mass near H all $2^{144}$ words of length 144 built from two specific nonreturn blocks occur from some starting state. A proof may be able to exploit the fact that only one trajectory is reachable from blank. [Construction and limits of a cut search](CUT_758.md)
* Neighboring reset seeds can often be identified exactly. Every pair A(1,4q−1), A(1,4q+1) for q ≥ 1 merges. There is a corresponding rule for even seeds with explicit boundary cases. These rules can reduce a backward reachability search. [Identities and proof](reset_pairs.md) · [Checker](check_reset_pairs.py)
* Exhausting all incoming paths to the exact terminal reached from H gives just two possible last resets, H−2 and H. Analogous searches for the three published smaller candidate pairs also terminate. The nearest pair can be skipped in one excursion. Its exact 93-update bypass is a test case for any proposed crossing theorem. [Complete reverse graphs and bypass](TERMINALS_758.md)
* The fine terminal word for H recurs at all exponents $m=292+242660k$ for integers $k\ge0$. Allowing all bulk residues in its coarser terminal word gives exactly two halting seeds through H, namely H−2 and H. A search for a smaller halter must allow a different terminal itinerary, or a preceding return. [Proof and exhaustive search](LIFTS758.md)
* Each exponent in that family has two or four explicit even reset seeds that lead to its halt. At sufficiently high exponents, every even seed in the translated twelve-million-wide strip overshoots its target on its first return. [Moving preimages and uniform return formula](MOVING_SEEDS758.md)

## Running the checks

Use Python 3.10 or later, with assertions enabled, from this directory. The Python scripts use only the standard library. The second forward interval also uses a C++17 compiler.

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
