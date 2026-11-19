# Exact first-contact tests for #397

On the blank trajectory, the first `f` reaches the empty edge on sweep index **926,416,354** (the first sweep has index zero). The occupied suffix then has length 137, and `f` appends `1001`. All 60 previous growths were `b` or `d`, with 44 and 16 occurrences respectively. The last occupied bit remained 1 at all completed sweeps up to this event. A proposed invariant allowing only `b` and `d` at the edge already fails on the actual blank trajectory.

The [checker](first_contact_397.py) replays the blank run to a return phase with 45 known cells, constructs one period of timestamped carries leaving those cells, then processes only those events up to the first `f`. It also checks the following integer first-contact formula directly against all six sweep rules.

## A binary register for a run of ordinary carries

Split a word into complete pairs `x_i y_i` in head-facing order, temporarily setting aside its last bit if its length is odd. Select the first bit `x_0` and each later `x_i` whose *preceding* pair has equal bits. Define J as the little-endian integer formed by these selected bits, with the first selected bit in the units place. For zero complete pairs use J = 0.

The [two-bit rules](PAIRED_PASS_397.md) give these facts.

* Each ordinary `a` leaves every pair equality unchanged. It complements both bits of a visited pair exactly when the incoming carry is `a`. As it traverses the word, that is the first pair and every pair following an equal pair.
* It stops at the first selected one. The lower selected zeros become ones, and that selected one becomes zero. Hence one `a` decrements J when J is positive, without reaching the end of the complete pairs.
* At J = 0 the next `a` traverses all pairs, sets all selected bits to one, and sends `a` beyond them if the last pair is equal or `d` if it is unequal. With no pairs the input `a` itself reaches the residual word.

Consequently **the first contact is on the (J + 1)-st ordinary `a`**. If there is no residual bit, that contact grows the word. A residual one also grows the word. A residual zero halts. Since `d = a²` even at the growing edge, a block equivalent to q ordinary `a` inputs contains a halt exactly when the starting length is odd, its last bit is zero, and **q > J**. The odd-length case compares J only on its complete pairs.

For `b,c,e,f` on a nonempty word, first use its first bit to find the outgoing carry in the original table. That carry is silence, `a`, or `d`, so the same test applies to the remaining word with q = 0, 1, or 2 respectively. This accounts for all six modes.

## Which sweep phases can halt

After blank sweep 64 use the [29-bit returning prefix](TRANSITIVE_SECTION_397.md), and let k count the occupied cells beyond it. The absolute pass indices below are residues modulo 1,024. The 33-mode period crossing the cut contains ten local `b` modes, which stop at the next occupied cell. The other 23 fall into two classes.

| State of the word beyond the cut | Possible source of a halt | Exact guard |
|---|---|---|
| k odd | `d` at phase 769 or `a` at phase 961 | Last bit 0 and J < 2 or J < 1 respectively |
| k even and positive | A source `c`, `e`, or `f` at one of 21 phases | Last bit 0 and the register after dropping the first bit is smaller than the outgoing q |

For ordinary source modes the test acts on all k bits. For the other source modes the ordinary part acts on k − 1 bits. This proves the parity restriction in the table. At k = 0 the actual first arriving source mode is `b`, which appends `01`.

A successful edge event from an ordinary source leaves k odd, irrespective of its previous parity. At even length the outgoing edge mode is ordinary and appends an odd-length extension. At odd length it appends an even-length extension. A successful event from the other source class similarly leaves k even. All four successful extensions end in one. Thus the occurrence of a zero terminal bit between two growths, and the size of the register at the eligible source phase, are the remaining tests for a halt. Whether the blank trajectory ever satisfies both remains open.

## A real prefix where the two-bit guard fails if made the frontier

Every word ending in `01` survives its next single carry. A carry reaching its last one cannot emit either halting mode. It cannot emit `a` either, since that would require `f` on the last one and no carry emits `f` on the preceding zero. So any growth from this suffix is by `b`, `d`, or `f`, each of which leaves the word ending in `001`. An early stop can nevertheless alter the guard. In particular, an incoming `b` at the penultimate zero changes it to one and stops.

