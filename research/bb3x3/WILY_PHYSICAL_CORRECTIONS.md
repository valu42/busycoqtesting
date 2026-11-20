# Wily after a physical correction

From the last known blank correction, a sufficient condition for nonhalting of both Wily machines is a first-letter test on the iterates of one 24-letter word. The test allows positive scalar excursions. A different infinite family of genuine finite starting tapes passes the test, undergoes a physical correction, and has infinitely many positive excursions. Whether the actual blank passes the test at all depths remains open.

All words below are in head-facing order. On a nonempty tail after the two fixed low zeros, each successive pair of the original sweeps acts as a single mode 0. Use the [scalar encoding](WILY_INTEGER_MAP.md) with bucket `B`, numerator `n=3z-B`, and virtual continuation `T=(10)∞`. For an arrival period `w`, let `Q(w)` be its phase-preserving output period through the two preallocated bits `10`. A cell processes one or two full periods until its bit returns. Retain each emitted event in order and take the primitive word starting at that same phase.

## A first-letter test from blank that permits positive excursions

The actual correction at scalar update 583 produces the 29-bit word

```text
10100101010100010010101000100
```

Its numerator is −318,922,769. Feeding mode 0 repeatedly through those 29 bits gives the following primitive period at the physical edge.

```text
P = 222030111101130321301012
```

Write `c_j` for the first letter of `Q^j(P)`. **There is neither a further physical correction nor a halt if and only if every `c_j` is 2 or 3.** If the condition fails, the first offending letter is the actual next corrective or halting mode, at width `29+2j` of the trimmed tail.

Indeed, from an empty edge a first 3 allocates 00. Equivalently, sending this first 3 into a preallocated virtual pair 10 writes 00 and stops. All later arrivals then see exactly the allocated cells in their physical state. Thus the physical arrival period at the next edge equals `Q(w)`. A first 2 analogously writes 11 on the first virtual pair and emits 3. This 3 writes 00 on the second pair and stops. Those four bits are the actual allocation 1100. Thus the new edge period is `Q²(w)` and the skipped intermediate first letter is 3. A first 1 halts and a first 0 makes the next correction. Induction proves the test. A first 1, when propagated virtually through 10, emits 1 again, so that all deeper first letters then equal 1.

The periods at these virtual cutoffs are all nonempty for this seed. Immediately before the 29-bit state on its virtual orbit is the singular sweep from numerator 2,031,034,478, as shown in the [blank scalar calculation](WILY_INTEGER_MAP.md). It reaches every finite cutoff. At each cutoff the evolution of the lower fixed-width bits is a permutation, since the single-bit rule at every fixed incoming carry is invertible. The earlier singular input's low prefix therefore recurs at a positive time, sending another arrival to the cutoff. This also ensures that in the successful case the physical run makes infinitely many edge extensions.

## All corrected physical words

For nonempty inputs, the words produced by a mode-0 edge correction are **exactly** the binary words with no adjacent ones and with final three bits 100. Each has a unique input. From mode 0 the primitive paths back to mode 0 that have not stopped read either `01` or `1 0^k 11` with `k≥0`. They write `10` and `0^(k+1)10`, respectively. Their nonempty concatenations, followed by the single allocated zero, give the characterization. To invert, remove the last zero and split immediately after each 10 to reconstruct the primitive paths. The bare empty-edge input instead produces the one-bit word 0.

