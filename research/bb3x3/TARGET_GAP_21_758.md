# The contiguous halting basin through scale 21

The scale-21 extension is certified by
[`target_gap_21_758.py`](target_gap_21_758.py), together with the complete
chunk receipts
[`target_gap_atlas_p29_758.tsv`](target_gap_atlas_p29_758.tsv) and
[`target_gap_atlas_p30_758.tsv`](target_gap_atlas_p30_758.tsv).
For

\[
H=\frac{3^{307}-8,282,708,212}{13,959,275},
\]

every reset configuration \(A(1,s)\) satisfying

\[
3,403,055\le H-s\le160,391,744,210,493,965,542
\]

halts. Both parities are included. This approximately triples the previous
basin width; the far endpoint satisfies the exact relation
\(F_{21}=3F_{20}-8\). It does not establish that the blank trajectory enters
the basin.

There are now **160,391,744,210,490,562,488 consecutive halting reset
seeds**, including **106,927,829,473,662,643,692 newly covered seeds**.
At the first crossing \(W>2(H-3,403,055)+1\), a preceding reset within
**35,642,609,824,553,458,330 counter calls** suffices to settle blank.
Indeed, escaping the basin would require that reset seed to be at most
\(H-F_{21}-1\), forcing a mass increase of at least
\(2(F_{21}-3,403,055)+3\), greater than nine times this call bound.
The previous sufficient recent-reset bound was
11,880,869,941,517,315,288 calls. Establishing the new reset recency on
the actual blank trajectory remains an open obligation.

## What the new computation covers

Write \(D=13,959,275\), and let \(d=H-s\). The previous contiguous basin
ends at

\[
F_{20}=53,463,914,736,831,321,850.
\]

The next fixed-word odd-reset corridor has exact even endpoints

\[
N_{21}=96,235,046,526,296,379,328,
\qquad
F_{21}=160,391,744,210,493,965,542.
\]

The two formulas are \(N_{21}=3N_{20}+4\) and
\(F_{21}=3F_{20}-8\). The checker verifies both physical endpoint words
and their failure at the adjacent even distances. The corridor word is
\(J^{292}L^8JL^6J^{243}LR\). The fixed even-reset word is valid throughout
the enlargement, as checked at its two ordered endpoints.

For the intervening odd-reset gap
\(F_{20}+2\le d\le N_{21}-2\), the common prefix
\(J^{292}L^8JL^6\) is legal. Its maximal subsequent jump launch has length
244 everywhere in the gap. Thus the aligned denominator exponent is
\(r=307-244=63\).

At the first complete grouped boundary \(m\ge63\), one has \(m=63\) or
64. If \(p\) pairs have occurred, the dyadic direction is
\(N/4^p\), with \(0<N<4^p\), \(N\equiv5\pmod {10}\). As before, every
surviving prefix begins with \(P\). The prefix cylinder is

\[
\frac{A+4^p x}{3^m},\qquad 0<x<1,
\]

and the physical header equation is

\[
N+A=tDh_0,\qquad t=3^{m-63}\in\{1,3\}.
\]

Here \(h_0\) is the left coordinate immediately after the common physical
prefix. Its exact period relation is

\[
h_0(d+32768)=h_0(d)+2D.
\]

The even countdown classes give exactly 8,192 distinct even residues
\(R\subset\mathbb Z/(2D)\mathbb Z\). Both the C++ worker and the Python
checker construct these residues from the physical counter formulas.
Consequently every possible cut numerator lies in

\[
N+A\equiv tD R\pmod {2tD^2}.
\]

The computation includes this whole residue superset; it does not assume
that each enumerated direction is attained by a reset in the gap.

The inherited exhaustive dyadic result covers \(p\le28\). The archived
high-pair receipt already covers the 496 prefixes with \(p=31\) and the
single prefix with \(p=32\), through guard depth 248. The new worker
completes the remaining cases:

| Pair count | Complete prefix cylinders | Atlas points | Guard-248 exceptions |
|---:|---:|---:|---:|
| 29 | 1,344,904 | 180,089,868,609 | 1 |
| 30 | 40,920 | 12,175,754,416 | 1 |

These counts follow independently from

\[
\binom{r-p-1}{p-1}+\binom{r-p-1}{p-2}.
\]

