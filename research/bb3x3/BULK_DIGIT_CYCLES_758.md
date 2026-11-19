# A 1,606,408-return cycle on the blank path and a digit-compression obstruction

In the first window above the power-35 gate, #758 and #153 execute at least **1,093 consecutive copies of one residue cycle**. Each copy takes exactly **1,606,408 first returns** and advances the reset seed by **268,435,456**. The resulting flight has exact endpoints $A(1,50{,}032{,}132{,}179{,}190{,}025)$ and $A(1,50{,}032{,}425{,}579{,}143{,}433)$, and costs **15,968,388,026,771,997,073,986,594,690,949,338,871,473,882 raw transitions**. The lifted seed increases each time, so repeated residue states describe progress through a finite corridor. The result requires 24,576 half-word lookup entries and visits 1,631,454 quotient residues. At power 292, a physical first-return word gives an exponential lower bound on the number of states in one natural low-digit compression scheme. Whether a different scheme can compute arbitrary corridor exits in polynomial time remains open.

## The exact return map

Consider an odd launch with complete first-return word $J^mL^bR$. Each $J$ adds 4 to $W=a+2c$. Every $L$ adds 5 or 9, and $R$ adds 5. At the end of the jumps $c=s-3^m+2m+1$. In the coordinate $y=(c+7)/2$, an $L$ sends $y$ to $T(y)=3\lceil y/2\rceil$ and adds $5+4(y\bmod2)$ to $W$. Put
$$
F_b(y)=\sum_{i=0}^{b-1}2^i(T^i(y)\bmod2),\qquad B_b(y)=\operatorname{popcount}F_b(y).
$$
For $b=3\pmod4$, an odd seed returns to odd with gain $2m+5(b+1)/2+2B_b(y)$. The next launch coordinate is $S(y)=y+C+B_b(y)$, with $C=m+5(b+1)/4$. The seeds $2n-1$ and $2n$ in the $y$ coordinate have the same image under $S$, since $T$ merges the pair and the first flag differs by one. We can use $n=\lceil y/2\rceil$ and $Q(n)=\lceil S(2n)/2\rceil$ modulo $2^{b-1}$. This quotient still has genuine mergers and changes of order. For $b=7,m=35$ it has image size 45 out of 64 and $Q(15)=40>39=Q(16)$ on the integer lift.

For any $\ell\le b$, integer $q$, and $0\le r<2^\ell$, the exact block formula is
$$
T^\ell(2^\ell q+r)=3^\ell q+T^\ell(r),\qquad
B_b(2^\ell q+r)=B_\ell(r)+B_{b-\ell}(3^\ell q+T^\ell(r)).
$$
It follows by induction using $T(2q+r)=3q+T(r)$ for $r=0,1$. A split after 14 of 27 bits evaluates a reset increment with two lookups, one multiplication and one addition for the next block index. Computing $B_t$ only needs its argument modulo $2^t$.

## A full cycle realized from blank

The integer interval $50,032,132,174,230,649\le s\le50,032,425,717,012,734$ lies inside archived row 0 of the power-35 grid. In this interval every odd launch follows $J^{35}L^{27}R$, and each even launch follows $IJ^{34}L^2JL^3R$, arriving at an odd seed with gain at most 99. The checker verifies the two endpoints for each parity. The counter order within a fixed-parity word extends the endpoints to the whole interval. Equivalently the odd interval is obtained by trimming $20/3^{35}$ at both ends of the gap after 13 successive bulk pairs. The grid's interior-cut bound places a reset within 100,000 seed units of its entrance. Thus one of the first 50,051 odd seeds in the stated interval occurs on the blank path. [Blank window construction](double35_frontier_758.py) · [Counter order and interior-cut bound](BLANK_WORD_SPECTRUM_758.md)

The C++ checker starts its quotient graph search at every one of these odd seeds. Each previously unknown path ends in its own cycle or rejoins a path already covered. It finds one cycle, which takes 1,606,408 steps and advances the lifted $n$ by $2^{26}$. Across all paths only 25,046 vertices are off the cycle. One further return recovers the exact $y$ phase because $S(2n-1)=S(2n)$. Every odd return increases the seed by at most 194, so the remaining interval fits at least 1,093 full cycles. Each cycle advances $y$ by $2^{27}$ and the reset seed by $2^{28}$. The resulting exact skip covers **1,755,803,944 first returns** and **293,399,953,408 seed units**.

The winding-one cycle visits its residues in strictly increasing cyclic order on the lift. After the transient, the next physical reset at or above the safe cut $50,032,132,179,189,869$ therefore has a unique seed. Scanning the cycle phases gives the source $50,032,132,179,190,025$. Advancing that source by 1,093 strides gives the destination $50,032,425,579,143,433$, which still lies inside the corridor.

## Timing the billion-return flight

