# Two cusp passages reduced to their unresolved reinjections

**The blank-tape decisions for #758 and #153 remain open.** This note records
the outcome of attempting a complete induced-passage argument. It proves
uniform finite reductions at two successive parity boundaries, preserving
the correlation between the real phase and the binary carries. It also
tests the proposed carry-based ranks against actual reset-origin families.
No new blank checkpoint or global closure is claimed.

The positive results concern every admitted exponent, rather than an
exponent census:

| Component | Proved reduction | Unresolved continuation |
|---|---|---|
| First cusp entrance | At most 229 attempts reach a halt, the spanning even corridor, or the first post-header jump/restart | The jump/restart after a long bulk run |
| Next boundary | The whole preceding even exit strip reaches three exact affine sections in at most `11m+54` calls, then a halt or first unresolved reinjection within `370m+770` calls in total | The continuation from that reinjection |
| Completed bulk-return branches | Return to even parity with explicit positive gains | An even-length bulk run can instead take a jump/restart |
| Carry normalization | Exact spacing after identifying sibling inputs | Its spacing valuation can increase or decrease arbitrarily at legal jumps |
| Uniform reinjection count | No constant bound exists even on genuine first-cusp entering lifts | A rank depending on scale or richer arithmetic data remains possible |

The current [uniform passage theorem](UNIFORM_PARITY_PASSAGE_758.md) therefore
has a proved connection through the next change of word. The two-boundary
return map is still not closed: the finite reductions explicitly stop at
the unresolved inputs. The [global safety obligation](GLOBAL_SAFETY_758.md)
has not acquired a full invariant from these results.

## 1. Coordinates and physical stopping conventions

Write `J` for the ordinary odd/odd jump, `L` for a bulk, `R` for the
even-left reset, `I` for the even-reset opening, and `E` for the exceptional
restart. At an odd/odd state put

$$
W=a+2c,\qquad u=(W-1)/2,\qquad h=(a+1)/2,\qquad
e=(c+7)/2.
$$

In particular $h=u-c+1$. A bulk has the exact formula

$$
e'=\frac32(e+\epsilon),\quad W'=W+5+4\epsilon,\quad
\epsilon=e\bmod2.
$$

In the original coordinates its guard and update are

$$
a\ge4\lfloor(c+1)/4\rfloor+3,\qquad
(a',c')=(a-4\lfloor(c+1)/4\rfloor-3,
         6\lfloor(c+1)/4\rfloor+5).
$$

Each proposed bulk subtracts exactly its guard threshold from $a$.
Consequently a positive final left counter proves all preceding bulk
guards. A visit to $a=1$ is stopped immediately as a reset; it must not
be passed over while looking for another return. A left counter of zero
can legally take `R`. All constructions below distinguish these cases,
explicit halts, ordinary `J` inputs and exceptional `E` inputs.

Fix

$$
m\ge20,\quad P=3^m,\quad \kappa_1=2187/2059,\quad\kappa_2=54/49,
$$
$$
C_m=\lfloor\kappa_1P\rfloor-2m-500,\qquad
E_m=\lfloor\kappa_2P\rfloor-2m-504.
$$

The finite [parity handoff](POWER_PARITY_TRANSPORT_758.md) already covers
all phases at the first cusp for $20\le m\le292$. The uniform reductions
here explain the residual structure; they do not replace that finite
result with a stronger full crossing theorem.

## 2. First cusp: a finite outer rank and 32 correlated sections

**First-cusp reduction.** Every reset in $[C_m,C_m+2m+40]$ has a finite
reduction to one of the following outcomes:

1. A halt.
2. An even reset in $[C_m,E_m)$, which the established even corridor takes
   in finite time to an even reset in $[E_m,E_m+2m+20]$.
3. A cusp header followed by its maximal bulk run, ending at the input
   of an ordinary `J` or exceptional `E`.

Reaching the first even reset, halt or unresolved input takes at most
229 attempted passages and $229(4m+8)$ elementary counter calls. This
bound excludes the subsequent long traversal of the even corridor, whose
termination has a separate positive-gain proof.

