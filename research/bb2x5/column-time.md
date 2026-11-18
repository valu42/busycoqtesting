# An exact blank checkpoint and raw clock for line 26

Start `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA` in A at coordinate 0 on the two-way all-zero tape. After **566,255,088,944,246,173,560,939 defined instructions**, A scans the blank at **−434,455,632,153**. There are 173 ordinary pairs. Their packed unsigned counters, least significant pair first, are

```text
u = 0x1497fd17f9ddbcff1becf8
e = 0x2403e802f8d5ac2a11a4b8
```

This specifies the entire tape. If the head is at −n, the cells −n+1 through 0 contain 4. Cells 1+2i and 2+2i encode the bits 1−uᵢ and eᵢ respectively, writing physical 1 for a set bit and 4 for a clear bit. Cell 347 contains the terminal 3. All other cells are blank. The top 87 pairs have uᵢ=eᵢ=0. This endpoint is the end of tick 54,306,954,019 in the [first-arrival calendar](column-phases.md#extension-through-cut-84). Its last dangerous carry stopped at pair 85, so **p(85)=173** as well. The leading scalar gaps at cuts 84 and 85 are 345 and 346. The decision from blank remains open.

The [record-gap continuation](column-records.md) extends this checkpoint to 205 pairs and includes an exact raw clock and full tape.

## Converting ordinary visits to elementary time

The [physical derivation](research-log.md#line-26--one-inequality-decides-a-finite-halt) gives the blank entry in five instructions and two trips per epoch. During epoch n, the two trips share three guard instructions, A0, A1, A2. Each trip traverses ⌊n/2⌋ aligned `44` pairs of the leading run, at six instructions per traversal including the return. The remaining instructions are attached to individual data-pair visits. Write a and b for the two safe arrivals, d for the dangerous one. The elementary forward and return rows give these costs on an ordinary occupied pair.

| Arrival | Initial bits | Outcome | Defined instructions |
|---|---|---|---:|
| a | any | pass | 6 |
| b | u=0 | pass | 4 |
| b | u=1 | stop | 3 |
| d | u=1 | pass | 6 |
| d | u=0, e=1 | pass | 4 |
| d | u=0, e=0 | stop | 3 |

A fresh pair reached by a costs 11, and by b costs 9. In either case this is five more than its ordinary visit in the initial bits (0,0). A fresh d reaches the undefined B3. The following formula applies to any prefix of T successful ticks from blank. The cited calendar establishes success throughout both reported checkpoints.

Let M denote the final number of allocated pairs. On the *all-ordinary* tape count the individual letters reaching cut j during the T ticks as Aⱼ, Bⱼ, Dⱼ. Set Sⱼ=2Aⱼ+Bⱼ and

$$
 V_M=\sum_{j=0}^{M-1}(S_j+2D_j),\qquad
 U=\operatorname{popcount}(u),\quad E=\operatorname{popcount}(e).
$$

Here U and E count set bits in the full packed values, including the three fixed low pairs. At a tick boundary those three pairs have returned to zero. The exact elementary time is

$$
 R(T)=192T^2-8T+3V_M+U+2E+7M-3M^2+5.
$$

To prove it, first do the accounting on one ordinary pair j, starting from zero bits. Every b flips u and passes on its odd-numbered visits. Its total time is (7Bⱼ+uⱼ)/2. Each d with u=0 flips e. There are Dⱼ−Dⱼ₊₁ stops, and Dⱼ−Dⱼ₊₁−eⱼ visits that clear a set e. Starting from a charge of six per d, subtract three for each stop and two for each clear. This gives Dⱼ+5Dⱼ₊₁+2eⱼ. Safe output counts satisfy

$$
 A_{j+1}+B_{j+1}=A_j+\lceil B_j/2\rceil=(S_j+u_j)/2.
$$

There are 8T original a and 8T original d inputs at cut zero. At cut M the ordinary totals are M letters a and nothing else. Indeed every allocation wraps into the virgin tail as one a and no physical arrival has entered the still-fresh pair at cut M. Summing the safe costs 6Aⱼ+(7Bⱼ+uⱼ)/2 and using the preceding equality gives 3ΣSⱼ+8T+U−M. Summing the d costs gives 6ΣDⱼ−40T+2E.

At every cut j<M delete the first j ordinary a visits. Those are the virtual visits produced when the j lower pairs were allocated. Each cost six, and left the virgin bits unchanged. Add five on each of the M real allocation visits for its terminal action. Finally sum 3+12⌊n/2⌋ over n=1,…,8T, obtaining 24T+192T², and add the five blank-entry instructions. Collecting the terms proves the formula.

## Computing the finite sums and checking the tape

The first three cuts contribute 72T to V. In each tick their ordinary period words are four copies of `aadd`, four of `aad`, and two of `aabbd`, respectively. Above them one tick is nine scalar P followed by Q, with P=b and a=P². A message consisting of g safe tokens and a final dangerous flag q contributes exactly g+2q at every cut it enters. The [paired transfer](column-phases.md#coordinates-and-the-scalar-word) gives the outgoing message and updated bits. This recovers every ordinary visit in the sum regardless of how successive safe tokens are grouped.

For a low calendar cut B, precompute its complete timestamped period. At a cut below B, count whole periods together with the part of the final period up to the target tick. Include any P following its last emitted Q. To propagate this unfinished gap, replay at most three whole lower periods and the residual prefix on the next ordinary pair, then send the lower unfinished gap as P alone. Four whole periods restore that pair and end in an emitted Q. This also recovers every final digit strictly below B. Above B feed the timestamped messages to groups of four pairs, retaining the four bit pairs and the sum of the four visit counts. Stop at a fixed accounting cut L beyond the real tape. Each of the L−M unallocated pairs has seen M virtual a, so V_M=V_L−2M(L−M). The output at L is 2M scalar P. The program checks the absence of Q there and the virgin upper bits. The largest visit totals fit unsigned 64-bit arithmetic on the specified interval. Python evaluates the quadratic clock using unbounded integers.

Two calculations with B=17 and B=18 agree on V_M=6,299,606,942,741, both packed counters and the elementary time. The calendars in the [first-arrival proof](column-phases.md#extension-through-cut-84) place the first Q at cut 84 on this tick. The index of the lowest set bit of the final e outside u is 85, the stop of this Q. As no earlier Q reached 84, this is also the first Q at cut 85. The virgin pair at 84 passed it, so its incoming safe gap was odd, namely 2·173−1. It emitted 346 P. The [common clock](column-reserve.md#one-clock-for-all-blank-first-arrivals) independently recovers both gaps from the endpoint.

The checker compares every one of the first 64 computed tapes and times with a literal two-state interpreter. A second check counts individual physical pair trips and compares four further checkpoints through tick 12,345, at 29,264,811,755 instructions.

## Bounds that hold beyond the computed checkpoint

The ordinary process admits a lower bound on the first time a dangerous carry can reach a new cut. For every $s\ge0$, through root tick $4^s$ **no** $Q$ can arrive at cut $3+s+2\cdot3^s$. In particular the first-arrival time for cut $3+k$ is $\Omega(k^{\log_3 4})$. This is a statement about the total ordinary process and makes no assumption about physical survival.

Indeed, cut $3+s$ receives exactly $3^s$ dangers and $9\cdot3^s$ safe scalar tokens in its first complete period of $4^s$ ticks. Start the counters to the right of that cut at zero. After $q$ dangers the local $e$ has bit length at most $2q$. Even with intervening safe tokens the local $u$ has bit length at most $2q+1$, since the safe selector is $2e+1$. The next $Q$ stops no higher than the first position above both supports, at index at most $2q+1$. This proves the bounds by induction, including the initially empty counters. Thus the last of $3^s$ dangers stops no higher than local index $2\cdot3^s-1$. For the asymptotic claim take the largest $s$ with $s+2\cdot3^s\le k$.

There are also uniform time estimates on all *successful* blank prefixes. Write $\alpha=\log_4 3$. The exact raw clock satisfies
$$
 R(T)=192T^2+O(T^{2\alpha}),\qquad
 R(T)\ge192T^2+340T-O(T^{\alpha}+\log^2(2T)).
$$
To see the upper bound, take $s=\lceil\log_4 T\rceil$. At cut $3+s$ at most $9\cdot3^s$ safe and $3^s$ dangerous tokens have arrived. At most every other safe token can wrap, since every safe token flips the first upper $u$ bit and every second one stops there. Thus $M\le\lceil9\cdot3^s/2\rceil$. There are at most $10\cdot3^s$ physical arrivals at this cut, and each can visit at most $M$ physical data pairs. Below this cut the sum of visit counts is $O(T+3^s)$, by summing at each cut $3+i$ at most $10\cdot3^i(1+T/4^i)$ visits. The three lower cuts contribute $O(T)$. An occupied visit costs at most six, with at most five extra instructions at each allocation. This proves the upper estimate by adding the guard and blank-entry time.

For the lower estimate take $s=\lfloor\log_4 T\rfloor$ and $B=3+s$. The $B$ low pairs exist by time $T$ on any successful run, since the complete period at cut $B$ ends in a passing $Q$. The three lowest ordinary pairs cost exactly $183T$ in total by the physical rows. The ordinary pair at cut $3+i$ costs $133\cdot3^i$ per $4^{i+1}$ ticks. Over that period it receives $12\cdot3^i$ letters a, $12\cdot3^i$ letters b, and $4\cdot3^i$ letters d, emits $3\cdot3^i$ dangers, and returns to zero bits. Discard the costs of the incomplete periods. Subtract the $3B(B-1)$ cost of the virtual visits deleted in those $B$ cells. Together with the guard this gives the explicit lower bound
$$
 192T^2+207T+5+
 133\sum_{i=0}^{s-1}3^i\left\lfloor\frac{T}{4^{i+1}}\right\rfloor
 -3B(B-1).
$$
Using $\lfloor x\rfloor\ge x-1$ and summing the two geometric series gives the claimed estimate. Neither bound decides whether infinitely many physical ticks succeed.

From this directory, use Python 3.10 or later and a C++20 compiler, with assertions enabled.

```sh
c++ -O3 -std=c++20 column_raw_time.cpp -o column-raw-time
python3 column_raw_time.py ./column-raw-time
python3 column_raw_time.py ./column-raw-time --extended
```

[Visit counter](column_raw_time.cpp) · [Raw-time and literal-tape checks](column_raw_time.py) · [Observed output](column-time-verification.txt)
