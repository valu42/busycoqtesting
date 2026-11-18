# A bound on parity changes entering from the right of line 36

For `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---`, the right end of the blank orbit contributes at most **$(t+3)/6$** net monomers over the first $t$ successful sweeps starting at epoch 32. Over any later interval of $t$ successful sweeps the bound is **$(t+45)/6$**. Monomers measure phase changes between runs of data on alternate tape cells. The bound includes the boundary’s additions and the cancellations forced within the final 50 cells. The [blank-tape nonhalting proof](line36-nonhalting.md) combines this estimate with a bound at the left cut.

Use the epoch convention of [the matching sweep](prior_sweeps.py). The word consists of openings 1 and closings 2, with A scanning the blank immediately before it. Epoch zero is empty. A prefix with six more closings than openings halts in that sweep.

## A count that also bounds tape imbalance

Tile a word $W$, from left to right, by dimers 11 or 12 and one-cell tiles called monomers. Let $M(W)$ be the minimum number of monomers, with $M(\varnothing)=0$. A complete dimer has nonnegative balance and so does its first cell. Consequently **no prefix of W has more than $M(W)$ excess closings**. This holds even when there are many long intervening dimer runs.

There is an exact formula. In a word of length $m>0$ indexed from zero, make a list starting at −1, followed by the positions of all 2s, then $m-1$. Keep a repeated last position if necessary. Count the odd spacings between consecutive positions. A dimer cannot pass across a 2 to its right, so every interval from just after one listed position through the next is tiled separately. Each such interval can be tiled with zero monomers if its length is even, or a single initial monomer if it is odd. This proves the formula. Equivalently, $M$ is the number of changes in the parity of the listed coordinates.

## The natural cut after one sweep

Let $W$ be any suffix of the old data. In matching, scan from right to left with initial debt zero. A 2 increments debt. A 1 pays one unit if possible and otherwise survives. Write $s_i$ for the survivor bits in ordinary left-to-right order on $W$. Put $D(a,b)=1+(a\mathbin{\mathrm{xor}}b)$. The new data at an interior location $i$ are $D(s_{i-1},s_i)$. At the right end an extra 2 is appended precisely if the final bit is 1. On the outward pass the machine has left 3 for a survivor and 2 elsewhere, and the return carry is one precisely after a 3. A wall reset fills data already passed when no earlier opener is unmatched, so it preserves this description there. Header and wall symbols precede the old data.

Write $Z$ for the exact suffix produced starting at old data position 1 in $W$. If $W$ has length $m$, this consists of the $m-1$ successive derivatives between old survivor bits, followed by the appended 2 when present. Set $\epsilon=[W\text{ ends in }1]$. An old ending 2 is accompanied by two nonsurvivors at the right edge, since its left-hand neighbor cannot be a surviving opener. An old ending 1 gives an appended 2. Thus $\epsilon$ alternates once the epoch is at least two cells wide.

Take a right cap, meaning the last $k$ digits, inside $W$. It must contain a 2. Let $U$ be its portion strictly after its leftmost 2. Calculate $d$, the debt exiting $U$ toward the left, and $f$, the number of odd-length runs of surviving ones in $U$. Define

$$
c=M(U)-d-f.
$$

The cap cancellations reduce the same $M$ that bounds tape deficits. The one-sweep bound is

$$
 M(Z)\le M(W)-c+(1-\epsilon).
$$

To prove it, in any input tiling a dimer 12 always produces survivor bits 00 and transmits the incoming debt unchanged. A dimer 11 emits 11, 10 or 00 according as the incoming debt is zero, one or at least two. A surviving opening monomer supplies one single 1. A dimer 11 leaving one survivor uses one outstanding unit from a closing monomer. A unit of debt can supply such a survivor only once. The number of odd one runs is at most the number of these single supplies, because 11 survivors occur in pairs inside one run. Together with the debt exiting the region, the odd-run count costs at most one unit per incoming debt or input monomer. On $U$, the unused amount is exactly $c$ in this accounting. In particular $c\ge0$. The anchor 2 separates optimal tilings, so if $W=P U$, then $M(W)=M(P)+M(U)$. Apply the count on $P$ with $d$ incoming units. Joining two boundary one-runs cannot increase the sum of odd-run counts. Therefore the total number of odd one-runs of $W$ plus its outgoing debt is at most $M(W)-c$.

Between surviving openers, zeros in the survivor sequence come in balanced substrings of even length. The trailing zeros after a survivor likewise form a balanced substring. Before the first survivor the number of zeros has the parity of the outgoing debt. If there are no survivors this last parity statement applies to the whole word. Thus the survivor sequence can be partitioned into equal-bit dimers and at most $M(W)-c$ single bits. Each odd one-run needs one, and an odd leading zero-run uses one unit of outgoing debt.

Temporarily include a trailing derivative to a virtual zero. Under the shifted cut, each equal-bit dimer $bb$ supplies the output dimer $1,D(b,\text{next})$, and a singleton supplies one digit. If the old last bit is 1, the trailing derivative is the actual appended 2. Otherwise its virtual 1 is omitted. Removing the final digit of a tiled word increases the minimum monomer count by at most one. This proves the inequality. More precisely, let $d_W$ be the outgoing debt of the entire suffix $W$. The zero-run parity uses only $d_W \bmod 2$ of its units. The stronger inequality is

