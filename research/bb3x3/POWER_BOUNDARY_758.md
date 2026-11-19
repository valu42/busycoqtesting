# Crossing the change of word at each power of three

For every $m\ge20$, the exact power skip extends through the first change of instruction pattern and the entire ensuing sequence of ordinary bulk calls. The extension computes the next counter state and its raw clock. It needs at most 25 more first-return evaluations near the boundary, a launch of $m$ or $m+1$ counter calls, and fewer than $3m$ bulk calls. At $3^{292}$ and its double, every candidate exit of the established gates has a live next call after this extension. The trajectory beyond that next call still depends on the exit phase. [Power skip](power_skip_758.py) · [Exit phases](POWER_GATES_758.md) · [Boundary verifier](power_boundary_758.py)

Put $P=3^m$ and let $q=P-2m-4$ at the first gate, $q=2P-2m-6$ at the second. Follow the reset sequence to the first odd reset above $q$ at the first gate or the first even reset above $q$ at the second. Each such departure has an even offset $e=s-q$ and the following exact launch.

| Gate | Range containing every departure offset | Launch length | State after launch |
|---|---:|---:|---|
| $P$ | $2\le e\le4m+34$ | $m$ | $(2P-1,\max(1,e-3))$ |
| $2P$ | $2\le e\le4m+16$ | $m+1$ | $(4P-1,e-1)$ |

At $P$, the first $m-1$ jumps give $(2P/3-1,2P/3+e-5)$. For $e\ge4$ they are followed by one more jump. For $e=2$ the counters differ by two and the right counter is 3 modulo four. The exceptional rule gives $(2P-1,1)$, exactly the launch for $e=4$. At $2P$ the initial even rule and $m$ jumps give the displayed launch directly. Positivity of the last right coordinate over the respective run of jumps ensures legality of all preceding jumps.

## Reaching the departure from the skip

Write $z=s+2m$. The primary power skip stops at the first reset above $bP-1000-2m$ for $b=1,2$. On the parity which keeps its word across $q$ (even at $P$, odd at $2P$), the same word holds throughout $|z-bP|\le P/1000$. At all four endpoints the verifier checks each affine guard margin at $P_0=3^{20}$ and checks its nonnegative slope by evaluating at $P_0+1$. This proves the claim throughout the two intervals at every larger $P$. The required starts satisfy $bP-1000\le z\le bP+2m+11$; indeed $2m+11,1000\le P/1000$ at $m=20$ and thereafter.

For the other parity only the short approach up to $q$ needs checking. At $P$, after $m-1$ jumps the two counters differ by $P-z\ge4$, enough to take the ordinary bulk. At $2P$, after the initial even rule and $m-1$ jumps the difference is $2P-z-4\ge2$. When it equals two the right counter is $4P/3-3\equiv1\pmod4$, which permits the bulk. Every other such even seed has difference at least four. In both cases the new left counter is even and between zero and 1,000, and the new right counter exceeds 1,000. The next call returns. An even left counter of zero is a legal return input.

The seed gains at $P$ are at most $2m+5$ on odd starts and $2m+29$ on even starts. At $2P$ the bounds are $2m+7$ on odd starts and $2m+9$ on even starts. These follow by adding the gains of the known words, including the last return. Each gain is odd and at least $2m+3$, so the seed parities alternate. A return from the desired parity at or below $q$ cannot send the complementary parity beyond $q+2m+9$; the next return gives the bounds in the table. This also covers the first exit above the primary skip's endpoint. The distance to $q$ there is less than 1,000, so at most $\lceil1000/(2m+3)\rceil+1\le25$ subsequent returns are needed.

## The first maximal bulk run

Set $x=\lfloor(c+1)/4\rfloor+3$. For either bulk residue the guard and exact update are
$$
a\ge4x-9,\qquad (a',c')=(a-4x+9,6x-13),\qquad x'=\lfloor3x/2\rfloor .
$$
At both launches, $3\le x_0\le m+12$. Through $2m$ bulk calls the sum of the proposed decrements of $a$ is below $8(m+12)(9/4)^m<P$. The last inequality holds at $m=20$, and $8(m+12)(3/4)^m$ decreases thereafter. Each proposed decrement is positive, so all $2m$ guards hold. Conversely, $x_i-1\ge(3/2)^i(x_0-1)$. Were $3m$ bulks legal, the last decrement alone would exceed $4P-1$, the largest possible launching left counter. The exact first nonbulk call is therefore reached after $2m\le k<3m$ bulks. Summing each permitted call's raw clock and the launch clock times the extension, including the case where $a=1$ at the end. [Clock rules](timing_758.py)

At $m=292$ the 224 possible first-gate departures give 120 jumps and 104 live returns as their first nonbulk call. The 296 second-gate departures give 140 jumps and 156 live returns. These exhaust the two sets computed by the gate verifier. Run `python3 power_boundary_758.py` to reproduce the counts and compare the scalar update against literal counter calls.
