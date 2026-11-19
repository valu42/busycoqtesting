# A finite test for periodic #758 excursions

Suppose a fine ordinary word of m elementary counter updates occurs t times consecutively on the blank trajectory. If the mass coordinate u at the end satisfies

$$
3^{m(t-2)} \ge u/2+7,
$$

then those repetitions **prove that the machine continues forever**. In particular at u≤H it suffices that (t−2)m≥292. The word may be any concatenation of odd/odd jumps J and pairs P of ordinary bulk moves. Each P specifies the residue of its input d modulo four. The implication requires the actual guards and consecutive repetitions. It does not bound the length of a nonperiodic excursion.

There is also a one-period certificate. For an observed mixed word, compute the invariant line below. If its initial point lies on that line, one complete legal occurrence suffices to prove infinite continuation. Moreover, an infinite excursion whose **coarse** J/P itinerary is eventually periodic will eventually supply a finite affine certificate even if its bulk residues were never specified.

## The integer defect and all future guards

Use the [odd/odd coordinates](CUT_758.md) u=(a+2c−1)/2 and d=(c−1)/2, so a=2u−4d−1 and 0≤d≤u/2. J gives (u+2,3d−u+1). P gives (u+v,(9d+b)/4) with (v,b)=(5,20),(9,35),(7,26),(7,29) in residue order. For a nonempty fine word with j jumps and p pairs, put m=j+2p, Q=3ᵐ, M=4ᵖ. Its composite is

$$
 (u,d)\mapsto (u+V,(Qd+Au+C)/M)
$$

with integer coefficients. Write λ=−A/(Q−M) and γ=(MλV−C)/(Q−M). Direct substitution shows that d=λu+γ maps to the same line at u+V. Its cyclic rotations give the line at every intermediate block phase. Their slopes are the unique periodic values obtained with the inverse contractions x↦(x+1)/3 for J and x↦4x/9 for P. Both preserve [0,1/2]. For a mixed word the slope lies strictly between 1/3 and 1/2 at J phases, and strictly between 0 and 2/9 at P phases.

At a single step the deviation f=d−λu changes to 3f+1−2λ′ for J or (9/4)f+b/4−λ′v for P, with λ′ the next slope. The additive term lies in [0,1] or [0,35/4], respectively. The inverse of either deviation update preserves [−7,0], so its unique periodic intercept satisfies −7≤γ≤0. The integer

$$
 Z=(Q-M)^2(d-\lambda u-\gamma)
$$

is multiplied by Q/M on each copy. Integrality follows from the displayed denominators. After t copies, coprimality of Q and M implies Qᵗ divides Z_final. If it is nonzero then

$$
 Q^t\le |Z_\mathrm{final}|\le (Q-M)^2(u_\mathrm{final}/2+7)
 < Q^2(u_\mathrm{final}/2+7).
$$

This gives the stated test because 3²⁹²>H/2+7. Zero defect places the trajectory on the invariant line.

To see why zero defect implies genuine infinite continuation, first consider a mixed word. At every cyclic phase the reduced denominator q of the slope divides Q−M, which is coprime to six. Under J the forward slope is 3λ−1 and keeps the same denominator. Under P it is 9λ/4; having odd denominator at the next phase requires the input numerator to be divisible by four, and again the denominator is unchanged. For a legal complete copy on the invariant line, the integer difference in d is λV. Hence q divides V. At each P phase the translation Δd=λV is therefore divisible by four. This preserves the required d residue, and hence both fine bulk branches. At a J phase the J guard margin c−a increases by (6λ−2)V>0 per copy. At a P phase the first and second L guard margins increase by (2−6λ)V and (2−9λ)V respectively. Both are positive. The coordinates stay nonnegative, and every future copy is legal. A pure J word has invariant line d=u/2, which gives a=−1. A pure P word has slope zero and strictly negative intercept. Neither pure word admits a physical zero-defect state.

For an infinite mixed coarse period, use the same cyclic slopes, now independent of which P residues occur. With λ=k/q at each phase, e=q d−ku is integral. If e/q>0 it grows at least geometrically until it exceeds the physical interval, whose width grows only linearly. If e/q<−7, its distance below −7 grows at least geometrically for the same reason. Thus an infinite survivor has −7q≤e≤0 at every phase. At P phases four divides k, so d modulo four is fixed by e modulo four and q. The next e is consequently determined by the current e and the phase. There are finitely many such pairs. A repeated one gives the same fine period thereafter and a translation along its invariant line. This argument permits arbitrary nonperiodic coarse paths.

## No ordinary affine period of 222,222 elementary calls or fewer

An exhaustive check rules out infinite ordinary affine orbits in every mixed periodic direction with reduced denominator **q≤1,000,000**. Thus any nonhalting ordinary affine fine period, at any physical start, needs **at least 222,223 elementary calls**. Indeed q divides V for a complete affine fine period, as proved above, and V≤2j+9p≤9m/2. The denominator bound also excludes these coarse directions when the fine period would be much longer. It makes no assertion about aperiodic excursions.

