# A threefold enlargement of the ordinary-state halting criterion

Put $D=13,959,275$, $H=(3^{307}-8,282,708,212)/D$,
$F=53,463,914,736,831,321,850$ and $L=3,403,055$.
Every odd/odd state with

$$
h=(a+1)/2\text{ even},\quad
2\le h\le112,473,097,570,044,405,002,
$$
$$
H-F\le u=(a+2c-1)/2\le H-L-2488
$$

reaches a reset inside the established halting basin within **553 counter
calls**, and therefore halts. The upper bound on $h$ is the largest even
integer below $3^{57}/D$. It is three times the previous bound plus two.
The rectangle contains exactly
**1,503,313,024,667,945,292,112,573,711,164,328,143,154** ordinary states.
This does not prove that the blank trajectory visits the rectangle.

## All but one prefix are already covered

The bound on $h$ guarantees 250 initial jumps:
$3^{250}h\le H-F$. Let $k$ be the maximal initial jump count, so
$250\le k\le292$, and write $r=307-k\le57$.
At alignment the ideal direction is $x=Dh/3^r$, with even numerator
before multiplication by the odd $D$. The physical-shadow proof in
[the earlier criterion](NONRESET_ENTRY_758.md) applies through aligned
depth 248, because

$$
3^{307-248-2}>D(F+2600).
$$

The even-coordinate/odd-guard parity obstruction excludes exact contacts.
This comparison covers the jump, pair, ordinary return, exceptional and
terminal decisions. The maximal launch leaves $x>1/3$; survival therefore
starts with a pair $P$.

At the first complete boundary $m\ge r$, one has $m=r$ or $r+1\le58$.
If its pair count is at most 28, the established dyadic exhaustion applies.
Every unlisted tail returns by depth $m+188\le246$. For the 972 listed
longer tails the minimum pulled-back physical clearance at $m\le58$ is
greater than $5.8\times10^{64}$, and in particular greater than $F+2600$.
These paths therefore return as before.

A cut with 29 pairs is possible only when $r=57$, $m=58$, with the sole
prefix **$P^{29}$**. Thus the extension requires one new lattice calculation,
without any assumed reset-header ancestry.

## Exhausting the missing cylinder

The inverse pair is $f_P(x)=(4x+5)/9$. Its 29-fold iterate gives

$$
x_{\rm initial}=\frac{A+4^{29}x_{\rm tail}}{3^{58}},
\qquad A=3^{58}-4^{29}.
$$

Consequently the cut direction is $N/4^{29}$, where

$$
0<N<4^{29},\qquad N+A=3Dh,
\qquad N\equiv-A\pmod{6D}.
$$

There are exactly **3,441,324,569** admissible numerators. They are odd
multiples of five, since $A$ is odd and divisible by five. The new checker
exhausts this arithmetic progression. Its output is

| $r$ | $p$ | Last guard | Cylinders | Probes | Angular tests | GMP fallbacks | Survivors |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 57 | 29 | 248 | 1 | 103,848,245 | 103,822,208 | 42,425 | 0 |

As in [the existing high-pair checker](HIGH_PAIR_HEADERS_758.md), an outward
cover of surviving angular cylinders on a $2^{22}$ grid skips intervals
that have already returned. Within the retained bins the new cursor takes
the first admissible numerator at or above each bin boundary, by exact
remainder arithmetic modulo $6D$. Thus each skip omits only empty bins or
directions already proved to return. The retained directions are propagated
using outward $2^{-60}$ rounding; ambiguous comparisons are replayed exactly
with GMP. All enter the ordinary-return interval by aligned depth 248.

The implementation reuses the archived angular-cover, rounded propagation
and exact propagation primitives. Only the admissible numerator lattice and
its enumeration are new. A separate small-grid check compares the accelerated
cursor with direct enumeration and exact rational trajectories on nine
progressions at denominator exponents 12, 13 and 14.

## Integer bounds and physical return

At $p=29$, every numerator and denominator at the cut is below $2^{58}$.
The progression step is $6D=83,755,650$, so its cursor and the next-bin
rounding fit in unsigned 64-bit integers. Working-grid numerators are at
most $2^{60}$; the factors three and nine used in the interval comparisons
and updates remain below $2^{64}$. Prefix constants and the array of powers
through $3^{79}$ fit in unsigned 128-bit integers. Exact fallback arithmetic
has arbitrary precision. These are the arithmetic ranges used by the
verified $r=57$ run.

For the newly covered cylinder $k=250$, so a return decision by aligned
depth 248 followed by one bulk and a reset takes at most 500 calls from the
original state. The existing lower-pair tails retain the uniform bound
$k+m+243+2\le307+1+243+2=553$. Mass strictly increases by at most nine per
call. Therefore the returned seed $s$ satisfies
$u<s\le u+2488$, placing it inside $[H-F,H-L]$.

The enlarged bound also replaces the even primitive-coordinate threshold
in the inverse-jump criterion. If $h=3^j h_0$ with even
$h_0\le112,473,097,570,044,405,002$, the same argument applies after at most
292 inverse jumps, with the established lower trim of 584 in $u$.

## Reproduction

Run in this directory:

```sh
c++ -O3 -std=c++17 target_bridge_even_lattice_758.cpp -lgmpxx -lgmp -o even_lattice
./even_lattice --self-test
python3 target_bridge_even_758.py --worker ./even_lattice
```

The final command replays the complete new lattice calculation, compares
its output byte-for-byte with the archived receipt, and checks the physical
inequalities and earlier long-tail clearances. Without `--worker` it checks
the arithmetic and receipt, using the archived exhaustive result.
