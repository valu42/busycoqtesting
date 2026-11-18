# Line 13: a deadline for the next parity test

For `1RB3RA3RB4LA1LA_1LB2LA1LA---1RB`, **the blank orbit must settle the parity test at cell 155 before $1.1\times10^{93}$ defined instructions**. At the [saved checkpoint](pair13_checkpoint.json), after about $1.50751\times10^{35}$ instructions, that odd cell had received only B. Its first A either opens the next pair safely or leads to B3 two instructions later. The two possible outcomes have the same deadline. The eventual blank halting time remains unknown.

The [pair and productivity proof](pair13.md) supplies the finite evaluation of each root request, the odd frontier test, and the one-cell period counts used here. The new arguments below concern the clock, the phases attained in a finite strip, and the total work of evaluating source periods. They have executable finite checks and have not been mechanized in a proof assistant.

## How many source groups can postpone one frontier?

Start with the initial A at coordinate zero. Call each subsequent block `BABAB` one group. These boundaries occur at $1+5g$ root requests and differ by one request from the repository's canonical $5q$-request checkpoints. The first group and initial A together emit A at cut 4. At that boundary the four cells have ordinary symbols 2,1,4,4. Each subsequent group restores all four and emits BA at cut 4.

Suppose the strip before a later cut has safely entered its repeating cycle. Let $P$ be the word it emits there during one cycle, with an odd number of As. A fresh next cell encounters A within the first copy of $P$ and either triggers its test or becomes ordinary. On the ordinary states one traversal of $P$ interchanges the two classes $\{4\}$ and $\{1,2\}$: each A toggles classes and every B preserves its class. In particular both 1 and 2 map to 4, and 4 maps to a single state $u$ in the other class. One additional traversal suffices to enter $\{4,u\}$. Two traversals then restore the entire state at the same input phase. Over both traversals its emitted word again contains an odd number of As by the pair report. We use this complete-period word without reducing it to a primitive period.

Thus at cut $4+k$ the stream repeats in root time with period $2^k$ groups after at most $B_k=2^{k+1}-1$ groups, unless an earlier frontier has halted. The induction starts at $B_0=1$ and uses $B_{k+1}=B_k+2\cdot2^k$. For a target frontier we may project the earlier cells with the proved usual return contract: once its parent has opened that frontier all earlier cells are permanently clear. Until the frontier's first A, its B entries issue no deeper calls. The projected first-A deadline therefore applies to the actual run. If testing a previously unreached coordinate, an earlier halt is also possible.

The period $2^k$ is **exact for the joint strip state** at these group boundaries. The first $k-1$ ordinary cells beyond cut 4 return after $2^{k-1}$ groups. Their output has odd A count, so the last cell toggles its class once in parity. Two traversals restore it. By induction the $k$ class bits realize every binary pattern once per cycle: both values of the last bit occur at visits to each earlier pattern separated by $2^{k-1}$ groups. This statement concerns the mature cells. It supplies no random-phase law for opening a virgin cell.

At odd $h=4+k\ge5$, one more period after $B_k$ suffices for the first A. The number of root requests through that event is at most $R=15\cdot2^k-4$. On blank, the first A at an odd cell is a single opportunity.

## Converting that deadline to raw instructions

