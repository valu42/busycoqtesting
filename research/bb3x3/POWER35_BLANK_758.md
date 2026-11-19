# The power-$3^{35}$ checkpoint on the blank orbit

After bypassing the fifth candidate pair, #758 on blank tape reaches the exact reset
$$A(1,3^{35}+34{,}754)=A(1,50{,}031{,}545{,}099{,}034{,}461).$$
It gets there after **more than $1.48278\times10^{48}$ and fewer than $1.98846\times10^{48}$ original Turing-machine steps**. The result also applies to #153 with a clock 50,707 steps smaller. The full blank-tape outcome remains open. [Fifth crossing](FIFTH_BLANK_CROSSING_758.md) · [Power-gate theorem](POWER_GATES_758.md)

From the fifth crossing at $K+118=40{,}486{,}323{,}621{,}582{,}766$, divide the interval up to $F=49{,}454{,}910{,}341{,}926{,}411$ into 897 windows of stride $10^{13}$, shortening the last one. Every odd reset throughout the gap returns to an even reset, gaining either 73 or 75. In 763 windows every even seed follows a single checked ordinary word through a live reset. Matching endpoint guards suffice for all intermediate seeds. The upper gain bound including an odd normalization is at most 5,000. Strictly increasing even resets therefore carry every input in the incoming 5,001-seed interval to an even reset in the outgoing interval. For the other 134 windows the exponent-34 packed worker checks all incoming possibilities. Each of its exact output bounds lies inside the next admitted interval. [Packed receipts](power35_packed_758.tsv) · [Even-seed checker](EVEN_POWER_758.md)

Every reset in $[F,F+5{,}000]$ enters the existing $3^{35}$ gate. The even short word starts sharply at $F+1$ and the odd one already holds at $K+119$. Each gain is at most 99, so the run cannot jump the whole gate. Its 13 possible exits merge along 550 distinct first-return edges at the stated checkpoint. The verifier checks the endpoint guards, the preceding even seed, the exit set and the merger. [Verifier](next_gate_after_fifth_758.py)

A sufficient next connection is a blank reset between 90,056,781,178,199,398 and 90,056,781,178,204,398. Every start in this window reaches **$2\cdot3^{35}+155{,}534=100{,}063{,}090{,}198{,}154{,}948$**. Its two guarded words have 39 boundary exits that merge along 1,893 edges. The link from the reached $3^{35}$ checkpoint to this next incoming window remains open.

## Raw time

| Clock at the reached checkpoint | Rigorous lower bound | Rigorous upper bound |
|---|---:|---:|
| #758 from blank | 1,482,784,176,152,518,686,967,781,313,684,540,616,202,754,440,890 | 1,988,454,072,317,701,732,753,123,726,748,110,537,604,032,294,736 |

Start with the proved clock at $K+118$ and apply the same bounds for the elapsed raw time between successive mass cuts. The simple windows guarantee selected reset gains below 5,001. The paired windows use the same bounded counter operation budget as those leading to the fifth crossing, so the first actual reset at or beyond any interior time cut overshoots by at most 100,000. Inside the gate itself the two short words give a bound of 99 up to $3^{35}-74$. The final merger uses the angular upper potential; its elapsed time is omitted from the lower bound. The full integer clock check is included with the replay below. [Clock method and incoming time](FIFTH_BLANK_CLOCK_758.md)

~~~sh
python3 next_gate_after_fifth_758.py --receipts power35_packed_758.tsv --require-complete --clock
c++ -O3 -std=c++17 -DPOWER_EXPONENT=34 cross_even_power_758.cpp -o cross_even34
python3 next_gate_after_fifth_758.py --receipts power35_packed_758.tsv --worker ./cross_even34 --jobs 4
~~~
