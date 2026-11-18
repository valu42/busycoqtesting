# Running the BB(2,5) simulations

[The simulation table](../SIMULATION_TABLE.md) tracks the largest counted blank-tape endpoint for each of the 37 encodings. Each file under `runs/` records a configuration and its checksum. The table links to the corresponding simulator. For the line 17 register the `--epochs` argument replays an absolute target from the checked blank-orbit entry. Checksums establish file integrity. The experiments use native code and Python.

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

Lines 8, 10, 11, 12, 13, 21, 22 and 31 have periodic responses from the initially blank negative half of the tape. Seven of the left-half periods and their discoverers are recorded in [the earlier sweep analysis](../mixed-and-sweeps.md). The simulator uses those responses to send an exact sequence of calls through the nonnegative cells. One call starts on a cell from its left and ends on the first move back to the left. A batch ends with the head at coordinate zero. The checksum covers the raw time, control state, number of completed periods and every visited nonnegative cell, including visited zeros.

1. `Driver` checks which states can be returned by a visited cell. It runs both first-call states on a literal virgin suffix and closes the set of reachable one-cell states over both possible inputs. Undefined branches produce a candidate. Any completed return must have the claimed state. On the negative half it executes the complete one- or two-cell transition table and checks that a block's j-th request to the next block refers to an earlier available response. It checks closure after the transient, including the subordinate call phase. This gives the contents, local cost and subordinate call count for any number of inputs. Repeated residues in the strictly decreasing sequence of subordinate counts allow the program to sum local times as arithmetic progressions and encode every negative cell.
2. For the nonnegative half, each cell translates its incoming requests into the ordered requests it sends to its right neighbor. Cell state includes the symbol and whether the neighbor is still virgin. The first return on a virgin suffix was measured directly. Later returns follow the checked transition-table condition. Input words are stored as a prefix, a repeated word with an arbitrary-precision multiplicity, and a suffix. A whole repeated word can be skipped when the cell returns to the same complete state at the same word boundary.
3. A successful batch ends at a depth with zero further requests. Induction back from this depth realizes every predicted return on an actual finite tape excursion. With E entries at coordinate zero and S entries summed over all nonnegative cells, those cells execute exactly 2S−E instructions. Every entry exits left once, and each subordinate entry costs one rightward call from its parent. A prospective undefined instruction triggers chronological bisection down to one period. The verifier then executes the actual nonnegative cells instruction by instruction. It sums the proved negative-half costs between excursions, which remain practical even at a huge clock. Only a physically scanned undefined instruction produces a halt checkpoint. A local call cycle, materialization limit or literal-work limit leaves the previous completed checkpoint available for a retry.

For example, after 5q positive excursions and their negative replies on line 13 the negative tape in physical left-to-right order is `(133)^q`. The negative half alone has taken 15q² instructions. At q = 2 × 10^16 the run has visited 150 nonnegative cells. The recorded step count includes the exact positive-half time as well.

