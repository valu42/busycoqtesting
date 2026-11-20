# A uniform mixed-word passage into the even corridor

This is an all-exponent family lemma at the first parity change in
[the power crossing](POWER_PARITY_TRANSPORT_758.md). It admits arbitrarily
long bulk runs, proves every guard from rational parameter inequalities, and
composes the resulting return with a whole subsequent corridor. A separate
corollary proves that its source bands capture genuine incoming winding
phases for every $m\ge2200$. **It does not cover every
incoming phase, or establish a new blank-tape checkpoint.**

## The passage theorem

Let
$$
m\ge20,\quad P=3^m,\quad b\ge3,\quad b\equiv3\pmod4,\quad
r=(3/2)^b,\quad Q=P/r\ge1000,
$$
and put $\kappa=2187/2059$. Define the rational numbers
$$
L_{m,b}=\frac{6561rP-44040r+3584+576b}{6177r-128},
\qquad
U_{m,b}=\frac{2187rP-25498r+2720+160b}{2059r-64}.
$$
Every integer reset seed satisfying
$$
L_{m,b}\le s+2m\le U_{m,b}
\tag{1}
$$
reaches an even reset in
$$
[E_m,E_m+2m+20],\qquad
E_m=\lfloor54P/49\rfloor-2m-504.
\tag{2}
$$
The passage is finite. An odd source takes the exact first-return word
$$
J^mL^6JL^bR,
\tag{3}
$$
whose return is even and strictly below $E_m$. An even source already belongs
to the even-preserving corridor. Thereafter every first return below $E_m$
has word
$$
IJ^{m-1}L^2JLR
\tag{4}
$$
and gains an even number between $2m+14$ and $2m+20$ in its seed.
Consequently at most
$1+\lceil(E_m-s)/(2m+14)\rceil$ first returns suffice for the whole passage.
This bound proves termination; it need not be evaluated by running those
returns.

The source interval is nonempty for every admitted pair of parameters:
$$
U_{m,b}-L_{m,b}\ge \frac{21Q}{2000}-7\ge\frac72.
\tag{5}
$$
In particular it contains integer seeds of both parities. Taking $b=3$ is
permitted for every $m\ge20$. Increasing $b$ by four gives further bands
closer to the cusp, until the stated $Q$ cutoff is reached. The proof has no
enumeration over exponents or over the possible bulk carry strings.

## The six-bulk cusp header

For an odd seed write $z=s+2m$. After the opening $J^m$ the state is
$$
(a_0,c_0)=(2P-1,z-P+1),\qquad W_0=a_0+2c_0=2z+1.
$$
For a proposed ordinary bulk put $e=(c+7)/2$ and
$\epsilon=e\bmod2$. Its exact arithmetic is
$$
e'=(3/2)(e+\epsilon),\qquad W'=W+5+4\epsilon.
$$
After six such bulks and one jump let $W_*,c_*$ denote the mass and right
counter. If $H_6=\sum_{i=0}^5\epsilon_i$, expansion of the six affine
updates gives
$$
W_*=2z+35+4H_6,
$$
$$
64c_*=2059z-2187P+14232+
\sum_{j=1}^6 w_j\epsilon_{6-j},
\tag{6}
$$
where
$$
(w_1,\ldots,w_6)=(320,608,1040,1688,2660,4118),
\qquad \sum_jw_j=10434.
$$
Indeed $w_j=64(6(3/2)^j-4)$. The same carry bits occur in both displayed
coordinates; retaining this correlation improves the source bounds.

Here and below a scalar bulk recurrence can first be evaluated formally.
Its left decrement is $4\lfloor(c+1)/4\rfloor+3$, exactly its ordinary
guard threshold. If the final available left counter remains positive,
all preceding proposed decrements are available too. This will prove the
physical guards rather than assume them.

