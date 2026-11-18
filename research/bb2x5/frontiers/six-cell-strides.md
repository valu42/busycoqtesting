# Six-cell strides on lines 14, 16 and 28

The independent moving-window checkpoints at 10 billion raw steps contain long runs of the following six-cell words. Each example is aligned at an absolute coordinate divisible by six.

| Line | Observed tiles |
|---|---|
| 14 | `113132`, `440200` |
| 16 | `031313`, `130313`, `131303`, `220220` |
| 28 | `032323`, `232303`, `230323`, `101101` |

Two stacks represent the tape to either side of a cut aligned to a multiple of six. Each stack stores a word and its multiplicity, with the nearest word on top. The simulator starts in A at coordinate zero on blank tape.

Consider a rightward move of the cut. The head now scans the first cell to the right of the cut in state q. Let G be the six-cell word immediately behind it and W the next six-cell word ahead. The worker executes the chosen machine’s rules on GW until their first exit. If the exit is to the right with state q and final tape DG, the head is in exactly the same position relative to G as before. For k consecutive copies of W it can replace `G W^k` by `D^k G`, moving the head 6k cells to the right and adding k times the observed local instruction count. The same check with reversed positions applies when moving left. The arbitrary exterior cells play no role before that first exit. Each cache hit compares both complete words, entry side and state.

When those conditions fail, the worker retains the ordinary two-word trace. A trace that reaches its 512-instruction work limit inside a pair resumes from its actual position. If a jump would overshoot the requested raw clock the worker shortens the batch or takes literal instructions. Reaching an undefined instruction stops the simulation on the scanned cell. The saved endpoint uses the same physical tape format as the moving-window survey, including the absolute head and the clock from blank.

All three machines reached 1,000,000,000,000,000 raw steps from blank.

| Line | Two-tile operations | Head and state | First nonzero cell | Occupied span |
|---|---:|---|---:|---:|
| [14](runs/stride-14.json) | 2,411,932,479 | −6,184,044 in B | −15,190,109 | 15,193,623 |
| [16](runs/stride-16.json) | 128,948,904 | +64,633,136 in A | −62 | 65,269,682 |
| [28](runs/stride-28.json) | 109,643,944 | −34,327,352 in A | −54,857,023 | 54,857,059 |

On each line, a further million literal instructions agreed with a continuation from the recorded endpoint on the clock, head, state and complete tape.

From `research/bb2x5`, replay the endpoints and test the simulator.

```sh
c++ -O3 -std=c++17 frontiers/six_cell.cpp -o /tmp/bb25-stride
for line in 14 16 28; do
  python3 frontiers/six_cell.py --line "$line" --engine /tmp/bb25-stride --target 1000000000000000 \
    --checkpoint "/tmp/stride-$line.json" && cmp "/tmp/stride-$line.json" "frontiers/runs/stride-$line.json" || exit 1
done
BB25_STRIDE=/tmp/bb25-stride python3 frontiers/test_six_cell.py
```

Pass `--resume frontiers/runs/stride-14.json` and a larger absolute target to continue. The tests compare the complete tape, head, state and clock with literal execution at short stops, including a constructed B3 halt, and reproduce the independent 10-billion-step moving-window checkpoints from blank on all three lines.
