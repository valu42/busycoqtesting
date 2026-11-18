# Machine 31 and the fourth entry at an even cell

Machine 31 is `1RB3RB---4RA2RA_2LA2RA3LB4LB1LB`. Its blank-tape verdict is open. The run below completes **5,000,000,000,000,000,629,129,529,982,682,216 defined instructions**. The first remaining possible A2 is at **+172**. The exact clock, head, state and positive tape are in the [resumable checkpoint](frontiers/runs/line31-phase.json). The negative tape is determined by the group count.

There is a single word problem for this machine. Start with the infinite word
`AAAAA(BAAAA)…`, where the parenthesized block repeats forever. Apply the same two-cell transformation $F$ repeatedly. **The machine halts exactly when the fourth letter is B in some iterate.** If the first such iterate is number $j$, counting the seed as zero, the head reaches the undefined instruction A2 at coordinate $2j$. This statement includes the position of the start of each word.

## Deriving the transformation

Use the [certified negative driver](mixed-and-sweeps.md) and the [fresh-cell entry table and paired halt criterion](https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/edge31.md). A first A entering a virgin even cell sends BB to the virgin odd neighbor. The two symbols are then 4 and 3. A later B sent as the first letter to the next virgin even cell is followed immediately by A. The first B writes 2 and returns in A, and that second entry reaches literal A2. A first A instead opens the next pair safely.

For an ordinary cell, number symbols 1, 4, 3 by phases 0, 1, 2. $T_p$ reads a word starting in phase $p$. Each A increases the phase by one modulo three and each B decreases it by one. The table shows the output **before** changing the phase. An empty output is ε.

| Starting phase | Input A | Input B |
|---:|---|---|
| 0 | B | A |
| 1 | A | ε |
| 2 | A | ε |

If the physical entry stream at an even cell is $A w$, the proposed entry stream at the next even cell is $T_2(T_1(w))$. A leading B there represents the exceptional BA described above. Otherwise these are its real entries until a halt. The unopened odd neighbor and an ordinary cell can disagree precisely in that exceptional case. Every ordinary cell emits at least one letter in each three consecutive inputs. A single root request can travel through only a finite previously opened strip before opening a fresh pair or halting, so the first bad entry of the infinite-stream calculation is physically reached in finite time.

Set $F=T_2\circ T_0$. Four As from phase 0 emit BAAB and end in phase 1. BAAB from phase 2 emits AAA and ends in phase 2. Therefore, for **every** suffix $w$,

```text
F(AAA A w) = AAA T₂(T₁(w)).
```

The true root input is an initial A followed by the certified replies `(ABAAA)…`, equivalently `(AABAA)…`. Prepending three As gives exactly the seed `AAAAA(BAAAA)…`. Induction now proves the fourth-letter criterion. Each surviving iterate starts with AAA, and its remainder is the physical even-cell history. The fourth letter in the first failing iterate records the B that initiates A2.

The single-symbol distinction in this seed matters. The comparison word `(BAAAA)…` differs only at its first letter. Under $F$ its successive periods are **BAAAA → ABBA → AAAABBA → AAAABBA**. The last word is an exact fixed infinite stream. The true seed changes its initial B to A and follows a different orbit. Separately, starting the *physical* source one place later, at `(ABAAA)…`, gives physical periods ABAAA → A → ABBAAAA → ABBAAAA. Both controls follow by applying the three-row table to one or three periods.

## Testing four cells upstream

The earlier two-cell criterion requires the physical even parent to begin ABABAA or ABABABB. A parent four cells upstream must start with one of **3,256** minimal prefixes. Their lengths range from **11 to 40**. The unique shortest is **AABAAABAAAB**.

To generate these words, consume the first parent A and use ordinary phases (1, 2). Branch on incoming A and B. Retain a branch while its two-cell output is a proper prefix of either target, accept on a full match and discard on a mismatch. Each pair emits a letter within nine inputs, so the search is finite. The checker replays every accepted word and its one-letter-shorter predecessor against the literal physical rules. Every full word reaches A2 at +4 and every predecessor completes.