In outcome 3 the header originates from an odd reset satisfying

$$
-501<s+2m-\kappa_1P<500m,\qquad 1\le c_*<17000m.
$$

The small-right bound applies **before** the long bulk run, not at its
unresolved endpoint. The proof never assumes that the next first return
from that endpoint exists.

### A wide capture band

Choose the largest $b\ge3$, $b\equiv3\pmod4$, such that
$Q=P/(3/2)^b\ge4000m$. Then

$$
4000m\le Q<20250m.
$$

For the source band $[L,U]$ in the earlier uniform passage theorem,

$$
U-L\ge42m-7,\qquad
2m<L-\kappa_1P<\frac{3645}{8}m-6.
$$

The upper bound follows from $L-\kappa_1P\le9Q/400-6$.
For the lower bound, its exact formula gives

$$
L-\kappa_1P>
\frac{128\kappa_1Q-44040}{6177}
\ge\frac{512000\kappa_1m-44040}{6177}>2m.
$$

The numerator is positive, so enlarging its denominator to 6177 is valid.
Every incoming seed starts below this capture band.

### One complete attempt, with no assumed return

Take an odd source with $\delta=s+2m-\kappa_1P\in(-501,500m)$,
and write $z=s+2m$. The prefix $J^m$ reaches
$(2P-1,z-P+1)$. Its next six bulks are legal and leave $a_6>1$.
Indeed their decrement is at most $(665c_0+7685)/32$, and

$$
\frac{46656}{2059}3^m>332500m+8414
$$

proves the claim throughout the strip. This inequality holds at $m=20$
and persists when the exponential side triples.

Here $a_6\equiv3\pmod4$. If $a_6>c_6$, the seventh bulk is legal:
the positive even gap is at least two when $c_6\equiv1\pmod4$, and at
least four when $c_6\equiv3\pmod4$. Its output is even, nonnegative,
and below 16000, whereas its right counter is above 16000. Thus `R`
follows, giving the old odd-preserving return $J^mL^7R$ with gain
$2m+20+2H_7$. For the bound, the formal quantity
$c_*=c_6-a_6+1$ is greater than
$(-2059\cdot501+14232)/64>-15896$, and
$a_7\le-c_*-1<16000$. The bulk lower bound gives
$c_6>(729/64)((\kappa_1-1)P-493)-7$, already large enough at $m=20$.

Otherwise the ordinary jump is legal. With the six actual carry bits
$\epsilon_0,\ldots,\epsilon_5$ and $H_6=\sum\epsilon_i$, it gives

$$
W_*=2z+35+4H_6,
$$
$$
64c_*=2059z-2187P+14232+
\sum_{j=1}^{6}w_j\epsilon_{6-j},\qquad
(w_1,\ldots,w_6)=(320,608,1040,1688,2660,4118).
$$

The same bits control both coordinates. Their sum of weights is 10434,
so

$$
1\le c_*<\frac{2059\cdot500m+24666}{64}<17000m,\qquad
W_*<2\kappa_1P+1000m+59.
$$

Also $a_*>c_*>0$, since $2\kappa_1P>51000m+967$.

Now follow only legal bulks, stopping immediately at $a=1$ or at the
first non-bulk decision. Fewer than $3m$ bulks are possible: otherwise
$c_{3m}\ge8(3/2)^{3m}-7$ and $W_{3m}<2\kappa_1P+1027m+59$
would contradict

$$
16(3/2)^{3m}>2\kappa_1P+1027m+73.
$$

At the endpoint the original scalar rules give exactly: an axis reset,
an `R` reset, a halt, an ordinary `J` input, or an exceptional `E` input.
The last two are returned as unresolved inputs, without executing an
unbounded continuation.

Every resetting outcome has gain

$$
2m+20\le g\le G_m:=\frac{31m+63}{2}.
$$

