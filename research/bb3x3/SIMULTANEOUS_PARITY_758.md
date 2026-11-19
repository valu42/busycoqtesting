# Long ordinary excursions in both launch parities of machine 758

On two portions of the actual blank orbit, every consecutive reset launches a long ordinary suffix. The depth below counts individual two-counter calls **after** the maximal opening jump run. The opening itself takes exactly another $m$ calls in either parity.

| $m$ | Inclusive seed interval | Minimum suffix depth | Consecutive proved blank origins inside |
|---:|---|---:|---:|
| 34 | 16,949,613,841,245,601 through 16,949,613,841,383,298 | 44 | 615 (277 even, 338 odd) |
| 35 | 50,848,841,523,849,635 through 50,848,841,524,150,094 | 45 | 1,308 (829 even, 479 odd) |
| 292 | 204,076 consecutive integers strictly below $H$, endpoints constructed by the checker | 492 | Blank entry open |

The indicated prefix holds for **every integer seed** in each interval. In particular the first two intervals include genuine long excursions from both parities along one and the same blank trajectory. This rules out a uniform bound on post-opening depth obtained by selecting whichever launch parity has the shorter prefix. It places no lower bound on the work of an algorithm that batches these prefixes.

## A common surviving direction

Put $Q=3^m$ and write $x=Q/(s+2m)$. At the odd opening the physical direction is exactly $x$. At the even opening it is $y=(2/3)Q/(s+2m+2)$. Measure the even direction on the same axis by multiplying it by $3/2$.

Let $K$ be the limit set of $f_J(z)=z/3$ and $f_P(z)=(4z+5)/9$ on $[0,1]$. Here $J$ denotes one ordinary jump and $P$ denotes two ordinary bulks. Use a cylinder for the interval $f_{w_1}\circ\cdots\circ f_{w_l}([0,1])$. Start the odd search at $V=PPPPP$, with interval $[58025/59049,1]$, and the even search at $W=PJPJ$, with rescaled interval $[155/162,481/486]$. They overlap and their widths are within a factor of three.

Split the longer interval and keep a child overlapping the other interval. The other interval has at least a third of the longer one's width, whereas the removed middle gap has width $2/9$ of the longer width. If the other interval protrudes past an endpoint of the longer one, it meets a retained child there. If it is contained, it is too long to fit in the removed gap. In each case the intersection with some child has positive width. Indeed, every endpoint of every cylinder descending from $V$ or $W$ before rescaling is an odd numerator over a power of three. A cylinder beginning with $P$ has endpoints $(A,A+4^p)/3^d$, where $p\ge1$ counts pairs and $d$ counts elementary calls. Appending $J$ changes $A$ to $3A$, and appending $P$ changes $A$ to $9A+5\cdot4^p$. Rescaling the even endpoints by $3/2$ therefore gives reduced even denominators, distinct from every odd-cylinder endpoint. The new widths are again within a factor of three since every child has between $1/3$ and $4/9$ of its parent's width. Each phase is split infinitely often because a repeatedly shrinking interval eventually becomes shorter than its partner.

The two nested paths thus contain a common point of $K$ and $(3/2)K$. Every such finite pair of overlapping positive cylinders can continue indefinitely by this rule. The ideal common point alone decides neither the infinitely rounded trajectory at a fixed finite power nor the fate of blank.

## A finite cycle cannot describe both ideal words

Every positive point of $K$ with an eventually periodic $J,P$ word is a rational with odd numerator and odd denominator in lowest terms. Indeed, a periodic block with $p\ge1$ pairs and elementary depth $d$ acts by $z\mapsto(A+4^p z)/3^d$. Its first pair gives $A$ odd, and subsequent letters preserve oddness, so its fixed point is $A/(3^d-4^p)$, a ratio of odd integers. A repeating all-jump block gives zero. In a finite prefix, $f_J$ preserves an odd numerator and denominator, $f_P$ takes an odd denominator to an odd numerator and denominator, and $f_P(0)=5/9$. This covers every positive eventually periodic word.

