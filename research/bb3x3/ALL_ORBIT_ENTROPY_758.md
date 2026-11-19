# Word entropy on every infinite #758 orbit

**Every infinite blank-compatible counter orbit has fine word entropy at least $(\log 3)/4$.** This includes orbits with infinitely many resets or exceptional restarts. If ordinary stretches become negligible compared with their starting mass, the stronger conclusion holds that **every finite word in the five-letter fine alphabet occurs on that one orbit, infinitely often**. This is a necessary condition for infinite continuation. The blank machine still requires a halting or nonhalting proof.

Use the grouped ordinary blocks from the [factor-complexity proof](FACTOR_COMPLEXITY_758.md). $J$ is one odd/odd jump and $P$ is a pair of ordinary bulk moves. The fine alphabet distinguishes the four input residues of $P$. Count factors within ordinary stretches, cutting at resets and exceptional moves. Incomplete pairs at the ends can be discarded. Write $p_f(n)$ and $p_c(n)$ for the numbers of distinct length-$n$ fine and coarse factors in the entire trajectory. Entropies use natural logarithms and divide by the number of grouped blocks. When there are arbitrarily long ordinary stretches, $p(n+m)\le p(n)p(m)$ gives the existence of $\lim_n\log p(n)/n$. The proof below supplies such stretches in both cases.

## Ordinary intervals with length comparable to mass

In odd/odd coordinates put $u=(a+2c-1)/2$. Suppose there are ordinary intervals at arbitrarily high starting $u$ containing at least $\varepsilon u$ complete blocks for one fixed $\varepsilon>0$. This includes an infinite final ordinary excursion. Select $T=\lfloor\varepsilon u/2\rfloor$ starting positions. Take $n=\lceil\log_3(10T U)\rceil$, where $U=u+9\lceil\varepsilon u\rceil$. For all sufficiently large $u$, the first $T+n$ blocks fit in the interval and their mass coordinates do not exceed $U$.

The determinant and repeated-edge theorem gives $p_f(n+1)\ge\sqrt{T+1}-1$. A smaller count would force a periodic ordinary tail, which the global denominator bound and finite sweep exclude at every mass. Since $U=O(T)$ and $n=2\log_3 T+O(1)$, taking logarithms proves the fine entropy lower bound. It suffices to apply this along the selected unbounded sequence because the entropy limit exists. [Determinant theorem](FACTOR_COMPLEXITY_758.md) · [Exclusion of periodic tails](FINITE_AFFINE_PERIODS_758.md)

## Exceptional moves cannot hide all resets

In the other case, for every $\varepsilon>0$, every ordinary interval at sufficiently high starting mass $u$ has fewer than $\varepsilon u$ complete blocks. We first show that on infinitely many scales resets then occur in **every fixed open subinterval** of $1<s/3^m<251/250$, where $A(1,s)$ denotes a reset.

Use raw counter mass $W=a+2c$. Rule $E$ at $A(c+2,c)$, $c\equiv3\pmod4$, gives $A(W+6,1)$. Define

$$
r_0=1,\quad D_0=0,\qquad q_i=\left\lfloor(r_i+1)/4\right\rfloor,\qquad
r_{i+1}=6q_i+5,\quad D_{i+1}=D_i+4q_i+3.
$$

If $i$ is odd and $D_i\le W+6\le D_i+r_i$, that $E$ is followed by $i$ legal bulk moves and an even-left return. Indeed the post-$E$ left counter covers the sum of the required decrements. At the end it lies in $[0,r_i]$ and is even. Hence there is a reset within $i+2$ calls of the $E$ input, including the exceptional call. [Exceptional annulus calculation](CUT_758.md)

Write $b=3/2$. The exact right updates are $r_{i+1}=br_i+7/2$ or $br_i+13/2$. The convergent series for $r_i/b^i$ gives a constant $K>0$ with $r_i=Kb^i+O(1)$. Since $D_{i+1}-D_i$ differs from $r_i$ by two or four, $D_i=2Kb^i+O(i)$. In particular $(D_i+r_i)/D_i\to3/2$.

There are infinitely many integer $m$ with an odd $i$ for which

$$
6/5 < 2\cdot3^m/D_i < 5/4.
$$

To see this, the logarithms of $2Kb^{2j+1}$ lie on an arithmetic progression of spacing $2\log b$. The rotation by $\log3/(2\log b)$ is irrational, since equality of nonzero powers of $3$ and $(3/2)^2$ would contradict prime factorization. A rotation into a smaller open interval strictly between the displayed bounds therefore occurs infinitely often. Replacing $2Kb^{2j+1}$ by $D_{2j+1}$ preserves these strict bounds eventually. The favorable exponents can be restricted to any prescribed arithmetic progression, because a nonzero integer multiple of the same rotation is still irrational. On these scales the entire mass range $2\cdot3^m\le W\le 2(251/250)3^m+1$ is inside the odd-$i$ annulus with room on both sides. Also $i=O(m)$.

