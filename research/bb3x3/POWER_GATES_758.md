# A single reset checkpoint at each power of three and its double

For every exponent **20 ≤ m ≤ 292**, deep reset entry just below either $3^m$ or $2\cdot3^m$ forces one exact later reset. For the **546** intervals, the [table](power_gates_758.tsv) gives the checkpoint as $A(1,b3^m+t)$, where $b$ is the multiple (1 or 2) and $t$ is the offset. The blank orbit visits the first 30 checkpoints, through $2\cdot3^{34}$. [Fifth crossing and latest power link](FIFTH_BLANK_CROSSING_758.md) [Proof of the three latest links](POWER_CROSSINGS_758.md) In particular all possible entries at $2\cdot3^{32}$ synchronize at $A(1,2\cdot3^{32}+41,023)$.

Put $P=3^m$ and $D=34(4m+40)$. The two deep entry intervals are inclusive.

| Multiple $b$ | Lower reset parameter | Upper reset parameter |
|---|---:|---:|
| 1 | $\lceil9999P/10000\rceil$ | $P-2m-4-D$ |
| 2 | $\lceil19P/10\rceil$ | $2P-2m-6-D$ |

At the frontier nearest the known large halting seed $H$, any deep entry at $P=3^{292}$ reaches **$A(1,3^{292}+1,934,340)$**. The 224 candidate exits of that interval merge along 5,561 distinct first-return edges. This checkpoint lies about 2.7154% below $H$. The first link beyond the initial 26 checkpoints runs from $2\cdot3^{32}+41,023$ to the deep interval at $3^{33}$. For this specific gate the odd word remains valid down to 3,335,436,339,933,247 and the even word down to 5,494,990,037,991,760. The preceding seed of each parity fails its word. A 5,001-seed incoming window beginning at **5,494,990,037,991,759** therefore suffices, using the endpoint argument below. The corresponding sharp lower bounds for an all-parity window are **10,006,309,019,799,870** at $2\cdot 3^{33}$ and **16,484,970,113,975,417** at $3^{34}$. A proof connecting the later checkpoints to blank and to a halting interval remains open.

## Computing the possible exits

Use J for the odd/odd update, L for either ordinary bulk update, R for the even-left return, and I for the opening update from an even reset. At a reset $s$ the following words hold in the indicated corridors.

| Multiple | Odd seed | Even seed |
|---|---|---|
| 1 | $J^{m-1} L R$ | $I J^{m-1} L L J L L L R$ |
| 2 | $J^m L R$ | $I J^{m-1} L R$ |

At multiple 1 the odd word holds through $O=P-2m-4$ and the even word through $O+2m+7$. At multiple 2 the even word holds through $E=2P-2m-6$ and the odd word through $E+2m+11$. For both rows the verifier checks the lower and upper endpoints for each parity. The batched J prefix has a constant left counter and an increasing right counter as a function of the seed. The checks use the [ordered endpoint argument](CONFLUENCE.md) for the remaining word. Each intermediate left counter is either even or greater than one. Thus R is the first return.

At multiple 2 an odd seed gains $2m+5+2[s=3\bmod4]$. An even seed gains $2m+7+2[s+2m=2\bmod4]$. Every even return goes to an odd seed equal to 3 modulo four. Every odd return goes to an even seed equal to $2m+2$ modulo four. Once in these classes the increments alternate between $2m+7$ and $2m+9$. The even seeds repeat every $4m+16$. The first even reset above $E$ therefore belongs to the following set of $m+4$ seeds:
$$
s_i=E+2+4i,\quad 0\le i\le m+3.
$$
Each is attained from its class by backing up enough full periods within the deep corridor. From $s_i$, I followed by $m$ Js gives $A(4P-1,4i+1)$. For the actual blank reset $2\cdot3^{32}-20$, $i=12$ and the right counter is 49.

