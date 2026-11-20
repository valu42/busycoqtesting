# Completing the wider even-coordinate halting rectangle

Every odd/odd counter state satisfying

$$
2\le h=(a+1)/2\le3,036,773,634,391,198,935,066,
\qquad h\text{ even},
$$
$$
H-F\le u=(a+2c-1)/2\le H-L-2488
$$

reaches a reset inside the established halting basin within **553 counter
calls**. Here $D=13,959,275$, $H=(3^{307}-8,282,708,212)/D$,
$F=53,463,914,736,831,321,850$ and $L=3,403,055$.
The upper left-coordinate bound is 81 times the original even-coordinate
bound, plus 66. This settles **all 465 prefix cylinders** left inconclusive
by the [filtered membership criterion](FILTERED_ENTRY_758.md), and the
next exponent's additional **4,525 cylinders**.
Membership in this larger rectangle now requires only its integer bounds
and parity conditions.

For odd/odd states $u$ is even. The rectangle contains exactly
**40,589,451,666,034,522,887,199,881,945,647,343,614,082** counter states.
Its entry from the actual blank trajectory remains unproved.

## Reduction to the missing angular directions

The launch and physical-shadow argument in the filtered criterion is
unchanged. The maximal initial jump count is $247\le k\le292$.
Set $r=307-k\le60$, and initialize the rational direction
$x=Dh/3^r$. The last launch jump and the first illegal jump imply
$1/3<x<1$, so a surviving prefix starts with $P$.

At the first complete boundary $m\ge r$, $m\in\{r,r+1\}$ and

$$
x_{\rm initial}=\frac{A+4^p x_{\rm tail}}{3^m},
\qquad N+A=3^{m-r}Dh,
\qquad x_{\rm tail}=N/4^p.
$$

The numerator $N$ is an odd positive multiple of five. All cut directions
with $r\le57$ are already covered by the
[complete threefold rectangle](TARGET_BRIDGE_EVEN_758.md), including its
single $r=57,p=29$ cylinder. The new verifier invokes that theorem's
arithmetic and receipt checker explicitly.
At the remaining exponents, cut directions with $p\le28$ are settled by
the dyadic survey and its individual long-tail guard margins.
The new computation treats every remaining
direction for $r=58,59,60$, with **no restriction on the ancestry of $h$**.

For each prefix its complete admissible set is

$$
0<N<4^p,\qquad N\equiv-A\pmod{2\cdot3^{m-r}D}.
$$

The exhaustive results use the indicated last angular guard:

| $r$ | $p$ | Last guard | Prefix cylinders | Admissible directions | Atlas image tests | Exact fallbacks | Survivors |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 58 | 29 | 248 | 29 | 106,681,061,641 | 544,570,092 | 15,026 | 0 |
| 59 | 29 | 248 | 435 | 1,696,573,012,589 | 8,660,417,440 | 239,568 | 0 |
| 59 | 30 | 248 | 1 | 13,765,298,277 | 70,266,916 | 2,000 | 0 |
| 60 | 29 | 249 | 4,495 | 18,462,706,313,573 | 94,245,716,148 | 2,603,736 | 1 |
| 60 | 30 | 249 | 30 | 440,489,544,851 | 2,248,547,630 | 62,404 | 0 |

The enumeration covers complete arithmetic progressions containing
**20,720,215,230,931** directions. One direction survives its angular
budget. The separate exact guard calculation below proves its later
physical return; every other direction returns by its stated guard.

## The single longer direction

The sole budget survivor has

$$
r=60,\quad m=61,\quad p=29,\quad
N=247,582,280,329,091,635,
$$
$$
A=110,426,321,454,572,863,635,202,307,315.
$$

The independent prefix census verifies that this is an actual cut
cylinder, and its unique even left coordinate is

$$
h=(A+N)/(3D)=2,636,868,592,263,816,134,566.
$$

Starting with the exact direction $N/4^{29}$, the tail enters the return
interval after 198 elementary calls, at aligned depth 259. At every tail
guard, write its current direction as $a/b$ without cancelling the
power-of-four denominator, and let $3^j$ record the number of elementary
calls. Define

$$
g=\min\{9a,\,3|3a-b|,\,|9a-5b|,\,9(b-a)\}.
$$

Pulling the guard back through the tail and its cut prefix gives aligned
clearance

$$
\frac{3^{307}}{D3^{61}}\min_{\rm guards}\frac{g}{9\cdot3^j}
>6\times10^{79}>F+2600.
$$

The same bounded physical-shadow correction therefore applies through
this entire longer tail, at **every** mass in the stated band. Its
physical return takes $247+61+198+2=508$ calls. Independent literal
counter replays at both extreme admissible masses also return in 508
calls. They check the implementation; the uniform clearance inequality
proves all intervening masses.

The [raw exponent-60 receipt](wider_even_r60_758.txt) preserves the
survivor's exact numerator and prefix constant. The worker reports exit
code one for this angular-budget survivor. The complete Python verifier
expects that status and resolves the survivor with the displayed exact
guard proof.

