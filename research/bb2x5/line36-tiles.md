# A six-phase tiling for line 36

The sweep model for `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---` has a family of right-infinite words that repeat after six symbolic updates. Any sequence of 64 distinct finite tiles can follow a 26-cell prefix. On the actual blank orbit, the first 3,319 of 6,336 cells at epoch 2,005 agree with this family. Whether the blank orbit halts remains open.

## The six phases

An epoch word lists the digits from left to right. From the blank tape, epoch zero is empty. Opening digit 1 contributes +1 to the height, and closing digit 2 contributes −1. Six unmatched closings in a sweep reach B4. The matching rule, guard and finite sweeps are those in [the previous line-36 analysis](mixed-and-sweeps.md#4-parity-sweep-on-line-36) and [the word interpreter](prior_sweeps.py).

Start with the 26-cell phase-0 prefix in the table. To construct one phase-0 tile, concatenate one choice from each of the six ordered pairs of strings in `PIECES`. These twelve short literals define all 64 distinct tiles. Each has length 164 to 170. The argument below determines the other five versions of each tile. [Tile definitions and checker](line36_tiles.py)

| Phase | Prefix | Minimum height | Header length |
|---:|---|---:|---:|
| 0 | `22211111221112111111111212` | −3 | 6 |
| 1 | `22112111121121112121211111` | −2 | 1 |
| 2 | `11122121121221212111112111` | 0 | 1 |
| 3 | `22211111111111111121112121` | −3 | 6 |
| 4 | `22112111121111111111111212` | −2 | 1 |
| 5 | `11122121121211111111111211` | 0 | 1 |

At each phase, each tile has no unmatched closings and 84 to 90 unmatched openings. Every finite prefix of a tile therefore has nonnegative height. Appending any number of these tiles preserves both the prefix's matching and its guard minimum. Each tile can be matched independently, including at a boundary between different choices.

## Why arbitrary choices compose

Mark every unmatched opening with bit one and every other digit with bit zero. The ordinary return sweep produces digit 2 at a change of bit and digit 1 when consecutive bits agree. The previous bit for the first digit of a tile comes from the last digit of the preceding prefix or tile. At any single phase, this terminal bit is the same for the prefix and for all 64 tiles.

Let $P$ be the current prefix. Its finite output, after removing the final right-edge carry if present, has the form $P'C$. Here $P'$ is the next 26-cell prefix and $C$ is a common overlap of the header length in the table. For each current tile $T$, compute its digit stream $D$ from the marked bits and the shared previous bit. The checker verifies that $D$ ends with $C$. Write $D=EC$, and define the next tile to be $T'=CE$. The following exact finite identity holds for every number of tiles, with independent choices at each position.

$$
F(P T_1\cdots T_m)=P' T'_1\cdots T'_m C K.
$$

The final carry $K$ is a single 2 when the common terminal bit is one and empty otherwise. Indeed, the output starts with $P'C$ and then emits $E_1C,E_2C,\dots,E_mC$ before the carry. This proves the finite identity by concatenation. Every fixed finite part of the output stabilizes when the input is extended by more tiles. These stabilized parts define the right-infinite symbolic update.

The checker computes the guard and overlap at each phase and compares all 384 one-tile finite identities with the existing sweep interpreter. At the sixth update the prefix returns and every tile returns to its original word. Thus every right-infinite concatenation has period dividing six. On the ordinary Turing machine, a sweep over an infinite word would take infinitely many steps. The six phases here refer to the symbolic update.

## Comparison with the blank orbit

These checkpoints use phase 0 at epochs congruent to 1 modulo 6. The matched cell count includes the prefix, the complete tiles and the longest initial part of a next tile. The word at epoch 127 was also reached directly in 89,229 elementary transitions, with the head at coordinate −327. All 127 preceding epoch comparisons use the literal tape interpreter.

| Blank epoch | Full tiles | Matching cells | Word length |
|---:|---:|---:|---:|
| 25 | 0 | 31 | 66 |
| 127 | 1 | 199 | 389 |
| 1,201 | 11 | 1,979 | 3,790 |
| 2,005 | 19 | 3,319 | 6,336 |

Run `python3 line36_tiles.py` from this directory. The finite identity gives an exact boundary after a known tile sequence. The remaining proof obligation is to control the actual finite suffix. Unmatched closings from that suffix can pair with openings in a preceding tile and change its output. The checkpoints give no guarantee that the matched prefix keeps growing or that the guard always survives.
