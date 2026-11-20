# From the doubled power-35 checkpoint toward power 36

**The connected blank prefix now reaches the exact reset 100,583,090,198,237,340.** Seven [additional window receipts](blank_bridge_758.md) extend the chain through grid cut 52. Together with the existing certificates, 4,129 of 4,831 windows are certified and 702 remain open. Run `python3 blank_bridge_758.py` to check this extension; the earlier standalone checker below reads only its original receipt archive.

## Initial continuation and original grid

Starting at the doubled-gate reset $A(1,100{,}063{,}090{,}198{,}154{,}948)$, machines #758 and #153 both reach the exact reset **100,073,090,198,235,044**. The [complete doubled-35 crossing](DOUBLED_POWER35_758.md) establishes this starting configuration on both blank orbits.

The next gate begins at seed **148,364,731,025,779,389**. Reaching its 5,001-seed entry strip would force the exact reset **150,094,635,297,111,153** by the power-36 gate merger. The regular grid from the doubled checkpoint to that strip has 4,831 windows of width $10^{13}$, with the final window shortened. Identical guarded words at the two even endpoints certify 4,095 of these windows. Six computed crossings certify the first regular window as well. This reduces the original computation to **735 further windows** requiring individual return evaluations. The regular receipt table stores completed windows from this set, and the checker reports the connected prefix and remaining count. [Checker](power36_followon_758.py) · [Initial receipts](power36_initial_758.tsv) · [Regular receipts](power36_regular_758.tsv)

## Why the window chain applies

Let $P=3^{35}$. In the [doubled-to-single corridor](POWER_GATES_758.md), every odd reset has a single return to an even seed, with gain 75 or 77. For each regular window $[a,b)$, take the first and last even seeds. When they take the same ordinary word through a live return, opposite counter ordering supplies the same guards to every intervening even seed. Every bulk adds at most nine to $a+2c$. The resulting bound on the normalized even-to-even reset gain, including a possible odd return, is at most 5,000 in each accepted window. Monotone growth then takes every incoming reset in $[a,a+5000]$ to an even reset in $[b,b+5000]$. The word test allows an earlier intermediate reset. The trajectory still reaches the certified later one.

For the initial regular window the [even-power worker](cross_even_power_758.cpp) uses six successive cuts at offsets $10^8$ through $10^{13}$. At offset $10^{11}$ there is a single possible exit, **100,063,190,198,155,040**. At offset $10^{13}$ the outgoing even seeds are enclosed between 100,073,090,198,154,948 and 100,073,090,198,155,214. The checker follows each of the 134 even seeds in that range to the stated common reset, verifying 2,728 distinct first-return edges.

At exponent 35 we group at most three bulk pairs per packed stage. Its largest numerator is bounded by $4^3(3P+50000)/2<2^{64}$, as required before the unsigned shift. The existing [paired transition proof](EVEN_POWER_758.md) then applies with the same checks throughout this corridor. The exponent-35 audit compares 1,179,648 even inputs and their adjacent odd inputs against literal counter transitions, and checks 100,020 incoming seeds through small windows. At the far gate the even and odd endpoint words each have odd gain bounded by 101 and 77 respectively. The [power-gate calculation](power_gates_758.py) merges its exits in 1,455 edges.

## Further exact checkpoints and verification time

At 475 of the 4,832 grid cuts, every one of the 5,001 possible incoming reset seeds merges into a single specified even reset. These include 63 of the first 128 cuts, with cuts 0 through 34 consecutive. The evidence is a positive certificate for each listed cut. Normalize each odd seed to even with the proved 75-or-77 gain. Advance the smallest remaining even seed using the original counter map, normalize an odd output, and merge equal results. Replaying the 475 certificates costs 1,731,488 normalized even-to-even edges in total. The largest costs 6,745. A connection to any listed strip therefore determines a specific next reset, and the crossing proof still determines which strips the starting orbit reaches. [Full-strip mergers](power36_strip_mergers_758.tsv)

To estimate the cost of the 735 individual windows, sort their indices and divide the list into eight consecutive groups, of sizes 91 and 92 (seven groups of 92). Use one uniformly selected index from each group, with Python's `Random(75836)`. The sampled indices are 141, 315, 939, 1523, 1888, 2437, 4253 and 4652. On this host the original worker took 22.04, 18.46, 17.48, 18.39, 13.66, 15.54, 30.50 and 11.07 CPU seconds, respectively. Weighting by group size estimates 301 billion normalized return evaluations and **3.75 CPU-hours** for the original 735 windows. With eight dedicated cores and ideal scaling that is about 28 minutes. The actual elapsed time depends on host load and the unsampled windows. A separate timing of row 1 gave 273,656,056 normalized evaluations in 13.99 CPU seconds. These are verification costs for this finite bridge.

From the research directory, run the following commands to check the symbolic grid, replay the six initial crossings, and test the worker against the literal rules.

```sh
python3 power36_followon_758.py --checkpoints
python3 power36_followon_758.py --strip-mergers
c++ -O3 -std=c++17 -DPOWER_EXPONENT=35 cross_even_power_758.cpp -o /tmp/cross36
python3 power36_followon_758.py --worker /tmp/cross36 --replay
c++ -O3 -std=c++17 -DPOWER_EXPONENT=35 audit_even_power_758.cpp -o /tmp/audit36
/tmp/audit36
```

This command computes all outstanding windows in parallel, saves every successful receipt as it finishes, and writes a combined regular table. The same command resumes after interruption using the existing receipt directory.

```sh
python3 power36_followon_758.py --worker /tmp/cross36 --rows /tmp/power36-rows --fill --jobs 8 --export power36_regular_758.tsv --require-complete
```
