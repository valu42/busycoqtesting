# The exact #758 crossing of the second candidate pair

For $K=2{,}031{,}355{,}966{,}425{,}479$, **the consecutive blank-tape resets on either side of the pair $K,K+2$ are $K-39$ and $K+41$**. The exact outgoing parameter is **2,031,355,966,425,520**. This chooses one of the 15 previously certified possibilities.

Start at cut 1,927,938,094,216,160, at the end of window 1202 (zero-based) in the [second crossing section](BLANK_CROSSINGS.md). Both the scalar and accelerated checkers send its full 5,001-seed incoming window to reset 1,928,257,804,717,219. Even if we widen this result to the entire interval from 1,928,257,804,717,083 through 1,928,257,804,722,083, the original counter rules send every seed to the same reset **1,928,257,804,761,237**. The local verification traces 6,249 distinct first-return edges.

| From the common reset | Exact first-return calculation | Ending reset parameter |
|---|---:|---:|
| Initial bridge | 64 ordinary returns | 1,928,257,804,768,921 |
| Repeated 17-return segment, total gain 1,536 per segment | 26,013,946,962 repetitions | 1,968,215,227,302,553 |
| Connecting bridge | 20 ordinary returns | 1,968,215,227,304,800 |
| Repeated single-return segment, gain 80 | 789,259,239,008 repetitions | 2,031,355,966,425,440 |
| Crossing return | 1 ordinary return | 2,031,355,966,425,520 |

There are **1,231,496,337,447 first positive returns** from the common reset through the last row. Every return strictly increases its reset parameter.

For each edge of a repeated segment, write $s$ for its initial reset, $\delta$ for the translation (1,536 or 80), and $N$ for the number of repetitions. The verifier runs the original counter rules at $s$, $s+\delta$ and $s+(N-1)\delta$. At every step, both coordinates at the far input equal the first coordinates plus $N-1$ times their respective differences between the first two inputs. These differences preserve every required congruence. The branch inequalities and equalities are linear, so their validity at both extremes certifies them at every intermediate input. The active update is affine on these residues, establishing the same identities at the next step. Each interior first counter stays strictly above 1 or identically zero. The last states are therefore first returns, and their output parameters differ by the original translation. The last edge of each segment lands exactly at the next translated start.

Run the [verifier](exact_second_758.py) in the same directory as the counter sources. Its default command compiles the fast crossing checker for the extra incoming window and checks all subsequent arithmetic. The preceding blank-to-window proof is supplied by the [blank crossing driver](check_blank_crossings.py).

~~~sh
python3 exact_second_758.py
~~~