The source for line 10 begins `BBA` and then repeats `AB`. Its negative cell after five outside calls has symbol 2, has made four subordinate calls and has spent nine local steps. After seven it returns to 2 with six subordinate calls and thirteen steps. Both source positions and both subordinate positions have the same period phase, so these two-call differences extend indefinitely. The simulator reads the actual transient and tracks the distinguished starting phase at every positive cell. This makes it possible to continue the blank run in the situation described in [the earlier line 10 period calculation](../research-log.md#line-10--exact-periods-lose-the-distinguished-starting-point).

Build with GMP and a C++17 compiler. From `research/bb2x5` the following commands replay or extend the saved results. `stream-recipes.json` lists `[repeat_count, groups_per_batch]` for exact replay from blank.

```sh
c++ -O3 -std=c++17 frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-stream
python3 frontiers/replay_streams.py --engine /tmp/bb25-stream --line 13
python3 frontiers/longitudinal.py --engine /tmp/bb25-stream --line 13 \
  --resume frontiers/runs/stream-13.json --groups 100000000000000 \
  --batches 1 --checkpoint /tmp/line13-next.json
BB25_WINDOW=/tmp/bb25-window BB25_STREAM=/tmp/bb25-stream python3 frontiers/test_longitudinal.py
```

The tests compare full tapes and raw times with the literal interpreter on all eight lines. They check batch splitting both at blank and beyond each published endpoint. For every supported line the tests locate the last batch boundary before its independent moving-window checkpoint, expand the entire physical tape, and advance to the same raw step using the moving-window simulator. The comparison covers 100 billion steps on line 13 and 10 billion on the other seven.

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

## Exact raw timing for line 5

The A and B families below are the two normal forms of mxdys and Racheline. In both families the physical state is A. The initial blank tape reaches A(4,4) in 136 defined instructions. The timed simulator uses the [existing normal-form recurrence](../arithmetic5.py) and [published analysis](https://wiki.bbchallenge.org/wiki/1RB3LA1LA1RA1RA_2LB2RA---4RB1LB).

Let C(a,k,b) have left word `1 4^a 1^k` and right word `1^b 2`, with the head scanning the first symbol of the right word. A(a,b) is C(a,4,b). B(a,b) has left word `1 4^a 1^(b+3)` and right word `11`. All other cells are blank. Each cost below is measured in defined raw instructions, including the final entry into an undefined instruction where applicable. `line5_timed.py` replays the nine local identities symbolically against the literal instructions using affine run lengths and opaque exterior tape. The blank initialization is checked separately.

| Local transition | Raw cost |
|---|---:|
| C(a+1,k,b+1) → C(a,k+2,b) | 2k+3 |
| C(0,k,b+3) → A(k,b) | 2k+15 |
| C(0,k,2) → B(k−2,3) | 2k+39 |
| C(0,k,1) → B scanning 2 (halt) | 2k+5 |
| C(a,k,0) → B(a,k−4) | 1 |
| B(a+3,b) → B(a,b+5) | 6b+42 |
| B(0,b) → B(b+3,0) | 2b+24 |
| B(1,b) → A(4,b+2) | 5b+72 |
| B(2,b) → B(b+5,2) | 6b+68 |

Here k ≥ 4. Starting at A(a,b), j = min(a,b) applications of the first row cost j(2j+9) and leave k = 4+2j. A complete doubling A(a,b) → A(2a+4,b−a−3) costs 2x²−3x+3 with x = a+4. Over K consecutive doublings put y = 2^K x. Their total cost is 2(y²−x²)/3 − 3(y−x) + 3K. From B(a,b) write a = 3q+r. The q triple reductions cost q(15q+6b+27) and leave B(r,b+5q), where the applicable residue row finishes the event. The Python and GMP engines tally these costs separately from the number of published recurrence events.

```sh
c++ -O3 -std=c++17 frontiers/line5_timed.cpp -lgmpxx -lgmp -o /tmp/bb25-time5
python3 frontiers/line5_timed.py --engine /tmp/bb25-time5 --rounds 100000 --checkpoint /tmp/line5-timed.json
python3 frontiers/line5_timed.py --resume frontiers/runs/line5-timed.json \
  --rounds 100100 --every 25 --checkpoint /tmp/line5-next.json
BB25_TIME5=/tmp/bb25-time5 python3 frontiers/test_line5_timed.py
```

A running snapshot records both integer parameters, the raw time in `steps_hex`, and the separate recurrence count in `events_hex`. The A/B word gives the complete tape up to translation. A physically halting snapshot records the predecessor of the certified terminal rule and the arrival time on B2. The Python engine saves intermediate rounds and resumes exact timing. The GMP engine replays from blank and saves at the requested return.

## Line 17 and the exact cost of a header sweep

The 424-pair register starts at raw step 2,308,940 with the head at −844. After E successful sweeps its physical word, immediately to the right of the head, is `231302 (12)^E D 2`. The saved checkpoint gives E, D, the head and the exact raw time. Each pair of D consists of a trit and an outgoing flag. The first call to the terminal singleton changes the return behavior. The timed simulator requires every output prefix at that cut to be empty. The register, pulse rules, and first-edge argument come from [the two-cell derivation](../frontier-background.md) and [the integer-register calculation](../marked-register.md).

For a digit i let Rᵢ count raw probes entering its pair, and let Iᵢ count moves between the two cells of that pair. Rᵢ₊₁ counts raw probes it sends to its child. Each completed incoming probe makes one left exit, each outgoing probe makes one right exit, and all remaining instructions move inside the pair. Thus its local cost is Rᵢ + Rᵢ₊₁ + Iᵢ. A simple pulse U always consists of one raw probe. The compound pulse C takes four probes for initial trit 0 and three otherwise. Literal two-cell traces give the following internal move counts for every possible normal return.

| Pulse | Trit 0 | Trit 1 | Trit 2 |
|---|---:|---:|---:|
| U | 0 | 0 | 2 |
| C | 2 | 6 | 4 |

The header uses 58 instructions plus its number of outgoing probes. Each leading `12` relays the four slots `0100`, takes nine raw input probes and makes ten internal moves. Its trit and flag reset at the end of the epoch. Summing the pair and header costs cancels the need to match individual probe positions. For E completed epochs the time from blank is

```
2,308,940 + 58E + 14E(E−1) + sum(2Rᵢ + Iᵢ over the 424 fixed data pairs).
```

The 14E(E−1) term sums 28k over pile lengths k = 0,…,E−1. On the fixed pairs, each unmarked run advances a trit modulo three. A mark at trit r starts a burst of r+1 compound pulses. The digit emits its child mark precisely when a compound pulse runs at trit 1. The simulator truncates a burst at the requested slot and retains its pending bit. The pending bit of digit i+1 gives the final outgoing flag of digit i. The last digit keeps its flag since the singleton receives no calls during a successful replay.

The first six digits use their complete finite-state transfers. Subsequent homogeneous digits skip complete input periods at equal trit and pending bit. After the selected cut, the native worker feeds bounded chunks of mark timestamps through the remaining homogeneous digits. Each digit retains its last mark until either another arrives or its precise end time becomes known. This supports finite prefixes that end midway through a burst. Arbitrary-precision Python counters cover the root clock and periodic part. The native worker bounds the size and arithmetic of finite timestamp lists, and the Python tail reads the final 21 nonhomogeneous pairs directly.

From `research/bb2x5`, replay the saved result from the blank-orbit entry or choose another absolute epoch target. The `--cut` parameter trades periodic-word size against the number of marks processed in the finite part.

```sh
c++ -O3 -std=c++17 frontiers/line17_marks.cpp -o /tmp/bb25-marks17
python3 frontiers/line17.py --epochs 1000000000000000000000 --cut 64 \
  --mark-budget 900000000 --engine /tmp/bb25-marks17 --checkpoint /tmp/line17.json
BB25_WINDOW=/tmp/bb25-window BB25_MARK17=/tmp/bb25-marks17 python3 frontiers/test_line17.py
```

The tests exhaust every normal pair/pulse control case, replay the complete physical tape through 425 epochs with an elementary interpreter, and meet the independent 100-million-step moving-window checkpoint. The Python-only timestamp implementation and a native replay using a different cut produce byte-identical full configurations and time at 10¹⁸ epochs.
