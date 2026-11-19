# Extending the connected return chain from Y

The [first connected chain](CHECKPOINT_Y_758.md) ends at $Y+158,145,479,878$ after its thirteenth primary corridor. Three further primary corridors each lead to an exact common reset. Every seed in the [connected annular entry interval](CHECKPOINT_Y_758.md) therefore reaches **$Y+1,801,202,590,593$**. Reaching that entry interval from blank and the fate of this later reset both remain open.

All positions below are integer offsets from $Y$. The gate number counts the final bulks in its odd return word.

| Gate | Previous common reset | First known reset in gate | New common reset | Interior skips | Literal returns outside skips |
|---:|---:|---:|---:|---:|---:|
| 715 | 158,145,479,878 | 237,191,085,301 | 355,796,242,152 | 109 | 6,429,216 |
| 713 | 355,796,242,152 | 533,685,576,786 | 800,541,568,128 | 178 | 12,212,687 |
| 711 | 800,541,568,128 | 1,200,798,185,990 | 1,801,202,590,593 | 306 | 22,644,424 |

The gap to each destination is split into intervals. Equal complete ordinary return words at the odd endpoints certify that all intervening odd seeds take the same word. All even seeds here have their known return with gain at most 615. Adjacent certified intervals can be combined, keeping the maximum gain bound over the constituent words and both parities. The checker bisects an interval with differing endpoint words until its width drops below 30 million seeds. Any uncovered portion is followed by literal first returns from the current exact source.

On reaching a certified interval at least 30 million seeds wide, the checker evaluates every seed in the last gain-bound positions that can exit the interval on its next return. It then advances the smallest resulting state until all possible exits coalesce. This gives the exact successor checkpoint even when the return itinerary varies across the interval. The same merge at the validated primary gate supplies the next row's source. The three rows skip 62,719,122,992, 147,336,071,510 and 343,481,473,564 units of reset seed respectively. These are distances in seed space. No elapsed raw clock is asserted for the skipped stretches.

The [receipts](checkpoint_y_mixed_758.tsv) record $k$, source, gate start, first excluded gate endpoint, arrival, common reset, literal returns outside the skips, number of interior skips, interior merger evaluations including edge probes, seed distance skipped, and the number of candidate intervals initially retained. Replay from the research directory.

```sh
c++ -O3 -std=c++17 checkpoint_y_758.cpp -lgmpxx -lgmp -o /tmp/checkpoint_y
cut -d' ' -f1,3,4 checkpoint_y_mixed_758.tsv | /tmp/checkpoint_y --mixed > /tmp/mixed-y.tsv
cmp checkpoint_y_mixed_758.tsv /tmp/mixed-y.tsv
```
