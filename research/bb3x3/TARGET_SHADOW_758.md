# Predicting a reset excursion below the large halting target

Let $H=(3^{307}-8,282,708,212)/13,959,275$. For **every** odd reset $s=H-d$ with $10^4\le d\le 10^{64}$, the beginning of the excursion following its two initial jump runs is determined by iterating a rational map. For the full range the rule decides every grouped instruction starting at elementary depth 0 through **155**, or gives the exact ordinary return earlier. Up to $d=2,716,248,271,952,006$, including the scale-10 and scale-11 corridors, the depth is **257**. In particular a direct halt or exceptional rule cannot occur there before an ordinary return within the predicted portion. The rule applies on both sides of every change of ordinary word in these ranges. It does not bound the length of an excursion which survives this portion.

## The rule

Put $D=13,959,275$, $U=3^{307}/D$, and at an odd/odd state write $h=(a+1)/2$, $u=(a+2c-1)/2$. Starting at $A(1,s)$ take the [common prefix](scale_clauses_758.py) $J^{292}L^8JL^6$, then take the maximal next string of $k$ jumps. Each jump sends $(h,u)$ to $(3h,u+2)$. Both ends of the range follow the common prefix. At each letter of that prefix the smaller seed gives a larger or equal left counter and a smaller or equal right counter. These orders persist at an ordinary bulk and jump, so the endpoint checks prove the prefix for every intermediate odd seed. The same endpoint test gives the existing fixed 300-call return word on the intervening even seeds.

At the end of the second jump run set $x=h/U$. Iterate the following exact rules.

| Direction | Actual instruction | New rational direction |
|---|---|---|
| $0<x<1/3$ | Jump $J$ | $3x$ |
| $1/3<x<5/9$ | One bulk followed by an ordinary reset | Stop |
| $5/9<x<1$ | Two bulks $P$ | $(9x-5)/4$ |

Depth counts a jump as one call and a pair as two. The rational variable is initialized just once. No rounding, bulk residue lookup, or update of the true mass is required to predict the listed instructions. To recover the exact counters or the increase of the reset seed, apply the predicted word to the counter state.

## Why a guard cannot be mistaken

For a pair, the exact integer update is
$$h'=(9h-5u+e)/4,\qquad u'=u+v,$$
where $(v,e)$ is one of $(5,-20),(9,-34),(7,-24),(7,-30)$. See the [grouped guards](even_power_prefix_758.hpp). In particular the direction tests in exact units of $h$ are within 4 of the lines $h=u/3$ and $h=5u/9$. An incoming $h=1$ is already a reset.

Consider one guard line $h'=\mu u'$ at the end of any realized ordinary word. Pull it back, writing $h-\lambda u=R(h'-\mu u')+B$. At the empty word $R=1,B=0$. Pulling a jump back replaces $\mu$ by $\mu/3$, multiplies the downstream discrepancy by $1/3$ and adds $2\mu/3$. Pulling a pair back replaces $\mu$ by $(4\mu+5)/9$, multiplies the discrepancy by $4/9$ and adds $(4\mu v-e)/9$. All these directions lie in $[0,1]$. Thus after any word $0<R\le1$ and $0\le B\le14$, since $14(4/9)+70/9=14$. For a guard in $\{0,1/3,5/9,1\}$ after $l$ elementary calls, its inverse direction is $q/3^t$ with $t\le l+2$.

There is a parity obstruction to an exact tie. Immediately before the second jump run, the left counter is 3 modulo 4. Indeed each bulk subtracts $4j+3$ and a jump preserves any odd left counter modulo 4. The 14 bulks in the common prefix start from left counter 1 modulo 4. Consequently the aligned $h=3^k h_0$ is even and positive. Every positive inverse guard direction has **odd numerator** over a power of three: inverse jumps preserve the numerator and an inverse pair gives $4q+5\cdot3^t$. The only other guard direction is zero. In particular $h\ne(q/3^t)U$, since $D$ is odd.

The common prefix increases the mass coordinate by $\gamma\in[621,649]$. At alignment $u=H-d+\gamma+2k=U-d+\eta$, where $0<\eta<1200$. Here $k\le292$ follows from $3^{293}>H+2000$, $h_0\ge1$ and the legality of the jumps (at the 293rd jump its output would already exceed the available mass). The aligned $h$ satisfies $3h>u+2$. At the maximum distance let $h_{0,\max}$ be the pre-alignment value, also the maximum by counter ordering. Direct integer comparison verifies
$$H-10^{64}>3h_{0,\max}D(10^{64}+2000).$$
This proves $3^k>D(d+2000)$ throughout the stated range.

For $t\le307$, the nonzero rational $h-(q/3^t)U$ has absolute value at least $3^{\min(k,307-t)}/D$ by divisibility. At every depth $l$ with $3^{307-l-2}>D(d+2000)$, this exceeds $d+2000$. Replacing $U$ by $u$ changes the initial comparison by at most $d$. Pulling the guard forward divides the remaining discrepancy, less its correction $B$, by $R\le1$. Thus every physical comparison has the same sign as the ideal comparison, with more than 1,980 units to spare. Applying this to $0,1/3,5/9,1$ at successive group starts excludes a reset at $h=1$, the exceptional edge, and the terminal after a single bulk. It also proves the chosen ordinary branch by induction. The two advertised depths are the direct integer evaluations of this inequality.

Run `python3 target_shadow_758.py`. It checks the prefix endpoints and uniform integer bounds, and compares 18,511 rational predictions at selected offsets against literal counter updates. A quick return ends a comparison at its first reset. The universal depth follows from the arithmetic argument; the samples do not exhaust the offset range.
