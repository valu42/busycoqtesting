# A Wily return map on finite zero-gap words

Read the binary digits of n/3 from the low end, and record the number of zeros before each successive one. The gap sequence is eventually all ones for every numerator prime to three. Store just the finite word before that all-one continuation, removing any trailing unit gaps. For Wily's [blank-connected negative checkpoint](WILY_EXCURSION.md) the resulting word is

```
6 2 5 1 1 6 2 3 1 1 2 2 1 3 1 1 6 2 1 0 2
```

There is an exact test for a sign escape: skip successive single unit gaps and triples of gaps of the form `0,s,0`. The remaining finite word must be precisely `3`, `4`, `0,s,2` or `0,s,3`, for any nonnegative integer s. Thus this particular finite-word orbit would decide nonhalting for both Wily machines if one could prove it never enters that language. The avoidance question is open.

## The map

In the following table letters are individual gaps, not bits. Let D increase just the first gap of a sequence by one. Implicit unit gaps can always be read beyond the finite stored word.

| Initial gaps | New gaps under F |
|---|---|
| 1, w | 0 followed by D(F(w)) |
| 0, s, 0, w | s+1 followed by D(F(w)) |
| 2, s, w | 0, 0, s+1, w |
| r, w with r ≥ 3 | 0, 0, 0, r−3, w |
| 0, s, 1, t, w | s+1, 0, t+1, w |
| 0, s, r, w with r ≥ 2 | s+1, 0, 0, r−2, w |
| All unit gaps | 0 followed by all unit gaps |

The first two branches are the only recursive ones. The [checker](wily_gap_map.py) implements them using iteration. To derive the table, in the notation of the [dihedral-label proof](WILY_DIHEDRAL.md) write F = c j, where j flips the first bit and c passes all initial zeros and the first one, then applies b to the remainder. A first-bit flip inserts a leading zero gap and reduces the old first gap by one when that old gap was positive. If the old gap was zero, the flip removes it and increases the next gap by one. The b carry on bits starting in zero flips the first two bits and stops. On a leading one it writes zero and passes F to the rest. In gap coordinates those statements give the six finite branches by direct substitution. The all-unit input corresponds to numerator −2 and has image −1.

Equivalently, start at −2 and restore the gaps from right to left. Restoring a gap r sends the suffix numerator m to 2ʳ(3+2m), since it prefixes r zeros and one. This gives a direct inverse to the encoding.

## Sign at the last defect

If all gaps after the first are units, the numerator is $-2^r$, where r is the first gap. Otherwise its sign is positive exactly when its last nonunit gap is zero. To see this, put the start of the all-one high gap tail at binary place 2^L. Its numerator is −2. The entire numerator is 3z−2·2^L, where z is the low L-bit word. Read the bits of z/2^L from the high end and compare with 2/3, which has repeating fractional digits `10`. The top low bit is a one. A final nonunit zero gap gives a second consecutive one, and a final gap of at least two gives at least two consecutive zeros after the one. There is a lower delimiter one exactly when this gap is not the first gap, which explains the separate first-gap case.

For a negative starting word, the final nonunit gap is positive whenever it is an interior defect. An unprocessed positive final defect retains its sign. The branch beginning in r ≥ 3 can leave a zero as the last defect precisely if this is the last explicit gap and r is 3 or 4. The branch beginning `0,s,r`, r ≥ 2, does the same exactly when r is the last gap and equals 2 or 3. In the other stopping branches a final operand of at least one is increased, leaving a positive last defect. The recursive prefix only changes the first gap of the stopping output and cannot change those conclusions. An all-unit singular recursion from a negative input is −2 itself and has negative image. This proves the escape language at the start.

## Integer step of the signed height

Set W = Σ(−1)ⁱ(gᵢ−1) over gap positions i starting at zero. Its value is 6 at the blank checkpoint and 0 at its last positive predecessor. If k recursive branches precede a stopping rule, then

$$
W(F(n))=-W(n)-1+3(-1)^k.
$$

A singular update has the same formula without the final term. Substitution of any of the four stopping rules gives W(F(n))+W(n)+1 = 3, regardless of the free operands. The operation D increases W by one. Substituting either recursive branch negates W(F(n))+W(n)+1; on the all-unit limiting case it is zero. This proves the formula at all finite inputs and explains the parity which selects the direction of each height step. The exact height step and the endpoint language do not establish the blank orbit's sign at all later times.

Run `python3 wily_gap_map.py` to compare the word map to the scalar permutation on short words and numerators of both signs.
