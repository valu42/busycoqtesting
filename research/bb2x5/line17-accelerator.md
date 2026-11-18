# Line 17 accelerator and first-overflow timing

Machine `1RB2RA3LB---2LB_2LA0LA4RB0RB1LA` starts in A on an all-zero, two-way tape. The clock counts defined elementary instructions. The 424-pair counting phase starts at instruction 2,308,940. Its next overflow first brings the head, in B, to the previously unseen cell +12. The sole halting instruction is A scanning 3, which can occur on a later return.

## Exact blank-tape run

The deepest completed blank run reached **10,706,070,760,419,157,619,517,903,863,810 sweeps** without halting. Its exact clock is **1604679315779428558158711107420718740667238049241268905851427862** raw instructions (≈ 1.60468 × 10^63). The head is in A at -21,412,141,520,838,315,239,035,807,728,464. Pair 191 received one input. The terminal received zero slots. This is approximately **11,462×** the raw clock at the previous independently published 10^29-sweep checkpoint. [Latest resumable checkpoint](frontiers/runs/line17-epochs.json) · [Per-pair instruction counts](frontiers/runs/line17-aligned-1e31-counts.txt)

At the intermediate **10^30-sweep checkpoint**, the machine has executed exactly **14000000000000000000000000000145389392205733010185916014084982** defined raw instructions and is in state A. Pair 186 received one input, the deepest of pairs 0–423 reached in this phase. No slot reached the singleton. The clock is about **100×** the [previous 10^29-sweep checkpoint](https://github.com/valu42/busycoqtesting/blob/12c4acdce3310d435190895136f65826a702f1c8/research/bb2x5/frontiers/runs/line17-epochs.json) and about 278× the initial 6 × 10^28 run on this research branch. [Intermediate checkpoint](frontiers/runs/line17-1e30.json)

The [parallel simulator](frontiers/line17_tiles.cpp) splits each packed pulse word into tiles. A first pass computes each tile's action on the six possible trit and pending-bit states. Composing those actions in order gives the exact entering state for each tile. The tiles can then emit bits, probe counts and instruction counts in parallel. The simulator multiplies a period only on recurrence of the complete digit state. Large words use temporary files. A finite tail retains its own phase, including a partially consumed marked burst. The [driver](frontiers/line17.py) reconstructs all six local pulse counts from the emitted slots, probes and internal moves at every pair. It checks trit conservation, matches completed bursts to incoming marks and pending flags, and requires zero outgoing slots at the terminal before saving an ordinary sweep checkpoint.

On the available host, four threads with passive OpenMP waiting replayed the 10^30 sweeps from the verified 424-pair entry in **11 min 59.7 s**. Shorter replays took 1.7 s at 10^20 sweeps, 4.4 s at 10^22, 12.9 s at 10^24 and 23.9 s at 10^26. These are single wall-clock measurements during shared-host use. At 10^30 the period at cut 107 contained 70,476,474,672 bits. The number and length of these words determine the computer time. Dividing a forecast raw clock by this run's effective raw instructions per second would give a misleading ETA.

The tiled worker also reproduced the full previously published 10^29 checkpoint from blank, including its SHA-256 checksum, in 5 min 26.8 s on this host. The existing 17 register and edge tests passed. A second implementation replayed the literal blank trajectory through 837 complete sweep boundaries, including the two earlier overflows. At both new endpoints, both native workers and an independent physical fixed-register interpreter matched the entire register, head, state and elementary clock over a further 10,001 sweeps. [Independent checker](frontiers/line17_literal_check.py) · [Saved per-pair counts](frontiers/runs/line17-1e30-counts.txt)

For the larger run, `--at-least` chooses a sweep boundary at which the early digit periods all end together. The simulator tracks the transient, period length in root sweeps, and local costs for each digit. Once the cut's word grows past the chosen limit for generating further periods, it streams complete copies through the remaining digits. At cut 108 one such word has 140,952,929,200 slots and 17,619,113,632 marks. The source supplies one copy every 1,784,345,126,736,526,269,919,650,643,968 sweeps after the two-sweep offset. The selected boundary consumes exactly six copies. All 108 aligned prefix rows passed the cycle-state, mark and clock-balance checks. The earlier packed worker independently matched every count and ending state for the first 95 pairs. [Period sizes and alignment](frontiers/runs/line17-aligned-periods.txt)

The four known marks in the homogeneous region occur at local slots 5, 11, 17 and 23. The table records the deepest pair each mark had entered. A mark can take many additional sweeps to reach just one more pair. These fronts therefore give a direct measure of how far the decisive suffix is from the simulation.

| Sweeps | Slot 5 | Slot 11 | Slot 17 | Slot 23 | Deepest pair entered |
|---:|---:|---:|---:|---:|---:|
| 10^29 | 173 | 169 | 165 | 161 | 175 |
| 10^30 | 184 | 180 | 176 | 172 | 186 |
| 10,706,070,760,419,157,619,517,903,863,810 | 189 | 185 | 181 | 177 | 191 |

The two later rows follow directly from the saved cumulative slot counts. Cut 403 is the entrance to the final 21 pairs. [Earlier mark fronts](https://github.com/valu42/busycoqtesting/blob/12c4acdce3310d435190895136f65826a702f1c8/research/bb2x5/line17-edge-time.md)

## The fifth future mark is fixed

At cut 403 the first five marked slots of the true input are **5, 11, 17, 23 and 29**. The next mark can occur no earlier than slot 33. The previous 10^29 checkpoint fixes only the first four by this calculation. The larger aligned run still gives these same five. Cut 403 itself has received zero slots in both checkpoints.

The [pending-burst simulator](frontiers/line17_drain.py) reads the physical boundary at 10^30 sweeps. It completes the pending bursts while supplying unmarked root slots. At each pair, a marked input can generate at most one child mark before the following input mark, and later input marks cannot change an earlier child's position. Deleting all future input marks therefore leaves an initial segment of the real child marks. That property composes across the register. The all-zero continuation is used only to isolate marks whose positions are already determined. The separation and the slot-65 lower bound below ensure the first 32 slots at cut 403 are physically received before +12.

There is a short independent check. At cut 168 the measured input has 29 slots and five marks. Its first four and the initial 26 bits are known, leaving only slots 27, 28 and 29 for the fifth. Of these three possibilities, only slot 29 produces the observed ending trit 1 with a pending pulse. Starting at trit 1 with a clear flag, a pair receiving this sequence reproduces the same first five marked positions. All remaining pairs up to cut 403 start in that state. On the known upstream prefix the sixth mark at cut 163 occurs at slot 34, moves to 33 at cut 164 and dies at the next pair. A later ancestor must supply the sixth mark at cut 403. [Drain proof](frontiers/line17-drain.md) · [Finite prefix check](frontiers/line17_mark_prefix.py)

## Guaranteed timing of the next overflow

The first visit to +12 occurs by sweep **1.592 × 10^165** and before **3.545 × 10^331** raw instructions. The prior published ceiling was 3.176 × 10^344 raw instructions. The calculation anchors an exact period at cut 108, then bounds how much of that repeating input must reach later pairs. It assumes ordinary replies only up to the first contact. [Derivation](frontiers/line17-period-envelope.md) · [Certificate and exact integers](frontiers/runs/line17-period-bound-aligned-five.json)

The terminal receives its first input between slots **65 and 81,526,469** at cut 403, immediately before the final 21 pairs. The upper endpoint uses the five known marks followed by the slowest admissible continuation. The four-mark prefix previously gave 81,526,541. [Five-mark suffix calculation](frontiers/runs/line17-five-mark-suffix.json) · [Replay](frontiers/line17_suffix_prefix.py) For the lower endpoint, the true cyclic stream at cut 53 has mark gaps of at least four. Consider two consecutive surviving input marks a distance of k mark intervals apart. Write G for their total separation and r,s for their starting trits. The intervening marks all have residue zero. The timestamp recurrence makes their child gap (G+4k−r+5s)/3. Here G≥4k, r≤2 and s≥1, so the integer child gap is at least four. This holds through all 350 clear homogeneous pairs.

The [suffix checker](frontiers/line17_slot_floor.py) enumerates every permitted continuation of the 26 known cut-403 bits in increasing length. Equal complete physical suffix, pending state and mark cooldown give the same future choices. The first possible visit is at slot 65. A continuation attaining it is marked at 5, 11, 17, 23, 29, 37, 41, 46, 51, 55, 59 and 63. The checker also lifts that example through all 350 homogeneous pairs after one genuine cut-53 period. The true upstream period repeats indefinitely, so the witness does not determine the blank machine's return. [Prior upper endpoint and decision slots](line17-edge-time.md)

## How long until the next overflow?

A working estimate is **of order 10^150 elementary instructions**. Different plausible growth laws move this estimate by nearly nine orders of magnitude. These experiments measure sensitivity to the growth law and to the width of the register. They supply no calibrated probability interval for the actual machine.

We shortened only the long run of identical `02` pairs. Each variant keeps the original header, its initial marked digits, its last 21 physical pairs and the distinguished root input `0100`. The 21 widths run from 31 through 131 in increments of five. For each one, the [width experiment](frontiers/line17_width.py) finds the first root slot that reaches the singleton. A separate forward pass starts immediately before that sweep and checks the triggering slot. These are auxiliary starting tapes. Only the full 424-pair configuration has the claimed blank-tape provenance. [All 21 first arrivals](frontiers/runs/line17-short-widths.jsonl)

| Register pairs | First sweep reaching the singleton |
|---:|---:|
| 31 | 11,189 |
| 61 | 20,344,422,438 |
| 81 | 136,336,455,585,066 |
| 86 | 101,123,887,735,351 |
| 111 | 42,202,720,100,314,632,294 |
| 131 | 93,100,751,524,546,815,175,974 |

The decrease from width 81 to 86 illustrates a phase effect. Across the 21 variants the last 21 pairs required between 273 and 7,602 incoming slots, with median 1,883. Each width supplied its own actual ordered input to this suffix.

**A transmission model.** A mark arriving at trit 0 dies. At trit 1 or 2 it emits one child mark. In a surrogate with an independent uniform initial trit at each pair with a clear pending flag, each incoming mark sees a uniform residue. For a fixed input word its residue is a permutation of the starting trit. It therefore has mean two compound pulses and a 2/3 chance of emitting a child mark. The marks in one stream can be correlated. For mean long-run input slot rate L and mark rate M, the output rates are (L+8M)/3 and 2M/3. Their limiting common ratio is 2/3 per pair. Calibrating the mean rates at cut 53 predicts about 1.54 × 10^-17 slots per sweep at cut 95, where the measured complete-period rate is about 1.537 × 10^-17. Early individual slots can arrive much sooner than the reciprocal mean rate suggests. The real homogeneous pairs all start at trit 1. Treating the surrogate transmission rate as a long-distance law for those pairs is the forecast assumption.

| Extrapolation to 424 pairs | Implied first-overflow sweep | Implied raw clock |
|---|---:|---:|
| Fixed transmission rate. Median of log10(sweeps) − width × log10(1.5) over all 21 widths | 1.70 × 10^74 | 4.03 × 10^149 |
| Fit both slope and intercept by ordinary least squares to the same 21 log clocks | 4.61 × 10^78 | 2.97 × 10^158 |

Fitting the fixed-rate intercept on the first 13 widths alone and predicting the remaining eight gave observed-to-predicted sweep ratios from 0.77 to 5.74. A second check kept both fits trained on the original 21 widths and moved each test width by one pair. On these 20 held-out widths, 32, 37, …, 127, the median factor between predicted and observed sweep counts was 2.60 for the fixed slope and 1.96 for the fitted slope (using the larger divided by the smaller). The two models perform similarly at the tested widths while giving very different forecasts at 424. The true width is 293 pairs beyond the largest test. Small changes in the fitted slope compound over that distance. The experiments also share input and suffix structure, so their errors cannot be treated as 21 independent draws. [Recompute both fits](frontiers/line17_width.py) · [Held-out timings](frontiers/runs/line17-adjacent-widths.jsonl)

**What that means on this computer.** The aligned run took 1,391.475 seconds (23 min 11.475 s). Of those, 866.569 seconds streamed 845,717,575,200 cut-108 slots, about 976 million slots per second. Keeping this cut and the measured throughput fixed, the 1.70 × 10^74-sweep scenario would require about 4.36 × 10^38 years of streaming. The 4.61 × 10^78-sweep scenario would require about 1.18 × 10^43 years. The calculation multiplies sweeps by the exact cut rate of 7.8994 × 10^-20 slots per sweep and uses 365.25-day years. Such a run would also require wider finite-stream counters. These are cost estimates for a fixed algorithm and memory budget. A way to select future marks directly could change the cost entirely. [Measured timings](frontiers/runs/line17-aligned-timing.json)

**A check conditioned on the fifth mark.** We also tried every cyclic shift of the exact cut-59 period whose first 32 bits match the newly established cut-403 prefix. Feeding those 1,264 substitute streams to the actual last 21 pairs gave a median of 2,486 suffix slots to first contact. The 5th and 95th percentiles across those shifts were 336 and 7,713. At the extrapolated mean input rate of 8.93 × 10^-72 slots per sweep that median corresponds to about 2.79 × 10^74 sweeps, or 1.09 × 10^150 raw instructions. The real cut-403 stream has one distinguished phase and a different period. These substitute quantiles measure sensitivity to the unknown continuation. [Phase experiment](frontiers/line17_phase.py) · [Counts and ranks](frontiers/runs/line17-phase-comparison.jsonl)

**Converting sweeps to raw instructions.** Let E be the number of the sweep that first visits +12. For the E−1 completed sweeps, the header and growing pile alone cost 58(E−1) + 14(E−1)(E−2). For an upper bound, complete E virtual sweeps with ordinary replies at the terminal cut and charge its first real B2 move separately. At cut i, count input slots nᵢ and marked inputs Mᵢ. At the root n₀=4E and M₀=E. Each incoming mark and any initially pending burst can emit at most one mark, so Mᵢ≤E+i. At most 3(Mᵢ+1) compound slots run at the pair. The slot identity 3nᵢ₊₁+v′=nᵢ+v+4C implies nᵢ≤6(E+i) by induction. A pair costs at most 14 instructions per input slot in the crossing-count formula. Charge at most four probes per input at the final cut. Including initialization gives

```text
2,308,940 + 14(E−1)² + 44(E−1) < first visit to +12
first visit to +12 ≤ 14E² + 35,684E + 9,851,901.
```

Thus using 14E² in the table contributes negligible error at these sweep counts. The uncertainty comes from estimating E. [Exact local costs and checkpoint convention](frontiers/README.md#line-17-and-the-exact-cost-of-a-header-sweep)

## Halting after overflow

The [exceptional-sweep simulator](frontiers/line17_pile.py) follows the physical head through the entire growing pile. It caches a block crossing only when the contents, entry side and entry state match. A crossing records the rewritten block, the exact instruction count, and either the exit or the scanned halt. On the two historical blank-orbit resets it reproduces the first visits to +10 and +11 at instructions 2,628 and 2,306,191, then the 20- and 424-pair headers at 2,889 and 2,308,940.

Among the 21 shortened configurations, **10 halted and 11 reached a new header**. Three halts required another accelerator. It recognizes the entire tape pattern `24044 (04)^L [A0] 13031302 D 2` against blank exterior, where D is the fixed data word. The embedded header sends the same data probes as the original header, consumes one left `04` and adds one `12` to the right pile per ordinary sweep. Its three header paths cost eight more local instructions each. After checking that L sweeps produced zero terminal calls, the worker reconstructs the full tape and finishes the return physically. On the 116-pair variant, reaching A3 took a further 8.599 × 10^41 raw instructions after the first virgin-cell visit.

In ten of the resets the new width was the old width plus the number of previously completed ordinary sweeps plus 2. In one it was that sum plus 4. Both historical resets of the real machine used the latter offset. On the separate grid of 20 shifted widths, 12 halted and 8 reset. These observations support one mechanism for extremely long gaps between chances to halt. They do not fit a halt probability on the full machine. [Physical returns for the first grid](frontiers/runs/line17-analogue-returns.jsonl) · [Returns for the shifted grid](frontiers/runs/line17-adjacent-returns.jsonl)

For illustration, suppose the next real return resets after about 10^74 sweeps, creates a register of about 10^74 pairs, and that register also takes roughly 1.5^width sweeps to overflow. In that scenario the base-ten logarithm of the *following* raw clock is of order 10^73–10^74. The new width, the trit and flag pattern, and the growth law at that width are all assumptions.

The community estimate assigns a 20–35% halt chance per overflow. Under an independent constant-chance model, that gives a median of two to four further overflows. Only two previous overflow outcomes have been observed on this blank trajectory. Both reset. The distribution of the next actual reset width and the timing of later overflows remain unknown, so the experiments do not give a raw-step median or a wall-clock ETA to a halt. [Original probability attribution](https://wiki.bbchallenge.org/w/index.php?title=1RB2RA3LB---2LB_2LA0LA4RB0RB1LA&oldid=8484) · [Conditional overflow-count quantiles](halting-outlook/line17.md#conditional-count-quantiles-and-limits-of-the-runtime-model)

## Reproduction

Run from `research/bb2x5` with Python 3.10+ and assertions enabled. The native workers require a C++17 compiler and GMP. The build below uses OpenMP and POSIX mapped files. The `-mssse3` flag enables the x86 SIMD path. Omit it for the scalar path. Give it a writable working directory with room for temporary packed words.

```sh
c++ -O3 -std=c++17 -fopenmp -mssse3 frontiers/line17_tiles.cpp -lgmpxx -lgmp -o /tmp/bb25-tiles17
c++ -O3 -std=c++17 frontiers/line17_packed.cpp -lgmpxx -lgmp -o /tmp/bb25-packed17
python3 frontiers/line17.py --tiled-engine /tmp/bb25-tiles17 --threads 4 \
  --epochs 1000000000000000000000000000000 --word-bits 160000000000 \
  --depth --checkpoint /tmp/line17-1e30.json
BB25_TILE17=/tmp/bb25-tiles17 BB25_PACK17=/tmp/bb25-packed17 python3 frontiers/test_line17_tiles.py
python3 frontiers/line17.py --tiled-engine /tmp/bb25-tiles17 --threads 4 --at-least \
  --epochs 10000000000000000000000000000000 --word-bits 250000000000 \
  --depth --checkpoint /tmp/line17-aligned.json
python3 frontiers/line17_literal_check.py --self-test
python3 frontiers/test_line17_pile.py
python3 frontiers/line17_width.py --engine /tmp/bb25-packed17 --cuts $(seq 10 5 110) > /tmp/widths.jsonl
python3 frontiers/line17_width.py --summarize /tmp/widths.jsonl --validation frontiers/runs/line17-adjacent-widths.jsonl
python3 frontiers/line17_width_return.py /tmp/widths.jsonl --engine /tmp/bb25-packed17
python3 frontiers/line17_slot_floor.py
python3 frontiers/line17_drain.py frontiers/runs/line17-1e30.json
python3 frontiers/line17_mark_prefix.py frontiers/runs/line17-1e30-counts.txt
python3 frontiers/line17_suffix_prefix.py 5
c++ -O3 -std=c++17 frontiers/line17_phase.cpp -o /tmp/bb25-phase17
python3 frontiers/line17_phase.py --engine /tmp/bb25-phase17 --cuts 53 59 --marks 4 5
```

The [period-bound derivation and replay commands](frontiers/line17-period-envelope.md) use the saved exact counts and periods. The [intermediate cut-99 result](frontiers/runs/line17-period-bound-99.json) can also be checked with the original packed worker.
