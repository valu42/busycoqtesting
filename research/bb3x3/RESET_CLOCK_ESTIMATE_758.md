# How long would #758 take if its blank orbit reached A(1,H)?

**A numerical model estimates about $2\times 10^{415}$ original Turing-machine steps.** This forecast is conditional on reaching the particular reset $H=(3^{307}-8{,}282{,}708{,}212)/13{,}959{,}275$. The blank orbit might halt elsewhere or run forever. The estimate supplies no probability for any of these outcomes. If the two machines halt, #153 takes exactly 50,707 fewer steps. [Target and twin](RANKINGS.md)

The model estimates the clock between the proved blank reset $C=18{,}378{,}934{,}934{,}402{,}308$ and $H\approx 2.14467918\times 10^{139}$. The certified blank clock at $C$ is between $7.528\times10^{46}$ and $1.119\times10^{47}$ steps. Literal evaluation of the 307 calls from $H$ gives $2.792557974\ldots\times10^{279}$ steps. The unknown journey *to* the candidate accounts for essentially the entire estimate. [Blank clock](CROSSING_CLOCK_758.md) · [Terminal calculation](mass_clock_758.py) · [Checkpoint](FOURTH_GATEWAY_758.md)

## Numerical model

Let $R(s)$ be the next reset seed after $A(1,s)$ and $t(s)$ the exact raw transition count to that reset. The elapsed time across a connected series of resets is the sum of $t(s)$. Dividing this sum by the total increase in $s$ gives the observed time per unit increase in seed. The estimator divides $[C,H)$ into equal-width strata. It estimates this local rate and multiplies it by the width of each stratum.

1. Draw a uniform integer in each stratum and take the even and odd seeds at or immediately above that integer. For each seed, execute eight first returns, then measure total time divided by total seed gain for the following sixteen returns. Redraw a pair if either sample halts. The program reports every such rejection. It raises an error if an excursion exceeds its computation budget.
2. Record the parity of the first return from each seed. When both parities map to the same output, apply unit weight to that parity. When both flip, weight them equally. When both preserve their inputs, carry the weights from the preceding stratum. Initially use the actual parity of the lower endpoint. These weights approximate which local paths the blank orbit would visit.
3. Integrate the weighted rates across the strata. The local simulations use the exact branch clocks. Selecting fresh seeds across different strata is the extrapolation. Long-lived residue effects beyond parity, rare long excursions, or an atypical connected orbit could change the answer. Variation between random grids measures sampling sensitivity only.

For fast, exact local timing, put $h=1,b=s$ for an odd seed. For an even seed the opening I call costs $14s+24$ and gives $h=2,b=s+4$. After $j$ leading J calls the counters are $(2h3^j-1,b+2j+1-h3^j)$. Another J is possible precisely when $3h3^j\le b+2j+2$. Summing the J cost $3a^2+5c+6$ over the maximal $k$ such calls gives
$$
12h^2\frac{9^k-1}{8}-17h\frac{3^k-1}{2}+(5b+14)k+5k(k-1).
$$
The verifier takes all remaining branches individually, including the return or terminal branch. Its startup checks compare the fast first return with literal counters on small seeds, power boundaries, and the candidate itself. [Original branch costs](timing_758.py) · [Estimator](reset_clock_estimate_758.py)

## Checks on connected orbit segments

The first three rows compare predictions with literal first-return clock sums at successive blank resets. The fourth uses the independently verified clock across the fourth crossing. The final row starts from a known escape just above the target and runs to its exact merger. The table uses 4,096 strata and random seeds 0, 1 and 2. The error ranges enclose the three grid results and have no probabilistic coverage guarantee.

| Seed interval | Actual elapsed steps, rounded | Observed relative error |
|---|---:|---:|
| 100,008 to 1,000,007 | $2.7778682\times10^{16}$ | +0.09% to +0.15% |
| 1,000,007 to 10,000,048 | $2.3616775\times10^{19}$ | −0.03% to +0.13% |
| 10,000,048 to 100,000,009 | $2.1360134\times10^{22}$ | −0.27% to −0.05% |
| 17,354,320,242,846,420 to 18,378,934,934,402,308 | $1.2878280\times10^{46}$ | +0.003% to +0.006% |

The fourth crossing spends almost its entire length in two corridors with fixed instruction words. Checks over the three smaller intervals exercise a different range of behavior. The post-target check uses 140-digit seeds, but covers only 0.059% of the target seed and lies in a corridor of fixed words. Its initial reset has no known connection to blank. On the whole interval from 100,008 to the fourth checkpoint, the model gives $8.70$ to $8.73$ times $10^{46}$, inside the proved bracket for the blank clock. The exact elapsed time across that interval remains open. [Fourth-crossing structure](BLANK_RETURN_PROFILE_758.md) · [Exact post-target clock](TARGET_CLOCK_758.md) · [Blank clock](CROSSING_CLOCK_758.md)

The three 4,096-stratum candidate runs return $2.1281$, $2.1526$ and $2.1455$, each times $10^{415}$. At 16,384 strata the corresponding values are $2.1448$, $2.1377$ and $2.1456$. Keeping 4,096 strata and increasing the local window to 32 initial returns and 64 measured returns changes each original result by less than 0.002%. All three configurations completed without a halting sample on the candidate interval. Only one significant figure seems warranted for the extrapolation.

~~~sh
python3 reset_clock_estimate_758.py --replay
python3 reset_clock_estimate_758.py --strata 16384
python3 reset_clock_estimate_758.py --burn 32 --keep 64
~~~
