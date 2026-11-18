# BB(6) research and the next machines to prove

On November 18, 2026 the local import of the October 30 list had 608 permanent lines. It marked 523 `OPEN`, 49 with proposed nonhalting proofs, 28 with proposed halting proofs, seven with simulation-reported halts, and one with a proposed equivalence. The open rows include a few machines for which a published proof still needs matching and replay here. Use the full transition string when comparing different lists. [Register](MACHINES.csv) · [Claim board](ROADMAP.md#claim-board) · [October list and tracking history][bb6]

## Proof queue

The first two rows are the shortest routes found to a verified local decision. For new mathematics, the order below favors machines whose missing case can already be exhibited on the real blank run. Only line 133 is claimed by this campaign.

| Order | October line / ID | Starting evidence | Next result to check |
|---:|---|---|---|
| 1 | **539 / 155900** | A published Coq file ends in a halting theorem for the exact blank machine. The author reports a full build in about 33 minutes. | Rebuild `H155900.v` with the evaluated run and check `Print Assumptions halt`. [Proof, build script and log][539] |
| 2 | **608 / 181655** | A second Coq file uses the same underlying simulator from another initial state and proves that a detour either preserves the simulated path or halts earlier. The author's full build took 6,573 seconds with concurrent jobs. | Rebuild `H181655.v`, check the detour theorem and the blank-start conclusion. [Proof, build script and log][608] |
| 3 | **133 / 35069**, claimed | A sound counter simulator for line 581 applies to a different blank seed here. A reachable exception now has a general recovery theorem. | Prove the carry beyond a run of all-one separator bits. The first test case in the checkpoint crosses a `11101` marker and expands eight bits to eleven. [Proof and replay](line133-odometer.md) |
| 4 | **33 / 9146** | Four whole-round branches are already proved in Lean. The blank run reaches counter 19,199 with tail `TD(15998)` at step 1,842,640,229. | Prove the observed transition to counter 28,802, then check whether its new tail belongs to a family closed under rounds. [Round theorems and next configuration][33] |
| 5 | **393 / 111043** | The author proved local sweeps over repeated words in Lean. A saved configuration has 453 blocks, with several kinds of separators. | Derive the first rule that propagates a change between successive large blocks and tracks whether D can read a one. [Sweep rules and checkpoint][393] |

The recorded build times help order the first two replays. They are the proof author's measurements. Both machines are still marked `OPEN` pending independent verification here. For an unstaffed machine beyond this shortlist, look first for a blank-start proof or witness tied to its full table, then a reusable sound simulator with a known missing branch. A reduction to an open arithmetic orbit is a longer-term project.

## What BB(6) research has established

- **Record setters.** Searches for long-running halters give lower bounds. In June 2025 mxdys found a six-state machine giving $S(6)>\Sigma(6)>10\uparrow\uparrow(10\uparrow\uparrow(10\uparrow\uparrow8))$. Here $S$ counts steps and $\Sigma$ counts ones at halt. The exact BB(6) value remains open. [Records and history][bb6]
- **Eliminating machines in bulk.** Enumeration, equivalence checking and automatic deciders shrink the set requiring individual proofs. Finite Automata Reduction can certify nonhalting by finding a regular language containing all eventually halting configurations and excluding the blank start. The October list groups 1,303 machines into 608 representatives. [List and decider results][bb6] · [Finite Automata Reduction][far]
- **Proving large jumps.** Researchers recognize repeated tape words, prove a symbolic rule on arbitrary repetition counts, then combine those rules to cross much larger runs. A 2026 preprint reports eleven BB(6) accelerations formally verified in Lean. Each reduces the blank run to an arithmetic system whose eventual behavior remains open in the paper. [Dos Santos et al.][ds]
- **Identifying the mathematical obstruction.** For Antihydra, start at 8 and iterate $x\mapsto x+\lfloor x/2\rfloor$. Halting is equivalent to some prefix containing more than twice as many odd terms as even terms. A proof for this specific orbit is required by any complete BB(6) result. [Ligocki's derivation][antihydra]

## What the BB(2,5) work contributes

This repository tracks a different list of 37 two-state, five-symbol machines. It has one verified blank-tape decision. Its line 36 runs forever. Two integer certificates bound the debt accumulated during sweeps, keep state B away from its undefined instruction on symbol 4, and guarantee that the next sweep can start. The proof includes a physical path from blank and positive elementary progress between checkpoints. [Blank-tape theorem](../bb2x5/line36-rocq.md) · [Independent kernel replay](../bb2x5/line36-kernel-replay.txt)

| Method in the repo | Concrete result and remaining question |
|---|---|
| Sweep invariants | On lines 34 and 35, a dangerous visit is expressed in terms of excess closings in a tape segment. The active campaigns seek bounds that hold at every future sweep from blank. [Decision board](../bb2x5/ROADMAP.md) |
| Arithmetic return maps | Line 4's first million returns imply more than $10^{1,719,137}$ defined steps. Line 26 halts exactly at a least fixed point. Its active campaign has excluded widths through 207. [Line 4](../bb2x5/line4-scalar.md) · [Line 26 campaign](https://github.com/valu42/busycoqtesting/pull/7) |
| Fresh-cell histories | Line 22 permanently clears cells 0 through 274. To halt at cell 275, the next three arrivals at cell 274 must all be A. The next question is whether its actual parent stream can send them. [Stream proof and replays](https://github.com/valu42/busycoqtesting/blob/afe22505b751e6d04d35e55d0d5127a8aaedf7e4/research/bb2x5/anchored-phase.md) |
| Literal and accelerated replays | The simulation table covers all 37 machines and records units, endpoints and evidence. Comparing both tape contents and clocks at a reachable checkpoint gives a concrete test for any proposed acceleration. [Simulation table](../bb2x5/SIMULATION_TABLE.md) |

For a BB(2,5) continuation, the roadmap prioritizes line 26's fixed-point argument, line 35's sweep guard and line 22's parent stream. The first two directions had active owners at the time of this review. Line 22's phase campaign had a published handoff. [Current claims and handoffs](../bb2x5/ROADMAP.md#claim-board)

[bb6]: https://wiki.bbchallenge.org/wiki/BB(6)
[far]: https://wiki.bbchallenge.org/wiki/Finite_Automata_Reduction
[ds]: https://arxiv.org/abs/2610.22603
[antihydra]: https://www.sligocki.com/2024/07/06/bb-6-2-is-hard.html
[539]: https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0LC_1RC1RA_1LD0RE_1LA1LD_0RA0RF_0LD---/coq/README.md
[608]: https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB1RA_1LC0RD_1LD1LB_1LE0LF_0RA---_0LB0LE/coq/README.md
[33]: https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0LF_1LC0RB_0LD1LA_0RA1LE_0LA0RA_1LA---/README.md
[393]: https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0RA_1RC0RF_1RD1LE_1RE---_1LF1LE_1RA0LE/README.md
