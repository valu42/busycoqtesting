# Extending the physical shadow by reversing dyadic directions

For every odd target reset with $10^4\le d\le32,078,348,842,098,793,106$ whose aligned exponent is $r=62$, the physical machine follows its ideal itinerary through the grouped guard at elementary depth **251**, or makes the predicted earlier ordinary return. This gives enough depth for every dyadic tail whose return decision takes at most 188 additional calls, including a prefix that straddles depth 62. It certifies the physical decisions themselves. A separate angular search must show that a return actually occurs.

## Which comparisons need checking?

Write $U=3^{307}/D$, $D=13,959,275$, and let $h,u$ be the true integer coordinates at alignment. For each word of ordinary grouped instructions, let $l$ denote its **elementary** length and $q$ its number of pairs. Its ideal forward slope is $3^l/4^q$. Write $x_l$ for the image of $h/U$ and $\lambda$ for the inverse image of a guard $\mu=b/3^t$, where $(b,t)$ runs over $(0,0),(1,1),(5,2),(1,0)$. At the first group boundary $m\ge r$, either the excursion has returned or $m\in\{r,r+1\}$ and $x_m=N/4^p$ with $N$ odd and divisible by five. Every continuing jump and pair preserves this form, with a jump leaving $q$ unchanged and a pair increasing it by one. Hence at every later group boundary, $x_l=n/4^q$ with $0<n<4^q$, $n\equiv5\pmod {10}$, and $1\le q\le\lfloor l/2\rfloor$. [Dyadic cut](TARGET_BASIN_758.md)

Inverting the affine word gives the exact signed distance in the initial coordinates,

$$
h-U\lambda= U\frac{4^q}{3^l}(x_l-\mu)
 = \frac{3^{307-l-t}}{D}(3^t n-b4^q).
$$

For the same realized physical word, the [physical pullback estimate](TARGET_SHADOW_758.md) gives $h-\lambda u=R(h_l-\mu u_l)+B$ with $0<R\le1$, $0\le B\le14$ and $|U-u|\le d$. Thus $|h-U\lambda|>d+2000$ forces $h_l-\mu u_l$ to have the ideal sign, with absolute value greater than 1,986. The four guards include both endpoints. At an odd/odd group start the lower endpoint excludes $h_l=1$. In the exact grouped test, writing $d'=(u_l-h_l)/2$, the first comparison uses $u_l-3d'=(3h_l-u_l)/2$; the second uses $2u_l-9d'=(9h_l-5u_l)/2$. Their residue-dependent boundaries are within 4 of $h_l=u_l/3$ and $h_l=5u_l/9$ respectively. These two tests classify both instructions of a pair, or the bulk followed by a reset. They exclude single-bulk exceptional and terminal edges as well. There is no separate ideal group boundary between the two bulks. This proves the claimed agreement by induction from the [uniform shadow](TARGET_SHADOW_758.md). [Exact grouped tests](packed_return_758.hpp)

## Excluding the small signed distances

At any additional group depth $l$, a potentially ambiguous guard must have

$$
 |3^t n-b4^q|\le\left\lfloor\frac{D(d_{\max}+2000)}{3^{307-l-t}}\right\rfloor.
$$

The verifier enumerates every odd multiple of five in this closed integer interval for every allowed $q$ and guard. A physically attainable candidate must admit an ordinary history back to the cut. From the reduced dyadic numerator $n$ the inverse history, if integral, is forced:

* A jump has predecessor numerator $n/3$ with the same denominator and requires $3\mid n$.
* A pair has predecessor numerator $(n+5\cdot4^{q-1})/9$ over $4^{q-1}$ and requires divisibility by nine. This forces $n\equiv1\pmod3$ and hence excludes a jump predecessor.

The verifier reverses these steps, consuming one or two elementary calls and subtracting one pair at the inverse pair. It accepts either depth $r$ or $r+1$ as a possible cut, including histories incompatible with a particular header. If the reverse fails to reach either depth with a positive feasible pair count, the candidate cannot have occurred. The scale-20 gap has uniform depth 249. At depth 250 the distance test produces no candidates and at 251 it produces 103. None reaches a cut. All absolute distances and branch tests in the calculation are integers.

```sh
python3 dyadic_guard_shadow_758.py
```

## Larger ranges

The same test can reverse an entire interval $[a,b]$ of numerator candidates at once. For a jump the predecessor interval is $[\lceil a/3\rceil,\lfloor b/3\rfloor]$. For a pair at $q\ge2$, put $v=5\cdot4^{q-1}$; the interval is $[\lceil(a+v)/9\rceil,\lfloor(b+v)/9\rfloor]$. Intersect both with the residue five modulo ten. The jump multiplication by three preserves this residue. At a pair $v$ is divisible by ten and multiplication by nine also preserves it. The forward numerators in the two images have distinct residues modulo three. Therefore the counts add exactly. A singleton interval can be tested by the simpler pointwise inverse.

If the actual exponent is smaller than a proposed $r$, the itinerary still crosses depth $r$ or $r+1$ with a dyadic direction. Thus a successful exclusion applies simultaneously to all smaller exponents. For example the command below certifies through depth 263 for every exponent at most 74 under the indicated upper distance and the original physical-shadow hypotheses. The last guard alone has 16,379,132,932,986 candidates and zero with a cut ancestor. This certifies the physical meaning of a finite ordinary word. To extend a halting basin at these exponents one must also prove angular return for the relevant headers.

```sh
python3 dyadic_guard_shadow_758.py --r 74 --upper 17047749786993825769927746 --last 263
```

## Direct clearance on complete long tails

For a listed cut numerator $N/4^p$, iterate the ideal map all the way to its first return. After $e$ further elementary calls write the direction as $a/b$ with $b=4^{p+p_e}$, where $p_e$ counts further pairs. At each group start the least initial clearance over the four guards is $U c/3^m$, where

$$
c=\frac{\min(9a,3|3a-b|,|9a-5b|,9(b-a))}{9\cdot3^e}.
$$

This is the same pullback identity with $l=m+e$. Its value is independent of which header word reached the cut. The [basin verifier](target_basin_758.py) minimizes $c$ across every group start of all 972 listed tails, including the terminal group start. The minimum occurs on the $5/9$ guard at $e=243$, for $p=28$ and $N=62,420,325,085,947,185$. At $m=63$ its physical clearance exceeds $2.3928\times10^{62}$ in aligned units. At scale 20 this certifies all 972 paths through their returns.

The same 972 families are safe through $r=106$ in the domain of the physical shadow theorem whenever a trajectory reaches one of them at its cut. Indeed $h=3^{307-r}h_0<U$ there, while the [affine header identity](scale_transport_758.py) gives $2\cdot32768h_0\ge55,837,100d-203,238,392$. The resulting upper bound on $d+2000$ at $r=106$ is below $3.160\times10^{40}$, while even the smallest clearance at $m=107$ exceeds $2.429\times10^{41}$. For smaller $r$ the distance bound decreases and the clearance increases. Other dyadic directions and high-pair prefixes at those higher scales require their own checks.
