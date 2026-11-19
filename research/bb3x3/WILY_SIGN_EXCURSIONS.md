# How far back does a Wily sign escape begin?

Write $e<0$ for an input with $F(e)>0$, and $p_e$ for the most recent positive integer before $e$ in its two-sided orbit. Every such $p_e$ exists. The time from $p_e$ to $e$ has **no uniform upper bound**. On the other hand, for each $0<\delta<1$ and fixed $c>0$, the fraction of escape sources with $p_e<c|e|^\delta$ tends to zero. A bound on the particular blank excursion would decide a different question from this counting theorem. [Integer map, escape forests and order on negative excursions](WILY_INTEGER_MAP.md)

## The last positive exists

Let $B=B(e)$ be the smallest admissible power-of-two bucket. Its value cannot increase on a backward negative segment, except at $-1\mapsto-2$; the next predecessor there is 5. Thus before the first positive, all negative predecessors are in $[-\max(B,2),-1]$. A negative state cannot repeat: determinism would put $e$ on a negative cycle, contradicting $F(e)>0$. Pigeonholing gives a first positive within $\max(B,2)$ steps. At that step the inverse sweep on the original bucket returns a positive numerator strictly below $5\max(B,2)$, by the four inverse edge numerators in the integer-map proof.

## An unbounded family of waiting times

Use the escape lifts $L(m)=4m+6$ and $S(m)=2m-3$ for odd $m$, $2m+9$ for even $m$. On even inputs, $T=L\circ L\circ S\circ S$ satisfies $T(m)=64m+270$. For either $e_0=-8$ or $-16$, all $e_k=T^k(e_0)$ are escape sources. They tend to $-\infty$ in the ordinary ordering and to $x=-30/7$ in the 2-adic topology.

The inverse of $F$ on a numerator reads its binary digits from the low end. It removes a low 0 by recursing on $y/2$, or a low pair of ones by recursing on $(y-3)/4$. A low 1 followed by 0 ends the scan. The two possible stopping branches add 3 or subtract 21. At any point whose scan ends, the full inverse is therefore translation by a fixed integer on a sufficiently small residue class around that point. This follows by reversing the scanned affine lifts. The exceptional integer $-1$ is outside the rational class used here.

The identity $x=14+2^7/(1-8)$ shows that its high binary digits have an isolated 1 every three positions. Adding an ordinary integer changes only finitely many digits of this nonconstant periodic tail. Thus the inverse scan ends at every $x+j$ for $j\in\mathbb Z$, regardless of the low bits. For any fixed $t$, composing these local translations gives integers $c_0,\ldots,c_t$ and a modulus $2^h$ such that $F^{-i}(n)=n+c_i$ for $0\le i\le t$ whenever the integer $n$ lies in the residue class of $x$ modulo $2^h$. For all sufficiently large $k$, $e_k$ lies in this residue class and $e_k+c_i<0$ for every $i\le t$. Hence the waiting times of this specific family tend to infinity.

## A density bound on small positive entries

The assignment $e\mapsto p_e$ is injective. From $p_e$ its next state is negative and $e$ is the unique last negative state before the next positive. In particular $p_{e_k}$ tends to infinity on the family above: only finitely many distinct positive integers fit below any fixed bound. This observation supplies no rate of growth in $|e_k|$. A positive $p$ with $F(p)<0$ is obtained by positive lifts from 1, 2 or 5: descent from a positive multiple of four gives a positive image, and the only positive descent inputs whose next recursive argument is nonpositive are 1, 2 and 5. The output lifts preserve sign. The positive children of 1 and 2 are among 10, 13 and 14. Once $m\ge5$, either lift of weight $w$ sends $m-3$ to a value at least $2^w(m-3)$ after subtracting three from its result; the weights are two for $L$ and one for $S$. Therefore a positive entry $p\le Y$ arises from one of finitely many seeds and a lift word of total weight at most $\log_2 Y+O(1)$.

The number of words of weight $k$ satisfies the Fibonacci recurrence. With $d=\log_2((1+\sqrt5)/2)$, there are $O(Y^d)$ possible positive entries. Injectivity gives

$$\#\{e:-X\le e<0,\ F(e)>0,\ p_e<c|e|^\delta\}=O_c(X^{\delta d}).$$

There are $\Theta(X^d)$ escape sources in the same range by the escape-forest count. The relative frequency of these violations is $O_c(X^{-(1-\delta)d})$. A uniform bound would require controlling the exceptional excursions individually. In particular, $p_{-5870}=1$ at backward time 17, so a universal coefficient of 1 fails already at $\delta=1/8$.

## Selecting the first sign change without stepping through the orbit

The [first-contact checker](wily_first_contact.py) acts on a single binary digit at a time. A chronological period of incoming modes at that digit ends either at its initial bit or at its opposite. In the latter case, two copies of the period restore the bit. Pass that complete period through the digit, dropping identity carries. This gives one period of all arrivals at the next digit. Iteration reaches any specified digit. The periods are represented by shared binary concatenations.

At the selected digit, the checker finds the first requested event in the complete period or proves that it never occurs. To obtain its original scalar time, work backward through the digits: the $j$th emitted event comes from the $j$th input whose carry continues. Each binary concatenation records the incoming count, outgoing count and ending bit for each possible starting bit, so the checker can select that input by descending the tree. Whole periods skipped in this calculation restore the same bit. The newly written bit at the chosen input reconstructs the post-event value at each level. The same algorithm locates the first specified carry at an allocated word edge in either direction.

For the ordinary sign of an integer numerator, compose binary division by three, the inverse Wily sweep, and multiplication by three. This finite transducer acts directly on the bits of $n$. Choose a signed residue width whose half-modulus exceeds $5\max(B(e),2)$. Until and including the last positive, its highest bit is the actual sign bit, by the preceding bounds. A first flip gives the exact positive value and backward time. For example, on the family with $e_0=-8$ the calculation gives the following results.

| $k$ | $e_k$ | Backward steps to $p_{e_k}$ | $p_{e_k}$ |
|---:|---:|---:|---:|
| 0 | −8 | 1 | 11 |
| 8 | −1,045,478,484,925,298 | 51,888 | 1,268,563,994,814,446 |
| 18 | −1,205,354,627,874,156,413,766,008,076,426,098 | 13,693,004,464 | 10,799,795,530,424,662,588,516,838,483,950 |

Run `python3 wily_first_contact.py` to compare the forward and inverse transducers, carry selection, and sign-change times with literal execution on small inputs. Use `python3 wily_first_contact.py --family 18` to reproduce the table and the companion family rooted at −16. These families certify long negative prehistories and give no visit from the blank seed.
