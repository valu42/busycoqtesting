# Ordered pairs and the inverse checkpoint map on line 26

The blank decision for `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA` remains open. The aligned upper word uses digits $2u_i+e_i$ from low to high. The three lower ordinary pairs return to zero bits on each tick. The first actual blank tick ends with upper word `21`. Eight physical epochs make one tick. [Literal tape convention](column-phases.md#coordinates-and-the-scalar-word)

## All ordered-pair counts still lose necessary information

For a finite word $w$ define $N_a$ as its number of digits $a$ and $N_{ab}$ as the number of index pairs $i<j$ with $w_i=a$ and $w_j=b$. Adjacency is unrestricted. There is **no inductive blank-safety invariant depending only on the four $N_a$ and sixteen $N_{ab}$**, even if the invariant also knows the current epoch, guard length and width. This includes arbitrary nonlinear functions of those counts.

The following finite certificate consists of ordinary machine execution with four explicitly marked word replacements. All replacements preserve every displayed statistic. The blank machine itself follows only the prefix before the first replacement.

| Completed tick | Upper word before replacement | Upper word after replacement |
|---:|---|---|
| 8 | `0102201000` | `0012210000` |
| 16 | `0113330100000` | `1130303001000` |
| 24 | `10033321330000` | `13303021030003` |
| 27 | `200232212301032` | `022210303222301` |

Start from A at coordinate zero on the two-way blank tape. Follow the ten-entry transition table. At each indicated checkpoint replace only the upper data pairs, encoding each new digit using the same two physical symbols. The left guard, head, tape width, epoch and end marker stay fixed at that replacement. From the final replacement the machine executes 10,842 defined instructions and reaches B3 at coordinate 39 during its next tick. The script replays the whole certificate from the literal blank, including each intervening tape and the final undefined instruction. Pair counts can be checked by scanning left to right and adding the current $N_a$ to $N_{ab}$ whenever reading $b$.

An inductive safe family of the stated kind would contain the genuine first checkpoint. At every replacement it would assign the same truth value to both words. Its closure and guaranteed safety for the next tick would propagate membership along every intervening ordinary segment. The final segment contradicts that guarantee. The certificate also works with any clocks carried unchanged by a replacement and advanced by their ordinary machine rules, provided membership uses the tape only through the stated counts. This excludes an abstraction of the tape. It does not exhibit a blank halt.

## A unique predecessor and its stopping test

Take any finite upper word with packed counters $(u,e)$ and width $m$. At each tick the all-ordinary map applies nine $P$ subtractions and one $Q$ increment. The positive process has a partial, single-valued inverse. An output with $e\mathbin{\&}\mathord{\sim}u=0$ has no ordinary predecessor on the nonnegative counters. In digit language it contains no 1.

Otherwise let $b$ be the lowest set bit of $e\mathbin{\&}\mathord{\sim}u$. Undo the $Q$ by
$$
 e_0=e\mathbin{\mathrm{xor}}\big((\mathord{\sim}u)\mathbin{\&}(2b-1)\big).
$$
Indeed binary increment on the positions outside $u$ created its first selected one at that stopping bit and cleared all preceding selected ones. The inverse has $0\le e_0<e$. Set $S=2e_0+1$. To undo each of the nine $P$, take $b$ as the lowest set bit of $S\mathbin{\&}\mathord{\sim}u$, with $b=0$ for the empty intersection, and set
$$
 u\gets u\mathbin{\mathrm{xor}}\big(S\mathbin{\&}(2b-1)\big).
$$
This is ordinary increment on the selected digits of $u$. The case $b=0$ undoes one forward wrap, since the forward sparse subtraction had set all its selected bits. Subtract one from the candidate earlier width for each such case.

There is a physical predecessor exactly if the reconstructed width is nonnegative and both reconstructed counters fit. They then encode its unique tape. Each safe operation takes finite time and adds its pair exactly at the counted wrap. The last dangerous operation stops at a set bit of the supplied finite output. This verifies the physical forward step. Conversely, any successful predecessor must have these bits and this width by the two binary inverse operations. Every backward chain on nonnegative ordinary counters terminates, since its $e$ decreases on every tick. For physical words it can also terminate earlier on the width test. The genuine first word `21` has no physical predecessor among the normalized words already possessing all three bottom pairs. The literal five-step entry and the first eight epochs supply that initial checkpoint.

This gives a direct backward test for the ancestry of any proposed finite halting tape. A proof excluding blank ancestry for all possible terminal words is still needed. The checker verifies both inverse directions on all 5,461 inputs of widths zero through six.

Run `python3 column_order.py` with assertions enabled. [Literal interpreter and inverse](column_order.py) · [Observed output](column-order-verification.txt)