The parameter inequalities imply
$$
\kappa P+14<L_{m,b}\le U_{m,b}
<\frac{59049}{55081}P<\frac{27}{25}P.
\tag{7}
$$
Hence the opening jumps are legal. The last proposed jump of the opening
requires $z\ge P$, which also implies every preceding jump guard.
For any $j$ proposed bulks,
$$
(3/2)^j(c_0+7)-7\le c_j\le(3/2)^j(c_0+13)-13.
\tag{8}
$$
Their total left decrement is
$D_j=2(c_j-c_0)-G_j$, with $5j\le G_j\le9j$.
In particular
$$
D_6\le\frac{665c_0+7685}{32}<2P-2
$$
for $c_0\le2P/25+1$ and $m\ge20$. Thus all six bulks are legal and leave
$a_6>1$. The formal next right counter is $c_*=1-(a_6-c_6)$.
Equation (6) and $z>\kappa P+14$ give $c_*>1$, so $a_6<c_6$ and the
following jump is legal. It is an ordinary jump, not the exceptional restart.
The state reached is exactly the header (6).

## A whole bulk run without enumerating its carries

Starting at this header, propose $b$ bulks. Write $c_b$ for their final
right counter and $G_b$ for their mass gain. Equation (8) gives
$$
r(c_*+7)-7\le c_b\le r(c_*+13)-13,
\qquad 5b\le G_b\le9b.
$$
The final left counter is $a_b=W_*+G_b-2c_b$. The two sufficient inequalities
$$
2r(c_*+13)-26\le W_*+5b,
\qquad
W_*+9b\le3r(c_*+7)-21
\tag{9}
$$
therefore imply $0\le a_b\le c_b$.

Substitute the correlated header (6) into the second inequality in (9).
Its rearranged lower bound on $z$ has carry coefficients
$256-3rw_j$, which are all negative because $r\ge27/8$.
The most demanding case is consequently all six carries zero, and its
bound is exactly $z\ge L_{m,b}$. For the first inequality, the rearranged
upper bound has coefficients $128-rw_j$, again all negative. The most
demanding case is all six carries one, whose sum gives exactly
$z\le U_{m,b}$. Thus (1) proves both inequalities for every actual carry
pattern, without selecting or listing that pattern.

There is no hidden premature reset. The left counter after $J^m$ is
$1\pmod4$. Each bulk adds one to it modulo four; an ordinary jump preserves
an odd left counter modulo four. The header after $L^6J$ is therefore
$3\pmod4$, and $b\equiv3\pmod4$ makes $a_b\equiv2\pmod4$.
Consequently $a_b\ge0$ actually implies $a_b\ge2$. Every earlier left
counter in the proposed bulk run is larger. All bulk guards are legal,
and none visits the reset value one. The final even-left state satisfies
$a_b\le c_b$ and takes $R$. This proves the exact first return (3).

Its output is even: $a_b/2$ and $c_b$ are both odd, so
$s'=a_b/2+c_b+2$ is even. Equivalently, $W_*\equiv1\pmod4$ and
$G_b\equiv b\pmod4$ give the same conclusion from the mass charge of $R$.
The total seed gain is
$$
s'-s=2m+\frac{39+5b}{2}+2(H_6+H_b)
\le 2m+\frac{63+9b}{2},
\tag{10}
$$
where $H_b$ counts the high carries in this run. This uses the exact
charges of all $m+6+1+b+1$ calls.

## Composition with the spanning even corridor

Set
$$
C_m=\lfloor\kappa P\rfloor-2m-500.
$$
The even word (4) is valid for **every $m\ge20$ and every even seed in
$[C_m,E_m)$**. Here is a uniform guard proof, so this part does not rely on
the earlier finite check of exponents through 292.

