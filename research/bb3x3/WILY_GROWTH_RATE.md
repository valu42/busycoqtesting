# Sublinear Wily growth and the frequency of the two stopping directions

On every infinite physical Wily trajectory with scalar driver $F=s_0$, new suffix cells are allocated on a set of sweeps of density zero. In fact, uniformly over starting times $u$,

$$
\lim_{N\to\infty}\sup_{u\ge0}\frac{w_{u+N}-w_u}{N}=0,
$$

where $w_t$ counts the allocated cells of the scalar suffix after $t$ updates. Ordinary stops have two directions in the integer lift defined below. Each direction occupies asymptotic frequency $1/2$, also uniformly over $u$. The conclusions allow mode-0 corrections. If the actual blank runs forever, its scalar suffix therefore grows unboundedly and sublinearly, by the [blank growth argument](WILY_BIRTH_SHADOW.md). The growth rate theorem is conditional on survival.

## An infinite growing trajectory has an aperiodic shadow

For each physical time $t$, let $v_t$ be the allocated word. The [shadow construction](WILY_BIRTH_SHADOW.md) gives an infinite binary ray $x$ such that $v_t$ is a prefix of $F^t(x)$ at every time. One can also see existence directly. Pull the cylinder of rays beginning with $v_t$ back by $F^t$. These nonempty closed cylinders are nested: the inverse image of the written prefix at the next sweep determines the previous input prefix by invertibility of the bit rules. Compactness gives a common ray. When $w_t$ is unbounded this ray is unique.

Suppose this shadow has period $p$. If every sweep in its period stops, all their stops have a common finite depth bound. Otherwise consider any singular phase, a sweep that never stops on its infinite input. Its next singular phase exists by periodicity. Above the deepest stop of the finitely many intervening sweeps the two singular carries act successively on the same columns. The [two-carry graph](WILY_TAIL_GERMS.md) forces one of the following two behaviors at all sufficiently high columns:

| High input of the first singular sweep | First active carry | First written bit |
|---|---|---|
| Constant zeros | 2 on 0 | 0 |
| Alternating | 0 on 0 or 1 on 1 | 1 or 0, respectively |

There are finitely many phases, so choose one cutoff above all such transients and regular stops. A physical birth at any greater width is impossible on this shadow. Mode 2 allocates a word beginning in 1, whereas the zero-tail shadow writes 0. Mode 0 allocates a word beginning in 0, whereas the alternating shadow writes 1. A physical mode 1 ends the trajectory. Thus periodic shadows cannot support unbounded physical growth.

## Visits to the edge have zero density, uniformly in time

On an infinite shadow orbit of the tree automorphism $F$, let $p_k$ be the period of its first $k$ bits. These periods divide each other and tend to infinity: bounded periods would make the whole ray periodic. Uniform probability on each of these finite cycles is consistent under truncation, so it defines an invariant probability $\mu$ on their inverse limit, the orbit closure. A point has mass at most $1/p_k$ for every $k$, hence $\mu$ has no atoms.

Let $S_k$ be the set of rays whose scalar sweep still has an active carry after processing $k$ bits. These are decreasing sets of finite prefixes. Their intersection $S$ is the singular set. If $y\in S$ and $F^j(y)\in S$ for some $j>0$, apply the two-carry graph to the first two singular sweeps in this finite interval. Above all intervening stops, their input to the first sweep must be eventually zero or eventually alternating. There are countably many such $y$. Consequently the sets $F^{-j}(S)$, $j\ge0$, have pairwise $\mu$-null intersections and all have the same measure. Since $\mu$ has total mass one, $\mu(S)=0$. Continuity from above gives $\mu(S_k)\to0$.

For fixed $k$, the indicator of $S_k$ along the shadow repeats every $p_k$ updates. Its average on any interval of length $N$ differs from $\mu(S_k)$ by at most $p_k/N$. Once the physical width reaches $k$, every birth lies in $S_k$. The finitely many earlier times contribute at most a constant divided by $N$, uniformly over interval starts. First send $N$ to infinity, then $k$ to infinity. This proves that the upper density of births in length-$N$ intervals tends to zero. Each birth adds at most four cells, proving the asserted width estimate. A bounded-width trajectory makes only finitely many births, so it satisfies the same estimate.

## Exact signed increments, including physical corrections

Associate integer isometries $X(z)=z-1$ and $Y(z)=1-z$ to the digits 0 and 1. Let $D(v)$ be their product in head-facing order, with the right factor acting first. Use $W(v)=-D(v)(1)$ and

$$
V_t=(-1)^t\bigl(W(v_t)+\tfrac12\bigr).
$$

This $W$ is the [alternating zero-gap height](WILY_GAP_MAP.md) of the physical word with virtual continuation $(10)^\omega$. Indeed each block $0^r1$ acts as $1-r-z$. The pure unit-gap continuation fixes zero and prefixing one initial 1 gives the continuation $(10)^\omega$ value one. Also $|W(v)|\le |v|+1$.

Give carries 0, 1, 2, 3 the respective maps $1-z,z-1,z+1,-z$. On each bit the incoming carry followed in the product by the input digit equals the written digit followed by the outgoing carry, with one exception. Mode 1 reading 0 gives the outgoing expression minus three. It sends mode 3 to the next cell, where the sweep stops if that cell exists. A sweep thus has at most one such discrepancy. Transporting it past an earlier written prefix multiplies its sign by the slope $\epsilon=\pm1$ of that prefix.

For an edge carry $e$, the residual discrepancy is $e(1)-D(\mathrm{extension})(1)$. It equals zero for mode 0 allocating 0, three for mode 2 allocating 1100, and zero for mode 3 allocating 00. Thus on every internally stopping sweep at time $t$,

$$
 V_{t+1}-V_t=3(-1)^t\epsilon,
$$

where the prefix for $\epsilon$ ends just before the unique mode-1-on-0 transition. A mode-3 birth has the same formula. A mode-2 birth has an increment of magnitude three with the slope taken over the whole written old prefix, and opposite sign. A mode-0 correction has increment exactly zero. These formulas follow by applying the telescoped product identity to the value one. They distinguish the two time-normalized directions; the unsigned recursion-depth parity in the gap table has an additional time-parity factor.

Since the width is $o(t)$, so is $V_t$. Summing its increments and discarding the zero-density births shows that each of the two internal directions occupies half of all times from the start. To obtain the uniform-in-$u$ assertion, use the same height on just the first $k$ bits of the shadow. Its magnitude is at most $k+3/2$. If the carry has stopped by depth $k$, its normalized increment exactly equals the increment on the physical internally stopping sweep, once the physical width is at least $k$. Otherwise its increment has magnitude at most five: the single possible bit discrepancy contributes at most three, and the unresolved carry can change the terminal value one by at most two. Comparing the truncated increments to $+3,-3$ on the two physical internal directions and zero on births costs at most eight per visit to $S_k$. The discrepancy between the counts of the two directions on any interval, divided by its length, therefore tends to zero by the preceding periodic-frequency estimate. For bounded width, there are finitely many births and $V_t$ itself is uniformly bounded. This also gives the uniform conclusion in that case.

Run `python3 wily_growth_rate.py` to check the local integer identities, the periodic-shadow incompatibility and the exact physical height steps on all words of width at most twelve.
