# Packet streams for entries 405 and 482

**No blank-start halt or nonhalting proof has been found.** This applies the existing longitudinal packet method to two further supplied inputs, with independently learned finite rules, Coq checks, and a new streaming/window implementation.

| Supplied entry | Machine |
| --- | --- |
| 405 | `1RB0LB_0RC0LF_1LD1RE_0LA0RB_0RD0RF_0LA---` |
| 482 | `1RB0LB_0RC0LD_1LD1RE_0LA0RB_0RD1RF_1LA---` |

## Method and attribution

The longitudinal packet/cycle method comes from valu42's `PacketHalt274` work. [Upstream PR #39](https://github.com/ccz181078/busycoq/pull/39), pinned at `720c177d9ac0aa5cc35801a85337026e09f4b2b9`, demonstrates automatic packet learning for its own target in `PR_PacketHalt267.v`; that result is excluded from this branch's new-result claims. The finite oracle used here was cross-checked against all 507 laws in that source. Its source was not copied into this branch. These two targets and their small packet catalogues were learned independently.

For both targets the right-going interface is `(C,[0])`, and the returning interface is `(A,[0])`. A packet law replaces a finite word `u` by `v`, returning to the left after requiring `k` matching calls on its untouched right tail. The learner executes an ordinary finite tape, substitutes only the specified interface at an external call, and accepts only the matching left return. A halt found **after** an assumed external return is not accepted as an unconditional halting packet.

If repeated calls cycle through packet words, a large call count is divided by the finite cycle length. The sum of the cycle's external calls gives the next tail count. Both catalogues include

```text
1010 -> 1010, requiring two right-tail calls.
```

Here words are written nearest-cell first. Passing `n` calls through `m` copies of this packet requires `n*2^m` calls on the remaining tail. [ResearchPacketCoverage.v](../../verify/ResearchPacketCoverage.v) proves that statement for arbitrary natural `n,m`, using BusyCoq's existing `segRLs` composition theorems. This is a genuine exponential call-count compression, but the method is credited to the existing packet work. It is not a new exponential speedup over previous packet evaluators, nor a certified runtime bound for a native checkpoint.

## Boundaries and streaming representation

At a complete boundary the machine is in A on a 1, its entire left side is blank, the next cell is 0, and the finite right word is `w`. The blank start reaches `w=1` in four ordinary steps. Entering the next boundary round prepends `10` to `w` and starts one right-going call. These two bridges are checked in Coq.

[packet_stream.cpp](packet_stream.cpp) stores both the tape word and the remaining call count using [sliding_bits.hpp](sliding_bits.hpp), factored from the SOC25 implementation without changing its arithmetic. It rewrites a consumed packet in place and advances a cursor. Power-of-two cycle lengths and multipliers become shifts of the call count. There is no recursive packet stack and no mandatory full-integer shift for every packet.

The catalogue is deliberately finite. An unrecognized packet reports `unknown_packet`. A right-going `111` packet reports `halt_candidate`, justified by a separate Coq local-halting lemma, but a native occurrence still needs replay from blank. Artificial boundary words `0x1d` and `0x19` exercise this detector; neither is claimed reachable from blank. The latter also has a direct Coq halting proof. An unconditional one-call rule `0 -> 1`, with no tail calls, handles transient prefixes that have no finite packet cycle. The evaluator decrements the outstanding call count and rechecks the updated word, so a transient path into a halting packet is not missed.

The simulator preserves the last **complete** boundary. If time, space, an unknown packet, or a halt candidate interrupts a round, the partial rewrite is discarded before saving. Checkpoints contain the machine identity, completed rounds, logical packet-event count, and complete hexadecimal tape. A format-valid checkpoint is not a reachability certificate.

## New composed windows

The second acceleration combines several packet operations into an exact lookup. The key consists of 16 upcoming tape bits and the four low bits of the call count. Write

```text
n = 16*H+r,  H>=1.
```

