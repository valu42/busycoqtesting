# Line 110 and the four-one halting test

**BB(6) line 110, ID 28035, remains open.** Its table is `1RB0LB_0RC0LD_1LD1RE_0LA0RF_1RB0RD_0RB---`. The theorem `Line110.blank_iff` says that it halts from blank exactly when the visit interpreter enters a word beginning `1111`. This applies at any depth of a suspended visit. A copy of `1111` elsewhere on the tape is insufficient. [Rocq interpreter and equivalence](Line110Visits.v)

## The visit law

A visit begins in C looking at a word, with zero in the cell immediately to the left. On return, the head is in A two cells left of its entry. The guard stays zero. Write $V(u)$ for the returned word when the visit to $u$ returns, and read every word from left to right. A requested child visit that reaches F1 halts the physical machine.

| Input | Returned word or event | Defined instructions outside child visits |
|---|---|---:|
| `0` + $u$ | `1` + $u$ | 2 |
| `100` + $u$ | `000` + $V(u)$ | 6 |
| `110` + $u$ | `000` + $V(u)$ | 8 |
| `1010` + $u$ | `1010` + $V(V(u))$ | 16 |
| `1011` + $u$ | `0001` + $u$ | 14 |
| `11100` + $u$ | `000` + $V(\texttt{10}\,V(V(u)))$ | 16 |
| `11101` + $u$ | `10101` + $u$ | 18 |
| `1111` + $u$ | F reading one | 3 |

These eight prefixes exhaust every binary input. From blank, two instructions enter the first visit on the all-zero word. After each outermost return, six instructions start the next visit on `10` followed by the returned word. The saved frames in `Line110.advance` specify when each child is called and which tape cells are waiting on its left. The theorem `advance_spec` checks the elementary instruction count of every frame transition against the literal machine. Every transition makes positive progress. [Formal statements](Line110Visits.v)

The first four return rules also occur in the three machines of upstream PR 59. Those machines halt on `1011`. Line 110 returns on that word, so the witness for its relatives singles out a place where the computation can be continued. The upstream equivalence file also relates line 110 to another starting table. [Sibling checker and attribution](https://github.com/ccz181078/busycoq/pull/59) · [Existing equivalence, TM825](https://github.com/ccz181078/busycoq/blob/33209bc7dc282b38c8cd6be507bfc551fea56108/verify/Eqv_v2.v#L8368)

## Counted blank run

The Python run completed 4,096 outer visits after approximately $3.29253100\times10^{618}$ defined instructions. At return the head is at −8,190 in A reading one. The tape to its left is blank. To its right are a zero guard and a suffix with 8,906 ones, occupying 25,415 cells through its last one. The little-endian suffix digest is `81864c3d7fe9a1abd2bbae0478fe452f40fa1703c22d6de45e7d0f0a82eacf25`. The simulator prints the full clock in hexadecimal. [Batched simulator](line110_visits.py)

Every other visit to a three-cell block ending in zero enters its suffix. Each visit to a `1010` block enters its suffix twice. The simulator combines those calls with integer arithmetic and retains a pending call for `11100`. A separate literal interpreter compared whole outputs, halt outcomes and completed clocks on 1,280 guarded inputs, including 235 halts. It matched the first 24 blank returns cell for cell through 418,986 instructions. The 4,096-return clock comes from the Python calculation. [Controls](check_line110.py)

From this directory run the following.

```sh
python3 check_line110.py
python3 line110_visits.py 4096
```

## Replay the visit proof

Start in this directory with Coq 8.20.1. The six-state definition is on upstream's BB6 branch. The following uses its November 3 revision.

```sh
research_dir=$(pwd)
git clone --branch BB6 https://github.com/ccz181078/busycoq.git upstream-busycoq
git -C upstream-busycoq checkout --detach 33209bc7dc282b38c8cd6be507bfc551fea56108
cd upstream-busycoq/verify
make Makefile.coq
make -f Makefile.coq -j3 Individual62.vo
cd "$research_dir"
coqc -q -Q upstream-busycoq/verify BusyCoq -Q . BB6Research Line110Visits.v
coqchk -silent -bytecode-compiler yes -Q upstream-busycoq/verify BusyCoq -Q . BB6Research BB6Research.Line110Visits
```

Both `Print Assumptions Line110.advance_spec` and `Print Assumptions Line110.blank_iff` report `Closed under the global context`. The remaining decision is reachability of the four-one guard on the actual blank orbit.
