# Extending the scale-10 halting interval for #758 and #153

Every reset $A(1,H-d)$ for **543,249,654,390,404 ≤ d ≤ 911,916,090,650,670** eventually halts. Here $H=(3^{307}-8,282,708,212)/13,959,275$. This adds **6,500,000,000,000 consecutive seeds** beyond the previous far edge and gives a total of **368,666,436,260,267**. At the first crossing of mass $a+2c>2(H-543249654390404)+1$, a reset in the preceding **81,925,874,724,503** counter calls now suffices to prove halting. Entry from the blank tape is open. [Previous scale-10 certificate](LOWER_SCALE_GATES_758.md)

The [manifest](outer_wall_758.tsv) contains 40 contiguous bands totalling 5,542,734,372 bisection nodes and 2,771,367,206 accepted leaves. At odd countdowns the established even-seed word returns with gain at most 615. At even countdowns, equality of the two endpoint words proves the intermediate seeds halt or make a first return bounded by that word. The exact reference caps the suffix below 10,000 calls, each gaining at most nine in mass. Together with its prefix and jump batch, its seed increment bound is below 50,000. Every nonterminal return from the extension therefore has strictly smaller countdown and lies above the scale-10 near edge. Strong induction joins every verified band to the previous corridor. A bypass must gain at least twice the width plus one in mass after its preceding reset, at no more than nine per call. [Universal endpoint argument](UNIVERSAL_758.md)

After any entry in this extended interval, fewer than $2.823\times10^{293}$ original Turing-machine steps remain. This uses the established terminal mass ceiling $V=2H+1258$, at least four mass units gained per continuing call, and the per-call upper bound $(V^2+30V+195)/3$. The [original total-time bounds](HALTING_TIME_758.md) still give $2.10448\times10^{414}<T<8.206\times10^{416}$ from blank if it enters this interval. The lower bound follows by evaluating the prior angular potential at $2(H-911916090650670)+1$.

## Integer matcher

The original [GMP verifier](gateway_758.cpp) independently reproduces every band. The [faster endpoint comparator](outer_wall_fast_758.cpp) uses signed 128-bit integer arithmetic when its guards separate the two possible outcomes. Both produce the same four-column receipt. To derive its error margin, write $u$ for the positive post-prefix left counter plus one, $k$ for the ensuing jump count, $m=2\cdot3^{307-k}$, and $A=13,959,275u$. The aligned physical left counter is $a=3^ku-1$. The exact target identity gives
$$
(2H)A-ma=m-2\cdot8,282,708,212u.
$$
The verifier checks $|A-ma/(2H)|<1$ and $|mW/(2H)-m|<1$ throughout its guarded pass, where $W=a+2c$. The value of $k$ follows from the sorted cutoffs $\lfloor2H/3^k\rfloor$. The alignment threshold uses $2H-2d+g+2$ in the original evaluator. In the accelerated range its difference from $2H$ is positive in magnitude and smaller than $3^k$; equality with the integer cutoff takes the exact path.

Suppose the current coordinate error is at most $e$. A jump maps $a$ to $3a+2$, so the new error is at most $3e+1$. After two bulks the exact left counter is $(9a-5W)/4-3e_1/2-g_1/2-e_2$, with $e_1,e_2$ either 2 or 4 and $g_1$ either 5 or 9. Using the integer quotient $(9A-5m)/4$ rounds downward. Its new error is at most $\lceil9e/4\rceil+3$. The comparator requires margins $3e+3$ and $9e+15$ before classifying the first and second guards. They cover the normalized mass variation, the bulk constants and the exceptional equality cases. An ambiguous guard, a long word, or a saturated error bound invokes the original GMP evaluator. The unbatched GMP comparator replayed the entire first band of 100 million steps in countdown distance (1,624,237 bisection nodes). Both comparators also agreed on four independent ten-million-seed checks; the first involved 267,191 bisection nodes. A separate comparison checked 20,000 endpoint signatures, including the first 8,000 even countdowns at the old far edge.

## How much of each previously bridged gap halts?

The original strip-transfer receipts also bound how many starting seeds in each gap can still be undecided. The bound is deterministic and counts reset origins. Blank follows one fixed trajectory.

| Gap before scale | Distinct distances | Proven halting, at least | Possibly undecided, at most |
|---:|---:|---:|---:|
| 8 | 26,827,143,426,691 | 26,204,211,785,319 | 622,931,641,372 |
| 9 | 80,481,430,280,063 | 79,298,902,285,795 | 1,182,527,994,268 |
| 10 | 241,444,290,840,183 | 238,790,434,528,865 | 2,653,856,311,318 |

In each [archived transfer](lower_scale_bridges_758.tsv) at least one possible exit survives. A successful common-word leaf admits all starts in its integer interval. Every continuation from such a start exits in the strip inserted by the algorithm, and every member of that strip leads to a halting seed by the rest of the transfer chain. Direct lookups likewise certify their actual starting seeds.

The traversal visits all children of every split in these rows. To see this, a still-live frontier cannot be empty at an intermediate call since it can never restart after becoming empty. On entering the first block it contains an input at the high edge. A direct block can overshoot its low edge by at most the recorded maximum gain. A common-word block inserts the whole exit strip, starting immediately below its low edge. Therefore on passing any block boundary the greatest remaining candidate is at worst one maximum gain below that boundary. This also follows by following the last input of a processed block when that input returns, or by preserving a preexisting candidate just below the boundary. In the rows counted here every elementary look-up continues (zero terminal branches in each receipt). Each child of a split has at least 125,001 integer positions, and each recorded maximum gain is at most 5,000. A whole child cannot be skipped.

Consequently a row with $v$ visited nodes has $(v+1)/2$ leaves. Each direct leaf has at most 250,001 positions. Each directly evaluated start is distinct inside a row because all positive transitions strictly decrease the countdown, and the worklist removes duplicates. Thus at most $250,001(v+1)/2$ minus the number of direct evaluations in that row can remain undecided. A single-node row covers its entire interval because its width exceeds the direct cap. Summing these upper bounds counts shared endpoints conservatively. The new totals use the existing exact receipts and can be reproduced immediately.

```sh
c++ -O3 -std=c++17 outer_wall_fast_758.cpp -lgmpxx -lgmp -o outer_wall_fast_758
python3 check_outer_wall_758.py --worker ./outer_wall_fast_758 --jobs 2
python3 check_outer_wall_758.py --gap-bounds
```

For an independent replay compile `gateway_758.cpp` to `gateway_758` and run `python3 check_outer_wall_758.py --row 1` or omit the row to check the full manifest.
