# Line 173 runs forever from blank

The October 30 register identifies line 173 as ID 45924, `1RB0LE_1RC1RE_0RD1RC_1LA0LB_1LF0RB_---1LD`. The merged BusyCoq theorem `FIBv7.TM3.nonhalt` already proves its nonhalting. This entry records an independent replay on November 18, 2026. [Upstream proof at revision 33209bc](https://github.com/ccz181078/busycoq/blob/33209bc7dc282b38c8cd6be507bfc551fea56108/verify/FIBv7.v#L2678) · [Literal table used for the replay](Line173Identity.v)

From blank A the machine reaches a checkpoint with a single run of nine ones. The upstream return lemma covers every positive odd run length. Each returns to another positive odd run in at least one elementary step. Induction supplies arbitrarily many steps from the blank seed. [Blank entry](https://github.com/ccz181078/busycoq/blob/33209bc7dc282b38c8cd6be507bfc551fea56108/verify/FIBv7.v#L97) · [Odd-run return](https://github.com/ccz181078/busycoq/blob/33209bc7dc282b38c8cd6be507bfc551fea56108/verify/FIBv7.v#L2650)

## Reproduce the check

Start in this repository's `research/bb6` directory with Coq 8.20.1 and GNU Make. The replay file spells out the twelve instructions directly. Applying the upstream theorem to it checks the table by definitional equality and uses BusyCoq's own blank configuration.

```sh
replay_dir=$(pwd)
git clone --branch BB6 https://github.com/ccz181078/busycoq.git upstream-busycoq
git -C upstream-busycoq checkout --detach 33209bc7dc282b38c8cd6be507bfc551fea56108
cd upstream-busycoq/verify
make Makefile.coq
make -f Makefile.coq -j3 Individual62.vo ES_v3.vo Longitudinal.vo
coqc -q -Q . BusyCoq FIBv7.v
coqchk -silent -bytecode-compiler yes -Q . BusyCoq BusyCoq.FIBv7
cp "$replay_dir/Line173Identity.v" .
coqc -q -Q . BusyCoq Line173Identity.v
coqchk -silent -bytecode-compiler yes -Q . BusyCoq BusyCoq.Line173Identity
```

Both kernel replays passed on Coq 8.20.1 with OCaml 5.3.0. `Print Assumptions literal_nonhalt` reports the standard dependent functional extensionality axiom, `FunctionalExtensionality.functional_extensionality_dep`.
