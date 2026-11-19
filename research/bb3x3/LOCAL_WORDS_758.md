# Short ordinary histories at a fixed #758 mass

Fix any integer mass coordinate $u_*$ within $10^{100}$ of the halting seed $H$. Specify a fine ordinary word with $n\le291$ elementary calls, and specify any grouped boundary of this word as the cut. There are at least $3^{291-n}$ distinct odd/odd configurations at **that exact mass** realizing the specified word and cut, with no reset anywhere in the word. The uniform threshold is sharp. A word of 292 consecutive jumps cannot occur at these cuts with a reset-free start. At 292 calls the [reconstruction bound](SEPARATED_FACTORS_758.md) also gives at most one candidate for any prescribed word ending at $u\le H$.

This applies inside the joined halting basin, where all resets lead to a halt. It shows why testing which local ordinary words are physically possible, even with both their fine residues and the exact central mass specified, supplies no forbidden word through 291 calls. It does not show that any of the constructed configurations is reached from blank or survives passage through the basin.

## Constructing the configurations

Write $h=(a+1)/2$, $d=(c-1)/2$ and $u=h+2d$. An ordinary jump $J$ has charge 2 in $u$. An ordinary pair $P_s$, labelled by $s=d\bmod4$, has charge $v_s$, with $(v_s,b_s)$ equal to $(5,20),(9,35),(7,26),(7,29)$ in label order. The mass at every phase is determined by the cut and its word. Throughout the proof these masses exceed $3Q+100$, where $Q=3^{291}$, and are less than $2\cdot3^{292}$. These integer inequalities still hold at a distance of 2,628 mass units beyond the specified range.

At the end of each prefix the integral histories, before checking guards, select exactly one residue for $d$ modulo $M=3^{\text{calls}}$. Start with $M=1$. A jump sends the residue $z$ to $3z-u+1$ modulo $3M$. A pair sends it to $(9z+b_s)/4$ modulo $9M$, using the inverse of four. In reverse, the latter condition gives an integer $(4d-b_s)/9$ with the specified label modulo four. These operations thus preserve every required integrality condition.

Suppose the word contains a pair. Choose any terminal $d$ in this residue class among the $Q$ integers beginning at $L=\lceil Q/16\rceil$. There are exactly $Q/3^n$ choices. Their terminal $h=u-2d$ exceeds $2\cdot3^{289}$. Pull the word back using the exact unguarded maps. Every resulting $h$ stays at least two. A reversed jump divides $h$ by three, and a reversed pair with predecessor mass $u$ gives
$$
h_{\rm prev}=(4h+5u-4v_s+2b_s)/9 \ \ge\ 5u/9 > 2\cdot3^{289}.
$$
Since the word contains a pair, every jump run has at most 289 jumps. The same argument for $d$ starts with $d\ge L$. A reversed jump sets $d_{\rm prev}=(d+u-1)/3\ge L$ for nonnegative $d$. A reversed pair satisfies $d_{\rm prev}+7\ge4(d+7)/9$ because $b_s\le35$. There are at most 145 pairs in any run, and $(4/9)^{145}(L+7)>7$. Consequently $d\ge0$ throughout.

All these formal moves meet the physical guards. For a jump this follows from nonnegative output $d$. For a pair both bulk decrements are positive and the left counter after both is at least three, so each decrement is legal and leaves the intermediate left counter above one. All right counters are positive. The inverses on this fixed word are injective in $d$ at fixed mass, yielding distinct cut configurations.

For a pure jump word, start with $h=2+(u_{\rm start}\bmod2)+2i$ for $0\le i<3^{291-n}$. All $h$ remain at most $3Q$ and at least two, so every jump is legal. Conversely 292 jumps would give $h_{\rm end}\ge2\cdot3^{292}>u_{\rm end}$.

The [witness constructor](local_words_758.py) implements the construction for an arbitrary word, split and index. Running it beside the other checkers verifies the integer bounds and replays 3,711 short word/split pairs at both endpoint indices, plus 540 long examples, through the original counter map.

```sh
python3 local_words_758.py
```
