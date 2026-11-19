# Exact coalescence of neighboring #758 counter configurations

Write A(a,c) for the [two-counter model](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA). Equality of two later counter configurations implies that the two runs thereafter halt or continue together. The statements below compare configurations of this model. The cost in raw Turing machine steps may differ.

## All odd reset seeds except 1 have a sibling

For **every** nonnegative integer a congruent to 1 modulo 4 and integer q ≥ 1, the two configurations A(a,4q−1) and A(a,4q+1) reach the same counter state in the same positive number of map calls. In particular this applies to every pair of odd reset seeds (3,5), (7,9), (11,13), and so on, by setting a = 1.

To prove this, let the two current second counters be x and x+2, where x is 3 modulo 4. While a ≤ x, both take the odd/odd branch j, producing first counter 3a+2 and second counters x−a+1 and x−a+3. The first remains 1 modulo 4 and the smaller second counter remains 3 modulo 4. It stays positive since x ≥ a. This shared prefix is finite because a+1 triples each time and x never increases.

At its end either a = x+2 or a ≥ x+6, by the residues. For a = x+2 the lower state takes the exceptional rule while the upper takes j. Both give A(3a+2,1). In the other case put x=4s−1. Both states take the ordinary update and give A(a−4s−3,6s+5).

This yields an exact simplification for the exceptional consumption of A(a,a−2) when a is 1 modulo 4. It has the same successor as j from A(a,a). More generally one may use the representative with second counter 4q+1 whenever a is 1 modulo 4 and the second counter is 4q−1. To avoid confusing equivalence with a time advance, apply the representative's update immediately. Its future is equal to that of the original input up to a finite equal-length prefix as proved above. When applying canonicalization repeatedly from the blank start, a j move from a canonical second counter preserves its residue modulo 4, so no infinite sequence of postponed mergers is possible: each replacement couples the two runs at the next non-shared j decision.

## Even reset seeds

Let C ≥ 4 be even. From A(1,C), the first update gives A(3,C+3). Write n for the number of subsequent j calls until the first counter exceeds the second. Then

```
a = 4·3^n − 1
r = C + 5 − 2·3^n + 2n,       1 ≤ r < a.
```

For every such C with r > 1 its sibling is C−2 if r is 1 modulo 4, and C+2 if r is 3 modulo 4. The two runs coalesce on the next map call after those n j calls.

Indeed the sibling's residual r' is the other member of (4q−1,4q+1). Both residuals are positive and less than a because a is 3 modulo 4. The second counter after j is c−a+1, so positivity of the final residual implies legality of the preceding j step. Positivity propagates backward since the second counter decreases by a−1 at each j call. Hence the sibling executes precisely the same n calls from its own initial A(3,C±2+3). In both cases a ≥ 4q+3, so the next update produces A(a−4q−3,6q+5).

At r=1 this pairing construction has no positive lower partner. These seeds are exactly C=2·3^n−2n−4 in the stated range. Other later coalescences for them remain possible.

Both results concern equality of future behavior. They neither force a blank-tape trajectory into a halting interval nor assert that every orbit has a further reset.
