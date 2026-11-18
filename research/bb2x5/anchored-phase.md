# Anchored halting tests on lines 21 and 22

The blank-tape decision is open for both machines. There are exactly 36 minimal input prefixes on line 22 and 84 on line 21 that force B2 two cells to the right of a fresh cell. The longest have 18 and 21 letters respectively. The calculation below also determines how far the checked tapes protect the right edge when subsequent root inputs are allowed to vary. It can exclude a halt at cells the machine has yet to visit.

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
| [21](frontiers/runs/anchored-phase-21.txt) | 140,737,488,486,409 | 1,029,966,114,604,059,164,430,770,074,110 | 280 | 281 |
| [22](frontiers/runs/anchored-phase-22.txt) | 562,949,955,518,597 | 16,479,457,925,756,396,852,344,128,697,144 | 265 | 266 |

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

## Exact replay from blank

At 492,581,211,340,933 root groups on line 22 the last visited coordinate was 258. The exact continuation calculation first admitted B2 at 266, permanently clearing the seven unvisited cells 259 through 265. The 64-cycle checkpoint later visited all seven safely. Its last three digits, at 263 through 265, were 333. At that boundary the next four entries at 265 are decisive for a halt at 266. Four As emit BB. Any other four-letter prefix rules out a halt there. Four Bs supplied at cut 263 give one such halting control and reach B2 in 36 local instructions. Two As supplied there send A first to 266 and complete in 16 local instructions. Pulling the four-A condition back through the two mature cells gives 654 minimal fatal prefixes and 747 minimal clearing prefixes at cut 263. At most 29 future entries there settle coordinate 266. This is sharp. The common 28-letter prefix `ABAAAABAABAAAABAABAAAABAABAA` followed by A forces a halt there, while B clears it. The checker follows both controls with the literal transition table. These controls specify future inputs at 263. The blank source selects its own continuation.

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
