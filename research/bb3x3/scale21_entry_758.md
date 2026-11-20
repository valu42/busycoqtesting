# Ordinary-state entry across the scale-21 mass band

The complete even rectangle and the R88 sufficient predicate retain
their previous left-coordinate bounds across the enlarged scale-21
mass band. The checker explicitly invokes the completed basin verifier
before reporting a halting conclusion. The R87 scale/depth transport
below also follows from the prior shadow certificate without a new
enumeration.

Put

$$
F_{21}=160,391,744,210,493,965,542=3F_{20}-8,
\qquad L=3,403,055.
$$

The [scale-21 basin](TARGET_GAP_21_758.md) supplies the reset-halting
dependency. With that dependency and the guard check below, both the
[complete even rectangle](wider_even_entry_758.md) and the
[R88 filtered test](entry_transport_758.md) extend to the following band
at odd/odd counter states, with both $h=(a+1)/2$ and $u$ even:

$$
H-F_{21}\le u=(a+2c-1)/2\le H-L-2488.
$$

The left-coordinate predicate is unchanged. Every even
$2\le h=(a+1)/2\le3,036,773,634,391,198,935,066$ is accepted. Beyond
that full rectangle, apply the existing first-cut test through

$$
h_{\max}=69,471,640,166,665,074,144,382,279,320,672,514:
$$

accept an early ordinary return or a first complete dyadic cut with at
most 28 pairs. The other cuts remain inconclusive. Every accepted
ordinary state first returns inside the enlarged reset basin within
**553 counter calls**.

## Why the same left coordinates still work

Let $U=3^{307}/D$, where $D=13,959,275$. For canonical exponent $r$, the
maximal physical initial jump run is still $k=307-r$. The extremal
left-coordinate floors do not change when the lower mass boundary moves
from $H-F_{20}$ to $H-F_{21}$. The integer gap between successive
launch thresholds is far larger than this change of mass.

At the aligned launch, $0<U-u_*\le F_{21}+594$. The same pullback proof
therefore requires clearance exceeding $F_{21}+2600$. Uniform
parity/divisibility supplies this through depth **247**, since

$$
\min(3^{219},3^{58})>D(F_{21}+2600).
$$

All first cuts lie at depth at most 89 and are already physically
shadowed. A continuing dyadic direction has odd numerator divisible by
five. For a later guard $b/3^t$ at elementary depth $l$, only the integer
distances

$$
|3^t n-b4^q|
\le\left\lfloor\frac{D(F_{21}+2600)}{3^{307-l-t}}\right\rfloor
$$

can threaten the physical comparison. The unchanged
[reverse-guard checker](dyadic_guard_shadow_758.py), with
`r=88`, `upper=F21+600`, `last=277`, tests those candidates. The
[receipt](scale21_entry_guard_758.tsv) records every new depth 248–277.
All 30 depths have zero possible cut ancestors. The final depth has
**764,815,183,667,524** candidate distances before inverse exclusion.

For a smaller own cut exponent, any surviving dyadic tail reaches a
complete boundary at depth 88 or 89 before the initial shadow ends.
The reverse checker imposes no pair-count cap at that later boundary.
Consequently it includes the actual history even when more pairs have
accumulated since the original cut with at most 28 pairs.

The dyadic angular words themselves do not depend on the physical mass.
Thus the existing full-rectangle lattice exhaustions can be reused.
Their one longer $r=60$ direction returns at aligned depth 259, within
the new shadow; its exact individual clearance also exceeds the enlarged
error bound. For the 972 listed low-pair tails, the original exact margin
at the worst cut $m=89$ still exceeds $F_{21}+2600$ through their entire
returns. All remaining low-pair tails return by $m+188\le277$.

The counting and mass argument are unchanged:
$k+m+243+2\le553$, and a first reset has seed
$u<s\le u+2488$. Hence the upper trimming and return bound remain valid.

## A reusable scale/depth transport lemma

The wider band also admits a proof through $R=87$ directly from the old
R88 certificate. In fact,

$$
F_{21}+2600<3(F_{20}+2600).
$$

For a new candidate guard at depth $l$, relabel its entire dyadic inverse
history by increasing every depth by one. Its integer numerator and pair
count are unchanged. Its guard-distance bound is contained in the old
bound at depth $l+1$, and every condition $2q\le l$ in the reverse check
only becomes weaker after this relabelling. A new cut at $r$ or $r+1$
becomes a valid formal dyadic cut at $r+1$ or $r+2$.

If $r\le87$, that shifted cut is at exponent at most 88. A continuing
history reaches the later complete cut at depth 88 or 89, where the
old unrestricted checker admits every pair count. The established zero
ancestor counts through old depth 277 therefore exclude every new late
guard through depth 276. New earlier guards are covered by the uniform
shadow through 247. This proves the wider-band filtered criterion through

$$
h\le23,157,213,388,888,358,048,127,426,440,224,170
$$

without any new guard enumeration. Once the new cut is already
physically shadowed, more generally an error enlargement
by at most $3^s$ can be exchanged for shifting all comparison depths by
$s$, while reducing the maximum own cut exponent by $s$. The exact
inverse arithmetic is preserved; this is an inclusion argument, not an
assumption about typical angular paths.

## Size and verification

There are 80,195,872,105,245,280,000 allowed even masses. The full $r=60$
rectangle consequently contains

$$
121,768,354,998,108,739,585,604,304,504,361,494,240,000
$$

ordinary states. The unchanged R88 predicate certifies at least

$$
2,785,667,018,390,042,971,352,885,981,204,136,291,108,270,980,923,840,000
$$

ordinary states across this wider band. Its inconclusive left-coordinate
count is the same as before. These counts do not establish entry of the
selected blank trajectory.

```sh
python3 scale21_entry_758.py
python3 scale21_entry_758.py --replay-shadow
```

The default checker requires the complete scale-21 basin verification,
rechecks the archived rectangle dependencies, launch inequalities,
long-tail margins and guard-receipt counts, and performs physical
first-return replays at the new lower edge, just below the former lower
edge, and at the upper edge. The second command additionally replays the
new reverse-guard exhaustion. The old dyadic and lattice exhaustions
remain explicit dependencies, with their replay commands in the linked
notes.
