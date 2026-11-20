# Exact prefixes for the #758 crossing checker

The parity-aware checker represents each pending seed inside a direct-trace interval by one bit. Processing the least set bit gives the same ascending seed order and duplicate suppression as the ordered-set version. The checker widens certified parity classes as described in [the crossing proof](BLANK_CROSSINGS.md). On an unresolved class it needs the exact first positive return.

## Sharing exact first-return prefixes

Within a same-parity interval the first reset move and an initial run of jumps produce a fixed first counter $a$ and an increasing second counter $c$. After any further common word of jumps and bulk moves, $a$ remains nonincreasing and $c$ remains nondecreasing as functions of the initial seed. An endpoint comparison therefore proves a common ordinary branch for the whole interval. Each cached prefix stops before taking a move from an interval whose minimum $a$ is at most 1. Thus it cannot skip an earlier visit to $a=1$.

Suppose the prefix has $b$ bulk moves. Translating the seed by $2^{b+1}$ preserves the second-counter residue modulo four at every bulk move. Initially the translation in $(a,c)$ is $(0,2^{b+1})$. A jump sends a translation $(A,C)$ to $(3A,C-A)$. A bulk move sends it to $(A-C,3C/2)$ and consumes one bit of divisibility. A table stores one exact output for each seed residue of the chosen parity. A translated output follows by adding the computed translation. At a return the output seed shifts by precisely the original period, since every translation preserves $A+2C$.

In smaller aligned intervals the checker groups further common runs. For a bulk move put $x=\lfloor(c+1)/4\rfloor+3$. Then $x'=\lfloor3x/2\rfloor$, the decrement of $a$ is $4x-9$, and the new $c$ is $6x-13$. Over $n$ bulk moves the total decrement is

$$
8(x_n-x_0)-9n+4\,\#\{i:0\le i<n,\;x_i\text{ is odd}\}.
$$

Increasing $x_0$ by $2^n$ increases $x_n$ by $3^n$ and preserves all the counted parities. This gives a table for runs of up to seven bulk moves. A jump run uses the original power-of-three formula. Ambiguous or exceptional branches at the end of a cached prefix use the scalar rules. A rare long tail is replayed with the reference checker's original 5,000-call budget.

## Reproduction

Use a C++17 compiler supporting the GCC/Clang trailing-zero builtin. Run these commands in the directory containing the counter sources.

~~~sh
c++ -O3 -std=c++17 cross_758_fast.cpp -o /tmp/cross_758_fast
/tmp/cross_758_fast 2044855966425482 2045355966425482
python3 audit_return_prefix.py
~~~

The benchmark shard prints the following six fields, matching the ordered-set parity checker.

~~~text
2044855966425482 2045355966425482 2045355966425482 2045355966425602 12766 43135720
~~~

The audit compares 65,294 seed/range cases, including 50 halting cases, against unbatched Python counter steps.

## A bulk coordinate that retains the carries

The following mathematical representation applies to runs of any length; it does not add another bulk table. At a positive odd right counter put

$$
 E=(c+7)/2\ge4,\qquad \rho=3/2.
$$

An ordinary bulk satisfies exactly

$$
 E'=T(E)=3\lceil E/2\rceil=\rho(E+\epsilon),\qquad
 W'=W+5+4\epsilon,\qquad \epsilon=E\bmod2.
$$

The same carry bit controls both the right-counter rounding and the mass gain. For $E_i=T^i(E)$ and $\epsilon_i=E_i\bmod2$, define

$$
 \Psi(E)=\lim_{j\to\infty}\rho^{-j}E_j
 =E+g(E),\qquad
 g(E)=\sum_{i\ge0}\epsilon_i\rho^{-i}.
$$

