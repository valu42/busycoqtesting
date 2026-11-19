# Both blank runs reach the power-36 checkpoint

Starting at the [proved doubled-power reset](DOUBLED_POWER35_758.md), the blank trajectories of #758 and #153 reach **$A(1,3^{36}+112{,}032)=A(1,150{,}094{,}635{,}297{,}111{,}153)$**. All **4,831 regular windows** connect. Their final exit lies in the 5,001-seed entrance strip at **148,364,731,025,779,389**, whose trajectories merge at the stated reset.

Identical endpoint words certify 4,095 windows. Six shorter receipt-backed crossings compose the first window. The other 735 windows have numerical crossing receipts. The [regular table](power36_regular_758.tsv) has 737 rows because it also records independent crossings of two symbolic windows. The last 374 missing windows required **156,776,746,761 normalized return evaluations** in the crossing worker, including paths from different possible entrances. [Chain checker](power36_followon_758.py) · [Six initial receipts](power36_initial_758.tsv)

| Encoding | Raw transitions from blank, lower bound | Raw transitions from blank, upper bound |
|---|---:|---:|
| #758 | 40,012,539,094,432,622,425,761,039,078,783,022,163,296,725,878,663 | 50,608,957,723,627,340,180,750,709,167,530,934,478,033,830,181,741 |
| #153 | 40,012,539,094,432,622,425,761,039,078,783,022,163,296,725,827,956 | 50,608,957,723,627,340,180,750,709,167,530,934,478,033,830,131,034 |

Run `python3 power36_bulk_corridor_758.py --clock` for the complete receipt-chain check, the exact three-bulk segment timing and the tightened clocks at both this reset and the [following six-window checkpoint](DOUBLE36_FRONTIER_758.md). `python3 power36_followon_758.py --require-complete --clock` also checks the full grid with the earlier, wider clock bounds. The Python command checks coverage and containment of the archived numeric results and recomputes the symbolic words, mergers and clocks. The worker replay commands below recompute the individual numeric crossings. Both machines' eventual blank-tape fates remain open.

## Three exact bulk corridors on the blank path

Both blank orbits reach **$A(1,100{,}579{,}892{,}930{,}565{,}916)$**. Rows 28, 30, 31, 32, 33 and 34 of the regular receipt table certify the difficult crossings before cut 35 at $100{,}413{,}090{,}198{,}154{,}948$. The symbolic endpoint test covers row 29. Any of the 5,001 seeds in the new strip reaches the stated reset in **1,700,198,749,078 to 1,700,198,749,129 first returns**. The [corridor checker](power36_bulk_corridor_758.py) verifies the connection against the regular receipts.

Through the even seed $e=100{,}579{,}892{,}930{,}498{,}732$, every even seed in this corridor takes the opening update, 35 jumps, 13 bulks and a return. The endpoint counters bound every intermediate even input in opposite order. The minimum first counter before each bulk or jump exceeds one, so the final instruction gives the first return. Every bulk adds 5 or 9 to the mass. The resulting odd seed gains at most 135, then advances by 75 or 77 to an even seed. The even-to-even gain is at most 212. Enumerating the last 212 seed units gives 35 possible even exits, which coalesce in 1,240 literal first-return edges. Restricting to the 5,001 actual strip entrances gives just two of these exits. For this count the displacement of two first returns is periodic modulo $2^{14}$ because each of the 13 bulks uses one bit of precision from a right counter known modulo four. Repeated squaring of the residue transitions counts all pairs up to their last even input. Literal returns determine the remaining path.

At this common reset the #758 raw clock is between **11,838,458,173,511,211,482,968,407,317,939,796,133,592,905,661,006** and **15,477,415,402,902,052,567,966,318,480,033,313,646,404,995,083,394**. Subtract 50,707 at either endpoint for #153. The bound extends the doubled-power clock using the common-word rates. Each crossing witness has resets spaced less than 100,000 seed units apart. In a packed witness the initial launch and up to 256 prefix and 5,000 fallback groups each use at most two counter calls per group, followed by at most 77 seed units of normalization. A symbolic witness has at most 10,000 calls after launch. The corridor itself has even-to-even gain at most 212. Each counter call increases mass by at most nine.

