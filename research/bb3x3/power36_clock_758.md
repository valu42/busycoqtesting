# Raw clocks at the completed power-36 blank checkpoint

The [complete connected window chain](power36_final_758.md) places both
blank trajectories at

$$
A(1,3^{36}+112,032)=A(1,150,094,635,297,111,153).
$$

At that checkpoint both machines have taken more than
**$3.9169625267\times10^{49}$ raw Turing-machine transitions** and fewer
than **$5.2818905772\times10^{49}$**. The exact inclusive bounds are:

| Encoding | Lower bound | Upper bound |
|---|---:|---:|
| #758 | 39,169,625,267,626,016,222,638,085,861,124,527,996,579,493,163,120 | 52,818,905,771,297,598,690,448,450,091,510,656,735,026,479,051,906 |
| #153 | 39,169,625,267,626,016,222,638,085,861,124,527,996,579,493,112,413 | 52,818,905,771,297,598,690,448,450,091,510,656,735,026,479,001,199 |

These are bounds on the time of an attained live configuration, not a
claim that either machine has halted. Halting from blank remains open.

## Clock proof

Start with the independently checked
[doubled-power-35 clock interval](DOUBLED_POWER35_758.md). Apply the
existing [common-word timing method](CROSSING_CLOCK_758.md) on consecutive
seed intervals of width $10^{13}$ from that checkpoint to the power-36
gate. Where both parities share a guarded return word, it bounds cost per
seed gain. The certified angular potential gives the upper bound on
the other intervals. The same calculation applies to the simple-word
gate through the final lower cut $3^{36}-76$. The global potential covers
the remaining short flight to the exact gate merger.

The common-word calculation covers
46,623,523,094,855,066 of the 48,301,640,827,624,441 seed positions before
the gate, and every one of the 1,729,904,271,219,656 positions in the gate
interval. The calculations use integer and rational arithmetic.

The timing method permits at most 100,000 seed units between selected
resets. The unchanged crossing worker uses a launch, at most 256 packed
groups, and at most 5,000 subsequent groups. Each group uses at most two
counter calls. Its symbolic range checker instead allows at most 10,000
calls after its launch. Bounding both the launch and any final odd
normalization by 40 calls gives fewer than 10,600 calls in either case.
Since mass increases by at most nine per call and mass at a reset is
$2s+1$, this is less than the required 100,000 seed units. The direct gate
words have seed gains at most 101. Thus the timing allowance holds
through every part of this connected passage.

The corresponding #153 clock differs by the already established 50,707
raw steps. This offset is retained exactly in the second table row.

## Reproduction

```sh
python3 power36_clock_758.py
python3 power36_clock_758.py --replay-previous
```

The [clock verifier](power36_clock_758.py) first checks all 4,831 window
certificates and the final gate merger. It refuses a blank-orbit clock
claim if the connected crossing proof is incomplete. It then rechecks
the angular potential, guard endpoints, and the new timing sums. The
second command also recomputes the incoming doubled-power clock instead
of using its previously verified bounds. Full crossing-worker replay is
documented in the connected-chain proof.