Then $\Psi(T(E))=\rho\Psi(E)$ exactly. This is a semiconjugacy: $\Psi(2q-1)=\Psi(2q)$ because $T$ sends those two inputs to the same point. The correction obeys $0<g(E)<3$ for every positive integer $E$. Some iterate must be odd, since a positive integer cannot keep dividing by two forever. Equality $g(E)=3$ would require every iterate to be odd; then $E_j+3=\rho^j(E+3)$ could be integral for every $j$ only if $E=-3$. This also proves uniqueness among functions $\Psi(E)=E+O(1)$ with this scaling identity: iterate the identity and divide by $\rho^j$.

This exact function is distinct from a finite approximation to it. After just $t$ carry steps, rational arithmetic gives the certified enclosure

$$
 \rho^{-t}E_t<\Psi(E)<\rho^{-t}(E_t+3),
 \tag{1}
$$

of width $3\rho^{-t}$. Moreover $\Psi$ is nondecreasing, since every $T^j$ is nondecreasing. Endpoint enclosures therefore also bound $\Psi$ throughout an input interval.

### A phase-conditioned return of arbitrary run length

Start from positive odd $a_0,c_0$, let $W_0=a_0+2c_0$, and take any odd integer $b\ge1$. If

$$
 \boxed{
 \frac{W_0+39+9b}{6}
 \le\rho^b\Psi(E_0)
 \le\frac{W_0+14+5b}{4},
 }
 \tag{2}
$$

then the original counter map takes **$L^bR$ up to its first subsequent reset**. Here this means the first positive-time visit to $a=1$; the input need not itself be a reset. The criterion proves the guards; it does not assume that the bulk run is already known to occur.

Indeed let $S_j=\sum_{i<j}\epsilon_i$. Formal bulk iteration gives

$$
 W_j=W_0+5j+4S_j,\quad
 E_j=\rho^j\Psi(E_0)-g(E_j),\quad
 a_j=W_j+14-4E_j.
$$

The upper bound in (2), $S_b\ge0$ and $E_b\le\rho^b\Psi(E_0)$ imply $a_b\ge0$. Every formal bulk decreases $a$ by the positive quantity $4\lfloor(c+1)/4\rfloor+3$, while its right counter stays positive. A nonnegative final $a_b$ therefore proves every earlier bulk guard and $a_j>1$ for $j<b$. The lower bound in (2), $S_b\le b$ and $E_b\ge\rho^b\Psi(E_0)-3$ imply $W_b+21\le6E_b$, which is exactly $a_b\le c_b$. Since $b$ is odd, $a_b$ is even, and the next move is the reset $R$. The case $a_b=0$ is allowed by the counter map.

The returned seed has the exact form

$$
 s'=\frac{W_0+5b}{2}+2S_b+2.
 \tag{3}
$$

In particular it belongs to an interval of width $2b$:

$$
 \frac{W_0+5b}{2}+2\le s'\le\frac{W_0+9b}{2}+2,
 \qquad
 s'\text{ is even}\iff W_0+b\equiv0\pmod4.
$$

The output parity is independent of all carry choices. For example $W_0\equiv1\pmod4$ requires $b\equiv3\pmod4$ for an even returned seed.

If $t\le b$ initial carries have been evaluated, use $S_t\le S_b\le S_t+b-t$. This strengthens (2) to

$$
 \frac{W_0+39+9b+4(S_t-t)}6
 \le\rho^b\Psi(E_0)
 \le\frac{W_0+14+5b+4S_t}4,
 \tag{4}
$$

and confines (3) to an interval of width $2(b-t)$, with lower endpoint $(W_0+5b)/2+2S_t+2$.

Equations (1) and (4) give a finite certificate using only $t$ carry steps, even when $b$ is much larger. For precision, suppose the true value $X=\rho^b\Psi(E_0)$ is separated from both required phase endpoints by at least $\eta X$, where $\eta>0$. The enclosure width relative to $X$ is at most $3\rho^{-t}/E_0$. Thus $3\rho^{-t}/E_0<\eta$ suffices to certify the inequalities, provided $t\le b$ as above. At fixed relative margin the required precision is independent of the later run length $b$; runs shorter than that precision can be checked directly. A failed certificate makes no assertion about the run's actual outcome or a subsequent excursion.

