# The fifth candidate on the actual BB(3,3) blank orbit

The consecutive resets of #758 at the fifth candidate pair are **40,486,323,621,582,550 and 40,486,323,621,582,766**. The candidate seeds $K=40{,}486{,}323{,}621{,}582{,}648$ and $K+2$ lie strictly between them. This eliminates that particular terminal from the blank orbit of both #758 and #153. The clock at the later reset is between $7.80097\times10^{47}$ and $1.08733\times10^{48}$ original #758 steps. The fate of the full machine remains open. [Clock bounds and reproduction](FIFTH_BLANK_CLOCK_758.md) · [Machine equivalence](RANKINGS.md)

| Known entry | Checked transfer | Consequence for the blank orbit |
|---|---|---|
| Fourth checkpoint, 18,378,934,934,402,308 | 5,820 successive windows of width up to $2\times10^{12}$, ending at 30,018,927,059,399,750 | Reaches a reset at that cut or up to 5,000 above it. [Window table](double34_crossings_758.tsv.gz) · [Verifier](check_double34_758.py) |
| That entire exit interval | The two short gate words carry it to the doubled power at exponent 34. All possible gate exits coalesce in a total of 693 first-return edges. | Reaches the exact reset $2\cdot3^{34}+32{,}211=33{,}354{,}363{,}399{,}365{,}349$. [Gate theorem](POWER_GATES_758.md) |
| Doubled-power checkpoint | 640 successive windows of width up to $10^{13}$, ending at 39,752,584,607,270,532 | Enters the previously proved fifth-pair approach. [Window table](fifth_power_bridge_758.tsv) · [Verifier](check_fifth_power_bridge_758.py) |
| Every exit of the second chain | Two ordinary return words and two certified transfers merge the possibilities at $K-198{,}990$. | Exactly 1,054 further first returns give $K-98\to K+118$ as the crossing. [Local merger and verifier](FIFTH_CROSSING_758.md) |

A window with cuts $x,y$ proves that each reset in $[x,x+5{,}000]$ reaches a later live reset in $[y,y+5{,}000]$. Thus the rows compose even when a worker keeps more possible exits than the actual run visits. In particular, the second chain can mix rows certified with the [ordinary worker](cross_758_fast.cpp) and the [even-seed worker](EVEN_POWER_758.md). The latter advances an odd seed by its exact live first return before working on even seeds. Each worker checks all possible incoming points. The first chain starts at the [blank checkpoint proved after the fourth pair](POWER_CROSSINGS_758.md).

Starting from either $K$ or $K+2$, the 69th counter call halts at input $A(26{,}990{,}882{,}414{,}388{,}552,26{,}990{,}882{,}414{,}388{,}551)$. Exhausting the 585 states in its inverse tree finds exactly those two possible last resets, both at depth 68. Reset parameters strictly increase. Their omission at the consecutive crossing rules out this terminal at any later time as well. [Terminal ancestry](MIXED_TERMINALS_758.md)

## The next power checkpoint

Put $F=49{,}454{,}910{,}341{,}926{,}411$. A reset in $[F,F+5{,}000]$ forces the exact later reset **$3^{35}+34{,}754=50{,}031{,}545{,}099{,}034{,}461$**. From $F$ onward both parity words hold up to the start of the established $3^{35}$ gate. For the even word the first allowed even seed is $F+1$. The preceding even seed takes a different word. For the odd word the lower endpoint can already be taken at $K+119$, the first odd integer above the fifth crossing. Endpoint order proves the guards in between. The live words increase the reset parameter by at most 99. From $[F,F+5{,}000]$ one therefore enters the old gate, whose 13 possible exits merge along 550 distinct first-return edges. [Next-gate checker](next_gate_after_fifth_758.py) · [Gate table](power_gates_758.tsv)

The stretch from $K+118$ to $F$ lies entirely in the certified domain of the exponent-34 even-seed worker. At stride $10^{13}$ the gap consists of 897 windows. In **763** windows, both extreme even seeds follow the same ordinary word to a live reset. Odd seeds convert to even with gain at most 75. Including this normalization, every return used by these 763 checks advances at most 5,000 seed units, so each window sends its entire input to the next window alive. **134 windows**, including the first, still need a different argument. Reaching this checkpoint would still leave the link from blank to the 140-digit halting target open.

## Reproduction

The first two commands check completeness, indexing and endpoint containment of both receipt tables. The last two replay the local crossing and the next-power condition. For a full computational replay, pass a compiled ordinary worker to the first verifier with `--worker` and both the ordinary and exponent-34 paired workers to the second verifier with `--ordinary` and `--paired`. [Build and audit instructions](EVEN_POWER_758.md)

~~~sh
python3 check_double34_758.py
python3 check_fifth_power_bridge_758.py --require-complete
python3 fifth_crossing_758.py
python3 next_gate_after_fifth_758.py
~~~