While building a window, maintain `n=2^e*H+b`. A packet is included only if its branch is valid for **every** `H>=1`, the coefficient remains divisible by its cycle length, and its output fits inside the 16 tape bits. Its remainder is then determined by `b` alone. The entry stores the resulting tape field, exponent, bias, width, and number of logical packet events. Runtime applies those updates using exact integer arithmetic. Small counts and rejected windows use the single-packet path.

The directory contains `2^20` entries of eight bytes. Known preperiod suffixes and cycle rotations are also accepted as starting packets, using the same checked finite laws. Table construction is outside the reported simulation time. `--single` disables this composition while retaining packet-cycle acceleration. At 10,000 complete rounds, sequential comparisons of the implementation on this host gave:

| Entry | Single packet / deque | Windows / deque | Windows / symbolic counter | Default, including prefix skip |
| --- | ---: | ---: | ---: | ---: |
| 405 | 4.504471 s | 1.338299 s | 0.913177 s | 0.647199 s |
| 482 | 8.119233 s | 2.799909 s | 2.703569 s | 2.598388 s |

All four paths agree on the entire final word and logical event count. The first three modes of each comparison disable prefix skipping to isolate the changes. Windows alone measured 3.37x and 2.90x over the corresponding single-packet path. The complete default modes measured **6.96x and 3.12x**, respectively. These compare paths in this implementation, not a previously published simulator. Table building is excluded; wall times depend on host load. The window builder and native streaming arithmetic remain **unverified**.

## Exact power-plus-offset call counts

A further representation keeps the call count as `2^e+d`, with a signed offset `d`, instead of immediately materializing the long binary integer. Dividing by `2^t` updates the exponent and uses **floor** division on the signed offset; multiplying by a power of two and adding a small constant update the two fields directly. If the exponent becomes small, the full value is evaluated exactly in 128 bits. If `abs(d)` reaches `2^100`, the counter is converted to the existing deque representation before any overflow. The fallback is exact and can occur during an ordinary search.

This makes both a long power of two and a long borrow, such as `2^80000-3`, cheap. At 10,000 rounds, with windows enabled and prefix skipping disabled in both cases, the change measured 1.47x on entry 405 and 1.04x on entry 482. Entry 405 required no dense-counter fallback in that benchmark; entry 482 required 9,778. This limited benefit on the second target is why the dense fallback remains necessary. A 1,000-round comparison starting at boundary 200,000 showed that the sparse representation was slower on entry 482 (10.712 versus 9.822 seconds before specializing the dense path). The default therefore selects the symbolic counter for **405** and the deque for **482**. `--dense-counter` and `--sparse-counter` explicitly select either representation. The aggregate default speedups above are measured directly, not obtained by multiplying ratios.

## Skipping the unchanged prefix

Every `1010` packet preserves its four cells for every incoming call count. The simulator remembers a prefix already known to consist of these packets. Prepending `10` at the next boundary preserves that many complete packets; scanning only at the old edge extends the known prefix. It then initializes the remaining call count directly to `2^m` and advances by `4m` cells, using the checked unbounded composition rule. With the symbolic counter, this avoids visiting the known prefix's packets individually or materializing its exponential call count. The dense counter still allocates its shifted limbs.

This cache is an optimization, not an assumed property of arbitrary input: a resumed checkpoint starts with no cached prefix, and all newly skipped cells are inspected. The unprocessed tail is still evaluated normally. `--no-prefix` disables the shortcut. It is compared against full packet processing on early orbits, the million-bit catalogue-failure regression, and 100 further rounds from each large checkpoint (400,000 and 300,000 rounds).

## Checks and searches

[packet_stream_validate.py](packet_stream_validate.py) contains an independent Python finite-tape oracle, cycle learner, and arbitrary-precision recursive evaluator. It discovers its packets instead of importing the C++ catalogue.

