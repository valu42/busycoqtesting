# What the two ends of a Wily Coyote or #397 word can certify

For #531/#532 and #397, no inductive safety invariant depending only on the
first `h` and last `k` bits of the **full sweep word** can decide the blank
run, for any fixed finite `h,k`. The invariant may also use the exact pass
number and exact word length. The obstruction is a finite sequence of legal
one-pass transitions after allowing the unrecorded middle to vary between
passes. This sequence need not occur from blank.

## Delivering a chosen carry

Use the bit and mode numbering of [the sweep tables](check_bb33.py). Wily
mode 3 and #397 mode 1 both flip the first bit and stop before the next cell.
Across the two possible starting bits, every mode occurs as the outgoing
mode of some transition. Consequently, from either bit, a prescribed mode
can be sent to the next cell in at most two input events. If necessary,
first flip the bit with the local stopping mode. This extra event sends
nothing to the next cell.

Given any particular word of `k` bits, request a dangerous carry at its far
edge. Lift this request through the last bit, then lift the resulting stream
through the preceding bit, and continue back to the first bit. At each cell
use its current value after the previous requests in its stream. At most
`2^k` input events suffice. The dangerous carry is the first event to reach
the far edge. No earlier event changes the length. This construction also
allows any specified bit pattern to be written without sending an event to
the far edge. Set bits from right to left, delivering the local stopping
mode whenever a flip is needed.

## Delivering those inputs on the scheduled passes

After at most `h` successful passes the first `h` bits of the full word are
the initial `h` bits of the protected periodic pattern from the
[sweep reduction](RANKINGS.md). Reading these bits starting in the ordinary
initial mode yields one of the scheduled modes. The same prefix remains
protected on the next pass whatever the middle bits, since each pass prepends
the initial bit and rotates the symbols of the protected prefix by one.

Allow the `d` bits between the protected prefix and the recorded suffix to
have any values. Treat an early stop in this middle as silence. The possible
outputs of a mode set after one free bit are the union of its two transitions
for each mode, with silence mapping to itself.

| Machine | Free bits | Modes that can reach the suffix |
|---|---:|---|
| Wily | `d ≥ 3` | All four modes and silence, starting in either scheduled mode |
| #397 | `d ≥ 4` | Either `{0,3}` or `{1,2,4,5}`, and silence, from each scheduled mode |

For #397 each additional free bit swaps the two sets of active modes. Direct
substitution verifies the table at depths 3 and 4, respectively. Reapplying
the transition-set rule proves it at every larger depth.

Choose the middle to deliver the next requested input to the suffix. For #397
when that mode is unavailable, choose a middle yielding silence. A successful
pass prepends one bit, growing the word, so the middle is now one bit longer.
The desired mode is available on the next pass. Repeat until the final
dangerous carry. Thus at most `2^k` passes for Wily, or `2^(k+1)` for #397,
suffice from any such abstract state.

An inductive predicate recording the two ends, length and pass number must
accept *every* choice of middle consistent with an accepted state. Therefore
it must admit this path once it accepts a long enough word with the protected
prefix. A purported safety proof from blank gives arbitrarily long such
words, because every successful pass prepends a bit. This proves the claim.

The same test applies after removing the entire known periodic prefix. In
that model the unseen length stays fixed until a carry reaches the far edge,
and the starting mode cycles between passes. For Wily both starting modes
admit every input; for #397 successive phases alternate the two active mode
sets. Thus a last-`k`-bit invariant on the **remaining suffix** cannot
certify any state with at least 3 (Wily) or 4 (#397) additional unrecorded
bits. A proof using more information about the middle remains possible.

Checking the invariant only once per full scheduled period also fails.
Begin with the two Wily carries or the four #397 carries of a single
period, in any cyclic phase. On one free bit, run this entire stream,
keeping the bit's updates between consecutive events. Remove outgoing
stops and keep all other events in order. Enumerating both starting bits
at each new cell gives every possible output stream. After three free
bits for Wily or six for #397, the possible streams include **every
one-event stream**. They still include each singleton after arbitrarily
many further free bits, since every carry is a transition output at some
bit. We can therefore supply each event of the construction using a whole
period, choosing the middle just once per period. For the full word, the
initially protected prefix grows by one each pass; the original middle
sees precisely one cyclic period.

Run `python3 suffix_obstruction.py` from this directory. It verifies the mode
sets and the induction on free length against the existing sweep tables, and
replays the construction for every bit word through width seven.
