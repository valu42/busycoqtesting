# Reconstructing and separating arbitrary ordinary words

The following results concern fine words in J (one odd/odd jump) and P (two ordinary bulk updates with the input residue d modulo four specified). They apply to nonperiodic words. Use u=(a+2c−1)/2 and d=(c−1)/2 at odd/odd block boundaries.

* Given u at a cut, **292 elementary calls of surrounding fine history suffice to recover at most one physical d** when the ending u≤H. The calls may be divided between past and future in any proportions.
* At u≤H, **two distinct states with mass-coordinate difference at most 16,384 cannot share 1,661 elementary calls of a fine ordinary word**. The bound is 255 calls at u≤3,706,040,379,353,000. It applies even to two nonoverlapping occurrences of a nonperiodic word.
* Every infinite aperiodic fine ordinary itinerary has at most one integer origin, across all masses. Conversely, at positive integer mass coordinate u≥8, a given odd/odd state admits **at most one** infinite mixed fine code satisfying the real and 2-adic inverse equations. Two specific launches admit none.

A known mass does not identify its actual local history. An arbitrarily long word could also avoid long nearby repetitions, so none of these statements proves the blank trajectory reaches the halting basin.

## Two-sided reconstruction

Write a fine word as (u,d)↦(u+V,(Qd+Au+C)/M), with Q=3ᵐ when m counts elementary updates and M=4ᵖ when p counts bulk pairs. The [composition formulas](excursion_power_758.py) are exact on their guards. Use subscripts − and + for the past and future words. At the known cut u, integrality of the past start and future end imposes

$$
 M_-d\equiv A_-(u-V_-)+C_-\pmod{Q_-},\qquad
 Q_+d\equiv-A_+u-C_+\pmod{M_+}.
$$

The multipliers are units at their respective moduli. The Chinese remainder theorem gives a single class modulo Q₋M₊. The physical interval for the future d has width at most (u+V₊)/2. Its inverse on the prescribed word has width at most M₊(u+V₊)/(2Q₊). Dividing by the class spacing leaves a ratio of at most $(u+V_+)/(2\cdot3^{m_-+m_+})$. A strict ratio below one gives at most one candidate. Replaying the word checks the remaining guards.

The verifier recovers cuts from actual model histories. For the [blank checkpoint](jump_after_third.py) it reconstructed all 18 splits of a 33-call ordinary word. From the **conditional** [scale-74 exit](SCALED_GATES_758.md), with seed H−10¹⁰·3⁷⁴+698, it reconstructed all 286 splits of a 292-call word. These are separate starting points.

## Why an infinite aperiodic fine word can have only one origin

For two origins following the same fine word, order them by u and put V=u₂−u₁ and k=d₂−d₁. V stays fixed. The exact differential maps are

$$
 J:k\mapsto3k-V,\qquad P:k\mapsto9k/4 .
$$

The P residue equality requires 4 to divide k. If V=0 and the origins differ, the magnitude of k grows by at least a factor 3/2 per elementary call. Physical d grows at most linearly in time, so this prevents an infinite common word. For V>0 the same applies to distance outside [0,V/2], since both maps expand that distance by at least 3/2 per elementary call. Therefore any infinite common word must keep k in this finite interval. Inside it, a further J can stay only for 3k≥V, and a P can stay only for 9k≤2V and 4 dividing k. These domains are disjoint. The resulting rational direction sequence is deterministic and eventually periodic. The [bounded deviation theorem](EXCURSION_POWERS_758.md) then shows that the actual fine itinerary is eventually periodic too.

There is an equivalent inverse constraint for a single origin. Let Rᵢ=4ᵖⁱ/3ᵐⁱ, where pᵢ and mᵢ count pairs and elementary calls before block i, starting at i=0. Let gᵢ be the u gain up to that index. On an infinite fine word put

$$
 \alpha=\sum_{i:J} R_i/3,\qquad
 \beta=\sum_{i:J} R_i(g_i-1)/3-\sum_{i:P} R_i b_i/9 .
