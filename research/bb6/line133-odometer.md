# BB(6) line 133 from its own blank tape

**Open, ID 35069.** The machine `1RB0LC_1LC0RE_1LD1LB_1LA1LD_1RF0RA_---1RE` reaches an exceptional counter configuration with 1,802,104,644,690,770,721,432,339,129,424,760,388,912 ones. The Rocq proof reaches that configuration from blank and gives a rule that carries it past the exception. The remaining halting question is whether a later carry can reach state F reading zero. [Formal proof](Line133Odometer.v) · [Claim board](ROADMAP.md#claim-board)

## Which parts of line 581 transfer?

Fractal Geometry Explorer identified the reflection and state exchange, proved six families of periodic sweeps in Lean, and reported a run of line 133 through 7,587,642,535,440,762,669 steps. Their BusyCoq PR 76 contains the sound accelerated simulator and a halting proof for line 581, ID 172044. Its ordinary counter rule batches visits to the untouched edge of the tape when two arithmetic conditions hold. [Earlier line 133 analysis][prior] · [Line 581 proof and authorship][pr76]

Reflect the tape and exchange A with C and B with D, leaving E and F fixed. All twelve instructions match, including the undefined instruction. Line 133's A on blank thus corresponds to **C on blank** in the line 581 table. The sibling's halting theorem starts in A. The new theorem `line133_halts_iff` identifies the correct initial configuration, and `line133_jump` transfers the guarded counter rule to the original machine, preserving the untouched tail. [Source](Line133Odometer.v)

## The reachable exception

A visit here means that the original machine reaches a fresh leftmost zero in state C. As a small control, literal execution from the original table gives visit 195 at coordinate −618 after 58,272 defined steps. The ordinary counter rule reaches visit 209 at coordinate −660 after 62,084 steps. The replay checks all written cells at both endpoints. [Literal replay](replay_line133.py)

After 4,195,051 rounds of the sound simulator from the C seed, the usual counter parser cannot take a jump. Its input ends in two long runs separated by `11`, without the terminating zero it expects. Let $w=110$, and read to the right starting **after** the current head. For every pair of natural numbers $a,b$ and every further tape stream $T$, the original machine advances between the following two configurations. In both it is in C on a fresh zero with an all-zero left side.

| | Right side in physical order, nearest cell first |
|---|---|
| Input | $w^{b+2}\;11\;w^{a+1}\;10111\;T$ |
| Output | $0\;w^7\;10\;w^b\;11\;w^a\;11\;w\;T$ |

`line133_recover` proves this rewrite from the original machine instructions. `line133_blank_checkpoint` proves the blank run reaches its input with $a=404277775835677427574742439536721155021$ and $b=310982904488982636595955722720554739540$. The checked population gives a lower bound on elapsed elementary steps because each step writes at most one new one. `line133_no_early_halt` excludes halting before that bound. [Proof](Line133Odometer.v)

| At this checkpoint | Value | Verification |
|---|---:|---|
| Ones on the tape | 1802104644690770721432339129424760388912 | Rocq and both Python replays |
| Visits from blank | 901052322345385360716169564712380193709 | Visit-based replay |
| Defined elementary steps | 945179272319321718189120748709437956615538042618113699570211475257662184454913 | Two Python replays |

The two programs follow different schedules. One runs the sibling simulator for the specified number of rounds, the other advances from blank to the specified visit. Both check the state, the blank half-tape, all 248 tokens on the other half, and the same step count. They share a step-count routine for counter jumps. The round-based simulator also checks that routine against a separate dyadic sum. In the saved tape, an integer means that many copies of `011` and a string gives literal cells, in the reflected machine's far-to-near order. [Full checkpoint](line133-checkpoint.json) · [Replay](replay_line133.py)

**Next proof obligation.** At this checkpoint the recovery takes five visits. A further 14 visits leave eight separator bits all equal to one. On the very next visit the carry crosses the next `11101` marker and returns with eleven bits, a one followed by ten zeros in the parser's order. Prove how such a carry passes an arbitrary number of levels, including the condition under which it enters F0. The marker and the exact before-and-after prefixes are checked by the replay. [Replay](replay_line133.py)

## Reproduce

From this directory, Python 3 can check the small prefix from the frozen register alone. Pass a checkout of the pinned accelerator to run both long replays and check the continuation through the eight-bit carry.

```sh
python3 replay_line133.py
git clone --filter=blob:none --no-checkout https://github.com/fractal-geometry-explorer/busy-beaver-explorer.git /tmp/explorer-line133
git -C /tmp/explorer-line133 sparse-checkout set tools/py holdouts/1RB1RD_1RC1RB_1LD0RA_1RA0LE_1LF0LC_---1LE/py
git -C /tmp/explorer-line133 checkout --detach c409c4b292369cb404e939753004bd1216fa3333
python3 replay_line133.py /tmp/explorer-line133
```

The formal proof uses Coq 8.20.1 and the pinned six-state BusyCoq library and odometer from PR 76. On November 18, 2026, all five printed theorems reported `Closed under the global context`, and recursive `coqchk` exited successfully. The commands below build the full sibling proof first. The bytecode option enables kernel checking of the VM computations.

```sh
git clone --filter=blob:none --no-checkout https://github.com/fractal-geometry-explorer/busycoq.git /tmp/busycoq-line133
git -C /tmp/busycoq-line133 checkout --detach 594cece3de0a12e514abd58b270f5df3551c87bc
odometer_verify=/tmp/busycoq-line133/verify
(
  set -e
  cd "$odometer_verify"
  for module in LibTactics Helper Eqb HashTable TM Compute Flip DirectedCompute Permute Pigeonhole Enumerate Individual BB62 Individual62 M_1RB1RD_1RC1RB_1LD0RA_1RA0LE_1LF0LC_HHH1LE
  do
    coqc -q -native-compiler no -Q . BusyCoq "$module.v"
  done
)
coqc -q -native-compiler no -Q "$odometer_verify" BusyCoq Line133Odometer.v
coqchk -silent -bytecode-compiler yes -Q "$odometer_verify" BusyCoq Line133Odometer
```

[prior]: https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0LC_1LC0RE_1LD1LB_1LA1LD_1RF0RA_---1RE/README.md
[pr76]: https://github.com/ccz181078/busycoq/pull/76
