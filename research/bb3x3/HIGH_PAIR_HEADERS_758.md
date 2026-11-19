# An exact header sieve for the high-pair part of the target gap

At an aligned odd reset below H the normalized direction is x=D h₀/3ʳ, where D=13,959,275 and h₀ is the integer after the common cusp prefix, before its second jump run. The aligned x is above 1/3. If it survives its first decision it takes P. The inverse maps in this coordinate are J(x)=x/3 and P(x)=(4x+5)/9. The [target-shadow proof](TARGET_SHADOW_758.md) specifies how much of this ideal itinerary is valid in the physical machine.

Take the **first** complete block boundary at or beyond r elementary calls. Write m for its time and p for its pair count, so m=r or r+1. The inverse word has the form x_initial=(A+4ᵖx_tail)/3ᵐ. Extending on the right sends A to 3A at J, or to 9A+5·4ᵖ at P. Initially A=0, and the forced first P gives A=5. Therefore the terminal direction is N/4ᵖ with

$$
N+A=3^{m-r}D h_0,\qquad 0\le N\le4^p.
$$

The target's header identity h₀(d+32,768)=h₀(d)+2D holds algebraically for all even offsets. Computing the prefix once for every even residue of d gives 8,192 distinct h₀ modulo 2D. The high-pair checker uses **all** these residues at each prefix. Dropping the particular offset interval enlarges its candidate set. Its result applies simultaneously to every allowed offset with that r.

For a prefix put t=3ᵐ⁻ʳ and M=2tD². The sorted residues tD·(h₀ mod 2D) specify every permissible N+A modulo M. The checker walks this sorted periodic set in [A,A+4ᵖ]. Small p are handled by the separate exhaustive tail survey. For large p the program enumerates all J/P prefixes starting with P, pruning only a subtree whose remaining elementary depth cannot bring its pair count up to the requested minimum.

Two exact filters speed up this walk.

1. A 2²²-cell grid covers [0,1]. Recursively generate the inverse-cylinder intervals [A,A+4ᵖ]/3ᵐ from both branches until their endpoints occupy the same or neighboring grid cells. Mark both endpoint cells, thereby covering the entire surviving interval. The inverse contraction is at most 2/3 per elementary letter, so at most 40 elementary letters suffice to complete this construction along any path. A tail surviving longer must be in a marked cell. An unmarked cell and every adjoining unmarked cell can be skipped by jumping to the next marked cell and then to the next permitted lattice residue.
2. For each remaining N use outward rounding in units of 2⁻⁶⁰. The initial dyadic direction is represented exactly for p≤30. Multiply both endpoints by three at J, and round (9x−5)/4 down at the low end and up at the high end at P. An interval strictly inside (1/3,5/9) certifies a reset decision. Any ambiguous comparison, or survival to the budget, triggers a fresh exact rational replay using GMP. The loop tests each guard at depths up to and including the budget.

For r≤53 and p≥24 the [ledger](high_pair_headers_758.tsv) contains 617,905 prefix cylinders and 57,087,748 angular tests. All remaining candidates enter the return interval by the guard at depth 257. The first possible cylinder in these rows occurs at r=47. The separate unrestricted dyadic calculation handles p≤23.

The checker reports a failure if any surviving candidate remains. Its zero-survivor lines refer to the header/dyadic combinations counted, independently of the blank trajectory. The extra 42 calls required between r and the requested budget cover the terminal crossing overshoot and the entire grid construction. Arithmetic limits and loop bounds in the C++ source support 2≤r≤60 and p≤30.

```sh
c++ -O3 -std=c++17 high_pair_headers_758.cpp -lgmpxx -lgmp -o high_pair_headers
./high_pair_headers 45 53 24 257
```
