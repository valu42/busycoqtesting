# Line 33 · what would justify a nonhalting forecast?

The blank orbit has a reserve of aligned `421` blocks. **One such block guarantees ordinary completion of a request batch on the shifted canonical register.** The open question is whether the actual sequence of shifts can exhaust that reserve and then take a halting branch. The [protection and congruence argument](reserve33.md) and [complete blank checkpoints](compress33.md) concern the exact machine `1RB2LA0RB4LB1RA_1LA3RA1RA---0LA`.

## A model with a checkable assumption

Consider stages of the type observed at stages 4–33: the scan reaches the end with a positive outer count, the two calibrated final states determine the outcome, and the reserve changes by exactly one. At stages with a previously generated ternary suffix of at least two pairs, the penultimate trit and the state on entry to that trit determine the sign. The most significant trit is fixed at +1. Of the three possible penultimate trits, exactly one would produce a loss for each incoming state.

| State before the penultimate trit | Loss trit | Counts in stages 6–19 (+1, −1, 0) | Counts in stages 20–33 (+1, −1, 0) |
| --- | ---: | ---: | ---: |
| U | +1 | 0, 3, 3 | 0, 3, 2 |
| V | 0 | 1, 1, 1 | 0, 2, 1 |
| W | −1 | 1, 3, 1 | 3, 1, 2 |

The two disjoint stretches have **4 losses in 14 stages** and **2 losses in 14 stages**. The earlier slice includes three consecutive losses. The later slice still has no +1 input in U, even though the exact transition table allows it. Both the state and the trit come from the generated register. Counting the three allowed trits does not show that each occurs with equal probability conditional on the state. [Chronological data and replay](compress33-shift-verification.txt) · [Checker](compress33_shift.py)

A sensitivity calculation makes the statistical assumption explicit. Suppose every future stage with a positive reserve stays in the calibrated ±1 regime, and a proposed probability law on future histories gives a conditional chance of loss at most $p<1/2$ after **every** surviving history. Starting at reserve $r$, that model gives
$$
\Pr(\text{ever reaching zero reserve})\le \bigl(p/(1-p)\bigr)^r .
$$
Indeed with $c=p/(1-p)$ and current reserve $R$, the conditional expected value of $c^{R_{\rm next}}/c^R$ is bounded by $p/c+(1-p)c=1$. Stop when the reserve first reaches zero or after a finite horizon. The probability of hitting zero by then is at most $c^r$. Increasing the horizon proves the bound. Halting requires leaving the protected region under these assumptions; hitting zero alone does not decide the subsequent machine.

Taking $p=1/3$ would produce $2^{-r}$. Uniformity of the relevant trit conditional on its incoming state and the full past would suffice for this example. The mandatory top digit, the [cross-stage congruences](reserve33.md), and the small observed cells in the table leave that hypothesis unverified. Even matching the overall loss frequency would not establish a bound after every history. The outlook remains **Unknown**. There is no raw-step median deducible from this comparison.

A more direct proof target is deterministic: bound the largest excess of losses over gains on **every prefix** of the actual future sequence before another exceptional type of stage occurs. A bound below the current reserve, together with an argument covering the remaining stage types, would settle survival. Merely finding a positive limiting average would leave early exhaustion possible.
