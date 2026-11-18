# Line 34 · a 52-sweep protected prefix and the limits of short periodic tiles

**Line 34 remains open.** For `1RB2LA4RA1LA3LA_0LA2RB3RB2LB---`, a cut between cells 66 and 68 isolates an exactly periodic left guard, subject to a specific debt allowance. From the cut, the suffix receives a known stream of zero, one or two openings and one known bit per sweep. Proving that the actual suffix stays within its allowance would prove blank-tape nonhalting. A separate calculation rules out extending this prefix by a short spatially repeating tail in the same 52-phase description. Neither result has been formally verified.

## The moving cut

Write O for digit 1, N for 2, and C for 3. The debt of a word is the maximum, over its prefixes, of the excess of C over O. Match each C with the nearest available O to its left. The survivor bit is one for each remaining O and zero for other cells. In a successful sweep each ordinary digit is produced by the function D of the previous and current survivor bits. Equal bits give O, 01 gives C, and 10 gives N. All six guard cases, including the condition for B4, are in the [physical reduction](line34_left.md). A unit left header means the new ordinary output of old cell i occurs at left-origin coordinate i+1, with coordinates starting at zero.

Start at blank epoch 1,300, with A at −1,300 after **3,661,354 raw instructions**. The word has width 1,585. Let phase p be the starting epoch modulo 52. The old protected width starts at x=67 in phase zero. The phase allowance U determines the next width by x′=x+1−U.

| Phase p | Maximum allowed debt U |
| --- | ---: |
| 2, 13, 40, 46 | 0 |
| 3, 7, 23, 41 | 2 |
| Other phases | 1 |

The 52 widths form a closed cycle between 66 and 68. The seed prefix is `1111111111111111311111232131111111123213111111112311111111213111231`. The [full checkpoint](fence34-seed.json) stores the finite tape as two symbol masks. Independently executing all 3,661,354 instructions from blank gives the same absolute head, A state and complete tape.

**Exact prefix test.** If the old protected prefix is correct, its prescribed guard and entire next protected prefix occur **if and only if** the old suffix has debt at most U. Until this test fails, the guard debt is zero at p≡0 modulo 13, two at p≡12, and one at the other phases. Every such sweep completes in finite positive time. Failure of the prefix test marks loss of this particular certificate. It does not imply B4.

Here is the finite proof. Starting from the seed, compute each next protected prefix using zero exterior debt and retain its first x′ digits. After 52 transitions the original 67 digits recur. For an arbitrary unknown suffix of debt d, all matching of the old prefix is identical to matching it with the canonical suffix consisting of d copies of C. The first x′ new digits then follow from the physical header and ordinary data within the old prefix. All accepted guards have header length one, and x′≤x+1. The verifier tries every d from zero through x+6 in each phase. Larger debts reach B4 even if every prefix digit is an opening. In each phase the complete accepted set is exactly the table's interval from zero through U. These are 3,821 finite cases including 156 representative checks with the literal interpreter. Induction gives the test for an arbitrarily long actual trajectory. [Checker](fence34.py) · [Verification transcript](fence34-verification.txt)

## The residual word needs only a periodic boundary

At every phase the last U old protected cells are openings. Write the prefix as Q followed by these U cells. Under the allowance test, they absorb all the incoming debt. The last survivor bit of Q is therefore independent of the true exterior. In increasing phase order its exact bits are

```text
0101110100101001111111011101100111100101011101011001
```

Let R be the old suffix. Check its debt against U. On success, prepend U openings to R, determine all its survivor bits by matching from the right, and apply D across them starting with the displayed left bit. Append N if the last bit is one. This produces the **entire next R**. Indeed, the next cut ends just before the first ordinary output of the dropped U cells and everything after those cells is old suffix data. The true guard and retained prefix are already certified above.

