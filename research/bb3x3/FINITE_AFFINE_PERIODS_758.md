# A global denominator bound for periodic ordinary excursions

An infinite ordinary excursion of #758 with an eventually periodic itinerary would require a mixed periodic direction of reduced denominator **at most 14,984,528**. The bound applies to every physical start at every mass. The [direction and deviation sweep](ORDINARY_DIRECTION_CYCLES_758.md) rules out all 400 candidate direction cycles through this cutoff. Consequently an infinite ordinary excursion would have an aperiodic itinerary. More generally, the complete counter-rule sequence of any infinite run is aperiodic, including runs with infinitely many resets.

## Integer phase states on a periodic tail

Use the odd/odd coordinates $u=(a+2c-1)/2$ and $d=(c-1)/2$. A coarse block is a jump J or a pair of ordinary bulk moves P. A fine block also specifies the residue $r=d\bmod4$ at P. A purely J tail triples $a+1$ at every block. A purely P tail grows the right counter exponentially. Either would exceed the linearly growing mass.

On a mixed periodic coarse tail, the cyclic normalized direction at each phase is $x=k/q$, with $0<k/q<1/2$, in lowest terms. The denominator $q$ is coprime to six and is the same throughout the cycle. Put $e=q d-ku$. The [ordinary-period proof](EXCURSION_POWERS_758.md) shows that these deviations remain in $[-7q,0]$ on an infinite tail. Their integer update is

| Block | Direction $k'$ | Deviation $e'$ | Mass-coordinate gain $v$ |
|---|---|---|---|
| J | $3k-q$ | $3e+q-2k'$ | $2$ |
| P | $9k/4$ | $(9e+qb_r)/4-k'v_r$ | $v_r$ |

In order $r=0,1,2,3$, the P constants are $b_r=20,35,26,29$ and $v_r=5,9,7,7$. The J direction satisfies $k/q>1/3$. The P direction satisfies $k/q<2/9$ and $4\mid k$. Thus $k$ determines its coarse successor. At P, $e\equiv qd\pmod4$, so $r\equiv qe\pmod4$. Hence the integer pair $(k,e)$ determines the fine successor. On the periodic tail it ranges over a finite set and eventually repeats. Take a minimal cycle of phase pairs. Each pair in this cycle occurs once. Its total mass-coordinate gain $V$ is a positive multiple of $q$, since $kV=q(d_{\rm end}-d_{\rm start})$ and $\gcd(k,q)=1$.

