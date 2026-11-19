# Raw running time near the large halting target

Let $A(1,H-d)$ be a reset in the last 3,403,055 seeds up to the known halting target $H$. The table gives the **remaining original Turing-machine transitions** from that reset. Each value is rounded to the displayed precision. The extrema are over every seed with the stated outcome. The [boundary proof](AFTER_TARGET_758.md) defines $H$ and the later reset $C$. Entry into this region from the blank tape remains open.

| Outcome | Starts | Shortest remaining time | Longest remaining time | Distances $d$ at shortest and longest |
|---|---:|---:|---:|---|
| Halt via $A(1,H)$ | 2,238,030 | $2.7925579742\times10^{279}$ | $1.2542062293\times10^{283}$ | 0 and 3,402,774 |
| Halt via $A(1,H-2)$ | 2,511 | $2.7925579742\times10^{279}$ | $1.9596063596\times10^{281}$ | 2 and 52,583 |
| Cross $H$ alive and reach $C$ | 1,162,514 | $5.2067023075\times10^{412}$ | $5.2067023075\times10^{412}$ | 288 and 3,403,054 |

The two extrema in the last row agree in their first **129 significant digits**. The relative spread is about $2.417\times10^{-130}$. This is elapsed time to the first visit to $C$. The future of $C$ is open. Starting deeper in the proved halting basin at $A(1,H-12{,}000{,}000)$, the machine takes $4.5300961671\times10^{283}$ transitions to halt, including 11,352 completed first returns and one terminal excursion. At $A(1,H-3{,}403{,}055)$ it takes $1.2527657029\times10^{283}$ transitions.

## Exact clocks

A first return sums the [raw branch costs](timing_758.py). For $k$ consecutive odd/odd jumps, set $u=a+1$, $W=a+2c$ at entry. The successive left counters and masses are $3^i u-1$ and $W+4i$, so summing the raw costs $3a_i^2+5c_i+6$ gives

$$
2T_k=6u^2\frac{9^k-1}{8}-17u\frac{3^k-1}{2}
  +k(23+5W)+10k(k-1).
$$

All 346 possible first resets above $H$ lie in the fixed-word corridor ending at $E$. The two parity words have at most thirteen bulk moves. Translation by $M=2^{14}$ preserves the low bits used to choose each fine branch. Within any single seed residue modulo $M$, every counter along its word is affine in the period index, by the [translation argument](RETURN_PREFIX_758.md). The first-return gain therefore stays constant and its raw time is a polynomial of degree at most two. Three evaluations determine the polynomial and the checker verifies a fourth. The [endpoint proof](AFTER_TARGET_758.md) certifies that the words hold through the whole corridor.

Iterate the seed residues until a residue repeats. One complete cycle has a positive stride divisible by $M$. Costs for successive copies of this cycle again form a degree-at-most-two polynomial, because every intermediate seed shifts by the same stride. If the first three costs are $a,b,c$, the sum over $n$ copies is $na+\binom{n}{2}(b-a)+\binom{n}{3}(c-2b+a)$. Each skipped cycle lies entirely within the verified corridor. After the final partial cycle the checker evaluates every actual return through $C$ using the counter rules. Of the 346 possible overshoots just above $H$, the shortest remaining clock to $C$ starts at $H+906$ and the longest at $H+62$. Their paths use 30 distinct exits above $E$.

For the full table, process $d=0,1,\ldots,3{,}403{,}054$. A terminal first excursion supplies its own clock. Otherwise add the first-return cost to the known clock from the next reset. The largest continuing seed increment is 1,409 throughout the region, so a rolling table suffices. The checker verifies the three outcome counts and prints the exact integer extrema and their starting distances.

Run the [checker](target_clock_758.py) from the BB(3,3) directory with Python 3.10 or later. The default computes the endpoint clocks and the 346 overshoot clocks. The second command computes the full table.

~~~sh
python3 target_clock_758.py
python3 target_clock_758.py --boundary
~~~
