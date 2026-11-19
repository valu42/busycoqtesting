# Eleven entry intervals with exact checkpoints below the 140-digit target

Let $P=3^{292}$ and let $H=(3^{307}-8{,}282{,}708{,}212)/13{,}959{,}275$ be the known halting reset. All eleven depth-eight ordinary intervals between $P$ and $H$ each force a single later reset from **every** starting seed in that interval. Their combined width is 43.98136610% of $H-P$. The closest one to $H$ starts at approximately $1.0255568581P$ and ends at $1.0267070054P$. Its 280 possible exits reach exactly the reset 4,511,571 above its upper endpoint. Which of these intervals the blank orbit visits is open. Percentages below describe distances and interval widths. [Checker](annular_mergers_292_758.py) · [Definition of the annular cells](ANNULAR_SKIP_758.md)

| Depth-eight cell | Start / $P$, rounded | Exclusive end / $P$, rounded | Possible first exits | Distinct edges in the final merger | Reset above last word’s exclusive end |
|---:|---:|---:|---:|---:|---:|
| 1 | 1.0015247602 | 1.0022888853 | 222 | 7,760 | 2,834,641 |
| 2 | 1.0034372617 | 1.0051647689 | 284 | 8,919 | 4,819,571 |
| 3 | 1.0063197486 | 1.0068982344 | 280 | 14,661 | 8,328,137 |
| 4 | 1.0077672112 | 1.0103950104 | 224 | 7,925 | 7,530,151 |
| 5 | 1.0133543082 | 1.0134523266 | 273 | 12,625 | 7,835,441 |
| 6 | 1.0143326579 | 1.0148404671 | 209 | 5,438 | 963,359 |
| 7 | 1.0176475657 | 1.0204526013 | 218 | 8,199 | 3,687,890 |
| 8 | 1.0214568187 | 1.0219596690 | 282 | 8,248 | 2,930,770 |
| 9 | 1.0227148733 | 1.0238497750 | 218 | 8,715 | 6,810,540 |
| 10 | 1.0246077765 | 1.0249871983 | 214 | 6,376 | 2,681,696 |
| 11 | 1.0255568581 | 1.0267070054 | 280 | 9,249 | 4,511,571 |

The ordinary-word proof already supplies two genuine first-return words throughout each cell. Let $U$ denote its exclusive upper endpoint. Summing the maximum mass charges in the two words gives an upper bound $g$ on the seed gain. An orbit started within the cell increases strictly until its first exit. The last in-cell seed lies between $U-g$ and $U-1$. Evaluating all those seeds gives precisely the possible first exits because each seed in the final strip is itself an allowed start. Advance the smallest outstanding exit by its literal first return, merging equal seeds. Nine cells merge this way immediately beyond their exclusive upper endpoint. For cells 4 and 6, the checker first advances through two additional parity-specific words. It prints the exact checkpoints for all eleven cells.

Every first exit from cell 4 is odd. A closed odd word carries all 224 exits to 18 seeds at $1.0116962404P$. Across those seeds 29 literal returns suffice to reach the even class. A closed even word carries them to five exits at $1.0116966947P$. Those five merge at the reported offset after 7,925 distinct first returns. For cell 6 the corresponding counts are 209, 11, 18, 9 and 5,438. Its two extra words end at approximately $1.0156560261P$ and $1.0157232127P$. In these two rows the last column measures from the first excluded seed of the final even word. The checker verifies its whole domain and skips complete residue cycles on each parity-specific word.

The seventh cell is the counterpart of the [actual trillion-return segment at power 35](POWER35_INNER_SKIP_758.md). At exponent 292 an odd start takes one return to become even, and the even branch preserves even parity. Its seven bulks fix the gain on each of 128 even residue classes modulo 256. After seven applications these 128 classes map into a single cycle of length 27 and stride 16,640. A start at least $9\times627$ below $U$ therefore follows the cycle before crossing and has only 65 possible exits between $U+4$ and $U+604$. All 65 merge in 6,929 literal edges. The 218-exit certificate in the table also handles seeds arbitrarily close to $U$.

## The route from the last checkpoint to the halting basin

Let $Y$ be the exact last checkpoint. It lies $2.5142588050\times10^{136}$ below $H$. Every even seed from $Y+1$ through $H-1$ follows the 300-call return word and gains at most 615 seed units. The obstacle is the odd input, including $Y$ itself. Its first word is $J^{292}L^8JL^{742}JL^4JLR$. This word holds exactly between odd seeds $Y-726$ and $Y+29{,}812$. Ten actual first returns carry the trajectory outside it to $Y+32{,}308$, and the eleventh brings it to the even seed $Y+35{,}577$.

The formal gain of this fixed word has least period $2^{756}$. It has 755 bulks, so translation by $2^{756}$ preserves all fine branches. The checker evaluates the formal gain at $Y$ and $Y+2^{755}$ as 3,216 and 3,218. This excludes every smaller period of the function on the cyclic residue group. The second evaluation tests the formal residue only. The actual guarded interval is 30,538 seed units wide between the two included endpoints, and the period exceeds $H$ itself. This prevents reusing the even-word cycle skip that advanced the blank orbit at exponent 35 on this first odd word.

The published scale-264 word corridor reaches out to distance $1.53\cdot10^{10}3^{264}$ below $H$. Its far edge still lies about $1.119\times10^{136}$ beyond $Y$. Even proving arrival there would leave open transfers toward the halting basin. A sufficient way to connect $Y$ is to prove that each odd reset on this remaining route halts or returns before it could bypass the full certified halting interval. The short even word already supplies that property for the intervening even seeds. [Scaled corridors](SCALED_GATES_758.md) · [Contiguous halting basin](TARGET_BASIN_758.md)

Run `python3 annular_mergers_292_758.py` beside the other BB(3,3) research scripts. Each of the eleven conclusions assumes entry into its own cell. Blank reachability and the onward connection to a halting corridor remain open.
