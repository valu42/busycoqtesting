# A scalar transport law for the connected reset orbit

For $P=3^m$ and $m\ge20$, take any finite section of the actual reset sequence with all its seeds in $[P,3P]$. Write $D$ for the last seed minus the first, $N$ for the number of complete first returns between them, and $G$ for the largest of their seed gains. For a nonempty section,
$$
0\le D-2mN=O\big(P/m+P^\delta G^{1-\delta}\big),\qquad
3^{-\delta}+(4/9)^\delta=1.
$$
The constant is absolute. The same bound holds on every prefix with the same upper bound $G$. Thus, on any family of completed crossings with $G/P\to0$, the reset seed divided by $P$ advances linearly in the rescaled return count $2mN/P$, with a uniform error tending to zero. This law sums over the words the connected trajectory actually uses. Applying it to a proposed blank crossing needs a bound on its largest excursion.

For example, suppose the blank trajectory crosses from below $3^{291}$ to above $3^{292}$ in successive resets and every reset step touching that passage gains at most $3^{219}$. Between its first and last resets inside the annulus the number of complete returns lies between $2.21868\times10^{136}$ and $2.38997\times10^{136}$, or between 92.7% and 100% of $3^{291}/291$. These figures are conditional. The large-gap alternative is precisely where a bridge based on this transport law can fail.

## Spacing and the cost of regular words

After a reset of a given parity, its maximal opening jump run leaves $h=b3^k$ and $t=s+4(b-1)+2k$, with $b=1$ on odd seeds and $b=2$ on even seeds. Since $h\le t<3h$, for $s\in[P,3P]$ the nonexceptional opening groups have $(h,k)=(P,m),(2P/3,m-1),(2P,m)$. Odd seeds within $2m+2$ of the upper edge may have $k=m+1$. Every opening increases the mass coordinate by at least $2m$, so all reset seeds in the section are spaced by at least $2m$. The fourth group's outgoing displacements total at most $2m+2$ when the whole section stays inside the annulus.

For the first three groups the opening gains at most $2m+4$. Split every following ordinary prefix into jumps $J$ and pairs of ordinary bulks $B$. A jump gains two mass units and a pair gains at most nine; the final bulk and reset gain at most seven. If any whole block occurs, the first is a pair by maximality of the opening jumps.

For an ordinary word $w$ let $I_w$ be its inverse cylinder under $f_J(x)=x/3$ and $f_B(x)=(4x+5)/9$, and $R_w=|I_w|$. All realized starts of this word have $x=h/t$ in $I_w$ enlarged at the right by $14/P$. Words ending earlier at an exceptional edge, a terminal or the reset axis have $x$ within $18/P$ of an endpoint in the survivor set $K$. These are the [uniform pullback bounds](LOCAL_RETURN_WINDOWS_758.md). A nonempty realized word starts with $B$, so $x\ge5/9$.

Take $0<G\le P$ (larger gains give the claimed asymptotic bound immediately). Stop the cylinder tree as soon as its width drops to $z=G/P$ or below. Its number of leaves $L$ is at most $(3P/G)^\delta$, since their lengths exceed $z/3$ and the sum of the $\delta$ powers is one. A regular return ends ordinarily before this cutoff.

For each nonempty ordinary word in the tree, its source seeds occupy an interval. In the unpadded cylinder $[a,b]$, converting the angular width to seed width gives $h(1/a-1/b)$, after clipping to the launch group's range. Physical padding extends that estimate by at most $14(81/25)h/P$, since $x\ge5/9$. With seed spacing $2m$, the number of source resets in that interval is bounded by one plus its width divided by $2m$. Across the three groups, the sum of the $h$ values is $11P/3$.

The normalized sum over all unpadded nonempty word intervals of their widths times the gain of the last block is less than 63 (units of $P$). To verify this, clip the normalized angular range to $[1/3,1]$, $[1/3,2/3]$ and $[0.66,1]$ for the three launches; the last lower bound follows from $2P/(3P+2m+4)>0.66$. The [checker](reset_count_transport_758.py) sums the rational reciprocal widths through 12 grouped blocks. At all later levels the normalized seed width is bounded by $(81/25)(h/P)R_w$. The first pair has contraction $4/9$, ordinary children have total contraction $7/9$, and their gain-weighted contractions total $2/3+9(4/9)$. The geometric tail bound gives a combined total below 62.423.

There are fewer than $2L$ nodes in the stopping tree. At $m\ge20$ the aggregate padding and counting error per node is bounded by $9(3+14(81/25)(11/3)/(2m))<72$. Summing the ordinary blocks actually visited, then the regular openings and final reset, bounds the regular excess over $2m$ per return in total by $11N+63P/(2m)+144L$.

## Charging long excursions to their starting intervals

A remaining return either reaches a stopped cylinder or takes an earlier exceptional or terminal-adjacent edge. Its origin lies in one of the $L$ stopped angular intervals enlarged at both ends by $18/P$, since these intervals cover $K$. On the physical launch range $x>1/3$ the seed derivative is at most $9h$ in absolute value. The outgoing seed interval of any such return is therefore contained in the corresponding starting interval, padded on its upper end by $G$. All actual return displacements have disjoint interiors. Their total in the three launch groups is at most
$$
L\sum_{h\in\{P,2P/3,2P\}}\!\left(9h(G/P+36/P)+G\right)
=L(36G+1188).
$$
This estimate includes arbitrary dynamics following an exceptional edge. It requires only the stated largest seed gain.

Combining the estimates gives $2mN\le D\le(2m+11)N+63P/(2m)+L(36G+1332)+2m+2$. Since $N\le P/m$ and $G\ge2m$, the transport law follows. One may substitute any larger cap up to $P$ throughout the construction. In the numerical example take $G=3^{219}$, $L\le3^{55}$ using $\delta<3/4$, and $2P-2G\le D\le2P$ after allowing the two boundary crossings.

Run `python3 reset_count_transport_758.py` from the BB(3,3) research directory to verify the finite rational bounds and sample the primitive accounting directly on physical returns.
