# Direct halts in the entire gap after the last power of three

Let $P=3^{292}$ and $P\le s\le H$. Use $Q$ for a pair of ordinary bulk calls. After the power launch, allow **any number of leading bulk pairs** followed by up to 16 more ordinary jump/pair blocks. The only seeds in the entire interval that then hit a direct terminal are **$H-2$ and $H$**. Both use four leading pairs and the three-block suffix $JQQ$. The last single bulk produces the halting state. The leading run can have up to 387 pairs on odd starts. This rules out an earlier halt of this form even in the part of the gap whose actual reset chain has not been joined. A second exhaustive test allows arbitrarily long leading pairs, a single run of jumps of any length, and arbitrarily long trailing pairs. Again only $H-2$ and $H$ halt. Thus any new direct ordinary halting origin in this interval must have **at least two jump runs separated by one or more pairs after the launch**, and at least 17 blocks after its initial pairs. [Conditional gate and connected trajectory](POWER_CUSP_758.md) · [Direct-terminal guards](MIXED_TERMINALS_758.md)

## Recovering every candidate seed

At an odd-left, odd-right state use $u=(a+2c-1)/2$, $d=(c-1)/2$, $h=u-2d$. After the reset launch $h$ is $3^{292}$ or $2\cdot3^{291}$ and $u=s+584$ or $s+586$ on odd or even starts, respectively. Put $x=u-h$, so $d=x/2$ and $x$ is even. The least seed in each parity gives the largest number of leading legal pairs, by the increasing order in $c$ and decreasing order in $a$ along an ordinary word. Testing those two endpoints gives maximum pair counts of 387 and one, respectively.

The preterminal state before its last single bulk satisfies $-17\le 9d-2u\le-10$. The exact condition at that state is $a=10q+9$, or $q$ odd and $a=10q+11$, where $q=\lfloor(d+1)/2\rfloor$. Every terminal from an odd-right ordinary path occurs after an unpaired bulk, since an odd-left, odd-right state has an even gap $a-c$. To invert a word, represent a necessary condition as $L\le Nd-Au\le U$. Prepending a jump gives $(A+N,3N,L+2A-N,U+2A-N)$. Prepending a bulk pair gives

$$(4A,9N,4L+36A-35N,4U+20A-20N).$$

The pair formula uses all four residue cases of the [ordinary paired map](EVEN_POWER_758.md). On each step $4Av-Nb$ is between $36A-35N$ and $20A-20N$ for the appropriate pair $(v,b)$, since $0\le A/N<1/2$. Thus the integer strip contains every realization, including mixed fine residues.

Prepend all $b$ possible leading pairs to the strip of each requested suffix and solve directly for the reset origin. Every compatible $x$ satisfies

$$2Ah+2L\le (N-2A)x\le 2Ah+2U.$$

The denominator is positive since prepending a jump preserves $N-2A$ and a pair sends it to $9N-8A>0$. Intersect the integer solution with the two endpoints of the reset interval and the parity of $x$. For each survivor, make up to eight of its first pairs exactly and check the strip for the remaining prefix. The pair update for $d$ is $(9d+b)/4$, so a translation of $d$ by $4^8$ translates its eight-pair image by $9^8$ with unchanged mass gain. A 65,536-entry table gives these exact images. Replay every remaining candidate with all guards. A paired run has decreasing left coordinate, so its final condition $2d+1<u$ simultaneously proves all its guards and excludes a return at left coordinate one. Subsequent jumps are tested individually. The exceptional branch throughout this mass range leads back to a reset by the [787-call return](CUT_758.md).

The depth-16 census used 25,559,040 combinations of launch parity, leading-pair count, and ordinary suffix, counted before pruning by the seed interval. It generated 75,317,669 candidate occurrences, with 115,870 left after the eight-pair filter. Overlapping candidate lists for different words count separately. The final guard check accepted the two known seeds.

Build the [verifier](power_cusp_terminals_758.cpp) with `c++ -O3 -std=c++17 power_cusp_terminals_758.cpp -lgmpxx -lgmp -o cusp_terminals` and run `./cusp_terminals 16`. Each output row gives the seed, leading-pair count, suffix length, and suffix bits in execution order from the least significant bit, with one denoting a pair. The last two fields give intervening jump and trailing-pair run lengths in the separate run search.

## A single interrupted bulk run

A second census allows the entire preterminal word after launch to be $Q^bJ^jQ^f$, with arbitrary nonnegative run lengths. If $j=0$, all pairs can be assigned to the leading run. To exhaust the case $j>0$, note that $h$ triples on each jump and can never exceed $u$. Just after the initial pairs, $u\le H+586+9\cdot387$. Even allowing the gain $2\cdot293$, this is below $3^{293}$, so $j\le292$. At the start of the trailing pairs we may use $d\ge0$ and $u\le H+586+9\cdot387+2\cdot293$. The $d$ update on a pair is nondecreasing, and $u$ gains at most nine per pair. Iterating the least possible $d$ from zero violates $2d+1<u$ by the 393rd pair even with the largest allowed $u$. Hence $f\le392$.

For each candidate $j,f$, start at the terminal strip, prepend $f$ pairs and then $j$ jumps, and use the same exhaustive leading-pair inversion. Actual consecutive jumps are replayed by $u'=u+2j$, $h'=3^jh$ and $d'=(u'-h')/2$. The final $d'\ge0$ establishes all earlier jump guards because after a failure $3h-u$ increases with subsequent hypothetical jumps. The decreasing left coordinate similarly checks the final run of pairs at once. There were 44,755,230 combinations, 131,815,639 candidate occurrences, and 173,896 left after the first filter. The two accepted seeds are $H-2$ and $H$, both with $(b,j,f)=(4,1,2)$. Run `./cusp_terminals --runs` to verify this class.
