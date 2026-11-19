# Synchronized ordinary returns beyond the secondary-cusp edges

For 364 of the [368 primary bulk corridors](SECONDARY_CUSP_758.md), every seed in the corridor reaches a new, explicit reset **81,564,441 to 107,988,950 seeds beyond that corridor’s upper edge**. These paths start at the [previously proved gate mergers](CHECKPOINT_Y_758.md). On all 364 paths the next certified interval has exactly the same lower and upper offsets from its respective edge. The four omitted corridors are the ones closest to $Y$; they already belong to the connected chain starting at $Y$. The calculation does not connect the distant gates to one another or establish blank entry into them. [364 exact transfers](y_edge_bands_758.tsv)

More generally, let $E_k$ be the first excluded odd seed at the upper edge of the primary corridor with $k$ final bulks. At odd inputs $E_k+z$ in any certified secondary interval, the first-return word is
$$
J^{292}L^8J\, L^{k-1}J L^{N-k+1}R .
$$
At fixed edge offset $z$, the sufficient interval for the odd total $N$ is the same at every $k$ where the collar below applies. The construction gives **72,680 disjoint intervals** in the gaps of the primary catalog. These contribute another **23.66550811%** of the integer positions from $Y$ to $H$. The two catalogs together cover **63.65467577%** with the specified classes of quick first returns. These fractions count reset positions and give no probability for the actual blank orbit. [Integer checker](y_edge_bands_758.py)

## Why the two long bulk counts add to nearly the same number

Write $\rho=3/2$, $n=k-1$, $W=a+2c$. Consider offsets $64\le z\le Y/(320\rho^n)-8$, truncated at the end of the gap. Odd seeds just after $J^{292}L^8J$ have $W=2s+2g+1$ with $606\le g\le622$. Across two such seeds separated by $z$, the [header identity](SECONDARY_CUSP_758.md) gives
$$
\left|\Delta c-\frac{19171}{256}z\right|<412,\qquad |\Delta W-2z|\le32 .
$$
One bulk sends $c$ to $\rho c+e$, with $e=7/2$ or $13/2$. It adds five or nine to $W$. After $n$ formal bulks the accumulated right-coordinate difference differs from $\rho^n\Delta c$ by at most $6(\rho^n-1)$, and the mass-difference error increases by at most $4n$.

At $E_k-2$ the $k$th bulk is legal; hence after the first $n$ bulks $c-a+1\le-1$. At $E_k$ the proposed $k$th bulk would give a negative left counter, so $c-a+1\ge-1$. The proposed jump after $n$ bulks sends the right counter to $c_J=c-a+1=3c-W+1$. Comparing with $E_k$ on the lower side and $E_k-2$ on the upper side gives
$$
\rho^n(224z-2000) \le c_J \le \rho^n(225z+2000)-13 .
$$
For instance $n\ge6$, $(4n+15)/\rho^n<4$ and $2/\rho^n<0.18$. The constants allow the two-seed displacement on the upper side. To justify the proposed first $n$ bulks, at $E_k-2$ we have $c_n\le(2H+8000)/3$. Increasing the seed to $E_k+z$ increases this by at most $\rho^n80(z+8)\le Y/4$. Since $W\ge2Y$ and $H<1.002Y$, the remaining left counter exceeds one. Every earlier proposed bulk is therefore legal. The lower bound on $c_J$ proves the jump guard.

If the next maximal run has $j$ bulks, then at its end $(W_j-4)/3<c_j\le W_j/2$. The lower bound follows since another bulk is illegal, and the upper bound follows from the nonnegative left counter. We have $j<800$, since even the minimum right-coordinate growth in 800 moves would exceed the available mass. Thus $2Y<W_j<2H+20,000$. The exact bulk update bounds $c_j$ between $\rho^j(c_J+7)-7$ and $\rho^j(c_J+13)-13$. Consequently $\rho^{n+j}$ lies between
$$
\frac{2Y-4}{3(225z+2000)}
\quad\hbox{and}\quad
\frac{2H+20,000}{2(224z-2000)} .
$$
At $z=64$, and hence at every larger offset, the ratio between these bounds is strictly less than $\rho^2$. At most **two consecutive values** of $n+j$ are possible across all admissible edges at that offset.

For a guaranteed return pick an odd $N\ge k$. Take all offsets in the collar satisfying
$$
 3\rho^N(224z-2000)\ge 2H+20,000,\qquad
 2\rho^N(225z+2000)\le 2Y-4 .
$$
After $j=N-k+1$ proposed bulks the left counter is then greater than one and no larger than the right. Because $j$ is odd, this is a legal ordinary return. Every intermediate bulk was legal because the final left counter remained positive. Even reset seeds have their known 300-call return. The verifier also checks the full physical word at both odd endpoints of every interval, using integer arithmetic. The monotone counter order certifies every odd input between those endpoints.

## The 364 connected transfers

For $N=733$ the common inclusive band is $53,719,288\le z\le80,126,735$ at $k=7,9,\ldots,733$. From each previous exact merger, iterate to the first entry in this interval. All 364 paths enter, taking **6,922,475** individual first returns in total. Inside the band every odd input has the displayed word with 741 individual bulks, 294 jumps and a reset. Its seed gain is at most $(9\cdot741+4\cdot294+5)/2=3925$; even inputs gain at most 615. All possible first exits therefore come from the final 3,925 positions. Across these bands there are 282,439 possible exits, and 6,470,604 further distinct first-return edges in their per-band merger calculations. Each band gives one new exact reset. The [receipts](y_edge_bands_758.tsv) list $k$, first actual entrance from the old merger, number of returns to the entrance, possible exits, merger edges, and final checkpoint. Entrance and checkpoint are recorded as offsets from $E_k$.

## Relative slopes for deeper branches

The edge estimate has a version independent of the number of interruptions. For two odd header seeds $z\ge0$ apart following the same ordinary word of $b$ bulks and $j$ jumps, put $M=\rho^b3^j$. Then
$$
(19171/256-1)z-450
\ \le\ \Delta c_{\rm end}/M
\ \le\ (19171/256)z+450 .
$$
For a bulk the variation in its additive right-coordinate correction is at most three. A jump acts on the right coordinate by $3c-W+1$ and subtracts the current mass difference after rescaling. After $i$ updates this difference lies within $32+4i$ of $2z$. If $M_{i+1}$ is the prefix multiplier including update $i$, then $\sum 1/M_{i+1}\le2$, $\sum i/M_{i+1}\le4$ and the sum of $1/M_{i+1}$ over jumps alone is at most $1/2$. Together with the header error of 412 these bounds give $412+6+16+16=450$. This permits recentering a further mixed-word edge using its own exact guard change.

Run in the BB(3,3) research directory.

```sh
python3 y_edge_bands_758.py
c++ -O3 -std=c++17 checkpoint_y_758.cpp -lgmpxx -lgmp -o /tmp/checkpoint_y
python3 y_edge_bands_758.py --merger-input | /tmp/checkpoint_y --edge-bands > /tmp/edge-bands.tsv
cmp y_edge_bands_758.tsv /tmp/edge-bands.tsv
```