At multiple 1 all first-return gains are odd, so consider pairs of returns from odd seeds. Their gains depend only on the seed modulo 64. Indeed adding 64 preserves the input residues of all Ls: each L consumes one bit of precision and the longest word has five Ls. The mass increase, and therefore the reset gain, is unchanged. The odd gain is at most $2m+5$ and the even gain at most $2m+29$. On the 32 odd residues, every pair orbit enters a cycle within 32 pairs. The margin $D$ permits a first even-to-odd return followed by all 32 pairs before the boundary. For each cyclic residue $r$ and its pair increment $g(r)$, enumerate all integer lifts $s=r\bmod64$ with $s\le O<s+g(r)$. These give every possible first odd exit. From an exit $x\ge P-2m$, $m$ Js give $A(2P-1,x-P+2m+1)$. The exceptional exit $x=P-2m-2$, if present, instead takes $m-1$ Js and the exceptional move, giving the same state $A(2P-1,1)$ as its sibling.

## Reducing every doubled-to-next-power link to its even excursions

The odd word $J^m L R$ holds from the deep $2P$ interval through $3P-2m-6$, the last odd seed of the next power gate. The checker verifies the same ordinary word at both ends. The intervening odd seeds have the exact return
$$
s\longmapsto s+2m+5+2[s=3\bmod4].
$$
Thus every odd reset in the entire intervening gap immediately leads to an even reset. For an even seed $s\ge 2P-2m-4$, the prefix $I J^m$ gives $A(4P-1,s-2P+2m+5)$. The full doubled-to-next-power link therefore requires control of excursions from **one fixed first counter** at each exponent. After any such excursion returns at an odd parameter inside the gap, the displayed formula supplies the next even parameter. At exponent 32 the two odd increments are 69 and 71.

In fact all these excursions use a single integer index. If the initial reset is odd, take the short return and call the resulting even seed $e$; otherwise use the initial seed as $e$. Put $i=\lfloor(e-2P+2m+6)/4\rfloor$. The even prefix followed by one L takes the actual orbit to
$$
X_m(i)=A(4P-4i-4,6i+5).
$$
Both even siblings with $e-2P+2m+5=4i-1$ or $4i+1$ hit that identical state. A short odd return gives the sibling with right counter $4i+1$. Thus one can evolve $X_m(i)$ to a reset and reapply the displayed index formula until the next gate is reached. At $X_m(i)$ the mass is $4P+8i+6$, so the index strictly increases between section visits. This uses actual common machine states, without assuming the sibling reset itself appeared. The blank exit at the $2\cdot3^{32}$ gate reaches $X_{32}(12)$.

## Exact synchronization

For each interval, repeatedly advance its smallest pending exit by a first return, merging identical resets. Every checked return is legal and strictly increasing. A single remaining reset is a common forward state of all original exits. The 273 intervals of multiple 1 have 18,754 exits in total, which merge along 1,342,960 distinct first-return edges counted within their respective intervals. At multiple 2 the totals are 43,680 exits and 1,784,769 edges. The largest single calculation uses 28,750 edges at multiple 2, exponent 289.

For all 26 intervals through $m=32$, the blank crossing proof supplies a reset inside the deep region. The intervals below the published checkpoint fall in the independently checked blank prefix. The $2\cdot3^{31}$ and $3^{32}$ intervals fall within the first and second candidate window runs, respectively. In these runs a symbolic witness takes at most 10,000 elementary updates after its initial J batch of fewer than 40. The direct checker uses at most 5,000 after that batch (the two optional shorter prefix caches also fit this bound with room to spare for the following estimate). Since each update adds at most nine to $a+2c$, each selected later reset is less than 50,000 above its source. The verifier checks that every deep interval is wider than 50,000. At $2\cdot3^{32}$ the [known exact jump](JUMP_AFTER_THIRD.md) crosses the interval by increments 71 and 73. Its outgoing even reset is one of the 36 exits, whose common checkpoint is reached in at most 857 distinct edges across the whole set.

Place [power_gates_758.py](power_gates_758.py) and [power_gates_758.tsv](power_gates_758.tsv) beside the existing counter verifier. Python 3.10 or later is sufficient.

```sh
python3 power_gates_758.py
python3 power_gates_758.py --m 291
python3 power_gates_758.py --all
```

The default checks all 546 analytic exit sets and replays the mergers at exponents 32 and 292. The full run replays every merger.
