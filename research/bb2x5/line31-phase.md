# Machine 31 and the fourth entry at an even cell

Machine 31 is `1RB3RB---4RA2RA_2LA2RA3LB4LB1LB`. Its blank-tape verdict is open. The run below completes **274,694,713,035,481,808,843,150,871,901,787,592 defined instructions**. The first remaining possible A2 is at **+182**. The [resumable checkpoint](frontiers/runs/line31-phase.json) gives the clock, head, state and positive tape. The group count determines the negative tape.

Start with the infinite word
`AAAAA(BAAAA)…`, where the parenthesized block repeats forever. Apply the same two-cell transformation $F$ repeatedly. **The machine halts exactly when the fourth letter is B in some iterate.** If the first such iterate is number $j$, counting the seed as zero, the head reaches the undefined instruction A2 at coordinate $2j$. Letters are counted from the start of each iterate.

## Deriving the transformation

The community credits Daniel Yuan with the [original longitudinal analysis](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved). The starting results here are the [certified negative driver](mixed-and-sweeps.md) and the [fresh-cell entry table and paired halt criterion](https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/edge31.md). A first A entering a virgin even cell sends BB to the virgin odd neighbor. The two symbols are then 4 and 3. A later B sent as the first letter to the next virgin even cell is followed immediately by A. The first B writes 2 and returns in A, and that second entry reaches literal A2. A first A instead opens the next pair safely.

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

The comparison word `(BAAAA)…` differs only at its first letter. Under $F$ its successive periods are **BAAAA → ABBA → AAAABBA → AAAABBA**. The last word is an exact fixed infinite stream. The true seed changes its initial B to A and follows a different orbit. Separately, starting the *physical* source one place later, at `(ABAAA)…`, gives physical periods ABAAA → A → ABBAAAA → ABBAAAA. Both controls follow by applying the three-row table to one or three periods. There is also a one-edit control that really halts. In the fixed aligned stream `(AAAABBA)…`, change its fifth letter from B to A and remove the three preliminary As to obtain the physical input. Its first 27 requests return. Request 28 gives the physical prefix ABABAA at +6 and reaches A2 at +8.

## Testing four cells upstream

The earlier two-cell criterion requires the physical even parent to begin ABABAA or ABABABB. A parent four cells upstream must start with one of **3,256** minimal prefixes. Their lengths range from **11 to 40**. The unique shortest is **AABAAABAAAB**.

To generate these words, consume the first parent A and use ordinary phases (1, 2). Branch on incoming A and B. Retain a branch while its two-cell output is a proper prefix of either target, accept on a full match and discard on a mismatch. Each pair emits a letter within nine inputs, so the search is finite. The checker replays every accepted word and its one-letter-shorter predecessor against the literal physical rules. Every full word reaches A2 at +4 and every predecessor completes.

A comparison at +36 preserves the **entire cyclic word**. Its physical period has length 7,751,148. Reading it from offset 5,182,449 (zero-based) gives exactly the same first 25 letters as the true start. Drive a virgin suffix at +36 with that rotation. Its first 247 requests return and request 248 reaches literal A2 at +52. The first 248 requests at the true phase all return. Every cyclic factor count, of every length, agrees between these two drivers.

After any finite sequence of root requests that all returned, a freely chosen continuation can give either outcome. From any ordinary phase $p$, input B repeated $p$ times followed by A emits exactly B. To emit exactly A, use B from phase 0 or A from phase 1 or 2. Compose these choices through the finite opened strip. One can send a first B to the next virgin even cell, or send it the entire safe periodic source `(ABBAAAA)…`. The latter inverse construction gives an ultimately periodic input because each inverse uses only a finite phase. The halting continuation can even be embedded in a purely periodic driver having exactly four As per B. After the finite forcing word, pad the initial block to counts $(4k,k)$ and repeat it. This preserves the entire supplied prefix and its forced halt.

## Period growth and a finite-field form

Let $L$ be the length of a chosen period and $d$ its number of As minus its number of Bs. If $d$ is nonzero modulo three, three copies bring the phase back. At each position those copies visit all three phases. Each A contributes two As and a B, and each B contributes one A. Consequently the next chosen period has length $2L+d$ and displacement $L$. If $d$ is zero modulo three, a single copy brings the phase back.