$$
 M(Z)+2\lfloor d_W/2\rfloor \le M(W)-c+(1-\epsilon).
$$

Summed over sweeps, this also bounds the cumulative even parts of the closing debts sent into the protected prefix.

## Changing the left cut

For a cut that adjusts to the debt, keep the natural $Z$ for even $d_W$. For odd $d_W$, retain the omitted digit at old data cell zero, provided the previous cell is also old data. The first survivor in $W$ is preceded by an odd run of $z$ zeros and every verified cap contains a survivor. The old previous cell and cell zero both fail to survive since an unmatched closing from $W$ remains. Their derivative is 1. The first 2 of $Z$ is at position $z-1$, so prepending 1 reduces $M(Z)$ by one, by the anchor formula. Consequently the adaptive suffix $Z_*$ satisfies

$$
 M(Z_*)+d_W \le M(W)-c+(1-\epsilon).
$$

This adaptive cut advances by one old data cell on even debt and zero cells on odd debt. It charges the entire closing debt against the right-hand budget.

The natural cut advances by one **old data cell**. Its image may be shorter by one cell. If the application chooses a wider next suffix $XZ$, include its exact additional charge $M(XZ)-M(Z)$. Suppose the first 2 of $Z$ is at position $j$. The charge is the count of odd spacings in the list −1, the positions of all 2s in $X$, $|X|+j$, minus $(j+1)\bmod 2$. In particular prepending any number of ones costs at most one monomer. For a smaller next suffix the exact difference can again be used. Merely deleting a prefix costs at most one because at most one dimer crosses its cut. When the cut varies across $t$ sweeps, the bound in the first paragraph is added to the initial $M$ and the sum of these left-cut charges. Every chosen old suffix must contain the cap. The [switch calculation](line36-halo-ledger.md) bounds the resulting change at the cut used in the blank proof.

## An exact finite certificate for cancellations

In a $k$-bit cap number the bits from the right and let bit 1 mean digit 2. Compute the survivor word $S$ and the outgoing matching debt from this cap. If its last tape digit is 1, append shifts the cap image by one. The new integer is $((S\mathbin{\mathrm{xor}}(S\!\gg\!1))\!\ll\!1)\mathbin{\mathrm{or}}1$, truncated to $k$ bits. If its last digit is 2, use $S\mathbin{\mathrm{xor}}(S\!\gg\!1)$. The single bit just beyond the cap could then change only the leftmost output bit, and only when the outgoing debt is zero. Keep both possibilities in that case. These edges include every actual successful sweep, allowing arbitrary exterior behavior. All vertices reached from the actual epoch-32 cap contain a 2.

Let $V_t(v)$ be the minimum total cap cost over all $t$-edge paths from $v$. Start with all entries zero and iterate $V_{t+1}(v)=c(v)+\min_{v\to w}V_t(w)$. For $k=46$ the graph has 3,840,923 vertices. The verifier compares all their integer entries and finds $V_{457}=V_{353}+34$. The recurrence preserves uniform constant shifts, hence $V_{t+104}=V_t+34$ for every $t\ge353$. Through the finite initial range the loss is at least $(34t-670)/104$ from every reachable cap, and $(34t-32)/104$ from the epoch-32 seed. These bounds now hold for all $t$. Adding at most $(t+1)/2$ right-boundary monomers and subtracting these losses gives the corresponding width-46 bounds, $(9t+361)/52$ and $(9t+42)/52$.

At width 50 there are 16,939,461 vertices. Give a cap edge from $v$ to $w$ integer weight $3c(v)-1$. Its total along a path of length $t$ is three times the number of forced cancellations minus $t$. To construct a potential $H$, start every entry at zero and repeatedly replace each entry by
$$
\min\left(0,\;3c(v)-1+\min_{v\to w}H(w)\right).
$$
The 508th synchronous update leaves all entries unchanged. The checker then verifies on every edge that $H(v)\le3c(v)-1+H(w)$. Its maximum is zero, its minimum is $-21$, and the epoch-32 seed has value zero. Along every path the edge inequalities telescope to give $3\sum c-t\ge H(v_{\rm start})-H(v_{\rm end})\ge -21$. Paths starting at the seed have $3\sum c\ge t$. At most $\lceil t/2\rceil$ boundary units are added because the final digit alternates. Subtract the forced cancellations to obtain the width-50 bounds in the opening paragraph.

From the directory containing the machine list, run

```sh
c++ -O2 -std=c++17 line36_right_cap.cpp -o /tmp/line36_right_cap
/tmp/line36_right_cap 50
```

The checker also compares cap images and the one-sweep inequality with an independent matching stack and tiling algorithm on every binary word of lengths 2 through 11. It obtains the seed by direct tape execution through 32 epochs and reads the exact machine from line 36 of the dataset. For a quicker independent calculation, width 30 uses 10,437 vertices and certifies at least $t/4$ cancellations from the seed. The default width 36 uses 95,863 vertices and yields an asymptotic net right-boundary contribution of at most $15/76$ per sweep.
