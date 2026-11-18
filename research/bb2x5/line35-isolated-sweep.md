# Can one sweep halt machine 35?

**A first isolated pulse can halt only on the sweep when it arrives.** Start at blank epoch 15 and measure the unmatched closings sent left across cell 28 at each sweep. Call a reading of 0, 1 or 2 quiet. If there is just one higher reading, the machine halts exactly when that reading reaches the threshold computed from the current 28 cells. If it passes, every later quiet sweep is safe. The first possible fatal reading is seven. A physically executed alteration attains seven on the genuine epoch-87 prefix. The blank run itself stays quiet through the sweep from epoch 365,590. Resolving the machine requires control of the exterior on the infinite blank orbit. [Executable sweep](line35_isolated_sweep.py) · [Finite proof](line35_isolated_proof.py) · [Independent checks](check_line35_isolated_sweep.py)

## What the sweep measures

The machine is `1RB2LA4RA1LA3LA_0LA3RB3LB2RB---`. At an epoch boundary A scans the blank immediately left of its finite word. The cell immediately to the right of the head is cell 1. A 1 is an opening, a 2 is a closing, and a 3 is neutral. Let $b(P)$ be the number of openings minus closings in the first 28 cells $P$. Let $h(P)$ be the largest excess of closings over openings in a prefix of $P$, including the empty prefix. The remaining cells send a debt $d$ equal to their own largest prefix excess. The guard reads

$$H=\max\bigl(h(P),d-b(P)\bigr).$$

