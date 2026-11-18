# A permanent zero-debt cut and a genuine 47-cell match on line 35

**Once $k$ right-hand triples are synchronized at an odd epoch, the cut before the last $3k$ cells sends zero matching debt to its left at every future sweep.** At blank epoch 300,001 this applies to **352,224 cells**. At that epoch 257,890 cells lie to the left of the cut. Subsequent growth on the left cannot affect the right-indexed suffix. The result applies to its entire virtual future and hence to every later physical sweep that is reached. Establishing safety of the growing left part remains open. [Blank checkpoint](frontiers/runs/line35-band.json) · [Executable proof and comparisons](line35_seam.py)

The full covered suffix has $2+3k$ cells. Move the cut two cells toward the right end. It now lies immediately after the first opening of the outermost triple, reading from right to left. Write $a$ for the center of the previous inner triple, with virtual $a=C$ at the permanent cap. On the odd sweep the opening receives zero debt, so it survives and sends zero debt. Its right-neighbor survivor bit is $[a\ne C]$. The intermediate digit at this same right index is $D(1,[a\ne C])$, and the debt it receives on the intermediate sweep is $[a=N]$. The three cases are

| Previous center | Intermediate digit | Incoming debt | Outgoing debt | Outgoing survivor |
|---|---|---:|---:|---:|
| $O$ | $O$ | 0 | 0 | 1 |
| $C$ | $N$ | 0 | 0 | 0 |
| $N$ | $O$ | 1 | 0 | 0 |

After the pair the triples remain synchronized. Thus this cut has zero outgoing debt in both phases indefinitely. The same proof applies to every cut after $3i$ cells for $1\le i\le k$. A cut may also follow the growing covered suffix by advancing from $3k$ to $3k'$ at the next odd epoch with $k'\ge k$. In particular the *entire* left strip can be matched internally at each sweep. The surviving bit on the right still determines a digit at the interface. [Pascal recurrence](line35-pascal.md) · [Neighboring cut with nonzero debt and an exact time budget](line35-pressure.md)

## The right side contributes a single binary input per pair

Hold one such cut fixed and write $U$ for everything to its left. On the odd sweep $U$ receives zero debt and survivor one. Its matching, guard, header and *entire* next left strip are therefore determined by $U$. On the even sweep $U$ again receives zero debt, so its second guard is determined as well. If both sweeps succeed, only the rightmost digit of the next odd strip can depend on the even survivor bit. In fixed right-index coordinates a cell writes $D(s_{\rm cell},s_{\rm right})$. Every other right neighbor is already in the known strip. Thus the two guard outcomes are **exactly** computable from $U$ alone. In terms of the preceding section the only right-hand input to the paired successor is $1-H_{k-1}$ on the even sweep.

At epoch 300,001 this gives a completely specified periodic binary input for the remaining 257,890-cell strip. Its period is **131,072 pairs**, with 65,328 even survivors equal to one per period. The period follows from the augmented Pascal recurrence. For index $j=k-1>0$ the period divides $2^{\lceil\log_2(j+1)\rceil}$, and the $j$-th temporal difference of $H_j$ is $H_0=1$, excluding the smaller power of two. The checker computes the entire period from the saved centers. The strip width and contents can still grow, so this finite input period does not settle its guard.

For arbitrary initial synchronized center bits the first $k-1$ of those control bits can be prescribed freely. At paired time $t$ the value $H_{k-1}(t)$ is $\sum_{i=0}^t\binom ti H_{k-1-i}(0)$ modulo two when $t<k-1$. The last coefficient is one. The desired samples successively determine $H_{k-1}(0),H_{k-2}(0),\ldots,H_1(0)$, all outside $U$. This statement concerns choosing a normalized starting tape. The true blank run has the specific register in its checkpoint.

## When the repeating pattern actually appears on blank