For successive cycle copies the two physical counters at a fixed edge depend affinely on the copy index. Every bulk branch is fixed by the starting $y$ residue modulo $2^{27}$, and every [raw branch clock](timing_758.py) is quadratic on that branch. Thus the whole cycle clock is quadratic. The first three literal timed cycles determine its initial value $15,679,425,115,476,133,945,105,303,627,540,336,820,502$, its first difference $-5,872,560,475,987,881,768,064,069,849,004,808,546$, and its second difference $10,760,770,080,039,614,645,256,564,425,562,624$. Summing these by binomial coefficients gives the displayed flight duration. A fourth literal timed cycle at index 1,092 verifies the prediction there. The Python checker also propagates the established blank-clock interval to the source and adds the exact duration for the destination. The #153 clock is 50,707 earlier at both ends.

## What the binary digits can compress

$F_b$ permutes $[0,2^b)$ modulo $2^b$. Toggling input bit $i$ preserves the first $i$ flags and toggles flag $i$, by the block formula and oddness of $3^i$. Consequently, on fixing the first $\ell$ input digits, the remaining flags realize every bit vector once. Their weight histogram is binomial and their total weight is $(b-\ell)2^{b-\ell-1}$ when $\ell<b$. The orbit visits a selected subset and can have a different weight histogram. The transform $F_b$ is nonlinear over the binary field even for $b=3$, where its first four values are $0,3,2,5$.

There is a quantitative obstruction to building a deterministic low-digits-first table that merges partial prefixes with identical weight functions on every higher continuation. The additive period of $B_t$ is exactly $2^t$: a translation by $2^{t-1}$ flips just the final flag, and every proper period on the cyclic domain would make this half-translation a period. Also
$$
(3/2)^\ell r\le T^\ell(r)\le(3/2)^\ell(r+3)-3
$$
by $3z/2\le T(z)\le3(z+1)/2$. Thus $T^\ell(r)$ for $r=0,4,8,\ldots,2^\ell-4$ are distinct. If $2^{b-\ell}>3^\ell+3(3/2)^\ell$, these carries are distinct even modulo $2^{b-\ell}$. The resulting high-continuation functions $q\mapsto B_{b-\ell}(3^\ell q+T^\ell(r))$ are pairwise distinct. Translation permutes the inputs, so equality up to an additive constant would require that constant to vanish, which contradicts the minimal period. There are at least $2^{\ell-2}$ states at this one decision layer, even for a table that emits a prefix weight along the way.

These parameters occur in physical reset states. For $m=292,b=255$, set $p=(b-1)/2$, $P=3^m$. Let $x=P/(s+2m)$. The middle gap after $p$ bulk pairs is $(1-(4/9)^p(2/3),1-(4/9)^p(4/9))$. Trimming $20/P$ from both ends gives the physical word by the guard comparison. The absolute derivative of $s$ with respect to $x$ is at least $P$, so the trimmed span is at least $2^b3^{m-b-1}-40$. This includes a full period of odd seeds. The checker also tests both odd endpoints literally. Taking $\ell=98$ requires at least **$2^{96}$** distinct continuation functions. Reachability of these target-scale states from blank is open. This lower bound concerns a decision diagram evaluating the weight from low digits. It leaves open algebraic methods for deriving a cycle or its entry and exit directly.

## Two necessary alternatives if blank reaches the target region

The same 255-bulk corridor lies wholly below the known halting seed $H$ and has seed span greater than $8.6898\times10^{93}$. On any blank trajectory that traverses its mass range, one of the following events occurs.

- A single excursion spans **more than $9.6\times10^{92}$ consecutive elementary calls without a reset**.
- One genuine residue cycle repeats **at least $8\times10^{13}$ times**, each copy containing **more than $6.6\times10^{73}$ first returns**.

To see this, split the seed interval at its integer midpoint. If its lower half contains no reset, then $W$ crosses the corresponding mass interval in increments of at most nine. Discarding the two edge increments leaves the stated bound on reset-free calls. Otherwise start at any reset in the lower half. Both even endpoints take $IJ^{291}L^2JL^3R$ and counter order extends the word across the interval. Its even seeds reach odd with gain at most 615. The odd word then stays closed with $C=612$. Every first return advances $y$ by at most 867 and the original seed by at most 1,734. The quotient has $2^{254}$ vertices, so at most that many returns find the eventual cycle, and at most that many further returns complete each copy. An extra return recovers the actual $y$ phase. These bounds fit more than $8\times10^{13}$ copies into the remaining half of the physical interval. The lifted $y$ must advance by a positive multiple of $2^{255}$ over each cycle, so its period is at least $\lceil2^{255}/867\rceil$. This excludes exhaustive cycle enumeration as a practical way to traverse such a return phase. A direct algorithm for its lifted passage could still succeed.

```sh
python3 bulk_digit_cycles_758.py
c++ -std=c++17 -O3 bulk_digit_cycle_scan_758.cpp -lgmpxx -lgmp -o cycle_scan
./cycle_scan
```
