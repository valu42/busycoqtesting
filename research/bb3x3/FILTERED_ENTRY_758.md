# A short membership test across a wider ordinary-state band

There is a deterministic sufficient halting test for odd/odd states with

$$
2\le h=(a+1)/2\le1,012,257,878,130,399,645,022,
\qquad h\text{ even},
$$
$$
H-F\le u=(a+2c-1)/2\le H-L-2488,
$$

where $F=53,463,914,736,831,321,850$, $L=3,403,055$,
$D=13,959,275$, and $H=(3^{307}-8,282,708,212)/D$.
For these odd/odd states $u$ is even. The test uses at most **60 elementary
angular updates**. Every accepted state reaches a reset inside the
[established halting basin](TARGET_BASIN_758.md) within **553 counter calls**.

Of the **506,128,939,065,199,822,511** possible even left coordinates, at
most **1,817,019,372,897** are left inconclusive. This bound applies at
every allowed even mass. Thus the test certifies at least
**13,529,817,173,439,023,215,201,758,674,733,101,452,556** nonreset states in
the band. These are counts of a specified finite set, not probabilities
for the blank trajectory. An inconclusive result does not imply
nonhalting; the blank trajectory's entry into this set remains open.

## The membership test

Let $r$ be the least integer with $3^r>Dh$.

1. If $r\le57$, accept by the
   [enlarged rectangular criterion](TARGET_BRIDGE_EVEN_758.md).
2. Otherwise initialize $x=Dh/3^r$, and apply the exact angular rules
   $J:x\mapsto3x$ for $x<1/3$, and
   $P:x\mapsto(9x-5)/4$ for $x>5/9$.
   A direction in $(1/3,5/9)$ gives an ordinary return, so accept it.
3. Stop at the first complete block boundary $m\ge r$, counting $J$ as
   one elementary call and $P$ as two. If the direction there is already
   in the return interval, accept. Otherwise accept when the prefix
   contains at most 28 pairs. Leave the remaining cases inconclusive.

The [implementation](filtered_entry_758.py) exposes `accepts(h, u)` and
`classify_left(h)`. It uses integer comparisons throughout, including the
angular computation. The latter function reports the cut exponent, depth,
pair count and reason for its decision.

## Why the predicate is sufficient

The upper left-coordinate bound is the largest even integer at most
$(H-F)/3^{248}$. Therefore the physical orbit starts with at least 248
jumps. Its maximal initial jump count $k$ is at most 292, as in the
[earlier nonreset criterion](NONRESET_ENTRY_758.md).

Put $U=3^{307}/D$. The ideal and physical launch counts agree, with
$k=307-r$. To check this without simulating the launch, evenness of $h$
excludes equality between $Dh$ and a power of three. At the proposed
last jump, $h_*=3^kh$ satisfies

$$
U-h_*\ge3^k/D>F+2600,
\qquad 3h_*-U\ge3^{k+1}/D>F+2600.
$$

The physical aligned mass is $u_*=u+2k$, with
$0<U-u_*\le F+594$. The last jump is therefore legal and the next is
illegal. In particular $r\le59$, $1/3<x<1$, and a surviving angular prefix
starts with $P$.

The [physical-shadow argument](TARGET_SHADOW_758.md) applies uniformly
through aligned depth 248. An inverse guard at depth $l$ has an odd
numerator over a power $3^t$, with $t\le l+2$, or is zero. Since $h_*$ is
even, its distance from the guard at mass $U$ is nonzero and at least
$3^{\min(k,307-l-2)}/D$. The exact inequality

$$
3^{57}>D(F+2600)
$$

therefore proves every required guard comparison through $l=248$.
This includes the possible exceptional edge, the terminal after one bulk,
and an earlier visit to $h=1$.

At the first cut $m\ge r$, one has $m=r$ or $r+1\le60$. If the prefix
contains $p$ pairs, its inverse form is

$$
x_{\rm initial}=\frac{A+4^p x_{\rm tail}}{3^m},
\qquad N+A=3^{m-r}Dh,
\qquad x_{\rm tail}=N/4^p.
$$

The forced first pair makes $A$ an odd multiple of five, and the remaining
inverse updates preserve this property. Thus $N$ is an odd multiple of
five with $0<N<4^p$. For $p\le28$ these are exactly the directions covered
by the [existing dyadic exhaustion](DYADIC_SURVIVAL_758.md).

An unlisted tail returns by its guard at most 188 elementary calls after
the cut, hence by aligned depth $60+188=248$. The archived longer tails
retain sufficient individual physical clearance even at cut depth 60;
the checker verifies this with their exact minimum pulled-back margin.
Their longest time to the final guard is 243 calls. The final bulk and
reset give the common bound

$$
k+m+243+2\le307+1+243+2=553.
$$

Mass increases by at most nine per call, so the returned seed obeys
$u<s\le u+2488$. It is consequently inside $[H-F,H-L]$ and halts.

## How many left coordinates can remain inconclusive?

The enlarged rectangle already settles $r\le57$. The remaining
high-pair cuts have only the following types. The count fixes the first
letter to $P$; when $m=r+1$, the last letter is also $P$ because that pair
straddles the cut.

| $r$ | $m$ | $p$ | Number of prefix cylinders | Maximum even $h$ values per cylinder |
|---:|---:|---:|---:|---:|
| 58 | 58 | 29 | 1 | 10,323,973,708 |
| 58 | 59 | 29 | 28 | 3,441,324,570 |
| 59 | 59 | 29 | 29 | 10,323,973,708 |
| 59 | 60 | 29 | 406 | 3,441,324,570 |
| 59 | 60 | 30 | 1 | 13,765,298,277 |

The two prefix counts for a fixed $(r,p)$ are
$\binom{r-p-1}{p-1}$ and $\binom{r-p-1}{p-2}$, with an out-of-range
binomial coefficient interpreted as zero. They sum to **465 cylinders**.
No angular enumeration of these cylinders is needed for the predicate.

For one prefix, allowing every $0\le x_{\rm tail}\le1$ confines $h$ to
an interval of span $4^p/(D3^{m-r})$. It therefore contains at most

$$
\left\lfloor\frac{4^p}{2D3^{m-r}}\right\rfloor+1
$$

even integers. Summing the table gives the upper bound
1,817,019,372,897. This deliberately counts some directions that the
predicate already accepts at the cut. It also ignores clipping to the
outermost left-coordinate bound, so both relaxations preserve the upper
bound. The inconclusive fraction is less than $3.591\times10^{-9}$ of
this specified population.

## Verification and scope

```sh
python3 filtered_entry_758.py
```

The checker verifies the new launch, physical-shadow, long-tail, counting
and mass inequalities. It also checks 40 selected left coordinates at
range endpoints and at the edges and interiors of representative cylinders
of all five high-pair types. These produce 75 accepted physical replays
at three masses and 15 inconclusive physical replays. All selected
inconclusive examples also return, illustrating why rejection is only a
limit of this sufficient test.

The universal result reuses the archived exhaustive survey through
$p=28$ and the enlarged rectangle's $r=57$ lattice certificate. The
script invokes the latter certificate's arithmetic/receipt checker; it
does not rerun those exhaustive searches. Their full-replay commands are
documented in the linked proofs. Neither the population count nor the
sample replays establish that the blank machine reaches an accepted state.
