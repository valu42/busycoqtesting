# An exact trillion-return segment on the blank orbit

Both #758 and #153 reach the reset $A(1,51{,}054{,}820{,}342{,}885{,}124)$. From the earlier reached reset $A(1,50{,}885{,}978{,}668{,}530{,}449)$ they take exactly **1,648,825,998,868 first returns** and **26,657,304,251,347,328,769,027,871,467,526,286,778,627,812,518 raw transitions** to get there. This is the power-35 counterpart of the large skip cell at power 292. The blank-orbit outcome at the latter scale remains open. [Timed verifier](power35_inner_skip_758.py) · [Target-scale annulus](ANNULAR_SKIP_758.md)

| Stage | Actual ending reset parameter | First returns in stage |
|---|---:|---:|
| Approach the odd fixed word | 50,885,978,668,575,677 | 305 |
| Odd fixed word | 50,885,984,713,694,735 | 40,557,300 |
| Enter the even fixed word | 50,885,984,713,696,064 | 4 |
| Even fixed word | 51,054,820,342,878,432 | 1,648,785,441,234 |
| Reach the local common reset | 51,054,820,342,885,124 | 25 |

Above the previous checkpoint $3^{35}+34{,}754$, the first 170 archived windows carry every incoming seed in a 5,001-seed interval into the next interval alive. One supplementary crossing from 50,881,545,099,034,461 to the cut 50,885,978,668,475,620 narrows its exit to the integers 1 through 167 above that cut. All 167 seeds merge at the stated source after checking 1,268 distinct first-return edges. The supplementary receipt can be replayed with the ordinary worker. [Window receipts](double35_frontier_758.tsv.gz) · [Crossing verifier](double35_frontier_758.py)

On the two long stages the endpoint guards certify the same sequence of branches for every seed of the active parity. An odd seed takes 35 initial jumps, then `LLLLLLLLLLJJJLLLLJLLLLJL` and the reset. An even seed takes its opening move and 34 jumps, then `LLJLLJLLL` and the reset. On each word the return gain is even, so its parity class is closed. Fixing the input residue modulo $2^{20}$ on the first word, or 256 on the second, fixes every fine branch and the return gain. The raw clock is quadratic on each residue, and a repeated residue allows entire cycles to be summed exactly. For example, one odd cycle contains 7,035 first returns and advances the seed by 1,048,576. The checker establishes every intermediate counter stays away from an early reset until the final branch. [Quadratic clock calculation](TARGET_CLOCK_758.md) · [Word translation argument](RETURN_PREFIX_758.md)

| Clock at the ending reset | Lower bound | Upper bound |
|---|---:|---:|
| #758 | 1,581,817,673,027,642,920,548,815,318,052,885,252,113,873,545,030 | 2,176,662,525,994,515,438,813,642,824,555,902,900,721,567,866,334 |
| #153 | 1,581,817,673,027,642,920,548,815,318,052,885,252,113,873,494,323 | 2,176,662,525,994,515,438,813,642,824,555,902,900,721,567,815,627 |

The raw bounds combine the previous power-35 clock with bounds through the new source and the exact segment duration. The synchronized #153 clock runs 50,707 steps behind #758. [Previous clock](next_gate_after_fifth_758.py) · [Interval timing](CROSSING_CLOCK_758.md)

Further along, the actual orbit crosses $t=\lfloor H/3^{257}\rfloor=51{,}428{,}028{,}152{,}740{,}925$, at the same ratio to $3^{35}$ as the known halting target $H$ relative to $3^{292}$ up to rounding. A supplementary receipt forces the exact seed $t-99{,}916$. After 629 first returns the next two consecutive seeds are $t-136$ and $t+69$. This explicitly identifies the smaller-scale crossing. No relationship fixing the residue at scale 292 has been proved.

## Reproduce or extend the proof

Run the following in `research/bb3x3` with Python 3.10+ and a C++17 compiler. The first Python command checks row structure and the downstream gate. The second replays both supplementary windows, the exact clocks and coalescence. The third independently re-executes all archived windows needed for both named checkpoints using the general first-return implementation.

```sh
c++ -std=c++17 -O3 cross_758_fast.cpp -o /tmp/cross758
c++ -std=c++17 -O3 cross_double35_758.cpp -o /tmp/cross35
python3 double35_frontier_758.py
python3 power35_inner_skip_758.py --worker /tmp/cross758 --clock
python3 double35_frontier_758.py --worker /tmp/cross758 --stop 279 --jobs 4
```

The remaining grid aims at $2\cdot3^{35}+155{,}534$. Its 8,006 windows have width $5\times10^{12}$ except for the last. Each archived row gives a sufficient crossing for every allowed start at its left cut. Only the consecutive prefix proves progress from blank. Later rows are reusable as earlier gaps close. The checker prints both counts. Upon reaching the final cut 90,056,781,178,199,398, the previously certified doubled-power corridor forces the exact target. To finish missing rows or save a partial snapshot, run the following. Add `--start I --stop J` to restrict the task. Each completed row survives interruption in the specified directory.

```sh
python3 double35_frontier_758.py --fill /tmp/bb35-rows --worker /tmp/cross35 --jobs 4 --save extended.tsv.gz
python3 double35_frontier_758.py --fill /tmp/bb35-rows --save snapshot.tsv.gz
python3 double35_frontier_758.py --table extended.tsv.gz --require-complete
```

The faster worker uses the same symbolic cover and widening as the general worker. For exact queries its two launch states have $h=2\cdot3^{34},u=s+72$ for even seeds and $h=3^{35},u=s+70$ for odd seeds. The angular coordinate is $d=(u-h)/2$. Both use the existing packed `J`/double-bulk operations with at most four bulk pairs per stage. Their true numerator fits in 64 unsigned bits because $256d'\le128(90{,}056{,}781{,}178{,}199{,}398+50{,}000)<2^{64}$. A call that exhausts its bounded continuation or encounters a possible halt emits no successful receipt. The audit compares 2,048,000 first returns to the counter rules, including contiguous seeds, random seeds and both ends of the supported range. [Worker](cross_double35_758.cpp) · [Packed implementation](packed_return_758.hpp) · [Audit](audit_double35_758.cpp)

```sh
c++ -std=c++17 -O2 -fsanitize=undefined -fno-sanitize-recover=all audit_double35_758.cpp -o /tmp/audit35
/tmp/audit35
```
