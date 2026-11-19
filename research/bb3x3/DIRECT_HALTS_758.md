# Direct halts after the initial power of three

The 546 power-gate checkpoints each reach 8,192 further resets. The
4,472,832 checked excursions include no halt. Each ends at a reset, so
a certificate that commits the machine to a reset-free infinite trajectory
cannot begin in one of these excursions. This finite check leaves the
later futures open.

A separate search exhausts the direct terminal word consisting of the
maximal initial J run, one block of ordinary bulk updates, and an immediate
halt. It includes the initial even-seed instruction when applicable. Write
$p=b3^m$ for $20\le m\le292$, with $b=1$ for odd initial seeds and
$b=2$ for even ones. At the end of the maximal J run the state has
$a_0=2p-1$ and $c_0=s+2m+4[b=2]-p+1$, odd and in $[1,2p-2]$.

| Number of bulk updates | Halting sibling pairs |
|---:|---:|
| 1 | 69 |
| 5 | 46 |
| 7 | 11 |
| 9 | 8 |
| 11 | 1 |
| 13 | 1 |

These are all 136 pairs. No other bulk-run length occurs. For each pair
$q,q+2$, every reset in $[q-100000,q-67490]$ passes both targets alive. Among the 100,003 tested seeds
from $q-100000$ through $q+2$, the longest contiguous run which halts
before passing the targets is 53. It occurs for $b=2,m=52$, with 13 bulks.
These results give no unavoidable intermediate target.

## A family at every fourth power

The one-bulk case also has an all-exponents solution. Put $c_0=4i\pm1$.
The first bulk gives $(a_1,c_1)=(2p-4i-4,6i+5)$. Gap one would require
$p=5i+5$, impossible for $p=b3^m$. Gap three requires $p=5i+6$ and odd
$i$, equivalently $p\equiv1\pmod{10}$. Thus $b=1$ and $m$ is a multiple
of four. For every positive multiple of four, $i=(3^m-6)/5$ gives the
two halting odd resets $s=3^m+4i-2m-1\pm1$.

## Exhaustion

Let $x_0=x=\lfloor(c_0+1)/4\rfloor+3$ and
$x_{i+1}=\lfloor3x_i/2\rfloor$. After $n\ge1$ ordinary bulks the cost
to the left coordinate is $S=8(x_n-x)-9n+4o$, where $o$ counts odd
$x_0,\ldots,x_{n-1}$. The right coordinate equals $c_n=6x_{n-1}-13$.
These are the [small-right strip](check_small_right_758.py) identities.
The left parity flips at every bulk. The first subsequent instruction
halts exactly when $n$ is odd and $h=a_0-S-c_n$ is either 1 or is 3
with $c_n\equiv3\pmod4$. The computed final left counter is then
positive. Since all the decrements are positive, enough left counter
was available for every preceding bulk. Both initial right counters
$4(x-3)\pm1$ are tested inside the maximal-run range.

With $R=(3/2)^n$, iterating the rounded update gives
$(x-1)R+1\le x_n\le xR$. Also
$4x_n-13\le c_n\le4x_n-11$. Substituting in
$a_0=S+c_n+h$, using $0\le o\le n$ and $1\le h\le3$, yields

$$
\frac{a_0}{12R-8}\ \le x\le\frac{a_0+12R+9n}{12R-8}.
$$

The interval has width below three because $24R>9n+24$ at $n=1$
and the difference grows thereafter. At most three integer candidates
need an exact calculation per length. When the upper bound falls below
three, $24R>a_0+9n+24$ and this strict inequality persists at larger
$n$. No subsequent length can yield a legal $x$.

For the local census, process seeds from largest to smallest, marking
each if it halts immediately or returns within the range to an already
marked seed. All surviving first returns increase the seed, making this
a finite exact classification. The largest distance of any marked seed
below a target is 67,489.

Place direct_halts_758.py beside the counter verifier and run it with
Python 3.10 or later. The default reconstructs all pairs and verifies
them with unbatched transitions. The optional --census and --futures
switches replay the two finite searches using the published first-return
function. Those reference replays are considerably slower than the
batched GMP computation used for the totals.
