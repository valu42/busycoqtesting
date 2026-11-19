# BB(6) line 596, bbchallenge ID 176107

The machine is `1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD`, started in state A on zeros. Its blank-tape halting status is open. The [pinned rankings](https://github.com/valu42/busycoqtesting/blob/175f2c272c1d5dfd1ff16f277839f19877cb2364/research/bb6/RANKINGS.md#L472) place it at rank 390.

The proposed comparison with a proved nonhalter first fails during return **175** of the blank run. After **24,560,125,895,592,097,263,948,984,175,956,746,215,829,548,953** successful elementary transitions, line 596 has just executed D0 and is reading a one in A where the comparison requires a zero. Line 596 completes that return. The replay below follows the actual machine through **1,500,000,000 completed returns**.

## Previous work

Fractal Geometry Explorer derived the round map, published a Lean proof of its soundness, identified the halting tail `011010101011` and reported two million rounds from blank. Their count of ones includes one fixed one from the marker. Throughout this note, their count is $n+1$. The round reduction and the discovery of that tail are theirs. [Prior analysis, proofs and programs](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/tree/3c7d4736362e77b987beb5c043056b24994b5a60/holdouts/1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD)

BusyCoq proved nonhalting from blank for a machine that differs at D0. It writes one and moves left into E. Line 596 writes zero and moves left into A. Dennis Koshta identified the exact condition for the two runs to rejoin immediately after this difference and checked two billion steps. His replay showed that the existing nonhalting certificate admits configurations which violate the condition. The witness here places the first violation on the actual blank run. [BusyCoq, nonhalt216](https://github.com/ccz181078/busycoq/blob/33209bc7dc282b38c8cd6be507bfc551fea56108/verify/FARv3.v#L648) · [Koshta, P-728](https://github.com/DennisKoshta/denniskoshta-portfolio/blob/82bf32df4f70f044eaa13a8a1ddad7b6e2614198/public/busy-beaver/machines/1RB1LF_1LC0RD_---1LA_0LA0RE_1LA1RA_1LB0LD/status.json)

The repository register and Fractal Geometry Explorer both list the exact machine as open. A search on 19 November 2026 compared the transition table with public BusyCoq results, the open pull requests and GitHub code results for both common spellings of the halt instruction. We found no published decision for this blank start. The search cannot establish worldwide priority.

## Exact returns

Write $P(n,x)$ for a configuration with D scanning a zero, all zeros to its left, and the word $011101\,1^n x$ immediately to its right. Words have implicit trailing zeros. Write $L(k,v)$ similarly with A scanning a zero and $110110(1110)^k v$ to its right. The initial 51 steps reach $P(2,\varepsilon)$. The next 60 steps from any $P(n,x)$ reach $L(0,1^{n+4}x)$ without reading $x$.

From $L(k,v)$ the next $9+4k$ steps reach B reading the first bit of $v$, with $1010011(0011)^k$ to its left. The complete local crossings used here are as follows. The arrow names the direction in which the head enters or leaves the finite window. The head never reads outside the window before its last move.

| Entry | Input | Exit | Output | Steps |
|---|---|---|---|---:|
| A → | 0110110 | B → | 1010011 | 9 |
| B → | 1110 | B → | 0011 | 4 |
| B → | 1111 | A ← | 1101 | 9 |
| A ← | 0011 | A ← | 1101 | 6 |
| C ← | 0011 | C ← | 1111 | 4 |
| A ← | 1010011 | A ← | 1101101 | 17 |
| C ← | 1010011 | D ← | 0111011 | 17 |

They give $L(k,1111v)\to L(k+1,1v)$ in $35+10k$ steps. The equality $1(1101)^k=(1110)^k1$ explains the restored left marker. When this rule ceases to apply, the evaluator takes elementary transitions on the right, opening individual `0011` blocks to its left as needed. When A or C moves left into the first untouched block, the last four rows cross the remaining blocks and the marker. A returns to $L$ with a leading one on the right word. C returns to $P$ with $4k+1$ ones before the right word, where $k$ is the number of untouched blocks beyond the marker. Reaching C0 ends the calculation in a halt. Exceeding an implementation budget reports an incomplete calculation.

## The first failed comparison

Let $p$ be the head position at D0. When cell $p-1$ holds zero, line 596 takes D0, A0, B0, C1, while the published nonhalter takes D0, E0. Both reach A at $p-2$ and leave ones at $p-1,p$. To detect the first failure on line 596, change its D0 destination to a fresh state G that takes the normal A0 instruction on zero and stops on one. Both machines take the same number of transitions until the detector fires. All seven window crossings and the two initialization identities hold for this detector as well. The checker verifies them directly from both tables.

After 174 returns the real machine is at $P(139072280281797265838838,\mathtt{01101011})$ at elementary transition 13815070816270554710970280936463660063164325600. The detector stops 10745055079321542552978703239493086152665223353 transitions later. At this point the original has a defined A1 instruction. The verifier checks its return to another $P$ boundary. The numbering here counts successful moves from blank, with the first inspection of an undefined instruction occurring before any further move.

## All empty-suffix starts that halt in the first 36 returns

For **every nonnegative integer** $n$, $P(n,\varepsilon)$ completes its first 35 returns. On return 36 it halts for **exactly 128 residue classes** of $n$ modulo $3^{36}=150094635296999121$. The least nonnegative representative is **44,932,349,626,276**. The blank start reaches $P(2,\varepsilon)$ at move 51.

For every integer $j\ge0$, the machine started at $P(44932349626276+150094635296999121j,\varepsilon)$ halts during its **36th return**. In the case $j=0$ it makes exactly 1427510327116636722563042017802061340 successful transitions from that starting tape.

For a fixed tail $x$ and residue $r\in\{0,1,2\}$, compute the return at $n=300+r$. If the interface closes without opening the left marker, adding $3h$ to $n$ adds $h$ untouched `0011` blocks after the first batch of sweeps. The subsequent interface runs and their right words are identical. On returning to $P$, the extra blocks give $4h$ additional ones. A halting interface reaches the same missing instruction for every $h$. Thus a verified row either halts or has the exact form $(3t+r,x)\mapsto(4t+c,y)$ for $t\ge100$. For the stated family the residues are `111111111111111211110111111011212102`. The verifier checks every affine row and the representative at $j=0$. Since $150094635296999121=3^{36}$, the extra summand at row $i$, indexed from zero, is $4^i3^{36-i}j$. It leaves all 36 branch choices unchanged.

The breadth-first checker [shortest596.py](shortest596.py) explores all three residues from each tail at minimum distance below 36. It verifies 1,959 affine rows and discovers 774 tails, including the frontier. The only halting rows occur at depth 36, at the tail `011010101011` with residue 0 or 2. Every path that halts in 36 follows edges increasing the minimum distance by exactly one. Enumerating their labels gives 128 distinct initial classes. After $i$ choices, write the initial counter as $a+3^it$ and the current one as $b+4^it$. The next choice determines exactly one digit of $t$ modulo 3, since $4^i=1\pmod3$. This recovers the classes without enumerating $3^{36}$ words. The 300 starting values below the affine threshold each complete 36 returns in the direct checker. They give no additional classes or earlier halts. Each of the 128 representatives also agrees for all 36 returns with the independent zone evaluator.

## Reproduce

From this directory, use Python 3 with assertions enabled. The checker uses only the standard library. For the long replay, use a C++17 compiler, 64-bit unsigned long and GMP.

~~~sh
python3 verify596.py
python3 shortest596.py --list
python3 return596.py --guard --returns 200
python3 return596.py --returns 600
python3 return596.py --rules rules.tsv --states 512
c++ -std=c++17 -O3 fast596.cpp -lgmpxx -lgmp -o fast596
./fast596 rules.tsv 1500000000
~~~

The C++ run starts at $P(306,\mathtt{010111})$, reached after nine completed returns. The direct verifier checks this configuration. For a group of $m$ verified affine returns, writing $n=3^m H+B$, $0\le B<3^m$, leaves the row choices determined by $B$ and the starting tail. The arithmetic result is $4^mH$ plus the result obtained on the low part $B$. The lower bound $n\ge300$ applies to the actual orbit throughout. It is preserved by every accepted row because the table builder checks $c\ge0$. The low part is an arithmetic representative and requires no separate reachability assumption. Recursive splitting and five-return lookups implement this identity. A missing table entry stops the verifier.

| Completed returns | Bits in $n$ | $n\bmod 1000000007$ | Tail |
|---:|---:|---:|---|
| 600 | 254 | 581001720 | 011 |
| 100,000,000 | 41,503,755 | 940392511 | empty |
| 335,544,320 | 139,263,481 | 118672314 | 011 |
| 671,088,640 | 278,526,956 | 673537329 | empty |
| 1,342,177,280 | 557,053,907 | 958126556 | 011 |
| 1,500,000,000 | 622,556,254 | 949589526 | empty |

The checkpoint after 1,500,000,000 returns has an empty suffix and a 622,556,254-bit counter. Applying the 35-return lower bound at that checkpoint proves **at least 1,500,000,035 completed returns from blank**.

The final directly replayed return alone takes more than $10^{373000000}$ elementary transitions. Let $B=622556254$ be the bit length of the final counter. If the preceding counter was $3t+r$, the final one is $4t+c$, with $c\le100000$ in the accepted table. Thus $t>2^{B-4}$. That return starts with $t+1$ regular sweeps. Their time alone includes $5t(t+1)>2^{2(B-4)}$, and $2^{10}>10^3$.

All 1,536 affine rows of the 512-state input table agree with Fractal Geometry Explorer's independently written Python zone evaluator after translating $n$ by one. Replaying a hundred million returns with individual rows also gives the same checkpoint. The extended replay and first failed comparison have executable certificates. They have no new Lean or Rocq kernel certificate.