$$

The P offsets bᵢ are 20,35,26,29 in input-residue order. Inverting n steps gives d₀=αₙu₀+βₙ+Rₙdₙ for the corresponding partial sums. The remainder tends to zero in the reals because dₙ grows at most linearly. It tends to zero 2-adically because an infinite physical word must contain infinitely many pairs (an eventual run of Js alone triples a+1). The two series converge in both spaces. For an odd reset, u₀=s and d₀=(s−1)/2, so s=(1+2β)/(1−2α) must evaluate to the same positive integer in both places. At an even seed apply the initial (i) rule: u₀=s+4 and d₀=(u₀−2)/2, so replace the numerator 1+2β by 2+2β and subtract four to recover s. The real denominator is positive because there is a P and the real inverse slope maps preserve [0,1/2]; the 2-adic denominator is odd. This is a necessary compatibility condition for an infinite physical itinerary.

## Finite reset residues and the limit of a congruence sieve

The inverse condition has an exact finite version. Fix **any formal fine word**, without assuming its physical guards, and put h₀=b, where b=1 for an odd reset and b=2 immediately after an even reset's initial (i) rule. Thus d₀=(u₀−b)/2. In the affine notation above, its endpoint is

$$
 d_n=\frac{(Q+2A)u_0-bQ+2C}{2M},\qquad
 Q=3^m,\quad M=4^p.
$$

Because Q+2A is odd, the endpoint is integral exactly when

$$
 \boxed{\quad u_0\equiv(bQ-2C)(Q+2A)^{-1}
       \pmod{2\cdot4^p}.\quad}
$$

The inverse in this formula is modular. Equivalently, since αₙ=−A/Q and βₙ=−C/Q, the residue is (b+2βₙ)/(1−2αₙ) modulo 2^(2p+1). All denominators in that rational residue are odd. The extra factor of two includes the starting parity u₀≡b modulo two.

Integrality of the endpoint is equivalent to integrality at **every** preceding block boundary. Formal forward evaluation introduces only powers of two in the denominators. Inverting J or P divides only by 3 or 9, respectively; starting with an integral endpoint, a preceding coordinate can therefore have a denominator that is both a power of two and odd, so it is integral. At a pair, integrality also forces its prescribed label: 9d+bᵣ is divisible by four exactly when d≡r modulo four, since bᵣ≡−r modulo four. This argument imposes no positivity or branch guard.

Now fix only a **coarse** finite J/P word with p pairs. Its 4^p fine labelings give exactly the 4^p residue classes of parity b modulo 2·4^p. To prove this, start from any integer u₀ of parity b and evaluate the coarse word formally. At each P there is exactly one label r=d modulo four making the next coordinate integral; J preserves integrality. Thus every parity-compatible u₀ belongs to one fine lift, and two distinct lifts cannot accept it. Together with the single-class formula, this proves that the classes partition the entire parity class. Appending a J adds no mass bits; appending a specified P selects one of four lifts to the next modulus, fixing two more bits.

The same conclusion holds at infinite depth. Fix a coarse infinite word containing infinitely many pairs. The nested residues for a fine labeling determine exactly one 2-adic mass U₂ of parity b, and conversely every such 2-adic mass determines exactly one fine labeling. The sums α₂,β₂ converge because the 2-adic norm of Rᵢ is 4^(−pᵢ), and gᵢ is an integer. Consequently

$$
 U_2=\frac{b+2\beta_2}{1-2\alpha_2}\in b+2\mathbb Z_2.
$$

The denominator is an odd unit. **Existence of a fine lift alone therefore excludes no coarse word for a specified integer reset seed.** Allowing all fine lifts without any additional linked restriction imposes only parity. A useful sieve must preserve the relation to the same lift's real constraint and physical guards. It may do this through a compressed relation or aggregate information; the fine labels need not be enumerated individually.

In the reals the same rational partial sums have limits αℝ,βℝ, with 0≤αℝ≤1/2 and −7≤βℝ≤0. If the first P follows k Js, then

