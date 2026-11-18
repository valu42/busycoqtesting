# BB(6) line 448 halts from blank

Line **448**, machine **127983**, reaches the undefined instruction **F1**. Its table is `1RB1RD_1LC0RE_1LD1LC_1RA0LB_0RD0RF_0LC---`. The start is state A on a two-way infinite tape of zeroes. [Frozen entry](BB6_holdouts_608.txt#L448)

## The witness

Reflect the tape and exchange A with C and B with D. E and F keep their names. Checking the twelve instructions gives the table `1RB1RA_1LC0RD_1LD1LB_1RA0LE_0LB0LF_0RA---`, starting in **C**. The arithmetic simulator for this table is part of Fractal Geometry Explorer's Coq proof for a different blank start. Its theorem `stepFast_spec` applies to **every** encoded configuration. Each successful call represents a finite sequence of elementary transitions, and a call returning `None` proves halting from its input. The engine builds on the ChaoticBell1 rules in BusyCoq PR 93. [Shared T4 proof](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0LC_1RC1RA_1LD0RE_1LA1LD_0RA0RF_0LD---/coq/H155900.v) · [Original engine and attribution](https://github.com/ccz181078/busycoq/pull/93)

| Start on the reflected table | Successful accelerated steps | Next call |
|---|---:|---|
| B, published control | 261,156 | `None`, head in F on 1 |
| C, line 448 | **427,055** | `None`, head in F on 1 |

These counts measure calls to the simulator. One call can stand for many elementary moves. The elementary runtime is undetermined here. A direct local check in the original orientation explains the last instruction. When A reads `0111`, the defined transitions A0, B1 and E1 put F on the last 1. When A reads `0110`, the machine writes `1111` and resumes in A, four cells to the right, after eight steps. Both rules hold for arbitrary tape outside the four cells. [Local sweep proofs](Line448Sweeps.v)

## Verification

The standalone file in upstream draft PR #100 contains the target table, the T4 simulator, and `Theorem halt : halts tm c0.` It imports `Individual62` and the Coq standard library. A public verification run checks the exact submitted commit with Coq 8.18.0, then passes the compiled objects to `coqchk` in a separate job. [Submitted theorem](https://github.com/valu42/busycoqtesting/blob/cdbb2630b998012b7466070118dadde9671f94ab/verify/M_1RB1RD_1LC0RE_1LD1LC_1RA0LB_0RD0RF_0LCHHH.v#L5739) · [Upstream draft](https://github.com/ccz181078/busycoq/pull/100) · [Compiler and checker logs](https://github.com/valu42/busycoqtesting/actions/runs/44398354450)

Two executions of the OCaml witness reproduced both stopping counts in the table above. The local `coqchk` accepted the shared engine, and both `stepFast_spec` and `run_pow_spec` printed `Closed under the global context`. A second upstream draft for line 448 independently reports the same terminal state and count from Python and JavaScript. [Parallel submission](https://github.com/ccz181078/busycoq/pull/101)

Fractal Geometry Explorer previously identified the C-start correspondence and reported 256,799 accelerated transitions from this start. The run above extends that trajectory to the first halt. [Earlier C-start work](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB1RD_1LC0RE_1LD1LC_1RA0LB_0RD0RF_0LC---/README.md#deepminds-engine-changed-for-this-table-18-november-2026)

## Replay

The decision theorem is `line448_halts : halts line448 c0`. Its finite certificate evaluates `run_pow 19` on the C start, with a budget of 524,288 calls and early exit on the first `None`. The theorem transports the result to line 448 using the checked reflection and renaming. [Coq proof](Line448Halt.v)

Use Coq 8.18.0, Python 3 and Git. The optional executable witness also uses OCaml, ocamlfind and Zarith. Run the following from `research/bb6`. The script copies the dependencies from the pinned BusyCoq commit and checks the SHA-256 digest of the external proof. It compiles the shared engine through its general soundness theorem. The original authors' computation for start B is a separate lemma.

```sh
git clone --branch BB6 https://github.com/ccz181078/busycoq.git busycoq-448
curl -fL -o H155900.v https://raw.githubusercontent.com/fractal-geometry-explorer/busy-beaver-explorer/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0LC_1RC1RA_1LD0RE_1LA1LD_0RA0RF_0LD---/coq/H155900.v
sh replay_line448.sh busycoq-448 H155900.v build-448-witness witness
sh replay_line448.sh busycoq-448 H155900.v build-448-proof
```

The first command invoking the replay checks both exact counts and reads the terminal cell. The second builds the decision with Coq's binary arithmetic, prints the assumptions of the theorem, and invokes `coqchk` with VM conversion enabled. [Replay script](replay_line448.sh)
