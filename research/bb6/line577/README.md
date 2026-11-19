# BB(6) line 577, bbchallenge ID 168919

The machine is `1RB0LD_1LC1RE_1LA1RC_1RA0LC_0RF---_0LD1RB`, started in A on an all-zero tape. The pinned ranking places it at rank 149 and holdout line 577. The only missing transition is E reading 1. [Pinned rankings](https://github.com/valu42/busycoqtesting/blob/175f2c272c1d5dfd1ff16f277839f19877cb2364/research/bb6/RANKINGS.md#L217)

The blank run executes at least **86597105634550683242220399832625532065265089196529793180480570975610884882393403647014563450505554078284888955574375286937328747915272052514346715229369099735730293270875253729127481455956835** transitions. The run is open at this checkpoint. After 1,000,000 replay commands the compressed configuration has SHA-256 `f2dbf8f9632b8de0c010723421b5ce84051f89ad153284c62cea09156c3a2de3`.

## Prior work

Google DeepMind proved non-halting of `1RB1RE_1LC1RB_1RA0LD_1RC0LB_0RF---_0LD1RA` from **state A**. Its 46-chunk Lean certificate ends in a translating glider. Fractal Geometry Explorer subsequently proved that the **state C** blank run of that table has the same halting outcome as line 577. Its machine ledger reports 53,075,697,817,764,149,403 elementary transitions without a halt on line 577. The search here starts the reference in C. All digit words and the 133 local shortcuts used as templates are due to DeepMind. [DeepMind certificate](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/NonHalt/M_1RB1RE_1LC1RB_1RA0LD_1RC0LB_0RFHHH_0LD1RA.lean) · [Published equivalence](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/db0bcfce198c2958a29d80a6d79de91575869de8/holdouts/1RB0LD_1LC1RE_1LA1RC_1RA0LC_0RF---_0LD1RB/lean/SyncDM.lean) · [Earlier run and local lemmas](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/3c7d4736362e77b987beb5c043056b24994b5a60/holdouts/1RB0LD_1LC1RE_1LA1RC_1RA0LC_0RF---_0LD1RB/README.md)

## Why the clock belongs to line 577

Reflecting the reference tape reverses its directions and preserves the clock. Undo that reflection and rename the reference states A, B, C, D, E, F to B, C, A, D, E, F. This gives exactly line 577 except at B0. From synchronized configurations, every transition except B0 agrees. B is entered only by writing 1 and moving right, so the cell immediately to its left contains 1. In B0 the reference writes 1 and moves right into C. Line 577 writes 1 and moves left into C, reads the old 1 and moves right, then reads the newly written 1 and moves right into C. The head, state and entire tape now agree. This replaces one transition by three. Induction from the two blank starts gives the exact clock

```text
line 577 transitions = reference transitions + 2 × occurrences of reference A0.
```

A0 denotes the instruction before the state renaming. Each reported clock counts defined transitions. The next lookup is the first instruction still to execute.

## Replay from the transition table

The program stores each half of the tape as words with integer repetition counts, nearest cell first, followed by infinitely many zeros. Changing the representation of the scanned side moves its first bit between these two lists and preserves the physical configuration. A single transition serves as the fallback when no shortcut applies.

1. The program extracts 118 local rewrites and 15 scans from the hash-pinned Lean file. It executes every proposed rule one elementary transition at a time on its finite input words, checks the exact output and refuses any read outside those words. This proves the rule for arbitrary surrounding tape. One scan returns to its own state with the same finite context, so induction permits any specified number of repetitions.
2. For the longer sweeps, `line577_rules.py` similarly checks the wall word, the 22 digit phases and the reset at the outer end. A call starts in D facing right with left prefix `010101010`. A normal return enters A facing left with right prefix `101111`, exposing the original left tail. When a phase forwards a call to the unknown right suffix, the checker stops at the specified entry boundary, substitutes its return contract once, and continues ordinary transitions. It checks both boundaries. The finite prefix never reads an unspecified cell. This is the substitution rule in the DeepMind proof. Composing it from the innermost returning call outwards proves each complete sweep.
3. Write the right tape at a sweep boundary as leading walls followed by digit/gap pairs and an arbitrary suffix. A digit receiving one call changes to its next phase and, according to that phase, consumes a wall on its right, produces a wall on its left, or forwards a call. The code sums these changes over full phase cycles and a remainder. It checks that each digit has enough walls for *all* its consumptions before crediting walls emitted by the next digit. It also requires zero calls to reach the arbitrary suffix. These conditions justify each batch by induction on the digit list and the call count. The order in which the search tries parsings only affects the choice of a verified move.
4. For the clock, charge each outer call its finite reset, each visited digit its checked local cost, and each crossed wall one wall-call cost. A gap initially containing `n` walls contributes `n` to each forwarded call, less all walls consumed up to that call. Walls emitted into that gap by the next digit contribute on its *subsequent* calls. The two prefix sums in `batch_clocks` compute precisely these adjustments. Prior complete periods contribute an arithmetic series. Both the ordinary and B0-adjusted clocks use the same number of wall visits. A wall costs 44 ordinary moves or 48 adjusted moves. A reset costs 31 or 35.
5. The terminal checks are the undefined E1 and the 125-transition glider. The glider checker executes one full period on a finite window, treating the left tail as arbitrary. It verifies the head moves right by one, a 1 is added behind it, and the fixed words are restored. Induction gives non-halting from any phase that matches the verified template.

## Independent controls

The C++ program reads the original twelve-entry ranking table and executes exactly one transition per loop. It compares the state and **both complete head-relative half-tapes**, trimming only the infinite blank ends. Six comparisons from the blank start passed. The reflected reference was also run independently to all six corresponding clocks.

| Replay commands | Reference moves | Line 577 moves |
|---:|---:|---:|
| 2,000 | 6,728 | 7,358 |
| 4,000 | 223,612 | 244,022 |
| 6,000 | 2,065,300 | 2,253,300 |
| 8,000 | 36,824,203 | 40,173,473 |
| 10,000 | 760,280,971 | 829,403,221 |
| 12,000 | 9,197,172,813 | 10,033,289,389 |

As a positive control, the state-A run entered the published glider after 288,318 search commands, at ordinary reference step `941824413590159858688296554836156508784476939723263856`. Returning to the C start changes the trajectory.

## Reproduce

Run from the directory containing the two Python files. The only dependency beyond Python 3.10 or later is the pinned text file. The C++ control requires a C++17 compiler. Leave assertions enabled.

```sh
source_file=M_1RB1RE_1LC1RB_1RA0LD_1RC0LB_0RFHHH_0LD1RA.lean
curl -fsSLo "$source_file" "https://raw.githubusercontent.com/google-deepmind/cryptids/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/NonHalt/$source_file"
python3 line577_replay.py "$source_file" --commands 1000000 --dump checkpoint.json
python3 line577_replay.py "$source_file" --state A --commands 300000
python3 line577_replay.py "$source_file" --commands 12000 --literal-checkpoints controls.txt
c++ -O3 -std=c++17 line577_literal.cpp -o line577_literal
./line577_literal original < controls.txt
./line577_literal reflected < controls.txt
```

The input file's SHA-256 is `68c78d084149e072cd1aecfb68cab24154554ed84ad1cffb26f77df1d5d4fd53`.
