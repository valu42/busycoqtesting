# Line 24 · alternating sweeps with an exceptional return

Line 24 is `1RB3LA1LA2RB2RA_2LA4RA3LB1RA---`. The community holdout list credits dyuan with longitudinal analysis of this machine. The formulas below follow directly from its transition table. [Community holdout notes](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved)

After 46 defined instructions, the head enters coordinate zero in A. The nonblank cells on either side of the cut are `1121 | 331332`. Group zero denotes this boundary. Each subsequent complete group sends A, then B, into the nonnegative tape. The simulator checks that both calls return to coordinate −1 in A before it counts the group.

## The negative tape and raw clock

At the start of group g, put m = 2g+1. The negative word is `11 2^m 1` ending at −1. On an A return there, the head crosses left over all m+3 symbols, rewriting the word as `33 1^m 3`. The instructions A0, B3, A3 extend the tape left and bring B to the first of the m ones. From B each pair `11` becomes `22` in four instructions (B1, A1, A4, A3). On the remaining `13`, B1 and A3 leave `42` and move right into coordinate zero in B. The negative word is now `11 2^m 42`. This first sweep took 3m+6 instructions.

On the second A return, A2 and A4 replace the final `42` with `21` and return A to −1. Now the same left crossing and rightward pair rule act on `11 2^(m+1) 1`. This time the run of ones has even length. Its final 3 takes B3, leaving 1 and entering coordinate zero in A. The resulting word is `11 2^(m+2) 1`, and the second sweep cost 3m+12. The negative-half cost through G complete groups is therefore 6G(G+3). Between the two sweeps of group G, add 6G+9.

## Guarding the positive tape

On the positive half B2 is the only left-moving instruction returning B. The batched worker temporarily traps B2 along with the genuinely undefined B4. Each completed call in the guarded machine then returns A, including the first call on blank. The [boundary stream simulator](README.md#exact-batches-of-boundary-crossings) sends the repeated AB inputs through successive cells, accumulating their exact local costs. A batch that finishes without touching either trap represents the same steps of the original machine.

If the worker encounters a trap, the simulator bisects the batch in chronological order. At one group it executes the original positive instructions, including B2, and counts both negative sweeps from the formulas above. A physical B4 yields a halt. If B returns across coordinate zero, the left-sweep hypothesis fails and the simulator stops at the previous saved boundary. Literal-work and stream-size limits also leave the previous checkpoint available.

## Replay and checks

From `research/bb2x5`:

```sh
c++ -O3 -std=c++17 frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-stream
python3 frontiers/line24.py --engine /tmp/bb25-stream --groups 17179869184 \
  --batch 268435456 --word-bits 2097152 --finite-slots 268435456 --checkpoint /tmp/line24.json
cmp /tmp/line24.json frontiers/runs/line24-sweeps.json
BB25_STREAM=/tmp/bb25-stream python3 frontiers/test_line24.py
```

To extend the run, add `--resume frontiers/runs/line24-sweeps.json` and increase the absolute `--groups` target. The saved positive word and group count give the complete physical tape. Differential checks compare the raw clock, head, state and both tape halves with literal execution at small boundaries and with the independent 10-billion-step moving-window checkpoint. Two artificial inputs exercise a real B4 halt and a B return across the cut.
