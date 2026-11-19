# What happens when the doubled-power skip ends?

For every exponent $m\ge20$, one attainable exit of the short-return corridor below $2P$, $P=3^m$, is the reset $s_m=2P-2m-4$. Consider these particular reset seeds as $m$ varies. In **every fixed arithmetic progression of exponents**, the first excursion from $s_m$ returns with natural density one. Half of the exponents give a reset immediately after the initial long string of bulk instructions. Among the others, **every prescribed finite sequence of ordinary jumps and bulk pairs**, followed by one bulk and a reset, occurs with an explicit positive density. This conclusion concerns the indexed exit seeds. Which exit the blank tape selects at a given gate is a separate question. [Power gates](POWER_GATES_758.md) · [Checker](power_phase_law_758.py)

In particular, subdividing $m$ into finitely many congruence classes and prescribing a finite list of exact post-bulk words cannot handle even this single family of possible exits. A more general rule, such as one that follows the direction after each bulk run, could still accelerate it.

## An actual approach to this exit

Choose $s=s_m-q(4m+16)$ between $1.91P$ and $1.92P$. Such an integer $q$ exists for all $m\ge20$ because that interval is wider than $4m+16$. At every even reset $s$ in this progression up to $s_m-(4m+16)$, write $z=s+2m$. The even opening $I J^{m-1}$ leaves $(4P/3-1,z-2P/3+3)$. The odd return following it starts at $t=s+2m+9$ and $J^m$ leaves $(2P-1,t-P+2m+1)$. In each case the right coordinate is positive, which justifies all the leading jumps. Both displayed right coordinates are 3 modulo 4. Each takes a bulk and then the even-left reset. Indeed, on the even path the pre-bulk gap is $2P-z-4\ge4m+16$, and on the odd path it is $3P-t-2m-2>P-2$. In each case the post-bulk left counter is smaller than the right one, as follows from $z\ge1.91P$ and $t+2m\ge1.91P$. Both left counters immediately after the bulk are even. The first return increases the seed by $2m+9$ and the second by $2m+7$, from the exact mass gains of their calls. Thus the path advances exactly $4m+16$ per pair through $s_m$. Its immediately preceding odd reset is $s_m-(2m+7)$, below the even gate cut $2P-2m-6$. [Individual counter rules](check_bb33.py)

## Irrational rotation of the angular coordinate

From $s_m$, $I J^m$ reaches $(4P-1,1)$. Put $b=3/2$. For an uninterrupted bulk run let $r_0=1$, $D_0=0$, and set
$$
 q_j=\lfloor(r_j+1)/4\rfloor,\qquad r_{j+1}=6q_j+5,\qquad D_{j+1}=D_j+4q_j+3 .
$$
After $j$ bulks the state is $(4P-1-D_j,r_j)$. The next bulk is legal precisely when $D_{j+1}\le4P-1$. Write $K=\lim_{j\to\infty}r_j/b^j$. Since $r_{j+1}-br_j$ is either $7/2$ or $13/2$, summing the geometric tail gives $7\le Kb^j-r_j\le13$. Also $D_j=2(r_j-1)-G_j$, where the accumulated ordinary mass gain satisfies $5j\le G_j\le9j$. Consequently $D_{j+1}=3Kb^j+O(j+1)$.

Let $v_m=\log_b(4P/(3K))$. If both distances to the neighboring integers exceed a fixed $\epsilon>0$, then for all sufficiently large $m$ the maximal bulk count is $j=\lceil v_m\rceil$. Set $\theta=j-v_m$. The last right counter divided by $4P$ is $b^\theta/3+O(1/P)$ and the last left counter divided by $4P$ is $1-2b^\theta/3+O(m/P)$. For $\epsilon\le\theta\le1-\epsilon$ the left counter is positive, stays above one throughout the bulk sequence, and ends strictly below the right counter. An odd $j$ gives an even-left reset. An even $j$ gives an odd/odd jump. At the end of that jump the normalized direction $x=(a+1)/(a+2c-1)$ is
$$
 x=3-2b^\theta+O(m/P).
$$

The increment of $v_m$ is $\log_b3$, which is irrational since equality of nonzero powers of $3$ and $3/2$ would violate prime factorization. Therefore $v_m$ modulo two is equidistributed even when $m$ is restricted to any fixed arithmetic progression. The discarded neighborhoods of the integer boundaries have arbitrarily small density as $\epsilon$ decreases. Thus odd $j$ accounts for half the exponents. For even $j$ followed by that first jump, the relative frequency, among *all* exponents of the progression, of $x\in(A,B)\subset(0,1)$ is
$$
 \mu(A,B)=\frac{\log((3-A)/(3-B))}{2\log(3/2)} .
