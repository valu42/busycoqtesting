# A lower bound on the complexity of the jump indicator

For each elementary update of the #758 two-counter map, write **1** for an odd/odd jump J and **0** for every other update. On **any infinite blank-compatible execution**, let $p(n)$ count the different length-$n$ binary words occurring in this sequence. Its entropy satisfies
$$
h=\lim_{n\to\infty}\frac{\log p(n)}n\ \ge\ 
\frac{(1-b)^2}{(1-b)(1/\log3+1/\log(3/2))+1/\log3}
=0.06316617567\ldots,\qquad b=\frac{\log2}{\log3}.
$$
The limit exists by subadditivity, and all logarithms are natural. In particular, a proof that this **one binary sequence** from blank has subexponential factor complexity would prove that #758 and #153 halt. An upper bound below the displayed constant would also suffice. The blank-tape complexity bound needed for that conclusion is open. The [earlier entropy theorem](ALL_ORBIT_ENTROPY_758.md) distinguished four ordinary bulk residues.

## Histories that determine a line

Use $u=(a+2c-1)/2$ and $d=(c-1)/2$ at odd/odd block boundaries, with $0\le d\le u/2$. Ordinary blocks are J, of elementary length one, and P, a pair of ordinary bulk moves of elementary length two. Their binary codes are 1 and 00. A fine P also specifies $r=d\bmod4$. At aligned boundaries the binary code recovers the coarse blocks. [Coordinates and updates](EXCURSION_POWERS_758.md)

Suppose an ordinary interval contains $T$ consecutive block positions, with $u\le U=O(T)$, and enough ordinary blocks at the ends to fit the logarithmic histories below. At a position record the shortest complete **fine past** of at least $m$ elementary calls and the shortest complete **coarse future** of at least $l$ elementary calls, where
$$
 3^m>144T,\qquad (3/2)^l\ge U,
$$
taking the least qualifying integers. We call this recorded history a vertex. At distinct occurrences of the vertex the physical points obey two constraints.

* The fine-past affine formula gives one congruence $d\equiv A u+B\pmod{3^m}$. The coefficient of the initial $d$ in the full affine numerator is a multiple of $3^m$, the denominator is a power of four, and the increment in $u$ is fixed. [Two-sided reconstruction](SEPARATED_FACTORS_758.md)
* The coarse future supplies a common real slope $x$. Start at its end with slope zero; invert J by $x\mapsto(x+1)/3$ and P by $x\mapsto4x/9$. All slopes lie in $[0,1/2]$. At a fine step with next slope $x'$, the deviation $d-xu$ evolves to $3(d-xu)+1-2x'$ at J, or $(9/4)(d-xu)+b_r/4-v_r x'$ at P. The offset in the first case is in $[0,1]$, and in the second in $[0,35/4]$. The inverse updates all preserve $[-7,0]$. Since the terminal deviation is $d_{\rm end}\in[0,U/2]$, pulling it back places the initial deviation in $[-7,1]$. The inverse contraction per elementary call is at most $2/3$.

The determinant of any three such $(u,d)$ is divisible by $3^m$. Subtracting $xu$ from the second coordinate preserves this determinant; the second coordinates now have span at most eight, and the first span at most $9T$. Expanding about any of the three points bounds the determinant in absolute value by $144T$. Hence it vanishes. Whenever the vertex occurs at least twice its points determine one nonvertical rational line.

An edge records the two successive vertices and the intervening fine block. The number of distinct such edges is at most
$$
F=2^{m+4}p(m+l+4).
$$
Indeed, start a binary word of length $m+l+4$ at the beginning of the first fine past. Its length up to the cut is $m$ or $m+1$. These data locate both histories by parsing from block boundaries. The labels through the intervening block use at most $m+3$ elementary calls; each P has four labels and costs two calls. The fine past of the second vertex starts no earlier than that of the first. Logarithmic margins inside an ordinary stretch suffice. Arbitrary extensions to the indicated binary length exist on the infinite orbit.

A repeated edge maps the first vertex's line onto the second vertex's line, since its fine block maps two distinct actual points between their occurrences. Deleting all edges seen just once cuts the span into at most $F+1$ runs. One run therefore has at least $(T-F)/(F+1)$ consecutive line-preserving edges. If $h$ were below the claimed bound, then, with $c=1/\log3+1/\log(3/2)$,
$$
 F\le T^{b+ch+o(1)},\qquad \rho=1-b-ch>0 .
$$
The run then has length at least $T^{\rho-o(1)}$.

## A long run with one denominator

At a line-supporting vertex the slope is a reduced $k/q$ with $q\le9T$ and $|k/q|\le U$: differences of two distinct actual $u$ values are nonzero integers of size at most $9T$. J sends the slope to $3k/q-1$, and P sends it to $9k/(4q)$. We discard at most $O(\log^2 T)$ positions at the ends of the long run to achieve all of the following properties at once.

