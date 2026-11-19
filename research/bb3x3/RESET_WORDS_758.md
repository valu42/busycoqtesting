# Recovering the reset origin of an ordinary #758 excursion

Let H be the known halting reset seed. Consider an excursion from A(1,s), with a fixed parity of s. An even seed first takes (i). After k leading odd/odd jumps J, suppose it continues with an ordinary bulk pair P and then more blocks, each either J or P. Both bulk residues are allowed in P. Assume all states under consideration have mass W = a+2c below 2H.

* The first **397 blocks starting at P** restrict the unknown reset seed to **at most four integers**, directly calculable from this coarse word, the entry parity and k.
* If the post-P word contains **291 J blocks**, the compatible reset seeds are contained in **one pair of siblings** that coalesce on the first individual bulk move. A single compatible seed or an empty interval is also possible.
* Even with the reset boundary imposed, **every one of 2¹⁴⁰ prescribed words** in two branches is attainable after the same launch of 291 initial Js and one designated bulk pair. The starts in this construction are bona fide reset configurations below H. Which of them are reached from blank remains unknown.

A fourth result below reconstructs at most one preceding exceptional restart from 397 blocks after its first J. The first two results reconstruct a reset origin when an itinerary is specified. The third gives a lower bound on the cost of listing all itineraries explicitly. They leave open which long itinerary, if any, the blank trajectory follows.

## A macroscopic exclusion for an even last reset

Let S be the even integer

```text
21397652060740660569179527531393249857985728116504484012736254799276123044548507478515077163843523468268930744915669252491365804261929780506
```

Every **even** s in [S,H−1] first returns to a=1 in exactly **300 calls**, by I J²⁹¹ L² J L² J L R. Here I is the initial even-seed rule and R is the final even-left return. This interval starts at approximately 0.9977087600484H. The next lower even seed S−2 fails this particular word.

The two endpoints execute the same word, so monotonicity along each common prefix, as established in [COVER_758.md](COVER_758.md), gives the word for all intermediate even seeds. The endpoint H−1 has the smallest left counter at every common prefix, and its left counter stays at least 3 between I and R. This verifies that R is the first return. The initial I gains 8 in mass, all 293 Js together gain 1,172, the five Ls gain at most 45, and R gains 5. The returned seed is at most s+615.

In particular set B=H−64,000,000 and U=H−3,403,055 as in the certified basin. If a trajectory avoids halting and first crosses W>2U+1, its last reset strictly before that crossing **cannot have an even seed s≥S**. A reset in [B,U] already forces halting. An even reset in [S,B−1] has a later reset with seed at most B−1+615≤U, still before crossing. Thus an even last seed would be at most S−2. Since live calls gain at most 9 mass units, such a last reset must predate the crossing by at least

$$
 \left\lceil\frac{2(U-S)+5}{9}\right\rceil > 1.09\times 10^{136}
$$

calls. The [joined halting interval](UNIVERSAL_758.md) requires at least 2,483,994,005,497 calls since the last reset for an escaping trajectory of either parity at the same upper crossing. The status of an odd last reset remains decisive much closer to the basin.

## Four-candidate bound

At an odd/odd phase use u=(W−1)/2 and h=(a+1)/2. Immediately after the k leading Js, the initial h equals 3ᵏ on odd entry and 2·3ᵏ on even entry. The corresponding initial u, denoted t, is s+2k or s+4+2k, respectively. J sends (u,h) to (u+2,3h). For P one has

$$
 u'=u+v,\qquad 4h'=9h-5u-e ,
$$

where (v,e) is one of (5,20), (9,34), (7,24), (7,30). This follows by substituting h=u−2d in the paired bulk formulas in [CUT_758.md](CUT_758.md).

For the first n coarse blocks, let Rᵢ be the product of the inverse factors 1/3 for J and 4/9 for P before block i, and let gᵢ=uᵢ−t. Indexing from zero, exact inversion gives

$$
 h_0=S t+T+R_n h_n,\qquad
 S=\sum_{i:P} 5R_i/9,\qquad
 T=\sum_{i:P} R_i(5g_i+e_i)/9 .
$$

The word fixes every Rᵢ and S. Compute lower and upper bounds for T by choosing (v,e)=(5,20) throughout or (9,34) throughout. If pᵢ counts earlier pairs, uncertainty in gᵢ is at most 4pᵢ. Thus the width in T divided by S is at most 14/5 plus four times the Rᵢ-weighted mean of pᵢ over P positions. Successive P weights have ratio at most 4/9. Their weighted mean index is at most (4/9)/(1−4/9)=4/5, by summing the upper-tail weights. The width divided by S is therefore at most 6.

Since the first block is P, S≥5/9. The remaining terminal contribution Rₙhₙ/S is at most (9/5)(4/9)ⁿH, less than 1 already at n=397. The interval for t has width less than 7. At most four integers of the required parity fit. Subtracting the known leading mass gain gives the shortlist for s. Longer itineraries can use the first 397 blocks and replay each candidate.

For a concrete test, start with s=3²⁹²+4,742. After the 292 leading Js the orbit takes 411 complete J/P blocks before the next even-left return decision. The first 397 blocks give the three candidates s−2, s, s+2. Direct replay keeps precisely s and s+2. Both execute the same 411 blocks and merge at their first L.

## Uniqueness after enough jumps

