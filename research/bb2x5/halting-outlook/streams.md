# Lines 13, 21 and 22: fresh-cell triggers and the actual input streams

Research pass: **2026-11-18**. Starting repository commit:
`2ab106f706cb1715d494c7f67464e9222092058f`.

| Line | Full machine string | Outlook after this pass |
|---:|---|---|
| 13 | `1RB3RA3RB4LA1LA_1LB2LA1LA---1RB` | **Possible halting**; no justified numerical stopping distribution |
| 21 | `1RB2RA3LA4LA2RB_2LA3RB---0RA1LA` | **Unknown** |
| 22 | `1RB2RA3LA4LA2RB_2LA3RA---0RA1LA` | **Unknown** |

## Later line 13 checkpoint

The current repository proves that a blank halt requires a first A after a positive even initial B-run at an **odd** coordinate. Through 10¹⁷ source groups, 75 odd cells began BA, and cells 91 and 97 began BBBA. All 77 are permanently clear. Cell 155 had received just B. The exact raw clock was 150,000,000,000,000,003,612,281,246,951,610,338. The two longer runs demonstrate why marginal letter counts or independent parity guesses cannot predict the first failure. Control inputs do reach the local halting rule. The blank-source parity beyond the checkpoint remains open. [Proof, full trace and replay command](../line13-edge.md)

