# Fused simulation of line 17

The fused simulator follows the blank machine `1RB2RA3LB---2LB_2LA0LA4RB0RB1LA` during ordinary sweeps of its 424-pair register. The [latest checkpoint](runs/line17-epochs.json) records its physical tape, state, head and elementary clock. The [cumulative counts](runs/line17-coded-counts.txt) reconstruct that checkpoint from the blank-entry configuration. A period of a prefix of the register is a separate result. The machine's clock advances to a published checkpoint only after the simulator has propagated every pulse to the end of the register and verified that the singleton received none.

## Completing a marked burst early

At the entrance of the homogeneous region, marks on the genuine periodic stream are at least four slots apart. A marked input to a clear physical trit consumes that slot and possibly one or two following plain slots. The small virtual transducer emits the complete burst at the marked slot. An unmarked slot advances the virtual trit modulo three and emits a single zero exactly when the old trit was two.

| Trit before mark | Emitted word | Virtual trit immediately after mark | Following plain slots until physical catch-up |
|---:|---|---:|---:|
| 0 | `0` | 2 | 0 |
| 1 | `010` | 1 | 1 |
| 2 | `00010` | 0 | 2 |

The catch-up slots produce no further virtual output. After them both versions have the same ordered output and trit 2. Separation prevents a new mark during catch-up. Composition preserves the ordered infinite word. A finite prefix can end partway through a burst, so the implementation also accounts for pulses already emitted by the virtual model that the physical register still owes.

A plain input acts on the virtual trit by adding one modulo three. A marked input acts by mapping $v$ to $2-v$ modulo three. Both are permutations. A block of $d$ virtual digits consequently has $3^d$ phase states. Compiling a legal sixteen-slot mask gives the ending phase, emitted bits and slot and mark counts at every digit. For six or seven digits, the x86 SIMD path represents the action on the first five digits by a permutation and the action on each following trit by a sign and an offset modulo three. A scalar implementation evaluates the same table.

## Physical boundaries and elementary costs

The worker feeds the last 128 source tokens to every possible **physical** starting state of the fused block. It retains the distinct legal ends. Starting from each end, it supplies plain inputs until all pending bursts finish. If that takes $n$ inputs, subtracting $n$ from the resulting clear base-three counter modulo $3^d$ gives the virtual phase. The worker requires a unique physical end for every virtual phase. This resolves the actual pending flags at the seam of the source period.

During the same plain continuation, a virtual block emits only zeros. Subtract that zero suffix from the physical continuation at each cut to obtain its owed word. For a finite interval the physical output consists of the starting owed word followed by the virtual interval output, with the ending owed word removed. The worker compares every removed bit with the independently computed owed suffix. It passes the resulting stream, in order, through the remaining physical pairs.

For one pair, let $n,m$ be the input and output slot counts and let $v,v'$ be the physical endpoint trits. The number of compound pulses is $C=(3m+v'-n-v)/4$. With $M$ incoming marks and starting and ending pending bits $p,p'$, the raw call count is $n+2C+M+p-p'$. If $M'$ marks were emitted, the internal move count is $2(m+M')$. The Python driver checks all 424 rows, tests the terminal, adds the exact header and pile costs, and saves the complete physical configuration after each source copy.

## Reducing the cost of each source copy

Across all 250 complete source symbols and 27 possible entrance phases of three trits, only 160 different ordered output words occur. Allowing all legal short final symbols increases that count to 164. The emitter interns each word by both its bits and its length. Its second table applies the remaining four trits to the interned word. Together these tables need 37,638 histogram entries for seven trits, down from 1,972,674. At startup the worker compares every composed ending phase with the independently compiled seven-trit action. Adjacent source copies can then share one disk pass, advancing up to four entrance phases together on each token.

Further down the tape, a table advances three physical pairs per input byte. Each transfer records the emitted word, physical ending state, slots and marks at each pair. The worker adds up to 32 local cost packets before unpacking them. The finite per-packet maximum keeps each ten-bit counter separate. Pending flags are part of the table address. Physical pair counts still reconstruct the elementary clock at every saved endpoint.

On 8,192 genuine cut-110 frames, two threads replayed four different entrance phases in 8.56 seconds with the flat seven-trit emitter and 4.13 seconds with split tables. Both produced the same ordered word and all seven slot and mark totals. In a separate end-to-end test, 160 consecutive copies of the small cut-59 period took 8.03 seconds with the flat emitter, 1.26 seconds with batched split tables and 0.85 seconds after grouping the physical suffix. Every interval's physical rows agreed byte for byte. These shared-host measurements cover the stated inputs and thread counts.

### Reusing a measured phase

For one fixed input period, the entering physical trits and pending flags through a given pair determine its entire output. Farther pairs cannot influence it during an ordinary sweep. The worker remembers the slot and mark counts for each such entry state. Once the first three pairs recur, it can skip their histogram. When all seven recur, it skips both histograms. It still emits the ordered bits, checks the ending phase of each stripe, carries the bits through the rest of the tape and counts what physically entered the suffix. A wrong last-cut tally fails that check even if the count file has a valid checksum.

The optional `--phase-counts FILE` retains each completed observation across runs. It binds the rows to the source checksum, cut and fusion depth. The [saved cut-111 phase counts](runs/line17-phase-counts.json) come from the full blank-tape trajectory. On 900 genuine cut-110 frames at six entrance phases and one thread, the emitter took 1.19 and 1.26 seconds counting both histograms. Supplying both totals reduced the two timings to 0.71 and 0.72 seconds. Both paths produced the same 87,277,433 ordered output slots. These timings exclude the physical suffix and disk spooling.

## Periods beyond the disk budget

