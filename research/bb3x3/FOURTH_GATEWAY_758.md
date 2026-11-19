# A wide interval misses the fourth candidate halt

Let $K=17,430,344,744,167,562$. **Every reset with parameter from 17,354,320,242,904,343 through 17,363,959,236,929,600 reaches a reset above $K+2$ alive.** This is a block of **9,638,994,025,258** consecutive input seeds. Across the local window from $K-1,000,000$ through $K+2$, only $K$ and $K+2$ themselves halt before passing the pair. An orbit starting below this block that ever reaches either candidate must skip **all 9,638,994,025,258 reset seeds in one excursion**. Its last reset below the block is at most $B-1$ and its first reset beyond the block is at least $C+1$. Their mass difference is at least $2(C-B+2)$. Each continuing call increases mass by at most nine, so this excursion must last **at least 2,141,998,672,280 counter updates**. A second disjoint bypass interval, [17,393,401,372,077,661, 17,408,159,912,737,553], has **14,758,540,659,893** seeds. Its even word inserts one more J immediately before the last L; the same parity argument sends all starts into the odd corridor. Skipping this interval requires at least **3,279,675,702,199** counter updates between consecutive resets. The independent question is whether the exact [power checkpoint](POWER_GATES_758.md) $3^{34}+9,103$ reaches the large bypass block.

Put $B=17,354,320,242,904,343$ and $C=17,363,959,236,929,600$. Every odd seed $s$ from $B$ through $K+1$ has the first-return word $J^{34} L^7 R$. The 34 Js gain 136 in mass, each L gains 5 or 9, and R gains 5. The reset increment is therefore $88+2t$, where $t$ is the number of high-charge bulks. It is even and lies between 88 and 102. Each successive reset remains odd until it crosses $K+2$. Every even seed in $[B,C]$ has word $I J^{33} L L J L L J J L R$. Its five Ls force an odd increment, at most 101. Its first return is an odd seed still below $K$.

The endpoint comparisons establish each complete word because the left and right counters vary in opposite directions with the initial seed. Checking the larger endpoint also puts every intermediate first counter above one. The first odd word fails at $B-2$ and the even word fails at $C+2$.

The seven Ls of the odd word require at most eight low bits to determine their residues. The exact increment consequently depends only on $s$ modulo 256. There are two cycles of eight odd residues each. Following a full cycle increases $s$ by $3\cdot256$ in each case. Every start of the large bypass block enters a cycle well before the cut. Listing each cyclic residue's integer lift on the two sides of $K+2$ gives the possible consecutive crossings:

| Last reset offset from $K$ | Next reset offset from $K$ |
|---:|---:|
| −81 | +19 |
| −65 | +29 |
| −47 | +47 |
| −35 | +65 |
| −19 | +79 |
| +1 | +95 |

For the million-seed census, the original unbatched transition halts at the two candidates. Every other seed in the window has a strictly larger first return and no such return equals either candidate. Induction gives exit alive. The largest observed jump was 388. In particular, reaching $K$ or $K+2$ from a still earlier last reset would require a reset increment of more than one million, hence more than 222,222 counter updates. A trajectory arriving through an odd reset in the longer $[B,K+1]$ corridor cannot take that route.

Run [check_fourth_gateway.py](check_fourth_gateway.py) beside the existing checkers. The optional second command also verifies every seed in the local census.

```sh
python3 check_fourth_gateway.py
python3 check_fourth_gateway.py --local
```

## A common later checkpoint

Every one of the six crossing phases reaches reset **18,378,934,934,402,308**. The next first return is 18,378,934,934,402,601. Thus an upstream proof of entry to the bypass interval also selects an exact later checkpoint without having to distinguish the six possible phases.

The odd $J^{34}L^7R$ word continues through $U=17,713,937,045,736,097$. Its first-return gain depends only on the seed modulo 256. Each phase passes $U$ after precisely 2,954,086,474,672 or 2,954,086,474,673 returns. After one or three literal returns, all phases are even. All those even words are $I J^{33} L L J L R$ through $V=18,378,934,934,326,344$, with increments depending only on the seed modulo 16. The $+65$ and $+95$ phases are already identical when they enter this second word. For each residue cycle, its total positive increment is an exact multiple of the modulus. Jumping whole cycles up to the end of each interval recovers each first exit exactly.

| Initial offset | First reset above $U$ | First reset above $V$ | First returns to common checkpoint |
|---:|---:|---:|---:|
| +19 | 17,713,937,045,736,185 | 18,378,934,934,326,356 | 10,747,030,481,909 |
| +29 | 17,713,937,045,736,103 | 18,378,934,934,326,378 | 10,747,030,481,914 |
| +47 | 17,713,937,045,736,121 | 18,378,934,934,326,400 | 10,747,030,481,912 |
| +65 | 17,713,937,045,736,139 | 18,378,934,934,326,416 | 10,747,030,481,905 |
| +79 | 17,713,937,045,736,153 | 18,378,934,934,326,352 | 10,747,030,481,902 |
| +95 | 17,713,937,045,736,169 | 18,378,934,934,326,416 | 10,747,030,481,905 |

From the five distinct exits above $V$, a direct replay of at most 328 first returns per seed reaches the common checkpoint. Run `python3 after_fourth_758.py` to replay both periodic jumps and the final merger. The [infinite terminal-family proof](FOURTH_FAMILY_758.md) identifies the fourth pair as the first member of a progression.

## Raw clock after the +65 crossing

Precisely 10,747,030,481,905 first returns separate $K+65$ from the common reset at 18,378,934,934,402,308. The elapsed raw time between them is **12,009,315,348,729,165,034,617,066,232,977,846,431,994,862,719 transitions**. Within each of the two long fixed-word intervals, a residue cycle translates every starting seed by the same stride. For each phase, every intermediate counter is affine in the cycle index and all branch residues are fixed. Each branch clock is a quadratic polynomial in those counters, so the clock of one cycle is quadratic in its index. Its first three values determine the exact sum by finite differences. The verifier checks a fourth value and times the intervening individual returns directly. [Exact clock and replay](fourth_clock_758.py)

The same method clocks the earlier part from the guaranteed reset 17,354,320,242,846,420 to $K+65$ at 868,964,390,669,458,400,613,660,337,140,973,728,114,577,608 raw transitions. Adding both exact elapsed times to the [mass-based lower bound](MASS_CLOCK_758.md) at that earlier reset gives a blank clock of at least **14,834,450,150,617,068,606,370,263,277,192,707,547,238,915,715** for #758 at the common checkpoint. The clock for #153 is exactly 50,707 transitions earlier.