Compare two same-parity seeds in increasing order that follow the same ordinary path. Immediately before their first L they have equal a and increasing odd right counters c. With q=⌊(c+1)/4⌋, L sends (a,c) to (a−4q−3,6q+5). If their q values agree, they merge at this move, which can group at most two neighboring same-parity seeds. Otherwise their left gap is at least 4 and their right gap is at least 6 after the first L. The second required L increases the left gap by at least another 4.

From there the smaller seed has the greater left counter and smaller right counter. Both L and J preserve these orders. L cannot decrease the left gap, and J triples it. After 291 additional Js a nonmerged pair would have left gap at least 8·3²⁹¹>2H, which contradicts the mass bound. For a fixed coarse word, membership as a function of the seed is an interval of its parity. At the first mismatch, a seed failing a prescribed L is above the interval, and a seed failing a prescribed J at an odd-left phase is below it. The verifier also implements an exact two-bisection inverse for this interval.

## A preceding exceptional restart

Rule (e) from A(c+2,c), c=4z+3, puts the trajectory at A(3c+8,1), with d=0 and u=9+6z. If the subsequent ordinary path survives, its first J is preceded by some number of complete bulk pairs. The right-counter sequence and all pairs' gains before that J are fixed by their count because d starts at zero. Thus at that J the initial d is known and the unknown initial mass coordinate t lies in one known residue class modulo 6.

Fix the next n=397 blocks starting with that J. Inverting J and P in the d-coordinate gives d₀=S t+T+Rₙdₙ, now with

$$
 S=\sum_{i:J}R_i/3,\qquad T=\sum_{i:J}R_i(g_i-1)/3-\sum_{i:P}R_i b_i/9,
$$

where bᵢ is one of 20, 35, 26 or 29. As before, gᵢ denotes cumulative mass-coordinate gain. We have S≥1/3. Put ρ=4/9. Because the initial block is J, Rᵢ≤ρⁱ⁻¹/3 for i≥1 and the uncertainty in gᵢ is at most 4(i−1) there. Dividing by S, the J terms contribute width at most (4/3)∑ₖ≥₀ kρᵏ=48/25. The bulk terms contribute at most (5/3)∑ₖ≥₀ρᵏ=3. Finally dₙ≤H/2, so the terminal uncertainty divided by S is at most Hρ³⁹⁶/2. Their sum is less than 6. There is at most one possible t in the required residue class and hence at most one possible c for the exceptional origin. The calculation requires both the specified block word and the number of leading bulk pairs, and it leaves their occurrence from blank open.

## Exponentially many words have genuine reset origins

Fix k=291, h=3ᵏ, and any word of n=141 blocks whose first letter is B. Each remaining letter can be J or B, where B specifies **two (b) updates**. Write t for the mass coordinate after Jᵏ and set d=(c−1)/2. Initially d=(t−h)/2. A J updates (u,d) to (u+2,3d−u+1). A B updates it to (u+5,(9d+20)/4).

For any such word the terminal coordinate has the form d=(At+C)/D with A odd and D=2·4ᵖ, where p counts the B letters. Therefore exactly one t modulo D gives an integer terminal d. This one congruence enforces the required residue at every earlier B too. Working backward in the affine numerators, each preceding numerator must be divisible by its own denominator because the multiplier 3 or 9 is odd. At B the additional divisibility is exactly 4 dividing its input d.

Choose t in that congruence class closest to the unique real root t* of d_final=u_final/4, which is equivalent to h_final=u_final/2. For the displayed positive-coefficient identity, now with fixed fine residues, write g=u_final−t, Q=3ʲ⁺²ᵖ and Rₙ=4ᵖ/Q. The root satisfies

$$
 t_*=(h-T-R_n g/2)/(S+R_n/2).
$$

The denominator lies between 5/9 and 1: starting at 1/2, apply x↦x/3 or x↦(4x+5)/9 in reverse order, with B first in forward order. Both maps preserve [0,1]. Also 0≤gᵢ≤5n and eᵢ=20, giving T≤(5n+4)S and T+Rₙg/2≤8n+4. Thus h−8n−4≤t*≤9h/5. Rounding t within its congruence class changes it by at most 4ᵖ; hence h/2<t<2h. It changes h_final−u_final/2 by at most (S/Rₙ+1/2)4ᵖ≤3Q/2. Since Q≤3²⁸²=h/3⁹, the terminal d lies far inside the physical interval, with min(d,u_final/2−d)>h/10.

Reverse the word. The two inverse margin estimates in [CUT_758.md](CUT_758.md) keep min(d,u/2−d) at least one third of its previous value per block while the margin exceeds 20. Thus every intermediate margin exceeds h/(10·3¹⁴¹)>100. This ensures the J and B guards, including the second individual move of B. At the start, d=(t−h)/2>0 implies t≥h. Consequently s=t−2k really executes the k leading Js: the last one's guard is t≥h, and all earlier guards follow since 3ᶦ grows faster than 2i for i≥1. The following B makes the leading J count exact. All these seeds and entire paths lie below H in u because 2h+5n<H. Distinct words give distinct seeds by determinism at the first difference.

Run `python3 reset_words.py` beside [check_bb33.py](check_bb33.py). It checks the inverse on small seeds, the numerical inequalities, the concrete 411-block history, and 1,156 reset constructions against the original ungrouped map. The quantified result uses the proof above, independent of which representative words are tested.
