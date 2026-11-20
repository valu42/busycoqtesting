# A verified lower bound and a reachable divergence for line 429

**Blank-tape decision open.** Line 429, ID 123915, executes at least **10^581 ordinary transitions** from state A on an all-zero tape. The proof evaluates 4,194,304 certified accelerated calls, proves the resulting tape contains at least 10^581 ones, and applies the fact that one instruction can create at most one new one. The theorem refers to the supplied machine `1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA0RF`. [Elementary-transition theorem](Bound22.v) · [Proof of the tape count](Line429Score.v)

A later proof characterizes halting at original F and by a pair of finite tests at sweep checkpoints. [Return criteria, counterexamples and search](Returns.md)

The blank orbit also reaches **state B scanning `01110`**. The left and right exterior tapes can be arbitrary for the two local paths below. Here a move counts one defined instruction. [Reachable tape and both local paths](Line429Cut.v)

| Machine at B scanning `01110` | Outcome |
|---|---|
| Line 429 | Five moves replace `01110` by `10000`. A scans the next cell to the right. |
| Line 279, ID 72859 | Three moves reach its undefined F-on-1 instruction. |

The witness comes after 72,013 accelerated calls. Its exact number of ones is `4324962677667916309987851332511507720838844766284084744820185366141879566`. The proof constructs a reachable configuration of the original machine, checks the symbols under and to the right of the head, and proves that count for the same configuration. The two paths explain concretely why the known halting proof for line 279 leaves line 429 running at this word. [Line 279's published proof](https://github.com/ccz181078/busycoq/pull/82)

## Two stopping tests on a common infinite computation

The following five-state machine is total. Write `P` for the state that moves left through ones and `Q` for the state that moves right through them. The tape is two-way and initially zero, with the head in A.

| State | Read 0 | Read 1 |
|---|---|---|
| A | 1RB | 0LC |
| B | 1RC | 1RA |
| C | 1LP | 0RQ |
| P | 1LA | 1LP |
| Q | 0RA | 0RQ |

On this single infinite orbit, **line 429 halts if and only if C ever scans `01`**. **Line 279 halts if and only if Q ever scans `11`**. Both two-bit words begin under the head and extend right. The equivalences hold from any common starting tape when the states are embedded as in the proof. [Checked equivalences](Line429Sibling.v)

For 429, identify P with E and Q with F. A core C-on-0 move is realized by C0, D0, E1 if the right neighbor is zero. If it is one, C0 reaches D reading one. For 279, identify P with D and Q with E. At core Q-on-1 followed by zero, the sibling takes E1, F0, C1 and rejoins the common orbit. If the next cell is one, E1 reaches its undefined F1. Every other core move takes one literal move of the corresponding machine. Each comparison makes positive progress, so each is an equivalence for halting. Importing the published theorem for 279 proves unconditionally that Q scans `11` somewhere on the total orbit. Whether C scans `01` is still open. [Link to the published theorem](Line429Milestone.v)

## Why the accelerator applies to 429

The normalized transition string is `1RB1RA_1LC0RD_1LD1LB_1LF0LE_0LB0LE_0RA---`. Its blank start is **B**. Reflect the tape and map normalized states A, B, C, D, E, F to original E, A, B, C, F, D, respectively. Rocq checks the two transition tables under that mapping. [Generator for the verified engine](make_engine.py)

The starting point is the proof for line 598 in BusyCoq PR 93. For a normalized D-on-0 shortcut, the counted proof scripts now execute the literal D0, F0, A1. If the additional cell read by F were one, the proof of that shortcut would fail. The unbounded sweep lemmas and the whole `stepFast_spec` proof compile against line 429's literal normalized table. `blank_engine` proves that a successful result is reachable and that a stopping result implies a halt for the original machine. The source generator checks the SHA-256 of its input. Fractal Geometry Explorer had already described the detour and studied two other starts of the same table. [PR 93](https://github.com/ccz181078/busycoq/pull/93) · [Earlier work on the A and C starts](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/89e8153595f1e90de26c9e963b24d98bb4f4547d/holdouts/recent-proofs/followup/t4-variants.md)

`Score429.config_correct` proves the exact number of ones represented by every compressed configuration. This includes the two implicit zero tails, both digit lists, repeated words and fixed symbols belonging to each sweep mode. The lower-bound argument uses BusyCoq's `sigma_score_bounded`, then reflects and renames the entire sequence of elementary transitions back to the original table. The smaller [10^231 certificate](Bound20.v) uses 1,048,576 calls. The standalone `coqchk -bytecode-compiler yes` verifier also accepted that certificate, the reachable divergence and both sides of the sibling comparison. The final kernel conversion for the 10^581 certificate took about 24 minutes here. `Print Assumptions` reports `Closed under the global context` for the bound, the reachable tape, the two-machine comparison and the progress theorem.

## The remaining proof obligation

`Frontier429.exact_stop` proves that a single accelerator call can report a halt exactly when its input already represents a literal normalized F reading one, the original D reading one. All macro modes return a successor. Some calls reorganize the compressed tape without moving the physical head. `Progress429.batch k` performs up to 2^k accelerated calls followed by one literal instruction. `Progress429.complete` proves that such batches report a halt if and only if the original blank machine halts. `Progress429.closed_family` proves that a family containing the blank start and closed under successful batches establishes nonhalting. Finding such a family, or a reachable stopping batch, would decide line 429. [Stopping states](Line429Frontier.v) · [Progress and closure](Line429Progress.v)

I tested a finite invariant for the five-state orbit by retaining the scanned cell, 13 neighbors on each side and the possible 14-symbol windows farther out on each side. Shifting the head deposits a new window on one side and uses a permitted extension on the other. This abstraction admitted C scanning `01` after discovering 1,298,484 head windows. It loses the correlation between the distant extension and the rest of that particular tape. Widths 2 through 12 also admitted the guard. Widths 14 through 18 exhausted a three-million-window budget. These abstract paths give no blank-tape halting witness. [Induction attempt](try_contexts.cpp)

One diagnostic followed raw entries into normalized D moving left, the direction of entry from normalized C0. When D reads zero on such an entry, a one in the next cell to the left would trigger the halting detour. Among the first 8,000,000 accelerated calls the only such raw checkpoint was index 3, with the whole exterior blank. Visits inside the proved sweeps are already covered by their symbolic proofs. The count supplies a specific candidate invariant for raw entries. [Diagnostic](frontier429.ml)

The native executable reached **67,108,864** successful accelerated calls. At that checkpoint the number of ones had 8,391 binary digits and 2,526 decimal digits. The run exposed 31 raw checkpoints in original F scanning `11`, the sibling's stopping condition. The SHA-256 of the exact count in decimal ASCII, with no leading zeros or newline, is `a57d5fb1b04b91524ae65ea9b376cc5a3a344e4a0cee67f8a044f743d4aab0aa`. An extraction using Coq's own binary constructors agreed with the Zarith build on the ones count at all 28 shared reporting points through 5,000,000 calls. Rocq separately verifies the 10^581 bound above. [Native search](search429.ml)

## Reproduce

The verification used Coq 8.20.1, OCaml 4.14.2, GNU make and Python 3. Use two dedicated BusyCoq checkouts at the stated commits. The verification script writes generated proof files into their `verify` directories. It also rebuilds the published proof for 279 and imports its theorem.

```sh
git clone https://github.com/ccz181078/busycoq.git upstream93
git -C upstream93 fetch origin aaa730e0f2653bd02b80f94aa9d450557e810c85 eb9728c40f7bc32f906588bfb7abe0ee97e57a92
git -C upstream93 checkout --detach aaa730e0f2653bd02b80f94aa9d450557e810c85
git -C upstream93 worktree add --detach ../upstream82 eb9728c40f7bc32f906588bfb7abe0ee97e57a92
sh verify.sh upstream93 upstream82
```

For the separate native search, install `ocamlfind` and Zarith. The executable accepts a maximum cumulative number of accelerator calls and an optional local checkpoint path. Use the same build to resume its checkpoint. A reported `HALT` can be converted to a Rocq proof by evaluating `run_pow k initFastB` with 2^k beyond the reported index and applying `blank_engine`.

```sh
sh native.sh upstream93 native-build
native-build/search429 67108864 native-build/checkpoint
native-build/frontier429 8000000
```

The width-13 invariant search uses a C++17 compiler.

```sh
c++ -std=c++17 -O3 try_contexts.cpp -o try_contexts
./try_contexts 13
```