The first term has \(m=r\). The second has \(m=r+1\), where both the
first and final pair are fixed. The chunk checker requires every index
from zero to the relevant count exactly once, with no missing or
overlapping interval. It requires the exact identities of both flagged
directions and proves their returns separately, as described below.

## Exact sparse enumeration

[`target_gap_atlas_758.cpp`](target_gap_atlas_758.cpp) reuses the inverse
cylinders and exact image arithmetic from
[`wider_even_lattice_758.cpp`](wider_even_lattice_758.cpp). For each prefix
header it merges two ordered sets: the supported numerator residues and
the disjoint integer intervals of a shared angular atlas. A bucket
directory only speeds up the search for the next atlas interval; every
candidate is tested against its exact integer endpoints.

For a header residue \(a=A\bmod M\), with
\(M=2tD^2\) and \(q=tD\), the successor of a requested numerator \(L\)
is computed by writing \(L+a=bM+z\) and choosing the first residue
\(R_i\ge\lceil z/q\rceil\). If there is none, the residue index wraps
and \(b\) increases by one. The resulting numerator is
\(bM+qR_i-a\). Advancing within an interval merely moves to the next
residue. This enumerates every supported integer in that interval and
never moves backwards.

For an atlas word with \(j\) pairs and elementary depth \(l\), its
inverse cylinder is

\[
\left[\frac{B}{3^l},\frac{B+4^j}{3^l}\right].
\]

For the incoming denominator \(Q=4^p\), the exact eligible numerator
interval is

\[
\left\lfloor\frac{BQ}{3^l}\right\rfloor+1
\ \le N\le\
\left\lfloor\frac{(B+4^j)Q-1}{3^l}\right\rfloor.
\]

At an enumerated integer the post-atlas direction is exactly

\[
\frac{3^lN-BQ}{4^{p+j}}.
\]

Numbers outside all atlas intervals have already returned. The two
receipts use 12 grouped atlas letters for \(p=29\), and 14 for \(p=30\).
The strict endpoints cannot discard an eligible direction: every
internal atlas endpoint has a nontrivial power of three as its reduced
denominator, whereas the incoming direction is dyadic. The only
integer endpoints are zero and one, both excluded by \(0<N<4^p\).

### The additional finite angular filter

A small bitset avoids replaying the same short tails billions of times.
Starting with \([0,1]\), the worker recursively applies the inverse maps

\[
f_J(x)=x/3,\qquad f_P(x)=(4x+5)/9.
\]

It stops each branch once the exact cylinder intersects at most two
adjacent cells of the \(2^{-20}\) grid, and marks both cells, including
endpoints. The maximum elementary depth of any stopped branch is 36.
Thus every direction that survives 36 elementary decisions belongs to a
marked cell. An exact post-atlas direction in an unmarked cell is known
to have returned within that finite depth. This conclusion uses a finite
tree, and makes no assumption about infinite rational trajectories.

The code asserts that cut depth plus the largest atlas depth plus 36 is
within the requested guard budget. For a marked image, outward rational
interval arithmetic proceeds on a \(2^{-60}\) working grid. An ambiguous
guard or an exhausted interval budget causes exact GMP replay from the
original numerator. Every failure to return by the budget is printed and
counted. Each of the two full scans found one such direction; both are
resolved by exact longer replay and physical guard clearance.

All prefix, atlas and filter arithmetic fits in unsigned 128-bit
integers. Here \(r\le63\), so header constants are below \(3^{64}\).
The generic atlas bounds are \(p\le30\), at most 21 grouped letters,
and elementary depth at most 42; hence its largest relevant product is
below \(3^{42}2^{60}<2^{128}\). Its image denominator uses at most 102
bits. The residue cursor uses 64-bit integers: \(Q\le2^{60}\),
\(M\le6D^2\), and each intermediate cursor value is below \(Q+2M\).
The finite filter has elementary depth 36 and no more than 18 pairs, so
its powers and endpoint products are smaller still. The inherited
working-grid operations are bounded by \(9\cdot2^{60}<2^{64}\); longer
exact trajectories use GMP.

## The two flagged tails

The first direction has

\[
(r,m,p,N,A)=
(63,63,29,188136122924663855,1144541009596807477707782023595).
\]

It returns after 186 further elementary calls, at aligned depth 249.
The floor of its minimum guard clearance, pulled back through the
header, is

\[
962,784,278,959,391,660,117,995,150,222,859,267,856,847,373,207,217,987,776,355,610,388,319,041,489.
\]

