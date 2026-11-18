# The right edge of line 35 follows a Pascal recurrence

The November 3 machine on line 35 is `1RB2LA4RA1LA3LA_0LA3RB3LB2RB---`. Its only undefined instruction is B4. One can transfer the [line 37 right-boundary calculation](line37-pascal.md) to this different machine. On every sufficiently long successful run, any prescribed number of triples at the right edge eventually enter a linear cellular automaton over the field with two elements. There is an explicit time bound for this conditional entry. An all-time bound on debt reaching the line 35 left guard remains open.

## The extra opening

At a normalized epoch A scans the blank immediately left of a finite word. Write $O,C,N$ for an opening, closing and neutral cell. On line 35 these are physical symbols $1,2,3$. On line 37, `1RB2LA3LA4RA1LA_0LA3LB3RB1RB---`, they are symbols $2,1,3$. Match each closing to the most recent available opening to its left. Unmatched openings have survivor bit 1. All other cells have bit zero. Line 35 reaches B4 on the sixth unmatched closing. On a successful sweep its outward pass leaves a surviving opening as 3 and all other ordinary cells as 2. A guard reset can fill an earlier part of the tape with 2s because the guard was reached only after all earlier openings had already been matched.

On line 35’s return pass a nonsurvivor produces ternary carry 1 and a survivor produces carry zero. In either machine's matching roles the output at an ordinary cell depends on adjacent old survivor bits by
$$
 D(0,0)=D(1,1)=O,\qquad D(0,1)=C,\qquad D(1,0)=N.
$$
Here the first bit is the material neighbor to the left and the second is the current bit. This follows on line 35 from the ternary order $3,1,2$ by adding the incoming carry. The literal definitions of both sweeps are available in [prior_sweeps.py](prior_sweeps.py).

A line 35 word ending in $C$ appends another $C$ on every successful sweep, since the final closing has survivor bit zero and outgoing carry 1. Number cells from the right starting at zero and denote their old survivor bits by $s_j$. With the appended digit, the successor digit at distance $j$ is $D(s_j,s_{j-1})$ for $1\le j$ below the old width. To compute this suffix, add a single $O$ to the extreme right of the old line 35 word and use the line 37 suffix rule. The extra $O$ survives and leaves all old matching unchanged. The line 37 successor appends $O$, with cell immediately on its left equal to $D(0,1)=C$. Delete that appended $O$. The resulting digits agree through the entire old width with the line 35 successor. This statement applies to the right data even when the two guards would make different decisions. It invokes no successful sweep of an auxiliary full line 37 machine.

## The two-cell boundary and the triples

In right-to-left order the line 35 seed at epoch 5 starts with $C,O$ followed by an $O,O,O$ triple. Its full physical word in left-to-right order is `213111112`. This is the actual blank execution after 97 defined instructions with head at $-5$. The right pair $C,O$ sends zero debt to its left and both its survivor bits are zero. It returns to $C,O$ on every successful sweep by the formula above.

At odd epochs take consecutive triples $(O,a_i,O)$ after this pair, starting with $i=0$ at the right. Set $b_i=[a_i=O]$. In the [line 37 three-cell calculation](line37-pascal.md#three-cell-blocks) a previous center $a$ supplies survivor bit $[a\ne C]$ and zero debt on the first sweep, then bit $[a=O]$ and debt $[a=N]$ on the second. The two line 35 boundary cells supply zero for all three actual quantities. Hence the virtual previous center on line 35 is $C$, giving $b_{-1}=0$. Each complete triple then returns after two successful sweeps to $(O,D(b_i,b_{i-1}),O)$. With $h_i=1-b_i$ this gives
$$
 h'_i=h_i\mathbin{\rm XOR}h_{i-1},\qquad h_{-1}=1.
$$
Complete triples send zero debt to their left at the covered odd epochs. In the intermediate phase their union with the two boundary cells sends exactly $[a_{k-1}=N]$ when $k\ge1$ triples were covered.

For clarity, the local calculation for an exterior triple $T$ uses $F(T,s,d)$, which reads the three cells from right to left. At each symbol $v$ it sets $u=[v=O\text{ and }d=0]$, outputs $D(u,s)$, replaces $d$ by $\max(0,d+[v=C]-[v=O])$, and sets $s=u$. Two sweeps with previous center $a$ act by
$$
 G(T,a)=F\bigl(F(T,[a\ne C],0),[a=O],[a=N]\bigr).
$$
For every $T$, $G(T,N)$ is one of $(O,N,C),(O,N,O),(O,O,O)$. For each of these three outputs $U$ and every following center $a'$, $G(U,a')$ has the form $(O,x,O)$. This is the same 81-case calculation as on line 37. The checker evaluates it using the common function on all triples.