$$
 \frac{5}{9\cdot3^k}\le1-2\alpha_{\mathbb R}\le3^{-k},
 \qquad
 U_{\mathbb R}=\frac{b+2\beta_{\mathbb R}}{1-2\alpha_{\mathbb R}}.
$$

This is a unique real candidate; it need not be positive or integral. The coefficient α is fixed by the coarse word, while β retains the fine labels and mass increments. The [reset-word bounds](RESET_WORDS_758.md) already localize the real candidates tightly after a specified launch. The real and 2-adic limits are values in different completions and are not to be identified with each other. Compatibility means that one prescribed ordinary integer u₀ separately equals Uℝ in the reals and U₂ in the 2-adics.

Even both equalities do not by themselves certify a physical excursion. For a positive initial integer mass u₀, they force integral formal states in the strip −7≤dᵢ≤uᵢ/2, which still includes negative right-counter values and reset boundaries. For a strictly ordinary reset-free continuation, require dᵢ≥0 and hᵢ=uᵢ−2dᵢ>1 at every positive-time block boundary, starting with a physical state having h₀=b. The original J guard is exactly d_next=3d−u+1≥0. For P, put q=⌊(c+1)/4⌋: each individual bulk requires a≥4q+3 and sends (a,c) to (a−4q−3,6q+5). A positive pair endpoint and the forced residue ensure both bulk guards; its even-left midpoint is larger than its positive odd-left endpoint, so it cannot be an unnoticed reset. In particular a pair landing at h=1 is a return and is excluded by hᵢ>1. The next section treats the separate virtual extension through certain negative d values.

This is a finite coding lemma and a clarification of the existing inverse condition, not a termination or decidability result. It handles the possibility of a nonreturning excursion without assuming a first return exists. Excluding all infinite ordinary codes would still leave the separate task of controlling finite excursions and exceptional restarts sufficiently to force the actual blank trajectory into a certified halting basin.

## The only possible simultaneous code from an integer origin

Here “mixed” means infinitely many Js and Ps. Assume the two inverse expressions hold for integer u₀,d₀ with u₀≥8. Formal forward evaluation of their word gives dᵢ rational with denominator a power of two. The 2-adic suffix formula at each phase writes the same dᵢ as a 2-adic integer, so each is actually an ordinary integer and the chosen P symbol is forced by dᵢ modulo four. Let αᵢ,βᵢ be the real series for the suffix, resetting g to zero at the start of that suffix. Its normalized angle satisfies 0<αᵢ<1/2. The intercept satisfies −7≤βᵢ≤0: the inverse deviation maps for d−αu preserve [−7,0] exactly as in the [affine period proof](EXCURSION_POWERS_758.md). Iteration to infinity gives the same bound without a periodicity assumption. As dᵢ=αᵢuᵢ+βᵢ, one always has dᵢ≥−7 and aᵢ=2uᵢ−4dᵢ−1≥1.

A negative d forbids J because 3d−u+1 would be below −7. For d=−7,−6,...,−1 the P outputs are −7,−7,−4,−4,2,2,5. The states −7 and −4 would force only Ps forever. Consequently a mixed code can have negative d only in {−3,−2,−1}. For nonnegative d, a prospective J needs 3d−u+1≥−3, or equivalently a−c≤6. A prospective P needs a_final≥1. Its first bulk decrement is at least c+2 and its second is at least 7, forcing a−c≥10. Thus both choices can never be possible.

This yields an exact partial integer map to test compatibility. At each block use J if 3d−u+1≥−3. Otherwise use the P specified by d mod 4 if its resulting a is positive. If neither applies, no infinite mixed code matches the origin at both places. Conversely, if this procedure continues forever from a physical start, it keeps d≥−3 and a≥1. The mass grows linearly, excluding an eventual all-J tail. An eventual all-P tail is impossible too, since any negative permitted d becomes positive after one P and the bulk right counter then grows exponentially. The two convergent inverse series consequently give the required integer at both places.

