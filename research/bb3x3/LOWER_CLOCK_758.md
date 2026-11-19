# A conditional lower bound for the #758 and #153 clocks

**If the blank orbit reaches either A(1,H−2) or A(1,H), it requires more than $2.10448\times10^{414}$ raw Turing-machine steps to halt.** In fact the lower bound applies as soon as mass $V=2H-3$ is reached or crossed and does not depend on the subsequent halt. Here $H=(3^{307}-8{,}282{,}708{,}212)/13{,}959{,}275$. The two encodings join with an offset of 50,707 steps, already allowed for in the rounded statement. Reaching this mass from blank is open. [Transition map](check_bb33.py) · [Raw timing rules](timing_758.py) · [Verifier](lower_clock_758.py)

## Grouping steps near the axes

Use $W=a+2c$, $x=a/W$, $N=256$, and begin at the first mass at least $M=10^{10}$. On the continuing blank orbit $c\ge1$, and even $c$ occurs only at $a=1$. A single continuing call gains 4, 5, 8, or 9 in $W$ and costs at least $3\min(a,c)^2$ raw steps. [Branch bounds](MASS_CLOCK_758.md)

A central vertex records $i=\lfloor Nx\rfloor$ and the parity of $a$ for $4\le i<252$. Two additional vertices represent the low axis ($Nx<4$) and high axis ($Nx\ge252$). A central edge represents one literal call. An axis edge represents the entire run from an axis state up to its first central state. Work only up to the first crossing of the target, so all masses are at most $2H+9$.

* On the low axis, $a<c$. An even $a$ first resets to 1, gaining 5. At $a=1$ an even $c$ first gives $(3,c+3)$, gaining 8. Both updates stay on the low axis. All remaining calls before exit use the odd/odd rule J, for which $a'+1=3(a+1)$ and the gain is 4. At most 293 such calls occur since $3^{294}>2H+10$. The gain ceiling is $4\cdot293+13=1185$. The first central state has odd $a$ and bin $4\le i\le12$ since $x'\le3x+2/W$.
* On the high axis, $a$ is much larger than $c$ and $c$ is odd, so all calls use an ordinary bulk rule. Both rules give $c'+7\ge(3/2)(c+7)$. Since $c+7\ge8$ and $8(3/2)^{788}>(2H+9)/2+7$, at most 787 calls occur. The gain ceiling is $G=9\cdot787=7083$. The first central bin lies in $249\le i\le251$, by the bulk output formula below. The bounds on both axis gains also hold for a visit truncated at the target crossing.

## Central edges and the finite certificate

Each central vertex has charge $C_i=3\min(2i,N-i-1)^2$ in units of $W^2/S$, where $S=4N^2$. This gives a lower cost throughout the bin. Axis vertices are assigned zero charge. The central rules below list all continuing outputs. Bin ranges include both endpoints. An output outside the central range is routed to the appropriate axis vertex.

| Continuing rule | Applicable bins and input parity | Output bins and parity | Gain ceiling |
|---|---|---|---:|
| J | $3i\le N$, odd | $3i-1$ through $3(i+1)$, odd | 4 |
| Reset | $3i\le N$, even | Low axis | 5 |
| Ordinary bulk | $3(i+1)>N$, either | $\lfloor(3i-N)/2\rfloor-1$ through $\lfloor(3(i+1)-N)/2\rfloor$, opposite parity | 9 |
| Exceptional boundary | $3i\le N+1$ and $3(i+1)>N$, odd | High axis | 8 |

For J, $x'=3x+(2-12x)/(W+4)$ and the discrepancy is smaller than one bin. For bulk put $y=(3x-1)/2$. Then $x'=y-(\delta+gy)/(W+g)$ with $\delta=2$ or $4$, $0<y\le1$ and gain $g\le9$. The discrepancy is nonpositive and smaller than one bin. At the exceptional boundary $a=c+2$ we have $x=1/3+4/(3W)$ and $x'=1-2/(W+8)$. Thus the true update belongs to the stated graph in all cases.

For $D=12500$, the verifier constructs integers $-A\le d_i\le0$ with $A=1{,}860{,}468{,}840$. It checks directly on all 1,655 edges $i\to j$ with charge $C_i$ and gain ceiling $g$ that
$$D C_i\;\ge\; Sg+d_j-d_i.$$
Integer relaxation computes the potential. The subsequent edge-by-edge checks are sufficient to certify it.

## Turning the certificate into raw steps

Write $w_k$ for the initial mass of edge $k$, $h_k$ for its true gain, and $T$ for total raw time. On complete edges the preceding inequality implies
$$SD T\;\ge\; S\sum_k h_k w_k^2+\sum_k(d_{k+1}-d_k) w_k^2.$$
The last sum is at least $-A(V+8)^2$ by summation by parts, since $d_k\le0$ and squared mass increases. Start at the first mass at least $M$, which is at most $M+8$. Discard any final incomplete axis edge. The remaining path ends at mass at least $V-G$. On each complete mass interval $w_k\le w\le w_k+h_k$, we have $0<w-G\le w_k$. Integrating $(w-G)^2$ over these intervals gives the combined lower bound
$$
T\;\ge\;\frac{S\big[(V-2G)^3-(M+8-G)^3\big]-3A(V+8)^2}{3SD}.
$$
At $V=2H-3$ the floor is $2.10448447880065\ldots\times10^{414}$. This omits all costs before $M$ and after the crossing. Run `python3 lower_clock_758.py` next to the linked transition map and raw timing rules to reproduce this calculation and check the graph on literal angular boundaries and axis excursions.
