# The power gate below H and the possible origins of a bypass

Write $P=3^{292}$. A reset anywhere in the last **1.15254%** of the approach to $P$, up to the upper cut below, forces the known checkpoint $A(1,P+1{,}934{,}340)$. The [previous gate](POWER_GATES_758.md) admitted the last 0.01% up to that cut. From the new lower endpoint to the checkpoint, the exact clock rounds to $5.22622259195\times10^{413}$ original #758 transitions across $4.02574746936\times10^{134}$ first returns. Entry from blank at this scale is open.

## The upstream gate

For each $20\le m\le292$ set $p=3^m$. Every reset from $\lfloor1458p/1475\rfloor-2m$ through $u=p-2m-4-34(4m+40)$ visits the checkpoint in the [power-gate table](power_gates_758.tsv). Throughout the added interval even starts take $IJ^{m-1}L^2JL^3R$ and odd starts take $J^{m-1}LR$. Checking the two endpoints of each parity suffices by the [ordered-counter proof](CONFLUENCE.md). The largest endpoints' intermediate left counters also exclude an earlier reset. Every return advances the parameter and the verified gain bound is smaller than the width of the old gate, so all new starts reach it.

For $m=292$ the sharp lower endpoint for these simultaneous parity words is

$$
B=\frac{1458P-876528}{1475}-1.
$$

The even seed $B-1$ has a different word. Let $u$ be the scale-292 upper cut above. At the first blank crossing above mass $2u+1$, a reset in the preceding $\lfloor2(u-B+1)/9\rfloor\approx5.34380701117\times10^{136}$ counter calls suffices to force the checkpoint. Indeed, a last reset below $B$ must gain at least $2(u-B+1)+1$ mass to cross, and a continuing call gains at most nine. The exact clock from $B$ uses the [residue-cycle summation](TARGET_CLOCK_758.md) with period 64, since the two parity words have at most five bulk moves.

## The remaining 2.715% to H

Suppose a trajectory starts at the checkpoint $S=P+1{,}934{,}340$, passes the known [halting basin](LOWER_SCALE_GATES_758.md) alive and avoids every reset in it. The basin extends from $L=H-33{,}533{,}929{,}283{,}358$ to $U=H-3{,}403{,}055$. The **last reset before the first mass crossing above $2U+1$** must lie in one of the unresolved spans in the following table. Percentages count seed values in the full range $S\le s<L$ separately for each parity.

| Starting parity | Seeds certified to halt or take a short return | Largest certified reset gain | Remaining disjoint spans |
|---|---:|---:|---:|
| Even | 98.39634895% | 768 | 27,525 |
| Odd | 97.95531034% | 780 | 35,042 |

Each remaining span has width below $1.073\times10^{-6}(L-1-S)$. Every even candidate origin in these spans is at least $0.002291H$ below $H$. The covered fractions describe the set of potential origins. They give no probability for the connected trajectory from $S$. The calculation leaves unresolved whether it visits the halting basin or halts earlier.

To verify a span of one parity, begin with the shared 292-call prefix. For odd $s$ these are jumps, yielding $(2P-1,s-P+585)$. For even $s$ they are $I$ and 291 jumps, yielding $(4P/3-1,s-2P/3+587)$. In an ordinary suffix a jump costs four mass units and a bulk costs at most nine. If both endpoints follow the same ordinary word through an even-left state outside the bulk guard, every intermediate member of that parity follows it by the counter order. The final state halts or returns with a charge of five. A visit to a reset earlier in the word gives an equally sufficient short return, because mass increases. Intervals that fail this comparison are bisected within their parity through depth 23. Adjacent unresolved leaves of the same parity are joined to form the reported spans.

A live trajectory avoiding the basin must have its last reset at $s<L$. If that reset were in a certified span, its next reset would satisfy $s<r\le s+780\le U$. Its mass would still be at most $2U+1$, contradicting the choice of the last reset. This localizes the excursion needed to bypass the entire halting interval.

Run the [upstream-gate checker](power_approach_758.py) and [gap checker](power_target_gap_758.py) from the BB(3,3) directory with Python 3.10 or later. To write the exact remaining spans, add the output option to the second command.

~~~sh
python3 power_approach_758.py
python3 power_target_gap_758.py
python3 power_target_gap_758.py --bands remaining.tsv
~~~