For a header followed by $j<3m$ bulks and `R`, the exact gain is
$2m+(39+5j)/2+2(H_6+H_j)$. For a direct visit to $a=1$, omit the final
`R` charge: the gain is $2m+17+5j/2+2(H_6+H_j)$; here $j$ is even and
at least two. These formulas prove both bounds, including the axis case.
Each attempt takes at most $4m+8$ calls, counting a possible halting call.

### The finite outer rank

While an attempt returns odd below $L$, increase $z$ by its proved gain.
The rank $\lceil(L-z)/(2m+20)\rceil$ decreases at each such advance.
The first reset above $L$ cannot skip the band because $U-L>G_m$.
Its offset is less than

$$
\frac{3645}{8}m-6+G_m=\frac{3769}{8}m+\frac{51}{2}<500m,
$$

so the entire pending family remains in the strip used above. Moreover

$$
\frac{(3645/8)m+495}{2m+20}<228.
$$

Thus at most 228 resetting attempts precede capture, and one further
attempt reaches even parity. A halt or unresolved `J/E` may stop the
reduction earlier. Every even reset obtained is below $E_m$: the source
and gain bounds give $s'<\kappa_1P+516m$, while
$(\kappa_2-\kappa_1)3^m>518m+505$. All displayed exponential inequalities
hold at $m=20$ and persist by comparison with their linear right sides.

The rank is deliberately **not** applied across the unresolved reinjection.

### Exact affine sections, including sibling coalescence

Eliminating $z$ from the header gives

$$
1995u+64h=2187P+\lambda,\qquad u\equiv0\pmod2,\quad h\equiv0\pmod6,
$$
$$
\lambda=20835+18(81\epsilon_1+135\epsilon_2+
171\epsilon_3+195\epsilon_4+211\epsilon_5).
$$

There are 32 distinct constants. The first carry cancels exactly. If
$\epsilon_0=1$, the odd sibling reset $s+2$ has first carry zero and
coalesces with $s$ at the first bulk. Its preceding right counters are
$4q-1$ and $4q+1$ with the same left counter. This is a genuine equality
of later states, not an assertion that the sibling reset occurred on
the original path. A fixed carry word has the exact translation

$$
z\mapsto z+128:\qquad (u,h)\mapsto(u+128,h-3990).
$$

## 3. The entire next exit strip enters three exact sections

**Second-boundary entrance.** Every even reset in
$[E_m,E_m+2m+40]$ reaches an ordinary odd/odd state within $11m+54$
counter calls, satisfying

$$
45u+4h=54P+\lambda,\qquad \lambda\in\{225,279,369\},\qquad
h\equiv9\pmod{18},
$$
$$
1\le c\le\frac{49m+555}{2},\qquad
W\le\frac{108}{49}P+4m+63.
$$

The exceptional section $\lambda=369$ has $c=1$. These are necessary
conditions for actual reached states; not every integer point satisfying
them is asserted to occur. In particular the preceding theorem's whole
even exit strip is included.

### Exact departure decision

For an even reset let $z=s+2m$. The opening $IJ^{m-1}$ gives

$$
(a_0,c_0)=(4P/3-1,z-2P/3+3),\qquad W_0=2z+5.
$$

After two bulks with carries $\epsilon_0,\epsilon_1$,

$$
a_2=3P-\frac52z-16-5\epsilon_0-2\epsilon_1.
$$

After one further jump, denote the state $(a_3,c_3)$. Then

$$
4c_3=19z-18P+130+38\epsilon_0+20\epsilon_1,\qquad
W_3=2z+19+4(\epsilon_0+\epsilon_1),\quad a_3\equiv1\pmod4.
$$

The prospective right counter of the next ordinary jump is the odd integer

$$
t=c_3-a_3+1=
\frac{49z-54P+318+98\epsilon_0+44\epsilon_1}{4}.
$$

There are exactly three possibilities:

* If $t\le-3$, a bulk leaves $\ell=-t-1-2\epsilon_2\equiv2\pmod4$,
  with $2\le\ell\le c'$. A reset follows. Its even seed gain is
  $2m+14+2(\epsilon_0+\epsilon_1+\epsilon_2)$.
