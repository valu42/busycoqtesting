# From power 36 to the one-bulk halting pair

Starting at $A(1,3^{36}+112{,}032)$, #758 and #153 both reach reset **150,104,635,297,137,581**. This first crossing spans $10^{13}$ units in the reset seed. At the far end of the proposed grid, every reset in its last 5,001-seed input strip reaches **270,170,343,534,399,442**. From there the trajectory visits consecutive seeds $q-48$ and $q+102$, passing the halting pair $q,q+2$ alive, then reaches **300,189,270,594,119,530** above $2\cdot3^{36}$. Here $q=270{,}170{,}343{,}534{,}598{,}339$. Connecting these two ends requires the remaining intermediate windows. [Verifier](double36_frontier_758.py) · [Window receipts](double36_frontier_758.tsv.gz)

| Segment | First returns | Raw transitions |
|---|---:|---:|
| Last grid exit to $q-48$ | 1,503 | 508,686,106,656,607,074,773,333,065,887,204,685,015 |
| $q-48$ to $q+102$ | 1 | 280,792,859,414,564,088,211,790,599,247,683,383 |
| Last grid exit through the doubled-power checkpoint | 375,236,588,244,450 | 54,355,875,010,564,556,531,051,350,392,993,602,744,906,412,070,046 |

## Why the pair is missed at the far end

Put $P=3^{36}$. After the 36 initial jumps from an odd reset $s$, the counters are $a=2P-1$ and $c=s-P+73$. With $i=\lfloor(c+1)/4\rfloor$, the next bulk yields a gap $a'-c'=2P-10i-9$. The halting gap one would require $5\mid P$. Gap three gives $i=(P-6)/5$, an odd integer as required by the right residue. The sibling values $c=4i-1,4i+1$ give precisely $s=q,q+2$, with $q=\lfloor9P/5\rfloor-78$. Literal first returns confirm both halts.

For an even seed the corresponding launch is the opening move and 35 jumps, with $h=(a+1)/2=2P/3$ and $c=s-h+75$. The first even seed following just one bulk and a live return is $h+4\lfloor2h/10\rfloor-76=180{,}113{,}562{,}356{,}398{,}866$. Indeed the even left counter after that bulk is at most the new right counter exactly when $10\lfloor(c+1)/4\rfloor+8\ge2h-1$. The gain there and throughout the common word is $79+(s\mathbin{\&}2)$. The sharp gate covering **both parities** starts at $q+3$. The first even and odd seeds there have the respective one-bulk return words; ordered endpoint checks extend the words to the existing [doubled-power gate](POWER_GATES_758.md). The preceding seed $q+2$ halts.

The actual proof window ends slightly below these thresholds at $q-199{,}000$. The 5,001 possible entries there merge at $270{,}170{,}343{,}534{,}454{,}530$ in 9,601 distinct edges, independently of the preceding window. The final grid receipt further reduces those entries to the single exit above. It reaches the merger in 440 returns. The [power skip](POWER_BOUNDARY_758.md) accelerates 375,236,588,242,473 further resets in its fixed-word portion, using 17 residue evaluations. All raw durations in the table refer to the real counter trajectory from the stated starting reset.

## Checking or extending the grid

The 12,008 regular windows run from $3^{36}+112{,}032$ to $q-199{,}000$ in strides of $10^{13}$, with a shorter last window. The endpoint words on both seed parities close 9,773 windows immediately. Allowing the published worker's interval subdivisions and parity closure certifies **10,010 windows without individual first-return evaluations**. The other **1,998** request an individual evaluation. The compressed table also contains six individually computed windows, leaving **1,992 open** in this handoff. The first regular window encloses the next reset in 177 consecutive seeds. All 177 meet at the stated starting-segment checkpoint after checking 715 first-return edges.

Four sampled windows give a rough estimate for the original 1,998 difficult cases. Divide their sorted indices into four nearly equal groups and select one per group with Python's `Random(75837)`. Rows 306, 3537, 7883 and 10661 took 1.85, 26.99, 17.42 and 33.99 CPU seconds on the test host, using 41.4, 719.3, 458.5 and 927.4 million individual first-return evaluations. Weighting by group size estimates **11.1 CPU-hours** for the 1,998 cases, equivalent to roughly 84 minutes on eight dedicated cores at ideal scaling. The wide spread limits the precision of this estimate. Separate runs of the first and last windows took 40.78 and 17.74 CPU seconds, respectively.

The maximal initial jump count grows monotonically with the seed within each parity. Endpoint checks prove that every even input in the grid takes the initial even move and 35 jumps, and every odd input takes 36 jumps. Use three packed bulk pairs per stage at this exponent. The greatest possible numerator is at most $64(q-199000+50000)/2<2^{64}$, so the worker's unsigned shift recovers the exact value. The ordinary worker's largest initial jump threshold also lies below $3^{36}$, which is present in its power table. The exponent-35 settings still use four pairs and keep their original input limit. An undefined-behavior-sanitized exponent-36 audit compares 2,048,000 first returns with the literal rules. [Packed updates](packed_return_758.hpp) · [Launch parameters](double35_prefix_758.hpp) · [Literal audit](audit_double35_758.cpp)

From the research directory the following commands check the two gates, inspect the connected prefix, and replay the singleton exit.

```sh
python3 double36_frontier_758.py --checkpoint 0
c++ -O3 -std=c++17 -DBB758_DOUBLE_POWER=36 cross_double35_758.cpp -o /tmp/cross-double36
python3 double36_frontier_758.py --worker /tmp/cross-double36 --start 12007 --stop 12008
c++ -O2 -fsanitize=undefined -fno-sanitize-recover=all -std=c++17 -DBB758_DOUBLE_POWER=36 audit_double35_758.cpp -o /tmp/audit-double36
/tmp/audit-double36
```

The symbolic census can also be repeated without evaluating a single individual return.

```sh
c++ -O3 -std=c++17 -DBB758_DOUBLE_POWER=36 -DBB758_SYMBOLIC_ONLY cross_double35_758.cpp -o /tmp/census-double36
python3 -c "from double36_frontier_758 import symbolic_census; symbolic_census('/tmp/census-double36')"
```

This command fills missing windows, retaining each result as it finishes. Restarting it with the same receipt directory resumes the calculation.

```sh
python3 double36_frontier_758.py --worker /tmp/cross-double36 --fill /tmp/double36-rows --jobs 8 --save double36_extended.tsv.gz --require-complete
```
