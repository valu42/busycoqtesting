# A billion-unit terminal-free strip at multiples of a power of three

Put $k=128$ and let $M$ be any positive multiple of $6\cdot3^k$. On a blank-compatible #758 or #153 counter trajectory, a halt or exceptional restart cannot occur at any mass
$$
M+1152\ \le\ a+2c\ \le\ M+1{,}000{,}000{,}000
$$
after the first 128 calls. This excludes a whole interval at once, regardless of the direction in which the trajectory enters it. The machine may reset, jump or take ordinary bulks throughout such an interval. Each live counter call increases mass, so entering the strip alive forces it to leave by its upper edge.

For example put $P=3^{292}$ and $M=2P$. From the [conditional merged checkpoint](POWER_GATES_758.md) $A(1,P+1{,}934{,}340)$ the machine must reach mass above $2P+10^9$ alive. The same holds starting afresh at *any* reset in the displayed strip. The conclusion concerns mass. It neither identifies a reset beyond the upper edge nor proves that the blank reaches the checkpoint. The known halting basin lies much farther ahead.

## Translating an ordinary inverse tree

Let $W=a+2c$. On the blank-compatible domain the right counter is odd except at an even reset. Every halt or exceptional restart has odd $c$ and gap $a-c\in\{1,2,3\}$. Its ordinary predecessors are given by the [exact inverse rules](TERMINALS_758.md). A target $(a',c')$ admits the following predecessor formulas before applying physical guards.

| Condition | Potential predecessor |
| --- | --- |
| $a'\equiv5\pmod6$ | $(b,c'+b-1)$, $b=(a'-2)/3$ |
| $c'\equiv5\pmod6$ | $(a'+4q+3,4q-1)$ or $(a'+4q+3,4q+1)$, $q=(c'-5)/6$ |

At the terminal subtract the reference pair $(M/3,M/3)$. Along an ordinary inverse branch propagate the reference by the corresponding homogeneous linear rule. A jump pulls $(A,C)$ back to $(A/3,C+A/3)$ and a bulk to $(A+2C/3,2C/3)$. The reference mass is always $M$. Its two coordinates initially are multiples of $2\cdot3^k$, and after $i$ backward steps both are multiples of $2\cdot3^{k-i}$. Hence, until the last of the $k$ inverse steps, subtracting the reference preserves both residue tests modulo six and yields exactly the same inverse formulas for the signed differences. An original ordinary ancestry of depth $k$ therefore yields a signed ancestry of depth $k$. Signed predecessors may include choices that violate an original guard, which is harmless for exclusion.

The signed tree needs only the region
$$
a_{\rm s}\ge-4,\qquad c_{\rm s}\ge-13,\qquad W_{\rm s}=a_{\rm s}+2c_{\rm s}\ge0
$$
if the original history stayed at $W\ge M$. To see the first two inequalities, start at the terminal with $c_{\rm s}=W_{\rm s}/3-h/3$, where $h$ is its gap. At every prior point write $c_{\rm s}=\alpha W_{\rm s}+e$. A reversed jump sends $(\alpha,e)$ to $((1+\alpha)/3,(4\alpha+e-1)/3)$. A reversed bulk sends it to $(2\alpha/3,(2g\alpha+2e-\eta)/3)$ with $(g,\eta)=(5,7)$ or $(9,13)$. For that bulk the right reference at its forward input is a multiple of four, so its two mass and right-coordinate corrections are exactly the original ones. Equivalently these identities follow directly from the two signed inverse formulas. The rectangle $0\le\alpha\le1/2$, $-13\le e\le2$ is invariant, as in the [post-bulk theorem](BULK_TERMINAL_SIEVE_758.md). Consequently $c_{\rm s}\ge-13$ and $a_{\rm s}=W_{\rm s}-2c_{\rm s}\ge-4$.

The signed terminal has odd $c_{\rm s}$, gap 1, 2 or 3 and $0\le W_{\rm s}\le10^9$. These conditions give 500,000,000 candidates. The verifier searches all their signed predecessor trees inside the three bounds above. It permits both bulk predecessors regardless of the original physical coordinates and includes both right residues for every candidate gap. The deepest ancestry has **127** edges. Across the entire sweep it visits 3,250,121,406 signed nodes counted with multiplicity. Thus 128 ordinary calls immediately before such a terminal are impossible if they all start at mass at least $M$.

## Short histories after a reset or exception

