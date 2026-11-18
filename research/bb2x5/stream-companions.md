# Blank-run checkpoints and proof tests

These side investigations ran alongside the [line 35 interior investigation](https://github.com/valu42/busycoqtesting/blob/1a47b45f468aa296f57255a7a127ce137464c69d/research/bb2x5/line35-middle.md). The five runs below end at completed periods of their actual negative-half drivers, with the head at zero. Each file contains the full positive tape and exact clock. Each machine remains open.

| Line | Completed source periods | Defined instructions | Visited nonnegative cells |
|---:|---:|---:|---:|
| [8](line8-30.json) | $10^{30}$ | 15,000,000,000,000,000,000,000,000,000,027,931,427,720,955,941,384,312,401,887,148 | 280 |
| [10](line10-364361109000.json) | 364,361,109,000 | 531,036,071,028,458,284,326,732 | 272 |
| [21](line21-continuation.json) | 1,100,000,000,000 | 62,920,000,000,231,828,444,310,888 | 244 |
| [22](line22-continuation.json) | 3,100,000,000,000 | 499,720,000,000,545,856,615,725,540 | 219 |
| [31](line31-100t.json) | 100,000,000,000,000 | 500,000,000,000,006,291,295,299,965,206 | 152 |

Line 8 reduces to three possible nonempty signals between two-cell blocks. At the second terminal pair the true input is constant BA when each BA is treated as one compound signal. The halting question is whether a later terminal pair first receives a single A. The finite run was replayed with the stock simulator from its earlier checkpoint. [Reduction, literal checker and replay](line8-pairs.md)

On line 10 both incorrect cyclic rotations of the actual coordinate-3 period halt under free input. The authentic phase is BAA. An ordinary stack of $k$ cells traverses every one of its $3^k$ vectors under complete BAA periods. A five-cell packet implementation and the original stream engine gave identical full checkpoints at the new endpoint. [Proofs, forced-input controls and stock replay recipe](line10-control.md)

On line 26, the blank upper word at tick 144 is `002311332320312000000000000000`. The word `000000000000002323120311332000` has the same endpoint pairs and all the same counts of overlapping adjacent triples. It reaches B3 on its 2,135th tick. This rules out an inductive invariant that admits the blank checkpoint and depends only on those counts and endpoint pairs. The checker compares the reduced step with the literal eight-epoch return for both histories. The companion calendar independently reached cut 90. The active reserve investigation already reports width 204 at cut 96. [Trigram checker](line26_trigram.py) · [Reserve investigation](https://github.com/valu42/busycoqtesting/pull/7)

On line 31 two implementations agreed on all 152 visited nonnegative cells and the exact clock at the stated endpoint. The paired right-edge investigation continues separately. [Claim board](https://github.com/valu42/busycoqtesting/blob/master/research/bb2x5/ROADMAP.md)

For lines 21, 22 and 31, build the stock engine from this directory and run the corresponding command. A matching complete checkpoint is the comparison target.

```sh
c++ -O3 -std=c++17 frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-companions
python3 frontiers/longitudinal.py --line 21 --engine /tmp/bb25-companions \
  --resume frontiers/runs/stream-21.json --groups 200000000000 --batches 5 \
  --max-bits 268435456 --finite-slots 6000000000 --checkpoint /tmp/line21.json
cmp /tmp/line21.json line21-continuation.json
python3 frontiers/longitudinal.py --line 22 --engine /tmp/bb25-companions \
  --resume frontiers/runs/stream-22.json --groups 1000000000000 --batches 3 \
  --max-bits 268435456 --finite-slots 12000000000 --checkpoint /tmp/line22.json
cmp /tmp/line22.json line22-continuation.json
python3 frontiers/longitudinal.py --line 31 --engine /tmp/bb25-companions \
  --groups 100000000000000 --max-bits 1073741824 --finite-slots 100000000000 \
  --checkpoint /tmp/line31.json
cmp /tmp/line31.json line31-100t.json
```