Fix any open subinterval of the cusp in reset units $s/3^m$. An infinite orbit must cross the corresponding mass interval because every live update adds between three and nine to $W$. If the interval contains no reset, its middle half cannot contain $E$ at sufficiently large favorable scales. Such an $E$ would produce a reset after $O(m)$ calls and $O(m)$ mass growth, still in the interval. Consequently its middle half would be traversed entirely by ordinary moves. After alignment this supplies $\Omega(3^m)$ complete blocks at starting mass $\Theta(3^m)$, contradicting the present case. Therefore every fixed open subinterval contains a reset on all sufficiently large favorable scales. The sufficient scale may depend on the subinterval.

## A cusp that realizes every coarse word

Write $h=(a+1)/2$ and $x=h/u$ at odd/odd phases. Away from guard boundaries, the limiting normalized updates are

| Domain of $x$ | Actual action at sufficiently large mass | Limit of the next odd-phase direction |
|---|---|---|
| $0<x<1/3$ | $J$ | $3x$ |
| $5/9<x<1$ | $P$ | $(9x-5)/4$ |
| $1/3<x<5/9$ | one bulk followed by an even-left return | reset |

The guards in the last two rows follow by testing the first bulk and then its successor. The first bulk guard has leading difference $3h-u$. At its successor the bulk guard has leading difference $(9h-5u)/2$. Errors in these comparisons are bounded independently of the input. For $P$ the exact update has $u'=u+v$, $h'=(9h-5u-e)/4$ for bounded integers $v,e$. For $J$ it is $u'=u+2$, $h'=3h$. Thus every fixed finite word with strict limiting guards is legal uniformly on a sufficiently small closed neighborhood of its initial direction for all sufficiently large masses. This follows by induction over the fixed word and holds for every allowed bulk residue. [Exact coordinates](RESET_WORDS_758.md)

Let $w$ be any finite coarse word. Start its normalized terminal direction at $1/2$. Invert the word $P^7 w$ in reverse order using

$$
f_J(x)=x/3,\qquad f_P(x)=(4x+5)/9.
$$

Both inverse branches send $(0,1)$ into the strict interiors of the corresponding guards. The resulting initial direction $x_*$ satisfies $1-(4/9)^7<x_*<1$. In particular $t_*=1/x_*$ belongs to $(1,251/250)$, since $1/(1-(4/9)^7)<251/250$. The same word is legal on an open interval around $t_*$ when the initial direction is $1/t$.

For an odd reset $s$ with $t=s/3^m$ in a smaller closed interval around $t_*$, the first $m$ jumps give $u=s+2m$, $h=3^m$. Their legality follows from positivity of the last right counter $s-3^m+1+2m$. The resulting direction converges uniformly to $1/t$. The real guards therefore give the desired exact $P^7w$ at large scales, with all interior coordinates large enough to exclude an earlier reset.

An even reset in the same neighborhood does not obstruct the construction. The initial even-entry move followed by $m-1$ jumps gives $u=s+2m+2$ and $h=2\cdot3^{m-1}$, with positive final right counter. The limiting direction is $2/(3t)$. Throughout $1\le t\le251/250$ the successive normalized actions are $P,J,P$, followed by a single bulk and a return. At $t=1$ the four directions are $2/3,1/4,3/4,7/16$. The verifier checks the strict inequalities at both ends of the interval, which suffice by affinity in $1/t$. The five bulk moves each add one to the left counter modulo four. Jumps preserve an odd left counter modulo four. The counter started at three after the even-entry move, so it is divisible by four at the return. The new reset is **odd**, and its increase in $s$ is at most $2m+29$ by the mass increments. This is negligible compared with $3^m$.

Finally take two nested neighborhoods around $t_*$ with positive clearance. A reset exists in the smaller one on all sufficiently large favorable scales by the preceding argument. An odd reset launches the word directly. An even reset produces an odd reset still inside the larger neighborhood. In either case the actual orbit contains $w$. This applies to each fixed finite $w$ on infinitely many increasing scales. Hence $p_c(n)=2^n$ for every $n$, and the fine entropy is at least $\log2$ in this case. No distributional assumption on the orbit is used.

## Forcing all five fine letters

The entry construction can also force many different choices of the bulk residues on the same trajectory. Fix a length-$n$ coarse word $w$ with $j$ jumps and $p$ pairs. Choose $\epsilon\in\{0,1\}$ so $k=7+p+\epsilon$ is odd. Repeat the inverse-branch construction for $P^7wP^\epsilon$, this time starting from the terminal direction $4/9$. This terminal direction is strictly in the one-bulk return interval $(1/3,5/9)$. The resulting open relative corridor has the complete odd return word

