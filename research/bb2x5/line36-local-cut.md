# A one-cell left cut for line 36

The blank machine `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---` already has a [Rocq nonhalting proof](../../verify/Line36Nonhalting.v). The following is an independently reproducible reduction of its left certificate. It uses two complete pieces of local history, one actual digit beyond the protected cut, and a 3,588-entry potential. Its finite calculation has been replayed in C++ and Python. The Rocq theorem uses the original certificate. [Original argument](line36-nonhalting.md) · [Build and kernel replay](line36-rocq.md)

## Cut and induction credit

Use exactly the six phase prefixes and piece alternatives in the [tile identities](line36-tiles.md). At the old cut coordinate $x$ the word to the left agrees with a phase reference. The cut may lie within a piece. Remember just the actual digit at $x$ and put $y=x+1$. Let $A$ count changes of parity along the last closing before $x$, all closings from $x$ onward, and the old terminal coordinate. Let $d$ be the debt of the suffix starting at $y$ and $d_0$ the debt of the suffix starting at $x$. Matching treats 1 as an opening and 2 as a closing. An exterior debt erases that many rightmost surviving openings. Always $d_0\le A+1$ by the parity-run bound in the original argument.

The number $h$ of header cells is 6, 1, 1, 6, 1, 1 in successive phases. The word grows by $h+\epsilon$, where $\epsilon$ is the old terminal survivor bit. The original 50-cell right certificate supplies a potential $-21\le H\le0$ and a cancellation $c$ such that $H\le3c-1+H'$ and $\epsilon'=1-\epsilon$. Use the [moving-cut calculation](line36-halo-ledger.md) with known old interval $[x,y)$ of length one. Its signed charge $C$ satisfies
$$
 A'\le A+C+1-\epsilon-c.
$$
Only the definition of $y$ and the actual known digits enter that calculation. New parity labels use $j-h+1$ and both lists start with their preceding closing. The existing lemma [halo_moving_cut](../../verify/Line36Halo.v) treats the two cut lengths as parameters.

We establish a left potential $-56\le V\le0$ and choose $x'\le x+h$ with
$$
 3(x'-x)-24C-4\ge V'-V.
$$
It follows by substitution that $J=3x-24A-V+8H+12\epsilon$ is nondecreasing. At literal epoch 331 the width is 1,035, $x=530$, $A=7$, the next piece is kind zero, the partial prefix is empty and the next digit is 1. The machine took 612,729 defined instructions to arrive here. The rough bound $J\ge1254$ already suffices. Thus $3x-24A\ge1254-56-12=1186$ and $x-8A\ge396$ at each established checkpoint.

Before assuming success of the next step, apply the density lemma $L-2b\le22$ to the tiled interval $[200,x)$, where $b$ is openings minus closings and $L$ is its length. Its balance is at least $(x-222)/2\ge87+4A$, strictly larger than $d_0$ and 11. A pristine reference extension has debt at most 11. Both real and reference matching leave a common intrinsic survivor in this interval, so the guard to its left has exactly the phase reference matching. The physical sweep therefore succeeds in finite positive time. There is room before $x$ for the preceding two complete pieces after the guard. There are initially 504 physical cells after the remembered digit. Since $x'\le x+h$, that exterior length never decreases and the 50-cell cap always fits.

## Incoming debts from zero through twelve

A potential state consists of the phase, the kind $k$ of the next piece, its literal proper prefix, and the digit at $x$. Identify identical prefixes of the two alternatives. Choose the two actual preceding complete pieces $a,b$, in kinds $k-2,k-1$ modulo six. Put $U=ab$ followed by the partial piece. Its balance over all choices is at least 20, verified in the finite calculation below. It therefore has at least 20 intrinsic survivors.

The real debt into $U$ is at most $d+1\le13$, and the reference debt is at most 11. Erasing either number preserves the leftmost intrinsic survivor in $U$. It also preserves the status of the first cell of $U$ and the outgoing debt at its left boundary. Thus the two masks agree before $U$ and on its first cell. Set the local coordinate origin at the old boundary before $a$. The first $h+1$ new digits there are precisely the first $h+1$ digits of the next-phase version of $a$. The last of these uses the first cell of $U$ and its old left neighbor. Each later known digit is computed directly from the two mask bits at $j-h-1$ and $j-h$, matching $U$ plus the remembered digit with incoming debt $d$. This gives all new digits through $y+h-1$. The argument applies to every earlier piece history.

Parse the longest next-phase prefix up to $x+h$ from that origin. Let $z=x'$ be its end. Take the next digit at $z$ as the new remembered digit. The enumerator checks the existence of a closing strictly before $z$ inside its local output on every case. The old preceding closing is also inside $U$. Hence both sentinel parities and all charges are obtained from the local data. Translating the origin changes every parity by the same amount and preserves all comparisons. At $d=0$ take the larger of the charges for the two possible first survivor bits in the unknown suffix. At $d>0$ that bit is zero.

There are 3,588 states, four choices of $(a,b)$ and 13 incoming debts, making 186,576 cases. For each ordered state pair retain the least weight $3(z-x)-24C-4$. There are 61,932 such pairs. Relaxing from zero stabilizes after 23 changing rounds, with minimum $-56$, maximum zero and seed value $-2$. The generator then checks the inequality again on every retained edge. An independent Python implementation uses the full phase prefix and a concrete earlier piece history for each case, computes the physical derivative, reparses from the global origin and checks every one of the 186,576 inequalities against the published potential. The common-survivor argument above explains why arbitrary earlier histories give the same local calculation.

## All incoming debts of thirteen or more

The remembered digit is erased if it is an opening and already has zero survivor bit if it is a closing. Thus $d_0=d\pm1\ge12$. In the protected prefix, use empty-exterior matching and let $i$ be its $d_0$-th surviving opener from the right. The bootstrap puts $i$ in $[200,x)$. It is the leftmost survivor changed by the real debt relative to the pristine extension, which erases at most 11. The interval $[i,x)$ has balance $d_0$, since the other cells there form internally matched pairs. Density gives $x-i\le 2d_0+22\le2d+24$.

Choose the new cut exactly at $i+h$. The digits before it agree with the next-phase reference, so it is a legal cut. From $i$ through the remembered cell all the real survivor bits are zero. At most one closing, at $i+h$, occurs in the known output from the new cut onward. In the moving-cut calculation the known new segment contributes at most one switch, the old known contribution is nonnegative, and the crossing digit at $y+h$ is an opening. The first unknown survival is zero. Its possible parity mismatch contributes at most one and its debt deduction is at least $d-1$. Hence $C\le3-d$. Since $h\ge1$ we have $x'-x\ge-2d-23$ and therefore
$$
 3(x'-x)-24C-4\ge18d-145\ge89>56.
$$
This covers every difference of two potential entries. Together the two debt cases preserve the credit and give successive true finite sweeps indefinitely, using the original certified right cap.

## Replay

Use Python 3.10 or later with assertions enabled and a C++17 compiler. Run from `research/bb2x5`.

```sh
c++ -std=c++17 -O2 line36_left_local.cpp -o line36-left-local
python3 line36_local_replay.py --rebuild ./line36-left-local
```

Without the optional argument the Python replay checks the supplied table directly. The table has 144 decimal integers ordered by phase, piece kind, alternative, and halo digit. Six-bit groups encode $-V$ in increasing order of proper-prefix length. Shared prefixes must decode to identical values. [Generator](line36_left_local.cpp) · [Replay](line36_local_replay.py) · [Potential](line36-left-potential.json) · [Observed output](line36-local-verification.txt)
