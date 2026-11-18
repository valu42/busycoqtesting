# Machine 7 and the first exceptional return

Machine `1RB---3RA2LA2RB_2LB3LA4LB4RA0RA` remains open from the blank tape. Its only undefined instruction is A1. We found a family of suffixes that force the machine to hit A1, an arithmetic test that rules out this route on many actual epochs, and a way to search consecutive epochs with one suffix simulation. A return in A or B means that the head has just crossed the left edge of the named suffix in that state. The suffix retains every write between calls.

At the verified 16,384-epoch checkpoint, the next target is the first A reply from the suffix at cell −89. If its count of prior B replies is congruent to 218 modulo 486, the machine reaches A1 on cell −94 exactly 26 instructions later. Whether the actual suffix reaches that residue remains open. [Six-cell proof and other residues](#a-halting-test-on-five-ternary-digits) · [Checkpoint and blank-orbit results](#results-on-the-blank-tape)

## Which guards occur from blank

A0 writes 1 and calls the cell to its right in B. A B return consumes the 1 through B1. An A return reaches A1. A halt during the suffix call already ends the computation.

At the moment a blank-orbit A0 installs its guard, its right neighbor is 0, 2 or 3. If A0 enters previously unvisited territory on the right, the next cell is virgin. The same holds at time zero. Otherwise an arrival from the right in A was a leftward A3 or B1 instruction, which just deposited 2 or 3 on the neighbor. This also covers revisiting a zero. The only instruction that writes zero is B4, and it leaves that zero moving right, so its first revisit comes from the right.

If the neighbor is 3, the B1 that just wrote it consumed a 1 previously installed there by A0. Its suffix two cells to the right of the new guard has therefore just returned B to that earlier A0. Its first cell is now 2 or 4, the only writes on leftward B exits. These restrictions still permit both halting paths below. Start A on the second cell of `0004` or `0022` with blank exterior. Three instructions later the first cell is a live A0 guard next to a 3. The machine reaches A1 on the first cell at raw time 65 or 31 respectively.

### A leading pair on every later epoch

**Permanent outer-header invariant.** Every completed blank epoch from epoch 2 onward leaves a word beginning with a 3, some number $k\ge0$ of twos, and a pair 42 or 44.

The underlying statement holds on arbitrary tapes. A suffix call that returns B after making at least one rightward excursion from its first cell leaves a prefix consisting of zero or more twos followed by 42 or 44. Consider its last instruction on the first cell. If it was B2, the last rightward move there must have been A4, the only rightward instruction writing 2. The child returned B, so the child cell now contains 2 or 4, while B2 leaves 4. If the last instruction was B0, the last rightward move must have been B4, the only rightward instruction writing 0. Its child was entered in A and returned B. An A entry cannot return B immediately, so this shorter child execution satisfies the same premise. B0 prepends one 2 to its output. Induction on the finite call length proves the statement.

The first blank epoch leaves 32. Every successful later epoch began by calling B on 3, which necessarily makes a rightward excursion. The fresh B1 then prepends the 3. Consequently, at every outer launch from epoch 3 onward, the tail V after the maximal run of twos begins with a pair, even after an exceptional epoch. This proof does not assume a bound on $k$ or on the time spent inside the child.

### B on the neighboring 3

Let U be the tape to the right of the 3. Each row lists replies **from U** and the ordered requests the machine sends **to U**. A completed row uses the evolved U when another round starts.

| Replies | Requests | Result at the 3 |
|---|---|---|
| BB | AA | Writes 2 and returns B to the guard |
| AB | AB | Writes 4 and returns B to the guard |
| BA | AA | Starts A0 here and sends B. An A return hits this new 1. A B return sends A onto the original guard |
| AAA | ABA | Writes 2 and returns A onto the original guard |
| AAB | ABA | Restarts in B on 3 |

B3 first writes 4 and sends A. A B reply leaves B4 to write 0 and send A again. An A reply leaves A4 to write 2 and send B. Reading the next reply on those physical digits gives the five rows. A halt in a pending call propagates at its actual cell. The simulator also combines A0 before 0 or 2 into three raw steps, including the B1 return from the installed guard. [Guard and epoch implementation](line7.py)

## A power of three that forces a halt

Consider a fresh guard scanning 0 with right tape `3 2^k V` for $k\ge1$. Write $D=3^k$. Start making successive A calls to V. Let $j$ count B replies before the first A reply, stopping once $2D$ replies have all been B. If V halts inside a call, the physical machine halts there.

* When $j=0$, the A reply comes back through every 2 by A3. B on the first 2 then returns B immediately, giving the safe AB row.
* When **$j=D$**, the first A call on the block of twos returns B and restores all its digits. The second A call receives V's A on its very first descent. It returns A through every 2. The BA row sends B onto the leading 2, which immediately returns B. The original guard now scans A1. Exactly $2D+2k+4$ instructions took place outside V.
* When all $2D$ replies are B, the two A calls on the leading block both return B. The outer guard succeeds with new right tape `3 2^(k+1) V′`. V′ is the exact suffix after its $2D$ calls. The rest of the machine executed $4D+1$ instructions.

For the remaining ranks, the implementation resumes the suspended instructions. An exception inside the leading twos can be absorbed and the outer guard can still return safely.

### A larger family of forced halts

For a rank in the second block write $j=D+n$ with $0\le n<D$. Pad $n$ to $k$ ternary digits. Suppose its first and last digits are 0, every digit is 0 or 2, and no two 2s are adjacent. **Each such rank forces A1 at the original guard, regardless of what V would do next.** There are $F_k$ such ranks, with $F_1=F_2=1$. In the first block the same offsets give a safe AB return. For example, with four leading twos the second-block ranks 81, 87 and 99 all force a halt.

At the instant V returns A, the suspended twos contain 3, 4 or 0 according to the ternary digits 0, 1 or 2 of $n$. The least significant digit is nearest V. Digit 0 executes A3, writes 2 and carries A one cell left. Digit 2 executes A0. Its right neighbor just processed digit 0 and now holds 2, so B2 returns immediately and B1 carries A left, leaving 3. Adjacent 2s would invalidate that guarantee. The initial and final zeros ensure that V is never reentered and the leading cell finishes as 2. The second-block BA row therefore reaches the original A1. Counting the interior strings with no adjacent 2s gives the Fibonacci recurrence.

The exact outside cost for this family is $2j+2k+4$. More generally, at the instant of the first A reply the cost already paid outside V is $2j-s_3(j)+k+2$, where $s_3$ is ternary digit sum. At layer $i$ counted outwards from V, the numbers of completed child and parent calls are $\lfloor j/3^{i-1}\rfloor$ and $\lfloor j/3^i\rfloor$. Each layer has also issued one suspended call. Summing these costs and the opening guard instructions gives the formula. Each digit 2 then costs two more instructions than digit 0 to carry A left, cancelling its contribution to the digit sum. A bounded literal replay of the suspended prefix also handles arbitrary ternary words. It records the first halt, safe exit or request that crosses back into V. [Rank replay and guard audit](line7_guards.py)

### Which low bits can the rank have?

Suppose V begins with $m$ pairs, each `42` or `44`. Read `42` as 1 and `44` as 0, least significant bit first, giving $a$. **Every normal first A reply from V occurs at a rank $j\equiv a\pmod {2^m}$**. This includes arbitrary tape beyond the pairs.

To see this for one pair, call its right-hand digit $e$ and the tape following it S. An A input to the first 4 sends B to $e$. B on 2 writes 4 and returns B immediately. B on 4 writes 0 and sends A to S. A B from S restores 2 and returns B through the pair. Thus, if S returns B to its first $n$ A inputs, those replies account for $2n+b$ ordinary inputs at the pair before the first exceptional one, where $b=1$ for initial `42`. If S next returns A, the suspended 0 calls S in B. An A on that follow-up hits A1 inside the pair. A B lets B1 return A and leave 3. The first pair cell then sends A onto this 3 and returns A. No other route gives a normal first A at the pair. Applying the argument to successive pairs gives the congruence. A mismatch with $3^k$ excludes the exact-rank halting route for the current epoch.

### Explicit halting tapes and one-cell controls

Encode an integer $n$ in $m$ pairs as above, ending in a single 3. Call the resulting word $S(n,m)$, with $0\le n<2^m$. Its first $n$ A calls return B, the next A call returns A, and a following B call returns B. The terminal 3 alone has this property at $n=0$ in two steps. Adding a pair of bit $b$ gives the property at $2n+b$ by the preceding argument. The terminal 3 keeps the entire calculation independent of the exterior.

The total time inside the word for all $n+2$ calls is $T(n,m)=2+7n-4\,\mathrm{popcount}(n)+8m$. Adding a pair costs $7n+3b+8$ instructions at the two new cells. The left cell contributes $2(2n+b)+4$ and the right cell contributes $3n+b+4$. The final B return costs one instruction.

It follows that the machine starting at the 0 of `0 3 2^k S(D,m)` reaches A1 at that very cell after **$9D+2k+5-4\,\mathrm{popcount}(D)+8m$** defined instructions. Choose $m$ one greater than the bit length of $D$. Changing the second digit of the highest pair from 4 to 2 increases the rank by $2^{m-1}$, so both blocks complete and the guard returns safely. The two inputs differ in exactly one cell at a distance that grows with $k$. A literal interpreter checks both outcomes for $1\le k\le8$, two choices of exterior, and the register cost for all $n<64$ at two widths. [Literal regression tests](test_line7_guards.py)

The same construction with $S(j,m)$ realizes every forced rank in the Fibonacci family in $9j+2k+5-4\,\mathrm{popcount}(j)+8m$ steps. The tests cover every member through $k=8$ and compare the suspended-prefix replay against independent physical traces for every rank in both blocks through $k=4$.

There is also a halting route that uses just one more reply. At any rank $j\equiv2\pmod3$ the deepest leading 2 is suspended on 0. V's first A therefore installs a new 1 and sends B straight back into V. If that B call returns A, this new guard halts, in either block. If V's first A left 2 on its first cell, B2 returns immediately and this particular guard is safe. A normal A exit can otherwise leave 3. A V starting with a 42 or 44 pair always leaves 2 on its first A return, as the pair proof shows. A new candidate for this one-more-reply route needs both the correct ternary phase and a 3 actually deposited by V.

In fact the leading pair becomes 22 on that first A return. The inner digit has returned A leaving 3, then A3 there and A3 on the outer digit each write 2. Prior B replies to A keep the first digit 4 and toggle the second between 2 and 4. Each all-B epoch uses an even number of A requests to V and therefore preserves the pair exactly. Immediately after the exceptional A, a B then an A on V must both return B, in one and three instructions, leaving 44.

The permanent outer-header invariant therefore excludes the one-more-reply halt at the deepest leading 2 on every applicable blank epoch from epoch 3 onward. The original guard can still halt. For its Fibonacci family the units digit may now also be 2. The known B2 on V supplies the return needed to carry A across that last digit. There are $F_{k+1}$ forced ranks in the second block for a blank-reachable header, allowing any units digit in the separated ternary strings with leading zero. With four leading twos the five ranks are 81, 83, 87, 99 and 101. The register construction realizes all of them on explicit tapes. Their reachability from blank remains open.

When $k=0$ and V begins with the guaranteed pair, the original guard takes the safe AB row if its first A call returns A. If the first A call returns B and the second returns A, V again begins with 22, the BA row requests B, and the original guard halts. Two initial B returns give the safe BB row. A halt inside V still propagates immediately.

### A halting test on five ternary digits

**For $k\ge5$, a first A return at rank $j\equiv218\pmod{243}$ forces A1 exactly 26 instructions later.** This holds in either block for every blank-reachable header with the leading pair. The low five ternary digits of $j$ are 22002. Since $3^k$ is divisible by 243, these are also the five low digits of the within-block offset. The last five suspended twos therefore contain 00330. The first cell of V now contains 2. The head is in A on the last 0. On these six cells alone, 003302 becomes 134244 after 26 defined instructions and A scans the leftmost 1. No exterior cell is read. The halt is always five cells to the left of V.

We also exhaustively checked windows of up to eight suspended twos and the first cell of V. The literal checker stops at a physical halt, a repeated complete local state or the first exit from the known window. Extending just the words without a shorter halting suffix gives 1, 2, 5 and 11 new certificates at widths 5, 6, 7 and 8 respectively. Together these 19 certificates cover **71 distinct ranks modulo $3^8=6561$**. A full physical interpreter replays each certificate on complete constructed tapes in both blocks, checking the halt coordinate, remaining tape window and exact time after the first A. [Exhaustive checker](line7_rank_words.py) · [All 19 traces](runs/line7-halt-rank-words.json)

## Searching consecutive epochs in one batch

In an uninterrupted stretch of all-B tail replies starting at `3 2^k V`, the total number of A requests to V over $t$ epochs is

$$ C_t=2D(1+3+\cdots+3^{t-1})=D(3^t-1). $$

A single run of these $C_t$ A requests computes the complete new tape. Its outside cost is $2C_t+t$, and the new header has $k+t$ twos. For a first exception after $J$ B replies, binary search finds the largest $s$ with $C_s\le J$. The accelerator replays and commits exactly those $s$ complete epochs, then executes the exceptional epoch through the ordinary guard code. A speculative tape never supplies a partially restored configuration.

Relative to the initial V, the very first exception of the stretch would force the exact-rank halt in epoch $r+1$ precisely at $J=D(2\cdot3^r-1)$, with $r=0$ denoting the first epoch. Finding the next normal A return under repeated A inputs is therefore a concrete decision question at a fixed tape cut. A halt inside one of those inputs is a separate possible outcome. [Rank and batch audit](line7_guards.py)

## Results on the blank tape

| Epochs audited | Internal A0 guards | Internal calls with a finite safe-return certificate | Outer B-on-3 replies |
|---|---:|---:|---|
| 1–1,024 | 427,138 | 427,138 | BB 1,018 times, AB 5 times, one initial B on 0 |
| 9,217–9,728 | 4,256,544 | 4,256,544 | BB 512 times |
| 9,729–10,000 | 2,351,269 | 2,351,269 | BB 272 times |

The two internal cases left open by the [earlier filters](https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/halting-outlook/line7.md) have certificates on short prefixes. At epoch 415, a B entry on `3434222424242244424424242` returns B in 129 instructions and leaves `2444222444242242424224444`. At epoch 827, `3434242` returns B in 21 and leaves `2444244`. Neither trace reads a cell to the right of the displayed word. Every internal call in the two late intervals was covered by a child 0 or 2, terminal 32 with blank exterior, or an ordinary prefix that extinguishes all emitted calls. [First 1,024 epochs](runs/line7-guards-0-1024.json) · [First late interval](runs/line7-guards-9216-9728.json) · [Second late interval](runs/line7-ranks-9728-10000.json)

In the first 1,024 epochs, 1,018 had the required header. Visible pairs excluded the target rank at 913 of them. They admitted it at 104, and one had no visible pair. In 1,001 cases both blocks of requests completed entirely in B. The other 17 had a normal first A return. The closest in relative distance was epoch 900 with $k=852$ and $j/3^k\approx1.0103363$. In all 272 epochs from 9,729 through 10,000 the residue was compatible, yet both blocks completed entirely in B. A passing residue test alone supplies no halting probability.

Every rank in the Fibonacci family is odd. A leading 44 pair fixed the exceptional rank to be even in 610 of the first 1,024 epochs, excluding the entire family there. Of the 17 actual first A replies, two returned safely using only the suspended prefix and 15 requested the tail again.

The four observed ranks congruent to 2 modulo 3 in this early sample occurred at epochs 13, 28, 415 and 827. All four deposited 2. The sole observed deposit of 3 was at epoch 2 and its rank was zero. Across all 1,018 applicable early epochs, epoch 2 was the only one whose V lacked a leading pair. All 272 applicable rank probes from epochs 9,729 through 10,000 had the pair.

The checkpoint at epoch 10,000 has 41,451 stored suffix cells and an exact clock of approximately $7.08015\times10^{4734}$. Its complete serialized state agrees with the simulator from before the guard changes, with the per-epoch rank audit, and with the geometric batch path started at epoch 9,216. The inherited tests also compare the blank tape against a literal interpreter through 18 epochs and an independent moving-window configuration at 100 billion raw instructions.

The geometric audit found the following first A replies in two longer intervals. Every other epoch in each interval completed both blocks entirely in B. Each exceptional epoch also completed safely after resuming the physical machine. [Epochs 8,193–9,216](runs/line7-blocks-8192-9216.json) · [Epochs 10,001–12,288](runs/line7-blocks-10000-12288.json)

| Epoch | Leading twos | $j/3^k$ | Next request to V after its first A |
|---:|---:|---:|---|
| 8,952 | 8,873 | 1.141180 | B after 1 instruction |
| 9,058 | 8,978 | 1.132257 | A after 9 instructions |
| 10,996 | 10,914 | 1.703924 | B after 1 instruction |
| 11,648 | 11,564 | 0.156231 | B after 1 instruction |

At epoch 8,952 a separate replay from the fixed physical cut at epoch 8,192 reproduced the first exceptional A on cell −77 at approximately $8.69775\times10^{4234}$ raw steps. The next six requests to V were all B and each returned B. The exact event clock and individual call costs are saved. [First-return checkpoint](runs/line7-first-A-8952.json) · [Fixed-cut replay](check_line7_first_return.py)

At epoch 10,996 the first A arrived on cell −80 at approximately $1.02614\times10^{5210}$ raw steps. The rank was 2 modulo 3. One instruction installed the new guard, and V had just deposited 2. Its B reply therefore took exactly one instruction. The next five A requests to V all returned B, in 3, 205, 3, 215 and 3 instructions. [Exact clock, head and six follow-up calls](runs/line7-first-A-10996.json)

At epoch 11,648 the same temporary guard occurred in the first block. The fixed-cut replay recovered V's first A on cell −82 at approximately $1.95504\times10^{5519}$ raw steps. V again deposited 2. The next six calls were all B and returned B in 1, 67, 1, 27, 1 and 19 instructions. [First-block event and six replies](runs/line7-first-A-11648.json)

The indexed blank run reached **16,384 completed epochs** at approximately **$3.85525\times10^{7775}$ raw steps**. The exact clock has 25,830 bits. A scans cell −16,384, followed by a 3, 16,293 twos and V beginning at cell −89. The stored suffix has 68,035 cells. [Full physical checkpoint](runs/line7-calls.json)

Every epoch from 12,289 through 16,384 completed both blocks with B replies. A batch-size-173 audit from epoch 12,288 and a separate batch-size-256 continuation from epoch 9,856 produced byte-identical checkpoints. The saved intervals contain 17 first A returns in the early sample and four in the two later intervals with exceptions. None satisfies a certified short ternary suffix. [Last 4,096 epochs](runs/line7-blocks-12288-16384.json)

V currently begins with 44, so its first exceptional A must have even rank. Every forced second-block Fibonacci rank above is odd, including the exact power of three. Each all-B epoch consumes an even number of A calls and preserves the initial 44. Thus the Fibonacci family is excluded through the first exceptional reply at this fixed cut, however many ordinary epochs precede it.

**A concrete route remains at the current checkpoint.** Let $J$ count all B replies to successive A requests at cell −89 before the first A. If $J\equiv218\pmod{486}$, machine 7 halts on cell **−94** exactly 26 instructions after that A. The counts spent in any whole intervening epochs are multiples of both 2 and $3^{16293}$, so they preserve the tested residues. The other certificates likewise give 71 compatible even residue classes modulo 13,122. The leading 44 gives $J=2n$ for a normal first A, so the six-cell route corresponds to $n\equiv109\pmod{243}$ for the suffix two cells farther right. Determining the first exceptional rank on that physical suffix, or detecting a prior halt inside a call, remains open.

## Replay

Run from `research/bb2x5`. Each epoch is one successful extension onto a fresh blank cell to the left. The indexed [checkpoint](runs/line7-calls.json) includes the exact hexadecimal clock, physical head and full located suffix. Each audit links its input and output states by SHA-256.

```sh
base=680c69635d58a26ad2d33814ac16df4f72a86975
git show "$base:research/bb2x5/halting-outlook/line7-8192-9216-checkpoint.json" > /tmp/line7-9216.json
python3 frontiers/line7_guards.py --epochs 1024 --ranks \
  --checkpoint /tmp/line7-1024.json --audit /tmp/guards-1024.json
python3 frontiers/line7_guards.py --resume /tmp/line7-9216.json --epochs 9728 \
  --checkpoint /tmp/line7-9728.json --audit /tmp/guards-9728.json
python3 frontiers/line7_guards.py --resume /tmp/line7-9728.json --epochs 10000 --ranks \
  --checkpoint /tmp/line7-10000.json --audit /tmp/ranks-10000.json
git show "$base:research/bb2x5/frontiers/line7.py" > /tmp/line7-original.py
PYTHONPATH=frontiers python3 /tmp/line7-original.py --resume /tmp/line7-9216.json \
  --epochs 10000 --checkpoint /tmp/line7-original.json
cmp /tmp/line7-original.json /tmp/line7-10000.json
git show "$base:research/bb2x5/frontiers/runs/line7-calls.json" > /tmp/line7-8192.json
python3 frontiers/line7_guards.py --resume /tmp/line7-8192.json --epochs 9216 --batch 73 \
  --checkpoint /tmp/line7-block-9216.json --audit /tmp/blocks-9216.json
python3 frontiers/line7_guards.py --resume /tmp/line7-10000.json --epochs 12288 --batch 113 \
  --checkpoint /tmp/line7-12288.json --audit /tmp/blocks-12288.json
python3 frontiers/line7_guards.py --resume /tmp/line7-12288.json --epochs 16384 --batch 173 \
  --checkpoint /tmp/line7-16384.json --audit /tmp/blocks-16384.json
cmp /tmp/line7-16384.json frontiers/runs/line7-calls.json
python3 frontiers/check_line7_first_return.py --resume /tmp/line7-8192.json \
  --audit /tmp/blocks-9216.json --output /tmp/first-A-8952.json
python3 frontiers/check_line7_first_return.py --resume /tmp/line7-10000.json \
  --audit /tmp/blocks-12288.json --output /tmp/first-A-10996.json
python3 frontiers/line7.py --resume /tmp/line7-10000.json --epochs 10996 --batch 113 \
  --checkpoint /tmp/line7-10996.json
python3 frontiers/line7_guards.py --resume /tmp/line7-10996.json --epochs 11648 --batch 113 \
  --checkpoint /tmp/line7-11648.json --audit /tmp/blocks-11648.json
python3 frontiers/check_line7_first_return.py --resume /tmp/line7-10996.json \
  --audit /tmp/blocks-11648.json --output /tmp/first-A-11648.json
python3 frontiers/test_line7_guards.py
python3 frontiers/line7_rank_words.py --width 8 --output /tmp/line7-rank-words.json
cmp /tmp/line7-rank-words.json frontiers/runs/line7-halt-rank-words.json
c++ -O3 -std=c++17 frontiers/window.cpp -o /tmp/bb25-window
BB25_WINDOW=/tmp/bb25-window python3 frontiers/test_line7.py
```
