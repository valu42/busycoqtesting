# BB(6) line 24 survives the predicted overflow

The blank run of ID **7846**, `1RB0LA_1RC---_0LD1RD_0RA0RE_0RF1RC_1LF0LA`, reaches a restart in state A after **4,679,860,003,204,851** defined elementary moves. Its eventual halting remains open. An October investigation singled out the event near 4.6 quadrillion moves as a possible halt or restart. The certificate below settles that particular event. [Earlier prediction and base-4 model](https://github.com/DennisKoshta/denniskoshta-portfolio/blob/b48bd32fab8b476135d47ffa4e5f9bfb9a80d8c7/public/busy-beaver/machines/1RB0LA_1RC---_0LD1RD_0RA0RE_0RF1RC_1LF0LA/decision.json)

| Defined moves from blank | Event |
|---:|---|
| 20,656,445 | State D starts a counter pass beside a wall of 82,430 ones. |
| 4,661,463,201,335,715 | After 6,132,267,261,786 complete passes, an empty digit reaches a wall of 18,396,801,867,788 ones. |
| 4,679,860,003,203,509 | The head finishes erasing that wall. |
| 4,679,860,003,204,851 | It also erases an older wall of 1,322 ones. The theorem `blankRestart` gives the full configuration. |

At the restart, read the left half nearest cell first. It is `111110110111` followed by blank tape. The right half, starting under the head, is 1,324 zeros, six ones, 18,396,801,867,785 zeros, four ones, and the suffix called `debris` in the proof. A separate literal C++ replay completed another **1,000,000,000** moves. Relative to the restart, it finished in F at cell 6,572,676 and reached no cell to the right of 6,572,731. It therefore never read the distant suffix. [Exact tapes and theorems](Checkpoint.lean) · [Literal replay](replay.cpp)

## Why the long calculation is checkable

Fractal Geometry Explorer proved the basic left and right sweeps, several complete passes and the blank-tape halting criterion. In its notation digit `k` means `1^(3k) 0`, and tail `Tj` means `1^$7+3j$` followed by blank tape. The study identified the case `2 0 1 Y` and collisions with the wall as gaps. [Prior proof and open cases](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/tree/89e8153595f1e90de26c9e963b24d98bb4f4547d/holdouts/1RB0LA_1RC---_0LD1RD_0RA0RE_0RF1RC_1LF0LA)

* If a sweep over suffix `Y` returns with suffix `Z`, then `2 0 1 Y` returns as `0 1 2 Z`. The head takes 28 moves to enter the suffix. It takes 36 more after the suffix returns to restore the left side. This rule holds for every surrounding left tape and composes at arbitrary nesting depth.
* A leading empty digit erases a wall of width $W \ge 1$ in $W+6$ moves. At the resulting A configuration, an older wall of width $m \ge 2$ behind separator `0 11 0` costs $m+20$ moves and leaves six ones as a marker. `eraseWalls` covers a list of any finite length.
* When the first two digits are `1 0` followed by a tail of $7+3j$ ones, the head reaches the first exterior cell in D after $26+3(j+4)$ moves. Exterior bits `001` then lead to the undefined instruction B1 in two further moves. This gives a halting family with an explicit tape hypothesis. [Wall rules](Wall.lean)

Each ordinary pass preserves the sum of the digits and tail index. It advances a signed integer by exactly one. For each digit separator, let $s$ be the total mass strictly to its right, including the tail. Add its weight $w_s$, where $w_0=1$ and $w_{s+1}=-1-2w_s$. The theorem `accounting` checks the sum on every pass rule, including a recursive carry. With no adjacent zero digits, there are at most $2M+1$ separators at mass $M$. The bounded sum rules out staying in this class of ordinary passes forever. At the two ends of the certified phase, the mass is 44 and the sums are 1,686,482,091,303 and 7,818,749,353,089. [Clock and phase bound](Counter.lean)

The Python generator reuses an entire sequence of suffix passes under a positive digit. Carrying a digit of size $k$ across a pass adds $14k+4$ elementary moves. The generated 2,257 Lean lemmas compose the timed rules and give **4,569,479,171,752,480** core moves. Each complete pass also spends 15 moves turning at the wall. These two counts give the first collision time in the table. Lean checks the generated proofs independently of the search that found them. [Timing rules](Timing.lean) · [Certificate generator](certificate.py)

## Verification and remaining question

The first 20,656,445 moves use Lean's compiled `decide +native` on the exact finite configuration. This part relies on Lean's native evaluator. The C++ interpreter checks the state, head coordinate and every cell of both half-tapes at that point. From that entry through the restart, the Lean kernel checks the timing and tapes with no native computation axiom. The checker prints the assumptions for the component theorems and their composition. [Blank-entry proof](Entry.lean)

A global decision still requires control of subsequent encounters with markers and older tape. The published criterion says that the run halts exactly when D scans `001`. The restart theorem gives a reachable tape for investigating that question. An unbounded nonhalting argument would have to show that every future restart avoids the critical word and continues making progress. [Existing halting criterion](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/89e8153595f1e90de26c9e963b24d98bb4f4547d/holdouts/1RB0LA_1RC---_0LD1RD_0RA0RE_0RF1RC_1LF0LA/lean/HaltIff.lean)

### Reproduce

Use Lean 4.34.0, Python 3 and a C++17 compiler. From this directory, with `lean` on PATH, run

```sh
git clone https://github.com/fractal-geometry-explorer/busy-beaver-explorer.git /tmp/bb6-line024-explorer
git -C /tmp/bb6-line024-explorer checkout 89e8153595f1e90de26c9e963b24d98bb4f4547d
./check.sh /tmp/bb6-line024-explorer
c++ -O3 -std=c++17 replay.cpp -o /tmp/bb6-line024-replay
/tmp/bb6-line024-replay
```

### Prior decision search, November 19, 2026

The repository register lists line 24 as open. I checked the claim board, the fork's branches and pull requests, upstream BusyCoq pull-request heads, DeepMind's Cryptids, Fractal Geometry Explorer, the community spreadsheet, indexed GitHub code and issues, and exact-table web and literature searches. The source scan of the four proof repositories included all state renamings fixing the initial state A, global tape reflection, and common halt spellings in encoded table strings and proof filenames. This covers public material that was accessible to the searches. Unpublished work and arbitrary semantic equivalences can escape such a search.

* Upstream PR 37 proves nonhalting for two related machines. Its near match writes **1** at D0. Line 24 writes **0** there. The blank run reads D0 as early as move 42. [Upstream proof](https://github.com/ccz181078/busycoq/pull/37)
* The community spreadsheet calls this a translated counter and has an empty decision field. Fractal Geometry Explorer lists the exact machine as open. The October prediction above explicitly parked the overflow question. [Community sheet](https://docs.google.com/spreadsheets/d/1mMp8bAcTFT91j7azn72liX8NSTwc2E_ozKnOGTfRCfw/edit#gid=1330361301&range=A834:F834)
* Harinaralasetty's investigation gives local transition and carry lemmas, hypothetical halting examples and a finite run of 6,307,258,355,399 moves. Enan Srivastava's dossier 59 proves a conditional nonhalting result assuming `SafeD59Orbit`, which the dossier leaves conjectural. Neither source reports a blank-tape decision. [Local lemmas and run](https://github.com/harinaralasetty/math-experiments/blob/7e4dc2a007909db77ee68c82b25dfc5f19110967/bb6/notes/024-attempt.txt) · [Dossier 59 and its hypothesis](https://github.com/Enan456/bbchallenge-proofs/blob/72965887b21cfc0310a90c93ec36b09d8b3ee8f6/packages/dossier1/palomar-meta/dossier59/formalization.yaml)
