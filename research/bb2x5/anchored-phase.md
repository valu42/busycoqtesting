# Anchored halting tests on lines 21 and 22

The blank-tape decision is open for both machines. The checkpoints below permanently exclude halts at specific rightward coordinates. For either machine a two-term recurrence gives the exact latest root entry that can halt at any specified coordinate under arbitrary input. On line 22 exactly 36 minimal input prefixes at a fresh cell force a halt two cells farther right. On line 21 there are 84. The longest prefixes have 18 and 21 letters respectively.

| Line | November 3 encoding |
|---:|---|
| 21 | `1RB2RA3LA4LA2RB_2LA3RB---0RA1LA` |
| 22 | `1RB2RA3LA4LA2RB_2LA3RA---0RA1LA` |

A coordinate is measured from the initial head at zero and increases to the right. A letter is the state of a rightward entry. Every leftward move enters A on both machines. At cell zero the actual infinite source is the initial A followed by repetitions of `BAABABABAAABA`. Equivalently it is the periodic stream with period `ABAABABABAAAB` starting at rank zero. The negative-half induction, one-cell table and equivalence between a fresh BB and blank halting are inherited. [Driver and cell derivation](mixed-and-sweeps.md#2-two-machines-with-the-same-exact-blank-half-input) · [Earlier one-parent criteria](https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/target21_22.md)

The exact origin matters even with that same periodic word. On both machines the first cell sends the rotation by one position to its right. Starting a fresh positive tape directly at offset five instead causes line 22 to reach B2 at coordinate 8 on its 34th root entry, after 251 defined positive-half instructions. Offset eight causes line 21 to reach B2 at coordinate 6 on its 17th root entry, after 118 instructions. The verifier checks both rotated controls with the physical transition table. A proposed invariant for all phases of the blank period would therefore include actual halts for those phases.

## Blank-tape checkpoints

The rightmost visited cell and the first possible B2 are measured from the initial head. At the two endpoints below both a halting continuation and a nonhalting continuation are possible if future root letters are free. Each machine's blank driver fixes those letters.

| Line | Complete root groups | Defined instructions from blank | Last visited | First possible B2 |
|---:|---:|---:|---:|---:|
| [21](frontiers/runs/anchored-phase-21-followup.txt) | 216,603,790,802,953 | 2,439,694,513,890,935,834,607,685,524,288 | 285 | 286 |
| [22](frontiers/runs/anchored-phase-22-followup.txt) | 2,251,799,815,782,533 | 263,671,325,338,629,373,356,678,820,819,282 | 274 | 275 |

## The line 22 grandparent test

Write $M$ for the stream transducer started on mature digit 3 and $F$ for the same cell started on a fresh zero. A fresh A emits BA and leaves 3. A fresh BA is silent and leaves 3. Hence $F(Aw)=BA\,M(w)$, $F(BAw)=M(w)$ and $F^2(Aw)=M^2(w)$. A leading BB halts this cell. The earlier parent criterion says that a fresh cell starting with BAAAAA halts its child.

From digit 3 the following words return to 3. Juxtaposition means concatenation.

| Input block | Output on line 22 |
|---|---|
| $B$ | $ABA$ |
| $AB^{2r}A$ | $A^rB$ |
| $AB^{2r+1}A$ | $A^{r+1}$ |

The first A changes 3 to 4. Subsequent Bs alternate between 4 and 1, emitting A on every second B. The closing A emits B from 4 and A from 1. On digit 1, either next letter emits A.

Let $\mathcal P_k$ contain the minimal prefixes guaranteeing that $M$'s output starts with $k$ As on an infinite input. Then

$$
\mathcal P_1=\{B,AB\},\qquad
\mathcal P_k=\{AB^{2k-1}\}\;\cup\!
\bigcup_{j=1}^{k-1}AB^{2j-1}A\,\mathcal P_{k-j}\quad(k\ge2).
$$

For $k\ge2$, an initial B emits ABA and fails the test. After A followed by $2k-1$ Bs, the first $k-1$ output As have appeared and either next input supplies the last A. An earlier even B run ends in an output B too soon. An earlier odd run of length $2j-1$ emits $j$ As, returns to 3 and leaves the shorter test in the formula.

A fresh cell therefore halts its grandchild exactly when its own input begins with a word in the union below.

$$
A\,\mathcal P_4\quad\text{or}\quad BAAA\,\mathcal P_5 .
$$

In the first case the initial A already supplied BA to the child. In the second case the silent BA must be followed by AA, the unique way for $M$ to start with B. Five further As must follow in its output. There are 12 prefixes in the first family and 24 in the second. Each cylinder is minimal. The verifier compares them to the one-cell table on a finite branching tree of 243 nodes. Once both tests are decided on a prefix it discharges all continuations together. It also drives the literal machine on both one-letter extensions of each of the 36 prefixes and checks the undefined instruction at coordinate 2. This establishes an anchored test at any grandparent. Its occurrence in the body of a stream has no such implication.

## The line 21 grandparent test

On line 21 the same three mature input blocks in the table emit ABA, a run of $r+1$ Bs, and a run of $r$ Bs followed by A, respectively. The checker starts at a fresh cell and branches on its next input while the emitted prefix can still begin one of the four target words. It records the first input prefix forcing a match and prunes an incompatible output. From any mature digit every child continuation is attainable, as proved below. The four parent targets BAAAAA, BAAAABB, BAABBA and BAABBBB have 6, 12, 18 and 48 minimal grandparent prefixes respectively. A second comparison discharges 333 nodes in the input-prefix tree. Both one-letter extensions of each of the 84 witnesses reach physical B2 at coordinate 2.

## What the current tape forces at the frontier

Fix a checkpoint after a complete root group. Keep the physical tape and allow arbitrary subsequent root letters. A prefix $u$ represents all infinite streams beginning with $u$. When the cell has digit $s$, process $u$ using the one-cell table. Let $v$ be the emitted word and $t$ the resulting digit, provided the prescribed input has succeeded locally. The set of **all** attainable child streams under locally successful continuations is again given by a single prefix. On line 22 it is $vA$ when $t=1$. In every other case on either machine it is $v$.

For the surjectivity step, define $h(A)=ABA$ and $h(B)=AA$. From digit 3, $h(w)$ sends $w$ to the child, returning to 3 after each code word. Digit 4 can send B by A or A by BA and finish on 3. Digits 0 and 2 can reach 3 silently by BA and A, respectively. On digit 1, an A sends A and leaves 3. A B sends B on line 21 and A on line 22, leaving 4. This proves both the forced letter and the attainability of every allowed infinite tail.

Start at coordinate zero with the empty forced prefix. Apply this rule along the saved tape and then through fresh zeros. A pending 2 halts on B and a virgin 0 halts on BB. The first coordinate where the forced prefix is compatible with its local trigger is the earliest possible future halt under arbitrary root input. Mature digits are locally safe. At a checkpoint a pending 2, if present, is the last visited digit, since its initial B emitted nothing.

When the trigger is forced, every continuation halts at this site or earlier. If the fresh-cell calculation repeats a safe forced prefix with all preceding sites clear, all continuations are safe. At an ambiguous trigger the two verdicts are genuinely possible under different input streams. On a fresh tape the two streams $U=(AB)^\omega$ and $V=B(AABA)^\omega$ satisfy $F(U)=V$ and $F(V)=U$ on both machines. Neither begins with BB. The elementary block checks for the cycle are in the verifier. At a virgin site with an empty forced prefix or just B, BB supplies a halting continuation and $V$ supplies a safe one. At a pending 2 with free input, choose B to halt or $A h(U)$ to send the safe stream. Pull these choices back along the processed cells using the constructions above. This preserves any already prescribed letters. The continuations can be taken ultimately periodic.

One can also prescribe a halt at **any greater coordinate** once an ambiguous fresh frontier is reached. The prefix BA on a virgin cell is silent, after which $h(w)$ sends any requested stream $w$ right. Repeat this construction to move the first BB to the desired cell. Its first B returns immediately and its second is undefined, so no call passes the target. Every earlier call in the resulting finite strip finishes by induction from its right edge using the local table. A hypothetical finite halt under the safe continuation would likewise appear at a definite cell of the two-cycle, contradicting its initial letters.

On line 21 every mature digit can already supply any future child stream. On line 22 the forced As can give protection beyond the visited tape. In particular a true checkpoint after 70,368,746,274,949 groups had visited only through 248, yet the earliest possible B2 with the future root phase relaxed was 254. This permanently clears unvisited cells 249 through 253 on the actual run. The true blank driver has one specific continuation throughout.

Every earlier prefix of the actual driver leading to one of these ambiguous checkpoints also admits both kinds of continuation. Follow the known blank execution to that checkpoint, then use the two constructions. Establishing a verdict for the actual machine requires controlling its specified periodic source beyond that checkpoint.

## Exact latest root entry for a halt at any specified cell

Consider a fresh positive half and allow arbitrary letters at the root. Count an entry when it begins, including the one that reaches the undefined instruction. Define
$$
(a_0,b_0)=(1,1),\qquad (a_{j+1},b_{j+1})=(2a_j+b_j,2a_j),\qquad
D_x=b_x+\sum_{j=0}^{x-1}2(a_j+b_j).
$$
On line 21 the latest possible root entry that can halt at coordinate $x$ is exactly $D_x+1$. On line 22 it is $D_x+1-b_{x-1}$ for $x\ge 1$, and it is 2 for $x=0$. For example the latest physical halts at coordinates 1, 2 and 3 occur on root entries 7, 21 and 59 on line 21, and 6, 19 and 53 on line 22. A shorter way to compute the exact deadlines is $H_0=2$, $H_1=7$ on line 21 or $6$ on line 22, and $H_{x+2}=2H_{x+1}+2H_x+3$ on both. The extremal sources are explicit. The actual periodic source is one particular choice.

Give input letters A and B weights $a,b$ with $a\ge b>0$. Give output letters weights $2a+b,2a$. The five tape digits have potentials
$$
\phi(0)=2a+2b,\quad \phi(1)=0,\quad \phi(2)=2a+b,\quad \phi(3)=a+b,\quad \phi(4)=b.
$$
Every successful one-cell instruction batch satisfies
$$
  \operatorname{weight}(\mathrm{input})\le
  \operatorname{weight}(\mathrm{output})+\phi(\mathrm{start})-\phi(\mathrm{end}).
$$
This follows directly from the one-cell table. The silent transitions $0\xrightarrow{B}2$, $2\xrightarrow{A}3$, $3\xrightarrow{A}4$ and $4\xrightarrow{B}1$ spend exactly the lost potential. The returns $1\xrightarrow{A}3$ and $4\xrightarrow{A}3$ emit A and B and also attain equality. From 3, B emits ABA. From 1, B emits A or B and leaves 4, which satisfies the inequality for either output.

Sum the inequality along each word, then across the $x$ cells to the left of the target, using weights $(a_j,b_j)$ at cell $j$. Immediately before the root entry that eventually halts at $x$, all earlier root entries have finished. The input so far at $x$ is empty or a single B. The $x$ initially fresh cells supplied total initial potential $\sum_{j<x}2(a_j+b_j)$. Their final potentials are nonnegative. This bounds the number of completed entries by $D_x$. On line 22 the parent of a future B2 cannot end on digit 1 at this point. Either letter on 1 sends A to the target, permanently clearing it. Every other possible parent digit has potential at least $b_{x-1}$. Subtracting that term gives the sharper bound.

For attainment, take $g(w)=BA\,h(w)\,AB$ with $h(A)=ABA$ and $h(B)=AA$. From a fresh cell, $BA$ silently reaches 3, $h(w)$ sends exactly $w$ and restores 3, and $AB$ silently ends on 1. Every transition used here attains equality. On line 21 supply $g^x(B)$ and one more B. All $x$ parents are on 1, that last B passes through each of them as B, and the target halts. On line 22 with $x\ge1$ supply $g^{x-1}(BAAAA)$ and one more A. The last parent sends one B and waits on 4. Each earlier 1 passes the final A, which makes that 4 send the fatal B. These finite controls issue no call beyond the target. The checker drives the physical instructions for all eight coordinates from 0 through 7 on both machines. It also searches every possible root letter on the finite strips ending at coordinates 0 through 4 and recovers the same maxima.

The first root letter of the blank run is A. Fixing just that letter permanently clears coordinates 0 and 1, and reduces the **exact** latest root entry at every $x\ge2$ from $H_x$ to $H_x-6$. That first A leaves 3 on each of the first two cells and every later cell fresh. Their combined starting potential drops by $(a_0+b_0)+(a_1+b_1)=7$, and one root entry has been spent. To attain the new bound, remove the silent initial BA from the extremal controls on those two cells, which already start on 3. The checker also realizes these constrained maxima through coordinate 7.

The same inequality gives a finite deadline at a deep blank checkpoint. Use the actual potentials of its intervening tape and the largest weight of a still-undecided prefix at the parent. The true periodic word at the chosen cut then supplies a known number of letters per cycle. At the line 22 cycle-64 checkpoint this puts the test for cell 266 before $1.204\times10^{87}$ root groups. A failure to complete a root entry before that bound also requires reaching the target, since the whole finite strip up to it returns while it is unsettled. The report checker computes the integer bound. The source-specific replay below is much faster at deciding individual cells.

## Exact replay from blank

At the 256-cycle checkpoint on line 21 the entire lifetime input to cell 280 was `BAA`. Its digit was 4 and cell 281 was fresh. The outstanding fatal continuations at 280 were precisely `AAA`, `AABB`, `BBA` and `BBBB`. At cycle 274 the actual history at 280 was `BAAAABAA`. The next four letters had been `AABA`, and cell 281 had received `BA`. This permanently clears 281. The checkpoint was at 150,633,093,136,393 groups and 1,179,897,094,887,568,638,532,449,895,848 defined instructions. The free-continuation calculation first admitted B2 at 282. At cycle 346 the input at 281 had become `BABABABA`, and the actual input at 282 began `ABAAABA`. The run had reached 285, whose input was `BAA`. The same four continuations now test 286. At cycle 394, 216,603,790,802,953 groups from blank, the entire input at 285 was still `BAA`.

At 492,581,211,340,933 root groups on line 22 the last visited coordinate was 258. The exact continuation calculation first admitted B2 at 266, permanently clearing the seven unvisited cells 259 through 265. The 64-cycle checkpoint later visited all seven safely. Its last three digits, at 263 through 265, were 333. At that boundary the next four entries at 265 are decisive for a halt at 266. Four As emit BB. Any other four-letter prefix rules out a halt there. Four Bs supplied at cut 263 give one such halting control and reach B2 in 36 local instructions. Two As supplied there send A first to 266 and complete in 16 local instructions. Pulling the four-A condition back through the two mature cells gives 654 minimal fatal prefixes and 747 minimal clearing prefixes at cut 263. At most 29 future entries there settle coordinate 266. This is sharp. The common 28-letter prefix `ABAAAABAABAAAABAABAAAABAABAA` followed by A forces a halt there, while B clears it. The checker follows both controls with the literal transition table. These controls specify future inputs at 263. The blank source selects its own continuation.

The independent scan from blank at cut 74 reached coordinate 274 after 256 cycles (2,251,799,815,782,533 groups). It recorded the first 12 letters at 263 as `BAABAABABABA`. The first five, `BAABA`, had already arrived at cycle 64. The next four were therefore `ABAB`. With the saved three digits 333, the literal continuation from 263 gives `BABA` at 265 and `ABAA` at 266. It uses 54 defined instructions on this suffix and visits through 269. The first A at 266 permanently rules out a halt there. The independently resumed clock first put the earliest possible B2 beyond 266 at cycle 195. At that checkpoint it had visited through 269, at 1,715,238,141,427,845 groups and 152,986,177,854,060,398,338,777,733,201,624 defined instructions. Reaching 274 also permanently clears every smaller coordinate.

The following five-cell transition occurs on the actual line 22 run. At cycle 195, cells 265–269 were `33334` and the cells to their right were fresh. At cycle 206, the next five entries at 265 had been `BAABA`. They changed those five cells to `43333` and sent `BABABA` into the fresh neighbors. Those neighbors became another `33334` and sent nothing farther. The rightmost cell advanced from 269 to 274 in 99 instructions on this suffix. On both machines a further `BAABA` supplied to the older `43333` would restore `33334` without output. The three block transitions and the 99 physical instructions are checked on both tables. Repeating the advance farther right depends on the actual entries into the new block. At the 256-cycle checkpoint the lifetime input to 274 was `BAA`. The earliest possible B2 is 275, and it requires the next three entries at 274 to be `AAA`.

The worker carries the distinguished first entries at each coordinate. It constructs its cell tables by following the encoded physical instructions, with each successful child call returning in A. At the root it starts with the exact 13-letter period. At a chosen cut it has a finite prefix and a repeating word. These represent the output after a known number of root groups and the additional output per cycle. For each preceding cell the worker processes its prefix and then whole periods until the incoming symbol state repeats. Including the transient periods in the next prefix and all periods in that state cycle in the next repeating word is exact. At the selected cut the worker consumes a finite number of these cycles in chronological chunks over the remaining positive tape. Its four-cell lookup composes the same four single-cell tables and counts the visits inside the block.

For $q\ge1$ complete root groups let $E$ be the sum of the rightward entry counts over all nonnegative cells, including the initial A. The total raw time is $52q^2-21q+8+2E-13q$. The first term is the negative-half clock. The remaining terms count positive entries, their left exits and the rightward moves between positive cells. The checkpoint specifies $q$ and the positive tape. At this boundary the head is at zero in A and the negative tape is given by the inherited driver. [Clock derivation and earlier checkpoints](https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/streams.md)

From the repository root, build the two workers with a C++20 compiler and GMP. The Python checks use the standard library.

```sh
cd research/bb2x5/frontiers
c++ -O3 -std=c++20 anchored_phase.cpp -lgmpxx -lgmp -o /tmp/bb25-phase
c++ -O3 -std=c++20 longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-reference
python3 anchored_phase.py --workers /tmp/bb25-phase /tmp/bb25-reference
```

The saved transcripts include every visited nonnegative digit and up to 18 initial entries per cut. Recreate the two files and check the earliest possible B2 at each recorded checkpoint with these commands from the same directory.

```sh
/tmp/bb25-phase 21 66 256 8 > /tmp/bb25-phase-21.txt
/tmp/bb25-phase 22 74 64 4 > /tmp/bb25-phase-22.txt
for line in 21 22; do
    cmp "runs/anchored-phase-$line.txt" "/tmp/bb25-phase-$line.txt"
    python3 anchored_phase.py --report "$line" "/tmp/bb25-phase-$line.txt"
done
```

The linked follow-up records contain selected complete positive tapes, clocks and initial-entry witnesses. Recreate each latest endpoint directly from blank and compare it to that record. Substituting an earlier cycle recorded in the same file checks that endpoint instead.

```sh
/tmp/bb25-phase 21 66 394 > /tmp/bb25-last-21.txt
/tmp/bb25-phase 22 74 256 > /tmp/bb25-last-22.txt
for line in 21 22; do
    python3 anchored_phase.py --match "runs/anchored-phase-$line-followup.txt" "/tmp/bb25-last-$line.txt"
    python3 anchored_phase.py --report "$line" "/tmp/bb25-last-$line.txt"
done
```

The two workers agree on ten complete positive tapes, raw clocks and ordered initial histories across both machines. A literal interpreter also reproduces the complete two-way tape, head, state, ordered histories and raw clock at 100 groups on each machine.

### Independent comparison with the previous blank runs

The new worker starts on blank. The older worker starts at the published 200-billion-group checkpoint and runs just the remaining groups. The raw clock, complete positive tape and every available first-18 entry history agree at the following common endpoints. The negative tape is fixed by the group count.

| Line | Additional groups in the older worker | Total groups | Defined instructions | Compared histories |
|---:|---:|---:|---:|---:|
| 21 | 789,852,169 | 200,789,852,169 | 2,096,461,366,212,858,538,115,728 | 225 |
| 22 | 791,818,373 | 200,791,818,373 | 2,096,502,424,963,218,640,733,530 | 203 |

From the same directory, the commands below read the two earlier JSON files at the indicated revision. [Line 21 predecessor](https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/streams-21.json) · [Line 22 predecessor](https://github.com/valu42/busycoqtesting/blob/dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb/research/bb2x5/halting-outlook/streams-22.json)

```sh
git fetch origin research/bb2x5-next-proof-34
rev=dcacb2022e4ed1ac33f1a11f30391c70abcbb3bb
for line in 21 22; do
    git show "$rev:research/bb2x5/halting-outlook/streams-$line.json" > "/tmp/bb25-old-$line.json"
    /tmp/bb25-phase "$line" 51 187 > "/tmp/bb25-overlap-$line.txt"
    python3 anchored_phase.py --bridge "$line" "/tmp/bb25-old-$line.json" "/tmp/bb25-overlap-$line.txt" /tmp/bb25-reference
done
```

The controls and finite computations have not been formalized in Rocq.