Write $z=s+2m$. Throughout this interval
$$
\kappa P-501\le z\le54P/49-505.
$$
The opening $IJ^{m-1}$ reaches
$$
(a,c)=(4P/3-1,z-2P/3+3),\qquad W=2z+5.
$$
It is legal because its largest jump threshold is $2P/3\le z+2$.
Using (8) for its next two bulks gives the lower bound
$(6P-5z-62)/2$ for their final left counter. This is greater than one.
The sufficient inequality $18P-19z\le94$ then makes the following jump
legal. After that jump the right counter lies in
$$
\left[\frac{19z-18P+98}{4},
      \frac{19z-18P+220}{4}\right],
$$
and the mass lies in $[2z+19,2z+27]$.
The final bulk and reset are justified by
$$
49z-54P\le-616,\qquad 162P-155z\le678.
$$
In fact the final left counter is at least
$(54P-49z-616)/4>1$, so this word too has no intermediate reset.
All four displayed guard inequalities follow from the interval for $z$
and $P\ge3^{20}$; their exponential margins increase with $m$.

The word has three bulks. Its exact gain is
$2m+14+2H_3$, $0\le H_3\le3$, and is even. It therefore preserves even
parity and advances by at least $2m+14$ on each return.

Both source parities in (1) enter this corridor below its upper edge.
For an odd source, $Q\ge1000$ implies $b<3m$, since
$(3/2)^{3m}>3^m$. Equations (7) and (10) yield
$$
s'\le\frac{27}{25}P+\frac{27m+63}{2}<E_m.
$$
The last strict inequality follows from
$$
\frac{27}{1225}3^m>\frac{31m+1073}{2}\qquad(m\ge20).
$$
It holds at 20 and persists when the left side triples while the positive
linear right side grows by $31/2$. Also $s'>s>C_m$. For an even source,
(7) directly places the seed in $[C_m,E_m)$. Repetition of (4) now reaches
(2) in finite time, with the stated output enclosure and return bound.

## Why the source bands are nonempty

Both denominators in (1) are positive. For integers $b\ge3$,
$b/r\le3/(27/8)$ and $1/r\le1/(27/8)$. Rewriting the lower endpoint gives
$$
L_{m,b}-\kappa P
=\frac{128\kappa Q-44040+(3584+576b)/r}{6177-128/r}.
$$
Its whole numerator is positive at $Q\ge1000$. First bounding that positive
numerator from above and its positive denominator from below, and only then
splitting the resulting fixed-denominator affine expression, gives
$$
L_{m,b}-\kappa P\le\frac9{400}Q-6.
$$
Similarly the numerator $64\kappa Q-25498$ is positive, and
$$
U_{m,b}-\kappa P
\ge\frac{64\kappa Q-25498}{2059}
\ge\frac{33}{1000}Q-13.
$$
These two inequalities prove (5). The same formulas give
$L_{m,b}>\kappa P+14$. The upper correction
$-25498r+2720+160b$ is negative, and $r\ge27/8$ consequently gives the
upper bound in (7). These are elementary rational inequalities; the checker
audits their constants exactly.

## Genuine incoming winding phases at every large exponent

The bands are not merely formal seed families unconnected to the preceding
odd corridor. At **every $m\ge2200$, every directed residue cycle of the old
odd return map has at least one integer lifted path captured by this
theorem**. This statement selects some lifts on each cycle; it does not
quantify over all lifts.

Let $b_{\max}$ be the largest admitted $b$, and choose $b=b_{\max}-8$.
It is still at least three, and
$$
1000(81/16)^2\le Q<1000(81/16)^3.
$$
Equation (5) makes this source band wider than 256. Its position satisfies
$$
14<L_{m,b}-\kappa P\le U_{m,b}-\kappa P<4400.
\tag{11}
$$
The upper bound follows by discarding the negative upper correction and
using $64\kappa Q/(2059-64/r)$, $r\ge27/8$, and the displayed bound on $Q$.

