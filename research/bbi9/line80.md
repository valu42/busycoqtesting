# BBi(9), six states and three symbols, line 80

**NONHALTS.** The machine below runs forever from state A on a two-way tape filled with zeroes. Andrew McKnight's November 16, 2026 holdout release lists it at line 80 in the six-state, three-symbol file and at line 37,628 in the full list. [Six-state source row](https://github.com/amcknight/beavers/blob/b488e67c6237bbb74f91c9a8076c31d5a9e5b961/bbi9/by_cell/BBi9_6x3_holdouts_81.txt#L80) · [Full list](https://github.com/amcknight/beavers/blob/b488e67c6237bbb74f91c9a8076c31d5a9e5b961/bbi9/BBi9_holdouts_37666_unofficial_2026-11-16.txt#L37628)

```text
1RB---2LF_2LC------_---2LD---_0LE---0LD_2RE---2RA_------0RE
```

An instruction writes a symbol, moves one cell and enters the indicated state. A dash in the table means the machine would halt.

| State | Read 0 | Read 1 | Read 2 |
|---|---|---|---|
| A | 1RB | — | 2LF |
| B | 2LC | — | — |
| C | — | 2LD | — |
| D | 0LE | — | 0LD |
| E | 2RE | — | 2RA |
| F | — | — | 0RE |

## Proof by returning to a pair of zeroes

Number the tape cells by integers and start at cell 0. Group cells into the fixed pairs $(2j,2j+1)$. A **checkpoint** has finite nonzero support and satisfies three conditions.

- The machine is in state A on the first cell of a `00` pair.
- Every pair strictly to its left is `00`, `02` or `22`.
- Every pair strictly to its right is `00` or `22`.

The blank start is a checkpoint. We show that every checkpoint reaches another in a positive, finite number of defined elementary steps.

Let the head be at $h$. The three instructions A0, B0 and C1 turn the pair at $h,h+1$ into `22` and place D at $h-1$. Moving left, D2 erases all consecutive `22` pairs immediately to the left. There is a first different pair because the tape has finite nonzero support. Write $b$ for its even, leftmost cell. There are two cases.

1. **The pair at $b$ is `00`.** D sees its right zero and steps left into E at $b$. E0 fills zeroes with twos moving right, through the erased pairs up to $h-1$. E2 at $h$ then puts A at $h+1$.
2. **The pair at $b$ is `02`.** D2 erases the right two. D0 on its left zero puts E at $b-1$. If that cell contains a two, E2 leaves it unchanged and puts A at $b$. The head is on a `00` pair, all erased pairs to its right are `00`, and the pair at $h$ is `22`. This is already a checkpoint. If $b-1$ contains a zero, its pair was `00` because the only allowed left pair ending in zero is `00`. E0 changes that pair to `02` and fills the zeroes from $b$ through $h-1$. E2 at $h$ puts A at $h+1$.

It remains to handle the common exit at $h+1$. The head and its left neighbor both contain two. Whenever A is on a two with a two immediately to its left, **A2, F2, E2** move the head right by one in state A, erase the former left neighbor and preserve the former head cell. Thus the same three instructions work again if the next symbol is two.

Let $z$ be the start of the first `00` pair strictly to the right of $h$. Such a pair exists, and all intervening pairs are `22`. The three-instruction move repeats until A reaches $z$. It erases exactly the cells $h$ through $z-2$, leaving the two at $z-1$. The pairs in $[h,z)$ are therefore zero or more `00` pairs followed by one `02` pair, with the head on the next `00`. Earlier pairs satisfy the left condition by the two cases above. The untouched right pairs satisfy the right condition.

Both exits recreate a checkpoint after at least the initial three instructions. Each scan is finite and preserves finite support. Induction gives a defined run of at least $3n$ steps for every natural $n$. Hence the blank run never halts.

## Independent elementary-step certificate

A second proof checks a different invariant after **each** instruction. It records the state, the parity of the head position and the five symbols centered on the head. It also restricts adjacent pairs on each side of the head by their position parity. The certificate admits 73 head contexts. Starting from the all-zero tape, all 116 possible one-step extensions preserve the invariant, and none of the contexts reads an undefined instruction. [Python checker and complete certificate](line80.py)

The SMT version uses an array indexed by mathematical integers for the tape. Z3 checks initialization, existence of a defined instruction, preservation of the head window separately on right and left moves, and preservation of the pair condition at an arbitrary integer position. Excluding counterexamples to all five obligations establishes the invariant on the unbounded tape by induction. [SMT-LIB certificate](line80.smt2)

Run either check from this directory.

```sh
python3 line80.py
z3 line80.smt2
```

Python reports 73 contexts and 116 extensions. Z3 4.13.3 returns `unsat` five times.

## Prior-art check

On November 19, 2026, the published BBi(9) release listed this exact table as undecided. Its earlier six-state, three-symbol file also retained it after incorporating other researchers' results. I tested all 480 ways to rename the five noninitial states, exchange the two nonblank symbols and reflect the tape. Exactly one of the 37,666 released entries matched. The release's merged-and-dropped ledger contains no matching table. [Release methodology and caveats](https://github.com/amcknight/beavers/blob/b488e67c6237bbb74f91c9a8076c31d5a9e5b961/bbi9/README.md) · [Earlier filtered list, line 82](https://github.com/amcknight/beavers/blob/b488e67c6237bbb74f91c9a8076c31d5a9e5b961/bbi/bbi9/cells/6x3/BBi9_6x3_holdouts_after_lists_unofficial.txt#L82) · [Ledger](https://github.com/amcknight/beavers/blob/b488e67c6237bbb74f91c9a8076c31d5a9e5b961/bbi9/merged_and_dropped.tsv)

I found no earlier public decision in the reporting repository's issues or pull requests, in the BusyCoq fork's existing pull requests, or in public GitHub and web searches for the exact table and distinctive transition groups. The first 14 elementary instructions from blank use all nine defined entries. Deleting any one makes the machine halt when it first reaches that entry. Private and unindexed work remains outside this priority check. [Reporting repository](https://github.com/amcknight/beavers) · [Community holdout index](https://wiki.bbchallenge.org/wiki/Holdouts_lists#Instruction-limited_Busy_Beaver)