* If $t\ge1$, the ordinary jump is legal and reaches $c=t$.
* If $t=-1$, then $a_3=c_3+2$ and $c_3\equiv3\pmod4$. The exceptional
  restart reaches $(3a_3+2,1)$. It must not be replaced by the formal
  ordinary jump, whose right counter would be $-1$.

No halt occurs at this departure decision.

### Uniform guards and the finite departure bound

All processed resets satisfy
$\kappa_2P-505\le z\le\kappa_2P+2m+14$. On this interval the
leading jumps are legal, and the final left counter of the two bulks is
at least $(12/49)P-5m-58>1$. The following jump's right counter is at
least $(36/49)P-9465/4>1$. These bounds prove the intervening guards.
If $t\le-3$, then $\ell\le6106$, whereas the new right counter is
larger than $(36/49)P-9465/4$. Thus the following reset is legal. No
intermediate left counter equals one.

Initially $\delta=z-\kappa_2P\ge-505$. Every old-word return increases
it by at least $2m+14\ge54$. After ten returns it would be at least 35,
where $t>0$. Hence at most ten such returns precede departure. A source
that still returns has $\delta\le-330/49$; its next gain is at most
$2m+20$. Thus the departure has

$$
-464/49\le\delta\le2m+650/49.
$$

An immediate departure from the initial strip also obeys the upper bound.
Substitution into $t$ gives the claimed bound on $c$. At an ordinary
departure,

$$
W=2z+23+4(\epsilon_0+\epsilon_1),\qquad
4c=49z-54P+318+98\epsilon_0+44\epsilon_1.
$$

Its mass is at most $(108/49)P+4m+2819/49$. The exceptional case adds
four, still below the stated bound. Each old return takes $m+5$ calls
and the final prefix takes $m+4$, proving $11m+54$.

Eliminating $z$ and $\epsilon_0$ gives

$$
49W-8c=108P+491+108\epsilon_1,\qquad
45u+4h=54P+225+54\epsilon_1.
$$

The exceptional case increases $u$ by two compared with the formal jump,
adding 90 to the last identity. Only $\epsilon_1=1$ can be exceptional:
after sibling canonicalization, $t=-1$ gives
$49z=54P-322-44\epsilon_1$; with $\epsilon_1=0$ it would require
$P\equiv35\pmod{49}$, impossible for a power of three. This gives the
third constant 369. The two jumps multiply $h$ by nine from an odd
value, proving $h\equiv9\pmod{18}$.

As at the first cusp, $\epsilon_0=1$ coalesces with the sibling $s+2$
at the first bulk. The canonical input has $z\equiv0\pmod4$ and
$\epsilon_1\equiv z/4+m+1\pmod2$. On each ordinary section,
$z\mapsto z+8$ sends $(u,h)$ to $(u+8,h-90)$.

## 4. Completed second-cusp returns and a forced reinjection band

Starting from the actual section in Section 3, fewer than $3m$ consecutive
bulks are possible. Their right counter is at least
$8(3/2)^j-7$, while the available mass after $3m$ bulks is below $3P$.
The same argument applies to a later even reset in the collar

$$
20\le z-\kappa_2P\le1000m.
$$

In that collar the header $IJ^{m-1}L^2J^2$ is legal. Its two-bulk left
counter is at least $(12/49)P-2500m-23>1$; the first subsequent jump
has a positive right counter of order $P$, and the second has $c\ge325$.

An odd bulk count $j$ leaves an even left counter. The next instruction
is a reset or halt. If it resets, put $H_2=\epsilon_0+\epsilon_1$ and
let $H_j$ count the later carries. Its seed gain is

$$
g_1=2m+\frac{27+5j}{2}+2(H_2+H_j+\chi),
$$

where $\chi=1$ for the exceptional entrance of Section 3, and zero
otherwise. The output is even for $j\equiv1\pmod4$ and odd for
$j\equiv3\pmod4$. An odd output takes the short return $J^mL^5R$,
which gains $2m+15+2H_5$ and returns to even parity. A bulk landing
directly at $a=1$ is also an odd reset and takes this short return;
its first gain omits the final reset charge, giving
$2m+11+5j/2+2(H_2+H_j+\chi)$.

