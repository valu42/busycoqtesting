# Direct terminal search with mixed jumps and bulk pairs

From either of the resets $A(1,K)$ and $A(1,K+2)$ for $K=40{,}486{,}323{,}621{,}582{,}648$, the 69th map call halts at the input $A(26{,}990{,}882{,}414{,}388{,}552,26{,}990{,}882{,}414{,}388{,}551)$. The exhaustive inverse tree of that particular input has 585 states and greatest depth 92. Its only possible last resets are $K,K+2$, both at depth 68. **Every reset in the 633,739,014,317,117-seed interval from 39,752,584,607,270,532 through 40,386,323,621,587,648 bypasses this pair alive.** Every reset in the nearer interval from $K-100{,}000{,}000{,}000$ through $K-74$ also bypasses it. Blank entry into the two halting resets is a separate question.

## Searching without fixing the bulk residues

At an odd-left, odd-right state set $u=(a+2c-1)/2$ and $d=(c-1)/2$. Then $c=2d+1$ and $a=2u-4d-1$. Write $P$ for two successive bulk calls, $L$ for one bulk call and $J$ for an ordinary jump. A reset $s$ has a possible initial even-seed opening $I$ followed by its maximal run of $m$ jumps. Set $b=1$ for an odd reset and $b=2$ for an even reset, $h=b3^m$, $t=s+2m+4(b-1)$. At the end of the prefix $u=t$, $d=(t-h)/2$. The maximally batched initial run is legal precisely when $h\le t\le 3h-3$ and $t\equiv h\pmod 2$. We consider its following coarse word $w$ of $J,P$ ending just before a final $L$ and a halt. A nonempty $w$ must start with $P$. Every ordinary direct halt with this number of blocks is represented: after an odd number of bulk calls the left counter is even, so the next call must be another bulk, a reset or a halt.

The jump maps $(u,d)$ to $(u+2,3d-u+1)$. For $r=d\bmod4$, a bulk pair maps it to $(u+g_r,(9d+e_r)/4)$.

| $r$ | $g_r$ | $e_r$ |
|---:|---:|---:|
| 0 | 5 | 20 |
| 1 | 9 | 35 |
| 2 | 7 | 26 |
| 3 | 7 | 29 |

Immediately before the final $L$, put $q=\lfloor(d+1)/2\rfloor$. That call leads to $(a-4q-3,6q+5)$. The gap must then be 1, or 3 with the right counter congruent to 3 modulo 4. Thus $a=10q+9$, or $a=10q+11$ with $q$ odd. Substitution gives the necessary strip $9d-2u\in\{-17,-15,-12,-10\}$. Replay uses the exact conditions on $a,q$.

For a current strip $\ell\le Dd-Au\le r$, its inverse under $J$ has coefficients
$$
(A+D,3D,\ell+2A-D,r+2A-D).
$$
Under $P$, use
$$
(4A,9D,4\ell+36A-35D,4r+20A-20D).
$$
Indeed the residue correction is $4Ag_i-De_i$. Its minimum occurs at residue 1 and maximum at residue 0 for $0\le A/D\le 1/2$. This slope interval is preserved by both inverse maps. Each inverse also preserves $-7\le\ell/D\le r/D\le0$ when starting with the terminal strip. The formulas follow by substitution, allowing different residue branches to overlap inside an enclosing strip.

The initial line gives a closed interval for every candidate:
$$
\left\lceil\frac{hD+2\ell}{D-2A}\right\rceil\le t\le
\left\lfloor\frac{hD+2r}{D-2A}\right\rfloor .
$$
At the first block the slope is at most $2/9$, either from an inverse $P$ or directly at the empty word. Thus the real interval has length at most $126/5$ regardless of $m$. The search enumerates every integer of the allowed parity in it, checks each original branch guard in paired coordinates, rejects an earlier reset and tests the final halt exactly. The optional exceptional target uses $3d=u-2$ and odd $d$, equivalent to $a=c+2$ with $c\equiv3\pmod4$. It tests the first exceptional encounter after the specified ordinary prefix.

## Exhausted direct searches

Rows overlap. The number of words includes the empty word. A bulk pair counts as one block. The two members of a pair are separate hit seeds.

| Leading $m$ | Maximum blocks | Words | Candidate launches | Direct halting resets |
|---|---:|---:|---:|---:|
| 33–45 | 18 | 262,144 | 13,927,110 | 32 |
| 33–70 | 20 | 1,048,576 | 162,850,019 | 76 |
| 30–35 | 23 | 8,388,608 | 205,706,204 | 10 |
| 31–34 | 25 | 33,554,432 | 548,553,467 | 10 |

The last two rows give exactly the following ordered lower seeds, each accompanied by its sibling two units larger.

| Lower seed | $m$ | Blocks |
|---:|---:|---:|
| 1,326,438,094,216,110 | 31 | 16 |
| 2,031,355,966,425,479 | 32 | 2 |
| 3,335,436,339,933,243 | 32 | 0 |
| 17,430,344,744,167,562 | 33 | 2 |
| 40,486,323,621,582,648 | 34 | 18 |