Put $Q=3\cdot2^k$, so $R=5Q-4$. The inherited [negative-half clock](streams.md#exact-timing-formulas-and-what-they-do-not-estimate) costs $15Q^2$ through the later canonical boundary of $5Q$ requests. This bounds all negative-half work before the target, since each completed request on the positive half returns in A.

On the positive side, let $J_x$ count rightward entries at cut $x$. A successful virgin block of four cells, starting at a multiple of four, emits at most as many requests as it receives. Each intervening single cell issues at most two calls per input. Thus each of the relevant cuts receives at most $8R$ entries by the target. For completed blocks before the target one may finish the last pending input with the usual child return to bound its output prefix. For the final partial block use the one-cell bound. At the deciding first A the odd frontier has had no earlier visits to its right. Counting the two directions across each traversed edge, and allowing five terminal instructions (two through B3, or five to complete a safe opening back at its parent), gives the conservative deadline
$$
T_h\le 15Q^2+16(h+2)R+5.
$$
At $h=155$ the decimal value is printed by the verifier. The estimate does not assume independence or mix different initial tapes.

## What a source period costs at large depth

If the blank run continues indefinitely, its total raw time at the canonical $5q$-request boundary satisfies
$$
T(q)=15q^2+O\!\left(q^{2\log_2\varphi}\right),\qquad
\varphi=(1+\sqrt5)/2.
$$
Here $2\log_2\varphi\approx1.3885$. In particular $T(q)/(15q^2)\to1$. The conclusion identifies the leading raw cost of completed source groups. Predicting a halt would additionally require a distribution or decision for the group containing the fatal first A.

To see why the positive half is lower order, write $L_k=a_k+b_k$ for the counts of A and B in the output at cut $4+k$ over its full root-time period. If $r_k$ counts odd cyclic B-gaps, then $a_{k+1}=b_k+a_k-r_k$ and $b_{k+1}=b_k+r_k$. Since $r_k\le a_k$, we have $L_{k+1}=L_k+b_k$ and $L_{k+2}\le L_{k+1}+L_k$. With $L_0=2,L_1=3$ this gives $L_k\le F_{k+3}$, where $F_0=0,F_1=1$. The long-run crossing rate at the cut is exactly $L_k/2^k$ per root group whenever that strip continues safely.

The startup work also needs a bound. The [four-cell certificate](pair13_potential.json) takes integer values from −19 to 0 on the reachable states. On **any interval** of successful inputs to such an aligned block, the output length is at most the input length plus 19, by subtracting the initial potential from the final one. Across an interval of $s$ successive cells, an initial and a final partial block cost a factor of at most eight each. The full blocks between them each add at most 19. Consequently a segment of $m$ input letters has at most $64m+152(s+1)$ descendants at the farther cut. Here a segment's outputs include all child calls, with their order preserved; these bounds apply equally to prefixes and to intervals between two root-group boundaries.

Split the root-time startup before $B_k$ at the earlier $B_j$. Over $[B_j,B_{j+1})$ the input at cut $4+j$ consists of two periods of length $L_j$, hence contributes at most $128 L_j+152(k+1)$ entries to cut $4+k$. Partial intervals use the same upper bound. The initial group contributes $O(k+1)$ by the same transfer from cut 4. Summing gives $O(\varphi^k+k^2)$ startup entries. After startup each further $2^k$ groups give $L_k$ entries. Thus through $q$ groups the cut receives at most
$$
O\bigl(\varphi^k+k^2+q(\varphi/2)^k\bigr).
$$
Use $k=4\lfloor(\log_2 q)/4\rfloor$ so the last cut is four-cell aligned. Every earlier cut costs $O(q)$ entries, across $O(\log q)$ cuts. Beyond it, the four-cell productivity bound decreases a nonempty word by at least one per block. Starting with $M=O(q^{\log_2\varphi}+(\log q)^2)$ entries, the total of all later entries is $O(M^2)$ by summing the decreasing lengths and allowing at most a factor eight inside each block. Positive raw work is at most twice the number of entries. Both the shallow and deep parts fit the displayed error term. The initial A offset between group conventions changes none of the bounds.

## Verification and next question

Run `python3 research/bb2x5/halting-outlook/timing13.py` from the repository root. It checks the initial four cells, enumerates complete reachable boundary states and every class-bit pattern through nine further cells, and checks actual circular words and Fibonacci bounds through cut 36. The measured comparisons use the saved $10^{14}$-group blank trajectory. At cut 36 the period predicts 30,510,150,827.467 crossings from its steady rate alone; the actual count is 30,510,151,011. The finite-time difference is allowed by the startup bound. [Verifier](timing13.py) · [Output and deadline](timing13-verification.txt) · [Actual fresh-edge checkpoint and shortest controls](pair13.md)

The immediate decision problem is the ordered input from the occupied prefix into 155. The mature strip's complete visit to every class-bit pattern cannot select that first event by itself.
