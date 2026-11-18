# Remaining machines: baseline and additional exact tests

The earlier report started at `2ab106f706cb1715d494c7f67464e9222092058f`. The 2026-11-18 update at `01b0a10592b3bf843c0fd5bb1718625c65632830` incorporates the line 26 floor, the line 35 guard reduction, the Rocq proof for line 36 and the owner's report for line 37. This report covers lines 1, 2, 6, 8–12, 14–16, 18–20, 23–28 and 31–37. [Original table](../SIMULATION_TABLE.md) · [Hydra-family report](hydra.md)

The current repository establishes nonhalting on line 36. For many other machines the only exact halt test is still the literal missing instruction. The [outlook table](../HALTING_OUTLOOK.md) gives current classifications and separates survival bounds from stopping predictions.

## Evidence and sources

**Inherited repository mathematics:** [research log](../research-log.md), [earlier frontier analysis](../frontier-background.md), [mixed/sweep analysis](../mixed-and-sweeps.md), [line-6 recurrence](../line6.md), [line-26 fixed-point reduction](../column-frontier.md), and the specialized sweep notes linked below. These are written arguments and tested code, not kernel-verified results. The raw floors and exact endpoint files are inherited from [SIMULATION_TABLE.md](../SIMULATION_TABLE.md); this report does not silently promote reported external runs into checked local endpoints.

**Current community check:** the [BB(2,5) holdout page](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved) was inspected on 2026-11-18 and matched by complete transition strings. It still lists these machines as open. It identifies bouncer/counter, spaghetti, longitudinal, and cellular-automaton families, and describes line 26 as likely nonhalting. Several original Discord links provide only an inaccessible JavaScript shell. Their detailed arguments were not reviewed; [the source audit](sources-audit.md) records this limitation and the individual URLs. Family names below are source descriptions, not decisions.

**Experiments inherited from the earlier outlook:** exact fresh-cell descriptions for lines 8, 11, 12 and 31, a finite-state/exhaustive/literal audit of those descriptions, literal samples of their actual fresh-cell histories, and a 2,000-epoch structural sample of line 6. No new accelerator is introduced: these experiments compose the inherited exact one-cell return contract and timed word recurrence. The new compositions are independently checked as described below.

## Fresh-cell conditions

For a nonnegative tape cell, list states of entry **from its left**, beginning with its first visit. A prefix condition concerns these entries, not the sequence of states at arbitrary raw steps. The initial visit at coordinate 0 is A. A and B here are control states. Each subordinate call finishes at its first exit left.

| Line | Exact halting prefix at a fresh cell | Why later ordinary inputs are safe locally |
|---:|---|---|
| 8 | `BB` | After safe initialization the cell/neighbor state stays in a closed set. |
| 11 | `B A^(3k+2) B`, integer k≥0 | Before the neighbor is first visited, A cycles symbols 2→4→1→2; the first B is fatal only on 1. |
| 12 | `BA` | Initial B leaves 1 and an unvisited neighbor; A sends B into it, whose B return reaches B4. |
| 31 | `BA` | Initial B leaves 2; the immediately following A is the undefined A2. |

These are exact reachable-instruction descriptions, **not** assertions that blank execution will supply such a prefix. For line 12 this is a *one-cell* prefix test; the inherited `AA` condition uses a *fresh three-cell block*. They are different cuts and do not conflict.

The inherited `Driver` computes literal virgin-suffix returns and checks closure of all reachable one-cell control states. For lines 8, 11 and 12, a virgin A call returns A and a virgin B call returns B; all subsequent completed calls return A. For line 31 these returns are respectively B, A, and B. A cell must remember both its symbol and whether its right neighbor is still virgin. Forgetting the latter would erase the only dangerous branches.