On a nonnegative path these are the original machine's ordinary blocks: for J its original guard is exactly d_next≥0, and for P its two positive bulk decrements leave a positive odd left counter, ensuring both guards. A virtual J to d=−1 from an input with c=3 modulo four and a=c+2 exactly represents E if followed by its forced pair. The virtual J and actual E produce the same a and second counters −1 and 1 respectively. The next bulk sends both to the same state since both have q=0. The other physical-to-negative transitions have a=c+2 with c=1 modulo four, or a=c+4 or c+6. In these cases the physical machine takes one bulk and then returns to a=1. Existence of a formal code therefore gives physical infinite continuation if every negative visit is of the indicated harmless E type. For a strictly reset-free excursion also require a>1 at all intermediate physical states.

As one sufficient way to avoid negative values, if at most K consecutive P blocks occur, αᵢ≥(4/9)ᴷ/3 at all phases. A simultaneous integer code with u₀≥21(9/4)ᴷ then has every dᵢ≥0. This would allow K=40 at the blank checkpoint after its initial (i) and K=391 at the scale-74 exit. In fact for each of these particular launches **no mixed code at all** satisfies both inverse equations. The forced map reaches a state with neither branch admissible after 72 and 490 complete blocks respectively. Independent replay gives a physical return there after an additional bulk and return. This result concerns those individual excursions, not the subsequent resets.

## A finite bound even for nonoverlapping occurrences

Take 1≤V≤16,384. An exhaustive integer graph computation shows that an interior direction k spends at most 28 elementary calls on transient edges before reaching a cycle or a vertex from which the common word must leave [0,V/2]. A premature departure from the prescribed direction also leaves that interval in one block (at most two calls). Reduced mixed direction cycles appear already in the graph at their reduced denominator: the cyclic denominators are coprime to six and their numerators are multiples of four at every P phase. The graph contains 25 distinct mixed primitive cycles.

For each such cycle with slopes kᵢ/q, follow the actual state deviation e=q d−kᵢu as in [the period proof](EXCURSION_POWERS_758.md). Exhausting all phases and all integers −7q≤e≤0 shows at most 22 elementary calls can keep e inside before a departure. The count excludes the departing block. Beyond this interval the distance grows by at least a factor 3/2 per elementary call while the actual word still follows this normalized cycle. Once the observed coarse word differs from that cycle, k exits [0,V/2] and its own outside distance grows at the same rate, regardless of which blocks follow. This analysis requires common fine residues for the two starting states, but does not prescribe their shared word.

For an upper mass-coordinate bound U put L equal to the smallest positive integer with (3/2)ᴸ>U+14 and D the smallest with (3/2)ᴰ>16384(U+14). Outside the k interval the initial distance is at least 1/2, and its physical maximum is at most U/2. Outside the e interval the initial distance is at least one and its physical maximum is at most q(U/2+7). Thus at most L−1 and D−1 further calls, respectively, can occur in those phases. Pure normalized cycles cannot persist longer than L−1 calls either: each J triples a+1 while each L multiplies c+7 by at least 3/2, and the odd/odd boundary coordinates satisfy a≤2U and c≤U. For J the stronger bound 3ᵐ≤U follows from (a+1)/2≤U.

In total the mixed case allows at most 28+22+2+(D−1)+2+(L−1) calls, also bounding the pure and transient-only cases. At U=H one may use (L,D)=(792,816), giving 1,660 calls. At U=3,706,040,379,353,000 use (89,113), giving 254. The statement counts only complete ordinary blocks.

Run `python3 decode_factors_758.py` alongside [check_bb33.py](check_bb33.py) and [excursion_power_758.py](excursion_power_758.py). It also checks the finite reset residue formula, prefix integrality equivalence, and the partition by fine lifts for all words of up to four blocks. These finite checks illustrate the algebraic proofs above; they do not evaluate the infinite limits. To verify the finite direction and deviation bounds, run

```sh
c++ -O3 -std=c++17 separated_factors_758.cpp -o /tmp/separated_factors_758
/tmp/separated_factors_758
```