## A bound on entry from blank

When $k$ triples are covered, the augmented bit vector $(1,h_0,\ldots,h_{k-1})$ evolves by $I+S$, where $S$ shifts one place toward the left side of the physical tape. Its exact period in pairs of sweeps is $P(k)=2^{\lceil\log_2(k+1)\rceil}$. Indeed $(I+S)^{2^r}=I+S^{2^r}$ and the first bit is 1. The last coordinate is nonconstant: its predecessor takes value 1 at some time, inductively from the constant boundary. At a transition from 0 to 1 in that last coordinate the new center is $D(1,0)=N$. Hence such a center occurs within $P(k)$ paired updates. Two further updates suffice to absorb the next exterior triple by the local calculation.

There are four unused cells beyond the first triple and two-cell boundary at epoch 5. Each pair of successful sweeps adds at least four cells, since each sweep has at least one header cell and appends a closing. Adding one guaranteed triple at a time therefore always leaves at least the three exterior cells required. By epoch
$$
 5+2\sum_{i=1}^{k-1}(P(i)+2)
$$
the first $k$ triples have joined, provided that many sweeps succeed. This proves eventual coverage of every fixed right suffix on any infinite blank run, and bounds the debt it can transmit. The untreated middle of the growing tape can still send additional debt to the guard. At epoch 1,001 the computed word has 2,037 cells with 459 covered triples beyond the two boundary cells.

## What a halt would require in the middle of the tape

Let $d_8$ be the debt sent from the cells strictly after the first eight. **If $d_8\le4$ at every epoch from epoch 5 onward, line 35 never halts.** The finite calculation has 71 prefixes and only 355 cases.

For a given eight-cell prefix $P$, the incoming exterior debt determines which of its openings survive and how much debt reaches the left guard. The resulting header depends only on the guard debt $H$. For $H=0,1,2,3,4,5$ the six physical headers respectively are `2`, `1`, `3`, `1323`, `1313`, `1331`. The virtual left survivor bit for the first old digit is respectively $1,1,0,0,0,0$. In the reset cases the wall and rewritten old guard supply the extra header digits. Applying $D$ to $P$ now determines the entire next eight-cell prefix. Thus one may realize exterior debt $d$ with the canonical completion $P C^d OC$ in matching roles, regardless of the rest of the actual tape.

Start with the true prefix at epoch 5. Repeatedly compute all five successors for exterior debts zero through four. The reachable set closes on 71 prefixes and 310 distinct ordered pairs, with maximum guard debt five. The verifier also carries out all $71\cdot5$ canonical sweeps on the literal two-state machine. Allowing exterior debt five in this same abstraction admits a failure on the successive choices $2,5,2,5$. Those choices refer to independent exterior completions. They have no established realization on the blank orbit.

Consequently a true halt requires some earlier or current epoch with $d_8\ge5$. Whenever the covered right suffix (the two-cell boundary and its Pascal triples) lies after this cut, the intervening middle word must itself have debt at least four on the intermediate phase, or five on the covered odd phase. Indeed the debt of a concatenation of a middle word and a suffix is at most the sum of their debts, and the covered suffix contributes at most one or zero respectively. A proof that the untreated middle never sends sufficient debt would complete the argument.

Run `python3 line35_pascal.py` in this directory. Its check covers every input ending in a closing through length eight, including successful guard resets and all six possible debts of a successful word, and compares the blank prefix with literal TM execution. [Source](line35_pascal.py) · [Observed output](line35-pascal-verification.txt)