The new residual evaluator reproduced 520 complete residual words against the independently timed full-word implementation. The allowance was discovered using epochs 1,300–5,999. It still held at every actual checkpoint from 6,000 through 49,999, including 44,000 held-out sweeps. Over both intervals the debt never exceeded one at the moving cut. Other cuts can carry six or more on the blank execution. No model of independent phases or runtime prediction is involved. Exact raw intervals are given by summing the [cost of each full sweep](target34.md#exact-clock-for-one-successful-sweep).

## An obstruction to stationary periodic tiles

Consider an auxiliary right-infinite word in the normalized **left** coordinates. Use the canonical finite matching debt (maximum prefix deficit) on its suffixes. Assume its full word returns every 52 sweeps and its left header has length one at every phase. Suppose also that it agrees with the first 17 digits of the true epoch-78 prefix, `11111111111111113`, at one phase. **It cannot be eventually spatially periodic with spatial period at most 24.** This rules out the direct use of short, freely repeatable tiles in such a construction. Longer spatial periods and evolving tile sequences remain open. The [line 36 proof](../line36-tiles.md) supplied the template under test.

To check the possible periodic regions, let b(i) be the old survivor at site i, with i taken modulo the candidate spatial period n. The next digit at i is D(b(i−2),b(i−1)). On a positive-balance ring the matching of this output is computed by two right-to-left tours. In the first tour from debt zero one obtains the unique periodic starting debt. Indeed the debt sent across a full tour from u is the maximum of its intrinsic debt and u minus its positive balance. The second tour gives the actual survivor mask. Balanced rings have no surviving openings; their next ordinary stream is all O. Negative-balance spatial tails cannot have finite matching debt. Treating these as zero masks in the catalogue also sends them into all O and cannot introduce an extra cycle.

The finite graph of all **33,554,430 masks** for lengths one through 24 has only two kinds of cycles whose temporal periods divide 52. All O is fixed. At each multiple of four there is also one four-cycle, with the surviving sites in a single residue class modulo four, moving from class a to class a−1 on each sweep. The C++ checker traverses the entire graph. A separate opening-stack enumeration on three copies checks widths through eleven in Python. [Ring enumeration](fence34_rings.cpp) · [Output](fence34-rings-verification.txt)

A finite nonuniform region cannot join either tail in the proposed time-periodic reference. Compare the actual survivor bits with the perfect tail everywhere, and let j be the rightmost differing bit. The 16 openings and one closing in the specified prefix ensure at least one disagreement beyond the left header. The closing has zero bit, and on the contiguous opening run the survivor pattern is a run of ones followed by zeros, which cannot equal isolated sites every four cells.

* For all O, the exterior carries zero debt. Changing b(j) changes whether the next digit at j+2 is an opening. It flips that site's survivor, with exact agreement farther right. The rightmost disagreement advances by two.
* For the moving four-wave, the perfect old survivors have class a. The next digits are C at a+1, N at a+2, and O elsewhere. Debt from strictly after site j+2 is one precisely for j≡a+2, and zero otherwise. At zero debt the changed b(j) again flips the survivor at j+2. In the exceptional case the perfect O at j+2 becomes N, passing its one unit of debt left. Thus both versions have zero bit at j+2. At j+1 the perfect survivor has class a−1; in the changed word that site now receives a positive debt and cannot survive. The rightmost disagreement advances by exactly one.

In each case the rightmost disagreement moves strictly right at every sweep. For the four-wave the successive advances on its eventual residue cycle are one, two, two. A stationary 52-sweep reference would have to put this disagreement back at its initial coordinate. The proof allows an arbitrarily long finite region before the periodic tail. It concerns normalized symbolic sweeps only.

## Reproduction and remaining question

From `research/bb2x5/halting-outlook`, run with Python assertions enabled and a C++17 compiler.

```sh
python3 fence34.py --epochs 50000
c++ -O3 -std=c++17 fence34_rings.cpp -o fence34-rings
./fence34-rings
```

The most direct remaining experiment is to analyze the standalone residual word at the four zero-allowance phases, where its first excess closing would break the certificate. A proof must account for the periodic boundary bit and the changing right end. A loss of the certificate from the real checkpoint would instead disprove the proposed all-time prefix lock.
