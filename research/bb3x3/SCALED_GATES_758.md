# Tripling the distance from the fixed halting seed

Write D=H−s for the distance of a reset seed s below the known halting seed H. For each n from 0 through 264 inclusive, put Gₙ=10¹⁰·3ⁿ. **Every odd reset seed with Gₙ≤D≤3Gₙ/2 has the same exact first-return word**

$$
 J^{292} L^8 J L^6 J^{264-n} L R .
$$

Here L is either ordinary bulk update and R is the even-left return. Every even seed in the same interval takes the [even-corridor word](RESET_WORDS_758.md). Two same-parity endpoints verify each whole interval because the left counter is nonincreasing and the right counter nondecreasing along a common ordinary word as the initial seed increases. The verifier checks that each endpoint's intermediate left counter stays above 1; the smaller of those counters bounds the entire interval from below.

## The actual exits of a deep traversal

At each scaled interval there are **at most 20 possible exit seeds**, irrespective of its width, for any trajectory that visits a reset at distance D in [Gₙ+39,000,000, 3Gₙ/2]. Across the 265 intervals there are 1,722 such exits in total. Eight intervals have exactly one. The exit means the first reset with distance strictly below Gₙ. The checker gives a positive offset e, so the exit is at **distance Gₙ−e** and **seed H−Gₙ+e**.

The even first return increases the seed by an odd value at most 615, giving an odd seed. Odd seeds remain odd. To compute the exact odd gain, put k=264−n and let b count how many of the fourteen Ls preceding Jᵏ have right counter 3 modulo four. If that prefix ends with second counter r, the last L has its larger mass increase exactly when r−2k is 3 modulo four. Indeed the left counter stays 3 modulo four during this J run. The odd seed increases by

$$
 626+2k+2\big(b+[r-2k\equiv3\pmod4]\big).
$$

The gain is even and at most 1,184. D modulo 65,536 determines every bulk residue in the formula. J consumes no bits of residue precision. On each L the right update sends an increment divisible by four to three halves that increment, consuming one bit. Starting with sixteen bits therefore leaves the necessary two bits after fourteen Ls. This period concerns the gain where the indicated word is legal.

On the 32,768 even classes of D, iterate the exact countdown gain modulo 65,536. After at most 32,768 steps every residue is on a cycle. The possible preceding even-seed move and all those steps consume less than 39,000,000 in distance. For a cycle of length ℓ, the sum of countdown gains around it is an integer multiple w of 65,536. There are exactly w possible integer lifts of exits through any fixed cut, called its winding number. To enumerate them, take each cycle vertex d and the unique integer x in [Gₙ,Gₙ+65,535] congruent to d. Record e=Gₙ−x+gain(d) exactly when e>0. Distinct cycle edges produce distinct exits because the map permutes its cycle vertices. Conversely each listed exit has a backward path along cycle states to the high edge of the corridor. These are exact possibilities for starts inside the stated deep interval, including all such starts attainable from blank.

At n=0 the single cycle has length 841 and winding 15; the offsets are 42, 138, 192, 268, 356, 422, 508, 608, 698, 742, 820, 874, 958, 1058 and 1146. At n=1 the winding is six and the offsets are 64, 240, 406, 598, 828 and 1026.

The eight singleton exits are (n,e) = (74,698), (80,478), (135,732), (194,246), (204,526), (225,144), (247,64) and (254,490). For instance the scale-74 exit is A(1,H−10¹⁰·3⁷⁴+698).

An inter-gate proof can begin at just these seeds. For example, for n≥1 it suffices to show each listed seed halts or reaches a reset with distance in [Gₙ₋₁+39,000,000, 3Gₙ₋₁/2]. This would link that gate to the preceding one. The index n=0 still requires a connection to the already certified halting region; see the separate numerical gateway results. The scale construction alone does not connect successive gates or establish that the blank trajectory enters one deeply.

## A common cover between the large corridors

Let x=D/3ⁿ range over [10¹⁰,3·10¹⁰]. One finite set of 27,423 closed subintervals of x simultaneously verifies a halt or return within **604 counter calls** for every odd seed in those subintervals at each n from 0 through 240. Their total length is exactly 19,491,376,875 out of 20,000,000,000, or **97.456884375% of normalized real length**. The remaining 53,333 interval leaves are undecided by this check. This is a length statement about countdown distances, not a probability for blank, and it does not certify contiguous travel through the remaining gaps.