- For each target, 1,000 complete rounds agree with Python on the entire tape; 100 rounds also agree with the learner's repeated-packet shortcut disabled.
- Ten ordinary-TM boundary snapshots agree per target, through 2,605 and 4,827 measured raw steps, respectively.
- Single-packet and window paths agree on the entire tape after 100,000 rounds per target. Each observed word then begins with 50,000 doubling packets; the exponential interpretation remains conditional on the native trajectory being correct.
- 100,000 random field/shift operations agree with unsigned 128-bit arithmetic. All useful window keys are checked at three independent high-counter values, with exact composition comparisons recorded in the result ledger. A further 200,000 random counter operations, including large exponents, negative offsets, conversion to dense storage, and complete materialization checks, compare the sparse counter with the deque.
- Split checkpoint runs, reloads, malformed inputs, rollback on budget exhaustion, unknown packets, and the artificial halting boundary are checked. The full native/Python suite passes under undefined-behavior sanitization.

Coq checks 34 finite packet laws, both blank-entry bridges, both round-entry bridges, both local halting packets, and the two unbounded exponential composition statements. All twelve printed assumption reports are closed; the file passes a separate kernel check. These local and composition proofs do not certify the native evaluator or its saved long runs.

The initial catalogue stopped at **161,210 complete rounds** of entry 405. At tape offset 1,001,246, the next packet was `001100` and required four calls. The independent learner found a six-cell preperiod/cycle, and its next complete boundary matched the native evaluator on all 1,001,253 tape bits. Six new local laws were checked in Coq before continuing. This was an insufficient catalogue, not a halt. [packet405_frontier.checkpoint.gz](packet405_frontier.checkpoint.gz) preserves the pre-extension boundary, and the standard validator rechecks it against the independent Python learner and both native comparison modes.

[packet_results.json](packet_results.json) records the full-run summaries, benchmark, validation, and checkpoint hashes. The compressed checkpoints store full tapes, not only hashes; decompress with `gzip -dc saved.checkpoint.gz > /path/to/saved.checkpoint` before `--resume`. A guessed invariant language `(000 | 100 | 1010)* 0^inf` was rejected: boundary word `0x41` returns to `0x185`, outside the proposed grammar. No nonhalting conclusion is drawn from the long surviving runs.

The final searches reached **500,000 rounds for entry 405** and **300,000 rounds for entry 482**, without halting. Their tapes contain 3,106,341 and 4,199,938 bits, respectively. The last 100,000 rounds of entry 405 used the cached prefix shortcut, with no dense-counter fallback. The final entry-482 segment predates the change to its faster default counter choice. Cumulative times in the ledger sum the continuation segments, excluding duplicate cross-check runs. [packet405.checkpoint.gz](packet405.checkpoint.gz) and [packet482.checkpoint.gz](packet482.checkpoint.gz) preserve the complete final tapes; both reload exactly.

## Reproduction

```sh
g++ -O3 -march=native -std=c++17 -Wall -Wextra -Wconversion research/holdouts-623/packet_stream.cpp -o /path/to/packet_stream
python3 research/holdouts-623/packet_stream_validate.py /path/to/packet_stream
/path/to/packet_stream --entry 405 --rounds 100000 --seconds 600 --max-bits 4000000 --checkpoint /path/to/405.checkpoint
/path/to/packet_stream --entry 405 --resume /path/to/405.checkpoint --rounds 100000 --seconds 900 --max-bits 4000000 --checkpoint /path/to/405.checkpoint
/path/to/packet_stream --entry 482 --rounds 10000 --single --hex
coqc -native-compiler no -Q verify BusyCoq verify/ResearchPacketCoverage.v
coqchk -silent -bytecode-compiler yes -Q verify BusyCoq BusyCoq.ResearchPacketCoverage
```

The saved entry-482 tape exceeds the default bit limit; use `--max-bits 5000000` when resuming it.

`--rounds` is an **additional complete-boundary-round** budget. `--hex` is intended for small full-state comparisons. The default bit limit is two million, applied to both the word and call counter, not all auxiliary allocation. Time checks occur during rounds; interrupted work is not counted. Every native result says `"verified": false`. All bounded failures remain unknown. AI-assisted implementation and tests by Codex, with the underlying packet method credited above.
