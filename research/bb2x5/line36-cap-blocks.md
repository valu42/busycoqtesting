# A smaller right-hand certificate for line 36

The machine `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---` runs forever from blank by the computer-assisted argument committed by valu42 in `077b13b`. The construction below replaces its 50-cell, 16,939,461-state right-hand calculation with **62,671 states and 200,597 edges**. The initial tape, physical sweep, six-phase tile identities, and left certificate come from that proof. This is a refinement of the existing nonhalting argument. The Rocq proof remains outstanding. [Original proof](line36-nonhalting.md) · [Original commit](https://github.com/valu42/busycoqtesting/commit/077b13b031a44944f6689a6058511ec435dc1dee)

## The exact loss forced by a known suffix

For a finite word $W$ of openings `1` and closings `2`, let $M(W)$ be the minimum number of monomers in a tiling by arbitrary monomers and dimers `11`, `12`. Match from the right with initial debt zero. Let $d(W)$ be the outgoing debt and $f(W)$ the number of odd-length runs of surviving openings. Define $L(W)=M(W)-f(W)-d(W)$. The three-cell ledger uses an inequality of the form $f(W)+d(W)\le M(W)-c$. Thus $c=L(W)$ can be used on each actual sweep even if only a lower bound on it is computable. Here $W$ is the actual uncontrolled suffix with the possible single formal opening prepended, as in the original ledger. [Ledger derivation](line36-halo-ledger.md)

If an optimal tiling of $W$ splits at the beginning of $S$, then $L(W)\ge L(S)$. To see this, prepend the tiles before $S$ in reverse order. An opening or closing monomer increases $f+d$ by at most one. A `12` dimer emits two nonsurvivors and transmits the incoming debt. A `11` dimer at zero debt contributes two adjacent survivors, preserving the parity of the initial survivor run. At debt one it pays one unit and supplies at most one new odd run. At larger debt it consumes two units. Each complete dimer therefore makes $f+d$ nonincreasing. The tiling restricted to $S$ is optimal, since a better restriction would improve the entire tiling. These facts establish the inequality and, starting from the empty suffix, $L(W)\ge0$.

**For every nonempty cap $C$, the least possible value of $L(XC)$ over all left contexts $X$ is**

$$\min\{L(C),L(1C)\}.$$

Take any optimal tiling of $XC$. Either it splits at $C$, or the last digit of $X$ begins a dimer straddling the cut. In the latter case that digit must be `1` and the tiling splits at $1C$. The preceding lemma gives the lower bound in both cases. The contexts empty and `1` attain the two candidate values. If the digit immediately before $C$ is known to be `2`, no dimer straddles that cut, so the stronger bound $L(C)$ is available. The context `12` attains it.

## Recovering one digit from an observed transition

Number cap bits from the right, starting at zero. A set bit encodes a closing. Compute the survivor mask $S$ by right-to-left matching and set $I=S\mathbin{\mathrm{xor}}(S\!\gg\!1)$. If the last digit is an opener, the appended closing gives successor $2I+1$ truncated to the cap width. If the last digit closes and the outgoing cap debt is positive, the successor is $I$. Each case has the unconditional cost $\min(L(C),L(1C))$.

In the remaining case the last digit closes and the debt is zero. The cap has two possible successors. Flipping the top bit of $I$ means the old preceding cell survived. Leaving $I$ unchanged means it failed to survive. At zero cap debt that preceding cell must then have been a closing. Charge the unchanged branch $L(C)$ and the flipped branch $\min(L(C),L(1C))$. The real uncontrolled suffix contains the cap and its preceding digit throughout the induction. For the derivative and append formulas, see the [physical sweep](line36-physical.md).

The checker computes $M$ by listing a left sentinel, every closing coordinate, and the rightmost coordinate, repeating the latter if it closes. Count the odd gaps between consecutive listed coordinates. A dimer cannot cross a cut immediately following a closing. Between two consecutive listed coordinates a tiling needs exactly the parity of the gap as its monomer count. This also works when there are no closings. The independent Python check computes the minimum with a tiling recurrence instead.

## Blocks of eight successful sweeps

At epoch $32+8j$ retain the last 41 digits. Start from the exact 41-bit seed 605,926,600,073, read from the 92-cell word at epoch 32 by literal execution. At the start of each block allow either possible digit just to the left of those 41. Propagate the resulting 42-cell caps through eight sweeps, branching on each allowed successor. Add the eight costs derived above and then forget the leftmost bit. Keep the smallest total for each possible destination. This constructs an edge of cost $c_e$. Whenever the eight real sweeps succeed, they follow an enumerated path and the sum of their actual $L(W)$ values is at least $c_e$. Keeping the cheaper of two paths to the same intermediate 42-cell cap can only lower the bound for each later path. Both initial choices are admitted again at the next block. Every intermediate cap is checked to contain a closing and a surviving opening. This property applies to a partial block as soon as its past sweeps have succeeded.

From the seed the closure has 62,671 visible states and 200,597 distinct directed edges. An integer potential $H$ satisfies

$$-16\le H(v)\le0,\qquad H(v)\le3c_e-8+H(w)$$

on each edge $v\to w$. The checker obtains it from zero by 32 changing synchronous relaxations, then checks the inequality on every edge. The seed value is $-2$.

Consider any interval of $t$ successful sweeps starting at or after epoch 32. Remove its two end fragments, each of length at most seven, to leave whole aligned blocks. If the interval lies inside one block, take it all as a fragment. Telescoping gives $3\sum c-t\ge-16$ on the complete part, with $c=L(W)$ on each actual sweep. Since $c\ge0$, including the fragments gives $3\sum c-t\ge-30$. The terminal bit $\epsilon$ alternates on each successful sweep, so

$$\sum((1-\epsilon)-c)\le (t+1)/2-(t-30)/3=(t+63)/6.$$

For an interval where the chosen suffix $W$ changes each sweep, the same calculation applies provided it contains the 42-cell cap and its preceding digit at each step. The original blank induction starts with 502 cells outside the left halo and preserves this lower bound.

## Substitution in the blank-tape proof

Use the original left charge $C$ and potential $V$ in $[-110,0]$. The two local inequalities are $A'\le A+C+(1-\epsilon)-c$ and $6(x'-x)-24C-4\ge V'-V$. At epoch 331 the verified seed is $x=530,A=7$. Applying the block bound gives at every successful checkpoint