To reproduce the bounds, write P=32,768 and C=55,837,100. After the prefix J²⁹² L⁸ J L⁶ let X=a+1. Then PX=CD+βᵣ, with r=D mod P. Propagating a change of P through all fourteen Ls preserves each input residue modulo four, so the shift in X and total mass gain are independent of the quotient. A check of the even residues gives −203,238,392≤βᵣ≤106,061,328. The distant endpoints verify the whole common prefix is legal. Align scales with another 263−n moves J. At that point

$$
 X=3^{263}(Cx+\beta_r/3^n)/P,\quad
 W=2(H-D)+1+g+4(263-n),\quad1242\le g\le1298 .
$$

Here g is the common-prefix mass gain. A positive final right counter c=(W−X+1)/2 guarantees all the aligned Js were legal: the last J requires X≤W−1, and the smaller preceding left counters satisfy their guards. For an interval of x, bound X and W using these formulas over all 241 scales, round X outwards to multiples of four and the c bounds outwards to odd integers. The two opposing corner states cover the whole rectangle under the same order as the reset comparison. The checker accepts a leaf only when both corners take the same ordinary word through an even-left decision that halts or returns. The longest accepted suffix takes 34 calls, and the initial prefix and alignment take at most 570.

## Why transporting a catalog of base words leaves gaps

At scale 240, at least **2¹²⁰ distinct post-alignment histories** occur from reset seeds with x in the same interval [10¹⁰,3·10¹⁰]. Scale zero contains only 10,000,000,001 odd reset seeds in that entire interval. Thus preserving individual branch words from base seeds cannot account for all larger-scale histories. The construction concerns all reset starts at that scale and does not imply any lower bound on histories reachable from the sparse preceding gate exits.

Here is an integer construction. Restrict D=Pz. At scale 240 the alignment has 23 Js. In the [reset coordinates](RESET_WORDS_758.md) u=(W−1)/2, h=(a+1)/2, d=(u−h)/2, the aligned u has slope −P as a function of z, and h has slope 3²³C/2. The slope of d is odd. Prescribe an initial J and B (two specific rule (b) moves), then any 120 letters from J and B. If p is the number of Bs, the terminal d is (Az+C₀)/4ᵖ with A odd. Indeed J gives d′=3d−u+1 and B gives d′=(9d+20)/4. One congruence on z modulo 4ᵖ makes the final d integral and therefore all the B input counters divisible by four, since each intervening multiplier is odd.

Choose the admissible z closest to the real root d_final=u_final/4. To verify this yields legal inputs uniformly, use the positive-coefficient identity from [RESET_WORDS_758.md](RESET_WORDS_758.md). Write R=4ᵖ/Q with Q=3ʲ⁺²ᵖ, j the number of Js. At the root the aligned h equals θu+e with 0≤e≤8·122+4. The coefficient θ lies in [5/27,1/3], since the initial J and B invert the final fraction by θ↦θ/3 and θ↦(4θ+5)/9 in reverse chronological order. The verifier checks that h is below 5u/27 at the lower distance bound moved inward by P·4¹²¹ and above u/3+8·122+4 at the upper bound moved inward by the same amount. The affine h−θu−e has positive slope, so rounding to the admissible class stays in the permitted distance interval.

Rounding z perturbs h_final−u_final/2 by at most (3²³C/2+P)Q, which is less than H/100 even at Q=3²⁴³. The terminal d is consequently more than H/10 from each boundary 0 and u_final/2. The reverse J/B margin bound in [CUT_758.md](CUT_758.md) keeps all margins above H/(10·3¹²²)>100. All individual guards hold. Distinct words give distinct input seeds by determinism. This explains why the sparse entering orbits matter for an attempted full decision.

Run `python3 scale_clauses_758.py` to verify all 265 corridors and count their exits, or append `--scale N` for one exact list. Run `python3 scale_transport_758.py` for the joint normalized cover, the integer inequalities and 1,156 witness checks. Both scripts use the existing counter map.
