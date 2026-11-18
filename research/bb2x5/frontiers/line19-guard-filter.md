# Four cells after the line 19/23 guard

Use line 19's orientation and transition table on both blank seeds. Reflection
takes line 23's blank A seed to line 19's blank B seed. At a guard launch the
head reads the first zero in `03U` in A. The particular halt at the original 3
requires the suffix U to answer the three requests B, B, A with A, A, A.
[Tape reflection and guard traces](line19-pair.md)

Only **16 of the 81** four-letter words over the right-hand alphabet
`{0,2,3}` survive the window invariant below as initial prefixes of U.
Three of those 16 exclude the required reply sequence for *every* suffix
continuation.

| Effect at this guard | Four-cell prefixes of U allowed by the window invariant |
|---|---|
| Cannot give three A replies | `0222`, `3000`, `3202` |
| Four cells permit three A replies under some choice of boundary answers | `0202`, `0230`, `0233`, `3020`, `3022`, `3023`, `3222`, `3230`, `3232`, `3233`, `3302`, `3330`, `3333` |

The second row is an outer bound on blank reachability. A real continuation
must produce its own sequence of boundary answers. An excluded halt at the
original 3 still leaves open the possibility of a halt deeper in U.
A [splice of two normalized line-23 tapes](line23-splice.md) tests how
much of the actual tape a reachability argument must retain.

Through $10^{11}$ defined steps, 27,016 of 58,548 line-19 launches had one
of the three excluded prefixes. On line 23, all 58,488 launches fell into
the excluded set. Of those, 2,230 began `0222` and 56,258 began `3202`. This counts
the observed launch tapes on the two blank trajectories.
[Line 19 run](runs/spaghetti-19.json) · [Line 23 run](runs/spaghetti-23.json)

## Three direct strip checks

The first B call on `0222` takes one local instruction and returns A with
`2222`. On `3202` the same result takes five local instructions. The remaining
calls on `2222` issue one B request to the right of the strip. On `3000`, the
first call already returns B.

| Original strip | Reply from the continuation to its one B request | Outer replies up to first B | Final strip |
|---|---|---|---|
| `0222` or `3202` | A | AAB | `2322` |
| `0222` or `3202` | B | AB | `2020` |
| `3000` | No request | B | `2320` |

If the continuation never returns, the guard cannot complete the reply
sequence. The checker also explores all finite strip states, granting either
answer to each outgoing request, to classify the other 13 prefixes.

## Why the window filter holds on the infinite tape

A head window stores three symbols to the left, the control state and
scanned symbol, and five symbols to the right. Each side is ordered from the
head outwards. The certificate also stores possible three-cell words strictly
to the left and five-cell words strictly to the right, at *every* distance.
The two blank initial head windows and the all-zero word of each width seed
the construction.

For a right move, the written symbol becomes the nearest left symbol.
Prepend it to the old left word and truncate to three cells. The first old
right symbol becomes the scanned symbol. The other four old right symbols
begin the new right word. Include every completion to five cells present
in the right-word set, and add the new three-cell left word to its side set.
A left move interchanges these roles, using each side's own width. Repeat
until none of the three finite sets grows.

For the induction, the entire blank tape satisfies the two side-word
constraints initially. On each physical step, the new word nearest the head
on the pushed side is the only side word that can be new. Every other side
word was already on its corresponding side, including the word exposed by
popping the opposite side. Its actual completion was therefore included.
This proves membership of the next physical window regardless of how far
the head has travelled. An undefined instruction has no successor.

At closure there are 13,720 head windows, 50 distinct left words and 94
distinct right words. An independent checker constructs physical tapes for
every stored head window, tries each of the five possible exterior symbols,
and executes one literal TM step. It checks the pushed word and, for every
permitted pop, the successor window. Filtering this closed set at `A:03U`
gives the 16 four-cell prefixes above. The strip tests also replay both
possible child answers instruction by instruction.

Run from `research/bb2x5`.

```sh
python3 frontiers/line19_guard_filter.py
python3 frontiers/test_line19_guard_filter.py
```

## A narrower launch filter for line 23

The normalized line-19 machine on the B seed represents line 23 from blank A by reflection and relabeling. Keeping four cells on the left and five on the right in the same closure excludes two additional four-cell launch prefixes, `3000` and `3232`, from the combined 16-prefix list. The resulting 14 classes apply to every physical B-seed launch, including future ones. Among them, `0222` and `3202` exclude the three A replies by the strip calculation above.

| Left cells | Right cells | Closed head windows | Left side words | Right side words |
|---:|---:|---:|---:|---:|
| 4 | 5 | 28,492 | 148 | 80 |
| 4 | 8 | 189,076 | 148 | 543 |

The wider check gives the same four-cell classes. One of them, `3233`, admits a concrete halting configuration even under this stronger local constraint. Put `03323320202022` at coordinates 0 through 13 of an otherwise blank tape, with A scanning the initial zero. Its head window belongs to the second closure, as do every four-cell word on its left and every eight-cell word on its right. Its guard sends B, B, A to coordinate 2. All three requests return A, at steps 49, 55 and 147. At step 149 the machine scans the undefined A3 at coordinate 1. Its furthest visit is coordinate 15.

Determining whether a blank launch can take this path requires additional reachability information. To reproduce both closure checks and the complete auxiliary trace, run `python3 frontiers/check_line23_launch.py` from `research/bb2x5`.
