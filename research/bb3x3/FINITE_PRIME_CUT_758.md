# A rational crossing for every finite choice of primes

For **every finite set of primes** $S$, a rational trajectory crosses the whole known halting band around $H$ using ordinary instructions, satisfies every required real branch inequality, and has coordinates in $\mathbf Z_p$ for all $p\in S$ at every phase. The primes can be chosen after seeing $H$, and any desired integer cut in the band can be made an exact phase mass. One can additionally prescribe any fine ordinary word of at most 200 elementary calls, and specify where the exact cut falls within it. All these trajectories have noninteger coordinates. They establish a limitation on proofs that relax the integer state to real inequalities and finitely many prime-adic integrality tests. A joint test that requires an actual integer in the intersection of the real and residue constraints can distinguish these trajectories. [Integer matching at finite depth](CUT_WORD_MATCHING_758.md) · [Earlier single rational crossing for all 64-bit moduli](MODULAR_GATE_LIMIT.md)

Write $u=(a+2c-1)/2$ and $d=(c-1)/2$. Let $B$ be the pair of ordinary bulks with incoming $d=0\bmod4$. The two affine steps used here are
$$
J:(u,d)\longmapsto(u+2,3d-u+1),\qquad
B:(u,d)\longmapsto(u+5,(9d+20)/4).
$$
We consider the cyclic word $W_n=(BJ)^nJ$ with $n\ge3$. There are at most two consecutive jumps and there are no consecutive $B$ blocks. This keeps the guards uniform when the period grows.

## Choosing the period after the primes

A full period, starting at any cyclic phase, takes the form
$$
(u,d)\longmapsto (u+V,(K d+A u+C)/L),
\qquad K=3\cdot27^n,\quad L=4^n,\quad V=7n+2
$$
with integer $A,C$. Put $q=K-L$ and solve for the invariant affine graph $d=xu+b$. The equations give $x=-A/q$ and $b=(LVx-C)/q$. In particular all phase denominators divide $q^2$. The graphs at consecutive phases map to each other by uniqueness.

Take $m$ to be the product of the primes in $S$ other than two and three. Choose $n\ge3$ divisible by $\varphi(m)$, using $\varphi(1)=1$. Euler's theorem gives $q\equiv2\pmod m$, and $q$ is always odd and coprime to three. Consequently every coordinate has denominator coprime to every prime in $S$, through any number of steps. The pair also has its correct dyadic label: at its input $d=(4d'-20)/9$ is zero modulo four, since the following phase is integral at two. [Grouped guards](MIXED_TERMINALS_758.md)

## Real branch guards independent of the period

The two normalized inverse maps are $f_B(y)=4y/9$ and $f_J(y)=(1+y)/3$. Both are contractions of $[0,1/2]$ into itself. Their cyclic fixed points give the phase slopes $x$. Every $B$ is followed by $J$, so its slope is at least $4/27$. Every $J$ slope is at least $1/3$. A $B$ slope is at most $2/9$, and there are at most two jumps before the next $B$. Thus all slopes are at most $f_J^2(2/9)=38/81$.

The phase offsets lie in $[-7,0]$. In reverse, a jump replaces the next offset $b'$ by $(b'-1+2x')/3$ and a $B$ by $(4b'-20+20x')/9$. Each is a contraction preserving $[-7,0]$, so the cyclic solution lies there. At each $J$ phase $3x-1=x'\ge4/27$. At each $B$ phase $2-9x=2-4x'\ge10/81$. Together these imply the real guards $3d\ge u-1$ at $J$, and $9d\le2u-12$ at $B$, for every $u\ge200$. Both $d$ and $u-2d-1$ are positive throughout. These bounds verify the ordinary rational branches at every phase inside and beyond the target band, regardless of $n$.

Start any phase at a chosen integer cut $T$ around $H$ and continue backward until the lower edge of the band is crossed, and forward through the upper edge. The mass changes by two or five on each grouped instruction, and every visited mass exceeds 200.

## Why these states are genuinely nonintegral

At the phase just before $(BJ)^nJ$, let $F=f_B\circ f_J$. Its fixed point is $4/23$, its slope is $4/27$, and $x=F^n(f_J(x))$. Hence
$$
0<x-4/23=(4/27)^n(f_J(x)-4/23)<(4/27)^n/3.
$$
The reduced denominator of $x$ is therefore larger than $3(27/4)^n/23>7n+2=V$ for $n\ge3$. If any phase had integral $d$, its real guard and dyadic label would make all subsequent values integral. Two consecutive visits to the indicated phase have $d$-difference $xV$, which is nonintegral. This excludes every such integer state directly.

## Prescribing an incoming and outgoing word

Fix any fine word $U$ of at most 200 elementary calls and any grouped boundary in it. Each $P_r$ counts twice and specifies $d\bmod4=r$. Append a repair word to $U$ so that the combined tail has exactly one more $J$ than $P$. If the tail needs more jumps, append that many $J$s. Otherwise append the required number of residue-zero pairs. In the period $(BJ)^n$ followed by this repaired tail, let $N$ be the total number of pairs; the number of jumps is $N+1$. Choose the filler length $n$ arbitrarily large with $N\equiv0\pmod{\varphi(m)}$. The same graph calculation now has $q=3\cdot27^N-4^N$, again coprime to the chosen primes and to six. At any pair the inverse formula $d=(4d'-b_r)/9$ ensures $d\equiv r\pmod4$ for its designated correction $b_r$.

There are at most 202 consecutive jumps or pairs, including rotation through the end of the period. Indeed each count in the repaired tail is at most 201, and the alternating filler adds at most one instruction to a run. All coarse direction maps are unchanged when a pair's residue changes. A run of pairs of length $t$ followed by a jump has initial slope at least $(4/9)^t/3$. Before a run of $t$ jumps followed by a pair the gap below $1/2$ is at least $5/(18\cdot3^t)$. Therefore at every phase both $x$ and $1/2-x$ are at least $1/(4\cdot3^{202})$. All four reverse pair maps for the offset preserve $[-7,0]$ since $0\le b_r/4-v_rx'\le35/4$ with $0\le x'\le1/2$, where $v_r$ is the mass gain. Thus at every $u\ge1000\cdot3^{202}$ the jump guard $3d\ge u-1$ holds at $J$ phases, and the sufficient guard $2u-9d\ge18$ holds at each chosen pair. This is below $H-10^{100}$.

To see that the graph remains noninteger, the repaired tail cannot fix the direction $4/23$. The normalized forward itinerary there is the two-cycle $B,J$, and the jump and pair domains are disjoint. Every return to that direction uses equal numbers of jumps and pairs. Consequently $0<|x-4/23|<(4/27)^n/3$ at the beginning of the filler. Its reduced denominator grows exponentially with $n$, while the total mass gain grows linearly. Choose $n$ large enough that the former exceeds the latter. The preceding nonintegrality argument applies. Place the specified phase of $U$ at the requested cut and extend along the phase graphs in both directions through the band.

The [checker](finite_prime_cut_758.py) reconstructs the graphs and checks the guards for six prime selections and five prescribed words, including 200 consecutive jumps and 100 consecutive residue-three pairs. The general choice of period and the uniform inequalities cover every finite prime set and every indicated fine word.

~~~sh
python3 finite_prime_cut_758.py
~~~
