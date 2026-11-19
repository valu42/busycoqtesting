# Fine words at prescribed reset residues

Suppose the blank-compatible orbit is infinite and its ordinary stretches
are sublinear in their starting mass, as in the reset-dense alternative of
the [five-letter theorem](ALL_ORBIT_ENTROPY_758.md). Fix any arithmetic
progression $m\equiv a\pmod A$. Every finite fine word occurs infinitely
often in completed excursions of odd resets near $3^m$ with $m$ in that
progression. This applies to $m\equiv292\pmod{242660}$, the exact
progression of the known lifted halter.

There is also control of the absolute reset seed. For any word length
$t\ge1$ let $n=10t^2 5^t$ and $Q=2\cdot4^{n+8}$. For **every** integer
$N>1$ whose prime divisors exceed $\max(A,Q)$ and every $r\bmod N$,
every fine word of length $t$ occurs infinitely often in completed
excursions starting at an actual odd reset $s\equiv r\pmod N$ on those
same exponent scales. In fact $r$ may be any prescribed function of $m$
since all residues are sampled at each selected scale. For example, on the
halting exponent progression one can require $s\equiv H_m\pmod N$.
The sufficient threshold is large. The statement
does not give the seed's position inside its residue class or a halt.

## Conditioning the leading exponent

For a coarse length-$n$ word $v$ with $j$ jumps and $p$ pairs, choose
$e\in\{0,1\}$ so $k=7+p+e$ is odd. Use the cusp corridor of the five-letter
theorem with complete ordinary return
$$
 J^m P^7 J^h v P^e L R.
$$
The extra jumps are inserted after the seven leading pairs. Their inverse
branches preserve the interior normalized direction, and the seven
leading inverse pairs still put the start in the required cusp. No extra
pair labels were introduced. The entire trace is legal for every odd
seed in a fixed open relative interval for all large $m$.

Put $z=(s-1)/2$, $D=2\cdot4^k$ and $C=j+h+5(k+1)/2$. The exact
return increment in $z$ is
$$
 d_m(z)=m+C+B_m(z),\qquad 0\le B_m(z)\le 2k+1.
$$
Choose $0\le h<\gcd(A,D)$ so $1-C\equiv a\pmod{\gcd(A,D)}$.
The Chinese remainder theorem gives simultaneous solutions
$m\equiv a\pmod A$, $m\equiv1-C\pmod D$. Fix one such solution further
modulo $\mathrm{lcm}(A,8D)$. The function $B_m$ on $z\bmod D$ is now fixed.
Indeed after the $m$ jumps, $u=2z+1+2m$ and
$d=(u-3^m)/2$. Changing $z$ by $D$ leaves enough low bits for $k$ pairs
and the high flag of the final unpaired bulk. Changing $m$ by a multiple
of $8D$ leaves $u$ unchanged modulo $2D$ and $3^m$ unchanged modulo $2D$,
so the same low bits of $d$ persist. Each jump sends $d$ to $3d-u+1$
without consuming bits. Each pair's low two bits determine its fine
label, and its division by four consumes two bits. The $u$ increment
depends only on that label.

The resulting finite map $T(z)=z+d_m(z)\pmod D$ has least nonnegative
increments from 1 to $2k+2$. On every cycle of length $l$ their sum is
a positive multiple of $D$, so $l\ge D/(2k+2)$. A full traversal of the
cycle at actual integer seeds increases $z$ by
$$
 W_l=l(m+C)+\sum_{z\text{ on the cycle}}B_m(z).
$$
Its slope in the still-variable $m$ is exactly $l$.

## Conditioning the seed

Let $q$ be a prime divisor of $N$. There are at most $D$ cycles, and
$1\le l\le D<q$. Consequently each cycle forbids at most one residue
of $m\bmod q$ if we require $q\nmid W_l$. There is a residue avoiding
all these exclusions, since there are fewer than $q$ cycles. Use it
for each prime divisor of $N$. None divides $\mathrm{lcm}(A,8D)$;
the Chinese remainder theorem imposes all choices on $m$. Now the
integer advance of every cycle is coprime to $N$. At each phase the
successive traversals visit every $z\bmod N$, hence every
$s=2z+1\bmod N$.

The favorable-scale lemma of the five-letter theorem applies within any
fixed progression of $m$. On all sufficiently large favorable scales
there is an actual reset in a narrower relative corridor. An even entry
first returns to an odd seed inside the corridor. The next $(N+1)D+1$
odd starts stay inside for sufficiently large $m$. This count is fixed
and each reset gains $O(m)$ in a corridor of width proportional to
$3^m$. They reach a cycle and visit every phase at the prescribed seed
residue. At least $l/2$ distinct phases modulo $4^k$ occur there,
since $D=2\cdot4^k$. Distinct such residues give distinct ordered lists
of the $k$ pair labels. Discarding the labels outside $v$ therefore
leaves at least $4^p/(2k+2)$ fine labelings inside the target block.

The same argument without any prime restrictions gives the first
assertion, in which no seed residue is specified. For any length $n$,
summing over the coarse words gives at least $5^n/(2n+18)$ distinct
length-$n$ fine factors of the selected completed excursions. Under the
seed restriction this estimate holds whenever all prime divisors of $N$
exceed $D$ for every row, which is ensured by $Q$ for the stated $n$.

If one length-$t$ fine word were absent after some time in the
selected excursions, their length-$n$ factor count would be at most
$(5^t-1)^{n/t}$ by testing disjoint blocks. For the stated $n$,
$(1-5^{-t})^{n/t}\le 2^{-10t}$, and $2^{10t}>2n+18$ for every $t\ge1$.
This contradicts the lower bound. All arguments may begin after any
fixed time, proving infinite occurrence.
