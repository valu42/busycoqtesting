# The physical sweep for holdout 36

Consider `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---`. At an epoch, A reads the blank immediately to the left of a finite word $w$ over `1,2`, with blank exterior. This includes the completely blank starting tape. Interpret `1` as an opening and `2` as a closing. Let $d$ be minus the minimum signed height of a prefix, including the empty prefix. If $d\ge6$, the machine reaches its undefined instruction B4 in finite time. Otherwise it reaches a new epoch in positive finite time, with exactly the word given below.

| Scanned symbol | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| A | 1RB | 2LA | 1LA | 4RA | 2LA |
| B | 0LA | 3RB | 3LB | 2RB | halt |

## Outward matching

A0 writes a guard `1` and sends B to the first unread digit. When B is at the next unread digit, the processed source cells are `3` at the unmatched openings and `2` everywhere else. B1 marks a new opening `3` and steps right. On a closing, B2 writes `3` and moves left. It crosses the contiguous run of previously processed `2`s, changing each to `3`. If it then reads a marked opening, B3 changes it to `2` and turns right. B3 restores every crossed cell and the closing itself to `2`, reaching the next unread digit. This matches the nearest still unmatched opening.

When no opening remains, this scan reaches the guard. On the first use, B1 writes `3` and turns right. On the second use, B3 writes `2` and turns right. Each turn restores all crossed cells to `2`. The number of times the guard is needed is the number of new strict prefix-height minima, namely $d$, unless the machine has already halted.

On the third use, B2 also crosses the spent guard, writing `3`. Let $z$ be the blank immediately left of this guard. Now B scans $z$, the half-line strictly to its left is blank, and the old guard and all processed source cells through the current closing are `3`. The following are all visits to $z$ during the local reset. The word column runs from the leftmost nonblank through $z-1$. At these visits $z$ itself is still blank.

| Steps from first reaching $z$ | State | Word |
|---:|:---:|:---|
| 0 | B | empty |
| 2 | B | `1` |
| 8 | B | `32` |
| 22 | B | `222` |
| 30 | B | `1333` |
| 32 | A | `1334` |

The table follows by substituting the ten instructions above. The intermediate excursions stay left of $z$. The final A0 writes a new guard `1` at $z$ and sends B to $z+1$. B3 crosses the former guard and all processed cells, restoring every one to `2`. Thus the reset introduces the wall `1334`, followed by a fresh guard and the former guard `2`. All source cells seen so far have now been matched or were unmatched closings. Their correct marks are all `2`. The next two guard uses again change the new guard from `1` to `3` to `2`. On the sixth use B crosses this `2`, moves directly onto the terminal `4` of the wall, and halts. Before that use the outward head never reads the wall.

## Return and headers

At the right-edge blank B0 leaves it blank and sends A left. Let $v$ be the raw processed row, including all guards and any wall. Consider the descent along $v$ from right to left. A1 and A4 write `2` and step left, and A2 writes `1` and steps left. A3 temporarily writes `4` and steps right in A. An already processed right neighbor is `1` or `2`. A toggles it and returns left onto the temporary `4`, where A4 writes `2` and steps left. If this `3` is rightmost, the excursion onto two virgin blanks uses A0, B0 and A1, leaving one additional `2` on the right before the same A4 return.

Therefore define $f(2)=1$ and $f(1)=f(3)=f(4)=2$. The output at position $i$ is $f(v_i)$, toggled between `1` and `2` exactly when $i>0$ and $v_{i-1}=3$. Append a final `2` iff the last symbol of $v$ is `3`. In particular, in the old source cells let $s_i$ indicate that position $i$ is an unmatched opening in the full word. Each output there is `2` exactly when $s_i\ne s_{i-1}$, otherwise `1`. The previous bit for the first source cell is given by the header.

| $d$ | Raw header in $v$ | Emitted header | Previous bit for source |
|---:|:---|:---|---:|
| 0 | `1` | `2` | 0 |
| 1 | `3` | `2` | 1 |
| 2 | `2` | `1` | 0 |
| 3 | `133412` | `221121` | 0 |
| 4 | `133432` | `221122` | 0 |
| 5 | `133422` | `221111` | 0 |

In the last three rows the sixth symbol is the former guard. The empty input gives the single-symbol word `2`. For a nonempty input a right append occurs exactly when its final digit is a surviving opening. Once the leftmost raw cell has been processed, A stands on the blank immediately to its left. The resulting contiguous word over `1,2` has blank exterior. This is the first later epoch. The ordinary outward search stays in B, the brief A visits in the reset leave the old run of `3`s untouched, and the right-edge A0 excursion lies to the right of the occupied tape. Each outward iteration consumes one source digit after traversing a finite interval, and at most one 33-step local reset occurs. Each return iteration processes one raw cell with at most five elementary transitions. Thus arbitrarily many successful finite word sweeps imply infinitely many defined machine steps.

The [physical sweep checker](line36_physical.py) replays the reset and all 8,191 input words through length 12 against the literal interpreter.
