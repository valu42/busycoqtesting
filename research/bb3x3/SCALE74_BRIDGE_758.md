# Scale 74 after its first change of return word

A trajectory entering the [scale-74 corridor](SCALED_GATES_758.md) deeply enough to reach its single exit subsequently reaches one exact reset at **offset 1,000,009,062,455 beyond the first-change cut**. Write B = 1,865,347,548,659,819,442,523,519,543,121,952,886,355,592,304 for that cut. At offset z the reset is A(1,H−B+z). The new checkpoint is still about 8.516×10⁴⁴ seed units from the upper edge of the scale-73 corridor. No blank-tape entry or inter-corridor crossing has been established.

## The first obstruction

The unique incoming offset is z = 812. After the fixed prefix J²⁹² L⁸ J L⁶, its remaining word is J¹⁹¹ L²⁴⁰ J L² J L R. It returns with gain 1863; the resulting even seed returns with gain 609. The complete word of the first return holds only at the six even offsets from 806 to 816, inclusive. Their gains are 1895, 1893, 1865, 1863, 1863 and 1861. The two neighboring words differ at offsets 804 and 818. Endpoint order gives the sharp interval. One return advances farther than the entire interval.

The fixed word's formal gain function has least period 2²⁵⁸ on odd seeds, including when composed with the following even return. For a word with b ordinary bulk moves, translating its seed by 2ᵇ initially changes only the second counter. If the second-counter displacement has binary valuation v, the first-counter displacement is divisible by 2ᵛ⁺¹. A J preserves this property. A bulk with v ≥ 2 lowers v by one, preserving its mass increment. Thus the first b−1 bulk residues are unchanged while the last high/low bit flips. The formal gain changes by two. Translation by 2ᵇ⁺¹ preserves every residue. For this particular word b = 257. Lifting the actual seed residue by 2²⁵⁷ changes the formal odd gain from 1863 to 1865 and the composed gain from 2472 to 2476. Since a period of a function on a cyclic group divides the group order at its least period, this excludes all smaller periods of the composite as well. This test uses a formal residue lift; the length-six guarded interval is checked separately.

## Passing the barrier and recovering the exact reset

Every even z from 812 through 10¹² follows the fixed prefix and 191 further Js. Positivity of the final second counter verifies the long J run, and the opposing endpoint orders verify all intervening seeds. For r = z mod 32,768 the exact second counter at that point changes by

$$
32{,}768+27{,}918{,}550\cdot 3^{191}
$$

per additional period in z. The checker verifies every residue against its translated representative. The affine extension comes from the fourteen ordinary bulks: translating by 32,768 keeps every bulk residue fixed, so the change in each counter follows the linear part of the common word. The total mass changes by exactly twice the change in z, and the pre-J left displacement at this period is −55,837,100. Multiplication by 3¹⁹¹ gives the displayed right displacement from conservation of the mass difference during the 191 Js.

For rapid exact evaluation of consecutive bulks, one L takes c to 6 floor((c+1)/4)+5. A block of l bulks preserves every input residue when c is increased by 2ˡ⁺¹, and translates the output c by 2·3ˡ. The checker tabulates the output and mass gain for representatives with l up to 12. After a block it verifies that the computed left counter exceeds one. This checks every intermediate bulk guard because each bulk subtracts its positive threshold from the preceding left counter.

For each even-offset band the checker compares the words at its two endpoints. A common batched prefix and common suffix ending in the even-left return certify that all intermediate seeds reach a larger seed. Otherwise the checker bisects the even offsets. The upper bound on the seed increment follows from each J adding four to the mass and each L adding at most nine. Odd offsets are even seeds and follow the pre-existing even-corridor word with increment at most 615. All 101 bands checked, with 1,240,135,053 bisection nodes, 620,067,577 accepted leaves, and a largest certified increment of 2,533. This proves the orbit must cross z = 10¹² at one of 2,533 consecutive resets. Directly evaluating the first return of the smallest remaining candidate and merging equal states gives the stated common checkpoint after 35,479 first-return evaluations.

## Reproduction

The Python checker verifies the exact edge word, the formal periods and the final join. The C++ verifier uses GMP for the full band cover and checks the [per-band receipts](scale74_bridge_758.tsv). The optional row number is one-based.

```sh
c++ -O3 -std=c++17 scale74_bridge_758.cpp -lgmpxx -lgmp -o scale74_bridge_758
python3 check_scale74_bridge_758.py
python3 check_scale74_bridge_758.py --row 1
python3 check_scale74_bridge_758.py --full --jobs 4
```