The fifth path is $I J^{34} L^4 J^2 L^8 J L^{10} J L^7$ followed by the terminal call. Allowing **every** bulk residue and both seed parities, the only resets up to the known $H$ with this particular mixed tail are $K$ and $K+2$. The inverse strip for the tail has $D=16{,}677{,}181{,}699{,}666{,}569$, $D-2A=13{,}739{,}374{,}908{,}094{,}985$, $\ell=-70{,}279{,}322{,}567{,}176{,}159$ and $r=-40{,}889{,}613{,}571{,}793{,}860$. The independent verifier extracts all candidate seeds at exponents 0 through 292 and replays their actual itineraries. Already $3^{293}-586>H$, and the minimum launch increases for later exponents.

The exceptional variant finds 14 input seeds at $m=30,\ldots,35$ through depth 23 and 84 at $m=33,\ldots,70$ through depth 21. The original counter map returns at all of them before any halt.

## Which inputs these candidates capture

The [survey](mixed_terminal_windows_758.tsv) lists 257 different direct halting pairs gathered from the mixed-word and earlier direct searches. These are a finite sample across exponents. For each pair $k,k+2$ the checker replays all 5,001 resets $k-199{,}000$ through $k-194{,}000$ to the first halt or a reset above $k+2$. All inputs bypass the pair in 253 rows. The remaining rows capture 875, 120, 150 and 951 inputs, respectively, in increasing $k$ order. The last is the known $H-2,H$ pair. Every row in the $m=33,\ldots,70$ depth-20 search has zero captures in this fixed window. These results do not address a different entry window or establish that the blank orbit visits the tested one.

The same first-return map confirms the following consecutive halting windows strictly below the known $H$ pair. In each row the reset on either immediate side of the window bypasses the pair alive. The third target is
$k=67031973341757228314446197656042783060587885387371250178974638183578180826471990549767534077392348$.

| Lower target $k$ | Input offsets from $k$ | Consecutive halting seeds | Last reset on every path |
|---:|---:|---:|---:|
| 4,581,767,045,681,768,136 | −3,602 through −3,594 | 9 | $k+2$ |
| 12,966,580,636,926,693,791,014,052 | −25,997 through −25,945 | 53 | $k+2$ |
| 98-digit $k$ above | −170,405 through −170,342 | 64 | $k$ |

At the fifth pair all 5,001 trajectories eventually reach the same reset $K+118$ after 6,704 distinct first-return edges. Among **all** 10,003 seeds from $K-10{,}000$ through $K+2$, exactly $K-73,K-71,K,K+2$ halt before passing the pair. The first two return immediately to $K+2$. In the two preceding intervals the [ordered-endpoint checker](reset_cover_758.hpp) certifies an increasing later reset throughout, with the following gain bounds.

| Distance from $K$, far through near | Certified leaves | Maximum increment bound |
|---|---:|---:|
| 100,000,000,000 through 100,000,000 | 83,292,670 | 763 |
| 100,000,000 through 10,000 | 861,226 | 672 |

A certified return may be later than a first return. The mass increases at every live step, and these upper bounds keep each selected return below $K-73$ until it enters the local verified bypass. Strict increase then proves the stated bypass for every input. An orbit starting below this interval that reaches the specific terminal must cross at least 99,999,999,928 in reset parameter in a single excursion. Because each counter call adds at most nine to mass $a+2c$, this requires at least **22,222,222,207 calls**.

## A deeper entry block

Put $B=39{,}752{,}584{,}607{,}270{,}532$ and $C=K-10^{14}$. From $B$ through $C+5000$, the even seeds have the common ordinary word $I J^{34}L^4 J L R$ and the odd seeds $J^{34}L R$. Both ends of each parity certify the complete words by the same opposite-order argument. Their reset gains are at most 99 and 75, respectively. A reset below $C$ in this block must therefore eventually enter $[C,C+5000]$, since successive certified returns increase. For all 5,001 inputs at that cut, the [crossing checker](cross_758_fast.cpp) places a later reset between $K-10^{11}$ and $K-10^{11}+191$. It used 671,750 certified blocks and 1,748,370,666 individual first returns. The entire output lies in the preceding proven bypass.

The 633,739,014,317,117-seed deep block raises the necessary excursion duration for an orbit that starts below it and reaches this specific terminal to **140,830,892,070,471 counter calls**. The orbit must cross the full deep block between consecutive resets, a parameter increment of at least 633,739,014,317,118. This argument does not establish that the blank orbit enters either bypass.

## Reproduction

Run beside the existing #758 checkers. The mixed-word enumerator uses C++17 with signed 128-bit integer support. Its stdout columns give seed, leading exponent, even-opening indicator, block count, and the two counters before the final bulk (or exceptional call). The optional Python survey also independently verifies every input seed in the data file and all output offsets.

~~~sh
c++ -std=c++17 -O3 mixed_terminals_758.cpp -o /tmp/mixed758
/tmp/mixed758 31 34 25
/tmp/mixed758 33 70 20
/tmp/mixed758 30 35 23 --exception > /tmp/exception758.txt
python3 check_mixed_terminals_758.py --exceptions /tmp/exception758.txt
python3 check_mixed_terminals_758.py --survey
c++ -std=c++17 -O3 fifth_bypass_758.cpp -o /tmp/fifth758
/tmp/fifth758
c++ -std=c++17 -O3 cross_758_fast.cpp -o /tmp/cross758
/tmp/cross758 40386323621582648 40486223621582648
~~~
