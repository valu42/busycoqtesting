# Line 33 · Balanced ternary at the right edge

`1RB2LA0RB4LB1RA_1LA3RA1RA---0LA` · **Unknown** · 2026-11-18

The blank run reached extension **41** in approximately **3.30025885 × 10^208156** defined instructions. Its saved tape has 2,948,584 nonzero cells, including 20 aligned terminal copies of 421. Extension 40 had a 487,078-bit clock, so the interval from 40 to 41 alone also rounds to 3.30025885 × 10^208156 instructions. The timing formula for any one interval is four defined instructions plus its full ordinary request cost. A terminal digit test explains most of the observed changes in that reserve. It does not bound their cumulative sum across future extensions. [Full extension-41 tape and integer clock](compress33-41.json) · [Single-extension protection theorem](reserve33.md)

## Established counter and raw clock

Use the [ordinary return rules](neglected33.md). A denotes a request on the first cell of the indicated word. A completed ordinary request returns in A at the cell immediately to its left. Let V(n) be the word after n requests on a virgin suffix. Its digits, read from **least to most significant**, are exactly the balanced ternary expansion of n. Write 24 for 0, 21 for +1, and 14 for −1. In particular a nonempty expansion always ends in 21.

On a previously untouched pair, one request creates 21. If n>0, the final pair has phase (n−1) mod 3 in the cyclic order (21,14,24) and forwards m = floor((n+1)/3) requests. Thus n−3m is its signed digit, and m<n. This proves the claim inductively. If the expansion uses K pairs and contains J negative digits, its complete raw clock is **5n + 4J − 2K** (zero for n=0).

For the timing identity, number the three existing pair phases 0,1,2. On a stable pair with n requests and initial phase h, set b=(h+2) mod 3 and write n+b=3m+r. The final phase is (r+1) mod 3 and the child receives m requests. The local raw cost is

$$5(n-m)+4\big([h_{\rm final}=1]-[h=1]\big).$$

Each individual cycle edge has cost 4, 1 or 5, so the formula telescopes for any batch. Initializing a virgin pair has the same phases as starting at phase 2, with two fewer local steps. Summing along the virgin suffix proves the clock above. For the other stable pair, 22, the child count doubles and the local cost is seven times the input count. Consequently a run of k such pairs passes $2^k n$ requests at local cost $7(2^k-1)n$. The new worker uses this identity, base-three conversion for the virgin word, and groups up to 39 ternary pairs in one division. At all remaining prefixes it follows the prior local rules, stopping when it requires an exceptional solitary 2.

## Which terminal digits decide the gain

Set C=421. In the [one-block protection theorem](reserve33.md), an epoch begins with a displaced digit, an aligned register of pairs, and a right reserve C^r. Moving the displaced digit through the register requires two counts. For a request count a, a displaced digit d, and an inner count s, the unprocessed part is $F^a(d F^s(\text{remaining word}))$. The positive outer count can run out before the end. The following test applies when the scan reaches the edge with the indicated carry.

After entering a strip of ternary pairs with a carry in U=(1,0), V=(4,0), or W=(4,1), the carry stays in this set for as long as the outer scan continues. The first component is d and the second is s. Three ternary pairs also suffice to reach this set from *any* d and s≤3: enumerating the local rules leaves five states after one pair, four after two, and these three after three. Their exact transitions are:

| Carry | +1 (21) | −1 (14) | 0 (24) |
| --- | --- | --- | --- |
| U | U | V | V |
| V | W | V | U |
| W | W | U | W |

The mandatory high +1 sends the scan to U or W. With r≥1, U means $1 C^r = 14\,21\,C^{r-1}$, consuming one aligned block. W means $4F(C^r)=4\,21\,C^r=C^{r+1}$, gaining one. Subsequent requests through those aligned pairs or the pure C suffix create only ternary pairs ahead of the retained reserve. Maximal *aligned* reserve counts therefore change by exactly one in these cases. The alignment matters: two extra C blocks would end in 42·14·21, and 42 is not a stable pair.

