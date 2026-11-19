# Raw clocks at three possible halting scales

The blank tape's halting time depends on which terminal it reaches. The following conditional bounds use the published mass clock and the exact clock on the connected fourth-crossing segment. Each row assumes that blank reaches one of the two specified resets. Time counts original #758 machine transitions and includes the final transition into halt. [Mass clock](MASS_CLOCK_758.md) · [Fourth-crossing clock](fourth_clock_758.py) · [Terminal rules](timing_758.py)

| Last reset seed | Counter calls from that reset through halt | Raw transitions from that reset, rounded | Conditional raw time from blank |
|---|---:|---:|---:|
| $K$ or $K+2$, $K=40{,}486{,}323{,}621{,}582{,}648$ | 69 | $1.8642\times10^{34}$ | $3.6222\times10^{46}<T<1.4543\times10^{49}$ |
| $H-2$ or $H$, $H\approx2.1447\times10^{139}$ | 307 | $2.7926\times10^{279}$ | $4.4119\times10^{413}<T<2.1922\times10^{417}$ |
| $H_{242952}-2$ or $H_{242952}$, $H_{242952}\approx3.7586\times10^{115917}$ | 242,967 | $8.5772\times10^{231835}$ | $2.8680\times10^{347745}<T<1.1801\times10^{347752}$ |

For the first row a wide interval of earlier resets is known to skip both seeds. The actual blank crossing remains open. The third row is the first larger member of the same exact terminal family as $H$ and represents a mathematically distinct possibility. None of the rows provides an upper bound on every possible blank-tape halt. The joined machine #153 uses 50,707 fewer raw transitions. [Fifth crossing](FIFTH_CROSSING_758.md) · [Lifted family](LIFTS758.md) · [Raw join](RANKINGS.md)

The bounds in this table use one method applicable across all three scales. At the main target the tighter conditional range is $2.10448\times10^{414}<T<8.206\times10^{416}$. [Current bounds and estimate](HALTING_TIME_758.md)

## Exact clock of the terminal family

Put $m=292+242660k$, $k\ge0$, $P=3^m$, $D=13959275$, $z=(3^{15}P-130491612)/D$, and $s=H_m=z-2m$. Before jump $i$, starting at $i=0$, the two counters are $a_i=2\cdot3^i-1$, $c_i=s+1-3^i+2i$. The jump costs $3a_i^2+5c_i+6$. Summing it for $0\le i<m$ gives
$$
J_m(s)=\frac{3P^2-17P+14}{2}+(5s+9)m+5m^2.
$$

After the jumps, the 15 remaining calls have the fixed branch word B C B B C C B B J B C B B C D. The tail counters are affine in $P$ and each timing rule is quadratic. Substituting these counters in the branch clocks gives the total raw time through halt
$$
T_s=J_m(s)+\frac{957722798631288P^2+48162983789306209P+819520394564959053}{194861358525625}.
$$
The verifier recovers the coefficients by rational polynomial interpolation and checks the guards and clock against the original map for both exponents in the table. Legality for all exponents follows from the existing family proof. Along this progression $T_s/s^2$ tends to $277781074759939/45753584909922$, approximately $6.07124175$. [Affine-family proof](LIFTS758.md) · [Clock verifier](terminal_clocks_758.py)

The adjacent seed $s-2$ has the same number of leading jumps because $z-2\ge P$ for every family member. The left counter then agrees with the one on the $s$ path and its right counter is $c=z-P-1\equiv3\pmod4$. Its first bulk uses C. Starting with $s$ instead gives right counter $c+2$ and uses B. Both moves give the identical pair of counters. The smaller sibling spends $10m$ fewer raw steps on the leading jumps, and $(3c+7)/2$ more on that first bulk. Its total through halt is exactly
$$
T_{s-2}=T_s+\frac{3(z-P)+4}{2}-10m.
$$
At $m=292$ the two paths reach the same input of terminal rule D, with mass $2H+1258$. At $K$ and $K+2$ direct replay gives the exact suffixes $18642013727143271422877704871912974$ and $18642013727143271412179764538538964$, respectively.

## From blank to each reset

Let $M$ and $C$ be the known reset parameters $17{,}354{,}320{,}242{,}846{,}420$ and $18{,}378{,}934{,}934{,}402{,}308$. Let $t_{MC}$ be their verified exact intervening clock. For a reset of mass $V=2s+1$, apply the [balanced-block argument](MASS_CLOCK_758.md) through $1+2M$, add $t_{MC}$, and then count only the complete blocks between $1+2C$ and $V$. In the final segment their number is at least $\lfloor(V-1-2C)/(9B)\rfloor$ with $B$ as in the mass-clock proof. For the upper bound set $F(W)=(W^3+45W^2+585W)/36$. The integral estimate gives an upper prefix time of $2+F(1+2M)-F(2)+t_{MC}+F(V)-F(1+2C)$. Adding the exact terminal suffix and rounding outward yields the table. [Checker](terminal_clocks_758.py)

~~~sh
python3 terminal_clocks_758.py
~~~
