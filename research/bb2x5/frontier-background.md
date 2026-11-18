# Earlier derivations for lines 17 and 10

These are the earlier results used by the current research log. The accompanying executable module is prior_frontier.py. All line numbers refer to the formal 37-machine list.

## Line 17 · a finite counting phase and its exit

Racheline identified this machine as a counter with a possible halt at overflow. The analysis here gives a marked-input description of the counter, a test for an internal halt, and a concrete conclusion about its next overflow from the 424-digit blank-orbit configuration. Priority over unpublished work is unknown. [Prior discussion](https://wiki.bbchallenge.org/wiki/1RB2RA3LB---2LB_2LA0LA4RB0RB1LA)

| Read | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| A | 1RB | 2RA | 3LB | halt | 2LB |
| B | 2LA | 0LA | 4RB | 0RB | 1LA |

### Configuration and entry

Let the head scan a blank in A immediately before `231302 (12)^k D 2`. The spaces mark cuts in the word. The rest of the tape is blank. An element of the register D consists of two consecutive symbols. Its first symbol is 1, 0 or 2 for its trit v equal to 0, 1 or 2, respectively. Its second symbol is 2+f, where f is a bit. Index the data pairs from zero, left to right. The final 2 is a singleton outside D. The k copies of `12` are handled separately.

The literal blank execution gives the following entry certificates. At each listed step k is zero. The checker below runs all 2,308,940 defined instructions to verify the last entry independently of any macro.

| Defined steps | Head | Data pairs | Rightmost cell previously visited |
|---:|---:|---:|---:|
| 252 | −12 | 7 | 9 |
| 2,889 | −37 | 20 | 10 |
| 2,308,940 | −844 | 424 | 11 |

The physical word D at the last entry is the concatenation of `220312221222`, 397 copies of `02`, and `030202121212121303130222031302221302122212`. Its final singleton is at coordinate 11. As cross-checks during discovery, the seven-digit entry completed nine ordinary epochs before its exceptional epoch. The twenty-digit entry completed 400. The proof below applies directly to the literal 424-digit checkpoint.

### What one pair does

A raw probe enters a pair from the left in A or B. Stop when the head exits left. A move past the right end calls the next pair. In the table `b` means such a call in B with a return in A. Symbols `a` and `X` mean calls in A with respective returns in A and B. A result such as `A02` means an exit to the left in A leaving `02`. Each entry can be verified just by running the displayed five-symbol table on two cells, supplying the indicated returns. For instance B entering `22` writes two 4s and sends B right. If A returns, A4 and B4 leave `12` and exit left in A. The alternatives in a cell are conditional on the return from its one A call.

| Pair | Enter A | Enter B |
|---|---|---|
| 02 | b → A02 | ε → A22 |
| 12 | bba → A13 or bbXb → A12 | ε → A02 |
| 22 | ε → B32 | b → A12 |
| 03 | bba → A03 or bbXb → A02 | ε → A23 |
| 13 | halts at A3 | ε → A03 |
| 23 | ε → B33 | bba → A13 or bbXb → A12 |
| 32 | halts at A3 | b → A22 |
| 33 | halts at A3 | bba → A23 or bbXb → A22 |

Define U to be a B probe. Define C to be two B probes followed by an A probe, with one more B probe if the A probe returned in B. An ordinary U returns in A. In an ordinary C, record 1 if its A probe returned in A and 0 if it returned in B. On the normalized data pair, U adds 1 to v modulo 3, and C adds 2. The bit returned by C is 1 exactly when the *old* v was nonzero. These assertions hold whenever the indicated child probes complete normally and the local A3 branch is avoided.

Here is the full rule for calling the next pair. A **generic slot** emits U if the local f is 0. If f is 1, it emits C and sets f to the child's returned bit. A **new start** emits C and sets f to the returned bit, and requires the old f to be zero. Record a generic slot as 0 and a new start as 1.

| Incoming pulse | v = 0 | v = 1 | v = 2 |
|---|---|---|---|
| U | ε | ε | 0 |
| C | 0 | 01 | 00 |

The table follows by composing the raw probe table. In particular C starting at v=1 first issues a generic slot. Its two B probes have by then brought v to 0. If f is still 1 the A probe meets `13` and halts. Otherwise this A probe on `12` issues the new C. This order matters because the earlier generic call may reach the far boundary first. In the proof we rule out the local conflict on the whole virtual ordinary stream. In finite boundary calculations the raw interpreter executes calls in chronological order.

### The marks supplied by the actual header

Start a header epoch with A on the blank immediately left of `231302`. Simulate only these cells and the blanks to their left. An outgoing B probe returns A and an outgoing A probe returns A until the first that returns B. The following finite paths list every outgoing probe. Each leaves A two cells left of its starting point, with `23130212` before the same right cut. The count excludes the subordinate work.

| First A probe returning B | Outgoing raw probes | Header steps |
|---:|---|---:|
| 1 | `BBBABBB` | 65 |
| 2 | `BBBABBABB` | 67 |
| 3 | `BBBABBABBAB` | 69 |

In pulse notation this is U followed by C until the first C returning 0, then enough U pulses to make four slots in total. A C returns 0 at v=0 and changes v by −1 modulo 3, so one of the three rows applies. Equivalently the header supplies the four marks `0100` with no initially pending C. After its mark, send C for successive slots up to and including the one returning 0. Elsewhere send U. A leading `12` has initial trit 0 with f=0. On these four slots it emits respectively ε, `01`, `0`, `0` and its trit returns to 0. Its child receives four slots and the burst starting on the second slot has at most three pulses, so f also returns to 0. By induction on k every leading `12` transmits the same block. Each normal epoch thus appends one `12` to the pile and delivers exactly `0100` to the fixed data cut. Across epochs the mark stream there is `(0100)` repeated.

### Why the 424 digits reach the edge

A digit need only remember v and whether its input C was pending from the previous slot. At the start of the data calculation this pending bit p is the f of the pair immediately to its left, or 0 at digit zero. A digit receiving a mark while p=1 signals the local A3 conflict in its sender. Otherwise a 1 or a pending slot is a C. After C, set p to the bit `old v ≠ 0`. A plain 0 with p=0 is U and leaves p=0. Outputs are the two-row slot table above. This description calculates the mark positions without inspecting subsequent digits.

Every emitted stream starts with 0. Two successive emitted marks are at least three slots apart. Indeed, a mark is the second output of C at v=1. The next input is the pending C at v=0, whose sole output is 0. A later marked output must have another 0 immediately before it. Each input burst has length at most three. Consequently an overlap is impossible except during the initial pending burst of a digit. If that digit has starting trit v, its initial burst takes v+1 slots. In this register the initially pending digits all have v=0 or 1. For v=0 the first unmarked slot suffices. For v=1 only a mark on slot two can pose a problem.

Let m indicate that the *second* input slot is marked. The root value is true. For a digit with input bit p initially set, the second *output* slot is marked exactly when v=1. For p clear the second output is marked exactly when v=0 and m is true. To see the latter claim, the first input is an ordinary U. Starting from 2 already emits a zero and the next nonempty output begins with zero. Starting from 1 reaches 2, whose next input emits either a zero or two zeros. Starting from 0 reaches 1 without output. Only a mark right then can emit `01` before another generic slot intervenes. These cases give a single pass over the initial digits, storing just the preceding flag and m.

The initially pending indices and trits are `(2,0), (404,1), (411,1), (412,0), (413,1), (416,0), (417,1), (420,1)`. The recurrence gives m=false at all five with v=1. Induction over the 424 digit positions proves the virtual streams well-defined with no conflicting mark. Every three input slots to any one digit emit at least one slot, because only ordinary U at 0 and 1 can be silent. Hence at most 3⁴²⁴ slots at the first digit are needed for an output at the terminal. This is an upper bound in header slots, not elementary steps.

Take the finite prefix ending at that first terminal call. Before it, raw probes have finite nesting depth and each local table path is finite. The growing left pile is finite in every one of the finitely many epochs. Induction down and back up these finite calls identifies the computation with the concrete execution. Both U and C begin with a raw B probe, so the first visit to the old singleton is B on 2 followed by B entering virgin cell 12. There is no preceding undefined transition. The next two literal instructions on the blank and the rewritten singleton return in B toward the register. A normal B probe would have returned in A. This is exactly where continuing the ordinary-epoch argument would lose the actual execution.

### Four marks survive 350 consecutive digits

The long run of identical pairs preserves more information than its trits alone. At cut 53 the first four marks are at one-based slots 5, 11, 17 and 23. This can be calculated from the literal period `0100` without running a full register epoch. For each digit propagate the finite prefix and then copies of the input period until `(v,p)` repeats at a period boundary. The intervening output is a period. At cut 53 there is no initial transient and the computed least period has 147,740 slots.

If a digit starts with `(v,p)=(1,0)` and its first k marks occur at slots 5, 11, …, 6k−1, then its first k output marks occur at exactly those slots. The first four plain inputs supply one generic output. At the mark the trit is 2, so the marked burst on three inputs emits `00`, then `01`, then `0`, ending at trit 2. The next three plain inputs supply one generic slot and restore trit 2 before the next mark. All subsequent groups therefore use six inputs and produce six outputs. Even the last asserted mark has the two following unmarked input slots available by separation. This proves the finite-prefix preservation for arbitrary k and arbitrary valid continuation.

Digits 53 through 402 all start with `(v,p)=(1,0)`. Thus at *every* cut from 53 to 403 inclusive the first four marks occur in the same four positions. This fixes a part of the input on the far side of 350 digits exactly. It does not determine the later marks needed at the exceptional return.

### The first return from coordinate 12

More of the suspended tape can be recovered without knowing the number of epochs elapsed. Every valid continuation of its input must respect the three-slot mark separation and complete each outstanding burst. Starting with the known unmarked first slot at digit 411, the following prefixes are forced. Each row after the first is a consequence of the preceding row and the single-pair table.

| Zero-based cut | Guaranteed initial marks |
|---:|---|
| 411 | `0` |
| 412 | `01000` |
| 413 | `00001000` |
| 414 | `010001000` |
| 415 | `0000001000` |
| 416 | `0001000` |
| 417 | `0001000` |
| 418 | `01000000` |

There is a small exhaustive certificate for these prefixes. Track `(trit, pending, cooldown, input position, output position)`. Follow the given input prefix and then both possible bits, permitting a mark only when the cooldown and pending bit are zero. A mark resets the cooldown to two. On an unmarked slot decrease the cooldown toward zero. Each emitted letter must agree with the next specified output, stopping when the row is complete. The clause about three inputs per output bounds every branch. The initial cooldown can be set to zero to include every actual continuation. `force_prefix` performs these finite checks.

Finally use the literal machine on the six pairs beginning at index 418 and their terminal 2. At every incoming slot of that slice, supply U or C from its incoming trit, mark and pending bit. Follow the guaranteed prefix and then both valid input possibilities, just as above. Stop each path at the first right extension. `right_events` gives exactly three possible words on coordinates −1 through 11 in this enlarged set of input histories. They are `s 444040444444` with s in {0,1,4}. This enumerates possible continuations at one cut. It makes no assertion that the actual blank history realizes more than one.

On every case, 55 elementary transitions starting in B at coordinate 12 take the head to −1 in A and leave `1213031302222` in cells 0 through 12. Up to the following exit at −2 the remaining possibilities are also elementary.

| Symbol at −1 | Additional steps | Exit state at −2 | Word starting at −1 through the rightmost written cell |
|---:|---:|---|---|
| 0 | 9 | B | `30203031302222` |
| 1 | 71 | A | `120222022202122` |
| 4 | 1 | B | `21213031302222` |

The middle branch also reaches cell 13. Identifying the actual suspended tape on the left, or proving the same eventual outcome for its possible continuations, remains open. The isolated assertion that more normal epochs follow the first terminal call is false for general starting registers. For example the artificial four-digit register with trits `(1,0,0,0)` and flags clear encounters an overflow and later halts. The register with `(0,0,0,0)` and flags clear encounters an overflow and returns to a new header. Direct checks give 1,477 steps to the halt in the first example and 225 to the header in the second.

## Line 10 · an exact right-edge test

**Machine** `1RB2RB3LA4LA1LA_2LB3RA---4RA1RB`. Its only undefined instruction is B2. The public holdout table lists this exact encoding. The edge recurrence and checks below were derived from the transition table. [Status entry](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved)

| Read | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| A | 1RB | 2RB | 3LA | 4LA | 1LA |
| B | 2LB | 3RA | halt | 4RA | 1RB |

No instruction writes a blank. An occupied cell probed from the left, whose rightward calls return in A, has three ordinary states. Its transformation of a word of entering states is denoted by Tₛ for starting tape symbol s. Each table entry gives the final symbol and the complete word of calls issued rightward. All entries terminate with an A exit to the left.

| s | Input A | Input B |
|---|---|---|
| 1 | 3, B | 4, A |
| 3 | 4, ε | 1, A |
| 4 | 1, ε | 3, BB |

The rightmost occupied cell is initially 3 following each successful extension. If it receives A on three successive inputs before its first B, the first two A's change 3 to 4 to 1. The third uses A1 and calls the blank in B, leaving 2 on the edge. B0 on the blank returns left in B and the machine halts at B2. The other cases exhaust the possible first B.

| Leading inputs at the edge | What a successful extension leaves | Input to the new edge if v denotes the unused suffix |
|---|---|---|
| B | Old cell 1 followed by new cells 4,3 | T₄(T₁(v)) |
| AB | Old cell 4 followed by a new 3 | T₄(v) |
| AAB | Old cell 4 followed by new cells 4,3 | T₄(T₄(v)) |

In the first and third rows the last B reads 3 or 1 and calls the virgin cell in A. A entering two blanks takes five elementary steps, exits left in A, and leaves 43. In the middle row B4 writes 1 and sends B to the blank. B0 comes back onto 1, then B1 sends A onto the new 2. A2 and A3 finish the return, leaving 43 in the old and new cells. These paths establish both the rule and the absence of an intermediate halt. Every later call into this successfully enlarged part returns left in A until the next edge operation is invoked. The only left-moving B instruction is B0. From a new right blank its very next cell is occupied, so a second left-moving B step there is impossible. In particular the fixed negative half receives only A exits from cell 0.

From the actual blank, five moves leave 43 on cells 0,1 and A scanning −1. The negative blank half, repeatedly entered in A, answers to the right with S = `BBA(AB)` with the parenthesized part repeated forever. To verify S, follow cell −1 on each incoming A and provisionally give its requests to the left the answers S from the identical subordinate half. After requests 1 through 8 its symbols are `1,2,4,3,2,4,2,4`, and the cumulative subordinate requests are `0,0,1,2,4,5,6,7`. The emitted letters match S. After request 5 the symbol and both period phases repeat every two requests, using two subordinate answers. At every request j all subordinate calls have indices strictly below j. Strong induction on j proves that every specified answer is actually furnished in finite time.

Applying T₄ at cell 0 to S gives `BBA` followed by B forever at the initial edge, cell 1. This establishes the criterion from blank. Each ordinary cell emits on every B and on at least one of any three consecutive A's, so an infinite ordinary input has infinite output. Every finite prefix at a finite cut is computed using a finite prefix at the preceding cut. For any finite sequence of successful extensions, the corresponding probes complete in finite time by the explicit local paths. Hence the blank run halts exactly if this particular iteration encounters an edge word starting `AAA`. An infinite sequence of successful extensions would furnish an infinite concrete run.

T₄ produces a leading A precisely from the initial pair `AB`, and returns to its starting symbol 4. Thus three leading A's after this last transformation require the corresponding input to begin `ABABAB`. I tested whether the all-B tail alone could force perpetual survival. An externally supplied word starting with four B's and an A and then all B's reaches a failing edge at coordinate 49. The real word has only two B's before that A. Exact finite propagation from the real word reached coordinate 187. The first 27 virgin-cell entry states also agree with a literal blank-tape simulation. No invariant yet excludes the required alternation at every future edge.

