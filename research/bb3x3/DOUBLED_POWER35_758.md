# The doubled power of three on the blank trajectory

The blank tapes of #758 and #153 reach the exact reset
$$
A(1,2\cdot3^{35}+155{,}534)=A(1,100{,}063{,}090{,}198{,}154{,}948).
$$
For both encodings the clock there lies between $1.17126785\times10^{49}$ and $1.51740901\times10^{49}$ raw transitions. A halt from blank remains open. [Previous blank checkpoint](POWER35_PARITY_BRIDGES_758.md) · [Full-grid and clock verifier](doubled_power35_758.py)

## The connected trajectory

Start at the [verified power-35 blank reset](POWER35_BLANK_758.md). The [grid](double35_frontier_758.tsv.gz) has 8,006 successive windows. Each row certifies that any entry among the 5,001 integer reset seeds beginning at its lower cut reaches a live reset in the recorded exit interval. Each such interval is inside the next window’s admissible entrance. The initial seed is exactly the first lower cut. Thus the actual orbit crosses every window and the final row pins its reset to the single integer **90,056,781,178,199,543**. The [window checker](double35_frontier_758.py) validates the indices, adjacent cuts and containment of each row. Its compiled worker replays the certificates on the original two-counter dynamics.

From this singleton, the rest of the flight is exact, including the number of raw Turing-machine steps.

| Stage | Ending reset seed | First returns |
|---|---:|---:|
| Enter the common-word corridor | 90,056,781,178,200,479 | 12 |
| Cross the corridor | 100,063,090,197,998,375 | 128,286,013,074,332 |
| Reach the doubled-power checkpoint | 100,063,090,198,154,948 | 614 |

The two short stages use literal timed first returns. Inside the corridor the [power skip](power_skip_758.py) proves one ordinary return word for each parity. The seed gains repeat modulo 64. On a repeated residue cycle, the raw clock per cycle is a quadratic in the repeat index, so summing the quadratic gives the exact elapsed time. This middle stage uses 156 timed-word evaluations. The three stages together take **128,286,013,074,958 first returns** and **2,064,800,570,200,302,539,140,344,402,993,658,760,635,001,476,898 raw transitions**.

## Clock from blank

Begin at the proved clock for reset 59,450,686,841,407,190. Apply the [common-word clock bounds](CROSSING_CLOCK_758.md) through the lower cut 90,056,781,178,199,398. The [packed window worker](double35_prefix_758.hpp) has a launch of at most 35 jumps, at most 256 packed groups, and at most 5,000 further groups per evaluated first return. A group costs at most two counter calls. The [symbolic range checker](reset_cover_758.hpp) allows at most 10,000 subsequent one-call updates after its launch. Each call increases $a+2c$ by at most nine. Both checks therefore bound the distance between selected reset seeds by less than the clock method’s 100,000-seed allowance. The clock calculation uses the global angular upper bound through the singleton seed, which is 145 above the final cut.

The eight-level rate test certifies common-word clock bounds on 29,765,427,990,510,600 of the 30,606,094,336,792,208 seed positions between the previous checkpoint and the final cut. Adding the exact three-stage duration gives the following integer bounds.

| Encoding | Raw transitions, lower bound | Raw transitions, upper bound |
|---|---:|---:|
| #758 | 11,712,678,510,935,380,362,058,354,962,364,020,304,705,317,061,556 | 15,174,090,093,546,359,518,174,460,234,028,779,946,439,652,299,731 |
| #153 | 11,712,678,510,935,380,362,058,354,962,364,020,304,705,317,010,849 | 15,174,090,093,546,359,518,174,460,234,028,779,946,439,652,249,024 |

Run in the BB(3,3) research directory. The first command validates the archived grid and checks the flight and clock. The other two replay all window computations from scratch.

```sh
python3 doubled_power35_758.py --clock
c++ -O3 -std=c++17 cross_double35_758.cpp -o /tmp/cross35
python3 double35_frontier_758.py --worker /tmp/cross35 --jobs 4 --require-complete
```

The [power-36 continuation](POWER36_FOLLOWON_758.md) starts at this exact doubled-power reset.
