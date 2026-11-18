# Line 20 and the exceptional B return

Line 20 reached 60,000,000,006,399,999,696,354 defined instructions from blank after 100,000,000,000 periods. The [checkpoint](runs/stream-20.json) gives the state at coordinate zero and all 181 visited nonnegative cells. The period count reconstructs the entire negative tape and its cost using `Driver.left`.

The [negative-half certificate](../mixed-and-sweeps.md#5-other-candidates-and-verification) gives the responses `BAAAB` followed by repetitions of `ABA` whenever a positive excursion returns in A. On the nonnegative half the instruction B2 writes 3 and exits left in B. All other defined leftward transitions exit in A. B1 is the machine's actual undefined instruction.

For bulk simulation we mark B2 undefined on the nonnegative half only. The stream worker stops if a batch could encounter this guard or B1. If it finishes, every subordinate call returned A and every instruction it counted belongs to the original machine. Each completed batch uses the [boundary-stream clock](README.md#exact-batches-of-boundary-crossings) for both halves. If it stops at a candidate, the driver bisects to a single period and runs that period on the original positive tape in chronological order. It checks the state at every return to coordinate −1 before applying the compressed negative-half reply. A B return that reaches −1 would invalidate that reply and stop the computation.

The first 329 periods run without a guard. In period 330, the original machine reads B2 at raw times 672,396 through 672,399 at coordinates 34, 33, 32 and 31. The resulting B return is absorbed inside the positive half. The period completes with A at coordinate zero at 674,448 steps. Every subsequent period through the saved endpoint passes the guarded simulation. This establishes a finite blank-tape run. Halting remains open.

From `research/bb2x5`, replay from blank in two batches, then compare the saved file.

```sh
c++ -O3 -std=c++17 frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-stream
python3 frontiers/longitudinal.py --engine /tmp/bb25-stream --line 20 --groups 1000 \
  --max-bits 33554432 --checkpoint /tmp/line20-seed.json
python3 frontiers/longitudinal.py --engine /tmp/bb25-stream --line 20 \
  --resume /tmp/line20-seed.json --groups 99999999000 --max-bits 33554432 \
  --finite-slots 10000000000 --checkpoint /tmp/line20.json
cmp /tmp/line20.json frontiers/runs/stream-20.json
```

To continue, use the saved checkpoint with `--resume` and give the number of **additional** periods with `--groups`. Smaller batches reduce the finite-stream memory and work required for one invocation.

`test_line20.py` compares all tape cells, head, state and clock at the exceptional period against the literal interpreter. It also materializes a later boundary state and uses the moving-window engine to reach the previously saved ten-billion-step tape.

```sh
c++ -O3 -std=c++17 frontiers/window.cpp -o /tmp/bb25-window
BB25_STREAM=/tmp/bb25-stream BB25_WINDOW=/tmp/bb25-window python3 frontiers/test_line20.py
```
