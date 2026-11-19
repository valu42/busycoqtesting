# One contiguous halting interval below the 140-digit target

Every one of **53,463,914,736,827,918,796 consecutive reset seeds** in the interval
$$
 H-53,463,914,736,831,321,850 \;\le s\le\; H-3,403,055
$$
eventually halts, for $H=(3^{307}-8,282,708,212)/13,959,275$. This joins every gap through scale 20. The scale-19 interval contained 17,821,304,912,273,704,228 seeds. A proof that the actual blank orbit enters the new interval would settle both #758 and #153. [Original contiguous interval](LOWER_SCALE_GATES_758.md)

A [further contiguous extension](HALTING_COLLAR_758.md) reaches 64,916,341,784,242,015,837 halting reset seeds.

## From a reset to a rational direction

Write $d=H-s$. The original interval reaches $d=33,533,929,283,358$. From there through the even distance $32,078,348,842,098,793,106$ just before the scale-20 corridor, every even seed follows its fixed 300-call first-return word. Each odd seed takes $J^{292}L^8JL^6$ and then a maximal run of $k$ jumps. The first word is legal at both endpoints. Throughout a common word the smaller $d$ gives a smaller or equal left counter and larger or equal right counter. These orders preserve the guards and make $k$ nonincreasing as $d$ grows.

Put $D=13,959,275$ and $r=307-k$. The endpoints give $50\le r\le 62$. The [physical itinerary theorem](TARGET_SHADOW_758.md) says that each next ordinary decision agrees with iteration of the rational number $x=D h_0/3^r$, where the aligned left counter plus one is $2\cdot3^k h_0$. For $r\le53$ this holds through elementary depth 257, for $54\le r\le61$ it holds through at least depth 250, and at $r=62$ it holds through depth 249. Reversing all dyadic guard candidates extends the last depth to 251. [Reverse guard calculation](DYADIC_GUARD_SHADOW_758.md) The three intervals $0<x<1/3$, $1/3<x<5/9$ and $5/9<x<1$ give, respectively, a jump with $x\mapsto3x$, an ordinary first return after a bulk and a reset, or two bulks with $x\mapsto(9x-5)/4$. The shadow theorem excludes ties, exceptional calls and hidden early resets during this comparison.

Stop at the first grouped depth $m\ge r$, counting a pair as two calls. Any earlier middle interval supplies the return. Otherwise $m=r$ or $r+1$. The first surviving branch must be a pair because the launch jumps were maximal. If the prefix has $p$ pairs, its inverse has endpoints $A/3^m$ and $(A+4^p)/3^m$. Its ending direction is $N/4^p$ with $N=3^{m-r}D h_0-A$. The integer $N$ is odd and divisible by five. The first pair makes $A$ odd and divisible by five, and later jumps and pairs preserve those properties.

## Two complementary exhaustions

1. At small pair counts we exhaust the dyadic directions. For $p\le23$ every eligible direction returns within 187 additional elementary calls. Through $p=28$, exactly 972 directions take at least 189. The others have decided by $m+188$, no later than depth 251. On each of the 972 long paths we compute the distance to every guard, including the final return. The exact minimum, pulled back to alignment and rounded down, is 239,286,929,249,958,920,641,899,888,561,181,373,889,102,205,359,558,372,943,219,700 at the worst possible cut $m=63$. This exceeds the largest physical perturbation of the initial state. Every such path consequently makes the ordinary return regardless of its header ancestry. [Dyadic exhaustion](DYADIC_SURVIVAL_758.md) · [Long directions](dyadic_long_tails_758.tsv) · [Guard proof](DYADIC_GUARD_SHADOW_758.md)
2. At large pair counts we enumerate every initial word reaching the cut. The prefix gives $h_0(d+32768)=h_0(d)+2D$ and only 8,192 possible residues of $h_0$ modulo $2D$. These determine arithmetic progressions for $N$ within each prefix. Integer interval tests discard directions already known to return early. Arbitrary-precision arithmetic resolves ambiguous comparisons. Every required case returns by its specified angular depth. The two searches meet at a pair count chosen separately for each $r$. At fixed $(r,p)$ there are exactly $\binom{r-p-1}{p-1}+\binom{r-p-1}{p-2}$ high-pair prefixes, corresponding to $m=r$ and $m=r+1$. [High-pair proof and verifier](HIGH_PAIR_HEADERS_758.md) · [Receipts](high_pair_headers_758.tsv)

Earlier proofs recovered and replayed four exceptional reset origins at exponents 59 and 60. The direct guard calculation also covers them. The longest listed direction takes 243 calls after the cut. Therefore a shadowed trajectory takes at most $307+257+63+243+2$ calls from its reset. Every continuing call adds at most nine to $W=a+2c$, and the mass gain between resets is twice the seed increment. Every resulting seed increment is positive and below 4,000. This is smaller than the distance to the near edge of the original interval. Strong induction on the countdown joins every seed in the gap to that interval. [Historical ancestry replay](header_tail_ancestry_758.py)

The final corridor, $32,078,348,842,098,793,108\le d\le 53,463,914,736,831,321,850$, has fixed odd word $J^{292}L^8JL^6 J^{244}LR$ and the same fixed even word. At each parity both endpoints verify the word, so all its seeds make a short positive return. The odd distance immediately before that corridor has an even reset seed and follows the even word. The induction includes every endpoint.

## What would finish the proof from blank?

Set $B=H-53,463,914,736,831,321,850$ and $U=H-3,403,055$. An infinite blank orbit must cross $W=2U+1$. Its last reset at or below that cut would have parameter at most $B-1$, since all seeds from $B$ to $U$ halt. At the first state above the cut the mass gain from the last reset is at least $2(U-B)+3$. Consequently a reset in the preceding **11,880,869,941,517,315,288 elementary calls** would force a halt. A bypass also requires at least 2,437,300,755 distinct length-335 fine words during this passage. Proving either a recent reset or a smaller bound on the number of words on the actual crossing would settle the blank orbit. [Word-count proof](FACTOR_COMPLEXITY_758.md)

A reset is sufficient, and the new test also accepts ordinary states directly. If the orbit enters the trimmed mass interval with even $h=(a+1)/2$ between 2 and 37,491,032,523,348,135,000, its next reset lies in the basin within 553 counter calls. [Ordinary-state criterion and exact bounds](NONRESET_ENTRY_758.md)

## Reproduction

The quick command checks the physical endpoints, the completeness of the archived high-pair rows, and the direct physical clearance of all 972 long paths using the exhaustive results. The last command also regenerates the exhaustive arithmetic surveys. The proofs use integer arithmetic and have not been formalized in a proof assistant.

```sh
python3 target_basin_758.py
c++ -O3 -std=c++17 -fopenmp dyadic_survival_758.cpp -lgmpxx -lgmp -o /tmp/dyadic758
c++ -O3 -std=c++17 -fopenmp dyadic_tail_join_758.cpp -lgmpxx -lgmp -o /tmp/join758
c++ -O3 -std=c++17 high_pair_headers_758.cpp -lgmpxx -lgmp -o /tmp/headers758
OMP_NUM_THREADS=4 python3 target_basin_758.py --dyadic /tmp/dyadic758 --join /tmp/join758 --headers /tmp/headers758
```