For fixed odd q coprime to three, write the slope k/q in lowest terms. Only two normalized updates are legal:

| Next block | Necessary normalized guard | Next numerator |
|---|---|---|
| J | q<3k and 2k<q | 3k−q |
| P | 9k<2q and 4 divides k | 9k/4 |

Each branch is injective, and their images are disjoint modulo three: a P output is zero and a J output is −q. Hence a forward path through these finitely many numerators cannot enter a cycle unless its own starting point lies on that cycle. The minimum numerator in a mixed cycle must follow a J and precede a P, since J strictly decreases k and P strictly increases it. Therefore this minimum is a multiple of four, equals −q modulo three, and satisfies 9k<2q. One residue class modulo 12 suffices. The verifier follows every such candidate until it leaves the domain or reaches a numerator at most its starting value. It retains exact returns in lowest terms. The same cycles are recovered through q=999 by allowing *every* starting numerator. The only remaining small possible denominator, q=1, admits no slope strictly between zero and one half. Pure words were excluded above.

For every resulting direction cycle, inspect one reference phase and every integer e in [−7q,0]. At a J phase the next value is e′=3e+q−2k′. At a P phase d modulo four equals qe modulo four, since four divides k and odd q is its own inverse modulo four. Then e′=(9e+qb)/4−k′v. Follow the entire direction cycle, discarding a path immediately if it leaves [−7q,0], and iterate the resulting deterministic reference-phase map. Every infinite bounded orbit would contain a repeated reference e. The sweep found 128 primitive direction cycles, the largest denominator being 961,331. Across them all 343,738,502 bounded reference deviations were checked and no deviation cycle occurred.

A finite coarse repetition bound follows too. Fix a coarse period of expansion Q/M and denominator q, and an integer s with (Q/M)ˢ>q(H+7). Each step's inverse deviation map preserves [−7q,0]. If at least s more periods occur with u≤H, the initial deviation is at distance at most q(H/2+7)(M/Q)ˢ<1 from this interval. Its integrality puts it inside. Thus s+7q+1 consecutive coarse copies below H would provide more than 7q+1 bounded deviations at the same phase. Two must coincide, giving an actual mixed fine translation certificate. In particular such a finite observation is impossible for the directions excluded by the sweep.

Compile and run the sweep with C++17:

```sh
c++ -O3 -std=c++17 affine_directions_758.cpp -o /tmp/affine_directions_758
/tmp/affine_directions_758
```

## Sharp bound when every pair is followed by a jump

Among all physical starts at u≤H for which the entire tested segment remains at u≤H, the maximum number of consecutive copies of PJ is **169**. All four residues of P are allowed. This differs from the [98-copy result](cut_residues.md), which fixes both bulk residues and asks for copies around one particular cut.

Here the slope is 4/23 at the start and 9/23 after P. Set e=23d−4u. One whole copy gives

$$
 e'=3((9e+23b)/4-9v)+15,\qquad u'=u+v+2,
$$

where the P residue is 3e modulo four. Thus e′=(27/4)e+B with 225≤B≤1503/4. For N copies put r=(4/27)ᴺ. From −4H≤e_final≤15H/2 it follows that the initial integer e lies in

$$
 [-4Hr-(1503/23)(1-r),\ (15H/2)r-(900/23)(1-r)] .
$$

The checker enumerates precisely those integers. For each, the recurrence fixes every residue and the total drift V. Choose the largest u≤H−V such that e+4u is divisible by 23. This tests all smaller feasible u in the same class: increasing u by 23 and d by 4 improves both bulk guards and the jump guard by the slope-margin calculations above, while preserving both residues. There are no surviving e values for N=170. For N=169 they are −61 and −46; both constructions replay on the original counter map.

## Check on the actual blank trajectory

The [certified checkpoint](jump_after_third.py) is the reset seed 2·3³²−20=3,706,040,377,703,662. The checker followed its next **8,192 consecutive first returns** to seed 3,706,040,379,351,922. Within each ordinary segment it checked every possible mixed one-period translation and every fine word occurring at least three times in succession. For all words the largest observed (t−2)m was 30, attained by the initial pure J run. For mixed words the largest was 3, first seen at seed 3,706,040,378,103,754 with three copies of P₁J. No infinite certificate occurred. As a separate check, the sharp maximum PJ count over arbitrary starts with u≤3,706,040,379,353,000 is 20. This latter maximum is over all starts, not only the blank trajectory.

Run `python3 excursion_power_758.py` alongside [check_bb33.py](check_bb33.py). The checker also verifies the symbolic identities for all 3,905 fine words of one through five blocks. The arbitrary-period proof is algebraic. Blank entry into a halting interval and any general bound on aperiodic excursions remain open.
