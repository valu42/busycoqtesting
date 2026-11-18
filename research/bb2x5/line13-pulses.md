# Line 13 and the parity of the next right-edge visit

The machine is `1RB3RA3RB4LA1LA_1LB2LA1LA---1RB`. At each growth checkpoint its decision reduces to a first return on a finite binary word. The first return always exists. An odd waiting time opens the next pair of cells. An even waiting time reaches the literal undefined instruction B3. The outstanding question is whether an even wait occurs on the word sequence starting from the empty word.

## The blank edge at cell 155

The first A entered cell **155** after **564,283,145,741,602,382,792,183,308,072,151,015** defined instructions. Its lifetime input started BA. One instruction later the head entered 156 in A. The new pair opened on pulse **193,955,861,944,859,742**. This permanently clears the pending odd cell from the [previous edge study](line13-edge.md).

The existing letter-based native worker advanced the published blank checkpoint to group 150,000,000,000,000,000, then to the canonical group immediately before the opening. Replaying the next five positive requests instruction by instruction gives both arrival clocks above. The complete pre-opening tape and clock are in the [run record](frontiers/runs/line13-pulses.json). An independent packed pulse search from the original checkpoint selected the same pulse.

The search continued to group **1,152,921,504,606,846,977**. The blank machine had then completed exactly \(2^{60}\) pulses and **19,938,419,936,773,738,169,791,518,345,369,146,404** defined instructions. Cell 157 had received exactly one B. Its right neighbor was still blank. Since the opening at 156, 958,965,642,661,987,234 further pulses have passed without an opening. The opening at 156 had an even absolute pulse number. Consequently an even absolute pulse number for the first entry into 158 would prove a halt at 157. An odd one would clear 157.

A separate run from virgin cells to \(2^{59}\) pulses ended at 4,984,604,984,193,434,561,506,482,696,633,003,556 defined instructions. All 154 available lifetime entry prefixes from cells 4 through 157 agreed over the overlap with the search resumed from the published checkpoint. The complete terminal tape, per-cell counts and final-group replay at 155 are in the run record above.

## Blank startup and a single repeated input

Use A and B for entries from the left and write C for the two successive entries BA. Count each C as one *pulse*. The verified negative half supplies an initial A at cell 0 followed by repetitions of BABAB. At the canonical boundary of group \(q\) the machine has completed \(5q\) requests on the positive half and has returned to coordinate zero. The first group uses ABABA. Each subsequent group uses BBABA. [Negative driver and existing one-cell proof](line13-edge.md)

At the first boundary the tape at cells 0 through 5 is `114421`. The first four cells sent a single A to cell 4. On each later group they return to `1144` and send one C to cell 4, both letters during the fourth request of that group. Thus the stream at cell 4 is A followed by Cs forever, up to a halt. Its initial A on the virgin suffix installs the pair `21` without visiting cell 6. At group \(q\), exactly \(q-1\) subsequent pulses have been applied. The short checker follows the literal instructions through the first three groups and checks the repeated phase.

For an occupied cell with an already visited right neighbor, the following table gives the new digit and the entire outgoing packet. The empty packet ends the pass.

| Old digit | A | B | C |
|---|---|---|---|
| 1 | 4, A | 2, empty | 4, B |
| 2 | 4, B | 1, empty | 4, A |
| 4 | 1, empty | 4, C | 1, C |

The A and B columns follow from the transition string and the mature child's left return in A. Composing B then A gives the C column. Every input therefore sends at most one packet to the next cell. A single pulse can be evaluated in one left-to-right pass.

## Exact growth recurrence

Start with the empty word \(w\). At each checkpoint the occupied segment from cell 4 rightward is \(w21\), with blank exterior. Digits of \(w\) are all 1 or 4. The last odd cell has received its first B and still has a virgin neighbor. Run successive C pulses through this finite strip using the table. Stop on the first pulse whose output is nonempty. Let \(k\) be the number of pulses including that one.