**Four consecutive triplings are impossible.** If they existed, their input displacements modulo three would be $d,L,2L+d,5L+2d$. If $d$ and $L$ are both nonzero, they are either equal or opposite modulo three, making the third or fourth expression zero. At the root $d=3$, so among the first $x$ cells at least $\lceil x/4\rceil$ stages take just one copy. In the purely periodic alignment below, one complete period at cut $x$ takes at most $3^{\lfloor3x/4\rfloor}$ root groups. Every period is nonempty. At any even $x\ge6$, four such periods suffice to determine the fourth letter, or an earlier cut has already halted. This bounds the time to decide a *specified* site and leaves the possible site unbounded.

The root-group periods in this construction nevertheless grow without bound. On the repeating pair, $F(A)$ is empty and $F(B)=A$. No input letter can branch, so applying $F$ twice shortens every nonempty finite word by at least one letter. If the root-group periods stopped growing, each later pair would transform the same single finite period without taking additional copies. Repeated shortening would make it empty. An infinite periodic input has a nonempty period image because three consecutive silent inputs are impossible. This rules out a fixed bound on the number of root groups needed to restore all upstream phases.

At +56 the aligned periodic word has **shortest period 53,427,204,485**, containing **15,648,460,017 Bs**. After $3^{32}$ root groups, all phases below +56 have returned to their starts, and +56 has changed phase. After $3^{33}$ groups its child has received 128,984,693,421 aligned letters. Across the three copies every input A contributes three output letters and every B contributes one. This gives the B count, which is coprime to the period length and therefore rules out every proper power. Removing the three preliminary letters only rotates the infinite periodic word. This describes the driver at +56 for as long as its right-side calls return.

One can retain absolute input time algebraically. Encode silence, A and B by 0, 1 and 2 in the field of three elements. If $f(t)$ is the incoming signal and $p(t)=p(0)+\sum_{s<t} f(s)$, the outgoing signal at that same time is $-f(t)-f(t)^2p(t)^2$ modulo three. This follows directly from the nine letter/phase combinations, including silence. Two such updates implement $F$ without shifting time indices.

## The exact delay to the next output

For a finite strip of ordinary cells in current phases $p_0,\ldots,p_{h-1}$, the longest freely chosen input that can leave the far end silent has length

$$R(p)=\sum_{i=0}^{h-1} b_i p_i,\qquad (a_0,b_0)=(1,1),\qquad (a_{i+1},b_{i+1})=(3b_i,a_i+b_i).$$

The first weights $b_i$ are 1, 2, 5, 11, 26, 59. Thus the current tape phases give an exact worst-case waiting time for the next letter at any specified cut.

Assign incoming A and B weights $a_i$ and $b_i$ at cell $i$, and silence weight zero. For each transition, the incoming weight plus $b_i$ times the phase change is at most the outgoing weight at the next cut. Here the phase change is an ordinary integer difference of digits 0, 1, 2. The ratio $a_i/b_i$ starts at one and updates by $r\mapsto 3/(1+r)$, preserving $[1,3/2]$. The inequality then follows from the cell table. Equality holds at phase zero on either input and at each nonzero phase on B. Summing along the strip shows that every silent root input reduces $R$ by at least one. When $R>0$, choose the root letter that delivers B to the first nonzero digit. All preceding zero digits exchange A and B, so exactly one choice does this. Every active cell then gives equality, the last B is silent, and $R$ falls by exactly one.

More generally, for prescribed output $v$ the longest input giving exactly $v$, including a possible trailing silent interval, has length $R(p)+a_h\#_A(v)+b_h\#_B(v)$. The same sum proves the upper bound. First drain $R$ to zero. At the all-zero vector either desired letter can be emitted in one input, with equality at every cell. Drain the resulting vector and repeat. This proves attainability even when the two prescribed output letters carry different weights. The checker compares the silent formula with exhaustive longest-path search for every phase vector of widths one through five and the prescribed-output formula for all output words through length three on strips up to three cells wide.

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