Even without the state on entry, the **nine most significant balanced-ternary digits** decide the sign for **5,168 of 6,561** possible such prefixes. To see this, work backwards from the final +1. Its preimage for a loss is the singleton U. The subset of starting states leading to a loss is either empty, full, or splits the three states into one distinguished state and the other two. Ignore which side is complemented when counting unresolved splits. A split distinguishing U stays unresolved for all three preceding trits, once with U distinguished and twice with V or W distinguished. A split distinguishing V or W has one transition to a U split, one to a V/W split, and one resolved transition. The two live counts therefore update by $(x,y)\mapsto(x+y,2x+y)$. For k free high trits before the mandatory +1 the total unresolved count has $T_0=1$, $T_1=3$ and $T_{k+2}=2T_{k+1}+T_k$. In particular $T_8=1393$. The verifier exhausts all these prefixes.

## Comparison with the actual blank orbit

For each stage 3 through 33 we traced the two counts and compared the **complete** next word and raw cost with the original ordinary evaluator. The scan reached the cut on every stage. Stage 3 exhausted the outer count exactly there. Stages 4–33 all reached it with positive count. Their losses were stages **5, 12, 17, 18, 19, 25, and 27**. All other stages in that range gained one aligned copy. Stage 33 started with 16 such copies and ended with 17. Separately, among the 23 stages in this trace whose previously generated virgin strip contained at least nine ternary pairs, **20** had their sign determined from the top nine pairs alone. In each eligible case the verifier checks the entry state, continuation through the strip, its provenance from a real earlier virgin batch, and the observed sign. [Reproducible per-stage trace](compress33-shift-verification.txt)

These finite results do not establish a drift rate. A uniformly drawn penultimate trit independent of the incoming state would put the carry in U one third of the time, since each table row has one U. No independence result identifies the penultimate trits on this orbit with that sampling rule. The actual three consecutive losses show why a one-stage gain is insufficient for an inductive lower bound. Unbounded running time or a halt-time estimate would require control of the actual sums or the eventual exceptional return.

## The same one-block guard can lead to either decision on other tapes

Use the real outer schedule throughout, with the head in A on zero at coordinate zero, the word `2y` immediately right and all other cells blank. For $y=2C$ (empty aligned register), the machine reaches B at −2 with precisely $C^8$ to its right after 234 raw instructions. Hence it enters the [proved infinite sweep family](neglected33.md#all-exceptional-replies-and-an-infinite-sweep-pattern). Inserting just two aligned 22 pairs gives $y=2\,(22)^2 C$. This machine completes five ordinary extensions and halts on B3 at +34 after **39,142** instructions. Both outcomes are literal checks. Thus even the exact schedule and an initial aligned reserve of one do not decide the future sign sequence. These are modified starting tapes.

## Reproduce and continue

From this directory, build with a C++17 compiler and GMP with 64-bit unsigned long. The first program compares 1,560 ordinary outputs and clocks against the original batch evaluator, and 936 exceptional flags. Within that set it checks 1,423 complete tapes and clocks by literal execution. The checks include arbitrary mixed words, high counts, and counts on both sides of powers of three. The independent shift calculation checks every stage 3–33 and the terminal-state prediction. The [second native evaluator](compress33_cross.cpp) uses the shifted register, the two observed terminal phases and biased ternary conversion. It replays from the complete extension-33 tape. Its final comparison covers every occupied cell, head, state, and exact integer clock. Both native calculations lack formal verification. [Verification results](compress33-verification.txt)

```sh
c++ -O3 -std=c++17 compress33.cpp -lgmpxx -lgmp -o /tmp/bb33-bulk
python3 compress33.py --engine /tmp/bb33-bulk --verify --epoch 41 --save /tmp/bb33-41.json
cmp /tmp/bb33-41.json compress33-41.json
c++ -O3 -std=c++17 compress33_cross.cpp -lgmpxx -lgmp -o /tmp/bb33-shift
python3 compress33.py --engine /tmp/bb33-shift --shifted --epoch 41 --save /tmp/bb33-cross.json
cmp /tmp/bb33-cross.json compress33-41.json
python3 compress33_shift.py 33
```

Use `--resume compress33-41.json --epoch 42` with the ordinary bulk worker to continue. [Bulk worker](compress33.cpp) · [Controls and checkpoint replay](compress33.py) · [Timed shifted scan and sign check](compress33_shift.py)

**Next proof step.** Bound the reserve deficit for the high-digit sequences that the integer transfers actually generate. A proof must also handle a scan that stops before its newly written ternary strip. The 28 eligible penultimate-trit/carry pairs are listed in the per-stage trace for testing hypotheses about that dependence. For example, targeting a bound on the total losses before the next certified gain would address the three-loss excursion that an invariant based solely on the current terminal pair misses.
