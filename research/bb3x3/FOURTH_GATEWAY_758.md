# A wide interval misses the fourth candidate halt

Let $K=17,430,344,744,167,562$. **Every reset with parameter from 17,354,320,242,904,343 through 17,363,959,236,929,600 reaches a reset above $K+2$ alive.** This is a block of **9,638,994,025,258** consecutive input seeds. Across the local window from $K-1,000,000$ through $K+2$, only $K$ and $K+2$ themselves halt before passing the pair. An orbit starting below this block that ever reaches either candidate must skip **all 9,638,994,025,258 reset seeds in one excursion**. Its last reset below the block is at most $B-1$ and its first reset beyond the block is at least $C+1$. Their mass difference is at least $2(C-B+2)$. Each continuing call increases mass by at most nine, so this excursion must last **at least 2,141,998,672,280 counter updates**. The independent question is whether the exact [power checkpoint](POWER_GATES_758.md) $3^{34}+9,103$ reaches the large bypass block.

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