At any one direction $k$, the cycle's values of $e$ span an interval of width at most $3q$. To prove this, let $W$ be the greatest span of $e/q$ over the directions of the cycle. At J the span is at most $W/3$. At P all predecessors with this $k$ have the same next direction $x'=k'/q$. Inverting its four formulas gives a common linear term $4(e'/q)/9$ and offsets $(-b_r+4x'v_r)/9$. On $0\le x'\le1/2$ the largest and smallest offsets differ by $(15-16x')/9$. The span is therefore at most $4W/9+5/3$. Taking the maximum gives $W\le3$.

## Ternary residues from a finite suffix

A J sends $(k,e)$ by three times an integer shear plus a constant depending on $q$. A P sends it by $9/4$ times an integer shear plus such a constant. More explicitly, the shear sends $(k,e)$ to $(k,e-vk)$ with $v$ the block gain. Division by four is invertible modulo every power of three. A fixed fine suffix of $n$ elementary calls therefore fixes **both** output coordinates modulo $3^n$, independently of the initial $(k,e)$. The number of cycle phases compatible with that residue pair is at most

$$
M_n(q)=\left(\left\lfloor\frac{q}{2\cdot3^n}\right\rfloor+1\right)
       \left(\left\lfloor\frac{3q}{3^n}\right\rfloor+1\right).
$$

The first factor counts possible $k$ in $(0,q/2)$. For each such $k$, the second uses the proved width bound at that direction.

Let $F_0=F_1=1$ and $F_n=F_{n-1}+4F_{n-2}$. This counts all fine words of elementary length $n$, since a J costs one and each of the four P symbols costs two. The sum of their **last-block gains** is $L_n=2F_{n-1}+28F_{n-2}$ for $n\ge2$, with $L_1=2$. Read backwards from each cycle phase until the suffix has at least $n$ calls. Either the suffix has exactly $n$, or it starts with P followed by exactly $n-1$. Weight the phase by the gain of its incoming block. Since all phase pairs on the minimal cycle are distinct, summing over the suffix classes gives

$$
q\le V\le L_n M_n(q)+4L_{n-1}M_{n+1}(q).
$$

Even this inequality implies the absolute bound $q\le1,290,157,064$.

## Merging two residues at the first bulk pair

At the earliest P in a suffix, group residues $0$ with $3$, and $2$ with $1$. In both pairs increasing $b$ by nine increases $v$ by two. If the suffix starts with $j$ jumps before that P, the resulting change in its output $e$ for identical formal input is $9(q-2k)/4$, where $k$ is the direction numerator just before P. The preceding jumps give $q-2k=3^j(q-2k_{\rm initial})$. Thus the two outputs agree modulo $3^{j+2}$ in both coordinates. Every remaining block preserves the agreement at the required enlarged modulus. This is a residue calculation with four invertible, so it also compares formally evaluated words whose guard would fail on the same initial point.

For exactly $n\ge2$ calls, pairing words in this way halves their total weight whenever the first P is earlier than the last block. The all-J word contributes two rather than one after halving. For the sole P occurring as the last block, the two merged classes have maximum gains seven and nine, for 16 in place of $28/2=14$. Thus $L_n/2+3$ bounds the weighted classes. In the overshoot case the first P precedes the final block when $n\ge2$, giving $2L_{n-1}$ in all. Hence

$$
q\le V\le (L_n/2+3)M_n(q)+2L_{n-1}M_{n+1}(q).
$$

## Checking every larger denominator

For each real $x\in[14,984,529,3\cdot14,984,529)$, the verifier finds one of $n=15,16$ making the displayed upper bound strictly smaller than $x$. The only changes in either floor occur at multiples of $2\cdot3^j$ or $3^j/3$. The seven resulting intervals are left-closed. Checking each left endpoint suffices because the chosen upper bound stays constant throughout the interval. The smallest slack is one. The same procedure on seven intervals at $n=19,20$ verifies the larger cutoff using the unmerged inequality alone.

The recurrence for $L_n$ and the base inequalities at $n=6,7$ imply $L_{n+1}\le3L_n$ for all $n\ge6$. The weights $L_n/2+3$ obey the same growth bound. Since $M_{n+1}(3x)=M_n(x)$, increasing $n$ by one and multiplying $x$ by three preserves the contradiction. Scaling the checked interval by all nonnegative powers of three covers every $q\ge14,984,529$.

Run the [exact cutoff checker](affine_period_cutoff_758.py) with Python 3.10 or later. All floor breakpoints and word counts in this verification are integers.

```sh
python3 affine_period_cutoff_758.py
```

An independent [Python verifier](recheck_ordinary_cycles_758.py) enumerates every possible normalized direction from a backward suffix ending in a jump and then a pair. For its residue $r$ and a modulus $M>Q^2$, the required fraction satisfies $rq-Mh=k$ with $0<k<q/2$ and $q\le Q$. Thus $h/q$ is closer to $r/M$ than any other rational with denominator at most $Q$. The standard nearest-fraction calculation recovers it. For each resulting cycle the program propagates all allowed deviation residues forward through a finite past, then repeatedly removes phases with no predecessor in the resulting bounded set. The set becomes empty in all 400 cycles.

```sh
python3 recheck_ordinary_cycles_758.py
```

## Complete branch sequences

The positive mass gains carry an infinite execution to unbounded mass. If it visits infinitely many resets, their parameters tend to infinity. An odd reset starts with first counter one, and an even reset takes the opening instruction to first counter three. For any fixed run length the required sequence of J updates is legal when the reset parameter is sufficiently large. This follows directly from the J rule, since the first counter values in that fixed run are bounded and the starting right counter tends to infinity. Thus arbitrarily long J runs occur, while a purely J tail is impossible.

If the execution has only finitely many resets but infinitely many exceptional E updates, their inputs have $a=c+2$ and $c$ tending to infinity. E gives $(3c+8,1)$. For every fixed $r$, the right counter values and left decrements of the first $r$ ordinary bulk moves from a right counter of one are fixed. Eventually the left counter is large enough for all $r$ guards. Arbitrarily long runs of elementary L therefore occur alongside the infinitely many E updates. A periodic tail containing E has bounded L runs. Here both bulk residues count as L. A periodic fine labeling would also yield a periodic sequence after those labels are combined.

With finitely many resets and E updates, any infinite execution eventually consists of J and bulk pairs. If the elementary J/L itinerary were eventually periodic, a mixed period could be read starting at a J, where the first counter is odd. Every intervening ordinary L run then has even length, so its J/P block itinerary would be eventually periodic as well. The cutoff and direction sweep exclude this final case. Therefore a decision for #758 must account for a halt or an aperiodic infinite execution.
