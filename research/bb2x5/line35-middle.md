# How much debt the interior of line 35 can send to the guard

**Line 35 remains open.** For `1RB2LA4RA1LA3LA_0LA3RB3LB2RB---`, after five successful sweeps over the same interval of ordinary data, every subinterval of length $L$ has at most $\lfloor(L+25)/8\rfloor$ more closings than openings. This gives a sufficient test for the blank run using just the **left quarter of each tape word and its total width**. The test succeeds at every checked epoch from 524 through 150,000. Proving its two inequalities for all later epochs would establish nonhalting. [Certificate checker](line35_middle.py) · [Timed blank run and altered-tape control](line35-timed.md)

## Applying the bound to blank

Use zero-based, half-open intervals in the physical left-to-right word at a sweep boundary. An opening $O$ is tape symbol 1, a closing $C$ is 2, and a neutral $N$ is 3. Write $b(P)=\#O-\#C$ and $d(P)=\max_{Q\text{ prefix of }P}(-b(Q))$, including the empty prefix. In particular $d(PV)=\max(d(P),d(V)-b(P))$.

Let $n$ be the width, $x=\lceil n/4\rceil$, $P=W[8,x)$, and $R=n-5-x$. For $20\le x\le n-5$, the two sufficient inequalities are

$$
 d(P)\le4,\qquad b(P)+4\ \ge\ 1+\left\lfloor\frac{R+25}{8}\right\rfloor .
$$

Each successful sweep prepends at most four header digits and appends one closing. The intervening positions are ordinary data images. Consequently every position in $W[20,n-5)$ has five ordinary ancestors at epochs at least five. A whole material interval follows the ordinary rule with the same offset at each sweep. This applies the length bound to every prefix of $W[x,n-5)$. The five rightmost cells have debt at most one. At odd epochs from five they are $OaOOC$ with $a\in\{O,C,N\}$. At the intermediate epoch their possible physical words are `11312`, `12312`, and `32312`. These follow from the first covered triple and its two-cell cap in the [right-boundary argument](line35-pascal.md).

