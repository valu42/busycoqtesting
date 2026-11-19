# What fixed-modulus filters can miss at scale 74

One exact rational orbit passes through the entire scale-74 mass band without a reset, satisfies all the ordinary real branch inequalities, and has compatible coordinates modulo every positive 64-bit integer. It also has coordinates in the $p$-adic integers for every prime $p\le2^{64}$. Its coordinates involve a nontrivial denominator, so this is not a Turing-machine trajectory. It identifies what an argument relaxing integrality to these simultaneous congruence and size tests must still rule out.

Use $u=(a+2c-1)/2$ and $d=(c-1)/2$. Take the periodic word consisting of one odd jump $J$ followed by 20 blocks $B$, each of which is two ordinary rule (b) moves. One period increases $u$ by 102. Its map on $d$ is of the form $(Qd+Au+C)/m$, where $Q=3\cdot9^{20}$, $m=4^{20}$ and $A=-9^{20}$. The invariant graph is

$$
d(u)=\lambda u+\gamma,\qquad
\lambda=\frac{9^{20}}{q},\quad
\gamma=\frac{102m\lambda-C}{q},\qquad
q=Q-m=36{,}472{,}995{,}277{,}659{,}158{,}627 .
$$

The integer $q$ is prime and exceeds $2^{64}$. The verifier checks the full factorization of $q-1$ and that 2 has multiplicative order $q-1$ modulo $q$. The reduced denominator of $\gamma$ is $q^2$ and $d(u)$ has the same denominator at every integral $u$ on this phase. This excludes integer states while allowing reduction modulo every modulus coprime to $q$.

At a $B$ phase the rational coordinate is zero modulo four. All branch inequalities hold starting at a mass coordinate just below $H-2G$, where $G=10^{10}3^{74}$, and their margins increase with each period. The verifier uses exact fractions to check all 21 phases, including the two ordinary guards in each $B$. It chooses the initial period phase so the orbit crosses $u=H-5G/4$ at the start of a period. This supplies both past and future through the actual size regime. It neither proves that the blank machine misses the scale-74 corridor nor supplies any integer path bypassing it. [Ordinary affine words and guards](EXCURSION_POWERS_758.md)

~~~sh
python3 rational_gate.py
~~~

## Integer witnesses with finite histories in both directions

At $T=H-5G/4$, **at least $2^{95}$ distinct integer states of mass $2T+1$** can execute 144 ordinary updates before the cut and 147 after it without a halt or reset. This is a statement about arbitrary starts. The [reset-conditioned calculation](SCALE74_ANCESTRY.md) identifies only 700 possible first crossings with the specified earlier gate reset.

Use motifs $BJ$ and $JB$, each containing three ordinary updates. Their endpoint formulas at the same initial $u$ are respectively $(27d-4u+44)/4$ and $(27d-9u+29)/4$, both at $u+7$. Prescribe 48 motifs before the cut and 49 after. In the 48 past positions, fix one motif whenever the input $u$ is $-3\bmod27$. This occurs at exactly two positions. The remaining 46 past choices yield distinct $d\bmod27^{48}$ at the cut. Indeed at the last differing motif the output difference modulo 27 is $\pm5(u+3)/4\ne0$, and every following common motif multiplies that difference by $27/4$. Each of the 49 future motif choices is distinguishable by determinism.

Every one of these prescribed words has a physical integer witness. Invert the word from terminal $d=x$. As in the [integer-word construction](CUT_758.md), exactly one class of $x$ modulo $27^{97}$ gives integral intermediates and the specified two bulk residues. Here the final $u_f=T+343$ satisfies $\lfloor7u_f/16\rfloor-\lceil u_f/16\rceil\ge27^{97}-1$, so there is an admissible $x$ in that interval. Its distance from both 0 and $u_f/2$ is at least $u_f/16$. The reverse margin proof for $B$ and $J$ loses at most a factor of three per block, and $(T-336)/(16\cdot3^{194})>100$. All 194 reverse guards hold, including the two moves of each $B$. This proves the count. The checker verifies the numerical bounds and replays 132 representatives on the ordinary integer map.

~~~sh
python3 twosided_gate_words.py
~~~
