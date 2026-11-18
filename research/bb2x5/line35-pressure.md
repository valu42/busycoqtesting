# How often a synchronized line 35 suffix asks for an opening

At blank epoch 300,001, consider the cut just before the last **196,613 cells**, fixed by its distance from the right end. The cells beyond this cut evolve independently of future left material. In every interval of $T$ consecutive pairs of virtual sweeps from this epoch, the number $E$ of unit debts they send left satisfies
$$
 |4E-T|\le562 .
$$
The constant **562 is attained** on this periodic signal. Every 131,072 consecutive pairs contain exactly 32,768 such requests. These are all-future statements about this particular suffix. If the physical machine eventually halts, the virtual forecast agrees with its execution for all sweeps it reaches. [Checkpoint and paired replay](line35-band.md) · [Certificate](line35_pressure.py)

## The temporal count

Number $k$ clean triples outward from the right cap. Let $H_0=1$, and let $H_i$ indicate that the center of triple $i$ is non-opening. A paired update sends $H_i$ to $H_i\mathbin{\mathrm{XOR}}H_{i-1}$. No debt leaves the cut on the odd sweep. A unit leaves on the intervening sweep precisely when the outer center is $N$, equivalent after a paired update to a $0\to1$ change of $H_k$. For a newly joined center the code checks the initial label separately. [Pascal suffix rule](line35-pascal.md)

If $P=2^{\lceil\log_2(k+1)\rceil}$, the augmented register repeats every $P$ paired updates. The number of rises in a period is half the number of toggles, which is half the number of ones in the temporal sequence $H_{k-1}$. For $k\ge2$ the smallest and largest possible rise counts over initial center phases are
$$
 L=P/2^{1+\operatorname{popcount}(k-1)},\qquad P/2-L .
$$
For $k=1$ the count is $P/2$.

To see sharpness, write $A_i=H_i(0)$. The value at paired time $t$ is the coefficient of $X^j$ in $(1+X)^t A(X)$, so the temporal samples of $H_j$ are sums of $\binom{t}{i}$ modulo two, with leading index $j$ and leading coefficient $A_0=1$. On a domain of $P$ samples the Hamming weight is at least $P/2^{\operatorname{popcount}(j)}$. Induct on $\log_2 P$. For $j<P/2$ the halves agree. For $j\ge P/2$ their pointwise XOR has leading index $j-P/2$, by $(1+X)^{P/2}=1+X^{P/2}$. The sum of their weights dominates the weight of that XOR. The lone leading term attains the bound, since it is one exactly when all set bits of $j$ are set in $t$. For $j>0$, changing $A_j$ complements the samples and gives the opposite extreme.

## A sharp bound on every interval

Take $k=p+1$ for $p=2^r\ge2$. Then $H_p(t+p)=1-H_p(t)$, so $H_k$ makes exactly $p$ toggles in a period $2p$ and exactly $p/2$ rises. For every interval of $T$ pairs and for all initial center bits,
$$
 |4E-T|\le p+1 .
$$
Discard complete periods. In a remainder of length $m<2p$, there are at most $\min(m,p)$ toggles and thus at most $\lceil\min(m,p)/2\rceil$ rises. The maximum of four times this bound minus $m$ is $p+1$, attained at $m=p-1$. The complement of the interval in a full period gives the lower bound. The first $p$ values of $H_p$ can be freely prescribed because the binomial evaluation matrix on $t,i=0,\ldots,p-1$ is triangular with diagonal ones. The initial $H_{p+1}$ is independently free. Taking $p-1$ toggles and starting at zero attains the upper bound. The complementary interval attains its negative.

For the actual checkpoint, the checker evaluates the binomial sum by a subset-sum transform over the two-element field. Its period walk adds 3 for a unit debt and subtracts 1 for every other paired sample. This walk returns to zero. Its largest cumulative value minus its smallest is the sharp absolute discrepancy for intervals of *any* length, since intervals may wrap around a period. With $k=65537$ the computed range is 562. The true right stream can therefore be used as a bounded external input when studying the material between this cut and the guard.