The simple reductions follow by exhausting this small state space. On line 8, initial B leaves `(2, virgin)`, and its next B halts; its next A initializes the neighbor safely. Initial A also initializes safely. On line 11 initial B leaves `(2, virgin)` and an A cycles the three virgin-neighbor states. A B on symbol 2 or 4 initializes safely; B on 1 is fatal after its child returns B. Hence the residue 2 modulo 3 in the exponent. On line 12 the only dangerous transient is `(1, virgin)` after initial B; a second B instead leaves `(2, virgin)`, from which either entry initializes safely. On line 31 B leaves `(2, virgin)`; A halts there, while subsequent B entries move through symbols 3,4,1 before safe initialization. Exhaustion of the remaining states gives no undefined branch. An internal halt in a child is a halt at that child's corresponding fresh-cell trigger, so this reasoning does not hide deeper halts.

**Verification:** [remaining-stream-triggers.py](remaining-stream-triggers.py) checks every input history of lengths 1–8: 510 per line. The extracted cell criterion agrees with its formula for all 2,040 histories. It also runs the complete finite request networks against the literal TM. For the 1,283 safe histories it compares the entire sparse tape, head, final control state and raw-step count. For 757 halting histories it compares halting status; it deliberately does not certify a halted configuration by composing speculative future returns. Every child is followed chronologically by the independent literal run. No skipped safe branch can hide a halt: every local transition is executed in the control-state calculation, and any undefined transition terminates that calculation.

**Actual blank samples:** an independent literal interpreter ran 1,000,000 raw instructions on each of the four machines. It recorded rightward first-entry times and up to 30 initial entry states at each visited nonnegative cell. It visited 34, 30, 65, and 24 such cells, respectively. The [saved results](remaining-stream-triggers.json) contain those histories, configuration hashes and all verification counts. A cell whose prefix is not yet long enough to decide the test is censored, not counted as a safe completed opportunity. These small samples are below the inherited endpoints and do not improve their raw floors.

**Opportunities, reachability, correlations, timing:** each fresh cell creates one initialization opportunity; line 11 may wait many A entries before its first post-initial B. The finite-state transducer generates the *next* cell's entry stream from the current one, so adjacent cells are strongly coupled. A nominal one-quarter chance for `BB` or `BA`, or an independent uniform residue for line 11, has no justification. The actual samples demonstrate safe prefixes only. Arbitrary input witnesses show the mechanism can halt, but not that its blank source reaches the witness. Proving an invariant of the iterated *phased* streams, or locating a genuine bad prefix, is the next step.

For exact raw timing, if E calls enter coordinate 0 and S is the sum of calls over all nonnegative cells, the positive half executes `2S−E` instructions: every entry exits left once and every subordinate entry also requires a parent's rightward move. Add the exact negative-half cost from `Driver.left(E)`. The left drivers are `BBABA`, `BBBA`, `BBBABABAABABBA`, and `ABAAA` respectively. These formulas convert a *specified finite stream calculation* into raw steps. They provide no spacing law for future fresh-cell opportunities, so no conditional median is reported.

Reproduce from the repository root (Python 3.10+; assertions enabled):

```sh
python3 research/bb2x5/halting-outlook/remaining-stream-triggers.py
python3 research/bb2x5/halting-outlook/remaining-line6.py --epochs 2000 --literal-epochs 376
```

## Line 6 sample from the earlier outlook

[remaining-line6.py](remaining-line6.py) iterates the inherited exact `probe` recurrence while removing persistent copies of `H=322323300`. It saves the entire residual, head, state, raw clock, a hash of the full word, header events, and regular samples in [remaining-line6.json](remaining-line6.json). Its first 376 blank checkpoints match the independent literal interpreter's **complete configurations and raw clocks**. The final residual's next complete B probe also matches literal execution, including residual and 777 raw instructions. The recurrence handles an internal halt immediately; its pre-existing totality proof applies to every finite residual.

At epoch 2,000 the machine is at head −2,000 in A after **144,834,636** raw steps, with a 7,986-cell stored word and **21** leading H copies. New header acquisitions after the inherited third occur at epochs 667, 737, 815, 972, 1012, 1051, 1252, 1325, 1332, 1472, 1498, 1565, 1602, 1705, 1829, 1858, 1936 and 1984. This is a structural sample, not an extension beyond the existing 10^10-step endpoint.