$$

For a binary word $w$ in a jump $J$ and a bulk pair $P_2$, form $I_w$ by starting at $(1/3,5/9)$ and applying the inverse branches in reverse word order, $f_J(x)=x/3$ and $f_{P_2}(x)=(4x+5)/9$. Inside this open interval the prescribed word executes, then one bulk and a reset. On any closed subinterval of its interior all normalized guards have a strict margin. The finite-size errors in the integer dynamics vanish as $m$ grows. The interval endpoints have zero density. Hence the exact frequency of this particular outcome after the first jump is $\mu(I_w)$. The surviving intervals at depth $k$ have total length $(7/9)^k$; the density of $\mu$ with respect to length is bounded above by $1/(4\log b)$. These tails therefore have limiting mass zero, proving that the exit's first return occurs for a density-one set of exponents. This permits a density-zero exceptional set, including particular exponents of interest. [Normalized branch guards](ALL_ORBIT_ENTROPY_758.md)

## A quantitative stopping rule for this exit family

In a dyadic range $M\le m\le2M$, take
$$
 n=\left\lfloor\frac{\log\log M}{\log(18/7)}\right\rfloor .
$$
Apart from a fraction $O((\log M)^{-\gamma})$ of these exponents, the initial run either returns immediately or reaches a reset within the following jump, at most $n$ additional coarse blocks, and a final bulk/reset. Here $\gamma=\log(9/7)/\log(18/7)>0.266$. The same statement holds within any fixed exponent progression; the implicit constant may depend on its step. In particular the first excursion takes $(1+\log_b3+o(1))m$ elementary counter calls in natural density. This counts its leading opening and jumps too. It gives no upper bound for every individual excursion.

For completeness, the phase rotation has interval discrepancy $O(1/\log M)$ over $M$ consecutive exponents. For its rotation angle $\omega=(\log_b3)/2$ modulo one (or any fixed positive integer multiple), $\|h\omega\|\ge c e^{-C h}$ for integers $h\ge1$. To see this, a small error reduces as above to comparing $3^{k-d}$ and $2^k$, with $d$ the progression step times $h$ and $k$ twice the nearest integer. Applying Dirichlet approximation with $Q=\lfloor\sqrt M\rfloor$ gives a reduced fraction $p/q$ with $q\le Q$, $|q\omega-p|\le1/Q$ and therefore $q\gg\log M$. In any block of $q$ indices the phases are within $1/Q$ of a translated equally spaced grid. The incomplete last block has at most $q$ points. Thus the interval discrepancy is $O(1/q+1/Q+q/M)$, as claimed.

The normalized depth-$n$ survivor set has at most $2^n$ intervals of total length $(7/9)^n$. Its phase preimage has length $O((7/9)^n)$ since the inverse of $3-2b^\theta$ has bounded derivative. The combined discrepancy across its intervals is $O(2^n/\log M)$. Finite precision adds boundary neighborhoods only. The initial angular error is $O(M/3^M)$ except within that same distance of an integer-phase seam. Until a guard mismatch, each branch expands error by at most three and adds $O(1/3^M)$, since the integer mass stays above its initial order $3^M$. Thus a mismatch through depth $n$ is contained in an $O(3^n M/3^M)$ neighborhood of some ideal boundary in the starting angular coordinate: inverse branch slopes are at most one. There are $O(2^n)$ such boundary points, including $0,1$ for premature resets at the axes. Their total length is negligible here and their interval discrepancy is again $O(2^n/\log M)$. Balancing the survivor and discrepancy bounds gives the stated $\gamma$.

## A rarity bound for short terminal or exceptional suffixes

Fix a budget of $N$ grouped blocks after the initial bulk run. Among $m\le M$, at most $O_N(\log M)$ exponents can execute a halt or the exceptional restart $E$ within this budget before their next reset. Here the one unpaired bulk that precedes a possible terminal counts as a block.

Indeed the possible threshold directions are the endpoints $0,1/3,5/9,1$ and their preimages under words of at most $N+1$ branches, a finite set. Away from these thresholds the normalized system performs only strict ordinary moves or a regular reset. For fixed $N$, each true normalized update differs from its affine branch by $O(1/P)$ on this bounded prefix. The thresholds representing corrections to the single-bulk/second-bulk decision satisfy the same bound. Pulling back shows that a terminal or exceptional case requires $x$ within $O_N(m/P)$ of one of the finite endpoints, including the $O(m/P)$ error in the initial direction. A mismatch in the predicted initial bulk count itself requires $v_m$ within $O(m/P)$ of an integer, by $D_{j+1}=3Kb^j+O(j+1)$. The inverse derivative of $\theta\mapsto3-2b^\theta$ is bounded, so in all cases $v_m$ modulo two lies within $O_N(m/3^m)$ of one of finitely many fixed phases.

