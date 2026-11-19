# How the halting basin changes with the exponent

Let m = 292 + 242,660k for k ≥ 0, and let Hₘ be the odd halting seed from [the scale-family calculation](LIFTS758.md). Write f(x) for the second counter at the first subsequent reset A(1,f(x)) after A(1,x). The seed Hₘ−2 halts along with Hₘ. Their second counters after the m leading J moves differ by two and have residues 3 and 1 modulo 4, so their first bulk moves agree exactly.

**Every exponent has two or four additional even seeds known to halt.** They are of the form x = Hₘ−2m−b with b in {25, 27, 29, 31}. Their first reset is Hₘ−2 or Hₘ. In contrast, the fixed-offset interval certified at m = 292 cannot continue feeding the corresponding Hₘ at every scale. From k = 25 on, every even seed in [Hₘ−12,000,000, Hₘ] returns **above Hₘ**. Every later reset has a larger parameter, by the strict increase of a+2c. Such a seed could still halt elsewhere.

## Only two odd seeds at each exponent follow the full coarse halting shape

Even when all bulk residues and both odd-second-counter halt rules are allowed, an odd seed taking m leading Js can follow the following direct halting shape only at Hₘ−2 or Hₘ.

```
J^m L^8 J L^5 halt
```

To see this, allow the coarse word to act without guards at Hₘ+d and H+d for any even d. Initially the coordinate displacement between the two scales is exactly the displacement at d = 0. Every step preserves this fact. For J it follows from affinity. For L the second-counter displacement on the d = 0 path is a multiple of four by the scale-family calculation, so the floor in L commutes with that displacement for every input. The resulting final first- and second-counter displacements agree since the d = 0 paths both end at gap 3. Consequently the unguarded final gap at offset d is identical at the two scales. At d = −4, −2, 0, 2 the base gaps are respectively 7779, 3, 3, −5547. The gap is nonincreasing in d. Only −2 and 0 qualify, and both follow the actual guarded halting path.

## A uniform return formula for even seeds

For an even x = Hₘ+δ with |δ| ≤ 12,000,000 + 2m + 31, the first-return word is

```
I J^(m−1) L L J L L J L R .
```

Here L is an ordinary bulk move and R is the even-first-counter reset. Put Q = 3^(m−1), D₀ = 13,959,275 and T = 130,491,612. After the initial I and the following m−1 Js the counters are exactly

```
a = 4Q−1
c = (3^16/D₀−2)Q − T/D₀ + δ + 3 .
```

The second counter is positive. This also verifies the legality of the prefix, since the next second counter in each odd/odd J is positive precisely when the current first counter does not exceed the current second counter. The intermediate first counters rise from 3.

The check propagates the rational coefficients of Q along the displayed tail. All coordinate coefficients exceed 0.9. The coefficient of a−c exceeds 0.9 for every L, and is below −0.9 at both Js and R. Initially the additive errors of a and c have absolute value at most E = 12,000,000 + 2m + 41. Each L or J multiplies this error bound by at most three and adds at most seven. Already at m = 292 the margin 0.9Q exceeds twice 3⁸(E+4) plus ten. For larger m the left side triples at each increment, while E increases by two. Thus all inequalities have room for every bulk residue, and intermediate tail states have first counter greater than one. Each L toggles first-counter parity and each J preserves odd parity. This proves that R is the first return.

Each J increases a+2c by 4, I by 8, L by 5 or 9, and R by 5. Consequently f(x)−x = 2m+21+2t, where t is the number of the five L moves with input second counter 3 modulo 4. Hence 2m+21 ≤ f(x)−x ≤ 2m+31. The lower bound exceeds twelve million for k ≥ 25.

## Moving first preimages

For a first return to Hₘ or Hₘ−2 in this even neighborhood, the increment bound gives x = Hₘ−2m−b for odd b between 21 and 33. Substituting δ = −2m−b into the two counters above determines each bulk residue. Start modulo 256 and halve the retained modulus after every L. After five bulk moves the remaining modulus is eight. Since D₀ is odd, its inverse modulo 256 gives the exact starting residue. The starting residue depends only on k modulo 64. Exact enumeration gives the following full distribution.

| Admissible offsets b | Number of k classes modulo 64 |
|---|---:|
| 25, 27 | 32 |
| 29, 31 | 16 |
| 25, 27, 29, 31 | 16 |

At k = 0, the first two offsets return to H−2 and the last two return to H. At other k, the verifier checks the destinations separately. No blank-tape entry into any of these seeds has been established. Run `python3 check_758_moving_seeds.py` beside [check_758_lifts.py](check_758_lifts.py).
