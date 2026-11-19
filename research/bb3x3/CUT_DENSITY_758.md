# Counting configurations that can bypass the scale-10 halting interval

At the middle of the [scale-10 interval](LOWER_SCALE_GATES_758.md), fewer than **$1.283\times10^{-38}$** of the physical odd/odd states at the nine possible aligned masses can lie on a blank trajectory passing the interval alive. Conditioning on a genuinely legal ordinary crossing with at least twelve preceding elementary calls, the fraction of states that could continue past the test is less than **$5.544\times10^{-37}$**. Every other state in that conditional ensemble halts. These are counts in specified finite sets. The unique state reached from blank, if the machine gets that far, need not be uniformly distributed in either set.

Let $F=905{,}416{,}090{,}650{,}670$, $N=543{,}249{,}654{,}390{,}404$, and $T=H-(N+F)/2$. Both distances are even. At odd/odd boundaries write $u=(a+2c-1)/2$ and $d=(c-1)/2$. There are exactly $\lfloor(u+1)/2\rfloor$ physical points at each such mass. A reset with parameter in $[H-F,H-N]$ halts. An exceptional step $E$ near the midpoint leads to a reset inside the same interval after 787 elementary calls with total mass gain 5,458. The [exceptional-annulus bounds](CUT_758.md) apply throughout the interval. A trajectory escaping the basin must therefore have ordinary blocks on both sides of the midpoint, with ample clearance for the finite test below. Its first odd/odd boundary at or above $2T+1$ has $u=T+i$, $0\le i\le8$. Its preceding block is a jump with $u$-gain 2 or a bulk pair with gain 5, 7 or 9. That gain must exceed $i$.

## A selection effect on the known blank orbit

At the verified even reset $C=18{,}378{,}934{,}934{,}402{,}308$, the next state is $A(3,C+3)$ at $u=C+4$. Exactly **one** of the $9{,}189{,}467{,}467{,}201{,}156$ physical odd/odd states at this mass can take 33 consecutive jumps, and blank takes that state. Indeed $h=(a+1)/2$ is a positive even integer there. Each jump triples $h$ and adds two to $u$. All 33 jumps are legal exactly when $3^{33}h\le u+66$, since the jump guard is $3h\le u+2$ and the final constraint is strongest. Here $\lfloor(u+66)/3^{33}\rfloor=3$, leaving $h=2$. This mass was selected at a known reset, where the launch is strongly constrained. [Proof that blank reaches the reset](POWER_CROSSINGS_758.md)

The selection persists along any trajectory with infinitely many resets. An odd reset launches with $h=1$, and an even reset launches with $h=2$ after its opening update. Set $k=\lfloor\log_3(u/2)\rfloor$. Either launch takes at least $k$ consecutive jumps since $2\cdot3^k\le u$. For $k\ge1$, an arbitrary state with the same property has $h\le(u+2k)/3^k<7$. Since $h$ has the parity of $u$, at most **three states per mass** qualify. As the reset parameters grow without bound, this family has slice frequency tending to zero although the trajectory enters it at every launch. This example concerns a long initial jump sequence. Its occurrence gives no implication about entry into the distant halting interval.

## Which residues have an incoming path?

For fixed incoming history of at least $n$ elementary calls, project the possible $d$ at $u$ modulo $3^{n+1}$. The extra digit accounts for a two-call bulk pair straddling the far end of the requested history. For $n=0$ allow all three residues modulo three. For $n=1$, a final jump gives $d\equiv-u\pmod3$ and a final pair gives $d\equiv2$ or $5\pmod9$. For $n\ge2$, use the four [pair constants](EXCURSION_POWERS_758.md) $(v,b)$ and take the union of

$$
3D_{n-1}(u-2)-u+3,\qquad
(9D_{n-2}(u-v)+b)/4
\pmod {3^{n+1}}.
$$

At the crossing restrict the final branch to gains $v>i$, including $v=2$ for a jump. Division by four is invertible at these moduli. The recursion retains every legal history. Conversely its residue conditions guarantee an integral inverse path when guards are ignored. For a pair, an integral inverse $d_{\rm old}=(4d-b)/9$ automatically selects the correct residue modulo four.