On the old odd corridor, $J^mL^7R$ gives
$$
F_m(s)=s+2m+20+2H_{7,m}(s\bmod256),\qquad 0\le H_{7,m}\le7.
\tag{12}
$$
The exact word is legal whenever $s\ge A_m=\lfloor24P/23\rfloor$ and
$s+2m\le\kappa P-20$. For example, (8) bounds its final left counter below
by $(2187P-2059z-26650)/64>1$, while its return guard follows from
$6305z\ge6561P-41608$. Both hold on this corridor. The seven bulk carries
depend only on the odd seed modulo 256: increasing the seed by 256 preserves
every bulk input modulo four.

The map (12) on the 128 odd residues modulo 256 has at least one directed
cycle. Choose any one of its cycles and any residue on that cycle. By the width of (11), it has a
representative $y$ in the new source band. Its lifted cycle predecessor is
$x=y-g$, where $2m+20\le g\le2m+34$. For $m\ge2200$, (11) gives
$x+2m<\kappa P-20$. Also
$x>\kappa P-4m-20>A_m$, using
$(\kappa-24/23)3^m>4m+20$, valid already at $m=20$ and preserved as $m$
increases. Thus this is a genuine old-word return
from $x$ to $y$.

Continuing backwards along that residue cycle subtracts positive increments
between $2m+20$ and $2m+34$. Every predecessor above $A_m$ remains in the
old corridor. Stop at the last predecessor at least $A_m$; it belongs to
$[A_m,A_m+2m+34]$. Its actual forward reset chain reaches $y$, takes the
mixed-word passage (3), and then traverses the even corridor to (2).
This proves an incoming-phase family without enumerating the cycle graph
or prescribing the fine carry strings. It does **not** say that every
integer lift on every cycle enters one of these bands.

## Relation to the finite blank certificates

The unrestricted incoming-cycle corollary starts at $m=2200$, beyond the
scale of the fixed halting target $H$. It proves that the uniform mechanism
captures genuine entering paths; it supplies no new entrance on the current
blank-to-$H$ route.

For smaller exponents relevant to the existing forward calculation, the
following are examples of the new source bands. Offsets are measured from
$\lfloor\kappa P\rfloor-2m$ and include both endpoints.

| $m$ | $b$ | Integer source offsets |
|---:|---:|---:|
| 35 | 71 | 340 through 507 |
| 35 | 75 | 62 through 90 |
| 36 | 71 | 1032 through 1545 |
| 36 | 79 | 34 through 48 |
| 292 | 771 | 73 through 106 |

The inherited finite handoff starts with every possible odd seed in
$[C_m,C_m+2m+40]$. A small replay through each seed's first even reset finds
that 42 of these 55 starts at $m=35$, and 14 of the 56 starts at $m=36$,
visit one of the new source bands. The other 13 and 42 starts are not
covered by this family. These are counts in an enclosing set of possible
phases, not a frequency statement about blank or about large exponents.
The old finite proof already handles all those starts. In particular this
new lemma identifies no fresh blank checkpoint; the actual blank cusp phase
is not specified by those set-valued receipts.

The positive result is the uniform passage from (1) through a genuine mixed
word and a full subsequent corridor, including nonempty attainable incoming
phase families. The remaining connection is to show that the selected blank
phase reaches such a band, or to classify the complementary phases by other
composable rules. The terminal strip (2) also has a further word change;
the old finite mergers there do not yet give an all-exponent merger theorem.

Run the [small verifier](uniform_parity_passage_758.py) beside the original
counter rules:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 uniform_parity_passage_758.py
PYTHONDONTWRITEBYTECODE=1 python3 uniform_parity_passage_758.py --seam-audit --incoming-audit
```

It checks the rational inequalities, the exact correlated header, scalar
guard execution and output parity on 18 selected parameter pairs through
exponent 1000. The optional audits reproduce the two finite phase counts and
construct captured incoming lifts at exponents 2200 and 2201, checking their
entrances and the last old-word return directly. The arbitrarily long middle
part is certified by its positive residue cycle, rather than iterated.
The proof for all parameters is the algebra above, not those examples.
