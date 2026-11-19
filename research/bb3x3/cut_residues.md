# A two-sided residue test at the #758 central cut

At the central cut let $u=H-10{,}000{,}000$, so $W=2u+1$. Consider two ordinary rule (b) updates followed by one rule (j). **There is an integer trajectory with 46 copies before this cut and 52 copies after it. No integer trajectory has 99 consecutive copies containing the cut at a copy boundary.** These trajectories start at arbitrary counter configurations. Their reachability from blank is open.

Use the [cut coordinates](CUT_758.md) $d=(c-1)/2$, $a=2u-4d-1$. The two (b) updates send $(u,d)$ to $(u+5,(9d+20)/4)$ for the designated residue $d=0\bmod4$ under their guards. Rule (j) then sends the result to $(u+7,(27d-4u+44)/4)$. Consequently the integer

$$
Z=529d-92u+900
$$

changes by the exact factor $27/4$ on every complete copy.

For a sequence with $h$ copies before the cut and $j$ after it, both $27^h$ and $4^j$ must divide its cut value of $Z$. Write $Z=27^h4^jv$. The initial and final values are $4^{h+j}v$ and $27^{h+j}v$. At the cut $27^h4^jv\equiv900-92u\pmod{529}$. Its right side is 3 modulo 23, so $v$ is nonzero. If $h+j=99$, the final mass coordinate is at most $u+693$. The physical bounds $0\le d\le u_{\rm final}/2$ imply $|Z_{\rm final}|\le174(u+693)+900<27^{99}$, a contradiction. Every longer sequence containing the cut contains a 99-copy subsequence containing the cut.

For $h+j=98$, the congruence and the same physical bounds leave just $v=12$, with $h$ equal to 0, 23, 46, 69 or 92. All five choices meet every original guard, as the verifier checks by replaying the individual two-counter updates. For the most balanced choice, the cut coordinate is $d=(92u-900+12\cdot27^{46}4^{52})/529$.

## What modular tests can distinguish

For every integer $u$ the rational value $d_*(u)=(92u-900)/529$ sets $Z=0$. Its denominator is coprime to both 2 and 3. Its 2-adic value is a multiple of four, as the two (b) moves require. One complete copy sends this value to $d_*(u+7)$. This gives a compatible solution to the update congruences **in both time directions at every power of three**, including simultaneous 2-adic residue tests. Its real slope $4/23$ lies inside the two-bulk region and the following slope $9/23$ lies inside the (j) region. The numerator of $d_*(u)$ is nonzero modulo 23, so the rational value never equals an integer. Integrality together with the finite real bounds makes the 99-copy exclusion possible.

The same limitation of modular tests applies to other periodic words. Fix any cyclic word using both symbols $B$ (the two designated (b) moves) and $J$ (one (j) move). Write $p$ and $s$ for their respective counts. Composing one period gives

$$
(u,d)\longmapsto (u+5p+2s,(Qd+Au+C)/m),\qquad Q=3^{2p+s},\quad m=4^p
$$

for integers $A,C$. A unique affine function $d(u)=\lambda u+\gamma$ is carried to its value at the next period, with $(Q-m)\lambda=-A$ and $(Q-m)\gamma=m\lambda(5p+2s)-C$. Its denominator divides $(Q-m)^2$, coprime to six. Applying the same argument to each rotation of the cyclic word gives the corresponding 2-adic and 3-adic values at every phase. At a $B$ phase, the reverse equation $d=(4d'-20)/9$ puts that value in $4\mathbb Z_2$. Thus these periodic update congruences also survive intersection of past and future residue tests for every power of three. Real guards, entire nonperiodic itineraries and blank reachability require additional information.

Run **python3 check_cut_residues.py** alongside [check_bb33.py](check_bb33.py).
