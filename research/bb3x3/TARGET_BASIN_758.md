# One contiguous halting interval below the 140-digit target

Every one of **17,821,304,912,273,704,228 consecutive reset seeds** in the interval
$$
 H-17,821,304,912,277,107,282 \;\le s\le\; H-3,403,055
$$
eventually halts, for $H=(3^{307}-8,282,708,212)/13,959,275$. This joins every gap through scale 19. The previous continuous interval adjoining the target region contained 33,533,925,880,304 seeds. A proof that the actual blank orbit enters the new interval would settle both #758 and #153. [Original contiguous interval](LOWER_SCALE_GATES_758.md)

## From a reset to a rational direction

Write $d=H-s$. The original interval reaches $d=33,533,929,283,358$. From there through the even distance $10,692,782,947,366,264,370$ just before the scale-19 corridor, every even seed follows its fixed 300-call first-return word. Each odd seed takes $J^{292}L^8JL^6$ and then a maximal run of $k$ jumps. The first word is legal at both endpoints. Throughout a common word the smaller $d$ gives a smaller or equal left counter and larger or equal right counter. These orders preserve the guards and make $k$ nonincreasing as $d$ grows.

Put $D=13,959,275$ and $r=307-k$. The endpoints give $50\le r\le 61$. The [physical itinerary theorem](TARGET_SHADOW_758.md) says that each next ordinary decision agrees with iteration of the rational number $x=D h_0/3^r$, where the aligned left counter plus one is $2\cdot3^k h_0$. For $r\le53$ this holds through elementary depth 257, and for the remaining ranges it holds through depth 250. The three intervals $0<x<1/3$, $1/3<x<5/9$ and $5/9<x<1$ give, respectively, a jump with $x\mapsto3x$, an ordinary first return after a bulk and a reset, or two bulks with $x\mapsto(9x-5)/4$. The shadow theorem excludes ties, exceptional calls and hidden early resets during this comparison.

Stop at the first grouped depth $m\ge r$, counting a pair as two calls. Any earlier middle interval supplies the return. Otherwise $m=r$ or $r+1$. The first surviving branch must be a pair because the launch jumps were maximal. If the prefix has $p$ pairs, its inverse has endpoints $A/3^m$ and $(A+4^p)/3^m$. Its ending direction is $N/4^p$ with $N=3^{m-r}D h_0-A$. The integer $N$ is odd and divisible by five. The first pair makes $A$ odd and divisible by five, and later jumps and pairs preserve those properties.

## Two complementary exhaustions

1. At small pair counts we exhaust every odd multiple of five below $4^p$. For $p\le23$ every such positive direction returns within 187 more elementary calls. At higher pair counts only a short explicit list lasts 189 calls. All other directions decide before the physical guarantee runs out since $m+188\le250$. For the listed directions, splitting the preceding word into two pieces gives every matching physical countdown. Those rare actual origins can be replayed with the original two-counter rules. [Dyadic exhaustion](DYADIC_SURVIVAL_758.md) · [Long directions](dyadic_long_tails_758.tsv) · [Recovery and literal replay](target_basin_758.py)
2. At large pair counts we enumerate every initial word reaching the cut. The prefix gives $h_0(d+32768)=h_0(d)+2D$ and only 8,192 possible residues of $h_0$ modulo $2D$. These determine arithmetic progressions for $N$ within each prefix. Integer interval tests discard directions already known to return early. Arbitrary-precision arithmetic resolves ambiguous comparisons. Every required case returns by its specified angular depth. The two searches meet at a pair count chosen separately for each $r$. At fixed $(r,p)$ there are exactly $\binom{r-p-1}{p-1}+\binom{r-p-1}{p-2}$ high-pair prefixes, corresponding to $m=r$ and $m=r+1$. [High-pair proof and verifier](HIGH_PAIR_HEADERS_758.md) · [Receipts](high_pair_headers_758.tsv)

For example, the two seeds at distances 835,854,016,615,180,604 and 835,854,016,615,180,606 both make a fresh reset on their 814th counter call. Their seed increments are 1,953 and 1,955. The other two matching origins, 3,521,634,644,642,563,784 and 3,521,634,644,642,563,786, return in 812 calls and gain 1,936 and 1,938. These four offsets were the exceptions examined in the scale-18 proof. At the new exponent 61, none of the 972 late directions through 28 pairs has an admissible reset origin. The 36,426 remaining high-pair prefixes all decide by depth 250. [Ancestry checker](header_tail_ancestry_758.py)

The shadowed paths have at most $307+257+257+2$ calls. Each continuing call adds at most nine to $W=a+2c$, and the increase in $W$ between resets is twice the seed increment. The resulting positive seed increments are below 4,000. For the rare physical replays the checker requires a halt or a first return in 2,000 calls with a seed increment at most 9,000. Both bounds are much smaller than the distance to the old interval's near edge. Thus each seed either halts or returns to a strictly smaller countdown still inside the induction range. Strong induction joins the entire gap to the original halting interval.

The final corridor, $10,692,782,947,366,264,372\le d\le 17,821,304,912,277,107,282$, has fixed odd word $J^{292}L^8JL^6 J^{245}LR$ and the same fixed even word. At each parity both endpoints verify the word, so all its seeds make a short positive return. The odd distance immediately before that corridor has an even reset seed and follows the even word. The induction includes every endpoint.

## What would finish the proof from blank?

Set $B=H-17,821,304,912,277,107,282$ and $U=H-3,403,055$. An infinite blank orbit must cross $W=2U+1$. Its last reset at or below that cut would have parameter at most $B-1$, since all seeds from $B$ to $U$ halt. At the first state above the cut the mass gain from the last reset is at least $2(U-B)+3$. Consequently a reset in the preceding **3,960,289,980,505,267,606 elementary calls** would force a halt. A bypass also requires at least 1,407,176,247 distinct length-334 fine words during this passage. Proving either a recent reset or a smaller bound on the number of words on the actual crossing would settle the blank orbit. [Word-count proof](FACTOR_COMPLEXITY_758.md)

## Reproduction

The quick command checks the physical endpoints, the completeness of the archived high-pair rows, and the actual rare reset origins using the exhaustive results. The last command also regenerates the exhaustive arithmetic surveys. The proofs use integer arithmetic and have not been formalized in a proof assistant.

```sh
python3 target_basin_758.py
c++ -O3 -std=c++17 -fopenmp dyadic_survival_758.cpp -lgmpxx -lgmp -o /tmp/dyadic758
c++ -O3 -std=c++17 -fopenmp dyadic_tail_join_758.cpp -lgmpxx -lgmp -o /tmp/join758
c++ -O3 -std=c++17 high_pair_headers_758.cpp -lgmpxx -lgmp -o /tmp/headers758
OMP_NUM_THREADS=4 python3 target_basin_758.py --dyadic /tmp/dyadic758 --join /tmp/join758 --headers /tmp/headers758
```