The same argument at cut 78 uses eleven bulks from each even seed after its opening and 35 jumps. In this corridor the output is already even and has gain at most 126. The last even input is $101{,}233{,}452{,}157{,}379{,}468$. Its boundary has 27 possible exits and all meet in 926 first-return edges. From the 5,001 entrants at cut 78 only three exits occur, and every one reaches **$A(1,101{,}233{,}452{,}157{,}436{,}950)$** in **3,399,147,919,854 to 3,399,147,919,899 first returns**. Its #758 raw clock lies between **12,029,516,641,463,799,224,113,870,091,644,714,792,019,914,097,366** and **15,834,990,276,561,360,219,217,857,645,920,693,681,411,362,894,480**. The check compares the computed displacement for every residue it uses with literal first returns at the far end of each corridor. Both results describe finite portions of the blank trajectory.

The longest run of symbolic grid windows spans indices 2,464 through 4,212. At cut 2,464, from any of the 5,001 strip entrances the even word has just three bulks. It remains valid through seed 142,194,917,649,788,560. Its 17 possible even exits merge in 1,295 first-return edges at **142,194,917,649,902,128**. Eleven exits occur from the specified strip. Each entrance takes **198,770,766,496,212 to 198,770,766,496,274 first returns** to this checkpoint. In the cycle the first-return gains alternate between 86 and 90. Carrying the exact raw clock on both residues gives a duration from **10,008,882,320,792,462,921,809,643,614,479,063,065,790,190,824,028** through **10,008,882,320,795,622,214,370,521,408,577,381,386,855,966,625,542** raw transitions according to the entrance. The [quadratic clock sum](target_clock_758.py) applies because each fine return word is fixed on its class modulo 16. Adding the early clock bounds up to the possible entrance, this exact range for the passage, and the remaining clock bounds from the shared exit gives the tightened power-36 clock above.

The cycle structure also follows directly from the individual bulk charges. After the opening and $m$ jumps, write $y=(c+7)/2=s/2-3^m+m+6$. For $b$ bulks put $B=B_b(y)$, the sum of the parity bits of $y$ and its first $b-1$ iterates under $y\mapsto3\lceil y/2\rceil$. Each set bit adds four units of mass. The even seed's first return gains $2m+(5b+13)/2+2B$. For $b=4k+3$ this gives an even successor and $\Delta y=m+5k+7+B$. For $b=4k+1$, applying the short odd return gives $\Delta y=2m+5k+7+B+((y+k+B+1)\bmod2)$. These formulas apply whenever the indicated guarded word and short odd return are valid. [Bulk charge flags](BULK_DIGIT_CYCLES_758.md)

At $m=35$, exhaust all $2^b$ possible residues of $y$, comparing every computed gain with a literal return. In each case, following predecessors of the identified residue cycle accounts for all residues. The maximum cumulative seed gain before joining that cycle bounds the transient of any strip entrance. After allowing each odd initial seed its short return, both blanks complete at least the number of whole cycles shown inside the corridor. The physical seed strictly increases on every cycle.

| Bulks | Normalized edges per cycle | First returns per cycle | Physical seed gain per cycle | Maximum seed gain to cycle | Full cycles guaranteed from blank |
|---:|---:|---:|---:|---:|---:|
| 13 | 167 | 334 | 32,768 | 19,110 | 5,090,415,415 |
| 11 | 107 | 107 | 12,288 | 5,514 | 31,767,737,566 |
| 3 | 2 | 2 | 176 | 174 | 99,385,383,247,888 |

```sh
python3 power36_followon_758.py --worker /tmp/cross36 --replay --start 28 --stop 78
python3 power36_bulk_corridor_758.py --clock
```

## Why the window chain applies

Let $P=3^{35}$. In the [doubled-to-single corridor](POWER_GATES_758.md), every odd reset has a single return to an even seed, with gain 75 or 77. For each regular window $[a,b)$, take the first and last even seeds. When they take the same ordinary word through a live return, opposite counter ordering supplies the same guards to every intervening even seed. Every bulk adds at most nine to $a+2c$. The resulting bound on the normalized even-to-even reset gain, including a possible odd return, is at most 5,000 in each accepted window. Monotone growth then takes every incoming reset in $[a,a+5000]$ to an even reset in $[b,b+5000]$. The word test allows an earlier intermediate reset. The trajectory still reaches the certified later one.

