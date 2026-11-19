# A forward checkpoint for the #758 and #153 orbit

Every A(1,c) with **1,079,817,520,208,950 ≤ c ≤ 1,080,000,000,000,000** reaches **A(1,1,080,000,000,055,450)**. The lower endpoint is the common checkpoint in [the preceding interval proof](CONFLUENCE.md).

The endpoint comparison in that proof works for longer branch sequences. When two endpoints take the exceptional branch E before their return, a = c + 2 for both. Because a is nonincreasing and c is nondecreasing across seeds, this forces equal endpoint states. All intermediate states coincide there, so E preserves the interval proof. Any mismatch, a halt at either endpoint, or a step limit causes the checker to split the same-parity seed interval. A singleton that cannot be certified fails the run.

The checker batches the initial common J steps. Writing u = a+1, the result after k steps is a′ = 3ᵏu−1 and c′ = c−u(3ᵏ−1)/2+2k. The sufficient bound 3ᵏu ≤ 2c+u implies that a ≤ c when each step starts. It suffices to check the smaller input c since a begins constant for each seed parity.

| Seed parity | Certified intervals | Largest upper bound on the increase in c at first return |
|---|---:|---:|
| Even | 1 | 71 |
| Odd | 196,904,171 | 801 |

All covered seeds return to a = 1 with a strictly higher c. They eventually leave the interval. The first return that crosses its upper boundary must start among its last 801 seeds. Applying the original two-counter rules one at a time to these seeds gives 47 distinct exits, from 1,080,000,000,000,003 to 1,080,000,000,000,136. They coalesce at the stated checkpoint along 2,175 distinct first-return edges.

The C++ checker covers every seed in the interval via recursive disjoint bisection. Its optional arguments set the inclusive endpoints for a new range. The separate Python exit check verifies the stated range using the standard two-counter implementation. Run both from this directory.

```sh
c++ -O3 -std=c++17 cover_frontier.cpp -o /tmp/cover_frontier
/tmp/cover_frontier
python3 check_frontier_exit.py
```

The result certifies a finite segment of the orbit. It leaves the connection to a halting configuration open.
