# What happens to the original halting basin at every lift?

At the original 140-digit target $H$, **all 8,596,946 reset seeds** at distances 3,403,055 through 12,000,000 below the target halt. At the next target with exactly the same direct halting word, **all 8,596,946 pass it alive**. Across every later lift, at most **12** seeds in this same offset interval halt before passing the target. A trajectory's fate after it passes a target remains open. These are exact counts for the specified starting sets. Blank entry into either basin remains unproved. [Original interval](COVER_758.md) · [Halting family](LIFTS758.md) · [Integer checker](lifted_basin_758.py)

Let $m=292+242660k$, $D=13,959,275$, $P=3^m$, $z=(3^{15}P-130,491,612)/D$ and $H_m=z-2m$. In the following table, capture means halting before a subsequent reset strictly above $H_m$. Every uncaptured seed reaches such a reset alive. A separate forward scan classified every start in the larger window. At $k=0$ exactly **10,837,487 of 12,000,001** are captured. At $k=1$ exactly **26 of 12,000,001** starts from $H_m-12,000,000$ through $H_m$ are captured. The farthest is at distance 3,401,471, just 1,584 short of the original interval. The first row uses the previous base proof.

| Family index $k$ | Captures in the 8,596,946-seed interval, in index order |
|---|---|
| 0 | 8,596,946 |
| 1 through 8 | 0, 0, 12, 0, 6, 0, 4, 8 |
| 9 through 16 | 2, 4, 2, 2, 2, 2, 2, 4 |
| 17 through 24 | 2, 4, 2, 2, 2, 2, 2, 4 |
| Every $k\ge25$ | 0 |

## One finite calculation treats infinitely many exponents

Write $s=H_m-d$ and $W=12,000,000$. The only direct terminal starts in the full range $0\le d\le W$ are $d=0,2$. For odd $d$, the reset is even, so its [uniform short word](MOVING_SEEDS758.md) returns with an increase between $2m+21$ and $2m+31$. For even $4\le d\le W$, the initial $m$ jumps, eight bulks, one jump and six bulks lead to odd-phase coordinates
$$
h=(a+1)/2=h_d,\qquad u=(a+2c-1)/2=z-d+g_d.
$$
After the first thirteen bulks and the intervening jump, increasing the exponent along the family translates both final counters by the same amount divisible by four. At each earlier bulk the translating right offset is divisible by four too, by the integral slope calculation in the [family proof](LIFTS758.md). This still holds when the same fixed $d$ is subtracted at both scales. Therefore the extra, fourteenth bulk leaves $h_d$ independent of $m$, and all mass charges are independent of $m$. The first thirteen bulks and jump meet their guards throughout the offset interval by opposite coordinate order at its endpoints; increasing the exponent preserves all guard margins by those same slopes. At the extra bulk the gap is independent of $m$ and its minimum at $d=4$ is 7,779. The initial jumps are legal throughout because their ending right counter is positive. Along the common bulk/jump word, every first counter stays above one. The endpoint with the smallest left counter is checked directly.

Adding 32,768 to $d$ preserves every bulk residue in the fourteen bulks, since each division consumes at most one binary digit. The high digits of the final counters depend affinely on that increment. Exact calculation at both representatives of each residue gives
$$
h_{d+32768}=h_d+2D,\qquad g_{d+32768}=g_d,\qquad 37\le g_d\le65.
$$
The two terminal offsets can be treated formally when building this table. Select $r$ so $1/3<x<1$, where $x=Dh_d/3^{15+r}$. All of the tested offsets have such an $r$ between zero and 21. The next $m-r$ jumps give actual $h=3^{m-r}h_d$ and $u=z-d+g_d+2(m-r)$. At mass scale $U=3^{15}P/D$, the normalized model therefore starts **exactly** at $h/U=x$, and the initial difference $|u-U|$ is at most $2m+W+100$. The last jump has a strictly positive guard margin because $x<1$, and the same holds for every preceding jump.

From each rational $x=p/q$, follow the normalized [ordinary direction branches](ALL_ORBIT_ENTROPY_758.md). For $3p<q$, take a jump with $p'=3p,q'=q$. For $9p>5q$, take a pair of bulks with $p'=9p-5q,q'=4q$. Otherwise require $q<3p$ and $9p<5q$; this is a single bulk and a live reset. Starting from all **5,999,999** even distances in the range, every comparison was strict and every path reached the live reset, with at most **58** grouped blocks before the final bulk.