The second direction has

\[
(r,m,p,N,A)=
(63,64,30,777865017584130175,3343848190836621005949279610625).
\]

It returns after 195 further elementary calls, at aligned depth 259.
Its minimum guard-clearance floor is

\[
11,292,473,431,637,801,390,039,388,297,349,820,517,250,589,757,212,092,534,102,149,802,929,981,073,132.
\]

Both values exceed \(N_{21}+2000\). The checker independently decodes
each claimed header from \(A\), replays the exact rational tail,
minimizes over all four guards at every group start including the final
return, and requires these exact lengths and clearance floors. It also
recovers every physical origin using all 16,384 even residue
representatives of the affine prefix. There are precisely two origins
for each direction:

| Pair count | Reset countdown \(d=H-s\) | Counter calls to reset | Seed gain |
|---:|---:|---:|---:|
| 29 | 96,233,342,737,222,047,692 | 802 | 1,899 |
| 29 | 96,233,342,737,222,047,694 | 802 | 1,901 |
| 30 | 93,717,244,529,141,180,700 | 812 | 1,938 |
| 30 | 93,717,244,529,141,180,702 | 812 | 1,940 |

All four origins lie inside the new gap. Literal iteration of the
original `champion_step` counter map checks these complete excursions
independently of the angular shortcut. The raw survivor lines remain in
the archived tables. The certificate accepts neither an unidentified
flag nor a different count.

## Transfer to physical counter trajectories

The largest gap countdown is \(N_{21}-2\), whose uniform physical shadow
extends through depth 248. The unlisted \(p\le28\) tails return at most
188 elementary calls after the cut, so they need shadow only through
\(64+188=252\). Exact reverse ancestry gives:

| Depth | Integer guard candidates | Candidates with a cut ancestor |
|---:|---:|---:|
| 249 | 0 | 0 |
| 250 | 103 | 0 |
| 251 | 165 | 0 |
| 252 | 583 | 0 |

The 972 archived longer dyadic tails are checked by their exact minimum
guard clearance. At the new worst cut, \(m=64\), the floor of that
clearance is

\[
79,762,309,749,986,306,880,633,296,187,060,457,963,034,068,453,186,124,314,406,566,
\]

which is larger than \(N_{21}+2000\). They therefore follow the
physical ordinary branches through their returns, including every
intermediate bulk and the final reset. Except for the two individually
verified directions, the new high-pair results finish within the
original uniform shadow depth 248.

The common prefix uses 307 counter calls and the launch uses 244. Even
the longest listed tail finishes within

\[
307+244+64+243+2=860
\]

calls from its reset. Each continuing call adds at most nine to
\(W=a+2c\). Between resets the mass difference is twice the seed
increment, so every new gap return increases the reset seed by a
positive amount smaller than 4,000. The fixed-word corridors also obey
that bound. Every starting countdown in the enlargement is more than
4,000 beyond the old near endpoint. Strong induction on countdown
therefore joins all new resets to the inherited basin.

## Verification and replay

The lightweight checker validates the prior scale-20 dependency, all new
chunk ranges, the two inherited high-pair rows, physical endpoints,
periodic residues, reverse guard counts, long-tail margin and induction
bound:

```sh
python3 target_gap_21_758.py
```

To rebuild and replay the new finite exhaustion:

```sh
c++ -O3 -std=c++17 -fopenmp target_gap_atlas_758.cpp -lgmpxx -lgmp -o /tmp/gap_atlas758
/tmp/gap_atlas758 --self-test
python3 target_gap_21_758.py --worker /tmp/gap_atlas758 --threads 7
```

Each raw worker run intentionally exits with status 1 because it reports
one direction beyond its guard-248 budget. The Python replay requires
that status, checks the full chunk data and exact flagged identity, then
verifies the longer angular and physical excursion. An unexpected
process status or any additional flag fails verification.

The self-test independently enumerates 1,803 header-supported directions
on smaller denominators, including 47 that survive a deliberately short
budget. It also compares 3,072 cursor queries against a separate full
residue scan and checks 4,998 filtered small-grid directions by direct
rational iteration. The full worker emits and flushes one receipt per
4,096-header chunk; its optional `first stop` arguments permit a missing
chunk to be rerun without discarding completed work. A benchmark sample
is explicitly labeled as such and is never accepted as a certificate.