At a putative terminal in the stated strip, all the previous $k$ calls start at mass at least $M$, since each adds at most nine. If they are all ordinary, the signed tree excludes the terminal. Otherwise consider the last nonordinary call among them.

A regular return gives a reset at $A(1,s)$ with $s\ge M/2$. From an odd reset the first $k$ jumps are legal. After $i$ jumps the right counter is $s+1-3^i+2i$. From an even reset the opening move gives $A(3,s+3)$, after which $k$ jumps are legal and the right counter after $i$ jumps is $s+5-2\cdot3^i+2i$. These formulas stay positive through $i=k$ because $s\ge3^{k+1}$. Positivity after a proposed jump verifies its guard. This also covers a last nonordinary call that is itself the even opening.

An exceptional restart at mass $W$ gives $A(W+6,1)$. Its first $k$ ordinary bulks are legal. Indeed the initial scalar $x_0=\lfloor(c+1)/4\rfloor+3$ equals three, each bulk changes $x$ to $\lfloor3x/2\rfloor$ and subtracts $4x-9$ from the left counter. The sum of all $k$ proposed decrements is below $24(3/2)^k<M$. Hence none of these three kinds of nonordinary call can be followed by a halt or another exception within the remaining part of the $k$-call history. A fresh reset inside the strip has the same protected opening, establishing the claim for that initial condition as well.

## How many terminal masses are possible globally?

Across all blank-compatible histories from resets, the number of distinct masses in $[X,2X]$ that can host a halt or exceptional restart is
$$
O(X^\sigma),\qquad \sigma=\log_3\big((1+\sqrt{17})/2\big)=0.85618343\ldots .
$$
The same bound holds for the blank trajectory and for the union over trajectories starting at a bounded mass. In fact an interval of length $L$ with lower endpoint $X\ge L$ has $O(L^\sigma)$ eligible masses, with a uniform constant for reset-started histories. This counts integer locations at which an event is possible. It gives no probability that a particular orbit halts.

Choose $n=\lfloor\log_3(L/64)\rfloor$, taking the bounded small lengths separately. Immediately before a putative terminal in this interval, the last $n$ calls, if present, start at mass at least $X-9n\ge X/2$ for sufficiently large $L$. A return or opening there supplies at least $n$ subsequent legal jumps, using the formulas above and $3^n\le L/64$. An exceptional call there supplies at least $n$ subsequent bulks. Hence all of those last $n$ moves are ordinary. A history starting recently at a reset cannot produce a terminal in fewer than $n$ calls either. From bounded initial mass, the first arrival at $X$ requires more than $n$ calls for sufficiently large $X$.

Fix the terminal gap $h$ and a fine inverse word of length $n$, in which each bulk predecessor specifies its sign. Two viable terminal pairs $(c+h,c)$ and $(\tilde c+h,\tilde c)$ differ by $(d,d)$ for $d=\tilde c-c$. After $i$ inverse steps their difference is $d(A_i,C_i)/3^i$, starting from $(A_0,C_0)=(1,1)$. A jump replaces the numerator pair by $(A_i,A_i+3C_i)$; either bulk replaces it by $(3A_i+2C_i,2C_i)$. Thus $A_i\equiv C_i\not\equiv0\pmod3$ at every step. Integrality at level $n$ implies $3^n\mid d$. Every fine word therefore permits at most one class of $c$ modulo $3^n$, or $O(1)$ possibilities in a mass interval of length $L$.

A jump predecessor is possible only from an odd left counter and leaves that parity odd. Both bulk predecessor choices flip it. If $o_n,e_n$ bound word counts starting at odd and even left parity, respectively, then $o_n=o_{n-1}+2e_{n-1}$ and $e_n=2o_{n-1}$ with $o_0=e_0=1$. Thus both are $O(\lambda^n)$ for $\lambda=(1+\sqrt{17})/2$, the same [fine-word count](COARSE_ENTROPY_758.md) used for ordinary directions. Summing over the three possible gaps proves the bound. In particular every such interval contains a consecutive terminal-free subinterval of length $\Omega(L^{1-\sigma})$ by counting the gaps between eligible masses.

## Reproduction

Compile and run [signed_ancestry_758.cpp](signed_ancestry_758.cpp) with a C++17 compiler. The default width is one billion. The optional argument selects a smaller width; for $10^6$ the checker visits 3,245,263 nodes and the maximum depth is 121.

~~~sh
c++ -O3 -std=c++17 signed_ancestry_758.cpp -o signed_ancestry_758
./signed_ancestry_758
~~~