Consequently the two infinite words for any positive common direction cannot *both* be eventually periodic. Scaling a positive odd-over-odd rational by $3/2$ leaves an even denominator after reduction. In particular, no nonempty finite directed graph whose accepting infinite paths specify only such pairs of words can generate them through a repeatable accepting cycle productive on each tape. For a synchronous nondeterministic Büchi automaton, any one accepting path revisits an accepting state and yields such a cycle by repetition. The same argument applies to an asynchronous generator if its paths are required to emit infinitely many letters on each tape: choose a recurrent accepting state and extend its return loop far enough to emit on both. This excludes a pair of repeating symbolic templates, while leaving arithmetic generators and finite descriptions with counters open.

## From rational intervals to consecutive integer seeds

For $n\ge10$, truncate each path at its first grouped boundary of depth at least $n$. Both resulting depths are $n$ or $n+1$. Their intersection $[a,b]$ has positive length, and all endpoints are integer multiples of $1/(2\cdot3^{n+1})$. Consequently
$$ b-a\ \ge\ 1/(2\cdot3^{n+1}). $$

Keep all integer seeds with $a+32/Q\le x\le b-32/Q$. Throughout the initial overlap, $s+2m>Q$ and the two directions in common units differ by less than $2/Q$. For $m\ge20$, throughout this band $Q<s+2m<1.02Q$; hence the maximal opening has $m$ jumps for an odd seed and one even-opening instruction and $m-1$ jumps for an even seed. This follows from the opening condition $h\le t\le3h-3$ and its monotone thresholds, with $(h,t)=(Q,s+2m)$ and $(2Q/3,s+2m+2)$ respectively.

The true direction for each seed has clearance at least $20/Q$ from the two endpoints of its own unscaled cylinder. Every earlier inverse guard $0,1/3,5/9,1$ lies outside the interior of the final cylinder. Multiplying by $t\ge Q$ gives at least 20 units of initial guard clearance. For an already realized ordinary prefix the exact identity $h-\lambda t=R(h'-\mu t')+B$ has $R\le1$ and $0\le B\le14$. Pushing the signs forward leaves more than four units of physical clearance, enough to exclude an early reset, exceptional branch or mid-pair terminal and to prove the next ordinary instruction. This proves the entire prescribed prefix by induction. See [the guard identity](TARGET_SHADOW_758.md) and [its use for arbitrary launch states](LOCAL_RETURN_WINDOWS_758.md).

The real seed interval has span at least $Q(b-a)-64$, by $|d(Q/x)/dx|\ge Q$ there. Thus at *every* $m\ge20$, depth $n=m-6$ gives span at least $3^5/2-64=57.5$ and at least 57 consecutive integer seeds of both parities. For $m\ge23$, depth $m-13$ gives span at least $265656.5$. Any increasing reset path crossing this latter interval with spacing at most $100,000$ must start at least two excursions inside it. The sharper individual table rows use the calculated overlap, then invert the padded rational interval and round inward. The algorithm splits the longer interval, chooses the child with greater overlap and breaks a child tie in favor of $J$.

## Exact links to the blank trajectory

The [fourth-terminal coverage](POWER_CROSSINGS_758.md) supplies row 135 on its fourth leg, and the [power-35 coverage](POWER35_INNER_SKIP_758.md) supplies row 162. Shorten the next row in each grid to the lower endpoint of the table interval. The usual worker allows 5,001 incoming integers. At both cuts it returns a singleton, proving the first reached seed there exactly.

| $m$ | Supplemental worker start | Unique first reset at or above the cut | First reset after the interval |
|---:|---:|---:|---:|
| 34 | 16,949,181,699,675,672 | 16,949,613,841,245,761 | 16,949,613,841,383,425 |
| 35 | 50,846,545,099,034,461 | 50,848,841,523,849,749 | 50,848,841,524,150,265 |

The [checker](simultaneous_parity_758.py) replays the prescribed prefix and runs the original unbatched first return at every one of the 1,923 consecutive blank origins. Its default run validates the two stored receipts against the archived preceding cuts and checks all the rational windows. To regenerate the two supplemental receipts as well, run in this directory:

```sh
c++ -O3 -std=c++17 cross_758_fast.cpp -o /tmp/pair758-34
c++ -O3 -std=c++17 cross_double35_758.cpp -o /tmp/pair758-35
python3 simultaneous_parity_758.py --worker34 /tmp/pair758-34 --worker35 /tmp/pair758-35
```
