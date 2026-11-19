# A word-complexity test for the actual blank crossing

If the blank trajectory passes the full deep-entry interval at scale 74 without a reset there, that single passage must contain **at least $10^{22}$ distinct fine words of 401 blocks**. In the joined halting interval, an infinite trajectory must similarly exhibit **at least one million distinct fine words of 325 blocks**. A block is either an odd/odd jump J or a pair P of ordinary bulk moves with the input residue specified. Both bounds count words on that single trajectory. [Scale-74 entry interval](SCALED_GATES_758.md) · [Halting interval](UNIVERSAL_758.md) · [Verifier](factor_complexity_758.py)

## Why a repeated word puts the states on a line

At an odd/odd state put $u=(a+2c-1)/2$ and $d=(c-1)/2$. For a fine word of $n$ blocks with $j$ jumps and $p$ pairs, its affine map on all its legal occurrences has the form
$$
(u,d)\longmapsto \left(u+V,\ (Qd+Au+C)/M\right),\qquad Q=3^{j+2p},\quad M=4^p .
$$
Here $j+p=n$, $Q$ and $M$ are coprime, and the drift $V$ is fixed by the word. Every continuing block increases $u$ by at most nine. [Fine branch rules](EXCURSION_POWERS_758.md)

Take $T$ consecutive starting positions of length-$(n+1)$ words, with the entire segment at $u\le U$. Consider three occurrences of the same length-$n$ word among the prefix and suffix positions. Twice their signed triangle area is an integer determinant $D$. After the word, the determinant is $D'=QD/M$. Integrality gives $Q\mid D'$. The differences of the three $u$ values remain unchanged and have magnitude at most $9T$. The final $d$ values lie in $[0,U/2]$. Expanding the determinant gives $|D'|\le 9TU$. If $3^n>9TU$, then $D'=D=0$. Thus every length-$n$ word that occurs at least twice has one well-defined line containing all its occurrences. It is nonvertical because $u$ strictly increases.

## How a repeated sequence of lines would force a periodic tail

Write $F$ for the number of distinct length-$(n+1)$ words in the segment. Regard each as an edge joining its length-$n$ prefix and suffix. At most $F$ edges occur just once. On an edge that occurs at least twice, the first block sends two distinct points of the prefix line to two distinct points of the suffix line. It therefore maps the whole first line onto the second one.

Follow consecutive occurrences of these repeated edges along the actual trajectory. If any length-$n$ word occurs twice within this stretch, the intervening fine word maps that word's line to itself. Its composite expands the transverse direction by $Q/M>1$, and it has positive mass drift. It has a unique invariant nonvertical line. The initial point is on that line, and a full copy of the word is legal. The [affine-period argument](EXCURSION_POWERS_758.md) proves every future copy is legal, with the same bulk residues and increasing guard margins. This would produce a periodic ordinary tail. The global denominator bound and exhaustive finite direction calculation exclude every such tail. [Exclusion of periodic tails](FINITE_AFFINE_PERIODS_758.md)

Each stretch therefore contains at most $F$ repeated edges, because a longer stretch would revisit one of its at most $F+1$ distinct vertices. The singleton edges divide the observed sequence into at most $F+1$ stretches. Consequently
$$
T\le F+(F+1)F=(F+1)^2-1 .
$$
In particular, $T=k^2$ forces at least $k$ different words.

## Finite tests for the blank trajectory

For scale 74 let $G=10^{10}3^{74}$, $B=H-3G/2$ and $U_0=H-G-39{,}000{,}000$. A reset in $[B,U_0]$ enters the gate. For the joined halting interval use its two verified endpoints as $B,U_0$. If a trajectory passes either interval without a reset in it, consider the part between mass $2B+1$ and $2U_0+1-5458$. An exceptional step there produces a reset after exactly 787 updates with mass gain 5,458. The bulk-decrement bounds for this identity cover both trimmed intervals. Thus only J and ordinary bulk moves occur in the passage. Discard at most one elementary move at each end to align its complete blocks. [Exceptional-return annulus](CUT_758.md)

| Interval passed without entry | Length-$n$ factors used to determine lines | Consecutive starting positions $T$ | Minimum number of distinct length-$(n+1)$ factors |
|---|---:|---:|---:|
| Deep-entry interval at scale 74 | 400 | $10^{44}$ | $10^{22}$ |
| Original joined interval | 324 | $10^{12}$ | $10^{6}$ |
| [Enlarged joined interval](LOWER_SCALE_GATES_758.md) | 321 | $1{,}900{,}000^2$ | 1,900,000 |
| [Scale-19 joined basin](TARGET_BASIN_758.md) | 333 | $1{,}407{,}176{,}247^2$ | 1,407,176,247 |
| [Scale-20 joined basin](TARGET_BASIN_758.md) | 334 | $2{,}437{,}300{,}755^2$ | 2,437,300,755 |
| [Scale-10 halting corridor](LOWER_SCALE_GATES_758.md) | 323 | $6{,}300{,}000^2$ | 6,300,000 |

The verifier checks $3^n>9TH$ in every row, and that the mass gain across the trimmed interval supplies at least $T+n$ complete blocks. A sufficiently low upper bound on the number of words on the actual crossing would force entry into the relevant interval. Entry at scale 74 fixes one exact subsequent trajectory; its continuation to a halt remains open.

The same argument can single out the actual midpoint state. Set $T_0=H-5G/4$. A reset between $B$ and $T_0-39{,}004{,}000$ forces the first mass crossing of $2T_0+1$ to be exactly $A(2\cdot3^{36}-1,T_0-3^{36}+1)$. If the blank reaches the midpoint in a different state, apply the proof to this shorter interval with $(7\cdot10^{21})^2$ starting positions and $n=400$. There must then be at least **$7\cdot10^{21}$ distinct length-401 words** within the passage. [Exact midpoint and inverse proof](SCALE74_ANCESTRY.md)

## Infinite ordinary excursions

Let $p(k)$ be the number of distinct length-$k$ fine words occurring on an infinite ordinary tail. Then
$$
\liminf_{k\to\infty}\frac{\log p(k)}{k}\ \ge\ \frac{\log 3}{4}.
$$
Indeed, fix its first mass coordinate $u_0$. For sufficiently large $n$ choose $T=\lfloor 3^{n/2}/20\rfloor$ and bound $u$ on the first $T+n$ blocks by $u_0+9(T+n)$. These choices satisfy the determinant inequality. Applying the preceding word count and taking logarithms gives the stated lower bound. The same bound extends to infinite trajectories with arbitrarily many resets or exceptional moves. [Every infinite orbit](ALL_ORBIT_ENTROPY_758.md)