The short return is justified by the five-bulk sufficient inequalities

$$
211z_1\le243P-2570,\qquad665z_1\ge729P-3688,\qquad z_1=s_1+2m.
$$

For the actual bridge output, the first reset has offset between $2m+6$
and $18m+34$. For a later collar source the first returned $z_1$ is between
$\kappa_2P+20$ and $\kappa_2P+1020m+100$. The displayed inequalities
hold on both ranges for every $m\ge20$. They make the final left
counter nonnegative and at most the right; its residue is two modulo
four, so it is at least two and no intermediate reset is skipped.

Consequently every completed reset branch from the first bridge section
reaches an even seed with offset

$$
2m+6\le s+2m-\kappa_2P\le20m+60
$$

within a further $4m+6$ calls. In the collar, a complete even-to-even
attempt has gain and length bounded by

$$
2m+16\le g\le\frac{35m+85}{2},\qquad
\text{calls}\le5m+10.
$$

An even bulk count may instead reach an ordinary `J` or exceptional `E`.
Those inputs remain unresolved. The following construction shows that
uncomplicated returns cannot postpone this issue indefinitely.

### A band that forces the unresolved branch

Choose the largest even $b\ge2$ such that $Q=P/r\ge1000m$, with
$r=(3/2)^b$. Then $1000m\le Q<2250m$. Define

$$
L_2=\frac{162rP-1038r+176+36b}{147r-8},\qquad
U_2=\frac{54rP-512r+108+10b}{49r-4}.
$$

Every even seed with $L_2\le z\le U_2$ executes its header and exactly
$b$ further bulks, ending at an ordinary `J` input with $3\le a_b\le c_b$.
Indeed the correlated header gives the two sufficient inequalities

$$
W+9b\le3r(c+7)-21,\qquad
2r(c+13)\le W+5b+23.
$$

The first follows from $z\ge L_2$: the carry coefficients after
rearrangement are $16-294r$ and $16-132r$, both negative, so the
most demanding case is both zero. The second follows from $z\le U_2$:
its coefficients are $8-98r$ and $8-44r$, so the most demanding case
is both one. The bulk bounds then give $3\le a_b\le c_b$.
Every earlier left counter is larger, proving all guards and excluding
an axis reset. Since $b$ is even, the endpoint is odd/odd and takes `J`.

The band satisfies

$$
20m+60<L_2-\kappa_2P<Q/16<1125m/8,
$$
$$
89Q/1000-11<U_2-\kappa_2P<Q/10,
$$
$$
U_2-L_2>53Q/2000-11\ge53m/2-11>\frac{35m+85}{2}.
$$

For these elementary estimates, $r\ge9/4$, $b/r\le8/9$, and
$1/r\le4/9$. Rewriting the lower correction gives

$$
L_2-\kappa_2P=
\frac{8\kappa_2Q-1038+(176+36b)/r}{147-8/r}.
$$

Its positive numerator and denominator bounds imply
$(8\kappa_2Q-1038)/147<L_2-\kappa_2P<Q/16$.
For the upper endpoint use $4\kappa_2/49>89/1000$ and
$36\kappa_2/425<1/10$. The remaining linear inequalities hold at
$m=20$ and have positive slopes.

After a successful first bridge return the source lies below $L_2$.
Each completed even-to-even attempt advances by at least $2m+16$.
The band is wider than the maximum gain, so it cannot be skipped.
All pending and first-crossing sources remain within $\delta<200m$,
inside the collar. Moreover

$$
\frac{(1125/8)m-(2m+6)}{2m+16}<70.
$$

At most 70 resetting attempts therefore precede entry, and a further
attempt forces `J`. A halt or unresolved input can occur earlier.
Combining all stages yields the finite reduction

$$
\boxed{\text{even }s\in[E_m,E_m+2m+40]
\quad\longrightarrow\quad
\text{halt or first post-header }J/E
\quad\text{within }370m+770\text{ calls}.}
$$

