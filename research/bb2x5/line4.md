# Exact timed reductions for formal holdout 4

The machine is `1RB3LA1LA1RA3RA_2LB2RA---4RB1LB`. After exactly 93 defined instructions on blank it is in B(2,7) in the **configuration** notation below. It reaches its first three A(6,b) returns from B at (b, elapsed defined instructions) = (71, 6393), (393, 172248), and (3081, 10139877). At return 1,024 its execution time exceeds 10¹⁸⁰². The blank execution halts if and only if one of the returns has b = 24·3ⁿ − n − 11 for some integer n ≥ 0. No return on blank can reach a halting target whose exponent n is 1, 15, 22, or 36 modulo 42. These four classes eliminate 2/21 of the candidate exponents. Whether one of the remaining targets is reached stays open.

Racheline published the two normal forms and the main unweighted successor rules in March 2025. Here the local tape rules include exact times, the missing A(a,0) case for a ≥ 2, and the boundary cases for small B configurations. An affine run-length interpreter certifies the rules for all their parameters against the literal instruction table. [Racheline's analysis](https://wiki.bbchallenge.org/wiki/1RB3LA1LA1RA3RA_2LB2RA---4RB1LB)

## Local rules

Write C(a,k,b) for a state-A head between the words 1 4ᵃ 1ᵏ and 1ᵇ 2. Then A(a,b) is C(a,3,b). In B(a,b) the TM is also in state A, between 1 4ᵃ 1ᵇ and a single 1. Every exterior cell is blank. Each positive duration in the table counts transitions whose instruction is defined. The last configuration of a halting rule is in B on symbol 2.

| Start | End | Duration |
|---|---|---:|
| C(a+1,k,b+2) | C(a,k+3,b) | 4k+8 |
| C(0,k,b+3) | A(k+1,b) | 2k+13 |
| C(0,k,2) | B(k+1,2) | 2k+12 |
| C(0,k,1) | halt | 2k+5 |
| C(0,k,0) | B(k−2,7) | 2k+60 |
| C(1,k,0) | B(k+1,5) | 6k+46 |
| C(a+2,k,0) | B(a,k+4) | 8k+22 |
| C(a+1,k,1) | B(a,k+2) | 4k+7 |
| B(a+3,b) | B(a,b+7) | 12b+56 |
| B(0,b+4) | A(6,b) | 3b+69 |
| B(1,b) | B(b+1,7) | 6b+76 |
| B(2,b) | B(b+4,5) | 10b+74 |

The parameters a and b range over nonnegative integers and k ≥ 3. In particular A(a+2,0) reaches B(a,7) in 46 steps. The four exceptional inputs B(0,b), for 0 ≤ b ≤ 3, reach B(0,4), B(3,7), halt, and B(6,2) in 33, 107, 55, and 65 steps respectively.

For example, consider the first rule with the head at the first of the next two ones. The first left pass writes k+1 threes. A4 turns its anchor into 3 and moves right. The A3 steps restore the k+1 ones. This takes 2k+3 steps. The second left pass sees k+1 old ones behind the head and turns the anchor from 3 to 1. In 2k+5 more steps the head is over the untouched suffix with k+3 ones on its left. The opaque left and right contexts stay intact.

The accompanying symbolic interpreter represents run lengths as exact affine forms on a nonnegative integer n. It can batch consecutive equal instructions only when the machine state and direction permit the whole span. Each comparison and each positive run length must hold throughout n ≥ 0. An unreadable sentinel represents arbitrary contexts in rows where a distant tape region is irrelevant. A rule succeeds only when the literal machine has reached the stated tape, state and head after the claimed duration, or the first undefined instruction on a halting row. Testing the parameter values 0 through 11 and proving the single symbolic case 12+n exhausts the natural numbers. Zero-length and positive-length runs can then be handled with definite branch conditions throughout the symbolic replay.

## From blank

From A(a,b), the first local rule consumes j = min(a,⌊b/2⌋) pairs. Its cost sums to 6j²+14j and leaves C(a−j,3+3j,b−2j). Exactly one terminal C rule applies. From B(a,b), let q = ⌊a/3⌋ and r = a mod 3. Consuming q triples takes q(42q+12b+14) transitions, leaving B(r,b+7q). The table handles its boundary. The small exceptions never arise on blank. The initial B parameter is 7, every successor B from a B boundary has second parameter 5 or 7, and the only C boundary emitting a B with parameter below 5 gives B(k+1,2), with k ≥ 3, so q ≥ 1.

A full A-to-A round goes from A(a,b) to A(3a+4,b−2a−3) when b ≥ 2a+3, in 6a²+20a+19 steps. Starting at A(6,b), n consecutive rounds leave a′ = 8·3ⁿ−2 and b′ = b−8(3ⁿ−1)+n and cost 48(9ⁿ−1)−16(3ⁿ−1)+3n. Take the largest n with b′ ≥ 0. The only possible halt from this phase requires b′ = 2a′+1, equivalently b = 24·3ⁿ−n−11. Conversely this value of b selects the specified n and forces the halt. An orbit that subsequently stays forever in B-phase transitions runs forever, because every transition is finite, defined, and of positive length.

On any return from B to A(6,b), that b increases strictly relative to the previous such A(6,b). The table machine always writes nonzero symbols, so the length of its occupied interval never decreases. Every B(0,b+4) to A(6,b) return starts with an all-ones left half of length b+5 before the head on 1, hence the head sweeps to the leftmost virgin blank and writes a nonzero there. At A(6,b) the occupied length is 11+b. Even if one speaks only of the returns that actually occur, they therefore visit distinct integer values in increasing order.

A separate finite residue count explains why terminating B excursions are common on free inputs. Fix the second B parameter b ≥ 4. For a congruence class of a modulo 3ᵗ that has avoided residue zero for t B reductions, varying a by 3ᵗ varies the current first coordinate by precisely 7ᵗ and leaves the current second parameter fixed. This follows by iterating the r=1,2 rules after grouping triples. Since 7 is invertible modulo 3, exactly two of its three lifts modulo 3ᵗ⁺¹ keep the next residue nonzero. Induction from t=0 gives exactly 2ᵗ surviving classes among 3ᵗ; the set of forever-B initial first coordinates has natural density zero. This count places no pointwise bound on the particular B excursions reached by blank.

## Halts after arbitrarily many returns

There is an explicit infinite family of initial configurations that halt after making an arbitrarily prescribed number of B-to-A returns. This concerns auxiliary starting tapes. In this formula n describes the number of complete A-to-A rounds in *each* return.

Fix n ≥ 0, put p = 3ⁿ, L = 8(p−1)−n, H = 24p−n−11, and choose j ≥ 0 with

    (3ʲ−1)(3n+11)/2 ≤ 16p−3.

From A(6, H−(3ʲ−1)(3n+11)/2) the machine makes exactly j B-to-A macro returns before the terminal A phase halts. For any fixed j the inequality holds for all sufficiently large n.

To see this, write a = 8p−2 and u = b−L. Once n rounds finish, an interior input 0 ≤ u ≤ 2a−4 with u ≡ 2a−1 (mod 3) makes a direct B-to-A return. If u=2s, the B state is B(a−s−2,3s+7). If u=2s+1, it is B(a−s−1,3s+5). The first coordinate is divisible by 3 in either case. Using the B(0,·) boundary formula after grouping triples gives the same returned value

    b′ = (7a+u−5)/3 = (b + 48p+n−11)/3.

Write K = 48p+n−11. As long as such returns stay in the same width, K−2b goes to (K−2b)/3. This also bounds the number of consecutive interior returns at that width by the exponent of 3 dividing K−2b, since K−2b > 0 everywhere in the width.

Now let bⱼ = H−(3ʲ−1)(3n+11)/2. The inequality ensures bⱼ ≥ L, and monotonicity in j gives this for all the smaller indices. For j ≥ 1 the gap from H is at least 3n+11, so u ≤ 2a−4. The identity bⱼ+K = 3bⱼ₋₁ implies the required congruence on u and proves the indicated return. The last value b₀=H forces the halt. For example n=4 gives 1009 → 1630 → 1837 → 1906 → 1929 → halt, where each arrow between numbers includes a B-to-A return.

## Four impossible halt levels modulo 42

On the blank orbit the halting target Hₙ = 24·3ⁿ−n−11 can never be reached for

    n ≡ 1, 15, 22, 36   (mod 42).

This excludes four entire arithmetic progressions of candidate exponents. It uses the actual initial return A(6,71).

First consider any return value y after the first return. If the preceding A phase enters B and subsequently makes a grouped B-to-B transition before returning to A, the last grouped B step starts at B(3q,5) or B(3q,7). It gives y = 7q+1 or 7q+3. Consequently y outside residues 1 and 3 modulo 7 must have come directly from the first B emitted by the preceding A phase.

Write m for that preceding phase's number of A-to-A rounds, a = 8·3ᵐ−2, and u for its residual right-hand count. The special inputs u = 2a−2, 2a, 2a+2 launch B with first coordinate 3a+1 or 3a+4, and u = 2a+1 halts. Every direct B-to-A return must therefore be an ordinary even or odd case. Substituting its B coordinates into the boundary rule as above, including the ordinary final odd case u=2a−1, yields

    y = (7a+u−5)/3,     0 ≤ u ≤ 2a−1.
    (56·3ᵐ−19)/3 ≤ y ≤ 24·3ᵐ−8.

If the source width m is known, its return value x is forced by x = 3y − (48·3ᵐ+m−11).

Now fix one of the stated residue classes with n ≥ 3 and put p = 3ⁿ, L = 8p−8−n, K = 48p+n−11. The candidate Hₙ has width n. Each class satisfies n ≡ 1 (mod 7), so 3n+11 ≡ 0 (mod 7). For these four classes Hₙ modulo 7 is respectively 4, 6, 0, 5. Starting at y₀=Hₙ, repeated inverse steps at width n would give

    2yⱼ = K − (3n+11)3ʲ.

In particular every yⱼ has the same residue modulo 7 and would require a direct predecessor. As long as yⱼ is an actual value of width n, it is at least L > 71. It cannot be the first return from blank. It is at most Hₙ, so the direct-return interval rules out all predecessor widths m > n. For a width m < n, that interval would imply yⱼ ≤ 8p−8. Combining with yⱼ ≥ L would give

    n+5 ≤ (3n+11)3ʲ − 32·3ⁿ ≤ 3n+5.

For n ≥ 3 we have 3ⁿ > 3n+5 and 32·3ⁿ > (3n+11)(3n+5). Both inequalities hold at n=3 and persist on incrementing n, since neither right-hand side triples. If 3ʲ ≤ 3n+5 the displayed difference would be negative. Otherwise it is divisible by 3 raised to min(j,n), a number larger than its alleged positive upper bound. This excludes every width m < n.

Thus a hypothetical occurrence of Hₙ forces a genuine predecessor of width n with value yⱼ₊₁ = 3yⱼ−K at every backward step. The displayed formula eventually gives yⱼ < L, a contradiction. The remaining small exponent n=1 has H₁=60, below the first return 71. In fact, for these classes the entire set of A(6,b) inputs that ever visit Hₙ at a B-to-A return (including the starting value Hₙ) is exactly the inverse family in the previous section. The inverse obstruction is independent of the blank initialization, and the forward local rules realize every listed member. For the small case n=1 the same description follows from immediate inversion: 60 has only predecessor 46; 46 falls below the width-one direct interval and above the width-zero interval, and both values are 4 modulo 7. The other 38 exponent classes remain undecided on blank.

Run `python3 line4_orbit.py` with assertions enabled. At the 1,024th return the right-run length has 2,994 bits and the precise time has 5,989 bits. The SHA-256 fingerprints of the shortest unsigned big-endian encodings are respectively `823aeb9c0850ba39b1dd241c1d224243e4a69241bf547138f10d9e61c562fb6f` and `f1fef71e717dbd6d460dc8df5382d2cd09a548ec4e582f8935a26255cf1122e6`.
