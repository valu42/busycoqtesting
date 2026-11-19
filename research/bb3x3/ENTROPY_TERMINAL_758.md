# A halting fine trace with congruent continuing traces

Fix any positive modulus $M$. At each lifted exponent $m=292+242660k$ put
$P=3^m$ and let $H_m$ be the [halting seed](LIFTS758.md). For every nonzero
multiple $t$ of $2^{15}M$ with $|t|\le P/10000$, the reset at $H_m+t$
executes exactly the same $m$ leading jumps and the same fourteen fine
ordinary instructions as the reset at $H_m$. At every corresponding state,
both counters agree modulo $M$. Their next instructions are as follows.

| Seed | Instruction after the common trace |
|---|---|
| $H_m$ | Halt at gap three |
| $H_m+t$, $t>0$ | Return to a reset |
| $H_m+t$, $t<0$ | Continue with an ordinary bulk |

For every fixed $M$, the interval admits both signs at every sufficiently
large family member. One sequence of shadows even works simultaneously
for every fixed modulus. At family index $k\ge1$ use
$t_k=2^{15}\lfloor\sqrt{k}\rfloor!$. Every fixed modulus eventually
divides $t_k/2^{15}$, while $\log t_k=O(\sqrt{k}\log k)=o(k)$ ensures
$t_k/P\to0$. Thus all the fixed-suffix normalized directions have the
same limits on this pair of sequences.

In particular the full finite ordinary trace,
all absolute residues modulo $M$ along it, the exponent class, and
the limiting normalized directions along its fixed suffix can coincide
with those of a halting family while the next instruction returns alive.
The [five-letter theorem](ALL_ORBIT_ENTROPY_758.md) guarantees that fine
words occur in the reset-dense alternative. This construction identifies
the extra information needed to apply it to this halter. The absolute
terminal gap must be controlled on the orbit. It leaves open whether an
earlier reset selects the exact halting seed or its basin.

## Proof

After the leading jumps, changing the seed by $t$ changes the two counters
by $(0,t)$. On a common jump their displacement $(A,C)$ becomes
$(3A,C-A)$. On a common ordinary bulk it becomes $(A-C,3C/2)$ as long
as the right residues agree modulo four. There are 13 bulks in the
common suffix $L^8JL^5$. Taking $2^{15}M\mid t$ retains divisibility
of both displacements by $4M$ throughout. In particular the fine
bulk labels agree. The final displacement equals
$$
 t\left(-\frac{4,650,361}{4096},\frac{4,658,553}{8192}\right).
$$
The gap after the common trace is therefore $3-13959275t/8192$.
Both inputs retain the parity and right residue of the original halting
state. At positive $t$ the even left counter is smaller than the odd
right counter and returns. At negative $t$ the gap exceeds four,
making an ordinary bulk legal.

The suffix guard margins hold throughout $|t|\le P/10000$. The
[verifier](entropy_terminal_shadow_758.py) propagates the two rational
endpoints at $t=\pm P/10000$ using the unguarded affine fine maps.
At each endpoint, both counters and the signed margin of every proper
suffix instruction exceed seven at $P=3^{292}$, and their slopes in
$P$ are positive or zero. Both final counters also stay positive.
All margins are affine in $t$, so these endpoint checks give the
guards throughout. The positive first right counter makes all leading
jumps legal, and they preserve the initial displacement.

## Every fine word is also compatible with a live return

For any prescribed finite fine word $w$, any odd modulus $N$, and any
initial seed residue $r\bmod N$, there are odd resets congruent to $r$
whose first excursion contains $w$ and then returns alive. This holds
at every sufficiently large leading exponent $m$, including along any
arithmetic progression of exponents.

Use the real inverse branches in the five-letter proof to build a fixed
open corridor just above $3^m$ with the complete coarse return
$J^m P^7 w_c P^\epsilon L R$, where $w_c$ forgets the fine residues and
$\epsilon$ makes the total number $K$ of pairs odd. The coarse return
holds for every odd seed in the corridor. Put $z=(s-1)/2$. Two
$z$ values differing by a multiple of $4^K$ have the same $K$ fine pair
labels. Indeed each pair consumes at most two bits of the displacement,
and jumps consume none. Conversely, the exact displacement calculation
in the five-letter proof gives $4^K\mid(z-z')$ for equal fine lists.
The corridor contains every class for large $m$, so the $4^K$ classes
correspond bijectively to all $4^K$ lists. Choose any list with the
prescribed middle labels. The Chinese remainder theorem intersects
its class modulo $4^K$ with $2z+1\equiv r\pmod N$. The fixed relative
corridor eventually exceeds the resulting period in the seed.

This supplies genuine reset excursions for the entire finite language,
including every combination with an odd absolute residue at entry.
It makes no assertion about which excursion the blank orbit selects.

## How a fixed corridor loses absolute position

The same issue arises when using a whole odd-to-odd first-return
corridor to send a dense crossing to an exact boundary reset. Suppose
its increment has the form $F(s)-s=2m+g(s\bmod D)$ for a fixed even
period $D$ and bounded $g$. These hypotheses apply to a fixed ordinary
tail after the maximal leading jumps on a region where its guards
all hold. On a residue cycle of length $l$, the lifted $l$-return sends
$s$ to $s+wD$ with integer
$$
 w\ge l(2m+\min g)/D.
$$
At any one phase of the cycle the starts in that residue class split
into $w$ disjoint tracks. They stay distinct even through intermediate
phases, by the defining period of the residue cycle. Every track has
a representative in a deep entrance interval of fixed relative width
once that interval is wider than $wD$. Here $wD=O(m)$ since $D$ is
fixed, whereas the entrance width is proportional to $3^m$. Distinct
tracks cannot share the first exit across the end of the corridor. Such a shared exit would place both exits at the same cycle phase and same integer
lift. Thus the number of possible boundary exits grows at least
linearly in $m$ for a fixed template. This argument permits
coalescence on a later different return word. It also permits templates
whose length or residue period grows with the exponent.