1. If the reduced denominator is divisible by three, its 3-adic valuation falls by one per elementary call, stopping at zero; zero can never increase. The initial part affected has $O(\log T)$ positions.
2. Once a denominator is even, each subsequent P increases its 2-adic valuation by two, and J preserves it. There are only $O(\log T)$ subsequent Ps. Each actual run of consecutive Js also has length $O(\log U)$, because J triples $a+1$ while $a\le 2u$. Discard this final portion. The remaining denominators are coprime to six and equal to one fixed $q$, since their other prime factors cannot change.
3. Outside $[0,1/2]$ the distance of the slope from that interval grows by at least $9/4$ per block. At its first outside value the distance is at least $1/(2q)$ and its maximum is $U+1$. Discard this final portion. On the remaining interval put $e=qd-ku$ at the actual point. It is integral. As long as the slopes stay in $[0,1/2]$, the inverse formulas above preserve $[-7q,0]$ for $e$; outside it the distance grows by at least $9/4$ per block. Its initial nonzero distance is at least one and its maximum is $q(U+7)$. This costs another $O(\log T)$ positions.

We obtain a central span of $S\ge T^{\rho-o(1)}$ positions in which
$$
 0\le k\le q/2,\qquad -7q\le e\le0.
$$
In fact $q>9S$ for all sufficiently large $S$. Here are the needed details. A pair $(k,e)$ cannot recur in the central span. On recurrence the intervening fine word would map its initial line to itself, with one full legal occurrence on that line. The [physical invariant-line argument](EXCURSION_POWERS_758.md) and the [global exclusion](FINITE_AFFINE_PERIODS_758.md) rule this out, including the pure words. Fix the least $j$ with $3^j>7q$. As in the denominator proof, a given fine suffix of elementary length at least $j$ fixes $k$ and $e$ modulo $3^j$ at its end. Indeed both coordinates transform by $3$ or $9/4$ times an integer shear, plus a known translation depending on $q$ and the fine block. This fixes the bounded pair exactly. Apart from the first $O(j)$ positions, a shortest complete suffix spans $j$ or $j+1$ calls. The numbers of fine words at these lengths are $O(\Lambda^j)$, where $\Lambda=(1+\sqrt{17})/2<3$, by the recurrence $f_j=f_{j-1}+4f_{j-2}$. Thus
$$
 S=O\bigl(\log(q+1)+(q+1)^{\log_3\Lambda}\bigr).
$$
The exponent is strictly below one, giving $S=o(q)$ along any sequence of such spans with $S\to\infty$.

## A second set of lines inside the central span

Within the $S$ positions, record nested pasts: a **coarse past** of at least $r$ elementary calls and a **fine past** of at least $m'$ calls. Both are the shortest complete pasts with the prescribed lengths. Take $3^{m'}>144S$ and $3^r>\max(q,144S)$ with the least qualifying exponents. Discard the first $O(\log T)$ positions so these pasts lie entirely inside the fixed-denominator span.

All occurrences of this new vertex have the same $k$. The coarse updates alone give $k\mapsto3k-q$ or $9k/4$, so a coarse past of length at least $r$ fixes its final numerator modulo $3^r$, independently of the starting numerator. The interval $[0,q/2]$ selects it uniquely. Consequently the physical points now lie in the strip $-7\le d-(k/q)u\le0$. The fine past gives the usual modulus $3^{m'}$. Since the $u$ span is at most $9S$, the same determinant argument proves collinearity.

Every line determined by two occurrences inside this span has reduced denominator at most $9S$, **strictly less** than $q$. On a repeated-edge run for the nested vertices, let $y$ denote their successive supporting slopes. Compare to $k/q$ along that same physical run. Both are transported by the same slope maps. Initially $|y-k/q|\ge1/(9Sq)$. After every block the difference increases by a factor of at least $9/4$, while $|y-k/q|\le U+1$ everywhere. Thus every inner repeated-edge run has length $O(\log T)$.

With $F'$ inner edges there can be at most $F'$ singleton occurrences and $F'+1$ repeated runs. The same encoding as before gives $F'\le 2^{m'+4}p(r+3)$, using the beginning of the coarse past, either $r$ or $r+1$ calls before the cut. Hence
$$
 \frac{S}{O(\log T)}\ \le\ F'+1
 \ \le\ S^{b+o(1)} T^{h/\log3+o(1)} .
$$
Here $q\le9T$, $S\le T$, $m'=\log_3 S+O(1)$ and $r\le\log_3 T+O(1)$. Combining with $S\ge T^{\rho-o(1)}$ gives $(1-b)(1-b-ch)\le h/\log3$, contrary to the assumed strict upper bound on $h$.

## Applying the argument to every infinite execution

If ordinary stretches of length at least $\epsilon u$ occur at arbitrarily large starting $u$ for some fixed $\epsilon>0$, take $T$ to be a fixed positive fraction of the stretch's first $\epsilon u$ positions. This gives $U=O(T)$ and all needed logarithmic margins. This case includes an infinite final ordinary stretch. In the remaining case the [reset-density argument](ALL_ORBIT_ENTROPY_758.md) proves that every finite word in J and P occurs. The binary encodings J $\mapsto1$ and P $\mapsto00$ give distinct factors at each fixed elementary length; their number satisfies the Fibonacci recurrence. This gives the stronger $h\ge\log((1+\sqrt5)/2)$ in that case.

The [checker](coarse_entropy_758.py) verifies the modular transport, inverse-strip bounds and binary context encoding on finite examples, and uses rational logarithm bounds to certify that the displayed entropy exceeds $1/16$.

The [finite crossing bounds](BINARY_PASSAGES_758.md) apply the binary argument to the scale-10 halting interval and the post-target checkpoint corridor.