The 47-cell circular pattern used in the [large-margin counterexample](line35-band.md#why-the-numerical-test-needs-a-reachability-argument) first develops an excess closing on its 888th update. A finite copy of this pattern can arise inside the blank machine. Number right indices from zero and take the 47 cells at indices $1350,\ldots,1396$. On blank epochs **1069 through 1074** all 47 digits agree with circular phases **875 through 880**, with rotation 2 in right-to-left order. At epoch 1068 the two words differed at 19 positions. At epoch 1074 they still agree, but their inputs for the next sweep differ.

On the blank tape the cut at 1,350 has been protected since odd epoch **979**, when 450 triples first synchronized. Its actual signal at epoch 1074 is zero debt and a surviving opening. The circular row requires debt one and no survivor there. At epoch 1075 three of the 47 symbols differ. At epoch **1082**, when the circle has one more closing than opening, the true interval instead has **eleven more openings than closings**. The proof of zero debt rules out the circular transition at the indicated true cut for all possible inner center phases. A matching row alone does not identify the next row on this interval.

## The excess closing also occurs outside the protected suffix

At blank epoch **2022** the 47 cells at right indices $[3213,3260)$ match the *final*, negatively balanced circular row, rotated by 25. In physical left-to-right indices they are $[852,899)$ of the 4,112-cell word. At the preceding epoch the same right indices matched circular phase 887. The protected zero-debt cut was only 2,451 cells from the right, so the permanent suffix theorem does not cover this occurrence.

The literal interpreter reaches the start of epoch 2022 in A at head −2,091 after **13,293,131 defined instructions**. The interval receives zero debt and sends **one** unit left. The next cell is neutral. The following cell is an opening and absorbs the unit. The guard sees zero debt and the sweep succeeds. Thus an invariant forbidding this 47-cell factor anywhere on the blank tape is false. The question is how much debt a sequence of such intervals can transmit before intervening openings absorb it. The optional literal replay checks every blank-tape instruction through this occurrence.

## What cell births rule out

At a successful sweep the numbers of new right-index columns are two or five. In order of increasing right index, their possible physical digit packets are `32`, `12`, `31`, `13`, `13231`, `13131`, and `11331`. The first digit is $D(v,s)$ for the leftmost old survivor $s$ and virtual bit $v$, followed by the physical header in reverse. These seven possibilities cover every legal guard debt, even if the packets at consecutive sweeps are chosen independently. [Birth rule](line35-guard-stream.md#an-exact-recurrence-for-the-blank-orbit)

Along all 888 updates of this circular trajectory, **at most 45 consecutive newborn digits** can match the prescribed circular values at their individual birth times. This bound allows arbitrary spatial phase and arbitrary portions of the temporal trajectory. For each phase $j$ of the old leftmost index, the checker retains the longest trailing match in birth order. It tries each allowed packet, compares its letters with the next circular row from $j+1$ onward, resets the length on a mismatch, and moves to $j$ plus the packet length modulo 47. This finite recurrence includes matches beginning or ending inside a packet. Thus every complete 47-cell copy formed during these frames must contain a cell that started with the wrong digit.

Subsequent correction is physically possible. At circular phase 107 take two copies in increasing right-index order starting at phase position 45 modulo 47, place them above a bare $OC$ cap, and start A on the blank immediately to the left of the resulting **96-cell nonblank tape**. In the next 47 cells born to its left, **24** first digits disagree with their prescribed ring digits. After **49 sweeps and 24,195 literal instructions** all 47 cells agree with the phase-156 circular row. The checker directly executes the original two-state machine on this finite seed. These two results distinguish direct production of a dangerous ring at birth from the possibility that initially different cells later synchronize. On blank the unresolved case is synchronized growth in the uncovered strip, outside the permanent zero-debt cuts.

Run `python3 line35_seam.py --literal --checkpoint frontiers/runs/line35-band.json` in this directory for the instruction-by-instruction replay and the future control period.