On sweep index 636,770 the actual blank suffix has 91 bits. Take just its first 40 and keep the genuine sweep phase. This hypothetical shortened word ends in `001`:

```
1100010001000000000110000001100000011001
```

On that very sweep it grows by `d` to length 43. The next four events crossing the old 40-bit cut are `b`, `a`, `c`, `d`, at sweep indices 636,865, 637,354, 637,697 and 637,734. Applied in order to the newly grown `001`, the first three leave `101`, `011`, `100`; the final `d` emits `e` and halts. The complete original blank program has 51 additional occupied bits beyond the chosen cut at the start of this comparison. Hence the earlier `001` guard, an ordinary `d` extension, and the actual stream phase do not by themselves certify the next growth.

Keeping the source phases of a pair of `d` growths also fails to decide what follows. On the real blank trajectory the successive growths at passes 28,417 and 37,346 are both `d`. They occur at phases 769 and 482 modulo 1,024 and at suffix lengths 65 and 68. At pass 9,288,449 the genuine 101-bit suffix has a different prefix of 47 bits ending in `001`. Truncating there yields `d` at pass 9,288,449, `d` at 9,289,186 and a halting `e` at 9,295,330. This starts at the same length parity and reproduces the two growth types and the two source phases exactly.

Run `python3 first_contact_397.py` in this directory.

## A two-state test at each newly created last cell

Every successful extension ends in a one. Follow that last bit until the
next edge event. The only carry that stops at this bit is `b`, which flips
it. Every other incoming carry immediately produces the next edge event.
Thus, measured **at the last occupied cell**, a halt occurs exactly when
its input starts with an odd number of `b` events followed by `a` or
`d`. This includes a possible halt on the first sweep after a growth.

| Next input after the initial `b` run | Last bit still 1 (even run) | Last bit now 0 (odd run) |
|---|---|---|
| `a` | `b` grows the edge | `c` halts |
| `d` | `f` grows the edge | `e` halts |
| `c` or `e` | `d` grows the edge | `a` grows the edge |
| `f` | `a` grows the edge | `d` grows the edge |

The entries follow from the six one-bit transitions. This is a local
condition on the order of the actual incoming events. Frequencies at a
fixed cut do not specify that order.

There is a short sufficient condition for consecutive `d` growths.
Immediately after `d` appends `001`, choose the cut just before those
three bits. Any number of incoming `b` events there leaves either
`001` or `101`. The first subsequent `c`, `e` or `f`, if it comes
before an `a` or `d`, sends exactly `d` through either three-bit
word. Thus the next edge event is a second `d`. This conditional
argument leaves the order of the actual input to that cut open.

## Finite-state invariants at the 1,024-sweep return

At the [blank-connected 29-bit cut](TRANSITIVE_SECTION_397.md), the
dynamic tail starts empty and takes the same 33-carry input every 1,024
sweeps. Any inductive safety invariant for these returns recognized by a
deterministic automaton reading the tail **from the far end toward the
cut** needs at least eight states. The result applies to a fixed word
predicate at this return phase.

The [generator](regular_guard_397.py) reconstructs 26 words that an
invariant must accept by iterating the blank-connected input. From the
[additional examples](regular_guard_397.tsv) it verifies 31 words that
must be rejected and 19 implications. A rejected word takes a halting
carry within eight periods. Each implication requires acceptance of a
live one-period successor whenever its predecessor is accepted.

Generate the seven-state SAT query with
`python3 regular_guard_397.py regular397.cnf`. For each tested suffix
and possible DFA state, the formula propagates the state reached from
the empty suffix by reading the next bit. The unknowns are the two
transitions and acceptance flag of each state. Reachable states can be
named in order of first discovery. Any smaller DFA can use spare states
as unreachable states. The resulting DIMACS query has 7,802 variables
and 54,950 clauses. Both CaDiCaL 1.9.5 and Glucose 4.2 report
unsatisfiable. The search leaves larger automata open.
