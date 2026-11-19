# Which smaller seeds can follow the known halting path?

For the #758 reset state A(1,c), let H be the known 140-digit halting seed. Its direct path is J²⁹² followed by the word B C B B C C B B J B C B B C D, using the published two-counter branch labels. D is terminal. **The only reset seeds up to H that halt with eight bulk moves, one J, five bulk moves and then an immediate halt, after their initial J run, are H−2 and H.** The two paths merge on the first bulk move. This rules out obtaining a shorter blank-tape decision by scaling this particular terminal path down. Other terminal words and earlier returns remain possible. [Published rules](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA)

## The exact fine-grained family

Write D₀ = 13,959,275 to distinguish this denominator from terminal branch D. For an odd seed with m leading Js, put P = 3ᵐ and z = c + 2m. Immediately after those moves the state is A(2P−1,z−P+1). Composing the displayed B/C/J word as affine functions and imposing the terminal equality a−c_current = 3 yields

```
D₀ z = 3¹⁵ P − 130,491,612.
```

The multiplicative order of 3 modulo D₀ is 242,660. The verifier checks the power at that exponent and at its quotient by each prime divisor. Hence integrality requires m = 292 + 242,660k, k ≥ 0. Every such m works. Relative to the m = 292 path, each tail coordinate changes by an integer times (P−3²⁹²)/D₀. This quotient is divisible by four. All residues therefore persist. The verifier checks the sign of each affine guard's slope, preserving all inequalities for larger P. The leading Js are legal because z ≥ P. The resulting halting seed is (3ᵐ⁺¹⁵ − 130,491,612)/D₀ − 2m.

An even seed would start with I then m Js. Here P is replaced by 2·3ᵐ and z by c+4+2m in the same affine calculation. Modulo 11, an integer solution would require 2·3ᵐ and 3²⁹² to have the same quadratic character. Their fifth powers are −1 and +1, respectively. This excludes an even seed with this exact terminal word for every m.

## Allowing every bulk residue

At an odd second counter c_current, both B and C have the same bulk expression when enabled. Set q = floor((c_current+1)/4). The next state is A(a−4q−3,6q+5) when a ≥ 4q+3. Call this operation L. For each fixed m and seed parity, apply the shape L⁸ J L⁵ without guards. As the initial seed increases, a is nonincreasing and the second counter is nondecreasing, including through the unguarded extensions. Thus a−c_current is nonincreasing. Every candidate for an immediately following halt has gap 1 or 3. Bisection finds the entire candidate interval, including plateaus, then the verifier replays every candidate with all original guards. More than 292 leading Js would already require a seed greater than H. This finite search checks both entry parities, every possible B/C choice in all 13 bulk moves, and both odd-second-counter terminal guards. It recovers exactly the two seeds stated above.

Run `python3 check_758_lifts.py` from this directory. This result concerns a family of starting configurations. The blank-tape orbit's entry into any member's basin is still open.