Every unresolved input here follows a maximal bulk run from one of the
three exact affine lines of Section 3, now with the expanded header bounds
$c<2500m$ and $W<(108/49)P+400m+31$. Indeed the later source offset is
below $200m$, so $c<2450m+115<2500m$; the original bridge's headers also
obey these expanded bounds. The exceptional section still has $c=1$. The remaining
problem has not been stopped by an arbitrary execution limit: the proof
establishes that one of the listed outcomes must occur within the bound.
Executing the final `J/E` and proving its later behavior is still required.

## 5. Carry spacing is exact, but it is not a terminating rank

The established [carry coordinate](RETURN_PREFIX_758.md) satisfies

$$
T(e)=3\lceil e/2\rceil,\qquad
\Psi(T(e))=\rho\Psi(e),\qquad
\Psi(e)=e+g(e),\quad0<g(e)<3,\quad\rho=3/2.
$$

Let $D(e)=\Psi(e+1)-\Psi(e)$ for positive integers. Then $D(e)=0$
exactly when $e$ is odd. For $e=2q>0$, put

$$
r=\nu_2(q+1),\qquad q_r=3^r(q+1)/2^r-1.
$$

The integer $q_r$ is positive and even, and

$$
D(2q)=\rho^{-r}D(2q_r),\qquad
\frac43(2/3)^r<D(2q)<4(2/3)^r.
$$

For odd $e$, the two inputs have the same $T$ image. For even $e=2q$,
scaling gives
$D(2q)=\rho^{-1}(\Psi(3q+3)-\Psi(3q))$.
When $q$ is odd the sibling identities reduce this to
$\rho^{-1}D(3q+1)$, replacing $q$ by $(3q+1)/2$ and reducing
$\nu_2(q+1)$ by one. When $q$ is even, a second scaling gives

$$
D(2q)=\rho^{-2}\bigl(\Psi(9q/2+6)-\Psi(9q/2)\bigr).
$$

The bracket lies strictly between three and nine, proving the bounds.
Zero is intentionally excluded; no application requires it.

Thus the only positive-integer plateaus are the sibling pairs
$\{2q-1,2q\}$. The quotient is strictly ordered, but its neighboring
gaps can be arbitrarily small. Their valuation is not a resource that
can only be consumed during a passage.

### Both directions of change occur on admitted second-cusp inputs

For positive even $e$ write $r(e)=\nu_2(e/2+1)$.
There are legal second jumps in the prefix $IJ^{m-1}L^2J^2$ with
$r(e)$ changing from an arbitrarily large value to zero, and others
changing from zero to an arbitrarily large value.

For the first family let $m\equiv20\pmod{42}$ and

$$
z=(54P+1978)/49,\qquad s=z-2m.
$$

This is canonical with carries $(0,1)$, and that jump has

$$
e_{\rm before}=(18P+5788)/49,\qquad e_{\rm after}=296,
$$
$$
r(e_{\rm before})=\nu_2(3^{m-1}+109),\qquad r(e_{\rm after})=0.
$$

The input valuation can be any sufficiently large prescribed value:
$\nu_2(3^{42}-1)=3$, so the powers of $3^{42}$ generate the units
congruent to one modulo eight, at every higher binary modulus.
The required target $-109/3^{19}$ is one modulo eight. Choosing the
appropriate lift also fixes an exact valuation.

For the opposite direction, choose $r\ge7$, set $c_r=2^{r+2}-11$,
and choose a sufficiently large exponent in the progression

$$
3^m\equiv43+9c_r\pmod{49},\qquad
z=(54P+4c_r-362)/49,\quad s=z-2m.
$$

Three has order 42 modulo 49 and the required residue is a unit, so
such a progression exists. This again gives carries $(0,1)$, with

$$
e_{\rm before}=(36P+19c_r+461)/98,\qquad
e_{\rm after}=2^{r+1}-2.
$$

The numerator of $(e_{\rm before}/2+1)$, over denominator 196, is
$36P+19c_r+657\equiv4\pmod8$. Hence its valuation is zero, whereas
the output valuation is $r$.

