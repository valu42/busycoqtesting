# Reset gaps on a known section of the blank orbit

Between the two proved blank resets **17,354,320,242,846,420** and **18,378,934,934,402,308**, the orbit makes exactly **11,538,952,370,487 consecutive first returns**. These take a total of **461,257,167,560,842 counter calls**. The longest of these return times is **134 calls**. A call means one update of the two-counter map. [Blank crossings](POWER_CROSSINGS_758.md) · [Exact raw clock](FOURTH_GATEWAY_758.md)

| Calls to the next reset | Number of occurrences |
|---:|---:|
| 39 | 7,792,944,006,905 |
| 42 | 3,746,008,362,829 |
| All other lengths combined, maximum 134 | 753 |

The [verifier](blank_return_profile_758.py) starts at the guaranteed merger before the fourth candidate pair. It replays 425 literal first returns to the odd corridor. Its complete word is $J^{34}L^7R$, hence each return takes 42 calls. The returns in the next even corridor have word $I J^{33} L L J L R$ and take 39 calls. In each corridor the seed increment depends only on the residue modulo a known power of two. Cycling its exact positive increments counts every first return up to the specified boundary. The remaining returns are timed individually using the original counter instructions. The verifier prints the complete length histogram.

Short gaps on this connected section support looking for a reset inside the [known halting intervals](LOWER_SCALE_GATES_758.md). The section also shows how strongly these observations depend on one another. All but 753 occur in two fixed-word corridors, both at reset parameters of order $10^{16}$. The large halting target has 140 digits. These counts give an exact description of the observed segment and provide no sampling law at that distant target.

~~~sh
python3 blank_return_profile_758.py
~~~