The [28-cell theorem](line35-chronological-strip.md#the-first-28-cells) gives $h(P)\le5$ at every reached blank epoch from 15 onward. Thus the **exact** fatal reading is $d\ge6+b(P)$. The scanner also computes $H$ on the full word, checks the equality, and records the closing cells that cross the cut, the openings that absorb them, and their birth epochs if they were born during the recorded run. Physical cell numbers and the head coordinate at B4 are reported separately. On successful sweeps it advances the complete tape and raw clock by the [timed return rule](https://github.com/valu42/busycoqtesting/blob/1a47b45f468aa296f57255a7a127ce137464c69d/research/bb2x5/line35-timed.md).

For a failing word let $f$ be the position of the sixth unmatched closing. In cells 1 through $f$, match each closing at $i$ with its nearest available opening $p_i$ to the left, using zero when it has no partner. Put $A_f=\sum(i-p_i)$ over these closings. The sweep takes exactly **$2A_f+18$ defined instructions**. To first reach $f$, the head travels a net $f$ cells right. Earlier closings account for $A_f-f$ units of backtracking. The third through fifth guard uses each add one, and the reset adds five more, giving $f+2(A_f-f+8)$ moves to that point. The last closing takes $f+2$ left moves to B4. Relative to the original head, the terminal head is at $-2$. The final nonblank word starts at $-3$ with `3433`, then $f$ threes, then the untouched input from cell $f+1$ onward. The interpreter checks the whole terminal tape and clock. [Literal comparisons](check_line35_isolated_sweep.py)

## Which pulse histories are safe forever?

All results below start from the exact epoch-15 prefix. A gap is the number of intervening readings at most two. Each finite certificate contains the seed and is closed under every permitted successor. The checks use the prefix and incoming debt only. A bound on the true exterior satisfying any row would decide the machine.

| Allowed readings at cut 28 | Required gap | Certified prefixes | Largest guard |
|---|---:|---:|---:|
| All at most 2 | 0 | 20,286 | 3 |
| All at most 3 | 0 | 58,682 | 5 |
| All at most 4 | 11 | 49,826 | 5 |
| All at most 6 | 43 | 50,156 | 5 |
| Any size, provided each high reading is below its current fatal threshold | 8 | 128,716 | 5 |

For a single pulse, the quiet closure has 20,286 prefixes. Their exact fatal thresholds range from 7 to 33. All larger-than-two inputs below the corresponding threshold give 13,262 distinct immediate successors. From these, the three quiet choices reach 71,627 prefixes. Every outgoing quiet edge succeeds and stays in that set. Thus even a pulse much larger than six can be survived permanently when the current prefix absorbs it and the later readings stay quiet.

For repeated pulses, the verifier stores the smallest remaining wait for each reachable prefix. A smaller wait allows every continuation of a larger one. It checks each edge against the finished table. It also passes **1,603,448 distinct prefix/debt inputs** through the independent scalar word sweep. One fewer intervening quiet sweep admits an abstract counterexample in each of the last three rows. The gap-42 counterexample already uses readings at most five. In the gap-seven example all high readings pass, then a reading of two halts. Each edge has its own literal tape realization. The examples do not establish a single blank-generated exterior producing the sequence. [Certificates and replayable counterexamples](line35_isolated_proof.py)

## Where a pulse actually lands

| Starting tape | Reading at epoch 87 | Outcome |
|---|---:|---|
| Blank, unaltered | 1 | Guard 2. The sweep succeeds. |
| Epoch 83 with two extra copies of its ten-cell block | 5 | Guard 4. Five sweeps take 3,676 instructions. |
| Epoch 83 with three extra copies | 7 | Cell 62 triggers B4, 656 instructions into this sweep and 3,404 since the edit. |
| Epoch 80 with 95 inserted delayed blocks | 6 | Guard 5. Eight sweeps take 144,193 instructions. |
| Epoch 80 with 96 inserted delayed blocks | 7 | Cell 1,223 triggers B4, 141,981 instructions since the edit. |

The epoch-83 block is `1231111112` at zero-based indices $[14,24)$. In the fatal control the unmatched closings are cells **1, 15, 47, 52, 57 and 62**. The control starts with its head at zero. At epoch 87 its head is at −4. It processes cell 62 at coordinate +58 and ends in B scanning 4 at −6.

For the epoch-80 controls insert copies of `2` followed by ten `1`s immediately before the terminal closing. Their first seven readings are $1,0,0,0,1,0,0$. Their first 28 cells at epoch 87 equal the genuine prefix. In the fatal case the unmatched closings are **1, 15, 1190, 1201, 1212 and 1223**. This distinction matters on blank. If all preceding readings were quiet, the first fatal pulse needs at least seven units. Every cell past cut 28 already existed five sweeps earlier, since a sweep adds at most five cells. The permanent terminal pair `12` cannot set a new deficit record. Thus any trigger past cell 28 lies in the ordinary cells, and losing seven openings needs at least 37 of them. Its trigger must therefore be **cell 65 or farther right**. The epoch-83 control had only four sweeps since its edit. The longer control has the full five-sweep ancestry. [Interval length proof](line35-chronological-strip.md#five-ordinary-sweeps-on-the-same-interval) · [Literal controls](check_line35_isolated_sweep.py)

## Blank replay and the next 54 sweeps

Starting from blank reproduced the published epoch-300,001 checkpoint. The next **65,536** sweeps reached epoch **365,537** after **436,079,626,737** instructions. The entire 743,397-cell word, head at −377,861 and raw clock also agree with an independent replay using synchronized right-hand triples. In this extension the cut sent zero 50,070 times, one 13,993 times and two 1,473 times. The smallest gap to the fatal threshold was eight at epoch 300,088. At epoch 300,027 cells 29 and 31 supplied two closings, and prefix cells 28 and 26 absorbed them. The report includes all four birth records. [Checkpoint](frontiers/runs/line35-isolated.json) · [Extension and cell witnesses](frontiers/runs/line35-isolated-report.json) · [Independent paired simulator](https://github.com/valu42/busycoqtesting/blob/d6f72418c0056b47948fb2a4b5182810e586c57d/research/bb2x5/line35_band.py)

At this checkpoint the rightmost 428,388 cells form a permanent zero-debt suffix. There are 315,009 cells to its left. Give the checker only $x$ visible cells from the left and the width up to that cut. At every future step let the boundary survivor vary freely. The universal guarantee changes with $x$. [Permanent-zero-cut proof](https://github.com/valu42/busycoqtesting/blob/d6f72418c0056b47948fb2a4b5182810e586c57d/research/bb2x5/line35-seam.md)

| Visible left cells | Hidden cells before the cut | Consecutive sweeps certified safe |
|---:|---:|---:|
| 63,002 | 252,007 | 1 |
| 157,504 | 157,505 | 3 |
| 314,981 | 28 | 50 |
| 315,009 | 0 | 54 |

For each unknown gap, bound its greatest prefix debt $E$ using the five-ancestor length bound. Count young cells and any terminal cell outside that rule at their full width. If the visible prefix has internal deficit $h$ and $s$ surviving openings, the whole guard is at most $h+\max(0,E-s)$. When $E\le s$ the header is fixed. All completions share the part of the next word to the left of the rightmost $E$ survivors that might be erased. Retain that common prefix and repeat. If several safe headers are possible the checker certifies that sweep and stops there. If the upper bound reaches six the forecast ends there.

Full-word replay separately checked every forecast guard. At epoch **365,591** the machine is in A at −377,915 with 743,505 cells after **436,208,497,795** instructions. Across the 365,576 full-cut sweeps from epochs 15 through 365,590, the maximum observed cut-28 reading remains two. [54-sweep replay record](frontiers/runs/line35-isolated-forecast.json) · [Simulation table](SIMULATION_TABLE.md)

## Replay and continue

From `research/bb2x5` run

```sh
python3 line35_isolated_sweep.py --epoch83-copies 3 --sweeps 5
python3 line35_isolated_proof.py
python3 check_line35_isolated_sweep.py
python3 line35_isolated_proof.py --checkpoint frontiers/runs/line35-isolated.json
python3 line35_isolated_sweep.py --checkpoint frontiers/runs/line35-isolated.json --sweeps 54 --save /tmp/line35-365591.json
```

To reproduce the saved tape independently from blank, run the first command below. To reproduce just the 65,536-sweep extension, use the remaining two. A run with `--word` or `--epoch83-copies` creates an experimental checkpoint whose clock starts at the edit. A report records the last reached boundary and any subsequent B4 separately.

```sh
python3 line35_isolated_sweep.py --sweeps 365536 --save /tmp/line35-from-blank.json
git show 1bcfb761d57825838ebeb1b4587235fa918928f3:research/bb2x5/frontiers/runs/line35-band.json > /tmp/line35-300001.json
python3 line35_isolated_sweep.py --checkpoint /tmp/line35-300001.json --sweeps 65536 --save /tmp/line35-365537.json --report /tmp/line35-extension.json
```

**Open decision route.** Prove that the material born on the genuine blank tape keeps the readings at cut 28 at most three. A weaker sufficient target allows readings through six with 43 quiet sweeps between them. If a genuine reading above two is found, locate its source closings and the openings that absorb them. A first fatal pulse after a quiet history must draw seven units from cell 29 onward. The birth records and cell-1,223 control give an explicit case for testing any proposed exclusion. [Claim or hand off this route](ROADMAP.md#claim-board)
