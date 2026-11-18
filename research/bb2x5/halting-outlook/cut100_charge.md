# Line 34 · Which survivor gaps can increase a distant deficit?

For `1RB2LA4RA1LA3LA_0LA2RB3RB2LB---`, the [eight-cell condition](cut100.md) would prove nonhalting if it holds on every blank sweep. A failure requires an excess of closings attained past the first eight digits after cut 100. This calculation identifies the only complete pair of gaps that can give a positive contribution to that excess. End corrections and intervening negative contributions matter.

Work in ordinary data generated on the preceding sweep. Write O, N and C for digits 1, 2 and 3. Mark surviving openings after matching. A **run** is a maximal consecutive group of marked openings. Let $a_i$ and $x_i$ be the start and length of run $i$. Let $q_i$ be the number of Cs in the following gap of unmarked cells up to the next run. Let $p_i$ be the previous generation's generating bit on run $i$. It stays constant throughout each run because O is emitted by equal bits.

Every O in a complete gap is matched to a C in that same gap. Matching cannot cross a surviving opening. The number of Os is therefore $q_i$. Cs are rises of the generating bit and Ns are falls, so the number of Ns is $q_i+p_i-p_{i+1}$. The gap length is $3q_i+p_i-p_{i+1}$. The next sweep emits one C and one N between the two run starts. Its excess of Cs over Os on that interval is therefore

$$
3-(a_{i+1}-a_i)=I_i-p_i+p_{i+1},\qquad I_i=3(1-q_i)-x_i.
$$

The bit terms telescope over complete consecutive gaps. An unpaired end interval must use its actual digits. The [exact run-start formula](fold34.md#an-exact-test-one-epoch-before-b4) supplies the endpoint test for any cut.

When $q_i\ge1$, the corrected increment $I_i$ is at most −1. When $q_i=0$, its gap is exactly one N and $(p_i,p_{i+1})=(1,0)$. The next complete gap necessarily has $q_{i+1}\ge1$, since another N-only gap would have to start with bit one. Pair each zero gap with that next gap whenever it exists. These pairs are disjoint. Their corrected contribution is

$$
I_i+I_{i+1}=6-3q_{i+1}-x_i-x_{i+1}\le1.
$$

It is positive **only** when both runs have length one and the second gap contains exactly one C. Its sole matched O precedes that C. Starting with generating bit zero, any N in that gap must follow the C. The two-run block is therefore **ONOOC or ONOOCN**, namely `12113` or `121132`, with the first and third digits surviving. Merely finding the visible digits does not identify a positive contribution unless their matching roles agree. All other paired contributions are at most zero and each unpaired positive-$q$ gap reduces the sum. A final $q=0$ gap awaiting its partner has $I_i\le2$.

This gives a specific quantity to control in an induction. At the real epoch-1,300 tape there are seven positive pairs in the scan starting at cut 99, the first at digit index 105 (zero-based, left origin). The guard and cut-100 debts are both zero there. A viable bound must charge positive pairs against the actual intervening losses and opening reserve. We have no all-time bound for that signed prefix sum. The checker verifies the identity and the classification on 24,564 ordinary-word and exterior-debt combinations. [Checker](cut100_charge.py) · [Output](cut100-charge-verification.txt)

Tracing three generations backward rules out five consecutive positive groups anywhere after cut 100 on the blank orbit. The intervening groups now matter. A separate periodic construction builds large deficits across eight generations and can force B4 on a finite extension of the genuine tape. [Ancestry proof and physical controls](cut100_ancestry.md)