The source at cut 110 contains 187,936,890,096 slots and 23,492,006,848 marks. It repeats every 5,353,035,380,209,578,809,758,951,931,904 root sweeps after sweep two. The following orders were computed by composing exact frame actions. The physical suffix check resolved all 2,187 phases of the seven-digit block. An independent direct computation on the 1,296 physical states of four digits reproduced the first four orders.

| Cut | Copies of the cut-110 period per closed orbit | Emitted slots per period |
|---:|---:|---:|
| 111 | 3 | 375,872,944,880 |
| 112 | 9 | 751,745,054,448 |
| 113 | 27 | 1,503,489,273,584 |
| 114 | 81 | 3,006,977,711,856 |
| 115 | 243 | 6,013,954,588,400 |
| 116 | 243 | — |
| 117 | 486 | — |
| 118 | 486 | — |

For each threefold lift every incoming mark sees all three trits, produces two child marks in total, and consumes six compound pulses across the three phases. Writing $L,M$ for the parent's period length and marks gives $L'=L+8M$ and $M'=2M$. This determines the first five lengths in the table. The last three rows record phase orders only. A separate seven-trit index on the newly materialized cut-111 stream reproduced the overlapping orders and established that cut 118 has the same period as cut 117. The cut-117 period spans approximately $2.60\times10^{33}$ source sweeps. It describes the prefix under ordinary replies. [Exact integers and check dimensions](runs/line17-virtual-periods.json)

## Running the simulator

Run the following commands from `research/bb2x5`. The exported word at cut 110 needs about 11.75 GB of disk in decimal units. Building it also uses temporary space. More than one phase per batch trades extra temporary disk for fewer reads of the source. The source checksum in the metadata covers its exact framing. Different valid frame boundaries can encode the same physical period.

```sh
c++ -O3 -std=c++17 -march=native -fopenmp frontiers/line17_tiles.cpp -lgmpxx -lgmp -o /tmp/bb25-line17
python3 frontiers/line17_virtual.py build --engine /tmp/bb25-line17 \
  --cut 110 --period /tmp/line17-cut110.code --threads 6
/tmp/bb25-line17 probe /tmp/line17-cut110.code 110 7 6
python3 frontiers/line17_virtual.py advance --engine /tmp/bb25-line17 \
  --period /tmp/line17-cut110.code --epochs 100000000000000000000000000000000 \
  --digits 7 --threads 6 --phase-batch 8 --index /tmp/line17-cut110-d7.index \
  --checkpoint /tmp/line17-latest.json --counts /tmp/line17-latest.counts
```

An existing source can advance one physical pair with the following command. The worker follows each starting phase until the complete trit and pending flag recur. It writes the phases in their original order and verifies every stripe endpoint. The cut-111 source needs about 23.5 GB. A cut-59 to cut-60 test compared every one of the 6,292,520 output slots against a separate export from blank, including the boundaries between frames.

```sh
python3 frontiers/line17_virtual.py lift --engine /tmp/bb25-line17 \
  --period /tmp/line17-cut110.code --output /tmp/line17-cut111.code --threads 6
```

To continue the published full-tape run toward $10^{34}$ sweeps, use the checkpoint and matching cumulative counts together. On the measured cut-111 stream, the source occupies 23,494,339,786 bytes and the seven-trit index about 310 MB. During a six-phase batch the other five phase streams occupy about 6.9 GB in the working directory. Keeping the cut-110 source as well uses another 11,749,096,276 bytes.

```sh
cp frontiers/runs/line17-phase-counts.json /tmp/line17-cut111-d7-counts.json
python3 frontiers/line17_virtual.py advance --engine /tmp/bb25-line17 \
  --period /tmp/line17-cut111.code --index /tmp/line17-cut111-d7.index \
  --seed frontiers/runs/line17-epochs.json --seed-counts frontiers/runs/line17-coded-counts.txt \
  --phase-counts /tmp/line17-cut111-d7-counts.json \
  --digits 7 --threads 7 --phase-batch 6 --epochs 10000000000000000000000000000000000 \
  --checkpoint /tmp/line17-further.json --counts /tmp/line17-further.counts
```

The optional stripe index saves the transfer of each piece of the source. Its companion checksum binds it to the exact source file and fusion depth. A resumed worker recomposes the whole action and reconstructs the physical phase from the saved trailing source tokens. Every emitted piece is checked against its expected ending phase.

The target is an absolute minimum sweep count. The worker stops at the first whole source copy at or beyond it. To continue from a compatible saved checkpoint, pass `--seed`. Supply its matching `--seed-counts` if cumulative counts are also requested. A new checkpoint is installed after each verified copy. During a batched disk pass several completed copies can become available together. The older fixed-target and packed workers remain available for cross-checks. [Driver](line17_virtual.py) · [Virtual phases](line17_ternary.hpp) · [Physical boundary reconstruction](line17_virtual.hpp)


The independent physical-period checker can run on the same exported source. It builds the transfer on all six physical trit and pending-bit combinations at each pair. At cut 110 with depth four its orbit has orders 3, 9, 27 and 81. The test suite also compares cumulative counts with the independent packed simulator on small periods containing pending boundaries.

```sh
c++ -O3 -std=c++17 -march=native -fopenmp frontiers/line17_physical_period.cpp -o /tmp/bb25-line17-physical
/tmp/bb25-line17-physical /tmp/line17-cut110.code 110 4 6
c++ -O3 -std=c++17 frontiers/line17_packed.cpp -lgmpxx -lgmp -o /tmp/bb25-packed17
BB25_TILE17=/tmp/bb25-line17 BB25_PACK17=/tmp/bb25-packed17 python3 frontiers/test_line17_virtual.py
```