These examples can be chosen inside the inherited exit strip itself.
For each specified valuation the offset $\delta=z-\kappa_2P$ is fixed.
In the loss family, increasing $m$ by $42\cdot2^{r-2}$ preserves an exact
input valuation $r$; in the gain family, increasing it by 42 preserves
the displayed conditions. Increase $m$ within that progression until
$\delta+505\le2m+20$. Then $s\in[E_m,E_m+2m+20]$ and its departure
is immediate. No assertion is made that blank selects this member.

For valuations at least three the spacing inequalities also give strict
changes of $D(e)$ in the opposite direction. This disproves scalar
monotonicity at every legal jump. It does not rule out a rank evaluated
only at selected later passages, or one retaining the entire correlated
section rather than the adjacent perturbation $e+1$ with $h$ fixed.

### Affine-section descent is only real descent

Keeping an exact line $Au+Bh=KP+C$ does not by itself solve the problem.
For the present sections $A,B,K>0$, so the normalized coefficient below
satisfies $\beta>0$.
Let $V=u-u_0$, $\alpha=A/K$, $\beta=B/K$, and
$D_0=C/K-\alpha V$. Then $\alpha u_0+\beta h=P+D_0$.
A jump sends $\beta$ to $\beta/3$ and leaves $\alpha,D_0$ unchanged.
For a pair with $h'=(9h-5u+e_r)/4$ and $u'=u+v_r$,

$$
\alpha'=\alpha+5\beta/9,\qquad
\beta'=4\beta/9,\qquad
D_0'=D_0+\beta(e_r-5V)/9.
$$

The last quantity decreases, but its total decrease can converge:
$\beta$ shrinks geometrically and $V$ grows at most linearly. The
representation permits increasing denominators. This is not a well-founded
rank; its limiting identity
is the existing real inverse-code condition in
[SEPARATED_FACTORS_758.md](SEPARATED_FACTORS_758.md).

## 6. Genuine first-cusp entrances need arbitrarily many reinjections

An exponent-independent bound on the number of reinjections cannot supply
the missing all-exponent theorem.
This can be shown on genuine entering lifts of the first cusp, rather
than arbitrary unrelated ordinary states.

Take $m=20+4480t$ with $t\ge1$, put
$q=\lfloor\kappa_1P\rfloor$, and set $y_m=q-2m+141$.
The first admitted exponent, 4500, is beyond the present target's scale.
The congruence $3^{4480}\equiv1\pmod{2059\cdot256}$ fixes the old
odd-corridor residue cycle:

| Seed modulo 256 | Seven carry bits | Reset gain |
|---:|---|---:|
| 225 | 0000001 | $2m+22$ |
| 31 | 1000011 | $2m+26$ |
| 97 | 0000000 | $2m+20$ |
| 157 | 0111100 | $2m+28$ |

Here $q\equiv124\pmod{256}$ and $y_m\equiv225\pmod{256}$.
Its predecessor is $x_m=y_m-(2m+28)=q-4m+113$. For all admitted $m$,

$$
\lfloor24P/23\rfloor<x_m<C_m<y_m\le C_m+2m+40,\qquad
x_m+2m<\kappa_1P-20.
$$

Thus the old word is legal and this edge crosses $C_m$ for the first
time. Backtracking the positive cycle reaches a reset in
$[\lfloor24P/23\rfloor,\lfloor24P/23\rfloor+2m+28]$; all intermediate
sources remain in its proved corridor. This constructs a genuine
entrance, without identifying the lift chosen by blank.

Also $2187P\equiv1895\pmod{2059}$. At $y_m$ the first six bulk carries
are zero, because $c_0\equiv121\pmod{128}$. The exact header therefore is

$$
c_*=4729,\qquad a_*=2q-9141,\qquad W_*=2q+317.
$$

Its guards follow either from the header inequalities above or directly
from $a_6=(2q-9143)/3>1$ and $c_*-1=c_6-a_6>0$.
The right counter is fixed while the mass grows like $3^m$.