$$ J^m P^7 w P^\epsilon L R . $$

There are $2k+1$ ordinary bulk moves. The left counter is 1 modulo four after $J^m$, and the remaining jumps preserve an odd left counter modulo four. At $R$ the left counter is $1+(2k+1)=0$ modulo four because $k$ is odd. Therefore every odd seed in this corridor returns to an odd seed. If $s=2z+1$, the mass gain gives

$$ z'-z=m+j+5(k+1)/2+B,\qquad 0\le B\le 2k+1 . $$

Here $B$ counts individual bulk moves whose input right counter is 3 modulo four. Fix $M=4^k$ and request favorable scales with $m\equiv 1-j-5(k+1)/2\pmod M$. The least nonnegative residue of each increment $z'-z$ is then between 1 and $2k+2<M$.

Start at a reset in a smaller interval strictly inside this corridor. The preceding density proof provides one on every sufficiently large favorable scale in this congruence class. An even entry first returns to an odd seed with a negligible change in relative position. From there the next $M+1$ odd starts all stay in the corridor for sufficiently large $m$, because $M$ is fixed and each return advances $s$ by $O(m+k)$. Their residues $z\bmod M$ take at least $M/(2k+2)$ distinct values. Indeed the segment up to the first repeated residue contains a cycle with distinct starting residues, and the sum of its positive residue increments is a positive multiple of $M$. This counting argument needs no deterministic transition on the residues alone.

Two starts with the same ordered list of the $k$ fine pair labels must have the same $z\bmod M$. To verify this, write $d=(c-1)/2$ at the odd/odd phases. Immediately after the leading jumps, the differences between two starts with $z$-difference $\delta$ are $\Delta u=2\delta$ and $\Delta d=\delta$. A common fine path keeps $\Delta u=2\delta$. After $i$ pairs, $\Delta d=A\delta/4^i$ with $A$ odd. A jump replaces $A$ by $3A-2\cdot4^i$, and a common fine pair multiplies $A$ by nine and the denominator by four. Integrality at the end forces $4^k\mid\delta$. These are the exact fine updates from the [ordinary-excursion calculation](EXCURSION_POWERS_758.md).

At most $4^{7+\epsilon}$ different lists give the same fine labeling of the middle $w$. Thus at least $4^p/(2k+2)$ of its fine labelings occur. The argument works beyond any fixed time. Summing over all length-$n$ coarse words gives

$$p_f(n)\ \ge\ \frac{1}{2n+18}\sum_{p=0}^{n}\binom np4^p
=\frac{5^n}{2n+18}.$$

Hence the fine entropy in this case is $\log5$. In fact every fine word occurs in every infinite tail. If one length-$\ell$ word were absent, disjoint aligned blocks of length $\ell$ could take at most $5^\ell-1$ values each, giving an entropy at most $\log(5^\ell-1)/\ell<\log5$. This contradicts the same lower bound on that tail.

## Where long ordinary stretches must recur if a word is missing

Suppose a fixed length-$\ell$ fine word is absent from an infinite tail. Choose $n$ large enough that $5^{\ell-1}(5^\ell-1)^{\lfloor n/\ell\rfloor}<5^n/(2n+18)$. The preceding count implies there is a particular coarse word $w$ with fewer than $4^p/(2k+2)$ fine labelings on this tail. For this $w$, take its inner reset interval and the arithmetic progression of exponents prescribed above. At any sufficiently large favorable exponent in that progression, even one reset in the inner interval would produce at least $4^p/(2k+2)$ fine labelings of $w$ on the same tail. There is therefore no reset anywhere in that interval at those exponents. The odd exceptional annulus forces its middle half to consist entirely of ordinary moves. Hence there is a fixed $c>0$ and an ordinary stretch of at least $c u$ blocks there, with starting $u$ of order $3^m$.

These favorable exponents have bounded gaps. An irrational rotation returns to any open arc with bounded gaps, since finitely many inverse translates of the arc cover the circle by compactness. Apply this to a smaller arc inside the strict annulus window, on the prescribed arithmetic progression. The $O(i)$ annulus error preserves the result at all sufficiently large exponents. Thus the missing word forces long ordinary stretches to recur with bounded ratios between their successive mass scales.

## Reproduction

The checker tests the rational cusp bounds, replays all $2^{10}$ ten-block words from both entry parities at $m=96$, checks the first and last eligible exceptional masses in odd-index annuli through index 189, and exhausts the modular fine labels for a seven-pair return template. The uniform statements for arbitrary lengths and infinitely many scales follow from the arguments above. [Exact checker](check_all_orbit_entropy_758.py)

```sh
python3 check_all_orbit_entropy_758.py
```
