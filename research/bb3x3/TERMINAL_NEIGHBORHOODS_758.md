# Which nearby reset seeds lead to each of 257 candidate pairs?

The large halting reset $H$ has a much larger verified local basin than any of the other 256 direct-halting pairs in the [fixed candidate list](mixed_terminal_windows_758.tsv). For each listed lower seed $K$, take the **same 5,000,003 consecutive starts** $A(1,s)$ with $K-5,000,000\le s\le K+2$. A start counts as a hit if it halts before any reset strictly above $K+2$. Both target seeds themselves are included. No other starting seed has a direct halt on its first excursion in any of these neighborhoods.

| Target | Starts that hit in its window | Fraction | Longest contiguous run of hits in its window |
|---|---:|---:|---:|
| $H-2,H$ | 3,837,489 | 76.7497% | 1,596,948 |
| Best other target (98-digit lower seed beginning 6703197334) | 29,620 | 0.5924% | 64 |
| All other 256 targets combined | 105,592 across their 256 windows | 0.00825% | 64 |

At 224 of the other 256 targets, no two consecutive starts hit. For each of these 256 pairs, every hit lies at distance at most 419,991 below its lower seed. An orbit from blank that ever reaches one of their listed reset seeds must therefore make a single excursion of **at least 1,017,780 counter calls**. Its reset before crossing the bypass interval is at most $K-5,000,001$. Its next reset above the interval is at least $K-419,991$. Each continuing counter call adds at most nine to the mass $a+2c$, and the mass at a reset is $1+2s$. This lower bound concerns a trajectory reaching the specific reset pair.

At $H$ the other 1,162,514 starts in the tested window reach a reset above $H$ alive. They all visit the same [later checkpoint](AFTER_TARGET_758.md). Combining this with the [contiguous basin](LOWER_SCALE_GATES_758.md), at least **33,533,928,120,845 of the 33,533,929,283,359** reset seeds in $[H-33,533,929,283,358,H]$ are proved to halt. Uniform sampling *inside that interval* gives a lower bound of 99.99999653%. The blank start is fixed. How it reaches this scale, and in particular whether it visits a reset in the interval, remains unresolved. The 257 targets come from the enumerations described in the [mixed-terminal search](MIXED_TERMINALS_758.md).

The H frequency also depends on the radius chosen. For $K=H-2$ the nested windows $[K-R,K+2]$ give the following exact counts. The [independent Python replay](check_terminal_radii_758.py) uses the original first-return function.

| Radius $R$ | Starts in the window | Hits |
|---:|---:|---:|
| 100 | 103 | 2 |
| 1,000 | 1,003 | 6 |
| 10,000 | 10,003 | 284 |
| 100,000 | 100,003 | 16,102 |
| 1,000,000 | 1,000,003 | 434,304 |
| 5,000,000 | 5,000,003 | 3,837,489 |

## Verification

For each target enumerate distances $d=K-s$ from $-2$ upward. Compute the first return from $s$ or find its halt. A direct halt is a hit. A positive reset gain $g$ gives precisely the result previously stored at $d-g$; if $d-g<-2$, the pair is bypassed. This proves the result by induction and tracks the largest run of consecutive hits. At the $H$ pair this calculation covers all 5,000,003 inputs. The first jump run is batched using $p=3^m$ for odd seeds or $2\cdot3^m$ for even seeds. Its final state is $A(2p-1,s+2m+4[s\text{ even}]-p+1)$, with $m$ maximal for a positive right counter. Subsequent counter updates use arbitrary-precision integer arithmetic.

When 5,000 consecutive starts have already bypassed the pair, the checker can certify all greater distances together. For a same-parity interval of starts it compares the endpoint words. A common initial jump count and a common ordinary suffix through the even return give a later reset at each intermediate seed. The first counter stays between the two endpoint values in reverse order, and the right counter in forward order. The common guards follow by the [ordered-endpoint argument](COVER_758.md). The checker uses the larger mass charge of nine for each bulk update, verifying an increase of at most 5,000 in the seed. Where the word comparison fails it bisects; a singleton is checked by its exact first return, including any exceptional move. Induction again proves bypass, since no selected reset can jump over the 5,000 excluded seeds. Any earlier intermediate reset in such a certified word also has smaller gain and preserves the argument.

The original counter map was also replayed independently through all 403,200 examined starts at the strongest other target, confirming its 29,620 hits, maximum run of 64, and final offset 398,197.

The [table](terminal_neighborhoods_758.tsv) records the lower target, hit count, widest run, distance of that run's far endpoint, and distance of the furthest hit found inside the window. The verifier takes an optional one-based target row. From this directory:

```sh
c++ -std=c++17 -O3 terminal_neighborhoods_758.cpp -lgmpxx -lgmp -o /tmp/terminal_neighborhoods_758
/tmp/terminal_neighborhoods_758 10
/tmp/terminal_neighborhoods_758 > /tmp/terminal_neighborhoods_758.tsv
tail -n +2 terminal_neighborhoods_758.tsv | diff - /tmp/terminal_neighborhoods_758.tsv
```
