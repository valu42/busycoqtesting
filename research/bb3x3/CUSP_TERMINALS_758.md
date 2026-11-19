# A direct terminal family inside the reset-density cusp

For every $m=597+1200j$, $j\ge0$, two odd reset seeds halt after $m$ ordinary jumps and fifteen ordinary bulk moves, on the next counter call. Their common limiting position is strictly inside the [reset-density cusp](ALL_ORBIT_ENTROPY_758.md):

$$
\lim_{m\to\infty}\frac{s_m}{3^m}=1+\frac{65,536}{42,981,185}=1.001524760194\ldots.
$$

These are all the exponents with a direct fifteen-bulk halt from an odd reset after its maximal initial run of jumps. Consequently, under the sublinear-ordinary-stretches alternative for an infinite orbit, that orbit actually visits a reset in **every fixed neighborhood** of these terminal pairs on all sufficiently large favorable scales in this exponent progression. The threshold depends on the neighborhood. The pair has fixed width in integer seed units; passage through all fixed relative neighborhoods leaves its exact reachability open.

## Exact family

Set $P=3^m$, $D=3^{16}-2^{16}=42,981,185$ and $Q=2^{15}$. Put

$$
i=28,826+Q\frac{P-75,627,293}{2D},\qquad s_m=P-2m+4i-2.
$$

The two seeds are $s_m,s_m+2$. Immediately after the $m$ jumps they have first counter $2P-1$ and second counters $4i-1,4i+1$. Both first bulks lead to $(2P-4i-4,6i+5)$. On applying fourteen more bulks, retain the left counter in the form $2P+A$, and call the right counter $C$. At $i=28,826$ this gives $(A,C)=(-100,759,486,50,495,099)$. The gap is one exactly when $P=75,627,293$ there.

Increasing $i$ by $Q$ preserves every bulk residue. The difference of right counters starts at $6Q$ after the first bulk and is multiplied by $3/2$ on each of the other fourteen. Hence the final $C\bmod4$ is unchanged and $C-A$ increases by $4D$. The target power residue is therefore modulo $2D$. Enumerating $0\le i<Q$ with the two possible terminal gaps, one or three with $C\equiv3\pmod4$ in the latter case, and the 1,200 distinct powers of three modulo $2D$ gives exactly $(m\bmod1200,i\bmod Q,\text{gap})=(597,28826,1)$. For the displayed increasing family, positivity of the final left counter verifies that all prior bulk decrements are available. The initial jump run is legal because its final right counter is positive and the next call is a bulk. Fifteen bulks change the odd left counter to an even one, so the final gap one halts.

The first member occurs beyond the exponent 292 of the known target $H$. At exponent 1,797, resets $s_m-2m-23$ and $s_m-2m-25$ each reach $s_m$ in one first return. Thus some of the direct seeds have earlier reset ancestors.

## The return words just below the pair

Write $z=(s+2m)/P$, $R=(3/2)^{15}$, and $z_*=1+2/(3R-2)$. After fifteen bulks the difference of the two counters divided by $P$ is $2-(3R-2)(z-1)+O(1/P)$. All previous guards are strict in the limit at $z_*$. Just below the target, at $z=z_*-\delta$ with $\delta P$ large, the next call is therefore a sixteenth bulk. Its resulting left counter is $(3R-2)\delta P+O(1)$; the right counter divided by $P$ stays bounded away from zero. The left counter is odd. A subsequent jump run triples the left counter plus one at every call, so its length is $\log_3(1/\delta)+O(1)$ as $\delta\downarrow0$ and $\delta P\to\infty$. In particular, all fixed relative neighborhoods on the approach side contain arbitrarily many different return prefixes as $m$ increases. At even starts the short ordinary word throughout this cusp already established in the [density proof](ALL_ORBIT_ENTROPY_758.md) leads back to an odd reset.

## Why a fixed residue cycle cannot select the two seeds

