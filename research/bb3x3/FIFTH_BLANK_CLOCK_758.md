# Raw clocks at the doubled power and the fifth candidate crossing

The first crossing chain carries the blank orbit of #758 from the known fourth checkpoint to the exact doubled-power reset. The second chain carries that reset to the fifth candidate pair. The two verified chains make both rows unconditional for the blank run. [Window receipts and proof](FIFTH_BLANK_CROSSING_758.md) The clock calculation reuses the [fourth checkpoint bounds](CROSSING_CLOCK_758.md). The raw clock for #153 is exactly 50,707 steps smaller throughout.

| Reached reset $A(1,s)$ | Required path from the fourth checkpoint | Lower bound on #758 raw steps | Upper bound on #758 raw steps |
|---|---|---:|---:|
| $s=2\cdot3^{34}+32{,}211=33{,}354{,}363{,}399{,}365{,}349$ | First chain | $4.36590\times10^{47}$ | $5.91417\times10^{47}$ |
| $s=K+118=40{,}486{,}323{,}621{,}582{,}766$ | Both chains | $7.80097\times10^{47}$ | $1.08733\times10^{48}$ |

The displayed bounds round outward. At the fifth pair, the consecutive resets are $K-98$ and $K+118$. The machine spends exactly **21,237,958,453,334,090,217,030,746,043,349,705** raw steps between those two resets. Its blank halting time remains open. [Fifth crossing](FIFTH_CROSSING_758.md) · [Clock verifier and integer bounds](fifth_blank_clock_758.py)

## Reachability requirements for the clock calculation

1. The first chain must certify all windows from 18,378,934,934,402,308 to 30,018,927,059,399,750. From the latter cut both short gate words continue up to the even cutoff $2\cdot3^{34}-74$. Their increments are at most 77. The proved gate merger then supplies the exact reset $2\cdot3^{34}+32{,}211$. [Grid and gate verifier](check_double34_758.py)
2. The second chain must certify all windows from the doubled-power reset to $B=39{,}752{,}584{,}607{,}270{,}532$. The common words from $B$ through $K-10^{14}$ have increments at most 99. The two existing window transfers from there end at $K-198{,}990$. Exactly 1,054 subsequent first returns take 20,265,035,542,707,572,423,545,951,432,277,768,588 raw steps and reach $K+118$. [Local proof and window transfers](FIFTH_CROSSING_758.md)

In both chains, at every cut $z$ inside a certified grid, the first actual reset at or beyond $z$ has seed at most $z+100{,}000$. The ordinary worker's certified increments are below that limit by its elementary update budgets. The paired exponent-34 worker can add at most 75 seed units for the final odd-to-even normalization. Its 256 cached phases and 5,000 further paired operations increase the seed by fewer than 50,000 units altogether, including the launch. Earlier actual first returns only shorten these gaps. These bounds also cover cuts inside the two ordinary transfers after $B$. [Ordinary-worker bounds](CROSSING_CLOCK_758.md) · [Paired worker](EVEN_POWER_758.md)

## Timing intervals

Use the first actual resets at or above each successive cut. The common-word estimator bounds the raw duration of the disjoint intervals between these resets and computes a guaranteed saving against the telescoping upper potential $S(1+2s)$. Start each leg from the previously certified clock interval. Add $\lfloor S(1+2s_{\rm end})-S(1+2s_{\rm start})\rfloor$ to the old upper bound, then subtract the savings. Add each common-word lower credit to the old lower bound. Uncovered portions contribute zero lower credit and no saving. The program divides the grid and short-word sections into intervals of at most two trillion seed units, with up to eight bisections. For the gate merger beyond the even cutoff and the final ten seed units before $K-198{,}990$, it uses only the potential for the upper bound. It times each of the 1,054 final returns directly. [Interval bounds and potential proof](CROSSING_CLOCK_758.md)

Run `python3 fifth_blank_clock_758.py` to recompute the clock bounds. Reachability is checked separately by the window and gate verifiers.
