# Which ordinary states return inside the scale-20 halting basin?

Write $h=(a+1)/2$, $u=(a+2c-1)/2$ at an odd/odd counter state of #758 or #153. Let $D=13,959,275$, $U=3^{307}/D$, $H=U-8,282,708,212/D$, $F=61,410,570,681,246,030,619$ and $L=3,403,055$. The following tests cover every admissible $u$ with $H-F\le u\le H-L-2488$. An odd/odd state requires $h\equiv u\pmod2$. A return in this interval halts by the [extended scale-20 basin](HALTING_COLLAR_758.md) whenever its seed gain is at most 2488.

| Ordinary left coordinate | Halting criterion | Maximum calls to reset |
|---|---|---:|
| Even $h$ through $1,012,257,878,130,399,645,022$ | Every coordinate | 553 |
| Odd $h$ coprime to 3 through $211,637,975,937,205$ | All except 263 possible exceptions in the [guard ledger](odd_header_ties_758.tsv). Its first row $h=1$ is already a basin reset. | 486 |
| Odd $h$ coprime to 3 through $H-F$ | A computable set leaves fewer than $1.872\cdot10^{-32}$ of these coordinates unresolved, uniformly for every admissible $u$ | 553 |

These criteria apply to a coordinate of the actual machine as soon as it is known. The fraction in the last row counts coordinates. It gives no probability law for a particular orbit. For a larger coordinate $h=3^j h_0$, the [inverse-jump argument](NONRESET_ENTRY_758.md) permits testing $h_0$ at $u-2j$.


At the fixed target crossing, all of the 264 odd primitive guard contacts below the stated cutoff are also settled by original-rule replay. [All contacts at the cut](ODD_TIE_CROSSING_758.md)

## Even coordinates through exponent 59

After the maximal initial run of $k$ jumps write $r=307-k$. The aligned ideal direction is $x=Dh/3^r$. If it survives the middle return interval, it starts with a pair $P$ and first crosses elementary depth $r$ at $m=r$ or $r+1$. The latter word must end in a pair. For an ordinary word containing $p$ pairs, its action is $(3^m x-A)/4^p$. Start $A=0$ and append a jump $J$ by multiplying $A$ by 3. Appending a pair replaces $A$ with $9A+5\cdot4^p$ and then increments $p$. At the cut the new numerator $N$ satisfies

$$N=3^{m-r}Dh-A\equiv -A\pmod{2D3^{m-r}}.$$

For $p\le28$ the existing [dyadic ledger](DYADIC_SURVIVAL_758.md) and [long-tail guard check](TARGET_BASIN_758.md) apply. At $r\le56$ this covers every feasible $p$. At $57\le r\le59$ enumerate the positions of the jumps among the remaining grouped letters. Each word prescribes a residue for $N$. Each residue can be searched on its whole arithmetic progression, including numerators from other possible starts.

| $r$ | Distinct $(m,p,N\bmod 2D3^{m-r})$ with $p>28$ | Largest tail before the return guard |
|---:|---:|---:|
| 57 | 1 | 151 |
| 58 | 29 | 163 |
| 59 | 415 | 188 |

The [header verifier](even_header_entry_758.py) reconstructs every progression. The [integer sieve](dyadic_survival_758.cpp) follows arithmetic progressions down the two ordinary branches, exactly as in the [dyadic exhaustion](DYADIC_SURVIVAL_758.md), retaining the original progression spacing when recovering its numerator. It records the first maximizing numerator and excludes any discarded gap that could affect the maximum. The [445 recorded rows](even_header_entry_758.tsv) can all be reproduced. The last short-tail guard has depth at most $60+188=248$. Evenness rules out all exact guard ties. The [physical rectangle proof](NONRESET_ENTRY_758.md) checks the short-tail integer margin, every long-tail margin, and the final return inside the basin.

## Odd primitive coordinates through exponent 45

For odd $h$ coprime to 3, take $r$ minimal with $3^r>Dh$ and suppose $r\le45$. At $k=307-r$, both $3^kh<U$ and $3^{k+1}h>U$ have clearance at least $3^k/D>F+2600$. The jump guard $3h\le u+2$ therefore gives exactly this initial launch length, as its successive tests are monotone. The aligned direction lies strictly between $1/3$ and $1$.

The possible first exact guard is $5/9$. Indeed the inverse branches $x/3$ and $(4x+5)/9$ preserve the property that a numerator over a power of 3 is nonzero modulo 5, excluding all preimages of $1$ and $1/3$ since $5\mid Dh$. Starting at a positive direction, a first arrival at zero requires a preceding $5/9$ contact. Each inverse image of $5/9$ after $l$ elementary letters has exact denominator $3^{l+2}$, because the numerator stays nonzero modulo 3. Hence contact, if any, occurs exactly at $l=r-2$. Inverse branches take $5/9$ and each of its interior preimages strictly inside their ordinary branch intervals. Thus each word of total elementary length $r-2$ beginning with $P$ contributes exactly the contact numerator $9A+5\cdot4^p$ at denominator $3^r$. It is eligible precisely when divisible by $D$.

