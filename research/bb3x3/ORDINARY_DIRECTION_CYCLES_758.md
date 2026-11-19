# Testing all rational directions up to a fixed denominator

For **every reduced direction denominator up to 1,290,157,064**, the #758 counter map has **no infinite ordinary excursion whose mixed coarse word is eventually periodic in that direction**. The computation is independent of the initial counters. In particular, at a cutoff of 14,984,528 the verifier finds 400 primitive direction cycles and excludes 98,775 bounded integer deviations. The separate [denominator proof](FINITE_AFFINE_PERIODS_758.md) puts every possible survivor inside the tested range.

## Enumerating the rational directions

Use the [ordinary excursion coordinates](EXCURSION_POWERS_758.md). A mixed periodic word has a cyclic normalized slope $x=k/q$, with $q$ coprime to six and $0<x<1/2$. At a jump $J$, $x'=3x-1$ and $x>1/3$. At a pair of bulk moves $P$, $x'=9x/4$, $x<2/9$, and $4$ divides $k$. The numerator updates preserve the reduced denominator. Each is injective, and their images are disjoint modulo three. Following a candidate numerator either exits the domain or returns to its starting numerator. Entry from outside an already closed cycle would contradict injectivity.

Every mixed cycle has a phase immediately after a $P$ and before a $J$. Fix a denominator limit $Q$ and select $N$ minimal with $M=3^N>Q^2$. Starting at this phase, enumerate every backward coarse suffix beginning with $P$. Stop when its total number $n$ of elementary calls first reaches or exceeds $N$. A suffix with $p$ pairs satisfies
$$
x_{\rm ref}=R+\frac{3^n}{4^p}x_{\rm prior}\pmod M .
$$
This notation denotes rational arithmetic modulo $M$ with denominators coprime to three. Reading one further step back, a $J$ subtracts $3^n/4^p$ from $R$, while a $P$ leaves $R$ unchanged. At the stopping depth the second term vanishes. Hence $k\equiv Rq\pmod M$. The search includes arbitrarily long or short primitive periods, since a suffix can cross the end of the period as often as required.

The Euclidean algorithm reconstructs the only possible reduced $0<k<q/2$, $q\le Q$ from each residue. For completeness, consider the lattice of integer pairs $(r,t)$ with $r\equiv Rt\pmod M$. Start with $(M,0),(R,1)$ and run Euclid on the first coordinates, applying the same quotient subtraction to the second coordinates. Consecutive pairs form a lattice basis. Stop at the first pair $(r,t)$ with $r\le Q/2$. When $R>Q/2$, the preceding remainder $r_0>Q/2$ and the corresponding coefficients $t_0,t$ have opposite signs (allowing $t_0=0$). A lattice vector of first-coordinate absolute value below $r_0$ can have second-coordinate absolute value less than $|t|$ only if both coordinates vanish: coefficients of opposite signs in this basis add in the second coordinate, while coefficients of the same sign with a nonzero first-basis coefficient already reach $r_0$ in the first coordinate. If the first-basis coefficient vanishes, every nonzero multiple has second coordinate at least $|t|$ in absolute value. Consequently any solution $(k,q)$ implies $|t|\le q$. When $R\le Q/2$, the same bound follows directly from $t=1$.

Now $|rq-tk|\le Q^2<M$, and the determinant is a multiple of $M$. Thus $(r,t)$ and $(k,q)$ are collinear. The Euclidean pair belongs to a lattice basis, while $(k,q)$ is primitive in the integer plane and belongs to the lattice. Therefore they agree up to simultaneous sign. Require $t>0$, $r>0$, $3r>t$, $2r<t$, $\gcd(r,t)=1$ and $t$ coprime to six. Test the actual normalized guards from $(r,t)$ and retain the smallest numerator as the canonical representative of a completed cycle.

## Testing bounded deviations without scanning all integers

At phase $k$ the integer $e=qd-ku$ must stay within $[-7q,0]$ on any infinite survivor. The exact transitions to the next numerator $k'$ are
$$
J:\quad e'=3e+q-2k',\qquad
P_r:\quad e'=\frac{9e+q b_r-4k'v_r}{4}.
$$
In residue order $r=0,1,2,3$, the four pairs $(v_r,b_r)$ are $(5,20),(9,35),(7,26),(7,29)$. At $P$ phases $4\mid k$, so $d\bmod4=qe\bmod4$. The forward residue is fixed by $q,e$.

For each direction cycle choose a reference phase and a suffix ending at that phase with $m$ elementary calls such that $T=3^m>7q$. The checker chooses a phase with fewest pairs in its shortest sufficient suffix for speed. Reading backward, maintain the identity $e_{\rm ref}=B+S e_{\rm prior}\pmod T$, initially $B=0$, $S=1$. Extending by an earlier $J$ adds $S(q-2k')$ to $B$ and multiplies $S$ by three. Extending by an earlier $P$ adds $(S/4)(qb_r-4k'v_r)$ to $B$ and multiplies $S$ by $9/4$. Try every $r$, even when it would be incompatible with some earlier fine choice. At the end $S=0\pmod T$. Each enumerated residue for $B$ has at most one lift to $[-7q,0]$ because $T>7q$.

Every deviation on a cycle has a past long enough for this calculation. Deduplicate its candidate lifts and apply the exact forward transitions at every phase. Delete paths exiting the real bound or returning to a reference deviation absent from this list. A surviving periodic deviation would revisit a reference entry. The verifier colors each explored path and reports any such cycle. Once a path reaches an earlier path that ended without a cycle, it can also be discarded. This allows all possible periods of the fine residues.

| Maximum $q$ | Backward coarse words | Distinct direction cycles | Fine suffix words | Distinct bounded deviations |
|---:|---:|---:|---:|---:|
| 14,984,528 | 1,346,269 | 400 | 494,824 | 98,775 |
| 1,290,157,064 | 63,245,986 | 2,349 | 15,757,128 | 3,297,267 |

None of these tests found a repeated bounded deviation. At $Q=1,000,000$ the new checker recovers all 128 cycles from the [earlier direct denominator sweep](EXCURSION_POWERS_758.md). The new test combines a finite modular past with exact future transitions and uses no fine-period length cutoff.

~~~sh
c++ -O3 -std=c++17 ordinary_direction_cycles_758.cpp -o /tmp/directions758
/tmp/directions758
/tmp/directions758 1290157064
~~~