The remaining experiments and checkpoints in this report belong to the [earlier outlook pass](https://github.com/valu42/busycoqtesting/commit/680c69635d58a26ad2d33814ac16df4f72a86975).

## Baseline and attribution

The current [community holdout page](https://wiki.bbchallenge.org/w/index.php?title=BB(2,5)&oldid=10980)
(last edited 2026-11-17; read 2026-11-18) matches all three **complete strings**.
It attributes a potentially halting longitudinal analysis of line 13 to dyuan,
and a simulation to about `10^17.50888` steps to Andrew Ducharme. It describes
21/22 as chaotic under longitudinal analysis and links mxdys's notes for 22.
The linked [line-13 discussion](https://discord.com/channels/960643023006490684/1349602897024782358)
and [line-22 notes](https://discord.com/channels/960643023006490684/1259770421046411285/1436149296004071615)
returned only Discord's JavaScript shell during this pass. Their contents were
**not** independently inspected; attribution here is to the public wiki summary.

Inherited repository results are the [certified left-half streams and line-21/22
criterion](../mixed-and-sweeps.md#2-two-machines-with-the-same-exact-blank-half-input),
the [timed boundary-stream simulator](../frontiers/README.md#exact-batches-of-boundary-crossings),
and its [literal-comparison tests](../frontiers/test_longitudinal.py). The negative
half answers with `(BABAB)^omega` on line 13 and
`(BAABABABAAABA)^omega` on 21/22. Cell 0 receives A followed by that stream.
The first-string characters and source phase must be retained: arbitrary factors
of a periodic representative cannot replace the distinguished initial position.

Inherited exact raw endpoints are:

| Line | Raw steps survived | Source periods completed | Positive cells visited |
|---:|---:|---:|---:|
| 13 | 6,000,000,000,000,000,722,456,249,389,064,786 | 20,000,000,000,000,000 | 150 |
| 21 | 520,000,000,021,075,314,101,532 | 100,000,000,000 | 218 |
| 22 | 520,000,000,017,608,277,588,346 | 100,000,000,000 | 194 |

The files are [13](../frontiers/runs/stream-13.json),
[21](../frontiers/runs/stream-21.json), and
[22](../frontiers/runs/stream-22.json). These are survival certificates, not
estimates of eventual halting. None is a formally verified halting decision.

## Line 13

The [paired input and period proof](pair13.md) rules out a permanently closed frontier. The [new clock bound](timing13.md) gives a deadline for the current test.

**New established result: the exact fresh-cell trigger.**

Call an entry into a cell from its left A or B according to the control state.
All successful returns from an already visited right neighbor are in A. A virgin
neighbor's first A entry returns A; its first B entry is simply B0 and returns B.
These return contracts are inherited and are checked by the repository's finite
`check_return_contract` computation. A divergent call is not a successful return.

For a fresh cell, its first B writes 1 and exits left in B. Subsequent B entries
toggle `1 -> 2 -> 1 -> 2 -> ...`, each exiting left in A and making no child call.
Consequently, before the first A the symbol is 1 after an odd positive number of
B entries and 2 after an even positive number.

* If the cell first receives A on blank, A0 calls its virgin neighbor in B. B0
  returns B, and B1 exits left in A, leaving 2. The neighbor has now been visited.
* If the first A follows an odd number of B entries, A1 calls the virgin neighbor
  in A. Its A return executes A3, leaving 4 and exiting left in A. Again the
  neighbor has been visited.
* If the first A follows a positive even number of B entries, A2 writes 3 and
  calls its virgin neighbor in B. That neighbor executes B0 and returns in B.
  The original cell is now at **B3**, the undefined instruction. Exactly **two
  defined raw instructions** separate that A entry from the halt.

After either successful initialization, the cell has symbol 1, 2 or 4 at its
returned boundaries and the child is no longer virgin. Its ordinary table is:

| Symbol | Input A: new symbol / child calls | Input B: new symbol / child calls |
|---:|---|---|
| 1 | 4 / A | 2 / empty |
| 2 | 4 / B | 1 / empty |
| 4 | 1 / empty | 4 / BA |

All child returns used in this table are A; it contains no internal halt. Thus
the **only** local trigger is the input prefix `BB(BB)*A`: the first A follows
2, 4, 6, ... B entries. An infinite initial sequence of B entries never triggers
it. This is a direct transition-table argument, **not a Rocq/Lean proof**.

Together with the inherited safe negative driver this gives a blank-orbit
criterion: some actual fresh nonnegative cell must receive that prefix. An
offending prefix does not depend on a hypothetical later child return: all prior
B entries issue no child calls and the decisive virgin B call immediately
returns. Therefore the terminal two-step path cannot be hidden behind an
uncompleted deeper excursion. This avoids turning an allowed but unrealizable
path into a blank-tape result.

The fresh-cell first-entry letters alternate A, B, A, B, ... while these entries
are safely initialized: a fresh A emits B first, and a fresh B with an odd
initial B run emits A first. The vulnerable first-B cells are therefore already
a special subsequence. Their run lengths are not independent samples from the
body of a stream.

## Lines 21 and 22

The [current upstream test](target21_22.md) identifies four dangerous parent prefixes for line 21 and one for line 22. It compares their starting positions with occurrences inside the actual streams.

**The inherited exact trigger remains open.**

The inherited one-cell table gives `B0 -> 2` with no right call. A second B at
that fresh cell immediately encounters B2. Every other completed initialization
enters the closed ordinary alphabet `{1,3,4}`. Hence the blank run halts exactly
when a fresh nonnegative cell's **first two entries are BB**. The second entry
itself takes zero defined instructions before the undefined transition is seen.

This is an opportunity at each new cell, not on each occurrence of BB later in
an initialized cell. Actual future input streams are successive images of one
specific periodic source, retaining their transient prefixes. The baseline
already shows that independently choosing length-10 factors creates a spurious
BB path. This pass does not promote that enlarged language to actual reachability.

## New experiments on actual blank execution

[`streams-analyze.cpp`](streams-analyze.cpp) includes the unchanged existing
finite-stream transducer and instruments each cell's actual finite input. It
counts entries, B letters and adjacent BB pairs exactly in the representation
`prefix + period^copies + suffix`; it retains the first 128 entries at each cut.
[`streams-investigate.py`](streams-investigate.py) merges consecutive batches,
including BB pairs crossing batch boundaries, reconstructs the raw clock and
stores the complete positive tape and a reconstructible negative half.

| Line | Newly analyzed endpoint | Raw instructions | Positive cells | Result |
|---:|---:|---:|---:|---|
| 13 | `q = 10^14` source periods | 150,000,000,000,003,612,281,246,906,468 | 128 | Earlier than inherited endpoint; adds exact stream statistics |
| 21 | `q = 2*10^11` | 2,080,000,000,042,150,626,016,264 | 225 | New exact survival endpoint |
| 22 | `q = 2*10^11` | 2,080,000,000,035,216,556,130,952 | 203 | New exact survival endpoint |

Full results and checkpoints: [13](streams-13.json), [21](streams-21.json),
[22](streams-22.json). The record stores source-group boundaries as well as
per-cut counts. Neither extended machine halted. The original simulation table
and all its checkpoint files remain untouched.

On line 13, 64 sampled fresh cells first received A. The other 64 first received
B: 62 currently have an initial run of length one, and cells **91 and 97** have
completed initial runs of length three. Cell 127 has so far received only one B;
its future run length is unresolved. No positive even completed initial B run
occurred. The leading pair alone is insufficient: the two `BB` prefixes at 91
and 97 are safe `BBBA`, not the line-21/22 trigger.

On line 21 all 225 recorded initial pairs are complete: 125 BA, 51 AB and 49 AA.
On line 22 there are 113 BA, 48 AB and 41 AA, plus a final cell with only A so far.
There is no BB initial pair.

### Correlations and a held-out portion of the execution

The following exact aggregate counts were converted to displayed frequencies.
Each range means a sum over those **spatial cuts**, not independent observations.
`f(BB)` divides by the number of available adjacent pairs, and `P(B|B)` here is
the descriptive ratio `#BB/#B`, not a stochastic assertion about the machine.

| Line | Cuts | B frequency | BB frequency | Descriptive P(B after B) |
|---:|---|---:|---:|---:|
| 21 | 60–99 | 0.379802 | 0.018871 | 0.049686 |
| 21 | 100–149 | 0.379785 | 0.018856 | 0.049650 |
| 21 | 150–199 | 0.379758 | 0.018843 | 0.049613 |
| 22 | 60–99 | 0.370850 | 0.010638 | 0.028684 |
| 22 | 100–149 | 0.370916 | 0.010639 | 0.028683 |

The body-frequency pattern in cuts 60–99 persists in the later 100–149 portion.
An iid-letter model at these B frequencies would instead give BB frequencies
around **0.144** and **0.138**. The actual pair frequencies are smaller by factors
about **7.6** and **12.9**. Independent letters are already a poor description of
these particular generated streams. This also illustrates why the different B1
instructions on 21/22 cannot be ignored when assigning probabilities.

Even a model fitted to these pair frequencies would need an additional argument
that the distinguished first pair at a newly reached cell samples the body like
a random phase. It does not follow from stable body frequencies. The spatial
streams are deterministic iterates, their prefixes are correlated, and these
machines were selected for having survived their previous opportunities. A
nonzero body frequency of BB proves only that BB occurs safely in initialized
cells. It proves neither a positive lower bound on future fresh-cell hazard nor
independence across fresh cells.

Line 13 has B frequency about 0.516 and BB frequency about 0.171 at deep sampled
cuts, but its fresh prefixes obey the additional parity and alternating-entry
restrictions just described. Using a generic random phase or a geometric initial
B-run without a dynamical justification would discard the problem's critical
information. No stronger eventual-halting prediction is supported by this pass.

## Exact timing formulas, and what they do not estimate

The line-13 formula `L=15q^2` and the entry-count raw-time identity are inherited
from the existing simulator and README. This pass independently derives them
below and derives the closed form for 21/22 from the inherited driver table.

Let `q >= 1` be the number of whole source periods completed at a canonical
boundary, and `E_x(q)` the number of consumed rightward entries into nonnegative
cell x. The period length is `m=5` for 13 and `m=13` for 21/22; `E_0=m*q`.
The sum includes only visited nonnegative cells. The exact total raw count is

```
T(q) = L(q) + 2 * sum_x E_x(q) - m*q
L_13(q) = 15*q^2
L_21(q) = L_22(q) = 52*q^2 - 21*q + 8.
```

Here L is the negative-half cost, not the entire run. On the positive half every
completed entry exits once to the left; every entry at x>0 also has one
right-moving instruction at x-1. Counting both gives the displayed positive-half
identity. The current incoming state at cell 0 has not yet consumed an entry.

These polynomial forms follow from the inherited exact one-cell negative-driver
table, rather than polynomial interpolation:

* On 13, a three-cell block takes `30q-15` local instructions and reduces the
  outstanding source-call count from `5q` to `5(q-1)`. Summing these blocks gives
  `15q^2`.
* On 21/22 the first three negative cells cost `78q-40` and leave `13(q-1)+1`
  subordinate calls. At `13r+1`, the next four cells cost `104r-47` and reduce r
  by one. The final one-call cell costs one. Thus
  `L=78q-39 + sum_{r=1}^{q-1}(104r-47)=52q^2-21q+8`.

Successive source periods alone therefore add at least `30q+15` raw instructions
on 13 and `104q+31` on 21/22, plus the positive-half work. Source periods are
**not** fresh-cell opportunities. For example line 21 had 218 positive cells at
`q=10^11`, reached 220 by `1.1*10^11`, and 225 by `1.4*10^11`; it still had 225
at `2*10^11`. The spacing is highly unequal even in this short extension.

The missing ingredient for a halting-time median or percentile is a justified
distribution, or deterministic recurrence, for the future **triggering fresh
cell and its source index q**. Neither the exact quadratic raw clock nor survival
to a huge q supplies this ingredient. These reports consequently give no median,
percentile range, expected stopping time, or asserted future growth scale.

## Verification and reproduction

Run from the repository root with Python 3, a C++20 compiler, GMP and assertions
enabled. Executables can be placed outside the source tree:

```sh
g++ -O3 -std=c++20 research/bb2x5/frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-stream
g++ -O3 -std=c++20 research/bb2x5/halting-outlook/streams-analyze.cpp -lgmpxx -lgmp -o /tmp/bb25-stream-stats
python3 research/bb2x5/halting-outlook/streams-investigate.py --engine /tmp/bb25-stream-stats --reference /tmp/bb25-stream --verify --output /tmp/streams-verification.json
python3 research/bb2x5/halting-outlook/streams-investigate.py --engine /tmp/bb25-stream-stats --line 13 --groups 100000000000000 --batches 1 --output /tmp/streams-13.json
python3 research/bb2x5/halting-outlook/streams-investigate.py --engine /tmp/bb25-stream-stats --line 21 --groups 10000000000 --batches 20 --output /tmp/streams-21.json
python3 research/bb2x5/halting-outlook/streams-investigate.py --engine /tmp/bb25-stream-stats --line 22 --groups 100000000000 --batches 2 --output /tmp/streams-22.json
```

The [verification record](streams-verification.json) checks every batch against
the unchanged accelerator and against a literal interpreter through 127 source
periods, comparing **the entire tape, head, state, raw count, per-cut entry counts,
B counts, BB counts and stored prefixes**. It checks all 2,047 input words of
length at most ten against each stated fresh-cell trigger and checks the
negative-clock formulas at every q from 1 through 10,000. The algebra above, not
these finite samples, establishes the formulas for arbitrary q.

No new execution-skipping rule was introduced. The underlying stream engine
examines the local undefined instruction before compressing a finite repeated
cycle. Its accepted batch contains only successful local transitions. If a
candidate undefined instruction is found, this instrumentation stops rather
than claiming a chronologically realized halt; the inherited simulator has a
separate chronological refinement path. The complete-configuration tests guard
against a changed first-visit return contract or a wrong source phase.

Two exploratory single-batch attempts exceeded the 536,870,912-bit materialized
word budget (13 at `2*10^16` periods and 21 at `10^11` periods). Their partial
outputs are not endpoints and are not used as survival certificates. The saved
runs use the successful batch sizes above. Bounded experiments and these
transition-table arguments have not been formalized in Rocq or Lean.

## Unresolved assumptions and next concrete steps

1. **Line 13:** track the exact leading B-run at each newly reached odd-position
   cell, continuing from the inherited q=`2*10^16` checkpoint. Derive a recurrence
   on the complete distinguished prefix that either permits an even run or proves
   oddness invariant. The newly observed safe runs of three at 91 and 97 show
   that “the first B is always immediately followed by A” is false.
2. **Lines 21/22:** preserve source phase and transducer state while constructing
   a finite representation of fresh-cell first pairs. Test a proposed invariant
   on the later saved cuts, then prove closure. A factor language that independently
   chooses continuations is insufficient, as the inherited counterexample shows.
3. **For an eventual probabilistic estimate:** first justify a model for the
   *distinguished boundary prefixes*, check it on held-out new frontiers, and show
   how any size-dependent hazard accumulates. Only then combine event indices
   with the exact raw-time formula. The present observations do not satisfy this
   requirement, so no classification is upgraded to probable halting.