If $m_2>m_1$ approach the same phase this closely, let $d=m_2-m_1$. For an integer $k$ we have $|d\log_b3-k|=O_N(m_1/3^{m_1})$. For large $m_1$, $k\ge d$ and the distinct integers $3^{k-d}$ and $2^k$ give $|b^k/3^d-1|\ge2^{-k}$. The preceding logarithmic estimate also bounds this difference above by $O_N(m_1/3^{m_1})$. Therefore
$$
 d\ge \frac{\log(3/2)}{\log2}\,m_1-O_N(\log m_1).
$$
For each threshold, successive exceptional exponents eventually differ by at least half the smaller one. This gives the logarithmic count. The estimate is for fixed $N$ and does not exclude a halt after a much longer excursion.

## Simultaneously checking the first eight blocks through exponent $10^{100}$

A finite version yields an exact uniform result over **every** $20\le m\le10^{100}$ for the same indexed exit. The opening and initial bulk run reach an ordinary reset or a jump without a halt or exceptional restart. On the latter branch, through the next eight grouped ordinary blocks and the decision immediately following them, every path either returns normally or continues by ordinary moves. The subsequent fate of a longer excursion is open. The [phase sieve](power_phase_sieve_758.py) verifies this claim in seconds using integer and rational arithmetic.

The threshold set starts at $\{0,1/3,5/9,1\}$ and includes all its preimages under at most eight inverse branches. There are 1,024 distinct thresholds. For each $z$ in the set the checker proves the simultaneous inequalities
$$
\left\|m\log_b 3 + \log_b\frac{2(3-z)}{3K}\right\|>2^{-500}
\qquad(1500\le m\le10^{100}),
$$
where $\|\cdot\|$ is distance to the nearest integer. Taking $z=1$ excludes an integer seam in $v_m$; $z=0$ gives the same test modulo one. Thus the actual initial bulk count is $j=\lceil v_m\rceil\le3m$. Indeed $|D_{j+1}-3Kb^j|\le28+9(j+1)$, whereas away from the seam its ideal gap from $4P$ on both neighboring comparisons is greater than $P2^{-502}$. The same inequalities and the derivative of $3-2b^\theta$, whose absolute value exceeds $1/2$, put the ideal post-jump direction more than $2^{-501}$ from every threshold, including both endpoints of $[0,1]$.

Specifically, were the first jump to be taken, its direction would be $3(4P-D_j)/(4P+G_j+4)$. From $|D_j-2Kb^j|\le28+9j$ it differs from the ideal by less than $100(m+1)/P$. Separation from 0 and 1 ensures $1<a_j<c_j$ before this call, excluding any intermediate seam reset and justifying the immediate reset for odd $j$ or the jump for even $j$. At a later odd/odd state the jump threshold differs from $1/3$ by at most $2/u$, the two-bulk threshold differs from $5/9$ by less than $20/u$, and the angular output of a valid ordinary block differs from its affine approximation by less than $20/u$ (substitute the four exact bulk-pair constants). The ideal directions at each later guard stay at least $2^{-501}$ from the applicable boundaries because the forward slopes exceed one and all preimages were checked. The mass coordinate satisfies $u\ge P$, and propagation through eight blocks costs less than $2000\cdot3^8(m+1)/P<2^{-510}$ at all these exponents. These margins also keep the physical coordinates away from premature resets at the axes. The remaining $20\le m<1500$ are checked directly using their exact bulk counts and actual integer transitions.

To verify the simultaneous phase inequalities put $Q=2^{1024}$. The checker encloses $K$ between $(r_{2000}+7)/b^{2000}$ and $(r_{2000}+13)/b^{2000}$. It bounds logarithms by summing $2\sum_{j\ge0}y^{2j+1}/(2j+1)$, with $y=(x-1)/(x+1)$ after reducing $1\le x\le2$. The geometric tail after 400 terms is below $1/Q$; all roundoffs are outward integers at scale $Q$. Let $A/Q,B/Q$ approximate the rotation and its threshold-specific offset. The code verifies that the combined error even at the largest $m$ is below $2^{-501}$. It then counts exactly how many residues $Am+B\pmod Q$ meet the interval of radius $2^{-499}Q$ about zero. The count is the difference of two sums of floors of affine functions of $m$. Euclidean lattice transposition evaluates each sum in time logarithmic in the modulus and upper exponent. Every count is zero.

Run `python3 power_phase_law_758.py` beside the original checkers to reproduce the entrance examples and finite counts for $20\le m\le2000$. The limiting laws and sparse-exponent estimate follow from the argument above.