The [aligned ledger](frontiers/runs/line31-phase-rows.txt) records the count, ending phase and first 16 letters (or all letters if fewer) at each cut after 40 complete periods at +56. This corresponds to 74,120,807,554,073,640 root groups. The positive tape and raw clock were reconstructed from these rows. After a further 1,000,000,000 groups, a second computation with the repository's physical longitudinal worker agrees on the entire checkpoint, including the exact increase of 7,412,080,805,407,364,062,912,987,332 instructions.

Cell +178 is first reached on root request **347,485,599,506,515,730**, after **241,492,483,728,805,292,863,332,089,319,455,362** defined instructions. The instruction about to execute is A0. At +56 this was aligned letter 2,003,775,823,336, the 26,969,257,391st letter of the 38th period. Counts of emitted letters locate the corresponding root request. The [preceding group boundary](frontiers/runs/line31-first178.json) has 69,497,119,901,303,145 completed groups and a positive tape ending at +177. Replaying its next five requests in physical order recovers the first arrival and the new tape.

At the final boundary the head is at zero in state A. The run has visited cells through +181. The even-cell entry prefixes are `ABAAAB` at +176, `AAB` at +178, and `A` at +180. For +182 to halt, the input at +180 must next begin `BABAA` or `BABABB`. Its next six entries suffice to decide this site. The earlier [18-trillion-group run](https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/edge31_checkpoint.json) left +142 as the first candidate. The [intermediate $10^{16}$-group checkpoint](https://github.com/valu42/busycoqtesting/blob/433d2f7387f82ecb29862def34ff9f8b4a1d3f9a/research/bb2x5/frontiers/runs/line31-phase.json) left +172.

## Reproduction

From `research/bb2x5`, use Python 3 with assertions enabled and a C++20 compiler. Omit `-fopenmp` for a single-threaded build. The split affects work and memory, and has no effect on the represented computation. Split 52 uses a period of about 4.72 billion bits. Smaller splits trade memory for additional streaming time.

```sh
c++ -O3 -std=c++20 -fopenmp line31_phase.cpp -o /tmp/line31-phase
export OMP_NUM_THREADS=4
python3 line31_phase.py --next-first-visit frontiers/runs/line31-first178.json
python3 line31_phase.py --check --engine /tmp/line31-phase
python3 line31_phase.py --check-period56 --engine /tmp/line31-phase --split 52
python3 line31_phase.py --engine /tmp/line31-phase --groups 10000000000000 --split 43 --compare frontiers/runs/stream-31.json
c++ -O3 -std=c++17 frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-physical
python3 line31_phase.py --verify-continuation frontiers/runs/line31-phase-rows.txt --physical-engine /tmp/bb25-physical --compare frontiers/runs/line31-phase.json
```

For repeated long runs, the worker can export the full period at +56. The archive occupies 6,678,400,568 bytes. It stores A as 0 and B as 1, earliest letter in the low bit of each little-endian 64-bit word, with zero padding in the last word. Its SHA-256 is `f7229ff07bdf8c80e94c3a1ad3f778f2971212785b00f5b33c3325e5b65b62ae`. Two independent exports agreed byte for byte. The Python runner verifies this digest before using the file, counts whole root cycles below the cut, and computes any partial cycle separately.

```sh
/tmp/line31-phase 1853020188851841 52 56 /tmp/line31-cut56.bin > /tmp/line31-cut56.rows
python3 line31_phase.py --engine /tmp/line31-phase --groups 69497119901303145 --split 52 --packed56 /tmp/line31-cut56.bin --compare frontiers/runs/line31-first178.json
python3 line31_phase.py --engine /tmp/line31-phase --groups 74120808554073640 --split 52 --packed56 /tmp/line31-cut56.bin --compare frontiers/runs/line31-phase.json
```

The tests exhaust all 4,095 supplied A-initial words through length 12, including 199 physical halts, and check all 3,256 four-cell triggers. Four small blank runs compare the head, state, clock and both tape halves with a literal TM, and compare aligned histories under three split choices. The older $10^{13}$-group run agrees on the complete checkpoint. Each new endpoint also predicts the next group from the final aligned phases and checks it by literal positive-tape execution with the certified negative clock. These checks establish finite computations. A complete blank-tape proof in Rocq remains open.
