# A right extension that hides debt for arbitrarily many line 35 sweeps

**Theorem.** Let $k\ge2$ be a power of two and $L=2k-1$. Take any normalized line 35 word ending in a closing whose next $L$ sweeps succeed. One can append material to its right, preserving every original digit and all $L$ successive guard readings, so that the altered tape reaches B4 on sweep $L+1$. The construction specifies every appended digit. The blank-tape decision remains open. The theorem identifies what a proof based on the left boundary must establish about the actual right material. [Line 35 sweep and stream definitions](line35-guard-stream.md)

## The block

Use physical symbols $O=1$ and $C=2$. Set $B_k=C O^{3k-2}$. Feed its right end the chronological boundary signal of a single terminal closing, which supplies letter 2 at every sample (debt one, survivor zero). The block emits letter 2 at offsets $0,\ldots,L-1$. At offset $L$, keeping those preceding inputs and changing the incoming debt to any $d\ge1$ gives outgoing debt **exactly $d+1$**. Hence the suffix $B_k^m C$ presents the same first $L$ samples as $C$ and sends debt $m+1$ on the next sample.

## Why the first change occurs there

Read $B_k C$ from the right. It begins with the permanent pair $C,O$, followed by $k-1$ clean triples $(O,O,O)$, followed by the outer $C$. Designate the initial sample as phase zero. At every even offset $2t$ the triples have form $(O,a_i(t),O)$. Write $h_i=[a_i\ne O]$. The two-sweep recurrence is $h_i(t+1)=h_i(t)\mathbin{\mathrm{XOR}}h_{i-1}(t)$ with $h_{-1}=1$ and all initial $h_i(0)=0$. Thus $h_i(t)=\binom{t}{i+1}\bmod2$. The pair acts as virtual previous center $C$. [Three-cell calculation](line35-pascal.md#the-two-cell-boundary-and-the-triples)

The outermost inner center has index $k-2$. It stays $O$ for $0\le t<k-1$, and becomes neutral $N$ at $t=k-1$. A $0\to1$ transition of $h_i$ gives center $N$. A $1\to1$ transition gives center $C$. At offset $2t$ a clean outer triple sends zero debt and survivor $[a_i\ne C]$. At offset $2t+1$ it sends debt $[a_i=N]$ and survivor $[a_i=O]$. Consequently the outer closing receives letter 1 at every offset through $2k-2$. It emits letter 2 and stays a closing on each such input. At $L=2k-1$ it receives debt one and emits debt two.

To prove the increase for **arbitrary** $d\ge1$, inspect every opening at this critical sample. The row $\binom{k-1}{j}$ is odd for $0\le j<k$ since $k$ is a power of two. The preceding row $\binom{k-2}{j}$ is odd exactly at the even $j$ in that range, as follows by expanding $(1+X)^{k-2}$ over the two-element field. Thus at $t=k-1$ the centers in order from the right are $N,C,N,C,\ldots,N$. For their intermediate triples at offset $2t+1$, the shared three-cell rule gives the following outgoing letters, also in right-to-left order.

| Previous center | Current center | Three outgoing letters |
|---|---|---|
| $C$ | $N$ | `0 2 2` |
| $N$ | $C$ | `0 2 0` |

Neither row has a surviving opening (letter 1). The opening of the boundary pair also consumes a unit of debt. The outer closing adds one. Starting with debt one at the right of $B_k$, every opening in the block was matched and the final debt was two. Its physical balance at this sample is therefore −1. Increasing the incoming debt leaves every opening matched, and the block adds exactly one to any debt $d\ge1$. Its symbols at this sample depend only on earlier samples. This proves the asserted identity, and induction over copies proves it for $B_k^m C$.

## Extending a finite tape

Write the given word as $P C$. Replace its final $C$ by $B_k^m C$. Since $B_k$ begins with $C$, the altered word still begins with the entire given word $P C$. Follow the interface immediately to the left of the replacement at its fixed distance from the new right end. For the first $L$ samples, all columns of $P$ and all new columns on their left see the same chronological inputs as before. Their survivor bits, outgoing debts and guard readings agree by the one-cell rule. Thus the first $L$ sweeps succeed. The altered tape can take a different number of elementary instructions on these sweeps.

At offset $L$ the replacement supplies debt $m+1$. At most $|P|+5L$ cells separate the interface from the guard because one successful sweep adds at most five columns. Each can consume at most one unit. Taking $m\ge |P|+5L+5$ leaves at least six units at the guard and forces B4. The exact threshold for a fixed history can give much smaller examples. [Finite-history formula](line35-guard-stream.md#what-a-chronological-invariant-must-distinguish)

For the true epoch-1 word `2`, seven copies suffice at both $k=2$ and $k=4$. The resulting 36-cell and 78-cell altered tapes shadow three and seven successful sweeps, respectively. From the normalized start the literal machine reaches B4 after 791 and 2,645 defined instructions. The genuine word succeeds on each corresponding sweep. The checker also evaluates the block identity for every power of two from 2 through 256, including the match of every opening at the critical sample. [Executable replay](line35_guard_stream.py)

The exact multiplicity can also be read off a genuine tape. If the genuine sweep at offset $L$ succeeds, delete its terminal closing to obtain the strip $S$. Its internal deficit is below six. The sharp threshold is $6+b(S)$, so the least multiplicity that reaches it is $5+b(S)$. At blank epoch 181 choose $k=32$. The entire 367-cell word is preserved, and the next 63 guards agree. On the following sweep the genuine guard debt is zero. With 273 copies it is five and the sweep succeeds. With 274 copies it is six and B4 follows. The checker replays both altered trajectories with exact word matching.

Every ordinary output body produced by a successful sweep has alternating non-opening symbols, since $C$ and $N$ mark opposite changes of a bit. A newly inserted stretch of consecutive $B_k$ blocks contains closings separated solely by openings. A proof can exploit the actual right-hand material and its history of generation. Accepting arbitrary right extensions after any fixed number of correct boundary readings admits the construction above whenever those readings last long enough.