For the initial regular window the [even-power worker](cross_even_power_758.cpp) uses six successive cuts at offsets $10^8$ through $10^{13}$. At offset $10^{11}$ there is a single possible exit, **100,063,190,198,155,040**. At offset $10^{13}$ the outgoing even seeds are enclosed between 100,073,090,198,154,948 and 100,073,090,198,155,214. The checker follows each of the 134 even seeds in that range to the stated common reset, verifying 2,728 distinct first-return edges.

At exponent 35 we group at most three bulk pairs per packed stage. Its largest numerator is bounded by $4^3(3P+50000)/2<2^{64}$, as required before the unsigned shift. The existing [paired transition proof](EVEN_POWER_758.md) then applies with the same checks throughout this corridor. The exponent-35 audit compares 1,179,648 even inputs and their adjacent odd inputs against literal counter transitions, and checks 100,020 incoming seeds through small windows. At the far gate the even and odd endpoint words each have odd gain bounded by 101 and 77 respectively. The [power-gate calculation](power_gates_758.py) merges its exits in 1,455 edges.

## Further exact checkpoints and verification time

At 475 of the 4,832 grid cuts, every one of the 5,001 possible incoming reset seeds merges into a single specified even reset. These include 63 of the first 128 cuts, with cuts 0 through 34 consecutive. The evidence is a positive certificate for each listed cut. Normalize each odd seed to even with the proved 75-or-77 gain. Advance the smallest remaining even seed using the original counter map, normalize an odd output, and merge equal results. Replaying the 475 certificates costs 1,731,488 normalized even-to-even edges in total. The largest costs 6,745. A connection to any listed strip therefore determines a specific next reset, and the crossing proof still determines which strips the starting orbit reaches. [Full-strip mergers](power36_strip_mergers_758.tsv)

The original computation used the following sample to estimate the cost of the 735 individual windows. To reproduce the historical estimate, sort their indices and divide the list into eight consecutive groups, of sizes 91 and 92 (seven groups of 92). Use one uniformly selected index from each group, with Python's `Random(75836)`. The sampled indices are 141, 315, 939, 1523, 1888, 2437, 4253 and 4652. On this host the original worker took 22.04, 18.46, 17.48, 18.39, 13.66, 15.54, 30.50 and 11.07 CPU seconds, respectively. Weighting by group size estimates 301 billion normalized return evaluations and **3.75 CPU-hours** for the original 735 windows. With eight dedicated cores and ideal scaling that is about 28 minutes. The actual elapsed time depends on host load and the unsampled windows. A separate timing of row 1 gave 273,656,056 normalized evaluations in 13.99 CPU seconds. These are verification costs for this finite bridge.

From the research directory, run the following commands to check the symbolic grid, replay the six initial crossings, and test the worker against the literal rules.

```sh
python3 power36_followon_758.py --checkpoints
python3 power36_followon_758.py --strip-mergers
c++ -O3 -std=c++17 -DPOWER_EXPONENT=35 cross_even_power_758.cpp -o /tmp/cross36
python3 power36_followon_758.py --worker /tmp/cross36 --replay --require-complete
c++ -O3 -std=c++17 -DPOWER_EXPONENT=35 audit_even_power_758.cpp -o /tmp/audit36
/tmp/audit36
```

For a modified or incomplete regular table, this command fills missing windows in parallel and saves receipts for resumption. With the complete table above it validates the existing entries. Use `--replay` to recompute the archived entries.

The same argument at cut 78 uses eleven bulks from each even seed after its opening and 35 jumps. In this corridor the output is already even and has gain at most 126. The last even input is $101{,}233{,}452{,}157{,}379{,}468$. Its boundary has 27 possible exits and all meet in 926 first-return edges. From the 5,001 entrants at cut 78 only three exits occur, and every one reaches **$A(1,101{,}233{,}452{,}157{,}436{,}950)$** in **3,399,147,919,854 to 3,399,147,919,899 first returns**. Its #758 raw clock lies between **12,029,516,641,463,799,224,113,870,091,644,714,792,019,914,097,366** and **15,834,990,276,561,360,219,217,857,645,920,693,681,411,362,894,480**. The check compares the computed displacement for every residue it uses with literal first returns at the far end of each corridor. Both results describe finite portions of the blank trajectory.

```sh
python3 power36_followon_758.py --worker /tmp/cross36 --rows /tmp/power36-rows --fill --jobs 8 --export power36_regular_758.tsv --require-complete
```