The opportunity is a completed left-extension probe. It halts either internally or if the probe replies A to the waiting guard 1. Totality means each such opportunity is reached in finite time unless an earlier halt occurs. Exact epoch cost is `2 + probe_cost(residual) + 48 × header_count`; observed costs through this sample range from 3 to 6,460,259. A persistent H prefix increases cost, but does not shield the residual: the inherited family `H^k3` halts in `31k+6` steps from the fresh A0 checkpoint for every k. Thus accumulating protected headers is not itself a nonhalting invariant, nor is increasing runtime evidence for halting. The specific residual sequence from blank remains the obstacle. No distribution of those residuals, constant hazard, or independence model is proposed. Next: characterize which residuals can occur after stripping all H copies and whether they exclude the inherited exact failure tests.

## Per-machine baseline

In the entries below, “floor” is survival in raw instructions, never a stopping-time estimate. Except where explicitly stated otherwise, the floor is the inherited exact endpoint linked from the unchanged simulation table. Physical halting entries are read directly from the full machine string.

### Line 1

`1RB---4LB1RA4RA_2LB2LA3RA4LB0RB`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

The current community source links Andrew Ducharme/mxdys analysis. The local repository has no complete reduced criterion for this variant. The only halt is A1. Unlike line 2, A3 writes 1 and moves right; the line-2 fixed-cut proof cannot be transferred unchanged.

**Next concrete step:** Derive a normalized return protocol for this exact A3 variant and test its exceptional A return.

### Line 2

`1RB---4LB0LA4RA_2LB2LA3RA4LB0RB`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

The inherited fixed cut receives B,A,A (with one permitted retry),B per three left extensions. Its negative prefix is (242) repeated; 2,400 extensions were matched literally. An A response on selected requests forces A1, sometimes after one diagnostic suffix request. The allowed family contains the B→A witness 24244442, but nested-call constraints prevent treating its existence as blank reachability.

**Next concrete step:** Track the actual nested-call history in the allowed-word construction; prove a stronger reachable-language invariant.

### Line 6

**Latest pass.** [Updated blank-run evidence and proof obligations](probe6.md). The earlier investigation follows.

`1RB---3LB4RB0LA_2LB3LA3RB4RA0RA`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

The inherited total word recurrence and its exact guard/internal halt conditions are described above. Every safe extension adds one 2, and the word avoids 02 and 222. These restrictions and persistent H headers do not exclude halting continuations. The new 2,000-epoch sample strengthens finite structural evidence only.

**Next concrete step:** Use the saved stripped residual and characterize its reachable language.

### Line 8

`1RB4LA1RA1RB1LA_2LB3LA---4RA2RB`

**Inherited floor:** ≈1.50000×10^57. **Outlook:** Unknown. **Estimated halting time:** none justified.

Inherited exact boundary simulation and BBABA left driver. The new complete local transient identifies fresh BB as the sole trigger, producing B2. The closed ordinary cell states do not constrain the first two inputs selected by upstream cells.

**Next concrete step:** Advance the exact phased fresh-cell stream and seek an invariant excluding BB, or a genuinely reached BB.

### Line 9

`1RB---4RB2RB4LA_2LB3LA3LB0RA0RB`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Community labels this bouncer plus chaotic counter. The inherited pair inspection gives rightward 22→00, 23→40, 33→20 in A; 32 reverses in B and the blank boundary has a separate return. The full interaction controlling A1 is unresolved.

**Next concrete step:** Close the return/boundary cases around these aligned pair rules before applying an arithmetic model.

### Line 10

`1RB2RB3LA4LA1LA_2LB3RA---4RA1RB`

**Inherited floor:** ≈2.10250×10^22. **Outlook:** Unknown. **Estimated halting time:** none justified.

