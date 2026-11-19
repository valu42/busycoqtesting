# The bulk corridors between the last annular checkpoint and the target

Let $Y$ be the [last annular checkpoint](ANNULAR_MERGERS_292_758.md), $H$ the halting reset, and $G=10^{10}3^{264}$. **The scale-264 corridor is the last of 368 disjoint corridors with the same form of first-return word. The gap between it and the preceding corridor measures $3.7236940920\times10^{135}$ reset units.** In a separate search, the only ordinary direct-terminal origins in $[Y,H]$ with at most two runs of jumps after the initial power launch were $H-2$ and $H$. The [exit-merger calculation](CHECKPOINT_Y_758.md) reduces all possible entries into each corridor to one later reset, and joins the first corridors to the actual trajectory from $Y$. Blank reachability of $Y$ remains open.

## The common opening

The exact checkpoint is $Y=\lfloor3^{301}/19171\rfloor+4{,}510{,}976$. Every odd seed from $Y$ through $H$ executes $J^{292}Q^4JQ^2$, where $Q$ is two ordinary bulks. The two endpoints verify the opening by the order in the left and right counters. Every even seed here has its previously certified [300-call ordinary return](RESET_WORDS_758.md).

Use $u=(a+2c-1)/2, d=(c-1)/2$. Immediately after $J^{292}Q^4J$, an odd seed $s=Y+x$ has
$$
 u=Y+x+g_r,\qquad 512d=19171x+\beta_r,\qquad r=x\bmod512 .
$$
Before the four pairs, translating the seed by 512 increases $u$ by 512 and $d$ by 256. All four pair input residues are preserved, so the mass translation stays 512 and the translation in $d$ becomes $9^4=6561$. The following jump $d'=3d-u+1$ changes the latter to $3\cdot6561-512=19171$. The 256 even residue representatives give $606\le g_r\le622$ and $86{,}491{,}247{,}812\le\beta_r\le86{,}491{,}353{,}110$.

## What the corridors cover

After the common opening through its first postlaunch jump, propose $k$ unguarded bulks. On an odd $k$ the result $(a_k,c_k)$ gives a genuine first-return word $L^k R$ exactly when $0\le a_k\le c_k$. Nonnegativity proves the preceding bulk guards because each subtracts its own guard threshold from the left counter. The minimum left coordinate and maximum right coordinate move monotonically as the seed increases. Two integer bisections therefore give the first included and first excluded odd seeds. Each intervening even seed also returns.

The nonempty corridors occur exactly for odd lengths from 7 through 741. Together their widths are 39.98916766% of $H-Y$. The $k=741$ odd interval begins at $Y+1{,}750{,}734$ and ends just before $Y+4{,}881{,}882$. The $k=9$ interval runs from distances $2.212726071G$ to $1.940615301G$ below $H$. The $k=7$ interval runs from $1.532330935G$ to $0.919638267G$ and is the [scale-264 word](SCALED_GATES_758.md) with zero jumps in its variable run. Thus 14.81030547% of the entire distance $H-Y$ lies in the single gap between these last two corridors. The width counts allow either side of each parity cut an endpoint convention of one seed; all displayed distances use the exact odd endpoints.

## Searching for another halting origin

A direct ordinary terminal after at most two postlaunch jump runs must have the form
$$
 J^{292}Q^4 J Q^b J^j Q^f L
$$
followed by the halting instruction. The common opening forces the first jump run to have length one. For $j=0$ all subsequent pairs may be assigned to $b$. Monotonicity and replay at $Y$ give $b\le371$. After $b$ pairs the coordinate $h=u-2d$ is positive. The putative 293rd jump would have $h\ge3^{293}>H+622+9\cdot371+2\cdot293$, contradictory to its available mass. For the final pairs, starting at the smallest $d=0$ and bounding the mass after $n$ pairs above by $H+622+9\cdot371+2\cdot293+9n$ makes the 393rd complete pair impossible. These are bounds on all legal words of this form.

Use the [terminal-strip inversion](POWER_CUSP_TERMINALS_758.md) for $Q^bJ^jQ^fL$. Suppose the inverted necessary strip is $l\le Nd-Au\le h$. The header identity gives an admissible interval in $x$ after division by the positive denominator $19171N-512A$. Its lower numerator is $512A Y+512(l+A g_{\min})-N\beta_{\max}$, and its upper numerator is $512A Y+512(h+A g_{\max})-N\beta_{\min}$. Check every even integer in this interval using its exact residue lane and all the ordinary guards. Across 42,689,604 classes there were 118,031,730 candidate occurrences, 430 after the eight-pair filter, and two exact hits. Both had $b=2,j=f=0$. Any earlier ordinary direct terminal in $[Y,H-4]$ would need at least three separate runs of postlaunch jumps.

Run [secondary_cusp_758.py](secondary_cusp_758.py) for the corridor edges and the literal success and failure checks at their neighbors. Compile [power_cusp_terminals_758.cpp](power_cusp_terminals_758.cpp) with `c++ -O3 -std=c++17 power_cusp_terminals_758.cpp -lgmpxx -lgmp -o cusp_terminals` and run `./cusp_terminals --secondary-runs` for the terminal census.
