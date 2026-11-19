# Wily Coyote from blank and from a family of alternate tapes

The later [integer-map certificate](WILY_INTEGER_MAP.md) reaches $2^{256}$ sweeps with a 769-bit suffix. The earlier checkpoint below establishes **$2^{192}$ sweeps from blank** for #531 and #532, with the same 577-bit suffix at that checkpoint. Each takes at least $2^{191}(2^{192}+1)>1.9701\times 10^{115}$ raw transitions. The eventual outcome of either blank tape is open. The four-carry sweep and raw-clock lower bound come from the [existing reduction and raw-tape checks](RANKINGS.md#wily-coyote-and-397--finite-blank-tape-runs).

At a sweep boundary, a word beginning with the eight bits **00000100** admits a complete decision for every finite choice of the remaining bits. For a continuation of length $n$, exactly $(2^n-(-1)^n)/3$ continuations halt. Every other continuation runs forever. This result starts the word in the initial sweep phase. In this notation the actual blank starts at the shorter word **00**. Bit 0 denotes tape symbol 2 and bit 1 denotes tape symbol 1.

## A decision for arbitrary continuations of 00000100

Remove the protected alternating prefix as in the reduction. The input sweeps at the first suffix cell are then driven by $(s_0s_1)^\omega$. For any allocated cell, the stream of arrivals from its left determines all its outgoing carries independently of later cells. A finite periodic arrival word drives each cell back to its initial bit after either one period or two. Every arrival flips the bit except $s_2$, so the parity of the number of flips per period determines which case applies. Dropping successful early stops yields an exact periodic stream at the next cell. It is important to retain the starting phase.

Write 30 for the two-event period $s_3s_0$, and similarly for the others. The four following periods form a closed set. The last column gives the next edge period after consuming its first event to allocate the indicated extension and propagating all remaining events through the allocated bits.

| Arrival period | Through bit 0 | Through bit 1 | At an empty edge |
|---|---|---|---|
| 1 | 30 | 03 | Halts on the first arrival |
| 2 | 2 | 1 | Appends 1100, next edge 30 |
| 30 | 2 | 1 | Appends 00, next edge 30 |
| 03 | 1 | 2 | Appends 0, next edge 2 |

Every row follows by applying the four carry rules to a single bit. For example, a 30 arrival at an empty edge first appends 00. The shifted arrival stream 03 at the first new zero produces constant 1 at the second zero, which in turn produces 30 at the next edge. Induction gives infinitely many safe extensions. Each successive extension requires a later sweep, and each individual sweep on a finite word terminates. The other two continuing edge cases enter this cycle in at most two extensions.

There is also a finite-word explanation for the equality of the rows 2 and 30. On a nonempty word, $s_3$ flips the first bit and stops. The following $s_0$ flips it back, sending the same carry to the rest as a single $s_2$ would have. On an empty word $s_3$ creates 00 and $s_0$ sends that word to 1100, exactly the extension of $s_2$. Thus 30 may be replaced by 2 even inside a longer sequence of sweeps acting on an arbitrary suffix.

Starting with period 01, the periods after the successive cells of 00000100 are **10, 32, 12, 3102, 011322, 23011, 2230, 2**. Once the initial eight bits are read, start at row 2 and scan any remaining bits with the first two table columns. The resulting row decides the outcome. For example, 00000100 runs forever, and replacing its final zero with a one produces 00000101, which halts.

For the count, identify row 2 with row 30. From either continuing class, exactly one of the two input bits enters row 1. Both bits from row 1 exit it. If $h_n$ counts length-$n$ continuations ending in row 1, then $h_0=0$ and $h_{n+1}=2^n-h_n$. This gives the stated formula.

## The opening of an edge period can hide opposite outcomes

For every $d\geq0$ there are two rotations of the *same* period that both begin and end with at least $2^d$ copies of 30. From an empty edge, one stream produces only $s_3$ extensions forever, while the other halts. Thus even all cyclic factors and their counts, together with arbitrarily long fixed beginning and ending segments of the period, can be shared by opposite examples.

The base periods are rotations **3030033030** and **3003303030**. Propagation from one empty edge to the next gives the two exact chains

$$
3030033030\longrightarrow30230\longrightarrow30\longrightarrow30,\qquad
3003303030\longrightarrow31030\longrightarrow11230\longrightarrow\text{halt}.
$$

To lift a pair, introduce one auxiliary letter $P$ that represents 30. When a stream starts with $s_3$, its action on a freshly allocated pair of cells is exactly its ordinary action on the *virtual initial bits 10*. The first $s_3$ flips the first 1 to 0, emits nothing and leaves the second zero in place, matching the actual allocation of 00. Read each of the following input blocks through virtual 10. Every block restores both bits, and its entire emitted word appears in the last column.

