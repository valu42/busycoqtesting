# Mass crossings that force a blank checkpoint

An integer search removes the long-ordinary-stretch alternative at the power bands below. Every blank-compatible counter trajectory that starts at or below the indicated lower mass and reaches the upper mass must visit the named reset. The result permits arbitrary initial counters with nonnegative left counter, positive right counter and an even right counter only at a reset. The blank runs of #758 and #153 visit each checkpoint. All trajectories captured at a given checkpoint therefore have the same subsequent counter history as blank. [Power-band alternatives](THREE_BULK_SCALE_TRANSPORT_758.md) · [Integer search](ordinary_band_sieve_758.cpp) · [Receipts](ordinary_band_sieve_758.tsv)

| Exponent | Start at or below mass | Reach mass | Forced reset parameter | Maximum future ordinary blocks at the cut |
|---:|---:|---:|---:|---:|
| 20 | 19,700,331,541 | 19,700,333,105 | 9,909,846,841 | 64 |
| 21 | 52,301,765,691 | 52,301,767,363 | 29,729,439,052 | 70 |
| 22 | 115,482,299,037 | 115,482,301,015 | 62,762,141,954 | 87 |
| 23 | 531,908,960,049 | 531,908,961,901 | 267,564,844,680 | 80 |
| 24 | 1,412,147,682,081 | 1,412,147,683,987 | 802,694,526,582 | 83 |
| 25 | 3,118,022,082,427 | 3,118,022,084,369 | 1,694,577,296,861 | 85 |
| 26 | 12,709,329,141,321 | 12,709,329,143,659 | 7,224,250,271,748 | 107 |
| 27 | 38,127,987,424,611 | 38,127,987,426,805 | 21,672,750,876,849 | 99 |

A terminal trajectory with an ancestor below one of these lower masses that survives to the upper mass and then halts would prove that both blanks halt. The ancestor can have either counter configuration permitted above. An infinite trajectory with such an ancestor would likewise prove that both blanks run forever. The tested gates precede the current blank frontier. The corresponding cut at exponent 36 and the much larger mass cut in the known halting basin remain open.

## Bounding all ordinary crossings

An ordinary block is the odd/odd jump J or two consecutive ordinary bulk updates P. Put $u=(a+2c-1)/2$ and $d=(c-1)/2$ at an odd/odd boundary. A long ordinary traversal first crosses $u=T$ at $u=T+i$ for $0\le i\le8$. The last incoming block must have half-mass gain greater than $i$. The physical range is $0\le 2d<u$. In these coordinates J maps to $(u+2,3d-u+1)$. P maps to $(u+v,(9d+b)/4)$, with $(v,b)=(5,20),(9,35),(7,26),(7,29)$ in order of input residue modulo four. [Counter rules](EXCURSION_POWERS_758.md)

Use the frozen inverse branches $f_J(x)=(1+x)/3$ and $f_P(x)=4x/9$. Given any finite ordinary word, start from its exact final $x=d/u$ and apply the frozen inverses to produce intermediate directions. The error $d-ux$ starts at zero at the endpoint. Reverse J replaces an error $e$ by $(e-1+2x)/3$ and reverse P replaces it by $(4e-b+4vx)/9$, with $x$ the output direction. Both preserve $[-7,0]$, since $0\le x\le1/2$ and $b\ge2v$. Thus every physical starting $d$ is inside the frozen cylinder at mass $T$, enlarged by seven below and four above. The upper enlargement permits all nine possible masses $T+i$.

Recursively split a prefix interval into its lower $4/9$ and upper $1/3$, stopping when its unpadded width is at most 24 units. The fixed-point grid has 32 units per integer. Every endpoint is a convex combination at a split. Positive rounding occurs only when a P sets the new upper endpoint, negative rounding only when a J sets the lower one. After $p$ P letters and $j$ J letters the positive error in grid units is at most $\min(p,9(j+1)/5)$. Indeed a whole run of P leaves the lower endpoint fixed and increases the maximum by at most $1/(1-4/9)=9/5$. Each individual P increases it by at most one. Likewise the magnitude of the negative error is at most $\min(j,3(p+1)/2)$. Both are at most $9(p+j+1)/14$. Integer floors, ceilings and the explicit grid-error allowance cover those errors at every leaf. The checker verifies that padded lower endpoints remain ordered and visits overlapping integer intervals once. Points outside the resulting union cannot have an ordinary future as long as the deepest leaf.

