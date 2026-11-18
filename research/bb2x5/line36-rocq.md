# Rocq formalization of line 36

The development uses the repository's two-way-infinite tape semantics and the literal transition table for `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---`. The [computer-assisted nonhalting proof](line36-nonhalting.md) gives the mathematical argument and the C++ certificate checks.

Build the formalization with Coq 8.20.1 from the repository root.

```sh
make -C verify -j3 line36
```

| Kernel-checked result | Source |
|---|---|
| The literal blank machine reaches the complete 1,035-cell induction seed in 612,729 elementary transitions. The protected cut is 530 and its initial charge is 7. | [Machine](../../verify/Line36Machine.v) and [seed](../../verify/Line36Seed.v) |
| On every finite word, a successful symbolic sweep takes the original machine to the stated next checkpoint in a positive number of steps. | [Physical sweep](../../verify/Line36Physical.v) |
| Every legal finite concatenation obeys the six-phase tile identity. Every factor in the tiled region satisfies the density bound. | [Reference update](../../verify/Line36Reference.v) and [density theorem](../../verify/Line36Tiles.v) |
| If a covered cut has the proved reserve, its actual next sweep succeeds on any exterior word. The two local potential inequalities and the charge inequality preserve the required reserve. | [Safety and reserve](../../verify/Line36Safety.v) |
| Matching gives the stated charge inequality on arbitrary trailing words, including positive and zero incoming debt. | [Right-side matching](../../verify/Line36Right.v) and [cut accounting](../../verify/Line36Halo.v) |

The final blank-tape theorem requires the frontier to reproduce itself with the certified bounds after every sweep. The finite-graph replay and the correspondence between graph edges and the next physical cut are the remaining integration steps.
