# When can line 429 halt?

**The blank-tape decision remains open.** Two Rocq theorems give exact criteria for this machine, ID 123915. One uses its original instruction table directly. The other checks the two complete half-tapes at the start of a sweep using finite automata.

## An exact test in original state F

The machine halts from blank if and only if it reaches **F scanning `00(10)^k001`** for some k ≥ 0. The word starts under the head and extends to the right. At such a configuration there are exactly **2k + 4** defined instructions before D reads 1, for every choice of exterior tape. For k = 0 the word is `00001` and the four instructions are F0, A0, B0, C0. Each additional `10` contributes B1, A0. [Reset theorem and exact times](Line429Reset.v)

The necessity proof follows the history of the final D1. Only a C0 instruction can enter D. If A1 entered C, A just wrote zero where D will look. A dangerous C0 must therefore have come from B. Tracing the B input back through preceding `10` pairs either finds the F reset or excludes the other sources of A using the symbols they just wrote. The induction starts on the actual blank tape. It proves that the F configuration occurs on that same run, before the halt. Fractal Geometry Explorer previously identified the last B scanning `001`. [Prior local proof](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/89e8153595f1e90de26c9e963b24d98bb4f4547d/holdouts/1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA0RF/README.md#halting-condition)

The following four cases exhaust finite-support tapes at reachable F scanning `00`. Skip the initial `00` and the maximal run of `10` pairs. F has a zero immediately to its left on every visit from blank. The proof gives the entire rewritten tape in every returning case. [Four-case proof](Line429ResetPass.v)

| Next bits | Result | Defined moves from F |
|---|---|---:|
| `01` | F scans the next cell beyond this pair | 2k + 4 |
| `11` | A scans the next cell beyond this pair | 2k + 6 |
| `000` | C scans the cell two positions left of the initial F | 4k + 20 |
| `001` | D reads 1 and halts | 2k + 4 |

## Two finite tests at a sweep checkpoint

Use the reflected and renamed table from the existing accelerator. Original E is normalized A, and the reflected blank start is normalized B. At a checkpoint, the normalized left half reads `0u` outwards. The scanned cell and the right half read `1w` outwards. Both finite words have implicit trailing zeros. The first checkpoint occurs after four elementary steps, with u empty and w = `11`.

**The original machine halts from blank if and only if a reachable checkpoint passes both tests.** The left automaton on u must return `Stop` and the right automaton on w must return `true`. Both tests are executable. The right test decides whether the following sweep can inherit the old left word's stopping outcome. If the joint test fails, the machine reaches another checkpoint after a positive number of elementary moves. This progress rules out an infinite sequence of bookkeeping operations before an unexamined halt. [Blank-tape theorem](Line429GateBlank.v) · [Left automaton](Line429LeftDFA.v) · [Right automaton](Line429Gate.v)

The rightward scan always turns on finite input. In particular, three consecutive zeros isolate everything farther to the right. The leftward scan can then be classified by the left tape alone. Each continuing case consumes a positive-length prefix. Its stopping cases take three moves from mode ML on `0001` or two moves from MJ on `001`. The return rules specify the new contents of both tapes. In particular, right prefixes `111` and `11010` at normalized A force another safe turn on every finite right tape and every left tape. [Rightward rules](Line429RightSweep.v) · [Leftward first return](Line429LeftLanguage.v) · [Output on both tapes](Line429LeftOutput.v) · [Composition](Line429Round.v) · [Landmark equivalence](Line429Criterion.v)

## What a blank-tape invariant must preserve

Take the left word of the real checkpoint at step 107 and the right word of the real checkpoint at step 39. Their combination halts after exactly 107 further moves. These words and clocks are in the normalized machine; reflection and renaming preserve the instruction count. At the start, even this hybrid passes safely through the next sweep. At move 39 its left test returns `Stop` while its right test stays closed. The two tests then coincide at move 93. [Reachable sources, two intermediate checkpoints and halt](Line429GateSplice.v)

| Configuration | Left word u | Right word w | Left stops | Right opens |
|---|---|---|---|---|
| Crossed halves, move 0 | `01101101` | `1111001001` | No | No |
| After 39 moves | `001101101` | `011100101` | Yes | No |
| After 93 moves | `1010001101101` | `0011001001` | Yes | Yes |

Consequently, one cannot prove blank-tape safety by allowing an arbitrary combination of separately reachable left and right words. Keeping both test results also permits a counterexample. The checkpoints at 39 and 13,671 both have left outcome Turn and a closed right gate. Combining the latter left with the former right keeps both test results and still halts 107 moves later. [Matching-gate obstruction](Line429MatchingGates.v) Even a shared six-cell window in the original state C admits a concrete halting splice. The original E phase has a separate 17-step example. [Six-cell obstruction](Line429Splice.v) · [Original E obstruction](Line429SweepSplice.v)

The 92-move halt in the six-cell splice belongs to an infinite family. In the original orientation, put the eight bits `01001010` immediately left of C in left-to-right order and let C scan `00101(1010)^n01`, n ≥ 1. The machine halts in exactly 5n² + 9n + 54 moves, regardless of the tape outside that word. Separately, eight explicit configuration-word prefixes are pairwise distinguishable by attaching a common suffix that gives a real blank configuration for one prefix and a halting continuation for the other. This gives a lower bound of eight states for any whole-tape DFA separator using the specified left-to-right encoding. [Parametric halt](Line429SpliceFamily.v) · [28 distinguishing suffixes and replay](verify_regular.py)

## Where the blank run goes

A literal simulation checked the first **10,000,000,000 configurations** of the reflected blank run, starting at time zero. It included every normalized A with left prefix `0` and scanned bit `1`, including occurrences inside a sweep. Each was classified by the two tests.

| Left result | Right closed | Right open |
|---|---:|---:|
| Turn | 325,061,613 | 674,874,396 |
| Stop | 0 | 0 |

For the first 1,048,576 elementary configurations, Rocq independently certifies that every shaped A has left outcome Turn. The check includes configurations where a closed right gate would mask a left Stop. [Kernel-checked prefix](Line429ShapePrefix.v)

The 999,936,009 observations suggest the stronger blank-orbit conjecture that the left test always returns `Turn`. The crossed-tape example shows that preserving this conjecture across later sweeps requires information from both tapes. With just one nonblank initial cell at normalized offset −6, the left test returns `Stop` at step 4 and the right test stays closed. Both are positive at step 16, and the altered tape halts at step 38. [Literal replay](sweep_gates.cpp) · [Checked one-mark control](Line429Control.v)

A separate replay followed every full sweep round starting before move 1,000,000,000. Of 70,684 true returns, 50,574 opened the right test and 20,110 closed it. All returned `Turn` on the left. On the original blank run there were 175 visits to B scanning `00` in the same prefix. In 32 visits the head stood at the rightmost previously visited cell and in 143 it stood one cell farther right. Each time the whole right suffix was blank. These are finite measurements. [Full-round replay](canonical_rounds.cpp) · [Right-edge replay](frontier_visits.cpp)

At the previously certified sibling-divergence checkpoint, 72,013 accelerator calls from blank, Rocq now reads the 22-cell word `0111011011010101010111` under original B. It proves that the head returns left in E after 95 moves, crosses a run of 1,227 ones and, after 1,334 moves in total, reaches C 1,230 cells left of the starting head with a zero immediately to its right. There is also a uniform theorem for all mixtures of the tokens `01` and `011` in this part of the tape. [Reachable recovery and parametric rules](Line429Recovery.v)

The separate native accelerator passed 116,000,000 successful calls. At that checkpoint the tape had a 3,320-digit number of ones, whose SHA-256 in decimal ASCII without a trailing newline is `21ad6cd956c0537ec08270be5062221154ae03077f61cb2e90020c2da9db6a6e`. The native count is separate from the existing kernel-certified lower bound of 10^581 elementary steps. For the first 1,048,580 native input checkpoints Rocq proves that index 3 alone has normalized raw D facing left and reading zero. The progress-guaranteed watcher detects exactly the dangerous case in which the following symbol is one. [Native predecessor](Line429Escape.v) · [Complete watcher](Line429Watch.v) · [Checked finite audit](Line429Prefix20.v)

## A search for a nonhalting invariant

I tried retaining one half-tape as an exact stack and summarizing the other by a deterministic binary automaton. The checker propagates possible paths to the halting state backwards. It enumerates accessible automata up to state renaming with the initial state fixed under a blank. Every candidate of one through seven states in both orientations still admitted an abstract halt. This covered 24,490,331 transition tables per orientation. It leaves open more expressive invariants, including ones defined only at sweep returns. [Enumeration and saturation algorithm](line429_far.cpp)

## Reproduce

Run the existing [verification script](verify.sh) with the two pinned BusyCoq checkouts described in the [build instructions](README.md#reproduce). In an already built checkout, compile the new units in the order given in the script. Its standalone C++ diagnostics use C++17.

```sh
c++ -O3 -std=c++17 sweep_gates.cpp -o sweep_gates
./sweep_gates 10000000000
./sweep_gates 1000 -6
c++ -O3 -std=c++17 canonical_rounds.cpp -o canonical_rounds
./canonical_rounds 1000000000
c++ -O3 -std=c++17 frontier_visits.cpp -o frontier_visits
./frontier_visits 1000000000
c++ -O3 -std=c++17 line429_far.cpp -o line429_far
for n in 1 2 3 4 5 6 7; do
    ./line429_far "$n" 0
    ./line429_far "$n" 1
done
python3 verify_regular.py
```
