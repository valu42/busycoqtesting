# A connected route onward from the last depth-eight annular merger

Let $Y=\lfloor3^{301}/19171\rfloor+4,510,976$. Every reset in the [eleventh depth-eight cell](ANNULAR_MERGERS_292_758.md) reaches $Y$. From $Y$ the actual deterministic trajectory enters thirteen successive ordinary return gates. **Every reset in any of those gates also reaches the same later checkpoint $Y+158,145,479,878$.** The first gate begins $1,750,734$ above $Y$. This extends the previous eleven literal first returns from $Y$ to joined intervals, with all intervening gaps crossed on a known trajectory. The blank orbit's entry to the eleventh cell remains open, as does the onward route to the target $H$.

The [receipt table](checkpoint_y_758.tsv) records the odd bulk count $k$, lower and exclusive upper gate offsets, first actual arrival from the previous checkpoint, number of literal first returns up to that arrival, number of distinct possible first exits, number of edges checked to merge those exits, and unique new checkpoint offset. All offsets are relative to $Y$.

| $k$ | First actual arrival | First exits | New common checkpoint |
|---:|---:|---:|---:|
| 741 | 1,751,669 | 797 | 7,020,408 |
| 739 | 9,580,711 | 746 | 20,082,170 |
| 737 | 27,191,413 | 802 | 48,355,536 |
| 735 | 66,821,937 | 723 | 105,803,286 |
| 733 | 155,986,751 | 780 | 239,700,330 |
| 731 | 356,605,973 | 700 | 539,522,850 |
| 729 | 807,999,148 | 782 | 1,216,186,006 |
| 727 | 1,823,637,116 | 718 | 2,744,815,021 |
| 725 | 4,108,825,146 | 768 | 6,174,189,006 |
| 723 | 9,250,491,068 | 723 | 13,884,267,034 |
| 721 | 20,819,245,244 | 764 | 31,238,221,767 |
| 719 | 46,848,941,695 | 709 | 70,284,773,740 |
| 717 | 105,415,755,498 | 759 | 158,145,479,878 |

## A continuous entry interval across the first nine gaps

Let $S$ be the inclusive lower endpoint of the eleventh depth-eight cell. **Every reset from $S$ through $Y+6,165,490,165$, including all intervening gaps, reaches $Y+158,145,479,878$.** This input interval contains about $2.3997\times10^{136}$ consecutive reset seeds. Entry of the blank orbit into this interval remains open.

This gives a finite alternative for the blank trajectory. If it crosses the entire interval alive, it either visits the displayed later checkpoint or executes **more than $5.33\times10^{135}$ consecutive ordinary counter calls** in that passage. Indeed, let $U=Y+6,165,490,165$. A run that misses the checkpoint has no reset at any mass from $2S+1$ through $2U+1$. This whole span lies in the [785-bulk exceptional-return annulus](CUT_758.md). An exceptional instruction at mass $W\le2U+1-5458$ would force a reset at $W+5458$, still in the span. After the first mass at least $2S+1$, which is at most $2S+9$, only ordinary calls can cross the stripped span. Each gains at most nine in mass. The resulting lower bound is $\lceil (2(U-S)-5465)/9\rceil$. The later checkpoint's own fate remains open.

The original cell ends just before $Y-4,511,571$. Its first 11,571 subsequent seeds return with gains from 605 through 3,455, by individual evaluation. Subdividing the next 4,500,000 seeds gives a uniform gain bound of 4,313, so trajectories from this collar reach the post-$Y$ interval. From $Y$ onwards the checker covers every gap through the $k=725$ gate. The largest certified gap gain is 4,484. Each destination gate is wider than the preceding gain bound, hence any starting seed in a gap reaches its destination gate before it can jump across. Entry inside any of the gates already leads to the exact recorded checkpoint.

For an interval of odd seeds, the verifier replays both endpoint return words, including the entire number of leading bulks after $J^{292}L^8J$. Equal ordinary words certify every intermediate seed by opposite counter order. The maximum possible mass gain on the word bounds its returned seed. Otherwise the verifier bisects. A singleton accepts its exact evaluated return, including any exceptional instruction. The even word bounds every even seed by 615. The [gap receipts](checkpoint_y_gaps_758.tsv) contain the inclusive low and exclusive high offsets, binary tree nodes, accepted leaves and maximum seed gain. The [contact check](check_checkpoint_y_gaps_758.py) verifies the connection to the old cell, the first 11,571 gains and the overlaps with all destination gates. The [local interval count](LOCAL_RETURN_WINDOWS_758.md) bounds the number of complete probes for width $W$ by $O(W^\delta\log(W+1))$, where $\delta=0.73177394\ldots$. The elapsed cost of an individual unusually long first return remains separate.