In scalar terms, the positive correction inputs are exactly the descendants of the positive-to-negative crossing root 2, represented at their canonical bucket. A mode-0 correction requires an input with highest bit 1, hence `p≥B/2` and the bucket is canonical. Its virtual output lies between `−28B` and `−25B−3`, giving canonical output bucket `64B`. The [crossing table](WILY_INTEGER_MAP.md#exact-changes-of-bucket-at-a-sign-crossing) forces root 2. Conversely a root-2 descendant has this 64-fold ratio. At the canonical input bucket, neither an internal stop nor a mode-2 or mode-3 allocation can give that ratio. The root preserves residue and therefore cannot halt.

The corrected numerator has a second exact description. If `p` was the input, the result is `F(p+6B)`. In fact `p+6B` is represented by the old physical word followed by `11T` rather than `T`: the new high numerator is 5 in place of −1. When mode 0 enters `11T`, it produces `0T`. Its first bit is now 0, the next mode 2 on the second 1 sends mode 1 into `T`, and this complements the alternating continuation. This agrees exactly with appending the physical zero. The virtual sweep from `p+6B` is singular. The corrected word has highest bits 00, so its new bucket `2B` is canonical.

## Corrected finite tapes with infinitely many positive excursions

Consider the reduced nonempty input `X=01011000110110110101`. Its first sweep makes a mode-0 correction, giving `Y=101000001010001010100`. In scalar coordinates this is the transition from `(1085774,2²⁰)` to `(−1061105,2²¹)`. The arrival period through `Y` is `23211301122322222`. The table propagates each complete periodic input through the empty physical edge. To reproduce any row, consume the first event for its allocation, rotate the period by one place, then send it through the allocated bits in order.

| Edge period | Physical allocation | Period at the next edge |
|---|---|---|
| 23211301122322222 | 1100 | 222303111030 |
| 222303111030 | 1100 | 303222030 |
| 303222030 | 00 | 311103022230 |
| 311103022230 | 00 | 211111122303030 |
| 211111122303030 | 1100 | 222303111030 |

The last four rows repeat and allocate twelve cells on every cycle. In the row beginning 31, the first event creates two zeros. The next arrival is 1. It writes 1 on the first zero, then mode 3 writes 1 on the second and stops. The two highest bits are now 11, forcing the scalar to be positive independently of every lower bit. Each allocation in the table ends in 00, forcing a negative scalar immediately after it. Thus the actual trajectory continues forever through infinitely many positive and negative excursions. For either original Wily encoding, prepend the two fixed zeros and use the initial sweep phase.

This certificate extends to arbitrarily large correction widths. For any integer `j≥0`, let

```text
Y_j = Y (10)^(2+6j) 000000100.
```

These words meet the corrected-word criterion above. Write `A=222303111030`. Processing two pairs 10 after `Y` gives `A`. Processing six more pairs from `A` gives `A` again. The final nine bits transform `A` into `222030303030303222`, whose first physical allocation leads straight to the row `311103022230`. The unique preimage of each `Y_j` therefore starts with a correction and enters the same mixed-sign cycle. The actual blank's 24-letter seed has no established entry to this cycle.

## A correction can hide either outcome for arbitrary periodic drivers

There are two rotations of the same finite period that give arbitrarily many consecutive mode-0 edge allocations before one driver halts and the other runs forever. The number here counts successive allocations. Other arrivals can occur between allocations. This statement concerns arbitrary periodic drivers at an empty edge.

The base periods give the following exact chains.

| Initial period | Following edge periods | Outcome |
|---|---|---|
| 0312003312 | 0212312, 231312, 30, 30 | Repeats the last row forever |
| 0033120312 | 1021312 | Halts |

For the lift, introduce a marked token `M` representing 3120. In the cyclic token word `M M 0 3`, cut the stream at the final 0 in the first or second marked token to obtain the two base periods. Substitute all tokens simultaneously as follows.

| Token | Substitution |
|---|---|
| 0 | 31 |
| 1 | 03 |
| 2 | 2 |
| 3 | 13 |
| M | 3 M 31 |

Starting on a single zero, each ordinary substituted block emits exactly its token and restores the zero. The block `3 M` emits 312 and restores the zero. Consequently the entire substituted marked block emits `M` and restores the zero. A cut inside the same marked token of the substituted circular word again starts with 0. This event allocates a new zero. At that cell the following initial 31 emits 0, the intervening complete substituted blocks reproduce their tokens, and the closing `3 M` emits 312. The resulting next edge stream is exactly the original cut. Induction adds one physical mode-0 allocation at each substitution while retaining both terminal outcomes and the rotation relation. The reachable 24-letter blank driver is a separate constraint.

Run `python3 wily_physical_corrections.py` in this directory to verify the finite identities and compare the correction language with every physical word through width 12.