### Correlated comparison across a jump

At an odd/odd jump, with $h=(a+1)/2$, one has $h'=3h$ and $E'=E-h+1$. Its original guard is exactly $E'\ge4$. For $h>1$ put $r=\nu_2(h-1)$. The first $r$ carry bits of $E$ and $E'$ agree, and

$$
 T^i(E)-T^i(E')=\rho^i(h-1)\qquad(0\le i\le r).
$$

Cancelling those common carries gives

$$
 \Psi(E')-\Psi(E)=-(h-1)+\Delta,
 \qquad |\Delta|\le3\rho^{-r}.
 \tag{5}
$$

For $h=1$, the two inputs agree and $\Delta=0$. At the first differing bit put $\sigma=T^r(E)\bmod2$; the other input has the opposite parity. Since $g$ lies in $[0,2]$ on even inputs and $[1,3]$ on odd inputs, (5) refines to $\Delta\in\rho^{-r}[-1,3]$ if $\sigma=0$, and $\Delta\in\rho^{-r}[-3,1]$ if $\sigma=1$. These are correlated bounds for the same jump, not independent choices of real errors. They do not constitute a decreasing rank.

There is also a simple relation to the earlier endpoint order. In formal $(a,c)$ coordinates, changing one bulk carry from zero to one injects $(-2,3)$. Later $J$ and $L$ steps with their carries fixed send a difference to $(3\Delta a,\Delta c-\Delta a)$ and $(\Delta a-\Delta c,3\Delta c/2)$ respectively. Both preserve $\Delta a<0$, $\Delta c>0$, and $\Delta W=4$. Thus all-low and all-high formal carries are opposed extrema along any fixed coarse word. They need not themselves be legal integer histories. This enclosure preserves the mass/right-counter relation; it does not settle a change of coarse word.

### The exact uncertainty left by a fixed modulus

For any $n$, a prescribed list of $n$ carry bits selects exactly one class of $E$ modulo $2^n$:

$$
 E\equiv-\sum_{i=0}^{n-1}\epsilon_i2^i3^{-i}\pmod{2^n}.
$$

Now fix a modulus $M$, a residue $a$, and any lower bound $N$. Let $r=\nu_2(M)$ and let $C_r$ be the contribution of the first $r$ carries, which are fixed by $E\equiv a\pmod M$. Then

$$
 \overline{\{g(E):E>N,\ E\equiv a\pmod M\}}
 =\left[C_r,C_r+3\rho^{-r}\right].
 \tag{6}
$$

To prove attainability, every finite continuation of those $r$ bits has its unique class modulo a higher power of two. The Chinese remainder theorem combines it with the odd part of $M$ and gives arbitrarily large positive representatives in the prescribed class. The infinite binary series has image $[0,3]$, since this interval is the union of $\rho^{-1}[0,3]$ and $1+\rho^{-1}[0,3]$. Finite approximations to any chosen tail therefore prove density throughout the displayed interval. The reverse inclusion follows directly from the fixed initial carries.

Consequently larger counter size does not reduce the uncertainty left by a fixed congruence class. No eventually periodic correction, or correction tending to a limit on each of finitely many residue classes, can equal $g$. This excludes exact bulk normalization by a finite residue lookup. It does not exclude increasing precision, aggregate carry counts, or a compressed invariant retaining the linked phase information. The positive certificates above use those distinctions.

Run `python3 bulk_carry_758.py` for focused exact-arithmetic checks. The verifier compares certified passages with the original ungrouped counter rules, including first-return timing, output intervals and parity; it also checks finite carry congruences, rational enclosures and the jump comparison. These checks audit the formulas. The quantified claims for all run lengths and all moduli follow from the proofs above, without enumerating their fine histories. No entry of the blank trajectory into a closed family of such passages is claimed here.