The inherited initialized right edge halts if AAA precedes its first B. This edge already contains 3, so its input convention differs from a virgin cell. Period lengths obey L(x+2)=2L(x+1)+2L(x); AAA occurs in period words, including 19,024 cyclic starting positions at cut 15, but the actual distinguished phase avoids them in the saved run.

**Next concrete step:** Track the phase map at successive fresh edges; a uniform random phase is not established.

### Line 11

`1RB2LA4LA1RA1LA_2LB3RB4RB---2RA`

**Inherited floor:** ≈2.81543×10^50. **Outlook:** Unknown. **Estimated halting time:** none justified.

Inherited BBBA driver and exact boundary simulation. The new fresh-input test B A^(3k+2) B exposes a precise residue obstruction: the number of A entries before the next B matters modulo 3, and upstream transitions generate that number.

**Next concrete step:** Determine the residue of the actual virgin-neighbor waiting run, including its dependence on earlier cells.

### Line 12

`1RB4RB4RA1LA3LA_1LB2LA3RB2RB---`

**Inherited floor:** ≈2.67029×10^82. **Outlook:** Unknown. **Estimated halting time:** none justified.

Inherited three-cell driver has a periodic fixed word and a fresh-block AA trigger. The new equivalent one-cell view gives fresh BA. Every finite prefix of the favorable block-periodic word has a halting extension under free inputs; actual source correlations must carry any proof.

**Next concrete step:** Control the actual infinite source tail, not only longer agreement with the fixed period.

### Line 14

`1RB2RA4LA1RB4RB_1LB2LA3RA---0LB`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only B3 is undefined. The current community page reports survival to at least 5×10^13, not locally reconstructed here. No complete macro argument or substantive eventual-halting heuristic was located in the reviewed repository.

**Next concrete step:** Extract recurring configurations from the full moving-window checkpoint and certify their return rules.

### Line 15

`1RB3RB1LA2LA3RA_1LB2RA4RB0LA---`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only B4 is undefined. An inherited blank-left response certificate has prefix BBBA and period BABAABBABBABAAAB; the unresolved right-side response compatibility prevents using it as an unconditional full simulator. The external page reports ≥2×10^13 steps separately.

**Next concrete step:** Establish a right-block return contract or locate the concrete incompatible-return branches.

### Line 16

`1RB2LA0RB0LB3LB_2LA4RB3RA0RA---`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only B4 is undefined. The current page links Peacemaker II analysis; the linked original was not readable. No accessible complete reduction or halting probability model was verified for this exact string.

**Next concrete step:** Extract a finite-state return representation from the saved actual tape before extrapolating a counter pattern.

### Line 18

`1RB2RA3LB4LA---_2LA0RB1LA2RB0RA`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only A4 is undefined. The community page links dyuan01/Legion analysis, but its original details were inaccessible. The local moving-window result supplies an exact finite configuration, not an all-time invariant.

**Next concrete step:** Identify the event that returns A onto 4 and constrain its context in the actual checkpoint.

### Line 19

`1RB2RA3LA---2LB_2LA4RA4RB0RB0LA`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only A3 is undefined; the community describes spaghetti dynamics and reports ≥4×10^13 raw steps externally. That report is not treated as a locally verified floor. No completed blank-orbit reduction was found here.

**Next concrete step:** Study repeated local returns around A3 using the complete saved tape; preserve causal entry order.

### Line 20

`1RB2RA3LA4LA2RB_2LA---3LB1RA3RA`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only B1 is undefined. Its inherited restricted left driver has prefix BAAAB then period ABA. A second B on a fresh cell may exit left in B instead of halting, invalidating an assumed A-return stream model. This is a concrete obstruction to transferring the line-21/22 method.

**Next concrete step:** Add the unexpected-return branch to the boundary state, then test closure.

### Line 23

`1RB3LA3LB0RB0LA_2LA4RB1LB1RA---`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only B4 is undefined. The community calls it a permutation of a spaghetti machine; this report has not checked a conjugacy or imported a decision from another encoding. The exact finite endpoint is the local evidence.

