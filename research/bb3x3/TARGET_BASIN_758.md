# Joining the halting basin below the 140-digit target

Every reset $A(1,H-d)$ with
$$
3,403,055\ le d\le\ 2,716,248,271,952,006
$$
eventually halts. This is **2,716,248,268,548,952 consecutive seeds**, approximately 81 times the size of the previously joined inner interval. It includes all the gaps between the scale-7, 8, 9, 10 and 11 corridors. The bound applies separately to every integer in the interval. Entry by the blank orbit would resolve both #758 and #153.

## How the gaps are closed

The [previous basin](LOWER_SCALE_GATES_758.md) ends at $d=33,533,929,283,358$. From there through $d=1,629,748,963,171,202$, every even reset follows its known 300-call first-return word. Every odd reset takes the common prefix $J^{292}L^8JL^6$ and then the maximal next group of $k$ jumps. The ordering of the left and right counters along the prefix makes $k$ nonincreasing as $d$ increases. Checking both endpoints gives $254\le k\le257$. Put $r=307-k$.

The [physical shadow theorem](TARGET_SHADOW_758.md) makes each subsequent grouped decision through depth 257 exact by iterating a rational number $x=D h_0/3^r$, where $D=13,959,275$ and $h_0$ is the positive even left coordinate before the second group of jumps. The three alternatives are a jump ($x\mapsto3x$), an ordinary first return (the middle interval), or a pair of bulks ($x\mapsto(9x-5)/4$). At entry the next jump is impossible by maximality. Thus a seed continuing beyond the first decision must begin with a pair.

Stop the rational iteration at the first grouped depth $m\ge r$, counting a pair as two calls. An earlier middle interval already supplies the return. Otherwise $m=r$ or $r+1$. After $p$ pairs the direction has the form $N/4^p$ with **$N$ odd and divisible by 5**. Indeed an inverse word has endpoints $A/3^m$ and $(A+4^p)/3^m$, so $N=3^{m-r}D h_0-A$. The first pair makes $A$ odd and divisible by five, and each later jump or pair retains that property.

Two finite exhaustions cover these rational directions.

* For $p\le23$, every positive odd multiple of five below $4^p$ reaches the middle interval within at most 187 more elementary calls. Since $m\le54$, this occurs within the proved shadow. The calculation recursively restricts arithmetic progressions to the two surviving intervals and exactly replays the remaining individual rational points. [Dyadic survey and verifier](DYADIC_SURVIVAL_758.md)
* For $p\ge24$, the fixed prefix gives $h_0(d+32768)=h_0(d)+2D$. Enumerating one period gives 8,192 possible residues modulo $2D$. Enumerate every initial word through this cut with sufficiently many pairs. In each interval enumerate the resulting arithmetic progressions of possible $N$, skipping only bins already proved to return early. The full survey for $r\le53$ found **zero** surviving headers through depth 257. Across the required high-pair cases and the smaller exponents archived alongside them, it checked 617,905 prefix intervals. [Method](HIGH_PAIR_HEADERS_758.md) · [Integer receipts](high_pair_headers_758.tsv)

This proves an ordinary reset within $307+257+257+2$ elementary calls for every odd seed in the gap, the final two calls allowing the return after the middle guard. Every continuing call adds at most nine to $W=a+2c$. At two resets the increase in $W$ is twice the increase in the reset seed. Thus the positive increase of the seed is less than 4,000. A reset in the gap returns to a strictly smaller countdown still above $3,403,055$. Strong induction attaches the **entire** gap to the old basin.

For $1,629,748,963,171,204\le d\le2,716,248,271,952,006$, the fixed odd word $J^{292}L^8JL^6 J^{253}LR$ and the same even word give a bounded positive return. Each word is legal at both endpoints of its parity, and the counter ordering preserves the guards between them. The intervening odd distance just before this corridor gives an even reset, also covered by the even word. The same induction attaches the outer corridor. The earlier sparse transfer receipts are unnecessary for the gaps above the old scale-7 endpoint in this proof.

## Consequence for blank

Write $B=H-2,716,248,271,952,006$ and $U=H-3,403,055$. A hypothetical infinite blank orbit must pass $W=2U+1$. Its last reset at or below that cut has parameter at most $B-1$. At the first state with $W>2U+1$, the required mass gain is at least $2(U-B)+3$. A reset in the preceding **603,610,726,344,211** elementary calls would therefore force a halt. We have not proved that the blank orbit has a reset this recent at that cut.

The finite proof uses ordinary integer calculations with explicit bounds. It is independent of sampling and has not been formalized in a proof assistant. Reproduce it in this directory. The first command checks all physical endpoints. The final command also reruns the two exhaustive rational calculations.

```sh
python3 target_basin_758.py
c++ -O3 -std=c++17 -fopenmp dyadic_survival_758.cpp -lgmpxx -lgmp -o /tmp/dyadic758
c++ -O3 -std=c++17 high_pair_headers_758.cpp -lgmpxx -lgmp -o /tmp/headers758
OMP_NUM_THREADS=4 python3 target_basin_758.py --dyadic /tmp/dyadic758 --headers /tmp/headers758
```
