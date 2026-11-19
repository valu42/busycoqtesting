# A larger contiguous halting interval at the 140-digit target

Every reset $A(1,H-d)$ with **$3,403,055\le d\le61,410,570,681,246,030,619$** halts, where $H=(3^{307}-8,282,708,212)/13,959,275$. This gives **61,410,570,681,242,627,565 consecutive halting reset seeds**, extending the [scale-20 result](TARGET_BASIN_758.md) by 7,946,655,944,414,708,769. This statement applies to machine #758 and to the common counter orbit of #153. It leaves entry from the blank tape open. The interval ends partway through the gap to scale 21.

At the first crossing above mass $2(H-3,403,055)+1$, a reset in the preceding **13,646,793,484,720,583,903 elementary counter calls** would now force a halt. Indeed, if the run passes the interval alive, its last reset had seed at most $H-61,410,570,681,246,030,620$. The resulting mass gap is at least twice the difference between the basin endpoints plus three, and each call increases mass by at most nine.

## Why this part of the gap can be exhausted

On odd reset seeds in the extension the [known header](TARGET_SHADOW_758.md) ends with 244 alignment jumps. The aligned left coordinate $h=(a+1)/2$ increases weakly with even countdown $d$. The two equal endpoint jump counts establish the value 244 throughout, since the maximal jump count is nonincreasing in $d$. Put $x=13,959,275h/3^{307}$; the [physical shadow](DYADIC_GUARD_SHADOW_758.md) relates its ordinary angular motion to the exact counters. Odd countdowns are even-seed starts with the known 300-call return.

Let $J$ denote one jump and $P$ a pair of bulks. Stop at the first group boundary at or past 63 elementary calls after alignment, counting a pair as two. An earlier middle-interval decision gives an ordinary return. Otherwise the cut is at 63 or 64 calls, with normalized direction $N/4^p$ where $p$ counts pairs and $N$ is an odd multiple of five. For $p\le28$ the [complete dyadic survey](DYADIC_SURVIVAL_758.md) gives either an exit decision within another 188 calls, or one of 972 listed tails. At depths 249 through 252 the [reverse guard checker](dyadic_guard_shadow_758.py) excludes every possible physical ambiguity. All 972 longer tails have initial clearance exceeding $7.97\times10^{61}$ in aligned coordinates, which exceeds the physical error bound $d+2000$. For $p=31,32$ the previously [exhausted header rows](HIGH_PAIR_HEADERS_758.md) cover every case, and the original physical shadow reaches their depth-248 guard.

For $p=29,30$ it suffices here to check prefixes beginning $P J^2$. Their [complete enumeration](halting_collar_headers_758.tsv) contains 36,425 prefix cylinders and 2,866,657,295 angular tests at these two pair counts. The same run rechecks one previously covered 31-pair cylinder. Every candidate returns by the depth-248 guard. The full high-pair verifier simply starts at the inverse cylinder for the fixed prefix. Its endpoints are $(5\cdot 3^2)/3^4$ and $(5\cdot3^2+4)/3^4$. At each $p$ the expected number of prefixes is $\binom{63-p-2}{p-1}$, counting both the cut at 63 and a final pair straddling 63.

To locate the first uncovered cylinder, recurse on the $J$ child before the $P$ child. Given an inverse cylinder $[A,A+4^p]/3^m$, the children have coefficients $(3A,m+1,p)$ and $(9A+5\cdot4^p,m+2,p+1)$. Discard the already checked subtree and every branch that cannot finish with 29 or 30 pairs. The order is exact because the normalized inverse intervals $[0,1/3]$ and $[5/9,1]$ are disjoint and both maps preserve order. Consequently every surviving header before the left endpoint of the first uncovered cylinder is covered. The [integer checker](halting_collar_758.py) compares that endpoint to the aligned coordinates of consecutive odd reset seeds bracketing the claimed far edge. The final included countdown is odd, giving the known even-seed return there.

Each positive first return in the extension gains fewer than 4,000 reset seeds. Countdown strictly decreases, and that bound prevents it from skipping the old halting interval. Induction joins the entire collar to the old basin.

```sh
c++ -O3 -std=c++17 high_pair_headers_758.cpp -lgmpxx -lgmp -o /tmp/high_pair_headers
python3 halting_collar_758.py --headers /tmp/high_pair_headers
```
