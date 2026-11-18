# Rocq formalization of line 36

**Line 36 runs forever from blank.** The theorem `line36_nonhalting : ~ halts line36 c0` concerns the literal machine `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---`. Here `c0` starts in state A on a two-way infinite tape filled with symbol 0. The proof establishes a positive number of elementary instructions between each pair of successive checkpoints. [Final theorem](../../verify/Line36Nonhalting.v) · [Machine definition](../../verify/Line36Machine.v) · [Mathematical argument](line36-nonhalting.md)

Rebuild from the repository root with Coq 8.20.1, GNU Make and a C++17 compiler. The six exhaustive phase checks can run in parallel.

```sh
make -C verify -j6 line36
coqtop -quiet -Q verify BusyCoq <<'EOF'
From BusyCoq Require Import Line36Nonhalting.
Check line36_nonhalting.
Print Assumptions line36_nonhalting.
EOF
```

| Kernel-checked result | Source |
|---|---|
| The literal blank machine reaches the complete 1,035-cell induction seed in 612,729 elementary transitions. The protected cut is 530 and its initial charge is 7. | [Machine](../../verify/Line36Machine.v) and [seed](../../verify/Line36Seed.v) |
| On every finite word, a successful symbolic sweep takes the original machine to the stated next checkpoint in a positive number of steps. | [Physical sweep](../../verify/Line36Physical.v) |
| Every legal finite concatenation obeys the six-phase tile identity. Every factor in the tiled region satisfies the density bound. | [Reference update](../../verify/Line36Reference.v) and [density theorem](../../verify/Line36Tiles.v) |
| If a covered cut has the proved reserve, its actual next sweep succeeds on any exterior word. The two local potential inequalities and the charge inequality preserve the required reserve. | [Safety and reserve](../../verify/Line36Safety.v) |
| Matching gives the stated charge inequality on arbitrary trailing words, including positive and zero incoming debt. | [Right-side matching](../../verify/Line36Right.v) and [cut accounting](../../verify/Line36Halo.v) |
| For all 32,064 left-state encodings, 16 possible histories and debts 0 through 28, the concrete edge exists and obeys the signed potential inequality. | [All six phases](../../verify/Line36LeftCertificate.v) |
| Every finite-debt edge admitted by the left checker reproduces the next physical tape, protected-cut position, and switch charge. For arbitrary debt of 29 or more, the protected successor follows from the tile density bound. | [Finite-debt correspondence](../../verify/Line36LowFront.v) and [unbounded-debt proof](../../verify/Line36HighBranch.v) |
| All 16,939,461 reachable 50-cell suffixes obey the right-edge potential inequality. A real successful sweep has one of the certified successor suffixes, and the terminal bit alternates. | [Certificate](../../verify/Line36CapCertificate.v) and [physical correspondence](../../verify/Line36CapInvariant.v) |

The `line36` target regenerates the right-edge potential table with `line36_right_cap.cpp`. Rocq checks every represented suffix and both possible boundary transitions against the formal word model. The checked theorem is independent of the generator's correctness.

The left-edge integer witness is explicit in [Line36LeftPotential.v](../../verify/Line36LeftPotential.v). The [generator](line36_rocq_left_potential.py) reconstructs it from the C++ enumerator. The Rocq checker evaluates transitions on actual bit lists using an independent implementation. Together the six phase checks cover 14,877,696 concrete transitions. The invariant starts at epoch 331 with credit 2,984 and reproduces itself after every successful sweep. [Blank-tape induction](../../verify/Line36Nonhalt.v)

For an independent replay of the compiled proof and its dependencies, run the standalone checker from the repository root. The bytecode option lets the checker replay the large computational equalities.

```sh
coqchk -bytecode-compiler yes -Q verify BusyCoq BusyCoq.Line36Nonhalting
```

`Print Assumptions` reports the built-in primitive integer and array types and their operations. There are no admitted lemmas or user-defined axioms in the theorem.

The independent clean build records the Coq version, the pinned source revision, and the complete output of `Print Assumptions`. [Verification transcript](line36-kernel-replay.txt)