A finite prefix of the root source always leaves both kinds of behavior possible if its continuation is free. From any ordinary phase $p$, input B repeated $p$ times followed by A emits exactly B. To emit exactly A, use B from phase 0 or A from phase 1 or 2. Compose these choices through the finite opened strip. One can send a first B to the next virgin even cell, or send it the entire safe periodic source `(ABBAAAA)…`. The latter inverse construction gives an ultimately periodic input because each inverse uses only a finite phase. This explains why a proof using only a finite observed prefix needs an additional restriction from the true periodic source.

## Recovering a physical checkpoint

The worker uses a purely periodic input at coordinate zero, which permits exact counts for long runs. It carries the following initial phases and preliminary letters. Removing these letters from the aligned word gives the physical even input or the ordinary odd input after its opening BB.

| Coordinate | Preliminary word | Initial phase |
|---|---|---:|
| 0 | ε | 0 |
| 1 | B | 0 |
| 2 | A | 2 |
| 3 | AB | 2 |
| 4 | AA | 1 |
| 5 | AAB | 1 |
| Every even coordinate from 6 | AAA | 0 |
| Every odd coordinate from 7 | BAAB | 2 |

On an even row, process the preliminary word and the first physical A. On an odd row, process just the preliminary word. In both cases the output equals the next preliminary word and the ending phase equals the physical ordinary starting phase. This directly verifies the six-row initialization and the repeating pair. For a finite horizon, a partial preliminary word contributes zero ordinary entries.

For $N=5G$ completed root requests, let $c_x$ count physical entries at coordinate $x$, including the opening BB on each reached odd cell. The positive excursions use $2\sum_x c_x-N$ instructions by counting both directions across each internal edge and the $N$ returns to the negative half. The negative driver uses $2N^2+3N$ more, finishing in state A at coordinate zero. The final ordinary phases give every visited positive symbol. No unvisited cell contributes to the count.

The worker transforms a period once if its signed letter count is zero modulo three, and three times otherwise. This restores the initial phase. It computes the image length of the final partial period separately. At the chosen split it streams finite pieces in chronological order. A piece with $n$ letters and $b$ Bs advances any initial phase by $n+b\pmod 3$. This gives each piece its exact starting phase and permits parallel evaluation.

At $10^{16}$ groups the rightmost visited coordinate is +171. The physical even prefixes at +166, +168 and +170 are ABAABABAAB, AABAA and ABA. The first two permanently clear A2 at +168 and +170. ABA at +170 still admits both target continuations. The earlier independent [18-trillion-group checkpoint](https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/edge31_checkpoint.json) left +142 as the first candidate.

## Reproduction

From `research/bb2x5`, use Python 3 with assertions enabled and a C++20 compiler. Omit `-fopenmp` for a single-threaded build. The split affects work and memory, and has no effect on the represented computation. Split 52 uses a period of about 4.72 billion bits. Smaller splits trade memory for additional streaming time.

```sh
c++ -O3 -std=c++20 -fopenmp line31_phase.cpp -o /tmp/line31-phase
export OMP_NUM_THREADS=4
python3 line31_phase.py --check --engine /tmp/line31-phase
python3 line31_phase.py --engine /tmp/line31-phase --groups 10000000000000 --split 43 --compare frontiers/runs/stream-31.json
python3 line31_phase.py --engine /tmp/line31-phase --groups 10000000000000000 --split 52 --compare frontiers/runs/line31-phase.json
```

The tests exhaust all 4,095 supplied A-initial words through length 12, including 199 physical halts, and check all 3,256 four-cell triggers. Four small blank runs compare the worker with a literal TM and three split choices. The older $10^{13}$-group run agrees on the complete checkpoint. These checks establish finite computations. A complete blank-tape proof in Rocq remains open.
