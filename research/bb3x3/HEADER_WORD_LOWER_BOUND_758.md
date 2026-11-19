# A lower bound on word-by-word search below the halting target

For the fixed target $H=(3^{307}-8{,}282{,}708{,}212)/D$, $D=13{,}959{,}275$, more than $10^{41}$ **different complete first-return words** actually occur among resets $A(1,H-d)$ with $10^4<d<2.52\cdot10^{63}$. All examples in the counting proof have $d$ divisible by 32,768 and the same two opening jump counts, 292 and 153. Thus a proof assigning a single fixed ordinary word to each certified set of starting seeds needs more than $10^{41}$ sets here. A proof combining many different words in one step, or following only the exits relevant to blank, can avoid this lower bound. The count does not establish that blank visits these seeds.

## Counting physical words without enumerating them

After $J^{292}L^8JL^6$, the jumplike coordinate $h_0=(a+1)/2$ at $d=32768i$ equals $2Di$. This follows from the established [header identity](RATIONAL_HEADERS_758.md). Put $U=3^{307}/D$ and propose 153 more jumps. Then $h=3^{153}h_0$ and the directions $h/U$ lie on the exact grid $i\tau$ with
$$
\tau=2D^2/3^{154},\qquad 32768/\tau<2.52\cdot10^{63}.
$$
Write $f_J(x)=x/3$, $f_P(x)=(4x+5)/9$ for the inverse ordinary jump and bulk pair. Let $\delta$ solve $3^{-\delta}+(4/9)^\delta=1$. Grow the binary tree of inverse cylinders $I_w=f_w([0,1])$ and stop along each path at the first interval of length at most $\epsilon=120\tau$. The stopping intervals have lengths in $(\epsilon/3,\epsilon]$. Their lengths to the power $\delta$ sum to one, because this sum is preserved at every split. There are therefore at least $\epsilon^{-\delta}>10^{41}$ different stopped words. For the numerical inequality it suffices that $\delta>8/11$, proved by $3^{-8/11}>449/1000$ and $(4/9)^{8/11}>551/1000$.

Prepend one pair to each word, giving $I=f_P(I_w)$ of length greater than $4\epsilon/27$. The image of $[2/5,7/15]$ in $I$ has length $|I|/15>\tau$, so contains some grid point $i\tau$. Its ideal itinerary executes $Pw$ and then hits the interior of the return interval $(1/3,5/9)$. The grid point is farther than $\tau$ from every inverse guard on that itinerary. At the final decision the distance is at least $|I|/15$. At any earlier decision the relevant inverse guard lies outside the interior of $I$, and the grid point has distance at least $2|I|/5$ from either endpoint.

These margins also verify the two real counters. The chosen countdown $d=32768i$ is between $(5/9)32768/\tau$ and $32768/\tau$. The [common opening](TARGET_SHADOW_758.md) is legal throughout. At the proposed alignment $u=(a+2c-1)/2=U-d+\eta$ with $|\eta|<1200$. The clearance from 1 gives $h<u$, which makes the 153rd jump and hence its predecessors legal. The clearance and $h/U>5/9$ then preclude another jump. At any later guard $\mu\in\{0,1/3,5/9,1\}$, the exact inverse formula in that same proof is $h-\lambda u=R(h'-\mu u')+B$ with $0<R\le1$ and $0\le B\le14$. Replacing $u$ by $U$ in the initial comparison changes it by at most $d+1200$. The integer check gives $\tau U>32768/\tau+1220$. Hence every selected guard keeps its true sign with more than four units to spare, including the final ordinary reset. Distinct stopped words give distinct physical first-return itineraries.

## A reachable header that outlasts the uniform shadow

Set
$$
d=2519807940164222286326480224696064445884526387481856382330434770.
$$
After the same opening and 153 jumps, this reset executes **357 consecutive ordinary bulks**, then returns. At the 154-call cut it has completed 77 pairs and its normalized numerator over $4^{77}$ is 22835963083295358096932575511191922154683810565. It is a genuine surviving header with a known physical past even though the uniform shadow guarantees only 157 calls at this countdown. The complete first return takes 818 elementary calls and increases the seed by 2,160.

Run [header_word_lower_bound_758.py](header_word_lower_bound_758.py) beside the machine checkers to verify the integer inequalities and replay the entire example.