## All 368 gates between the checkpoint and the halting target

Every one of the [368 pure-bulk intervals](SECONDARY_CUSP_758.md) has a unique later checkpoint. Their combined width accounts for **39.98916766%** of the reset seeds from $Y$ to $H$. Thus entry anywhere in these intervals reduces the future trajectory to one of just 368 explicit states. The calculation evaluated all 183,621 possible first exits, and their mergers used 4,728,215 separate first-return edges summed across the gates. The 368 checkpoints are distinct. Their offsets above their gate’s exclusive upper endpoint range from 1,032,644 through 21,608,914. For the $k=7$ interval containing the scale-264 corridor, 215 possible exits merge after 9,816 edges at the upper endpoint plus 3,911,056.

The [complete census](checkpoint_y_census_758.tsv) lists $k$, number of first exits, first-return edges in the merger, and checkpoint offset from the exclusive upper endpoint. It proves each transition separately, so the table alone does not connect the intervening gaps. The connected route starting at $Y$ is given above.

## Verifying the chain

On an odd input $Y+x$ the gate word is $J^{292}L^8JL^kR$. On an even input it is the known 300-call word $IJ^{291}L^2JL^2JLR$. The checker verifies the two odd endpoints of every gate. At a common ordinary prefix, increasing the reset seed weakly decreases the left counter and weakly increases the right. Hence the intermediate seeds satisfy the same guards. The right endpoint's left counter stays strictly above one before the return. The same endpoint argument and a 64-residue period verify the even word. The largest seed gain in a gate is bounded by the greater of 615 and $(4\cdot293+9(8+k)+5)/2$, rounding down. Every first exit must come from this many positions before the upper edge. Evaluate all those positions, then repeatedly advance the smallest possible exit, merging equal states until only one remains. Following that reset literally through the next gap proves its arrival inside the following gate.

To replay the individual returns, the odd header $J^{292}L^8J$ needs 256 representatives. Adding 512 to the odd starting seed changes $(a,c)$ after the header by $(-75660,38342)$. Indeed each bulk consumes one binary digit of a counter difference, so the eight bulk residue choices are preserved by this translation. The checker evaluates every representative and its translate. For the long subsequent bulk run put $y=(c+7)/2$. A bulk sends $y$ to $3\lceil y/2\rceil$ and gains either five or nine units of $a+2c$. A table of $2^{16}$ low residues supplies sixteen consecutive proposed bulks, with the upper bits translated linearly. The new left counter follows from the total mass gain. A packet whose final left counter is greater than one has all its bulk guards satisfied, since each proposed bulk decreases the left counter. The checker also precomputes an initial number of legal packets for each offset size. The conservative bound $c'+13\le3(c+13)/2$ keeps the formal right counter below one quarter of the smaller of $Y$ and the local base seed, while the mass is at least twice that smaller value. Every remaining jump, exceptional update, terminal or reset is then decided by the exact two-counter map.

Build and replay the [integer checker](checkpoint_y_758.cpp) with GMP from this directory. A byte comparison with the table checks every recorded count and destination.

```sh
c++ -O3 -std=c++17 checkpoint_y_758.cpp -lgmpxx -lgmp -o /tmp/checkpoint_y
cut -d' ' -f1-3 checkpoint_y_758.tsv | /tmp/checkpoint_y > /tmp/checkpoint_y.tsv
cmp checkpoint_y_758.tsv /tmp/checkpoint_y.tsv
```


To check the 368 independent gates against their exact absolute endpoints, use the same compiled program. It recenters its calculations at each 140-digit gate edge and checks both endpoint words there.

```sh
python3 -c 'from secondary_cusp_758 import gate_rows; [print(*row) for row in gate_rows()]' | /tmp/checkpoint_y --census > /tmp/checkpoint_y_census.tsv
cmp checkpoint_y_census_758.tsv /tmp/checkpoint_y_census.tsv
```

To check the uninterrupted entry interval, replay the gap receipts and the joins.

```sh
cut -d' ' -f1-2 checkpoint_y_gaps_758.tsv | /tmp/checkpoint_y --cover > /tmp/checkpoint_y_gaps.tsv
cmp checkpoint_y_gaps_758.tsv /tmp/checkpoint_y_gaps.tsv
python3 check_checkpoint_y_gaps_758.py
```

Replacing `--census` with `--follow-mergers` in the same pipeline traces 16,384 further unrestricted first returns from every one of the 368 common checkpoints. All 6,029,312 return. The smallest and largest total advances over a checkpoint’s run are 35,804,076 and 44,644,118 seed units, and the largest single gain is 3,497. The 368 displacements sum to 15,097,923,732.

Beyond the individual mergers, 364 corridors now have a [second connected gate and a further common checkpoint](Y_EDGE_BANDS_758.md).