The guards do hold when both $d$ and $u/2-d$ initially exceed $100\cdot3^{13}$. For a jump the inverse is $(d+u_{\rm old}-1)/3$, and each margin remains at least one third of its previous lower bound. For a pair the inverse $(4d-b)/9$ is at least $d/3$ when $d\ge35$. Its upper gap is at least one third of the previous upper gap by substitution, since $v\le9$, $d\le u/2$ and the mass here exceeds 100. At most thirteen inverse calls are needed. Thus every inverse state is well inside the physical interval. A jump ending at nonnegative $d$ satisfies its original guard. For a pair, the two positive left decrements leave a positive left counter, so both bulk guards hold. This proves a lower bound for the number of genuinely compatible crossing states by counting full residue periods inside these margins.

## Which states can continue?

The two normalized inverse direction maps are $(x+1)/3$ for a jump and $4x/9$ for a pair, on $[0,1/2]$ in $d/u$ coordinates. For any prospective finite word, set the end direction equal to the actual $d/u$ at the end. Pull back this direction to $x$ at its start. The [bounded intercept argument](SEPARATED_FACTORS_758.md) gives $-7\le d-ux\le0$. If the word has $j$ jumps and $p$ pairs, all its possible starting $d$ therefore belong to an interval of diameter at most

$$
\frac{u4^p}{2\cdot 3^{j+2p}}+7.
$$

For each of the nine masses the checker computes the largest population of the incoming residue set in any interval of a given integer length. A forward prefix can either use this population bound directly or split into its two possible next blocks. The recursion uses the smaller valid upper bound. The interval diameter depends only on $(j,p)$, so the same bound is available for every word with those counts. All splits stop after at most 399 blocks, since $(T+8)(4/9)^{399}<2$. A path exiting by a reset, halt, or exceptional step at this stage halts in the known basin.

The nine mass offsets give 60,139, 68,072, 39,827, 41,192, 39,980, 30,881, 30,844, 10,273 and 10,752 admissible residues modulo $3^{13}$, respectively. Summing the joint past/future upper bounds gives fewer than $1.238\times10^{102}$ states. There are more than $9.651\times10^{139}$ physical states in the nine slices, and more than $2.232\times10^{138}$ of them admit a legal incoming crossing with the required twelve-call history. The [integer checker](cut_density_758.py) computes all three counts without floating point and replays short histories against the original counter map.

## Conditioning on any one prescribed incoming history

Fix the aligned mass $u$ and specify an entire fine word of complete ordinary blocks ending there, with the last gain large enough to straddle $T$. Whatever admissible word is prescribed, the following fractions bound the possible survivors among states **actually realizing that word**. Each row describes a uniform draw within its own finite ensemble.

| Elementary calls in the prescribed word | Upper bound on the fraction that can escape |
|---:|---:|
| 0, unconditioned at a fixed aligned mass | $1.581\times10^{-37}$ |
| 100 | $4.678\times10^{-25}$ |
| 200 | $2.966\times10^{-12}$ |
| 250 | $7.032\times10^{-6}$ |
| 285 | $0.256$ |

With $n$ elementary calls, integrality of the backward path selects one residue class modulo $M=3^n$. Indeed a jump contributes a factor of three to the forward coefficient of the ancestral $d$ and a pair contributes $9/4$; every denominator introduced here is invertible modulo $3^n$. Conversely the final congruence makes each inverse state integral and selects the specified two-adic bulk residues. The margin argument above ensures that every member of this one class in the interior with both gaps at least $100M$ has the prescribed legal history. An interval of integer length $B$ therefore contributes at least $\lfloor B/M\rfloor$ realizations in the interior.

A future prefix confining the starting $d$ to real diameter $D$ meets a specified residue class at most $1+\lfloor D/M\rfloor$ times. Use this bound in the two-child recursion above, and divide by the lower count of realizations. The table holds uniformly over words since both counts depend only on $n$ and the mass bound. For comparison, at this scale a sufficiently long complete fine word already identifies at most one state. The actual blank orbit fixes its entire past. [Two-sided reconstruction](SEPARATED_FACTORS_758.md)

```sh
python3 cut_density_758.py
```