Until the first nonempty output, the last odd digit is 1 or 2. Its B entries toggle those digits without calling its right neighbor. Its first A either writes 3 and sends A from digit 1, or writes 3 and sends B from digit 2. In the first case the virgin even cell returns in A, so the ordinary table applies at the odd parent. The new even cell and its neighbor have become `21`. In the second case the virgin even cell executes B0 and immediately returns in B to the waiting odd digit 3. This is the actual undefined instruction. A C at the pending odd cell consists of one such B followed by A. The table's first nonempty output at the exterior is consequently either A or B.

On a full traversal every old digit ends on 1 or 4. Define the new binary word as the updated old strip. It has length \(|w|+2\). If the output was A, the full physical configuration for the next stage is this new word followed by `21`. Each new stage starts in the same group phase. A pulse occurs during the fourth root request, and the remaining request in that group sends nothing to cell 4.

Every produced binary word also avoids the factor `141`. A new 1 requires an incoming C on digit 4, forwarding C. If the next updated digit is 4, that incoming C met 1 or 2 and forwarded B or A. The following updated digit therefore cannot be 1. This restriction holds for every full traversal, including those after the first successful traversal of the altered seed below.

For the parity test give packets B and C weight one, and give A and silence weight zero. On each entry in the table, the parity of the change in the indicator “digit is 2” equals the difference of incoming and outgoing weights modulo two. Sum first over the strip and then over the \(k\) pulses. The initial strip has one digit 2 and the projected final strip has none. Every input pulse has weight one. All but the last exterior output are silent. Hence
\[
  1 \equiv k + [\text{last exterior output is B}] \pmod 2.
\]
This is an equivalence for the blank machine by induction from its literal startup. On a B output the projected final strip is used only to determine the packet. The literal parent halts before its modeled return completes. Each successful stage uses a positive finite number of elementary instructions. Infinitely many odd waits therefore suffice for blank nonhalting.

## Why the wait is finite for every binary word

In a mature cell, A and C toggle between digit 4 and the other two digits. B preserves that class. Consider an eventually periodic packet stream with an odd number of toggles in a full repeating word \(P\). Reading \(P\) sends each of 1 and 2 to 4 and sends 4 to one specific other digit. After at most one traversal the boundary states therefore alternate with period two. Corresponding input positions in the next two copies of \(P\) start in opposite classes.

