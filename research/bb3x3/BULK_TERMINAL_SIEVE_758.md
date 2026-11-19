# How soon can an excursion at a power gate halt?

Let $P=3^m$ with $m\ge20$. On either [power gate](POWER_BOUNDARY_758.md), after its launch and its first maximal string of ordinary bulk calls, let $\ell$ count subsequent ordinary jumps and bulks before the first exceptional call or halt. The count stops if a reset intervenes. Every such exceptional call or halt satisfies

$$
\ell\ \ge\ m-1-\left\lfloor\log_{3/2}(5m+11)\right\rfloor .
$$

A reset may occur immediately. The theorem restricts the first excursion before that reset. At $m=292$, all 520 gate departures reset and the longest observed suffix has 34 ordinary calls. The theorem would require at least 274 such calls to encounter an exception or halt. It also gives a 125-call bound for every odd reset between $3^{292}$ and $3^{292}+10^{30}$, inclusive, after its initial jumps and maximal bulk string.

## The inverse calculation

Throughout the odd-right part of an excursion put $W=a+2c$. A jump takes $(W,c)$ to $(W+4,3c-W+1)$. A bulk takes it to $(W+g,(3c+\eta)/2)$, with $(g,\eta)=(5,7)$ at $c\equiv1\pmod4$ and $(9,13)$ otherwise. These are the [literal counter rules](check_bb33.py).

At a halt or the exceptional branch the gap $h=a-c$ belongs to $\{1,2,3\}$, so $c=W/3-h/3$. Pull an equation $c'=\alpha'W'+e'$ back through one ordinary call by writing $c=\alpha W+e$.

