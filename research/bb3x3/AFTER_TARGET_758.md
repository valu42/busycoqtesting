# What happens when a reset misses the large #758 target?

Let $H=(3^{307}-8\,282\,708\,212)/13\,959\,275$ be the known 140-digit halting reset. Define $E$ as the last odd seed in the ordinary return corridor immediately above $H$ specified below. Put $C=E+7\,784\,831$. **Every reset from $H+1$ through $E+647$ reaches exactly $A(1,C)$.** The corridor extends about $0.05871946\%$ of $H$, or $1.25934\times10^{136}$ reset units. The exact integer $E-H$ is in the [checker](after_target_758.py).

Immediately below $H$, the outcomes can also be counted exhaustively. The following fractions refer to a uniform choice of reset seed within the stated inclusive interval.

| Initial reset seeds | Halt by the encounter with the $H$ terminal | Cross $H$ alive |
|---|---:|---:|
| $H-3{,}403{,}054$ through $H$ | 2,240,541 of 3,403,055 (65.8391%) | 1,162,514 |
| $H-33{,}533{,}929{,}283{,}358$ through $H$ | 33,533,928,120,845 of 33,533,929,283,359 (99.9999965%) | 1,162,514 |

Exactly 2,238,030 seeds in the first row reach the terminal through last reset $H$, and 2,511 through $H-2$. Both last resets give the same terminal. Among the remaining starts, the next reset above $H$ is one of 346 offsets from $H+2$ through $H+1{,}243$. These all subsequently reach $C$. For the second row the earlier [interval proof](LOWER_SCALE_GATES_758.md) allows an earlier halt as well as the known terminal. The two fractions quantify exactly what the choice of starting ensemble changes. Which reset the actual blank tape reaches, and whether $C$ eventually halts, remain open. [Published heuristic and original wall](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA#Large-scale_behavior)

## Proof of the common checkpoint

Use $J$ for an odd/odd jump, $L$ for an ordinary bulk move of either residue, $I$ for the initial move from an even reset, and $R$ for an even-left reset. On the even seeds from $H+1$ through $E-1$ the complete first return is $I J^{291}L^2 J L^2 J L R$. On the odd seeds from $H+2$ through $E$ it is $J^{292}L^8 J L^5 R$. At $E+2$ the odd word changes. The checker uses the original counter map to verify each endpoint. Increasing the starting seed within a parity class keeps the left counter nonincreasing and the right counter nondecreasing along each common prefix. Thus the two endpoint guards bound every intermediate guard. Checking the larger endpoint's intermediate left counters also excludes a prior reset. [Ordered endpoint proof](CONFLUENCE.md)

The maximal mass charge along the even word is 1,230 and along the odd word 1,294. Since the mass at a reset is $1+2s$, these bound the corresponding increases in $s$ by 615 and 647. All increases are positive. Hence every orbit starting in the corridor eventually reaches a reset above $E$, at most $E+647$. Advancing the smallest pending reset from $E+1,\ldots,E+647$ and merging equal resets leaves $C$ after exactly 14,216 distinct first-return edges, with no intervening halt. For the boundary layer below $H$, visit $H,H-1,\ldots,H-3{,}403{,}054$ in this order. The next reset is either above $H$ or has already been classified. The largest increase during this calculation is 1,409.

## A blank orbit that avoids both outcomes

A blank orbit that passes the upper mass cut alive without ever visiting $C$ must avoid every reset in the post-$H$ corridor until crossing. An exceptional call in the corridor, before its last 5,458 units of mass, gives a reset inside it in 787 calls by the [exceptional annulus identity](CUT_758.md). Thus the interior of such a passage consists entirely of ordinary jumps and bulks. With $T=(3\times10^{67})^2$ and $n=577$, the passage contains at least $T+n+2$ complete blocks and satisfies $3^n>9T(E+10)$. The [determinant word bound](FACTOR_COMPLEXITY_758.md) now forces at least **$3\times10^{67}$ different length-578 fine words** on this one passage. Equivalently, an infinite blank orbit either visits $C$ or has this much diversity when it passes the corridor. Visiting $C$ leaves its own eventual behavior to be determined.

Run the checker with Python 3.10 or later beside the other #758 verifiers. The default checks the corridor, its complete merger, and the finite escape inequality. The full count adds the near-$H$ boundary layer.

```sh
python3 after_target_758.py
python3 after_target_758.py --boundary
```

## Searching forward from the common checkpoint

Starting at $C$ itself, the next **500,000 first returns** use exactly **420,169,510 counter calls** and end at $E+1{,}256{,}970{,}693$. These are conditional counter calls from $C$. No blank visit to $C$ has been proved. The nearest larger direct terminal in the [existing survey](mixed_terminal_windows_758.tsv) is approximately 6.58% above $C$; all 5,001 earlier starts in that particular survey window bypass its pair. An independent search below covers $C\le s\le E+10^{60}$, with an explicit bound on the terminal branch word.

Even seeds throughout this search interval have the same short live return as before the edge. Every odd seed begins $J^{292}L^8JL^4J$. After this prefix put $y=(c+7)/2$. A bulk sends $y$ to $3\lceil y/2\rceil$. After $k$ consecutive bulks the resulting $y_k$ obeys $(3/2)^k y\le y_k<(3/2)^k(y+3)$. All tested odd starts with the same seed difference $z=s-E$ modulo 8,192 have $y(z+8{,}192)=y(z)+4{,}650{,}361$. To obtain the identity, shift the initial seed by 8,192 and propagate the coordinate differences through the twelve bulks and two jumps of the prefix. Each bulk loses one binary digit, leaving enough at every guard to preserve the low versus high bulk residue. The checker independently compares adjacent periods for every residue. The right counter is nondecreasing as $z$ increases.

Consider an ordinary first excursion that halts after this prefix. Before the final halting call, it must contain an unpaired last bulk. Represent its remaining ordinary moves as $L^{k}wL$ with $k$ even and $w$ either empty or starting with $J$; each other block of $w$ is a jump or a pair of bulks. We tested all such words with at most 18 elementary calls in $w$, allowing the initial $k$ to be arbitrarily large. In the search interval even 800 initial bulks would force the right counter beyond the available mass.

For the odd/odd state immediately before the final bulk, put $u=(a+2c-1)/2$ and $d=(c-1)/2$. The terminal condition gives $-17\le9d-2u\le-10$. Inverting $w$ yields a rational slope $\theta$ and $d-\theta u\in[-8,0]$ at the start of $w$. Indeed, with next slope $x$, the inverse $J$ sends the slope to $(x+1)/3$ and the deviation $g$ to $(g+2x-1)/3$. An inverse pair sends it to $4x/9$ and $(4g+4vx-b)/9$ for the [four paired-branch constants](EXCURSION_POWERS_758.md). All slopes are in $[0,1/2]$ and these substitutions preserve the deviation interval. At the start of $w$, $2/9\le\theta\le1/2$, since the word begins with $J$ or is empty. Thus $|y_k-\theta u|<20$. With $C\le u\le E+10^{60}+20{,}000$ this bounds the launch $y$ to at most ten integers for each viable $(k,w)$. Inverting its residue table gives concrete starting seeds. Across 6,765 words, all 4,362 distinct candidates have live first returns. This excludes the specified ordinary terminal class throughout the $10^{60}$-scale search interval; longer suffixes and other excursions remain open.

The [forward and inverse checker](continue_after_target_758.py) performs the inverse search by default. The optional trace batches fourteen consecutive legal bulks using the input residue of $y$ modulo $2^{14}$. These determine the additive correction to $y$ and the total mass gain. Since the left counter strictly decreases in a bulk run, a nonnegative final left counter suffices for all fourteen guards. Samples are also compared against individual unbatched calls from the original verifier.

```sh
python3 continue_after_target_758.py --trace
```