The emitted period also has an odd number of toggles. Every B or C in \(P\) emits C on its digit-4 visit. Every A or C in \(P\) has one visit in the other class. There it emits A precisely when the parity of the preceding run of B packets equals the indicator that the input is C. The previous toggle on that traversal left digit 1, and the intervening Bs toggle it between 1 and 2. Take these B runs cyclically. Writing \(h\) for the number of toggles, their contributions to the count of emitted As sum to \(h+\#B+\#C\) modulo two. The emitted Cs contribute another \(\#B+\#C\). The resulting toggle count is odd.

Beginning with one repeated C, induction carries this property across any finite strip of mature cells. After \(m\) cells the root-time period is at most \(2^m\), with a repeating block of that length that contains an outgoing toggle. Its onset is at most \(1+2+\cdots+2^{m-1}=2^m-1\) root pulses. In the finite-strip projection the first nonempty output therefore occurs by pulse \(2^{m+1}-1\) for any starting digits. For a growth stage use \(m=|w|+2\). The pending physical odd cell agrees with the projection up to the decisive call as proved above.

The finite first-return table in the checker exploits the binary reset. Given a binary strip and the first-return table for its left portion, take successive left returns until the last digit emits a packet. Every such left return supplies the successor binary left portion and its exact elapsed time. For the empty strip the next return is C in one pulse. This gives an independent scalar implementation.

## A periodic comparison and a failed induction

There is an exact safe input fixed by a fresh pair of cells. Let \(P=\mathrm{ABABB}\). On its first copy, a fresh pair emits ABAB and finishes on 44. From 44 each further copy emits BABAB and restores 44. Thus a pair fed \(P^\omega\) emits \(P^\omega\) at the next pair, with the same distinguished start. Every new pair consumes its first A, so a finite input prefix cannot visit infinitely many new pairs. The actual source at cell 0 is \(\mathrm{AB}\,P^\omega\), and the actual source at cell 4 is \((\mathrm{AB})^\omega\). This finite initial discrepancy changes the later periods.

One attempted induction used a succession of safe binary resets as its hypothesis. With the same constant C source, the altered binary word `44441111114144144141` followed by `21` survives **15 consecutive odd waits** and then reaches B3. The last wait is 8,207,912 pulses. The total is 12,212,553 pulses. The checker computes the waits exactly and replays the final failing packet on the literal strip. The example has an altered initial tape. It shows why counting earlier odd waits alone does not establish the next one.

## Verification

From this directory, run `python3 line13_pulses.py` with assertions enabled. The checker derives the packet table from the instruction string, checks the source phase, compares the first eight new-pair arrivals with the literal blank machine, and verifies the altered-tape example.

The rank search preserves each output packet's position in the root input. Batch a shallow strip of already mature cells. Starting at source pulse zero, let a depth-\(d\) startup span \(2^d-1\) root slots and the following period span \(2^d\). At the next cell the new startup is the old startup plus one period. The new period consists of the following two old periods. The odd-toggle argument above verifies the repeated boundary state. Each bit in a selection mask records whether that input slot produced a packet. Selecting the ordinal of a child packet and descending the stored masks gives its exact root pulse. Beyond the shallow strip the search processes finite chronological chunks. A fresh pair consumes its first A when it becomes 21. An initial B there identifies B3 at the preceding odd cell.

The C++ checker compares its bit operations and selected positions against the scalar packet table. The Python wrapper also checks multiple shallow-strip widths against direct chronological growth and compares all 64 six-digit binary seeds through 128 pulses, including actual B3 cases on altered tapes. The native A/B replay uses the separate pre-existing implementation and reconstructs the entire positive tape and elementary clock. For \(q\ge1\) the numbers of rightward entries at cells 0–3 are \(5q,3q+1,3q,q+1\). The negative-half cost is \(15q^2\). If \(J_x\) counts expanded A/B entries, positive-half instructions are \(2\sum_x J_x-J_0\). All clocks here count defined instructions.

The short checker also audits the long batch. Cells 4 through 157 took 9,014,488,734,238,432,784 expanded A/B entries during that batch. At each mature cell, let \(S\) be the number of single packets emitted to its child. Every incoming A changes the digit-4 indicator, and exactly the changes into 4 emit a single packet. Thus the number of incoming As is \(2S+[\mathrm{start}=4]-[\mathrm{end}=4]\). A fresh pair first consumes A and sends its mandatory B to the odd child. Accounting for that initialization recovers the separate A and B totals from each neighbor's packet counts. The checker tests the B-parity balance at every cell, the constant input at cell 4, the single B at 157 and the raw clock above.

Run from this directory. The long searches use several GB of memory. The C++ rank worker also has a portable path for processors without the two optional x86 bit instructions.

```sh
c++ -std=c++20 -O3 -march=native line13_rank.cpp -o /tmp/bb25-rank13
python3 line13_pulses.py --rank /tmp/bb25-rank13
python3 line13_pulses.py --rank /tmp/bb25-rank13 --until-groups 1152921504606846977
c++ -std=c++17 -O3 frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-stream
python3 line13_pulses.py --native /tmp/bb25-stream
```

The exact endpoint in the command checks the published opening and furthest cell against a replay from the older checkpoint. With a larger group number the rank search resumes from the new terminal tape. The A/B replay checks the terminal clock and tape as well and prints its progress every 50,000,000,000,000,000 groups or sooner at a recorded opening.

The earlier analysis proved that an infinite blank run must keep facing fresh odd cells and derived a deadline for cell 155. [Paired stream analysis](https://github.com/valu42/busycoqtesting/blob/c970885c2e6dce20b0a712d310ba16982660e2f5/research/bb2x5/halting-outlook/pair13.md) · [Earlier clock bound](https://github.com/valu42/busycoqtesting/blob/c970885c2e6dce20b0a712d310ba16982660e2f5/research/bb2x5/halting-outlook/timing13.md)
