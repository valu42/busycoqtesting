# Line 429 halts exactly if two zero gaps meet in a specified pattern

**Blank-tape decision open.** The machine is permanent line **429**, ID **123915**, rank **188** in the supplied ranking. Its table is `1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA0RF`. Start in A at cell zero on the all-zero two-way tape. Count defined instructions up to arrival at D reading 1. [Frozen entry](../BB6_holdouts_608.txt#L429) · [Original ranking](https://github.com/valu42/busycoqtesting/blob/175f2c272c1d5dfd1ff16f277839f19877cb2364/research/bb6/RANKINGS.md)

**Theorem.** The blank run halts if and only if, at some time in state A, the symbols starting under the head and extending to the right begin with

```text
00 1^k 0 1 00 1       for some k >= 1.
```

The first and second `00` are separated by a run of ones, a single zero and a single one. For example, `001101001` in state A forces D1 exactly 18 moves later, for *every* choice of the other cells. The open question is whether the displayed family occurs on the blank run. A sufficient nonhalting invariant would put at least two intervening zero symbols between every two consecutive internal `00` gaps at the start of each right sweep.

**Follow-up.** Rocq proves at least **10^581 elementary moves** from blank and exhibits a reachable tape at which the known line-279 halter stops while line 429 continues. [Theorems, stopping conditions and reproduction](verified/README.md)

## An exact sweep of the original tape

The following notation records actual configurations in state A. Words in each half-tape are read from the head outwards, with an infinite zero tail. A capital letter such as `U` denotes an unchanged suffix. Juxtaposition concatenates words. For example, `1^k` denotes k consecutive ones. Write `R(p,u,v)` when the cells strictly left of the head read `p u` outwards and the scanned cell and cells to its right read `v`. Write `L(u,v)` when the scanned cell and cells to its left read `u` outwards and the cells strictly to the right read `1 v`. Both descriptions use the machine's original orientation.

| Starting configuration | Next configuration | Defined moves |
|---|---|---:|
| `R(p,u,01V)` | `R(1,1 p u,V)` | 2 |
| `R(p,u,00 1^k 0 V)`, k ≥ 1 | `R(0,0^k 11 p u,V)` | k + 3 |
| `R(1,u,1V)` | `R(0,0u,V)` | 3 |
| `R(0,1^k 0 U,1V)`, k ≥ 0 | `L(U,1^(k+1) 0 V)` | k + 5 |
| `R(p,u,0000V)`, where `p u = 1^k 0 U` | `L(U,1^(k+3) 0 V)` | k + 8 |
| `R(p,u,0001V)` | D reading the final 1 | 3 |
| `L(11U,v)` | `L(U,10v)` | 8 |
| `L(10 1^k 0 U,v)`, k ≥ 0 | `L(U,1^(k+1) 01 v)` | k + 5 |
| `L(0U,v)` | `R(1,1U,v)` | 2 |

Here is a direct check of the table. A reading `01` takes A0 and B1. On `00 1^k 0`, A0 and B0 write the first two ones, C1 erases the first following one, F1 erases the rest and F0 steps past the zero. On `000`, A0, B0 and C0 each write a one and move right. D1 halts there if the fourth bit is one. Otherwise D0 turns left, E1 crosses the three new ones and the adjacent old ones, and E0 writes the new left sentinel. On a scanned one with a one immediately left, the path is A1, C1, F0. With a zero immediately left, the path is A1, C0, D0, E1, then E1 across the remaining ones and E0 at the first zero.

For `L(11U,v)`, the known one to the right supplies the eight-instruction path A1, C1, F0, A1, C0, D0, E1, E0. For `L(10 1^k 0 U,v)`, apply the preceding A1 path with zero on the left, retaining the old right sentinel. The final row is A0, B1. Each crossing of `1^k` follows by induction on a single E1 or F1. These derivations keep both exterior tails arbitrary. The only intermediate visit to A inside a row occurs in the eight-move row and scans a one.

Start with `R(0,0∞,0∞)`. Every row costs at least two moves. Between reversals each continuing row consumes at least one bit of the half-tape being scanned. With finite support, an uninterrupted left scan reaches `0`, and an uninterrupted right scan reaches a return or a halt, at the latest in the infinite zero tail. Thus the rows cover the whole computation and an infinite sequence of sweeps gives infinite elementary progress.

## Why a first halt requires both gaps

Call the word `v` at a left-to-right turn a *launch word*. Its head is the first bit of `v` in `R(1,u,v)`. Call a zero run *internal* when a one occurs somewhere after it. The first right sweep from blank turns on `0000`. Every later launch word starts with one, as follows from the return rows.

1. **Form of a new launch word.** During a left scan, continuing rows prepend either `10` or `1^j 01` with j ≥ 1. Their accumulated prefix `P` has no internal `00`. A nonempty `P` ends in `10` or `01`. On an actual right scan with pending bit zero, the next bit of the left half is also zero. Initially this holds on blank, and both continuing right rules that set the pending bit to zero put a zero behind it. Hence a reversal on a scanned one replaces the prefix up to and including that one by `P10`, retaining the suffix after the one. A reversal on `0000` gives `P 1^m 0` followed by the unconsumed suffix, for m ≥ 3.
2. **What precedes a double zero.** Until the first launch with three consecutive internal zeros, every internal `00` is preceded by one or two consecutive ones. If the pair follows the initial run of ones of the word, that run has length one. To prove this inductively, a `0000` turn is then in the final zero tail, so it leaves no internal pair. For a turn on a one the new word is `P10V`. A new pair can only straddle the boundary with `V`. Its preceding run is the last run in `P1`, of length one or two, and has length one if it begins the word. Any pair wholly inherited from `V` keeps or shortens its preceding run of ones because the new prefix ends in zero. An inherited pair at the very beginning of `V` would already create the first triple.
3. **The first triple.** A right scan changes only the consumed part of its input. To halt on `0001` it must therefore have begun with a launch word containing an internal triple. At the first creation of such a word, step 1 forces a reversal in `R(0,u,1001V)`. The old launch had at most double internal zeros, so the displayed `00` is the whole internal run. The right rule immediately preceding this reversal either consumed a single `1` in mode `R(1,…)` or consumed `00 1^k 0`. The single-one case would put two initial ones immediately before the pair if it was the first rule of the pass. Otherwise the preceding rule had to end in mode `R(1,…)` by consuming `01`, giving at least three consecutive ones immediately before the pair. Both contradict step 2. The remaining case gives exactly `00 1^k 0 1 00 1` at the earlier A configuration.

## Why the pattern forces a halt

Suppose the machine reaches `A` scanning `00 1^k 0 1 00 1 V`. On the blank orbit this must be a right-scan boundary. A left-scan boundary has a one immediately to the right, and the only intermediate A in the table scans a one.

For **k ≥ 2**, the first token costs k + 3 and leaves mode `R(0,…)` on `1001V`, with at least two leading zeros in `u`. The five-move reversal leaves `L(0U,10001V)`. The next rows take two moves to turn right, three to consume the leading one, and three to reach D1. This proves the unconditional local bound **k + 16**.

For **k = 1**, let 2r be the number of consecutive ones immediately left of the starting head. This number is even at the specified spot on the blank orbit. It is zero in mode `R(0,…)`. A new right pass starts by scanning a one in mode `R(1,…)`, switching to zero. Later, each rule that sets the mode to one consumes `01` and adds exactly two ones immediately left of the head. The first such rule after a zero mode therefore starts an even run and its repetitions preserve evenness. The initial blank configuration also has zero ones there.

After consuming `0010` and reversing on the next one, the left input begins with `1^(2+2r) 0` and the right suffix is `10001V`. Exactly r + 1 left rows on `11` prepend `(10)^(r+1)`. After the turn the right scan reads one initial `1`, then r + 1 copies of `01`, then `0001`. Summing the rows gives **27 + 10r** defined moves from the starting head to D1. This also holds on any tape with the indicated even left run.

An implementation can test a whole launch word with the anchored regular expression below. The leading one switches the initial mode to zero. Thereafter a single advancing `1` can occur only immediately after a token `01`. The other continuing token is `00 1^k 0`. These tokens are distinguished by the next input bits, so the expression recognizes exactly the launches whose right scan encounters the theorem's pattern. The final `1` need not be the end of the tape.

```text
^1(?:011?|001+0)*001+01001
```

## The blank run and the missing invariant

For the first **500,000** right launches, the smallest number of intervening zeros between consecutive internal `00` gaps was **7**, and the shortest separating word had **18** cells. A separating word attaining both minima was `110110101011010101` at launch 204, move 18,004. The halting pattern needs a separating word of the form `1^k 01`, with exactly one intervening zero.

The replay counted **136,010** births of an internal double. Before the first triple, a birth occurs at a reversal on `101…`, when `P10` is placed in front of `01…`. The new pair is the first pair in the new word. Distances between pairs in the retained suffix remain unchanged. Measuring from the new pair to the next one therefore covers every separation. The checker also enumerates the pairs in each full launch word for the first 5,000 launches and compares the two running minima.

| Right launches | Defined moves | State | Head coordinate | Ones on tape |
|---:|---:|---|---:|---:|
| 100,000 | 2,077,274,552 | A | −44,482 | 27,188 |
| 500,000 | 53,152,693,983 | A | −156,093 | 160,728 |

The two implementations agree on the state, head and both complete half-tapes at both checkpoints. The 100,000-launch checkpoint was also replayed one elementary transition at a time. The 500,000-launch digest is `2739ab00ba0d73d924d084174203af53412519f9f24f812dd95a1d73e6823ac5`. Its input is the decimal head coordinate, a vertical bar, the lowercase hexadecimal left half, a vertical bar and the lowercase hexadecimal head-and-right half. The nearest bit has weight one in each integer. Fractal Geometry Explorer already reports a longer finite blank simulation of 100,327,939,605,140 moves. The quantity measured here is the separation of the gaps. [Earlier run data](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/89e8153595f1e90de26c9e963b24d98bb4f4547d/holdouts/1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA0RF/data/far_1e14.json)

### Where a right-word invariant fails

Set just cells −8, −9 and −11 to one at time zero. The first five right launches have the same times, head coordinates and entire right words as on blank tape. At move 101 both runs are in A at −5 with right word `1101101101` followed by zeros. The respective left words, read outwards, are `11` and `111101`, followed by zeros. The altered tape reaches `001101001` at move 148 and reaches D1 at move 166. At move 125 its launch word had a single internal double. By move 140 the separating word between two doubles was `1101`. This is a counterexample to closure of the proposed lower bound under arbitrary left contexts.

The same distinction occurs far along the blank run. At launch **310,644**, move **20,200,782,534**, the head is at h = −146,976. Its left half reads `11` followed by zeros, its right half starts `1101`, and its leftmost visit so far is h − 2. Put ones at **−146,979, −146,980 and −146,982** on the *initial* tape. None of these cells has been visited by the checkpoint. Its right half is identical and its new left half reads `111101` followed by zeros. From there the next 65 defined moves end in D1 at −146,973. Replaying this altered tape independently from time zero gives **20,200,782,599** moves to the halt. The short path through those 65 moves reads only h − 11 through h + 2 before it reaches the terminal cell h + 3.

For a proof from blank, it would suffice to rule out the birth of an internal double whose next double is separated by `1^k 01`. The counterexamples show what that argument must retain about the left tape. A weaker alternative is to prove that the right-scan parser never reaches the first pair of any such two-pair word that is born. Neither step follows from the finite counts above.

## Reproduction

Run the following in this directory with Python 3.10 or newer and a C++17 compiler.

```sh
c++ -std=c++17 -O3 literal.cpp -o literal
python3 replay.py --turns 500000 --compare ./literal
```

The mathematical argument above covers unbounded exponents. The executable checks all nine rows against the literal table on 49,152 small frames, tests the launch expression on 8,192 finite right words, and checks longer instances of the forced halts. The fast sweep replay skips only fully read strings of advancing tokens. When a repeated input word restores the same mode, it concatenates that word's output and adds its clock once per copy. Reversals are evaluated separately. The independent C++ replay uses the twelve literal entries and caches exact exits from 16-cell intervals. Passing `--single` disables that cache. The C++ program prints the clock, state, head and both full half-tapes.

```sh
./literal 2077274552 --single > blank-100000.txt
./literal 20200782600 --one -146979 --one -146980 --one -146982 > changed-tape.txt
```

## Prior decisions checked on 19 November 2026

The supplied ranking is a historical snapshot. Its first-ranked machine, line 448, has since been proved halting. Line 247 also has an upstream halting proof even though the register consulted for this campaign still marked it open. Both were excluded before selecting line 429. [Line 448](https://github.com/ccz181078/busycoq/pull/100) · [Line 247](https://github.com/ccz181078/busycoq/pull/102)

- The supplied repository's register listed line 429 as `OPEN`. Its claim board, branches and pull requests yielded no previous decision for it. The original ranking points out related starts on lines 188, 415 and 426. A change of initial state can change the blank run. [Register at selection](https://github.com/valu42/busycoqtesting/blob/7c8d69cf2de5a2ecff4cd53bcec0fb87804e11b0/research/bb6/MACHINES.csv#L430)
- The source audit compared six-state transition strings under all 720 state permutations and both left-right orientations, tracking which state represents the original blank A. It covered the Rocq and Lean source blobs at the supplied repository's branch tips, upstream BusyCoq's BB6 branch and all 109 public PR heads then available, the DeepMind cryptids tree and Fractal Geometry Explorer's main tree. The 191 entries under DeepMind's `BB6/Halt` and `BB6/NonHalt` also had no matching table under those transformations. This search detects explicit textual tables. [Upstream branch](https://github.com/ccz181078/busycoq/tree/33209bc7dc282b38c8cd6be507bfc551fea56108) · [DeepMind catalogue](https://github.com/google-deepmind/cryptids/tree/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6)
- Fractal Geometry Explorer explicitly labels this exact machine open. Its files already prove local halting and sweep rules and record finite simulations. A related report follows two *other* starts of the same table. BusyCoq PR 82 proves halting for two different Chaotic Bell machines. These are prior results for this family. [Exact machine report](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/89e8153595f1e90de26c9e963b24d98bb4f4547d/holdouts/1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA0RF/README.md) · [Other starts](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/89e8153595f1e90de26c9e963b24d98bb4f4547d/holdouts/recent-proofs/followup/t4-variants.md) · [PR 82](https://github.com/ccz181078/busycoq/pull/82)
- Global GitHub searches used the full table with `---` and `HHH`, a canonical table with initial state C, and a reflected form with initial state B. Exact-table issue and pull-request searches, a general web search, a public copy of the annotated holdout sheet and a separate holdout hunt yielded no blank-tape decision. Unpublished results and differently encoded proofs remain outside this check. [Annotated list](https://github.com/Dojo-1/cryptid-verifier/blob/e14527f1c816882bb7735f1c40017274b0a93319/analysis/appendix-c-leads/bb6-annotated.csv) · [Independent hunt](https://github.com/JacobRSchwartz-AI/bb6-holdouts/blob/63900f2af164bd2a91d24257f506f70fceed1640/data/hunt.tsv)


To repeat the explicit-table comparison, run `python3 audit_tables.py /path/to/checkout` for each checkout. It reads locally fetched remote tips, deduplicates source blobs, and prints the mapped start state for each occurrence. Specific refs can follow the checkout path. For BusyCoq the check included the BB6 branch and the heads fetched by the following command.

```sh
git fetch --depth=1 origin '+refs/pull/*/head:refs/remotes/proofs/pr/*'
```

At the checked revisions the supplied repository yielded no matching explicit tables in 700 distinct Rocq and Lean source blobs, upstream BusyCoq yielded none in 1,785, and DeepMind yielded none in 464. Fractal Geometry Explorer yielded 24 table mentions in 3,131 source blobs, across the exact machine and three other starts. Its exact-machine sources give the table, finite bounds and local lemmas. These counts describe the public source search and do not establish absolute priority.