The [checker](odd_header_entry_758.py) joins the two halves of these words using integer congruences. After the compulsory initial pair, split at the first group boundary at or above $\lfloor(r-4)/2\rfloor$. For the prefix and suffix $v,w$, the composition gives $A_{vw}=3^{|w|}A_v+4^{p_v} A_w$, where $|w|$ is its elementary length. Store suffix residues $9A_w+5\cdot4^{p_w}$ modulo $D$ and look up the residue needed by each prefix. The result is exactly 264 contacts including $h=1$. The remaining 263 are listed as possible exceptions. They begin with $14,365,291$ and $43,063,105$.

At a surviving cut $m=r$ or $r+1$, the numerator $3^{m-r}Dh-A$ is an even multiple of five. The first pair makes $A$ odd, and all following jumps or pairs preserve its oddness. Reduction therefore gives an odd multiple of five over $2^b$ with $b\le 2p-1\le45$. No eligible numerator occurs for $b\le2$. For every $3\le b\le45$ the [dyadic maxima](odd_header_tails_758.tsv) are at most 176 by exact progression search. The last pre-return guard is at depth at most $46+176=222$ after launch. No reduced dyadic can meet $0,1/3,5/9,1$ here. At every earlier guard, exclusion of the contact ledger gives a nonzero aligned distance of at least $3^{\min(k,307-222-2)}/D>F+2600$. The [physical pullback](TARGET_SHADOW_758.md) then gives the same ordinary word all the way to the return. At most $k+m+176+2\le486$ calls gain at most $\lfloor9\cdot486/2\rfloor=2187$ in seed. This covers 70,545,991,978,806 odd primitive coordinates including the reset $h=1$.

## A mass-uniform test for the full coordinate range

Set $T=F+2600$ and start the ideal map at $h/U$ with no preliminary launch. At each group start test whether every pulled-back guard $\lambda\in\{\text{inverse images of }0,1/3,5/9,1\}$ has $|h-\lambda U|>T$. These distances are exact integer comparisons. If the ideal numerator and denominator are $n,q$, initialized at $Dh,3^{307}$ and advanced without cancellation, the initial distance for guard $b/z$ at elementary depth $e$ is $|zn-bq|/(zD3^e)$. The physical pullback has $0<R\le1$ and $0\le B\le14$, and $|U-u|\le F+594$. Consequently every passed guard gives the actual branch for **all** masses in the band. A jump gains 2 mass units, a pair gains at most 9, and the last bulk plus reset gains at most 7. The last bound follows directly from the two odd-right-counter residues in the [counter update](check_bb33.py). Certify the middle interval if the preceding word with $j$ jumps and $p$ pairs still satisfies $j+2p+2\le553$ and $2j+9p+7\le2488$.

To bound the exceptions, let $K$ be the closed set of directions surviving the two inverse branches on $[0,1]$ indefinitely, including their endpoints. All four guards belong to $K$, because 0 and 1 are fixed points and the other guards map to them. Consequently all their inverse images belong to $K$. Each ordinary word defines a closed interval of initial coordinates (a cylinder), of diameter $d=U4^p/3^{j+2p}$ in units of $h$. Stopping each branch of the word tree at a selected node gives a cover of $K$. Outside the union of these cylinders enlarged by $T$ at both ends, every guard has clearance greater than $T$. Such a point must reach the middle interval before entering a stopped cylinder. The test therefore succeeds if every split used in this cover satisfies the two budgets.

For each stopped interval the number of coordinates $h\equiv1,5\pmod6$ is at most $\lfloor(\lfloor d\rfloor+2T)/3\rfloor+2$, by counting the two progressions of spacing six. At each split take the smaller of this bound and the sum of the two child bounds. The recursion depends only on $(j,p)$ and stops at the budget limits or once $d<T+1$. It gives a common exceptional set bound

$$\frac{\#\,\text{possibly unresolved odd primitive coordinates}}{\#\{1\le h\le H-F:\ h\equiv1,5\pmod6\}}<1.872\cdot10^{-32}.$$

The [checker](uniform_ordinary_shadow_758.py) uses integer arithmetic for this inequality, exposes the word predictor, and compares sample predictions with literal physical words at both ends of the mass interval. The covering argument gives the uniform bound independently of these samples.

## Reproducing the computations

Run the first three commands for the ledger checks, bounds and physical samples. The last three rebuild both sets of exhaustive tail maxima from the progression descriptions.

```sh
python3 nonreset_entry_758.py
python3 odd_header_entry_758.py
python3 uniform_ordinary_shadow_758.py
g++ -O3 -std=c++17 dyadic_survival_758.cpp -lgmpxx -lgmp -o /tmp/dyadic-758
python3 even_header_entry_758.py --worker /tmp/dyadic-758
python3 odd_header_entry_758.py --worker /tmp/dyadic-758
```
