# Transporting the ordinary-state test through later guard comparisons

The sufficient test for target-band entry extends to even left coordinates
through

$$
h_{\max}=69,471,640,166,665,074,144,382,279,320,672,514.
$$

For every odd/odd state with $h=(a+1)/2$ even and

$$
2\le h\le h_{\max},\qquad
H-F\le u=(a+2c-1)/2\le H-L-2488,
$$

the predicate below either certifies a reset inside the known halting
basin within **553 counter calls**, or reports that this test is
inconclusive. Here $D=13,959,275$,
$H=(3^{307}-8,282,708,212)/D$, $F=53,463,914,736,831,321,850$, and
$L=3,403,055$. Odd/odd states with even $h$ have even $u$.

This extends the [earlier short membership test](FILTERED_ENTRY_758.md)
using a finite reverse-arithmetic exclusion of possible late guard
ambiguities. It does not require an angular enumeration of the newly
encountered high-pair prefix words. The proof still leaves open whether
the blank trajectory reaches an accepted state.

## Predicate and its dependencies

Put $R=88$. The displayed bound is the largest even integer at most
$(H-F)/3^{307-R}$. Compute the least $r$ with $3^r>Dh$.

* If the coordinate is inside the
  [complete even rectangle](wider_even_entry_758.md), accept directly.
* Otherwise initialize $x=Dh/3^r$. Apply $J:x\mapsto3x$ for $x<1/3$,
  or $P:x\mapsto(9x-5)/4$ for $x>5/9$. A direction in $(1/3,5/9)$
  certifies the ordinary return.
* Stop at the first complete block boundary $m\ge r$, counting a jump
  as one elementary call and a pair as two. Accept a return at that cut,
  or a surviving cut with at most 28 pairs. The other cuts are
  inconclusive.

The angle loop uses at most $R+1=89$ elementary updates. Its arithmetic
is exact. The [checker](entry_transport_758.py) exposes `accepts(h, u)`
and `classify_left(h)`.

The cut directions for at most 28 pairs reuse the
[exhaustive dyadic survey](DYADIC_SURVIVAL_758.md). Its unlisted tails
return by 188 additional elementary calls. The 972 listed longer tails
have individual exact physical-clearance certificates. The complete
rectangle remains a separate previously verified dependency.

## The physical launch and initial shadow

Let $k=307-r$. The same parity-separated threshold argument as in the
earlier filtered criterion proves that this is the actual maximal initial
jump count. Specifically, $Dh$ is even and never a power of three. At
$h_*=3^kh$,

$$
U-h_*\ge3^k/D,
\qquad 3h_*-U\ge3^{k+1}/D,
\qquad U=3^{307}/D.
$$

Here $k\ge307-R$, and both gaps exceed $F+2600$. The aligned physical
mass $u_*=u+2k$ satisfies $0<U-u_*\le F+594$. Thus the last jump is legal
and the next is illegal, uniformly over the mass band. In particular
$1/3<h_*/U<1$, and a surviving ordinary prefix starts with a pair.

Through aligned depth 248, the original parity/divisibility estimate
still gives physical clearance: an inverse positive guard has an odd
numerator over a power of three, while $h_*$ is even. Its nonzero
distance from $h_*$ is at least
$3^{\min(k,307-l-2)}/D$. The checker verifies

$$
\min(3^{307-R},3^{57})>D(F+2600).
$$

All cuts $r$ or $r+1$ are within this already established shadow.

## The later guard exclusion

After a cut with $p\le28$, every later surviving ideal direction has the
form $n/4^q$, with $n$ an odd multiple of five. For a guard
$\mu=b/3^t$ in $\{0,1/3,5/9,1\}$ at aligned elementary depth $l$,
the signed distance pulled back to the launch is exactly

$$
h_*-U\lambda
=\frac{3^{307-l-t}}{D}(3^t n-b4^q).
$$

The general physical pullback is
$h_*-\lambda u_*=S(h_l-\mu u_l)+B$, where
$0<S\le1$ and $0\le B\le14$. Hence an initial clearance exceeding
$F+2600$ makes the physical and ideal decisions agree, including the
exceptional and terminal tests inside an attempted bulk pair.

Set `upper = F+600` in the unchanged
[reverse-guard checker](dyadic_guard_shadow_758.py). This uses
the safe threshold `upper+2000 = F+2600`, covering the actual aligned
mass error of at most $F+594$. A potentially ambiguous guard must have

$$
|3^t n-b4^q|
\le\left\lfloor\frac{D(F+2600)}{3^{307-l-t}}\right\rfloor.
$$

