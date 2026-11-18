# Line 26 · halting as a least fixed point

**Machine** `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA`. The physical halting entry is B3. Formal line 26 starts with a blank two-way infinite tape, head at 0 in state A. The public notes credit mxdys with the competing-overflows interpretation. The [pair derivation](research-log.md#line-26--one-inequality-decides-a-finite-halt) gives the concrete entry in five elementary steps, the two trips per epoch, all individual column rules, and the equivalence with the packed arithmetic model. [Public status](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved)

The criterion below uses ordinary periodic words at fixed columns, including columns the real tape has not yet allocated. It identifies a specific fixed-point question. Finite calculations also give certificates that a dangerous carry cannot overtake the width during the entire interval following a specified checkpoint, up to the next increase in width. A global blank-tape decision is still open.

## Ordinary words and a scalar test

The input is the infinite periodic word W₀=(aadd) repeated. Let T act on a word by feeding it into one **occupied** column initialized with (o,e)=(1,0), discarding empty outputs. Put Wⱼ₊₁=T(Wⱼ). There is no deletion of an initial letter here. A and B below denote counts of lowercase tokens, not TM states.

| Input | New bits | Output |
|---|---|---|
| a | o,e | a if e=0, otherwise b |
| b | 1−o,e | Same as for a if old o=1, otherwise empty |
| d | o,e XOR o | d if old o=0 or old e=1, otherwise empty |

The true fresh column halts on d. On a or b it changes state just as the occupied column would and consumes its first output a. This is the only distinction between the two models. In the all-ordinary system, an a or b that crosses all the currently nontrivial bits subsequently emits a forever in untouched columns; their bits remain (1,0). Call such a root operation a **wrap**. It corresponds to one allocation, regardless of how many further ordinary columns receive the unchanged a. Each root d stops at a finite index, the least index where both packed bits u=1−o and e are zero. Thus every fixed finite projection has a well-defined ordinary history. Starting from zero, the extension count in the total arithmetic process is exactly the number of wraps. Until a d overtakes that count, the process agrees with the tape.

Each Wⱼ is pure periodic and contains a d. To verify this inductively, the first four period representatives are `aadd`, `aad`, `aabbd`, `aaabbbd`. For j≥3 the representative has (3s,3s,s) letters (a,b,d), where s=3ʲ⁻³ is odd. Over one traversal o flips because the number of b's is odd. Over two traversals each d has seen both values of o, so e flips an odd number of times. Four traversals restore the column. At each fixed position of the word the four starting bit pairs there take all four possible values: after two traversals o agrees and e differs, regardless of the position because a cyclic shift has the same counts. A fixed a contributes two a's and two b's; a fixed b contributes one of each; a fixed d contributes three d's. The next representative therefore has counts (9s,9s,3s). These are valid periods even without asserting least period.

Let τⱼ be the root time of the first d that passes the lower j ordinary columns and arrives at cut j. It exists by the period calculation. Let the prefix of Wⱼ strictly before its first d contain Aⱼ copies of a and Bⱼ copies of b. Define

**p(j) = Aⱼ + ⌈Bⱼ/2⌉.**

This is exactly the number of wraps strictly before τⱼ. Every wrap reaches cut j. Conversely each safe arrival there sees an unchanged e=0 in column j. An a always passes as a, and precisely the first, third, fifth, … b's pass as a. Subsequent columns have so far received only a's, all of which wrap. The remaining b's stop at j. As τⱼ₊₁≥τⱼ, p is nondecreasing.

**The blank TM halts if and only if iteration of p starting at 0 reaches a fixed point.** First, if p(j)≤j, the virtual d at τⱼ visits the first unallocated index p(j), or an earlier d has already done so. This forces a concrete halt no later than τⱼ. Conversely, a first physical halt with width m arrives in the ordinary model at cut m. An earlier d there would already have reached the then-unallocated width, which was at most m. Thus this is τₘ and p(m)=m. The correspondence with the finite, positive-duration raw trips comes from the pair rules. In the absence of any such d the machine continues through infinitely many finite trips. Finally p(0)=2. Monotonicity makes the iterates from 0 nondecreasing and bounds them above by any j with p(j)≤j. A bounded nondecreasing integer sequence stabilizes, and an unbounded one cannot reach a fixed point. When a fixed point exists this iteration reaches the least one.

An independent way to see the alignment is that the first j virtual outputs at cut j are all a as long as the first j columns have been safely allocated. Every such allocation emits an a into all still-untouched virtual columns. Inductively the fresh-column word is the ordinary Wⱼ with its initial j a's deleted: T preserves any initial string of a's and a successful fresh first token deletes precisely the next emitted a. The first-danger calculation above gives p without assuming prior success.

The first thirteen p values are 2,2,3,5,5,9,9,10,10,12,17,17,18. Calculating the number of wraps at successive first d arrivals in the independent packed recurrence agrees on the overlap. Through 131,072 root cycles it gives the exact fixed-point iteration 0 → 2 → 3 → 5 → 9 → 12 → 18 → 34 → 71. The gap calculation below gives the next iterate p(71)=142, which excludes every candidate fixed point smaller than 142. The increment of p can be zero, including from 5 to 6. No lower bound p(j)>j at all j is known here.

## A safety bound while the current width is fixed

At a checkpoint with width m and packed integers u,e, choose 3≤k≤m. Let U=⌊u/2ᵏ⌋ and E=⌊e/2ᵏ⌋ be the high parts. The future token stream reaching this cut is a suffix of Wₖ. This follows from the virtual model even if the first k true columns were installed at different times.

On any safe arrival at cut k that does not allocate, the highest changed bit of U goes from 1 to 0, so U decreases by at least one. For input a the selector on high bits is 2E, and for b it is 2E+1. On a d arrival the selected high positions are those outside U. If i is the least index with Uᵢ=Eᵢ=0, the increment of E is 1+(U modulo 2ⁱ), at most U+1. This follows by toggling the selected bits through i; all selected lower bits were ones. These assertions use the total model so they also detect a hypothetical first overflow. Root operations that make no arrival at k leave the high parts unchanged. A safe arrival at U=0 must allocate, so at most U nonallocating safe arrivals remain.

Write U₀,E₀ for the high parts at the checkpoint and bⱼ for the number of d's before the (j+1)-st safe token in the actual suffix at k. Then until the next allocation, including the last preceding d, the high E is bounded by

**E₀ + Σ bⱼ, with j from 0 through U₀.**

Indeed a d following s nonallocating safe arrivals can contribute at most U₀+1−s. It is counted in bⱼ for exactly U₀+1−s values of j if the stream is continued through all U₀+1 safe tokens. Early allocation can only shorten the interval in question. It follows that an upper bound strictly less than 2ᵐ⁻ᵏ certifies every d at the current width.

Even without a phase, let Cₖ be the range of the partial sums over one whole Wₖ period with weight 6 on d and −1 on a,b, including the empty sum. The total over the period is zero. Consequently any interval, including one crossing period boundaries, has 6D−S≤Cₖ, where D and S are its dangerous and safe counts. In particular bⱼ≤⌊(j+Cₖ)/6⌋. For cuts 3 through 9, the range values are 6,9,14,22,35,50,127.

When the phase is known, bⱼ can be summed exactly without iterating U₀ times. If a period of the rotated stream has S safe and D dangerous tokens, then bⱼ₊ₛ=bⱼ+D. The phase at a checkpoint following a known number of root cycles is obtained by skipping groups of input periods restoring the occupied-column state and processing the residual part at each cut.

For example, at cycle 17 the exact state is (u,e,m)=(688,274,11). At cut 7 the read position is 12, counting the first position of the period as zero. Here U₀=5 and E₀=2. The six b values sum to 3, so E stays at most 5 before the next allocation, strictly below the threshold 16. Through the first 131,072 root cycles, 73 cycles increase the width. At the ends of those cycles the earlier square bound certifies 50 of the next fixed-width intervals. The phase-independent bound above certifies another 22, and the phase-sensitive computation certifies the remaining one. This calculation does not show that the criterion continues to hold after arbitrary future allocations.

Run `python3 column_frontier.py` with assertions enabled. It checks the local inequalities against physical column words, the cyclic bounds against direct counts, the constants and phases, and the two evaluations of p. [Observed output](column-verification.txt)


## Computing p(71) without replaying the root clock

An ordinary period ends in d at every cut. It does so at the root. The returning ordinary state is (1,0), so the last incoming d saw o=1 and old e=1 and was emitted. Encode the period by the pairs (A,B) preceding its successive d's. During a gap beginning at (o,e), exactly A+⌊(B+o)/2⌋ safe tokens are emitted, all of type e. Then o toggles if B is odd. Apply the single d rule and start a new output gap whenever d passes. The order of a and b within any input gap is immaterial. This gives the full period of gaps at any chosen cut.

At that cut follow the packed high counters through an entire gap at once. Write u=2h+l, with l a bit. The number of safe arrivals passed by the low bit is n=A+⌊(B+1−l)/2⌋. The final low bit is l XOR (B mod 2). Each of the n arrivals decrements h on the same selected positions, the set bits of e. Read those positions in increasing order as the digits of an ordinary binary integer z and put M=2 raised to the number of selected positions. The whole gap replaces z by (z−n) mod M and adds ⌊(n+M−1−z)/M⌋ wraps. Unselected bits of h stay fixed. This proof also covers the empty selector M=1. The d at the end then visits all high positions through the least index where both u and e have zero bits. Record the current wrap count as p at any newly reached cut.

The C++20 verifier implements this calculation at cuts 15 and 16 separately and checks agreement on every overlapping index through 71. It also compares grouped subtraction with individual a,b updates for all 32×32 starting pairs and all safe words of length at most six. Before the target's first dangerous arrival e has no high bit at or above the target, and u has at most one additional bit. The target differences 55 and 56 therefore fit in the 64-bit implementation. At cut 16, gap number 30,139,997 first reaches cut 71 and the wrap count is **142**. The finite result also buys a range by monotonicity: for every j from 71 through 141, p(j)≥142>j. Whether any larger fixed point exists remains open.

Run the following from this directory; no optional processor instructions are needed. [C++ source](column_gaps.cpp) · [Observed output](gap-verification.txt)

```sh
c++ -std=c++20 -O2 column_gaps.cpp -o column-gaps
./column-gaps
```