For a covered point, a necessary test for 32 preceding elementary ordinary calls reverses J and P, rejecting noninteger predecessor coordinates and enforcing the crossing offset on the final block. It stops with zero or one calls left, which preserves every actual history of length 32. A faster preliminary table uses the same test for ten calls on $d\bmod 3^{10}$. Each inverse divides by three or nine with numerator multiplier one or four, so the first ten divisibility tests depend only on this residue. The chosen representative is at least $64\cdot3^{10}$. A reversed P at $d\ge35$ leaves at least $d/3$, and reverse J at $u\ge3$ does the same, so this representative cannot falsely fail by becoming negative. Original coordinates are used for the subsequent 32-call test.

On the remaining candidates, the checker uses the original J guard $3d+1\ge u$. Otherwise it tries P and rejects a resulting $2d'\ge u'$, which cannot represent a positive odd left counter. Allowing a reset with $a=1$ to continue only enlarges the resulting upper bound. The maximum of these future lengths and the deepest leaf is the bound in the table. The [independent checker](ordinary_band_sieve_758.py) compares a full brute-force traversal with the interval search at smaller cuts and replays retained maximizers against the original counter rules. At $T=10,000$ a separate forward enumeration through the actual grouped rules finds all 34 genuine arrivals with 32 elementary calls of history and a maximum future of 15 blocks, equal to the sieve bound.

For a bound $L$ set $W_-=2T+1-9(32+4)$ and $W_+=2T+1+16+18(L+4)$. All continuing calls gain at most nine in $W=a+2c$, each grouped block costs at most two calls, and the first aligned crossing overshoots by at most eight half-mass units. If a traversal from $W_-$ to $W_+$ were ordinary throughout, dropping incomplete end blocks would leave 32 prior elementary calls and at least $L+1$ future blocks at the crossing, contrary to the integer search. A traversal attaining $W_+$ survives to that mass. Therefore it either meets a reset or takes an exceptional restart in the local band. Every such restart enters a reset in the same full band by its previously certified one-dimensional bulk sequence; the checker verifies both endpoints and the remaining clearance. That reset follows either the doubled-power gate or the three-bulk gate to the checkpoint, including the checked merger of all possible exits.

## Counting the full angular search before enumeration

For raw search size, subtrees with the same rounded width, depth and lower endpoint modulo 32 are translations of each other by an integer number of $d$ units. A memoized count stores each subtree's number of leaves, sum of distinct covered integers and first and last leaf intervals. At a join, the endpoint orders are checked. The overlap of the two unions is exactly the intersection of the last left leaf with the first right leaf. Its size is subtracted once. This gives an exact workload count before the incoming arithmetic tests. For fixed depth and number of P letters, the true unrounded width is fixed and the error in a rounded width is at most $1/(1-4/9)$ grid units. Consequently the number of stored translation classes is $O((1+\log T)^2)$, even at the 140-digit target.

For the next blank scale, at $T=276,174,128,946,478,382$, **522,080,590,671** leaves cover **12,521,732,835,040** integer coordinates before ancestry testing. The count uses 26,720 translation classes. At the known halting cut $T=H-10,000,000$ the corresponding union contains about $2.34327\times10^{102}$ coordinates and the largest depth is 391. This counts candidate coordinates; it leaves the ordinary exclusion at both cuts open. An empty integer crossing at the latter cut, with the exceptional-return margins in the [halting band](CUT_758.md), would prove that #758 and #153 halt from blank.

From this directory run the default check for exponent 20, or replay the rows individually or together.

```sh
c++ -std=c++17 -O3 ordinary_band_sieve_758.cpp -o /tmp/ordinary_band_sieve
python3 ordinary_band_sieve_758.py /tmp/ordinary_band_sieve
python3 ordinary_band_sieve_758.py /tmp/ordinary_band_sieve --all
python3 ordinary_band_sieve_758.py --count 276174128946478382
python3 ordinary_band_sieve_758.py --count target
```