Every such numerator must also have an integer inverse history to a
dyadic cut. The two inverse arithmetic branches
are forced by residues:

* a jump predecessor requires $3\mid n$ and replaces $n$ by $n/3$;
* a pair predecessor replaces $(n,q)$ by
  $((n+5\cdot4^{q-1})/9,q-1)$, requiring divisibility by nine.

Their forward numerator classes are disjoint modulo three. The checker
reverses closed intervals of candidates using exact ceil/floor division
and the residue five modulo ten. It allows inverse histories without
checking every real guard, so its candidate set contains all physical
possibilities. A zero result is a sufficient exclusion.

For $R=88$, every newly needed guard through depth $R+189=277$ has zero
eligible cut ancestors. The final guard alone has
**256,653,068,233,911** candidate distances and none with a cut ancestor.
Together with the initial shadow, this covers every unlisted tail's
return, even when the cut straddles $r$.

### Why the larger cut covers all smaller exponents

The pair bound of 28 refers to the trajectory's **own cut** at $r$ or
$r+1$. After that cut, every continuing angular update preserves the
dyadic form with odd numerator divisible by five. If the path has not
already returned, it therefore reaches a complete dyadic boundary at
depth $R$ or $R+1$. The unchanged reverse checker allows every pair
count at this later cut. Its exclusions apply to the actual intervening
history even if the pair count has increased. An earlier return is
already covered by the initial shadow through depth 248.

Thus the single unrestricted check at $R=88$ supplies the late physical
shadow for every smaller own exponent. No bound of 28 is imposed at the
later physical depth 88.

## Long tails, total calls and the size of the sufficient set

For each of the 972 archived long tails, the minimum pulled-back
clearance is its stored rational margin times $U/3^m$. The new checker
uses the worst case $m=R+1$ and verifies that even this exceeds
$F+2600$. Therefore these tails remain physically valid through their
entire returns, independently of the short-tail reverse exclusion.

The longest listed tail has 243 calls to its return guard. Since
$k+m\le308$, a final bulk and reset give

$$
k+m+243+2\le553.
$$

The returned seed consequently satisfies $u<s\le u+2488$, placing it in
$[H-F,H-L]$.

The remaining high-pair prefixes can be counted without generating them.
For each exponent $r$ beyond the complete rectangle and every $p\ge29$,
the numbers of first-cut prefixes at $m=r$ and $m=r+1$ are

$$
\binom{r-p-1}{p-1},\qquad \binom{r-p-1}{p-2},
$$

with out-of-range coefficients zero. A prefix with inverse form
$(A+4^p x)/3^m$ gives an interval of left coordinates of span
$4^p/(D3^{m-r})$. It contains at most
$\lfloor4^p/(2D3^{m-r})\rfloor+1$ even integers. Summing these products
gives the explicit inconclusive-count bound printed by the verifier.
The sum deliberately includes some early-return directions and ignores
clipping of the outermost cylinder, preserving an upper bound.

Using the completed rectangle through $r=60$ as the direct base gives
the following conservative counts.

| Quantity | Bound or count |
|---|---:|
| Possible even $h$ values in the extended range | 34,735,820,083,332,537,072,191,139,660,336,257 |
| Symbolic cylinders covering the inconclusive cases | 213,993,618,558,412,084 |
| Maximum inconclusive even $h$ values | 29,508,796,918,002,988,626,564,742,279 |
| Inconclusive fraction of this population | Less than $8.496\times10^{-7}$ |
| Certified ordinary states across all allowed even masses | At least 928,555,672,796,641,559,099,374,786,107,014,199,106,742,812,666,396,612 |

These are cardinality bounds for a specified finite population. They
give neither a distribution on the blank orbit nor a bound on the number
of earlier reset chains that can merge into an inconclusive origin.

## Reproduction

```sh
python3 dyadic_guard_shadow_758.py --r 88 --upper 53463914736831322450 --last 277
python3 entry_transport_758.py
```

The first command independently performs the inverse arithmetic.
The second checks the physical launch, all required new guard depths,
archived long-tail margins, the combinatorial count and physical returns
from selected endpoints and cylinder-boundary states: 30 accepted
physical replays and eight selected inconclusive replays. The latter
also return but are not used to enlarge the certified set. It also invokes
the complete rectangle's receipt checker. The dyadic angular exhaustion
and the complete rectangle's lattice exhaustion remain archived proof
dependencies; their full replay commands are in their respective notes.