Thus the suffix after $x$ has debt at most $1+\lfloor(R+25)/8\rfloor$. Applying the concatenation identity to $P$ proves $d(W[8,n))\le4$. The existing 71-prefix guard graph covers every such exterior debt. The initial epochs through 523 can be replayed directly. The true cut-8 debt is at most four on this initial segment, as checked by the sweep calculation. If the two inequalities persist at all subsequent boundaries, induction with the guard graph supplies infinitely many successful finite sweeps. [Guard graph](line35-pascal.md#what-a-halt-would-require-in-the-middle-of-the-tape)

In the finite replay the last failure of the sufficient quarter test is epoch 523. From epoch 524 through 150,000 the minimum margin in the second inequality is 19, at epoch 573. The maximum tested $d(P)$ is two. At epoch 150,000, $n=305057$, $x=76265$, $b(P)=41488$, and $d(P)=0$. The second inequality holds there by 12,890 openings. The epoch is reached after 73,421,002,000 defined instructions from the blank tape.

## A restriction visible in two sweeps

The ordinary output of a cell with survivor bit $s_i$ is $D(s_{i-1},s_i)$, where equal bits give $O$, a rise gives $C$, and a fall gives $N$. Successive non-openings therefore alternate. Suppose the current row is itself an ordinary image of older bits $a_i$, and $i<j$ are consecutive surviving openings in the current row. Every closing strictly between them has its partner between them, and every intervening opening is matched. If $c$ is the number of these closings, the gap has $c$ openings. Its closings minus neutrals telescope to $a_{j-1}-a_i=a_j-a_i$, since the digit at $j$ is an opening. Therefore

$$
 j-i-1=3c+a_i-a_j.
$$

A nonempty gap becomes $N O^{j-i-2} C$ in the next row. Across a contiguous run of current survivors the older bit $a$ is constant. In the new row, list the distances from each $N$ to the next $C$, skipping intervening openings. Discard the distances divisible by three. The remaining residues must alternate between one and two as the older bit changes value. This holds for complete gaps whose endpoints have ordinary ancestry. In particular `321132` cannot occur there. It contains two successive $N$-to-$C$ distances of one.

The [888-sweep altered tape](line35-timed.md#an-altered-tape-shadows-almost-ten-guard-periods) contains `321132` in its planted block. This distinguishes its starting interior from genuine data of this age. After two further successful sweeps its ordinary descendants also obey the law, and it still eventually halts. The distinction at its starting epoch alone cannot close the guard argument.

A factor with excess $d\ge2$ needs at least $5d-7$ cells under this two-sweep restriction. Trim to a minimal offending interval starting and ending on $C$. If it contains $m$ closings, the $m-1$ intervening neutrals each begin a gap to the next closing. No two consecutive such gaps both have length one. At least $\lfloor(m-1)/2\rfloor$ of them contain an opening. Thus $d\le m-\lfloor(m-1)/2\rfloor$, giving $m\ge2d-2$ and length $3m-1-d\ge5d-7$. At genuine epoch 1406, the 18 cells $[571,589)$ are `232312323123231232`. They attain the shortest possible length for excess five, far from cut 8.

## A certificate for five sweeps

The checker uses a finite automaton to enclose three successive ordinary images, then excludes three further factors by direct backward matching. All states may end a finite word. The first model accepts every word on $O,C,N$.

For a current graph, let $A,C,N$ be its three labelled edge relations ($A$ here is the opening relation). Let $M_l$ connect endpoints of a balanced word of length $l$. A balanced word has equal numbers of openings and closings and no prefix with excess closings. It can begin with a neutral, or with an opening matched to a closing after a balanced interior. With relation composition in reading order, this gives

$$
 M_0=I,\qquad
 M_l=N M_{l-1}\ \cup\!\!\bigcup_{i+j=l-2} A M_i C M_j .
$$

For the three graph constructions the verifier uses candidate pairs $(B,p)=(1,1),(1,3),(13,3)$. It calculates the recurrence through $2B+3p+2$ and checks $M_l=M_{l-p}$ on the proposed tail. This finite check proves periodicity. Substitute the periodic candidate in the right side. At $l\ge2B+2p+2$ every split has an index at least $B+p$ that can be reduced by $p$. Conversely, every split for $l-p$ has an index at least $B$ that can be increased by $p$. Thus the right side also repeats. Induction in $l$ proves all remaining equalities.

Between successive surviving openings there is exactly a balanced word of nonsurvivors. At an old-graph state just past a survivor, the possible transitions to the next survivor after $l$ zeros are therefore enclosed by $M_l A$. The new graph records the previous state and the length class of $l$. Extending the zero run emits $N$ on its first zero and $O$ thereafter. Taking a new survivor emits $O$ at length zero and $C$ at positive length. The graph also allows an arbitrary initial partial gap with either preceding survivor bit, and permits the interval to end in a partial gap. These choices include both edges of any genuine finite interval regardless of exterior debt. Subset construction and partition refinement give graphs of 3, 12 and 49 states after one, two and three sweeps.

To exclude an additional factor, decode both possible starting bits for its $D$ representation and work backwards over the prescribed survivor bits. At a survivor the old digit must be $O$ and both adjacent debts are zero. At a nonsurvivor with debt $e$ on its left, the right debt is $e+1$ for a matched opening, $e$ for a neutral, or $e-1$ for a closing when $e>0$. If a parent itself needs an ordinary parent its non-openings must alternate. The exterior right debt can be capped at the interval length without changing the survivor bits. If the bit immediately left is one, its right debt is zero. If there is an internal survivor, the left-edge debt is at most the distance to the first survivor. Otherwise twice the interval length suffices after capping the right debt. This finite search allows independently chosen exteriors on older rows and hence includes all concrete histories.

| Forbidden physical factor | Number of ordinary images tested |
|---|---:|
| `231232312323123231232312` | 5 |
| `231232312323121323123231232312` | 5 |
| `3213123231232312` | 4 |

Deleting paths containing these factors from the three-sweep enclosure yields 177 states after minimization. Give $O,C,N$ edge costs $9,-7,1$ respectively. A path spelling a word of length $L$ has cost $L+8b$. The checker constructs an integer potential $v$ with initial value zero, minimum $-25$, and $v(j)\le v(i)+\mathrm{cost}(i,j)$ on every edge. Summation over an arbitrary path gives $L+8b\ge-25$, proving the claimed bound for all lengths. The certificate is a finite integer calculation in Python with a mathematical soundness argument.

From this directory run the default certificate, or add the blank comparison.

```sh
python3 line35_middle.py
python3 line35_middle.py --epochs 150000
```
