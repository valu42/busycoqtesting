# A connected route onward from the last depth-eight annular merger

Let $Y=\lfloor3^{301}/19171\rfloor+4,510,976$. Every reset in the [eleventh depth-eight cell](ANNULAR_MERGERS_292_758.md) reaches $Y$. From $Y$ the actual deterministic trajectory enters eleven successive ordinary return gates. **Every reset in any of those gates also reaches the same later checkpoint $Y+31,238,221,767$.** The first gate begins $1,750,734$ above $Y$. This extends the previous eleven literal first returns from $Y$ to joined intervals, with all intervening gaps crossed on a known trajectory. The blank orbit's entry to the eleventh cell remains open, as does the onward route to the target $H$.

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

## Verifying the chain

On an odd input $Y+x$ the gate word is $J^{292}L^8JL^kR$. On an even input it is the known 300-call word $IJ^{291}L^2JL^2JLR$. The checker verifies the two odd endpoints of every gate. At a common ordinary prefix, increasing the reset seed weakly decreases the left counter and weakly increases the right. Hence the intermediate seeds satisfy the same guards. The right endpoint's left counter stays strictly above one before the return. The same endpoint argument and a 64-residue period verify the even word. The largest seed gain in a gate is bounded by the greater of 615 and $(4\cdot293+9(8+k)+5)/2$, rounding down. Every first exit must come from this many positions before the upper edge. Evaluate all those positions, then repeatedly advance the smallest possible exit, merging equal states until only one remains. Following that reset literally through the next gap proves its arrival inside the following gate.

To replay the individual returns, the odd header $J^{292}L^8J$ needs 256 representatives. Adding 512 to the odd starting seed changes $(a,c)$ after the header by $(-75660,38342)$. Indeed each bulk consumes one binary digit of a counter difference, so the eight bulk residue choices are preserved by this translation. The checker evaluates every representative and its translate. For the long subsequent bulk run put $y=(c+7)/2$. A bulk sends $y$ to $3\lceil y/2\rceil$ and gains either five or nine units of $a+2c$. A table of $2^{16}$ low residues supplies sixteen consecutive proposed bulks, with the upper bits translated linearly. The new left counter follows from the total mass gain. A packet whose final left counter is greater than one has all its bulk guards satisfied, since each proposed bulk decreases the left counter. The checker also precomputes an initial number of legal packets for each offset size. The conservative bound $c'+13\le3(c+13)/2$ keeps the formal right counter below $Y/4$ throughout these packets, while the mass is at least $2Y$. Every remaining jump, exceptional update, terminal or reset is then decided by the exact two-counter map.

Build and replay the [integer checker](checkpoint_y_758.cpp) with GMP from this directory. A byte comparison with the table checks every recorded count and destination.

```sh
c++ -O3 -std=c++17 checkpoint_y_758.cpp -lgmpxx -lgmp -o /tmp/checkpoint_y
cut -d' ' -f1-3 checkpoint_y_758.tsv | /tmp/checkpoint_y > /tmp/checkpoint_y.tsv
cmp checkpoint_y_758.tsv /tmp/checkpoint_y.tsv
```