| Letter | Substitution | Emission |
|---|---|---|
| 0 | 312 | 0 |
| 1 | 11 | 1 |
| 2 | 03 | 2 |
| 3 | 231 | 3 |
| $P$ | $PP$ (the four events 3030) | 30 |

Write the base pair as $PP03PP$ and $P03PPP$. Apply the displayed substitution letter by letter $d$ times, then expand each remaining $P$ as 30. Both resulting words start and end with $P^{2^d}$ before expansion, and the words are still cyclic rotations. Since the virtual pair resets between blocks, its outgoing periodic stream is exactly the previous level's periodic stream, with the indicated initial phase. The first event at every lifted level is $s_3$. By induction the first stream always takes an $s_3$ extension and the other reaches the halting base case after $d$ extra extensions. The lift concerns arbitrary driving periods. The period at each actual blank edge has a specific phase fixed by its preceding cells.

### No finite automaton separates these two outcomes on all periods

The construction rules out a complete regular test on the written period, even one that can read the full period from the specified starting phase. Let $Q=03$. For every odd $L\geq 1$, consider the rotations

$$
V_+=P^{1+L}QP^2, \qquad V_-=PQP^{L+2}.
$$

In a virtual pair whose first bit is 1, each $P$ leaves the first bit in place, flips the second bit and emits 3 if the second bit was 0 or 0 if it was 1. Each $Q$ leaves both bits in place and emits 2 if the second bit was 0 or 1 if it was 1. There is an even total number of $P$'s in each period, so both virtual bits reset at the end.

The positive case emits $P^{(1+L)/2}\,2\,P$ at the next edge. This period begins with 3. Each of its tokens $P$ or 2 has the same action through virtual 10, so the following edge receives the pure 30 period. Every edge extension is therefore $s_3$. In the negative case the next edge period starts with **310**. It begins with 3, but reading that opening through virtual 10 emits **1** as its first output, so the following edge halts.

Suppose a finite automaton separated all periods whose every extension is $s_3$ from all halting periods. Reading $P^k$ induces a state transformation from a finite monoid, so these transformations are eventually periodic in $k$ with some positive period $p$. Choose $L$ as the odd part of $p$. After $d$ substitutions the written periods are

$$
P^{2^d(1+L)}R_dP^{2\cdot 2^d},\qquad
P^{2^d}R_dP^{2^d(L+2)},
$$

where $R_d$ is the same expanded substitution of $Q$ in both. Take $d$ large enough that all four exponents exceed the onset of periodicity and $p$ divides $2^dL$. The left powers of $P$ induce the same state transformation, and so do the right powers. The automaton returns the same answer on both words, contradicting the two proven outcomes. A sufficient regular test tailored to the actual blank periods remains possible.

## Exact blank computation

The [checker](wily_edge_stream.py) stores runs of constant 1, constant 2 or alternating 0 and 3. Every such run emits at most one run of one of the same three types. An input 1-run alternates its outgoing 3 and 0. An input 2-run leaves the bit fixed and emits a constant. Inside an alternating 0/3 run only the zeros emit and they all see the same bit. These observations prove the per-run transformation without expanding a long run.

At each cell the checker keeps an exact periodic arrival stream together with the number of its events belonging to the finite blank computation. It processes full periods in bulk, followed by the exact prefix that remains. The output count per period is independent of the initial bit, since only input 3 suppresses an emission. Once the event count fits inside one period, the checker retains the exact finite prefix. At a fresh edge it consumes the first arrival for allocation and rotates the periodic word by one event, or drops the first finite event. This procedure is the chronological sweep calculation evaluated by tape column.

| Completed sweeps | Suffix bits | SHA-256 of the ASCII bits in head-facing order |
|---|---:|---|
| $2^{96}$ | 291 | `2227cc873414ca1f243bc4281e0fa4f472146fffaab72223428979796be99bd1` |
| $2^{128}$ | 383 | `0b594c2242ceba0cd1a6c4d5ac6bd0388906f2ae0916910db037518ab0f377b0` |
| $2^{192}$ | 577 | `567df9a7f34a5764e1a90917ef2f35cfbb4984790de9560d8310261718d0f2d6` |

Through $2^{192}$ sweeps, extensions at suffix lengths 4, 8, 14, 22, 26, 31, 37, 41 and 65 receive $s_2$. The extension at length 30 receives $s_0$. Every other extension receives $s_3$. In particular every extension from length 69 through 575 creates 00. An induction establishing that every future extension receives $s_3$ would settle both blank tapes. The finite prefix at these edges does not establish the full periodic stream 30 required by the table.

Run from this directory with assertions enabled.

```sh
python3 wily_edge_stream.py --power 192
```

The checker verifies the periodic transitions, tracks all raw carry events by exact integer arithmetic and compares every sweep through 1,024 against literal suffix updates. It also compares with the earlier straight-line stream algorithm at two longer horizons and reproduces the previously archived $2^{96}$ digest when run with `--power 96`.
