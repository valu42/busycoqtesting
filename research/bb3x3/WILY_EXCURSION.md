# Which positive integer starts the Wily blank excursion?

For the Wily twins #531 and #532 there is a specific **last positive integer before the known negative blank checkpoint**:
$$
p_* = 16\,472\,443\,404\,719\,956\,078.
$$
Let $F$ be the [integer permutation](WILY_INTEGER_MAP.md), and let $E$ be the forest of negative integers that $F$ sends to positive integers. For each $e\in E$, write $P(e)$ for its nearest positive predecessor under $F$. This integer exists for every $e$. **The forward orbit from the blank checkpoint stays negative forever if and only if $p_*\notin\{P(e):e\in E\}$.** Proving this exclusion would prove that both machines run forever. A positive sign change in the virtual map would still require evaluating the physical edge rule.

The equality reduces the open question to a function on a binary tree with just two roots. There is no unknown time parameter in the target $p_*$. At the verified $2^{256}$-sweep checkpoint, any subsequent exit must have $|e|>2^{765}$. For example, an estimate $|e|\le 2^{250}P(e)^8$ for exits with $P(e)=p_*$ would suffice, since $p_*<2^{64}$. This particular inequality is an open target. It matters that the constant and domain are specified. For instance, the exit $e=-55297870363118536381$ has $P(e)=14$ at distance 7,300,461; the unscaled bound $|e|\le P(e)^8$ fails there. The [first-event verifier](wily_first_contact.py) computes this predecessor without iterating seven million times. An unbounded estimate comparing $|e|$ to $P(e)$, or an induction directly excluding $p_*$ on the tree, would suffice. The finite evidence below does not establish either result.

## Derivation

The blank-connected scalar checkpoint is $n_*=-227089934777573210432$. Exact inverse iteration reaches $p_*$ after 672,030 steps, with all intermediate numerators negative. Moreover $F(p_*)=-60830999776514433041$. This computation concerns the virtual integer orbit. The physical correctness needed for the conclusion starts at $n_*$ and holds for as long as the orbit remains negative. [Physical correspondence and backward bound](WILY_INTEGER_MAP.md)

The set $E$ comprises the descendants of $-8,-16$ under
$$
L(m)=4m+6,\qquad S(m)=2m+\begin{cases}-3 &m\text{ odd},\\9&m\text{ even}.\end{cases}
$$
Starting at $e\in E$, the consecutive negative inverse iterates stay inside its finite initial magnitude bucket, with the small exceptional pair treated separately. They cannot repeat, since their forward trajectory has a positive exit. Thus $P(e)$ is well-defined and computable. Conversely, from each positive integer $p$ there is at most one negative excursion that starts on the very next iterate. If $P(e)=p_*$, the segment starts with the negative run already verified through $n_*$ and ends at $e$. If the run from $n_*$ exits, its last negative integer is such an $e$. This proves the equivalence, including the possibility that the virtual orbit is periodic.

## An all-time filter on the excursion endpoints

The orbit of $n_*/3$ on binary prefixes of length 320 is a single cycle of length $2^{137}$ through its initial prefix. Among *all* $e\in E$ with $|e|\le 2^{160}$, exactly seven have a residue on this cycle. The phases in the table are modulo $2^{137}$, with $n_*$ at phase zero. They certify exclusions over the complete finite cycle, in both time directions.

| Possible $e$ | Phase represented as a negative integer | Reason it cannot end the blank excursion |
|---:|---:|---|
| −325005293 | −1720425 | Nearest positive predecessor 2031034478 |
| −3758096386 | −1721190 | Residue 2 modulo 3 |
| −21701425901 | −1718793 | Nearest positive predecessor 882945859 |
| −257634140162 | −1716582 | Nearest positive predecessor 51648659461 |
| −1948454754451451 | −1782631 | Nearest positive predecessor 5305511360593925 |
| −4323174695770738877 | −1048577 | Nearest positive predecessor 917310934306 |
| −4228484313993422914510738 | −104794398 | Residue 2 modulo 3 |

On the negative segment from $n_*$ the numerator remains $1\bmod3$. The only negative input that changes this residue is $-2$, whose sole predecessor is positive. The five displayed nearest positive predecessors all differ from $p_*$. The last one by backward distance takes 666,233 inverse steps to reach. The [monotone bucket proof](WILY_INTEGER_MAP.md) gives a larger lower bound on the first possible future exit directly from a finite blank trace. The table supplies different information: it identifies the individual sign-changing endpoints compatible with the entire modular orbit and explains why those endpoints belong to other excursions.

## How to check a cycle of length $2^{137}$

Use physical binary digits, so the rational being read is $n/3$. Let $R$ be the cyclic stream of carries emitted by the first $k$ digits during their complete return from the blank prefix. A phase in that return is stored by its sweep number and the number of events emitted before it. For the next input bit $b$, reading all of $R$ either fixes $b$ or flips it. In the first case the return length stays fixed. In the second it doubles and the second return through the old prefix starts with the opposite bit. The next return stream is obtained by passing $R$ through $b$ and, in the doubled case, appending the stream through $1-b$.

The event count up to any phase can be updated from a prefix of $R$. Every mode except 3 transmits one event. Every mode except 2 flips the bit. These two prefix counts determine both the lifted phase's next bit and its new event count. This explores every compatible phase without iterating the cycle. The run-length representation is the one already tested against the four original bit rules.

For pruning, keep $n=c+2^s m$ with $m\in E$. Reading enough low bits forces each inverse lift, since $2\bmod4$ selects $L$, and $1,3\bmod4$ select the two branches of $S$. A multiple of four must be one of the two roots. Exact candidates can then be checked at every higher bit. While a continuation remains open, the largest possible odd $m$ is $-7$ and the largest even $m$ is $-8$. These bounds only discard subtrees in which the magnitude already exceeds the requested limit. Finite-prefix orbit generation and forest pruning are independent.

Run either command with assertions enabled. The short check uses a $2^{100}$ size bound at precision 240 and produces the same seven candidates. Both commands also compare the sieve with literal modular orbits for five starting integers at four precisions.
```sh
python3 wily_orbit_sieve.py
python3 wily_orbit_sieve.py --large
```

## Infinite families excluded by the same cyclic calculation

These congruence tests also rule out whole families of arbitrarily large endpoints. Regard a word $w$ on $L,S$ as a composition with its leftmost letter outermost. Suppose $w$ contains $i$ long lifts and $j$ short ones, and put $h=2i+j$. Each $L$ increases the binary agreement of two distinct inputs by exactly two bits, and each $S$ increases it by one: when parity differs, the extra offset difference is a multiple of four. Thus $w^r(m)$ has its low $rh$ bits fixed independently of the inner forest member $m$. A mismatch with the orbit at any of those bits excludes **every** such endpoint, however large $|m|$ is.

The verifier tests all 8,032 primitive words of one through twelve letters (a primitive word is not a repetition of a shorter word). For 7,843 of them even one outer copy is impossible. For another 185, two are impossible. The four remaining thresholds are three copies for each of $LLS,LSSSL$, seven for $S$, and twenty for $L$. For example, every $L^{20}(m)$ equals $-2\pmod {2^{40}}$, a residue absent from the whole blank cycle. All the tests require at most 40 low binary digits. They constrain the outermost lifts; an interior occurrence alone does not prescribe the low bits of the endpoint.

The [excursion counting theorem](WILY_SIGN_EXCURSIONS.md) proves that small $P(e)$ relative to $|e|$ occurs on a density-zero subset of the exit forest. That theorem permits individual exceptions. Excluding $p_*$ from those exceptions remains the blank-specific problem.
