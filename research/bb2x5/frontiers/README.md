# Running the BB(2,5) simulations

[The simulation table](../SIMULATION_TABLE.md) tracks the largest counted blank-tape endpoint for each of the 37 encodings. Each file under `runs/` records a complete configuration and its checksum. Simulation can continue from any verified file. Checksums establish file integrity. The experiments use native code and Python.

From `research/bb2x5`, build the moving-window simulator with a C++17 compiler and replay or extend any line with Python 3.10 or later.

```sh
c++ -O3 -std=c++17 frontiers/window.cpp -o /tmp/bb25-window
python3 frontiers/survey.py --engine /tmp/bb25-window --line 14 --width 8 \
  --target 10000000000 --work 10000000000 --checkpoint /tmp/line14.json
python3 frontiers/survey.py --engine /tmp/bb25-window --line 14 \
  --resume frontiers/runs/window-14.json --target 12000000000 \
  --work 1000000000 --checkpoint /tmp/line14-next.json
```

A lookup starts at the join between two adjacent base-five words. The key includes both words, the side of entry and the control state. It composes literal first exits from individual words and stops at an exit, a halt or a local work cap. Even a capped lookup returns its precise intermediate position, symbols and defined-step count. The outer loop takes individual transitions when a jump would pass the target. Fixed-size caches replace old entries and compare complete keys on every hit. The native counter accepts absolute targets through 2^60. Word width may change on resume.

The initial window survey used width 8 and a limit of 10 billion window operations per machine. It targeted 100 billion raw steps on lines 7 and 13, 100 million on lines 3, 5, 17, 26, 29 and 30, and 10 billion elsewhere. Every target was reached. Each snapshot stores the occupied interval as compressed symbols, its left endpoint, and the absolute head, state and step count. Earlier, deeper results take precedence in the table where applicable. To refresh the table after saving checked results run `python3 frontiers/scoreboard.py`.

## Exact batches of boundary crossings

Lines 8, 11, 12, 13, 21, 22 and 31 have periodic responses from the initially blank negative half of the tape. The left-half periods and their discoverers are recorded in [the earlier sweep analysis](../mixed-and-sweeps.md). The simulator uses those responses to send an exact sequence of calls through the nonnegative cells. One call starts on a cell from its left and ends on the first move back to the left. A batch ends with the head at coordinate zero. The checksum covers the raw time, control state, number of completed periods and every visited nonnegative cell, including visited zeros.

1. `Driver` checks which states can be returned by a visited cell. It runs both first-call states on a literal virgin suffix. On the negative half it executes the complete one- or two-cell transition table and checks that a block's j-th request to the next block refers to an earlier available response. It checks closure after the transient, including the subordinate call phase. This gives the contents, local cost and subordinate call count for any number of inputs. Repeated residues in the strictly decreasing sequence of subordinate counts allow the program to sum local times as arithmetic progressions and encode every negative cell.
2. For the nonnegative half, each cell translates its incoming requests into the ordered requests it sends to its right neighbor. Cell state includes the symbol and whether the neighbor is still virgin. The first return on a virgin suffix was measured directly. Later returns follow the checked transition-table condition. Input words are stored as a prefix, a repeated word with an arbitrary-precision multiplicity, and a suffix. A whole repeated word can be skipped when the cell returns to the same complete state at the same word boundary.
3. A successful batch ends at a depth with zero further requests. Induction back from this depth realizes every predicted return on an actual finite tape excursion. With E entries at coordinate zero and S entries summed over all nonnegative cells, those cells execute exactly 2S−E instructions. Every entry exits left once, and each subordinate entry costs one rightward call from its parent. A prospective undefined instruction, a local call cycle or a materialization limit stops the batch with the previous checkpoint available for a smaller retry.

For example, after 5q positive excursions and their negative replies on line 13 the negative tape in physical left-to-right order is `(133)^q`. The negative half alone has taken 15q² instructions. At q = 10^16 the run has visited 144 nonnegative cells. The recorded step count includes the exact positive-half time as well.

Build with GMP and a C++17 compiler. From `research/bb2x5` the following commands replay or extend the saved results. `stream-recipes.json` lists `[repeat_count, groups_per_batch]` for exact replay from blank.

```sh
c++ -O3 -std=c++17 frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-stream
python3 frontiers/replay_streams.py --engine /tmp/bb25-stream --line 13
python3 frontiers/longitudinal.py --engine /tmp/bb25-stream --line 13 \
  --resume frontiers/runs/stream-13.json --groups 100000000000000 \
  --batches 1 --checkpoint /tmp/line13-next.json
BB25_WINDOW=/tmp/bb25-window BB25_STREAM=/tmp/bb25-stream python3 frontiers/test_longitudinal.py
```

The tests compare full tapes and raw times with the literal interpreter on all seven lines. They check batch splitting both at blank and beyond each published endpoint. A separate comparison runs line 13 to 81,648 groups, expands the entire physical tape and advances it with the moving-window simulator to its independently saved 100-billion-step checkpoint.

## Line 7 and exceptional returns

At the start of a blank-tape epoch, A scans a fresh zero to the left of a finite word. A0 writes a guard 1 and sends B into that word. A return to the guard in B writes 3 and starts the next epoch one cell to the left. A return in A reaches the undefined A1. The recorded word gives every cell to the right of the fresh head. Epoch zero is the initial blank tape.

The line 7 simulator counts a batch of N calls having the same entry state into a suffix. Its result gives the number of completed B replies and the first exceptional A reply or physical halt, if present. The following calculation applies until an exception from the right.

| Entry and initial digit | Child requests | Digit after N successful calls |
|---|---|---|
| A on 2 | 3N calls in A | 2 |
| A on 4 | N calls in B | 4 |
| B on 2 or 4 | ⌊(N + [digit = 4])/2⌋ calls in A | Toggles between 2 and 4 on each call |

If M child calls all reply in B, the parent executes N+M instructions. In a packet with d divisions by two, write N = 2^d h+r. The descendant count and sum of local instruction counts are affine in h, and all final digits depend only on r. Their coefficients are cached against the complete initial packet, state and residue. A run of k twos entered in A sends 3^k N calls into its suffix, with local cost 2N(3^k−1).

An exceptional child is handled in chronological order. After j ordinary child replies, A on 2 has completed ⌊j/3⌋ parent calls and is waiting on digit 3, 4 or 0 according to j mod 3. A on 4 has completed j and is waiting on 2. B has completed 2j+[initial digit = 2] and is waiting on 0. For p completed parent calls add p+j+1 local steps to include the outstanding request. A returning child resumes the actual suspended instruction, and an undefined entry at any depth immediately propagates its physical halt coordinate. Nonordinary symbols use the literal transition table. The implementation keeps the active calls on an explicit stack.

```sh
python3 frontiers/line7.py --epochs 4096 --checkpoint /tmp/line7.json
python3 frontiers/line7.py --resume frontiers/runs/line7-calls.json \
  --epochs 10000 --checkpoint /tmp/line7-next.json
BB25_WINDOW=/tmp/bb25-window python3 frontiers/test_line7.py
```

`steps_hex` is the exact unsigned raw time. The checkpoint stores the physically located suffix, head, state and completed left extensions. Use `int(payload['steps_hex'], 16)` in Python. `--every` sets the save interval in epochs and `--work` bounds the number of unit or packet operations in an invocation. Each completed save can be resumed. The external line 7 run linked in the table goes much farther and provides context for this reproducible local run.
