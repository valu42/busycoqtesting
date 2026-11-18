# Freely supplied entry streams on line 10

The machine is `1RB2RB3LA4LA1LA_2LB3RA---4RA1RB`. Keep the ordinary-cell return convention and edge branches of [the line 10 derivation](frontier-background.md#line-10--an-exact-right-edge-test). A normal edge holds 3. On its successive inputs, the first B selects one of the three successful branch words B, AB and AAB. The fourth possibility AAA reaches the undefined B2 instruction. Write `T_s` for an interior cell starting with symbol `s`, converting entries from its left into calls to its right.

**Claim.** Any finite list of successful branches followed by a halt can be forced by a finite input word at a normal edge. Its unused tail may be all B. The same holds with any fixed finite string of ordinary cells 1, 3, 4 before the edge. Any infinite list of successful branches can also be realized by a suitable infinite input stream.

For one cell, the following physical input words emit exactly the requested single output letter. Each entry gives its input and ending tape symbol.

| Starting symbol | Emit A | Emit B |
|---|---|---|
| 1 | B, finish 4 | A, finish 3 |
| 3 | AAB, finish 4 | AAA, finish 3 |
| 4 | AB, finish 4 | AA, finish 3 |

For example, A acting on 3 is silent and changes it to 4. A acting on 4 is silent and changes it to 1. B acting on 1 emits A and leaves 4. Together these operations give the middle row's A entry. The other cases follow from the same ordinary-cell table. Repeated substitution in this table from left to right gives a right inverse `I_s` on finite words. It preserves prefixes, consumes at most three input letters for each desired output letter, and satisfies `T_s(I_s(w)) = w`. This constructs a right inverse for any finite stack of ordinary cells by applying the individual inverses in reverse physical order.

The old edge consumes the branch prefix and sends the remaining word through the following cells, listed from left to right.

| Branch prefix | Initial symbols of the ordinary cells applied to the tail |
|---|---|
| B | 1 then 4 |
| AB | 4 |
| AAB | 4 then 4 |

To force word `w` at the next normal edge, invert that stack on `w`, then prepend the branch prefix. With `w = AAA` at the final edge, induction backwards through a prescribed list of finite length gives the advertised input. Every witnessed branch and the final halt occur within the forced prefix, so any unused tail is allowed. For infinitely many prescribed successes, begin with their successive finite prefixes and use an empty terminal word. The inverse constructions preserve prefixes, and every branch adds at least one letter. Their limit is a single infinite stream realizing all the prescribed branches. The concrete execution for each finite part takes finite time by the machine's local branch rules.

This gives a scope limit on an invariant that discards the actual upstream stream. With only the initial symbols of an ordinary finite suffix and a normal edge, both halting and indefinitely successful continuations are possible. The blank machine has a particular upstream stream, fixed by its negative half and the preceding cells. Its status is still open.

The accompanying [literal checker](line10_control.py) verifies all branch lists through length four, each with three choices of initial stack, for 363 complete histories ending on B2. Run `python3 line10_control.py`.

## A finite perturbation at the published checkpoint

The [published 72.5-billion-period checkpoint](frontiers/runs/stream-10.json) has 247 occupied nonnegative cells. Its last symbol is 4. Two consecutive A entries there halt. The first A4 writes 1 and returns left. The next A1 sends B into a virgin zero, which returns in B to the freshly written 2. The remaining 246 cells are ordinary. Applying the single-cell inverse through those cells therefore synthesizes a finite perturbation of the actual driver that agrees with the entire run through step 21,025,000,004,301,661,487,112. From then on it supplies a specific finite word and reaches B2 before the original periodic driver could be resumed. This is a witness on *modified input*, not a halt of the blank machine.

The forced word can be counted without materializing it. For a desired nonempty word with counts `a,b` and final letter `z`, the inverse cell emits one B per A and one A per B. Before every such emitted letter it also emits some As. Their initial number is `h`, respectively 0, 2, 1 for starting symbols 1, 3, 4. Each subsequent letter gets one prefix A if the preceding desired letter was A and two if it was B, by the table of ending symbols. Thus the new count of As is `b+h+a+2*b-1-(z == B)`, the new count of Bs is `a`, and the last letter is the opposite of `z`. Starting from `AA`, the synthesized word at cell zero has exactly **228454031675318707213066823549921717982091587249575142964902392763282552632512711408143400 letters**. This is one constructive witness length; no optimality is claimed.

## The three phases at coordinate three

At coordinate 3, the authentic normal-edge stream is the period BAA in precisely that phase. The other two rotations both halt when supplied to the same normal edge.

| Repeated stream | Input call containing the first halt | Coordinate of B2 | Defined moves on cells at or right of 3 before B2 |
|---|---:|---:|---:|
| AAB | 1,755 | 52 | 28,337 |
| ABA | 5,937 | 68 | 101,469 |

These are literal right-half counts. They charge one for each defined instruction, and each return left of coordinate 3 consumes the next supplied input. They contain no moves for generating the external input. The blank machine uses BAA and passes both coordinates.

## Every mature finite stack cycles through all its states

There is also an exact restriction on candidate invariants for the *actual* period BAA. Let an ordinary stack have `k` cells with any initial symbols from 1, 3, 4. Feed it repetitions of BAA, giving all calls across its right boundary the ordinary return in A. At period boundaries the stack visits all `3^k` possible symbol vectors exactly once before returning. The statement applies to a finite interval of the blank run for as long as that finite stack has ordinary returns throughout the interval.

In fact take any period with counts `a,b` congruent to 2,1 modulo three. A advances the first cell's phase and B decrements it, so one period advances the phase by one. In three traversals each input position sees all three phases. Across these traversals each input A emits a single B in total; each input B emits two As and two Bs in total. Thus the full output word has counts `2b,a+2b`, again congruent to 2,1. It repeats at subsequent three-period boundaries. By induction the remaining `k−1` cells have least return period `3^(k−1)` under this output word. Returning the whole stack requires a multiple of three source periods, so its least return period is `3^k`. Every starting vector returns, and there are exactly `3^k` vectors. Consequently an indefinitely mature stack driven by BAA has no proper invariant subset of its symbol vectors when sampled once per period. This strengthens the [cyclic letter-count argument](research-log.md#line-10--exact-periods-lose-the-distinguished-starting-point) to a statement about the complete local configuration.

## Continuing the actual phase

The [full checkpoint](line10-364361109000.json) records 364,361,109,000 source periods, 272 visited nonnegative cells, and **531,036,071,028,458,284,326,732** defined instructions from blank. The run is live in state B on cell zero. Its predecessor at 125,212,659,000 periods was independently reproduced with the original repository stream engine, including the tape, head, state, and the exact clock of 62,712,839,902,830,404,228,636. A five-cell transducer lookup with an exact repeated prefix period produced the final checkpoint. The original stream engine independently continued from the verified predecessor for 16 batches of 14,946,778,125 source periods each and reproduced the final checkpoint byte for byte. To replay from the published 72.5-billion-period file in 200 smaller equal batches, run the following from `research/bb2x5`.

```sh
c++ -std=c++17 -O3 frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/line10-stream
python3 frontiers/longitudinal.py --line 10 --engine /tmp/line10-stream \
  --resume frontiers/runs/stream-10.json --groups 1459305545 --batches 200 \
  --max-bits 50000000 --finite-slots 5000000000 --checkpoint /tmp/line10-replay.json
cmp /tmp/line10-replay.json line10-364361109000.json
```

The final endpoint proves a finite lower bound. Whether the actual stream ever starts AAA at a normal edge remains open.