Let $K_0=2\Psi(2368)$, and formally evolve the bulk right counter $c_j$.
Then $7<K_0\rho^j-c_j<13$. Its total left decrement satisfies
$D_{j+1}=3K_0\rho^j+O(j+1)$, by the exact mass charges.
Set

$$
v_m=\log_\rho\frac{2\kappa_1\,3^m}{3K_0}.
$$

Away from the integer seams of $v_m$, the maximal bulk count is
$j=\lceil v_m\rceil$ for all sufficiently large $m$.
For $\theta=j-v_m\in(0,1)$, an odd $j$ resets. An even $j$ instead
takes a jump whose normalized direction is

$$
x=3-2\rho^\theta+O(m/P).
$$

The rotation step $4480\log_\rho3$ modulo two is irrational, by prime
factorization. The same is true on every fixed subprogression.
Consequently an open direction interval $(l,r)\subset(0,1)$ has
frequency

$$
\mu((l,r))=
\frac{\log((3-l)/(3-r))}{2\log(3/2)}>0
$$

among all admitted exponents, counting those with an even bulk run
followed by a jump into the interval. This is the established
[power-phase argument](POWER_PHASE_LAW_758.md) with a different, exactly
realized fixed right counter. No unproved arithmetic property of
$\Psi(2368)$ is used; it is a fixed rotation offset.

Write $P_2$ for two bulks. The inverse branch of $P_2J^4$ is
$g(x)=(4x+405)/729$, with fixed point $\xi=81/145$. For each fixed
$n\ge1$ the open interval

$$
I_n=g^n((1/3,5/9))
=\xi+(4/729)^n((1/3-\xi),(5/9-\xi))
$$

has positive width $(2/9)(4/729)^n$. It realizes exactly
$(P_2J^4)^nLR$ in the ideal map. Every pair is a maximal two-bulk run.
On a closed interior subinterval all guards have positive margins;
the error along this fixed word is $O_n(m/P)$. Thus infinitely many
admitted exponents realize the same actual finite word. Their exact
density is $\mu(I_n)>0$, in every fixed exponent subprogression.

For every $n$ there are therefore genuine first-cusp entrances with at
least $n+1$ even-bulk-to-jump reinjections before their first return.
These are finite excursions; their post-reset future is not classified.
The theorem excludes a finite exact-suffix catalogue or a rank with a
uniformly bounded finite range that must decrease at every reinjection.
It does **not** exclude a scale-dependent rank, a parametric acceleration
of repeated blocks, or a richer correlated arithmetic invariant.

## 7. What remains to prove

The new reductions remove repeated uncomplicated returns as an independent
obstacle and connect the preceding even passage to the next exact section.
They have not proved what happens after the emitted `J/E` input.
A closing theorem still needs to take those reinjections to a halt or a
later certified section, with a finite-time argument and the upper bound
required by the [selected-reset barrier](PROOF_STRATEGY_758.md).

The tested scalar carry quantities do not provide that theorem. The exact
affine lines preserve more ancestry than independent angle/residue bounds,
but their current propagation yields only a convergent real descent.
The arbitrary-reinjection family shows why finitely many exact suffixes
cannot complete an all-exponent version of the argument. None of these
obstructions rules out the narrower blank-selected trajectory or a rank
that retains scale and more arithmetic information.

At $m=292$ the second boundary $(54/49)3^{292}$ is above the selected
target $H$. These local components are not a final-scale bridge into its
halting basin. The full blank-to-basin connection and both blank decisions
remain open.

## 8. Focused verification

The accompanying standard-library checkers audit exact formulas, all
small carry cases, original scalar stopping cases, selected physical
entrances, the exceptional third section, and rational enclosures for
carry spacing. The quantified results above follow from their algebraic
proofs, rather than an exhaustive list of exponents or long trajectories.
No Rocq/Lean formalization or full-target invariant is claimed.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 reinjection_cusp_758.py
PYTHONDONTWRITEBYTECODE=1 python3 reinjection_second_758.py
PYTHONDONTWRITEBYTECODE=1 python3 carry_spacing_758.py
```
