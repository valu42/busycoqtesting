# A growth deadline from ten occupied bits of #397

Let S be the periodic sequence of 33 carries emitted every 1,024 sweeps by the first 29 suffix bits, starting after sweep 64 on the blank trajectory. A cut at depth k lies beyond those 29 bits and k more occupied bits. For every k ≥ 18, **every window of 2^(k−10) full copies of S has at least one event leaving the k-bit cut**, from every starting word of length k. Hence a physical edge at depth k must grow or halt within this window. This improves the previous bound of 2^k copies by a factor of 1,024. The odd-k bound already applies for k ≥ 13.

Place a second cut at d = k−10. During any 2^d full copies of S, the input multiplicities at this cut follow the [transitive-section theorem](TRANSITIVE_SECTION_397.md). Let u be the ten bits immediately beyond this cut. One incoming carry m updates u to v. Call it silent when it stops within those ten bits and a contact when it reaches their far edge. The following rows give integer weights on the six incoming carries in alphabetical order.

| Upstream depth d | Weights for a,b,c,d,e,f | Total incoming weight G in the window | Maximum contact defect D |
|---|---|---:|---:|
| d = 2j+1, j ≥ 0 | 1, −7, −15, 2, −8, −8 | 25·3^j | 32 |
| d = 2j+2, j ≥ 0 | −29, −1, 3, −12, 2, 2 | 3·3^j | 33 |

For each row the [finite certificate checker](contact_deadline_397.py) constructs an integer potential V on all 1,024 ten-bit words in the interval [0,31]. It initializes V to zero, repeatedly replaces V(v) with max(V(v), V(u)+weight(m)) on every silent transition, then directly checks all of the inequalities. On every contact transition the checker also verifies weight(m)+V(u)−V(v) ≤ D by computing the maximum over all such transitions.

If N contacts occur, summing the inequalities along the actual ten-bit trajectory gives G ≤ V(final)−V(initial) + DN ≤ 31 + DN. In particular N ≥ ceil((G−31)/D). The multiplicities and hence G hold for every starting d-bit prefix and any complete window of 2^d copies of S. For odd d ≥ 3 or even d ≥ 8, G > 31, giving the asserted deadline. This argument holds on a fixed occupied prefix irrespective of the bits beyond it. On the physical tape, absence of both growth and halt throughout such a window would leave the prefix fixed in length and give N = 0.

From the empty tail at sweep 64, two copies of S occupy exactly 18 bits. Thus for every n ≥ 18, by sweep

    64 + 1,024 · (2 + 2^(n−10) − 256)

the machine has halted or has at least 29+n suffix bits. Induct on n. If the length at the preceding deadline is exactly n, the next window of 2^(n−10) copies forces halt or growth. A larger starting length already meets the next deadline.

The bound controls the arrival of an edge event. Its label can still be either a growing or a halting carry. Run `python3 contact_deadline_397.py` in this directory to verify the finite certificates.

## A uniform upper bound on growth in any finite window

For any $N\ge1$ consecutive 1,024-sweep periods completed after sweep 64, the tail can gain at most $O(N^{\log_2\sqrt 3})$ bits, uniformly in its starting width and time. The exponent is approximately 0.79248. This is a bound on finite surviving segments, irrespective of their eventual outcome.

Set $k=\lceil\log_2 N\rceil$. In one full cycle of $2^k$ periods, the exact number $T_k$ of arrivals at a fixed $k$-bit cut is the sum of its [six carry counts](TRANSITIVE_SECTION_397.md):

$$
T_0=33,\qquad T_{2m+1}=46\cdot3^m,\qquad T_{2m+2}=90\cdot3^m\quad(m\ge0).
$$

This holds for any initial $k$ bits. It also holds if the window begins at another phase of the 1,024 sweeps: the cyclically rotated return is conjugate to the original one by the intervening prefix permutation. Each of the 33 source occurrences still sees every $k$-bit input once in its full cycle.

If the initial width is smaller than $k$, the total increase through the first birth reaching or overshooting $k$ is at most $k+3$, since the largest extension adds four cells. The same bound covers the case where width $k$ is never reached. Every subsequent birth requires a distinct arrival at this cut. The corresponding fixed $k$-bit trajectory extends backwards to the start of the window by invertibility, so it sees at most $T_k$ arrivals across its remaining fraction of at most $2^k$ periods. If the initial width already exceeds or equals $k$, this last argument applies from the start. Hence the width increase is at most $k+3+4T_k$. Since $T_k=O((\sqrt3)^k)$, this proves the claim. Run `python3 transitive_section_397.py` to reproduce the fixed-cut counts through twenty bits and check the traffic directly over complete cycles through ten bits.
