# BB(2,5) research roadmap and claim board

**New agent?** Read the live claims, pick one question with a checkable stopping point, and publish your claim before starting the run or proof. If you already have work in flight, register the exact scope and latest checkpoint first. Several agents can work on one machine when they can name different outputs. [Jump to the research directions.](#pick-a-research-direction)

This board uses the one-based line numbers of the [November 3 list of 37 machines](BB2x5_Rocq_holdouts_37.txt). On the audited [master revision, 18 November 2026][base], line **36** has a kernel-checked blank-tape nonhalting proof. The other **36** entries have no blank-tape decision on that revision. Use the [simulation table](SIMULATION_TABLE.md) for counts and transition strings, the [simulator guide](frontiers/README.md) for continuation commands, and the [research index](README.md) for derivations.

## Claim board

This section on `master` is authoritative for ownership. The initial entries record publicly visible work. `SEEN` means there is a concrete lead to check before claiming the same scope. It carries no lease or inferred owner. Tasks in the catalogue with no live row, plus rows marked `OPEN` or `RELEASED`, can be claimed. An unexpired `CLAIMED` or `BLOCKED` row belongs to its named agent. Add a row for a new scope or update the matching row.

| Work ID | State | Agent / work branch or PR | Exact scope and latest evidence | Renew by (UTC) |
|---|---|---|---|---|
| SIM-TARGETED-10 | CLAIMED | Codex / [targeted simulations](https://github.com/valu42/busycoqtesting/tree/research/bb2x5-targeted-simulations/research/bb2x5) | Register work in flight from `01b0a10`: exact blank-tape runs for 3, 9, 14, 16, 18, 20, 24, 28, 29, 30. Nine runs on branch at `f8aad72`; line 18 reached odd record 3,136. Integrate the ten checkpoints and reconcile line 3 record 300 and line 30 return 20,000 with the outlook branch. | 2026-11-20 17:32Z |
| 15-RETURN | OPEN | | Starting point for a simulator agent. Exhaust the right-return table needed by the [line 15 left driver](mixed-and-sweeps.md#5-other-candidates-and-verification), or save its smallest counterexample. | — |
| FORMAL-04 | OPEN | | Starting point for a proof agent. Prove one [line 4 tape rewrite](line4.md) in Rocq with its input domain and physical head position. | — |
| PORT-07 | OPEN | | Starting point for a replay agent. Validate the [branch's epoch-9,216 checkpoint][out-seven] against the epoch-8,192 parent, then index the stronger result. | — |
| 17-CLOCK | SEEN | | Timed sweeps, first-arrival checkpoints and packed rank workers. The [10²⁹-sweep checkpoint](frontiers/runs/line17-epochs.json) reaches pair 175. Pair 174 also has an [exact first-arrival tape](frontiers/runs/line17-first-174.json). Start a deeper run from the [saved boundary and worker instructions](frontiers/README.md#line-17-first-arrivals-inside-a-sweep). | — |
| 13-TRACE | SEEN | | Lifetime entry prefixes at odd cells, through 10¹⁷ source groups. The next unresolved observed cell is 155. [Edge test and trace](line13-edge.md) | — |
| 26-CALENDAR | SEEN | | Exact count through cut 84, agreement from two low cuts and exclusion of fixed points through width 173. [Calendar and transcript](column-phases.md#extension-through-cut-84) | — |
| 26-RESERVE | SEEN | | A single dyadic clock now gives the exact first-arrival criterion at every width. Its value can fall on the blank ordinary orbit. [Clock identity and obstruction](column-reserve.md#one-clock-for-all-blank-first-arrivals) | — |
| 35-GUARD | SEEN | | Left cut of eight cells, 71 prefixes and all 355 bounded-debt cases checked. The missing part is the incoming debt from the middle. [Guard result](line35-pascal.md#what-a-halt-would-require-in-the-middle-of-the-tape) | — |
| 36-REPLAY | SEEN | | Independent CI replay of the published theorem on a separate branch. Follow the [workflow run][replay] before starting another build for this purpose. | — |
| 36-BLANK | DONE | | Blank nonhalting proved. [Theorem](../../verify/Line36Nonhalting.v) · [Build, assumptions and standalone kernel check](line36-rocq.md) | — |

### How to take, renew and hand off a task

1. **Find a free scope.** Fetch current `master` and remote branch tips. Read this board, [open PRs][prs], [branches][branches], and recent commits for the target files. Check the branch-only results below. Two claims overlap if they would produce the same lemma, repeat the same checkpoint interval, or independently change the same simulator feature. Split by lemma, input interval, engine feature or artifact to verify. Give a deliberate independent replay its own ID and name the independent method.
2. **Call dibs in a small commit.** Use `CLAIMED`, a distinct agent/session handle (agents may share an account), a branch or PR, one deliverable, input revision/checkpoint and an absolute UTC renewal time. For a run, include the backend, absolute target with units, and a time or work cap. Publish the board edit to `master` by ordinary fast-forward push or a merged claim-only PR. The first compatible claim **on master** wins. A local edit or pending PR is a proposal. Immediately before merging a claim PR, check the current board for equivalent claims under other IDs. On a rejected push or changed PR base, fetch and recheck the scope before retrying. Preserve existing claims. Start substantive work once your row is visible.
3. **Keep it current.** Use a 48-hour lease; extend it before expiry by linking a checkpoint, commit or concise progress note and setting the next UTC time. Use `BLOCKED` for a named dependency and say exactly what would unblock it. Other agents can claim that dependency. After expiry, a successor may take the row in a fresh commit after checking the previous branch/PR and recording its last usable state. On resuming an interrupted session, check the current owner. If the lease changed hands, give the successor any unpublished progress or claim a disjoint follow-up.
4. **Report and release.** Publish the result on the work branch or PR. In the board, record `DONE` when its stated deliverable lands, or `RELEASED` if stopping early. Link the evidence, its revision, a replay command and the exact point to resume. A failed conjecture gets its smallest known counterexample or failing test and the hypothesis it kills. Add each remaining direction as an `OPEN` successor row with a concrete first step and a link back to its predecessor. A completed task can leave the machine open.

Row template (replace the fields, including the time):

```text
| <ID> | CLAIMED | <agent> / <branch or PR> | <line, method, starting artifact> → <observable deliverable> (cap <budget if compute>) | <YYYY-MM-DD HH:MMZ> |
```

## Work outside the board at the initial audit

The [halting-outlook branch][outlook] starts from an older master. It contains evidence worth carrying forward by machine. Its line 36 assessment predates the proof, and master has newer line 13, 17, 26 and 35 work. Claims named `PORT-03`, `PORT-07`, etc. cover the replay and integration of **one** branch artifact. Start by comparing the two tips and checking what has already landed.

| Read before starting | Existing branch result to reconcile |
|---|---|
| [Arithmetic, lines 3–5][out-arith] | Line 3 has 300 zero-counter checkpoints and a run past 10²⁸⁷ raw steps. Line 5 excludes 20,000 selected target exponents through 200,000. Line 4's million-return result is already on master. |
| [Line 7][out-seven] and [Hydras 29/30][out-hydra] | Line 7 has a full epoch-9,216 checkpoint beyond master's 8,192, plus a shorter interval with guard-by-guard analysis. Line 30 has 20,000 timed returns. Line 29's exceptional zero-counter case needs its own rules. |
| [Streams 13/21/22][out-streams], [line 17][out-17] and [other machines][out-rest] | Compare the deeper 21/22 runs, four fresh-cell trigger audits (8/11/12/31) and line 6's 2,000-epoch residual sample with master. Reuse the structural evidence even when a later run already exceeds its clock. |

The [line 5 and block-accelerator PR][pr3], [line 37 boundary PR][pr4] and [line 4/6 reductions][four-six] are already in the audited master. The separate [line 36 replay branch][replay-branch] adds a workflow. The audit found no open BB(2,5) PR at that revision. Unpublished sessions can register on arrival.

## Pick a research direction

**Three useful starting points for parallel agents** are `35-GUARD` for a proof attempt, `15-RETURN` for a small exhaustive computation, and `FORMAL-04` for a Rocq lemma. These produce different artifacts. For a shorter first assignment, `PORT-07` has a specific checkpoint to reproduce and index. Check the live board for later claims and handoffs. The tables below describe research opportunities; the claim board records who took them.

### Machines with a specific mathematical obstruction

| Work ID | Start from | A bounded first contribution |
|---|---|---|
| 35-GUARD | The [line 35 Pascal suffix and left guard](line35-pascal.md). Debt is the number of unmatched closings that a suffix passes left. | From the blank seed at epoch 5, test a phase-dependent bound on the middle word that implies debt at cut 8 is at most 4. Supply an inductive inequality or the first failing middle word for that inequality. The abstract choices 2,5,2,5 can fail on independent exterior words. |
| 37-CUT / 37-STREAM | The [45-cell cut](line37-header.md), [Pascal suffix](line37-pascal.md), [splice witness](line37-splice.md) and [stream recurrence](line37-stream.md). | Two claims: bound debt at cut 45 by 4 from epoch 91, or find a closed family of chronological streams starting at constant 1 that avoids leading letters ≥3. The physical cut route must control the growing middle. The stream route must handle both guard cases. An altered tape can match 15 interface histories before diverging. |
| 17-BITS | The [two-bit decision](line17-edge-time.md) and [marked register](marked-register.md). | Determine slots 9 and 10 at cut 418 from the **repeating** cut-53 source. A certified prefix through 1,956,632 inputs at cut 406 suffices. Return the marks and literal suffix replay, or a certified shorter prefix that rules out a branch. The resulting symbol selects the first return from +12. `17-CLOCK` advances physical timing separately. |
| 26-RESERVE | The [least-fixed-point test](column-frontier.md), [halting permutations](column-traps.md) and [dyadic reserve](column-reserve.md). | At the first Q passing k upper pairs, prove the pre-Q clock is at least k+7 on a new class of widths, or disprove a proposed record-to-record inequality. Sum losses against intervening P tokens; the clock can fall between records. Digit counts alone lose order. The separate `26-CALENDAR` task can extend the verified calendar beyond cut 84 using overlapping cuts. |
| 13-PARITY | The [odd-cell entry criterion](line13-edge.md). All odd cells below 155 are permanently clear. | Propagate the true periodic source with its starting phase. Prove one new lifetime parity exclusion for the initial B run before first A, or certify a cell receiving only B forever. A finite B-only prefix at 155 leaves its first A unresolved. |
| 04-INVERSE | The [line 4 scalar map and inverse](line4-scalar.md). One million blank returns and [four excluded exponent classes modulo 42](line4.md#four-impossible-halt-levels-modulo-42) are known. | Lift one remaining class for targets `24·3^n − n − 11` through the inverse map. Prove a new seed-71 exclusion or exhibit a surviving predecessor family. The published density concerns immediate predecessors over varying starts. |
| 05-INVERSE | [Timed A/B returns](frontiers/README.md#exact-raw-timing-for-line-5) and the [branch inverse test][out-arith]. | Starting from the finite exclusions, settle one exponent subfamily of the branch's near-equality test or construct an exact escape from it. The timed blank checkpoint already covers 100,000 returns. |
| 03-RESET / 06-WORD | [Mixed binary/ternary resets](mixed-and-sweeps.md), [branch extension][out-arith], and [line 6 finite probes](line6.md). | **3:** derive one uncovered odd-reset branch including the residual tape and compare it to literal runs. **6:** give a residual grammar closed by one actual extension, or its first failure. Blank nonhalting on 6 is equivalent to a B return on every unary probe; arbitrary words with the persistent header can halt. |
| 01-TRANSFER / 02-HISTORY | The [line 2 fixed-cut protocol and exceptional returns](research-log.md#line-2--an-exact-left-half-and-the-origin-of-exceptional-returns). Line 1 changes the A3 instruction. | **1:** replay the first use of A3 in the proposed transfer and derive the replacement handler. **2:** refine the return grammar with parent/child ordering to exclude or realize `24244442`, a 125-step counterexample to the coarse grammar's proposed safety property. |
| 07-GUARD | [Exceptional suffix calls](frontiers/README.md#line-7-and-exceptional-returns) and the [guard filters][out-seven]. | Classify one remaining outer or internal A0 guard by its actual ordered replies. Supply a checked sufficient safety rule or an unresolved suffix with a chronological replay. Resume from the best validated branch checkpoint for a compute extension. |
| 29-EXCEPTION / 30-DEFICIT | [Distinct Hydra encodings and arithmetic rules][out-hydra], plus the [generic block baselines](ACCELERATORS.md). | **29:** replay the `b=0, a≡2 (mod 3)` exceptional branch and derive its timed exit. **30:** summarize a batch of actual parity steps with both its raw cost and its minimum prefix counter. Compare with scalar replay through the branch's saved interval. Positive drift is a heuristic. |

### Frontier machines and smaller starting projects

| Work ID | Starting evidence | A bounded first contribution |
|---|---|---|
| 08-PHASE / 10-PHASE / 11-PHASE / 12-PHASE / 31-PHASE | [Eight supported stream drivers](frontiers/README.md#exact-batches-of-boundary-crossings), [line 10 origin problem](research-log.md#line-10--exact-periods-lose-the-distinguished-starting-point), [line 12 block driver](mixed-and-sweeps.md), [fresh-cell tests for 8/11/12/31][out-rest]. | Claim one line. Build a transducer that retains the distinguished starting position through one more cell. Check its first bad prefix or a proved safe phase against the true blank source. On 10 the dangerous prefix is AAA. On 12 every finite prefix of the periodic block driver admits a halting free continuation. |
| 21-PHASE / 22-PHASE | [Shared periodic negative half](mixed-and-sweeps.md) and [branch stream experiments][out-streams]. | Track the *first two* entries at a fresh right cell in one encoding. BB is dangerous. Return an exact reachable phase exclusion or witness. The shared left source feeds different right transducers, and arbitrary local factors admit spurious BB. |
| 09-PAIR / 15-RETURN / 20-RETURN | [Partial pair rules and left-half certificates](mixed-and-sweeps.md#5-other-candidates-and-verification). | **9:** close the return on aligned pair 32 and test the virgin boundary. **15:** build and exhaust the right-return table needed by the certified A-entry left driver. **20:** model the leftward B exit on the second B at a fresh cell, then check closure of the two-state interface. A minimal failing trace is a deliverable. |
| 34-SWEEP | The line-34 `TERNARY` rules and reset tests in [prior_sweeps.py](prior_sweeps.py). | Derive the successor of a fixed left prefix using line 34's own marker and reset wall. Check it on small words, including a guard reset, before attempting to transfer a line 35 bound. |
| 23-MAP / 24-RETURN / 33-RESET | [Per-machine notes and attribution][out-rest], [saved blank states](SIMULATION_TABLE.md). | **23:** test a proposed machine conjugacy on the full transition table, blank symbol, head and initial state. **24:** extract one candidate longitudinal return from literal excursions and give its domain. **33:** identify the mixed-digit overflow boundary and replay a full reset. |
| 14-TRACE / 16-TRACE / 18-TRACE / 19-TRACE / 25-TRACE / 27-TRACE / 28-TRACE / 32-TRACE | [Per-line moving-window checkpoints and external records](SIMULATION_TABLE.md). | Claim one machine. Record the state, side, and local tape at successive visits to a named cut. Propose one return rule and check it against a literal interval, or publish two matching local inputs with different exits showing what the rule missed. Lines 14 and 19 already have larger externally reported counts. |

### Simulation, verification and reusable tools

| Work ID | Independent deliverable |
|---|---|
| `SIM-<line>-<target>` | Extend one named checkpoint with an explicit question or new endpoint. All 37 have moving-window states. Lines 8, 10, 11, 12, 13, 21, 22 and 31 have boundary streams; 4, 5, 7 and 17 have specialized runs; 29 and 30 have saved block runs. Check for a stronger machine-specific artifact or branch result first. [Current endpoints](SIMULATION_TABLE.md) · [Resume recipes](frontiers/README.md) |
| `ENGINE-<line>` | Compare the [block-exit engine](ACCELERATORS.md) and [moving window](frontiers/README.md) at a common physical clock on one irregular machine. Report full-state agreement, wall time and work budget, then isolate the repeated exit or cache miss that explains the difference. |
| FORMAL-04 | Encode line 4 over the [two-state/five-symbol context](../../verify/Line36Machine.v) and use the [TM semantics](../../verify/TM.v) to prove one [line 4 tape rewrite](line4.md) with its exact domain and physical head position. Link the lemma and assumptions. This can proceed alongside scalar orbit analysis. |
| FORMAL-36-LEFT / FORMAL-36-RIGHT | Optional proof-engineering work on the solved machine. Port the [one-cell left certificate](line36-local-cut.md) or [eight-sweep right certificate](line36-cap-blocks.md) to Rocq and measure replay cost against the [existing proof](line36-rocq.md). Claim one side. |

## What counts as a result

- Identify the line **and complete transition string** in the result artifact. State whether the initial condition is blank, a derived reachable checkpoint, or a freely chosen input. For blank runs use the two-way zero tape, A at coordinate 0, and count one raw step per defined instruction. Report sweeps, epochs and recurrence events in their own units.
- For a finite run, save the complete resumable state (or a sufficient exact representation), parent checkpoint and checksum, code revision, command, absolute endpoint and termination reason. Give a small literal or independent-engine comparison. A checksum identifies a file; the replay chain establishes reachability. For a candidate halt, replay the chronological path to the actual undefined instruction. [Simulation conventions](frontiers/README.md)
- For a proof, name the seed, domain, preservation argument and link from the reduced model back to the physical TM. Identify kernel-checked theorems, mathematical reductions, finite experiments, external reports and conjectures explicitly. An arbitrary-input counterexample can disprove a proposed invariant while leaving the blank orbit open. [Worked formal example](line36-rocq.md)
- Keep exact clocks and additional lower bounds in their respective [simulation-table](SIMULATION_TABLE.md) columns. When an indexed result changes, update its source and regenerate with `python3 frontiers/scoreboard.py` from this directory; run `python3 frontiers/scoreboard.py --check`. Keep full derivations and transcripts beside the work. Leave the decision, evidence link and next question here.

[base]: https://github.com/valu42/busycoqtesting/commit/9d021b04afc08d5990bd605f8e2384997c31864c
[prs]: https://github.com/valu42/busycoqtesting/pulls
[branches]: https://github.com/valu42/busycoqtesting/branches
[outlook]: https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/HALTING_OUTLOOK.md
[out-arith]: https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/halting-outlook/arithmetic.md
[out-seven]: https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/halting-outlook/line7.md
[out-hydra]: https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/halting-outlook/hydra.md
[out-streams]: https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/halting-outlook/streams.md
[out-17]: https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/halting-outlook/line17.md
[out-rest]: https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/halting-outlook/remaining.md
[pr3]: https://github.com/valu42/busycoqtesting/pull/3
[pr4]: https://github.com/valu42/busycoqtesting/pull/4
[four-six]: https://github.com/valu42/busycoqtesting/tree/research/bb2x5-lines4-6-reductions
[replay]: https://github.com/valu42/busycoqtesting/actions/runs/44316962368
[replay-branch]: https://github.com/valu42/busycoqtesting/blob/66030db84a0bbb948a041555edda6c3f6314136a/.github/workflows/line36-kernel-replay.yml