Consider any fixed open subinterval in the cusp. It contains a closed subinterval of positive length on which the odd launch, after its $m$ leading jumps, has a fixed strict ordinary return word for all sufficiently large $m$. Indeed the inverse direction branches of a surviving coarse block have contractions $1/3$ and $4/9$. The total length of the possible directions surviving $k$ such blocks is $(7/9)^k$. Thus every open direction interval contains an open ordinary return cylinder. The even cusp word is fixed and always returns to odd. On a smaller subinterval, either one odd first return, or that return followed by the even first return, gives a map from odd seeds to odd seeds
$$
F_m(s)=s+d_m(s\bmod M).
$$
The modulus $M$ is fixed because each bulk consumes one binary digit of precision and the number of bulks is fixed. All the increments are $2m+O(1)$ for single returns or $4m+O(1)$ for pairs.

Fix a cut inside this interval, above a fixed open subinterval of permitted starts. On any residue cycle of $F_m$, let $S$ be the sum of its positive increments. There are exactly $S/M$ different integer exits through the cut belonging to this cycle: each cycle edge contributes its lifts that start at or below the cut and end above. The count is obtained by summing the differences of the integer quotients by $M$, which telescope around the residue cycle. Their destinations are distinct because the map permutes the cycle. Each exit has a backward continuation by full periods of displacement $S=O_M(m)$ into the permitted start interval, whose width is proportional to $3^m$. Therefore **at least $\Omega(m)$ distinct exits are possible on one cycle alone**, in a seed window of width $O(m)$. This count applies even on a fixed congruence class of exponents. Every one of these lifted paths has mesh $O(m/3^m)$ in relative coordinates across the interval. Local reset density is compatible with every phase.

There is also an obstruction to following all these phases by a uniformly short capture. In an $O(m)$-wide seed window at mass comparable to $3^m$, the number of distinct fine ordinary excursion words with at most $b$ bulk moves is $O_b((1+\log m)^{b+1})$, allowing arbitrary lengths of the jump runs. To see this, after any fixed fine prefix the jump coordinate $h=(a+1)/2$ is affine in the seed and $u=(a+2c-1)/2$ equals the seed plus a constant at odd phases. A maximal run of $k$ jumps has $3^k h$ comparable to $u$ and $k=O(m)$: the exact next-jump guard is $3h\le u+2$, with $u$ gaining two per jump. Mass remains comparable to $3^m$ with boundedly many runs. If $h$ varies, delete its smallest value from the possible seeds in the window. All the remaining positive $h$ values have ratio at most one plus the width of the seed window because the affine slope is constant and distinct integer seeds are at least one apart. A constant $h$ needs no deletion. There are therefore only $O(1+\log m)$ choices of $k$, including the possible outlier. Branch on these choices and at most two fine bulk labels, and repeat through the bounded number of bulks. A return hitting $a=1$ on a bulk can stop there. An exceptional restart outputs a first counter comparable to $3^m$ and right counter one; it must take more than any fixed number of consecutive bulks before it can return or halt.

A fixed returning fine word adds a constant to the seed, by its exact mass charges. A fixed terminal fine word applies to at most two seeds: the left counter minus the right counter is strictly decreasing with the seed along a fixed ordinary word from a given parity, and the only terminal gaps are one and three. For any fixed number of such excursions the window remains $O(m)$ wide; counting their words multiplies fixed powers of $1+\log m$. Consequently only a power of $1+\log m$ of the $\Omega(m)$ phases can hit a bounded list of reset targets or halt within a bounded number of returns using boundedly many bulks per excursion. **Any all-phase argument forcing a terminal from a fixed interval at infinitely many scales must allow unboundedly many returns or unboundedly many bulk moves.** This obstruction leaves open a growing sequence of residue gates and does not select the phase followed by blank.

Run [cusp_terminals_758.py](cusp_terminals_758.py) with Python 3 beside the existing counter rules. It exhausts the integer residue condition and independently replays the first two terminal pairs.