## Sharing the angular prefix calculation

The former lattice checker restarted an angular simulation at each
retained numerator. The new [integer checker](wider_even_lattice_758.cpp)
builds one shared atlas of all $2^{21}$ words of 21 grouped letters
$J,P$. For a word with elementary length $l$ and $q$ pairs, its inverse
cylinder is

$$
I_w=[B,B+4^q]/3^l.
$$

These cylinders have disjoint interiors and contain every direction
surviving the first 21 groups. A direction outside their union has
already reached the ordinary-return interval. No eligible dyadic can
equal an internal inverse guard, since the guard has a nonzero odd
numerator over a power of three and the dyadic numerator is odd.

For the cut denominator $Q=4^p$, precompute each cylinder's complete
integer interval

$$
\ell=\lfloor BQ/3^l\rfloor+1,
\qquad
v=\lfloor((B+4^q)Q-1)/3^l\rfloor.
$$

Only numerators from the header's progression lying in $[\ell,v]$ need
further work. For each such numerator its exact image after the atlas
word is

$$
\frac{3^l N-BQ}{4^q Q}.
$$

The numerator at $\ell$ and its increment along the arithmetic progression
are precomputed or updated by integer addition. Thus the checker advances
directly past 21–42 known elementary instructions without executing them
again for each candidate. This is an exact affine evaluation of a proved
prefix, not an approximate simulation skip.

Round the exact image outwards to the $2^{-60}$ grid. Propagate both bounds
with the angular rules until a return interval is certified. Any ambiguous
comparison, including survival to the specified budget, triggers a fresh
GMP replay of the original $N/4^p$ from the cut. Every comparison is thus
covered either by exact integers or by an interval containing the exact
direction.

## Completeness and arithmetic bounds

At a fixed $(r,p)$ the first prefix letter is $P$. A cut at $m=r+1$ also
has last letter $P$, because that final pair straddles $r$. The two counts
are

$$
\binom{r-p-1}{p-1},\qquad\binom{r-p-1}{p-2}.
$$

The C++ worker traverses the corresponding binary tree. The Python checker
independently generates each prefix by choosing its pair positions, and
recomputes every progression's exact size. This checks both the cylinder
count and the population totals in the receipt.

For $p\le30$ and 21 grouped atlas letters, $l\le42$ and
$3^lQ\le3^{42}2^{60}<2^{128}$. All cylinder endpoint products therefore
fit in unsigned 128-bit integers. The exact image denominator is a power
of two of exponent at most 102; conversion to a 60-bit interval uses
shifts and outward integer rounding. The interval updates and comparisons
use at most nine times $2^{60}$, below $2^{64}$. The progression step is
at most $6D=83,755,650$. Its numerator cursor and subsequent increment
also fit in 64 bits. Every exact fallback uses arbitrary precision.

The finite verification includes **137,626 independently iterated rational
directions** at smaller denominators. Of those, 956 survive a deliberately
shortened budget; the atlas checker agrees with direct iteration on both
the returning and surviving directions. The new engine also reproduces
the established zero-survivor $r=57,p=29$ result independently of the old
outward-bin traversal.

## Returning inside the physical halting basin

The physical guard comparison is uniform through aligned depth 248,
because $3^{57}>D(F+2600)$. There is one additional guard available after
the dyadic cut: its numerator remains a multiple of five under both
angular updates. At depth 249 the pulled-back candidate error is less
than one for guards $0,1/3,1$. For the guard $5/9$ it is less than three,
whereas $9N-5\cdot4^p$ is a nonzero multiple of five. None of these guards
can be ambiguous. Thus the depth-249 decisions in the new rows are
physical as well. Every zero-survivor row gives a real ordinary return;
the single longer case has its own larger clearance above.

The lower-pair paths retain the bound
$k+m+243+2\le307+1+243+2=553$. Their unlisted short tails return by
$m+188\le249$, and the archived long-tail clearance at
$m\le61$ exceeds $2.15\times10^{63}$, much larger than $F+2600$.
Mass increases by at most nine per call, so the first returned reset seed
satisfies $u<s\le u+2488$. It lies in $[H-F,H-L]$ and halts.

The larger coordinate bound also applies to the inverse-jump criterion:
replace $h$ by its primitive part after removing powers of three, and
retain the lower mass trim of 584 for at most 292 inverse jumps.

## Reproduction

```sh
c++ -O3 -std=c++17 -fopenmp wider_even_lattice_758.cpp -lgmpxx -lgmp -o wider_even
./wider_even --self-test
python3 wider_even_entry_758.py --worker ./wider_even
```

The last command replays the new arithmetic exhaustion and compares the
results byte-for-byte with the [exponent-58/59 receipt](wider_even_lattice_758.tsv)
and [exponent-60 receipt](wider_even_r60_758.txt), then checks the physical,
population, unique exception and inherited long-tail inequalities.
It uses at most three worker threads. Omitting `--worker` checks the same
arithmetic and receipt using the archived exhaustive result.