$$x_t-4A_t\ge530-28-110/6-4(63/6)=441\tfrac23.$$

This suffices for the original induction. The tiled interval $[200,x_t)$ has balance at least $(x_t-222)/2$, strictly greater than both $A_t+1$ and 11. It absorbs the actual incoming debt and the reference debt before the guard. The next sweep has the safe reference header and finishes in positive finite time. The cut retains enough complete pieces for the left certificate, and $x'\le x+h$ keeps at least 502 cells outside the next halo. This proves the same blank-tape conclusion with the smaller right certificate. [Left finite cases, large debts and the blank bootstrap](line36-nonhalting.md#induction-on-the-actual-computation)

## The left potential needs fewer states

The previous complete piece's choice affects the enumeration of local histories. Its value can be forgotten when indexing the potential. Project each of the 28,704 original states to its phase, next piece index, literal partial piece, and three remembered bits. Enumerate *every* original edge as before. For each ordered pair of projections keep the least weight $6\Delta x-24C-4$. The resulting 14,352 states and 657,878 weighted pairs admit a potential in $[-110,0]$ after 17 changing relaxations. The checker pulls the potential back through the projection and checks each of the 1,752,900 original finite edges. The original analytic bound for debts above 28 covers the same potential range. This removes one piece choice from the potential lookup while retaining all of its physical effects.

There is also a sharp restriction on improving the rate via this left graph. Twelve enumerated edges form a closed walk with total displacement zero and total charge $-2$. Any bound $\Delta x-\lambda C\ge\lambda r+V'-V$ on all its edges with $\lambda>0$ gives $2\lambda\ge12\lambda r$ by summation. Hence $r\le1/6$ for any such potential. The projected check also verifies the twelve edges individually. The walk is a constraint on this finite abstraction. Its occurrence on the blank tape is unnecessary for the conclusion.

## Reproduction

Run from `research/bb2x5` with Python 3.10 or later, C++17, and assertions enabled. The Python driver uses the literal machine at epoch 32 and checks the cap minimum with an independent matching and tiling computation on 32,130 cap/context pairs. The C++ program constructs the entire block graph and verifies the potential. The second command pair checks the projected left graph and closed walk. These are ordinary integer checks. The files do not assert a Rocq theorem. [Driver](line36_cap_blocks.py) · [Checker](line36_cap_blocks.cpp) · [Output](line36-cap-blocks-verification.txt)

```sh
c++ -std=c++17 -O2 line36_cap_blocks.cpp -o line36-cap-blocks
python3 line36_cap_blocks.py ./line36-cap-blocks
c++ -std=c++17 -O2 line36_left.cpp -o line36-left
python3 line36_left.py ./line36-left --projected
```
