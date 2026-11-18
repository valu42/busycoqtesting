# A three-signal reduction for line 8

Line 8 is `1RB4LA1RA1RB1LA_2LB3LA---4RA2RB`. Its blank-tape status remains open. The reduction below turns the question into a first-symbol test on a stream over three letters. A complete source period can advance the simulation by at most five pairs.

Use the repository’s [negative-half driver](mixed-and-sweeps.md). The first positive entry is A and leaves the two cells `32`. Later entries from the negative half are `BBABA` repeated. Group either one A, one B, or two successive entries BA as a single signal. In the following table `z` denotes BA and a dash denotes no signal. Each entry gives the replacement pair and the one signal passed right.

| Old pair | A | B | z |
|---|---|---|---|
| 11 | 41, – | 31, – | 43, – |
| 13 | 43, – | 33, – | 41, A |
| 14 | 44, – | 34, – | 44, z |
| 31 | 43, – | 14, – | 44, – |
| 33 | 41, A | 14, B | 44, B |
| 34 | 44, z | 11, – | 41, – |
| 41 | 11, – | 44, B | 14, B |
| 43 | 13, – | 44, A | 14, A |
| 44 | 14, – | 41, z | 11, z |

The right tape consists of zero or more ordinary pairs followed by `32`. Ordinary cells pass their rightward requests in chronological order. On success each ordinary cell eventually takes a left step in A. The terminal pair on A immediately reaches B2, on B returns in A and becomes `1432`, and on z returns twice in A and becomes `4432`. These three facts follow by direct stepping into the virgin blanks. In the ordinary pairs the table follows by tracing the two cells, substituting A on successful rightward returns. Induction from the last pair proves that each whole-signal probe terminates or reaches B2. The table and terminal cases then prove the asserted tape shape by induction from `32`.

## The blank source and a fixed stream

Think of `32` as the current terminal pair. Its first received signal either halts it or creates the next terminal. A first B creates a new terminal and leaves the old pair in `14`. A first z leaves it in `44`. For each later input, propagate the nonempty outputs in the table to the next terminal.

For the first terminal on blank, the first signal is B and the residual driver is `BABAB` repeated. Starting at `14`, one copy of `BABAB` emits z,z and leaves `31`. From `31` each copy emits z and returns to `31`. **The second terminal therefore receives the constant stream z.** From there the original problem is precisely whether the iteration ever has first signal A. If a level receives only finitely many signals and no failure, omitted calls can never subsequently halt at greater depth unless they are emitted through that level. Equivalently one can work with the nested sequence of finite source prefixes. Each completed call processes finitely many pairs.

There is an explicit periodic reference stream $(z,B,z)^\omega$. Its first z leaves `44`. While in `44` the three subsequent inputs B,z,z emit z,B,z and return the pair to `44`. Thus every successive terminal under the reference drive receives exactly the same stream and expands. The actual drive at the second terminal is $z^\omega$.

## Why a finite matching prefix cannot certify survival

After any finite successful prefix the tape has finitely many ordinary cells followed by `32`. At any such ordinary cell a freely chosen input word can pass exactly one desired **raw** entry to the next cell. The two columns select inputs producing A or B respectively.

| Current symbol | To pass A | To pass B |
|---|---|---|
| 1 | BB | BA |
| 3 | B | A |
| 4 | ABB | ABA |

These paths have no other rightward calls. To realize a finite desired sequence, concatenate the inputs selected using the successively updated state. Applying this procedure from right to left across the finitely many ordinary cells forces one A into the terminal `32`, which halts. All earlier successful calls stay within the ordinary region. Consequently every finite prefix of the safe periodic reference admits a halting continuation by freely supplied input. This identifies the missing hypothesis in a prefix argument. A proof must control the actual continuation supplied by $z^\omega$ at the second terminal.

Run `python3 line8_pairs.py BB2x5_Rocq_holdouts_37.txt` in this directory. It checks the machine identity, all 27 ordinary transitions through their generated pair table, both stream identities, and the single-letter control codes. It compares positive-tape transitions with a raw interpreter on every pair word through two ordinary pairs and on 20,000 successive actual source letters.

## Finite blank run

The saved [checkpoint](line8-30.json) is at exactly $10^{30}$ five-entry groups, with 280 nonnegative cells visited. The head is at coordinate zero in A after 15000000000000000000000000000027931427720955941384312401887148 defined instructions. A run from blank using 16-bit packet lookups and a separate run from the earlier $10^{28}$-group checkpoint using the repository’s standard 8-bit lookups produced byte-identical files. Both runs use the repository’s longitudinal algorithm and raw clock, so this is a split-batch replay, not a second independent clock proof.

To reproduce from the repository’s existing checkpoint, run these commands in `research/bb2x5`. The last command expects the new checkpoint in the current directory.

```sh
c++ -O3 -std=c++17 frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-stream
python3 frontiers/longitudinal.py --engine /tmp/bb25-stream --line 8 \
  --resume frontiers/runs/stream-08.json --groups 990000000000000000000000000000 \
  --max-bits 800000000 --finite-slots 30000000000 --checkpoint /tmp/line8-replay.json
cmp line8-30.json /tmp/line8-replay.json
```