| Call | $\alpha$ | $e$ |
| --- | --- | --- |
| Jump | $(\alpha'+1)/3$ | $(4\alpha'+e'-1)/3$ |
| Bulk | $2\alpha'/3$ | $(2g\alpha'+2e'-\eta)/3$ |

Both inverse rules preserve $0\le\alpha\le1/2$ and $-13\le e\le2$, as is seen at the four corners of the rectangle. Starting from the terminal coefficients $1/3,-h/3$ and reversing $\ell$ calls therefore gives $\alpha=r/3^{\ell+1}$ for an integer $r$, with the same uniform error bound.

For an actual gate departure the launch is $a_0=BP-1$ with $B=2$ or $4$ and an odd $1\le c_0\le4m+31$. Let $n$ count the initial maximal bulk string, for which $2m\le n<3m$ by the [power-boundary theorem](POWER_BOUNDARY_758.md). Write $W_n=BP+\Delta$. The bulk gains give
$$
10m+1\le\Delta=2c_0-1+\sum_{i<n}g_i\le35m+61.
$$
The next bulk guard fails. Since its guard is $a\ge c+2$ or $a\ge c+4$, this gives $a_n-c_n\le3$, hence $c_n\ge(W_n-3)/3$. The inverse formula $c_n=\alpha W_n+e$ now implies $\alpha\ge1/4$, using $e\le2$ and $W_n\ge36$.

Define $x_i=\lfloor(c_i+1)/4\rfloor+3$. In the first bulk string,
$$
x_{i+1}=\lfloor3x_i/2\rfloor,\qquad
c_i=4x_i-\kappa_i,\qquad \kappa_i\in\{11,13\}.
$$
Thus $x_n=\alpha B3^m/4+\delta$, with
$$
\delta=(\alpha\Delta+e+\kappa_n)/4,\qquad
(10m+1)/16-1/2\le\delta<5m+12.
$$
In particular $\delta>3$. Put $K=m-\ell-1$. If $K\le0$ we already have the result. Otherwise $1\le K\le n$, and put $C_j=(2/3)^j Br3^K/4$. The values $C_j$ are integers for $1\le j\le K$, since $B$ is even. Define $d_j=x_{n-j}-C_j$, so $d_0=\delta$. Inverting the floor gives
$$
d_{j+1}=(2d_j+\epsilon_j)/3,\qquad
\epsilon_j=x_{n-j-1}\bmod 2.
$$
The positive integer $d_1$ is at least two. If $d_j\ge2$ and $j+1\le K$, then $d_{j+1}\ge4/3$ and is integral, so $d_{j+1}\ge2$. But $d_{j+1}-1\le(2/3)(d_j-1)$, which gives $1\le d_K-1\le(2/3)^K(\delta-1)$. Consequently $(3/2)^K<5m+11$, as required.

## How far the counters stay from the branch boundary

The same argument bounds the gap at every early state, including ordinary jump and return inputs. Put $b=3/2$. Suppose $\ell$ ordinary calls after the maximal bulk string comprise $j$ jumps and $q$ bulks, so $\ell=j+q$. Whenever $b^{m-\ell-1}\ge2(5m+12)$, the gap $h=a-c$ lies outside the interval
$$
-2^j b^{m-1}< h \ \le\ m\,3^\ell/2^q .
$$
For $m=292$ this covers every suffix length through 271 calls. A right-dominant state in that range has $c-a\ge(3/2)^{291}>1.74\times10^{51}$.

Indeed start the inverse calculation at $c=W/3-h/3$, now with unrestricted $h$. By its exact linear action on the error term, at the beginning of the suffix $c_n=\alpha W_n+e_0-\rho h/3$, where $-13\le e_0\le2$ comes from starting the same inverse word at error zero, and $\rho=2^q/3^\ell$. Suppose $h$ is in the forbidden interval. Then $-b^{m-\ell-1}<\rho h\le m$. The bulk end guard implies $\alpha\ge1/4$, since
$$
\alpha W_n\ge W_n/3-3-b^{m-\ell-1}/3\ge W_n/4 .
$$
The last inequality follows from $W_n\ge2\cdot3^m$, $m\ge20$. The exact offset is $\delta=(\alpha\Delta+e_0+\kappa_n)/4-\rho h/12$. The inequalities above give
$$
(10m+1)/16-1/2-m/12\ \le\ \delta\ <\ 5m+12+b^{m-\ell-1}/12.
$$
The lower bound is greater than three. The depth condition makes the upper bound less than $b^{m-\ell-1}$. This contradicts the integer conclusion $1+b^{m-\ell-1}\le\delta$. Thus even the closest possible ordinary guard crossings have the stated separation.

## An interval of reset seeds

Let $s=P+d$ be odd, $0\le d\le D$, and suppose $2D+4m+28\le2^m$. The first $m$ jumps from $A(1,s)$ are legal. After $i$ jumps the counters are $a_i=2\cdot3^i-1$, $c_i=P+d-3^i+1+2i$, which verify the guards and give the launch
$$
(a_0,c_0)=(2P-1,d+2m+1)
$$
after relabeling. Its maximal bulk string satisfies $m\le n<3m$. Indeed, the total left decrement proposed through $m$ bulks is less than $8x_0(3/2)^m\le P$, using $8x_0\le2D+4m+28$. The upper bound follows from $x_i-1\ge(3/2)^i(x_0-1)$: even from $x_0=3$, the last decrement $4x_{3m-1}-9$ would exceed $4P-1$ for $m\ge20$.

Now $5m+1\le\Delta\le2D+31m+1$. This still gives $\delta>3$, and gives $\delta-1<(2D+31m+23)/8$. Repeating the integer argument proves
$$
\ell\ge m-1-\left\lfloor\log_{3/2}\!\big((2D+31m+23)/8\big)\right\rfloor .
$$
For example one may take $D=3^{\lfloor m/5\rfloor}$ at every $m\ge20$. The size condition holds at $m=20$ and thereafter by $D\le(4/3)^m$ and $2(4/3)^m+4m+28\le 2^m$. The excluded depth then grows as $(1-\log_{3/2}(3)/5)m+O(1)$. The actual conditional merged checkpoint $P+1{,}934{,}340$ at $m=292$ lies in the larger numerical interval above.

## Reproduction

Run `python3 bulk_terminal_sieve_758.py` beside the other #758 scripts. It checks the inverse invariant, replays every published candidate departure for four exponents, and checks both ends and interior seeds of the larger $m=292$ interval. Depths use integer comparisons.

| $m$ | Guaranteed minimum $\ell$ | $P$ phases | Longest suffix to reset | $2P$ phases | Longest suffix to reset |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 20 | 8 | 20 | 15 | 24 | 16 |
| 35 | 22 | 13 | 25 | 39 | 22 |
| 292 | 274 | 224 | 34 | 296 | 28 |
| 1000 | 978 | 818 | 39 | 1004 | 34 |

All observed outcomes in the table are ordinary resets. Neither the theorem nor these returns determine the outcome of the blank machine.