Here the limiting branches imply actual integer guards at every family exponent, including the base. At every compared state the ideal quantities $h$, $U-h$, $|3h-U|$ and $|9h-5U|$ when needed are at least $U/(3^{36}4^{58})$. This follows from the nonzero rational numerators and the bound on $q$. A jump triples $h$ and adds two to $u$. A pair sends $h$ to $(9h-5u)/4$ plus a bounded correction and adds at most nine to $u$. The sup-norm error after $n$ blocks is bounded by $4^n(2m+W+1000)$. The checker verifies that the minimum guard margin exceeds one thousand times this error at $m=292$, and the exponential growth of $U$ preserves the inequality thereafter. The multiplier leaves room for the coefficients in both bulk-guard comparisons and their bounded integer corrections. The strict coordinate margins also exclude an intermediate reset at a bulk. Consequently the returned seed is genuine.

At exact aligned odd phases let $t=(c-1)/2=(u-h)/2$. J sends $(u,t)$ to $(u+2,3t-u+1)$. A bulk pair sends it to $(u+v,(9t+b)/4)$, where $(v,b)$ is $(5,20),(9,35),(7,26),(7,29)$ for $t=0,1,2,3\pmod4$. The final bulk and return add $5+2(t\bmod2)$ to $u$. Initial residues modulo $2^{136}$ suffice for all 58 pairs and the initial division by two. Thus the exact odd first-return gain lies between $4m-60$ and $4m+610$. To find the full capture basin, work backwards from distances 0 and 2. For each possible daughter distance, the two proven gain ranges give a finite list of possible parents. Filter using the exact computed gain. Every return strictly advances the reset seed, so this exhausts the basin. For $k\ge25$ even the first $m$ jumps of an odd seed gain $2m>W$, and every nonterminal seed passes the target on its first return.

Run the full checker with Python 3.10 or later. It also compares selected returns at exponents 292 and 242,952 against direct arithmetic on the full-size counters.

```sh
python3 lifted_basin_758.py
python3 lifted_basin_758.py --dense
```

## Growing windows below the same halters

The phenomenon persists on a scale growing faster than $m$. Let $1\le\alpha<2-\delta$, where $3^{-\delta}+(4/9)^\delta=1$ and $\delta=0.73177394\ldots$. Among all starts from $H_m-\lfloor m^\alpha\rfloor$ through $H_m$, the fraction that can halt before passing $H_m$ tends to zero as $m$ increases along the lifted family. The same conclusion includes a possible halt at a different terminal before that passage.

Put $B=m^\alpha$ and $L=\lceil\log m\rceil$. For $d\le B$ the established even word still holds for sufficiently large $m$: the guard coefficients have strict margins proportional to $P$ and the initial perturbation is only polynomial in $m$. Its return gains $2m+O(1)$. The common odd prefix also remains legal for $d\ge4$ because its first thirteen bulk guards have strict relative margins and the final bulk gap increases with $d$. Our header formula gives $h_d=Dd/16384+O(1)$ for all even $d$, with an absolute error independent of $m,d$.

For $L<d\le B$ align the second jump run as in the [cusp boundary-layer proof](CUSP_TERMINALS_758.md), using the true maximal run of $k$ jumps. Then $k=m-\log_3 d+O(1)$, $w=C_0 3^{m-k}$ is comparable to $d$ for a fixed $C_0>0$, and the aligned direction is $x=d/w+O(1/d)$. The error uses $B^2+mB=o(P)$. For the next $N=\lceil2\log B/\log(9/4)\rceil$ blocks each legal normalized inverse branch recovers its input with error $O(1/P)$, uniformly over this layer. Their contraction factors are $1/3$ and $4/9$, so accumulated inverse error is still $O(1/P)$. If all $N$ blocks survive, $x$ lies within $O(1/P)+(4/9)^N$ of the ordinary direction survivor set $S$. If a halt or exceptional instruction comes sooner, its normalized guard is within $O(1/P)$ of $1/3$ or $5/9$, both endpoints in $S$. This again puts $d$ within $O(1)$ of $wS$. An intermediate ordinary bulk producing a reset at $a=1$ yields a regular return of length at most $N$ here. Every other regular odd start returns with gain $2m+2k+O(N)=4m+O(\log m)$.

Every regular return gains at least $m$ for large $m$. Before passage there are at most $O(B/m)$ such returns; their summed displacement is $2im+O(E)$ for some $0\le i=O(B/m)$ and $E=C(B/m)\log m$. A captured start must therefore lie within $O(E)$ of some $2im$ or $2im+wS$, including starts that enter $d\le L$. The scales $w$ form a geometric progression through $O(B)$. A stopping-interval cover of $S$ by at most $(3/\ell)^\delta$ intervals of length $\ell$ follows from the displayed equation defining $\delta$. For each translation, summing at $\ell=E/w$ costs $O(B^\delta E^{1-\delta})$ integer points; all $w<E$ fit in one $O(E)$ neighborhood. Multiplying by $O(B/m)$ translations and dividing by $B$ gives an upper bound
$$
 O\left(\frac{B(\log m)^{1-\delta}}{m^{2-\delta}}\right)=o(1).
$$
This is a statement about reset seeds sampled in these specified moving windows. A single deterministic blank orbit may still select a captured seed.