**Next concrete step:** Write and verify the permutation, then transfer only results whose initial configurations also correspond.

### Line 24

`1RB3LA1LA2RB2RA_2LA4RA3LB1RA---`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only B4 is undefined. The community links longitudinal analysis by dyuan, but no accessible complete halting criterion is established here.

**Next concrete step:** Derive exact left responses and right return contracts for this full string.

### Line 25

`1RB2LB3LA0RA1LB_2LA4RA3RB3LA---`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only B4 is undefined. A community analysis link exists, but no accessible substantive probabilistic model or complete blank-orbit invariant was reviewed.

**Next concrete step:** Extract and verify a repeated macro configuration around the prospective B4 event.

### Line 26

`1RB2RB4LA2RA1LA_2LA4RA3LA---3RA`

**Inherited floor:** 377,503,392,604,154,203,337,765 defined steps. **Outlook:** Unknown. **Estimated halting time:** none justified.

At cut 84 the first dangerous carry follows 173 wraps. The plateau lemma extends the fixed-point exclusion through width 173. Permuting a genuine checkpoint can produce a halting artificial word, which constrains proofs based on digit counts alone. [Current bound](../column-phases.md#extension-through-cut-84) · [Halting permutations](../column-traps.md)

The inherited exact model has source (aadd) repeated and halts iff a cycle ends with e≥2^m. Equivalently, monotone p iteration from 0 reaches a fixed point. Iterates are 0→2→3→5→9→12→18→34→71→142, excluding fixed points below 142. The community likely-nonhalting label is recorded as attribution, not adopted without its substantive original argument.

**Next concrete step:** Prove p(j)>j at all sufficiently large j, or certify the next fixed-point iterate. A finite trend alone is insufficient.

For line 26, both the dangerous counter e and width m are unbounded in the **total arithmetic overmodel**, but this does not order their growth or show the actual tape survives. Between width increases V=E+U² cannot increase; the safety inequality fails as a universal invariant already at cycle six. Replacing aadd by adad causes an overflow at its fourth token, demonstrating that token order matters. The periodic counts (3s,3s,s) do not justify independent carries. Every trip traverses finite pairs with explicit finite raw traces; no distribution of times to a dangerous first arrival has been established. These are reasons for retaining Unknown despite the external likely-nonhalting description.

### Line 27

`1RB3LB---4LA1RB_2LA4LA4LB3RB1RA`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only A2 is undefined. The community labels this a potential cryptid and links mxdys analysis. No general recurrence sufficient to decide blank reachability was available in the reviewed repository.

**Next concrete step:** Recover the linked arithmetic interpretation, match the full string, and certify its blank initialization.

### Line 28

`1RB3LB4LA0LB---_2LA0LA1RB0RA3RA`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only A4 is undefined. The community links Peacemaker II analysis; the original was inaccessible. The saved exact tape provides the current reproducible baseline.

**Next concrete step:** Find a return description preserving the context of the A4 candidate.

### Line 31

**Latest pass.** [Updated blank-run evidence and proof obligations](edge31.md). The earlier investigation follows.

`1RB3RB---4RA2RA_2LA2RA3LB4LB1LB`

**Inherited floor:** ≈5.00000×10^27. **Outlook:** Unknown. **Estimated halting time:** none justified.

Inherited ABAAA driver on two-cell negative blocks and exact boundary simulation. The new positive-cell transient makes fresh BA the precise A2 trigger. Ordinary repeated calls are safe locally after initialization; the actual generated initial phase is unresolved.

**Next concrete step:** Track whether the actual next cell receives BA, including dependence on its predecessor's virgin-neighbor state.

### Line 32

`1RB3RB1LB2RA---_2LA2RB1LA4LB0RA`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only A4 is undefined. The community links Legion/dyuan analysis, but the original details were inaccessible. There is no reviewed all-time invariant or quantitative halting model.

**Next concrete step:** Extract a finite-state local return description from the saved checkpoint and test every exceptional branch.

### Line 33

**Latest pass.** [Updated blank-run evidence and proof obligations](neglected33.md). The earlier investigation follows.

`1RB2LA0RB4LB1RA_1LA3RA1RA---0LA`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

Only B3 is undefined. The community calls this a shift-overflow mixed-digit counter. That structural label does not establish the digit rules, timing, or which reset is blank-reachable for this machine.

**Next concrete step:** Derive and literally verify the exact reset map before predicting overflow outcomes.

### Line 34

**Latest pass.** [Updated blank-run evidence and proof obligations](target34.md). The earlier investigation follows.

`1RB2LA4RA1LA3LA_0LA2RB3RB2LB---`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

The inherited matching sweep treats 1 as opening, 3 as closing, 2 as neutral. A sweep halts on six excess closings; the return uses a ternary digit transform. Every finite sweep is exact, but future guard survival on the growing blank word is unresolved.

**Next concrete step:** Find a boundary-sensitive invariant for the actual sweep words; arbitrary safe seeds are insufficient.

### Line 35

`1RB2LA4RA1LA3LA_0LA3RB3LB2RB---`

**Inherited floor:** 10^10. **Outlook:** Unknown. **Estimated halting time:** none justified.

The inherited matching sweep treats 1 as opening, 2 as closing, 3 as neutral. Six excess closings reaches B4. The ternary return differs from line 34; no all-time guard bound has been proved.

The rightmost triples join a Pascal-mod-2 recurrence after a computably bounded number of successful sweeps. At the left, the transition graph on eight-cell prefixes from the actual seed has 71 states when incoming debt is bounded by four. Each of its 355 state/debt pairs completes safely. A true halt therefore requires incoming debt at least five at some epoch. A graph path using that fifth unit is an overapproximation until its exterior is shown reachable. Bound the middle word's debt as the right triples grow. [Derivation, tests and source](../line35-pascal.md)

### Line 36

`1RB2LA1LA4RA2LA_0LA3RB3LB2RB---`

**Proven nonhalting from blank.** Every raw-step floor is exceeded. The theorem `line36_nonhalting : ~ halts line36 c0` is for this literal machine. From the 612,729-step blank checkpoint a six-phase tiled prefix and a finite right-edge potential maintain a reserve of openings. Each real sweep stays below the six-unmatched-closing threshold, completes in positive finite time and restores the invariant. Induction supplies an infinite execution.

The repository supplies a Rocq formalization, a Coq 8.20.1 rebuild and a standalone `coqchk` replay command. Its reported assumptions are built-in integer and array primitives, with no admitted lemmas or user-defined axioms. This pass inspected the theorem, its machine definition and the replay documentation. [Proof](../line36-nonhalting.md) · [Formal verification and commands](../line36-rocq.md)

### Line 37

`1RB2LA3LA4RA1LA_0LA3LB3RB1RB---`

**Reported outcome.** The project owner reports a completed blank-tape nonhalting proof and asks that work move to a different machine. A proof artifact identifying the argument and its formal status has not been located for this exact string. The outlook label describes the reviewable evidence. This machine is excluded from targeting.

**Established in the available sources.** A sweep halts at two unmatched closings. The finite graph proves that an all-time bound of four on the debt after 45 digits implies nonhalting. The maximum observed over 200,000 sweeps was two. The first 199,999 traversals establish the raw floor 39,999,600,001. On continued survival every fixed right suffix eventually obeys a Pascal-mod-2 recurrence. The published fixed-cut proof leaves open whether the middle region can send enough debt on some later sweep. Attaching the author's completed argument or theorem for this string would allow the table to record its proof and formal status. [Fixed-cut argument](../line37-header.md) · [Merged PR](https://github.com/valu42/busycoqtesting/pull/4) · [Right-hand recurrence](../line37-pascal.md)
