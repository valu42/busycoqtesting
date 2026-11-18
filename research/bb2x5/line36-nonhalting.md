# Line 36 runs forever on blank tape

**Theorem.** Start `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---` in state A on an all-zero, two-way-infinite tape. Its execution never reaches the undefined instruction B4. This is the machine on line 36 of the [November 3 list](BB2x5_Rocq_holdouts_37.txt).

The proof starts with 612,729 literal instructions and then uses induction. Two finite integer calculations establish inequalities on opposite sides of a moving cut. The inequalities have exactly the rates needed to keep the cut away from the left guard for every future sweep. A Rocq formalization remains outstanding.

## Sweeps, tiles and the cut

At a checkpoint, A scans the blank just left of a finite word of openings (1) and closings (2). The initial word is empty. Match each closing with the nearest still available opening on its left. Write a 1-bit for each surviving opening, and a 0-bit everywhere else. The **debt** of a word is the greatest excess of closings over openings in any prefix, including the empty prefix. It is also the number of unmatched closings sent out of the word toward its left. Six unmatched closings in the entire word reach B4. At smaller debt a finite, positive number of instructions produces the next checkpoint.

In old material coordinates, an ordinary output cell is 2 if its survivor bit differs from the preceding bit, and 1 otherwise. A header of length $h$ precedes these data. A surviving final opener appends one extra closing, indicated by $\epsilon=1$. Thus the width grows by $h+\epsilon$. The [literal derivation](line36-physical.md) includes the third-closing reset and the finite return over the data.

In each of six phases there is a 26-cell prefix followed by six successive pairs of alternative pieces, repeated in order. Selecting one piece from each pair makes a tile. The [tile identities](line36-tiles.md) show that infinite concatenations evolve to the next phase with the same choices and piece lengths. This supplies a reference word for any finite legal prefix. The six whole-word debts in the reference are $3,2,0,3,2,0$, giving the header lengths $6,1,1,6,1,1$. These infinite words are only references for local matching. Every sweep performed by the actual machine is over a finite word.

Number cells from zero at the left of each checkpoint. Choose a cut $x$ after a prefix agreeing with the phase reference, possibly partway through a piece. Remember the next three **actual** digits, which can be arbitrary. Let $A$ be the number of parity changes in this list of coordinates:

1. the last closing strictly before $x$,
2. every closing from $x$ to the right end, in order,
3. the last physical data coordinate, repeated if it was a closing.

Two equal consecutive parities contribute zero. Between positions separated into runs of closings of a single parity, an interval in each run contains at most one more closing than opening. In particular, the debt $d_0$ sent into the protected prefix by the suffix at $x$ is at most $A+1$. This upper bound holds before making any assumption about the next guard or sweep.

At **epoch 331**, direct execution gives head $-871$ after **612,729** defined instructions. The word has 1,035 cells. Cut $x=530$ is at the end of the third complete tile, in phase zero. The three following digits are 111. The preceding closing is at 529, the last closing is at 1031, and the terminal coordinate is 1034. The initial budget is $A=7$.

## The two inequalities

Let $C$ be a signed charge assigned to a step of the left cut. Let $c$ denote cancellations forced within the final 50 cells of the old tape. The [switch-count derivation](line36-halo-ledger.md) gives the same budget on both sides:
$$
 A'\le A+C+(1-\epsilon)-c.
$$
It applies as long as the last 50 cells lie strictly beyond the three remembered digits. It accounts for a matching interval that spans both the cut and the cap. The closing at the far boundary of the three remembered cells is counted exactly once.

The [right-cap certificate](line36-right-cap.md) proves that for every interval of $t$ successful sweeps after the cap at epoch 32,
$$
 \sum((1-\epsilon)-c)\le (t+45)/6.
$$
The cap has 16,939,461 reachable states. Every actual cap transition is an edge. An integer potential in $[-21,0]$ verifies $3\sum c-t\ge-21$ on every path. The terminal bit alternates, so at most $\lceil t/2\rceil$ boundary units enter. This gives the displayed bound. Epoch 331 is reached by literal execution through epoch 32.

The **left certificate** assigns an integer $V$ in $[-110,0]$ to each cut state. Its inequality is
$$
 6(x'-x)-24C-4\ \ge\ V(\mathrm{next})-V(\mathrm{current}).
$$
Here $x'\le x+h$. Consequently the amount of tape beyond the three remembered digits never decreases. The initial 502 such cells suffice for the 50-cell certificate.

### Finite debts

The state records the phase, index of the next piece, choice of the preceding complete piece, matched prefix of the next piece, and three actual digits. All 28,704 such states are included, including ones that might never occur on blank.

Put $y=x+3$ and let $d$ be the debt of the suffix beginning at $y$. Given $d$, right-to-left matching determines the survivor mask on the known data up to $y$. Equivalently, match with zero incoming debt and then erase its $d$ rightmost surviving openings. This determines the header and the $y$ ordinary output digits through position $y+h-1$, forming a word $S$. Parse the longest next-phase prefix up through position $x+h-1$, stopping at the first digit incompatible with both choices. The position after this prefix is $x'$. Take the three digits $S[x':x'+3]$ as the new remembered data. If a partial piece matches both alternatives, its literal prefix is retained, so both continuations remain possible.

Only a finite amount of old choice history is required when $0\le d\le28$. The checker enumerates four choices immediately before the stored last complete piece. To justify any earlier padding, take the last four complete pieces, followed by the old partial piece and the three remembered digits. The checked balance of this segment is at least 46 for every choice, even if all three digits are closings. Thus the real incoming debt of at most 28 leaves a surviving opening in the common region. A pristine reference extension also sends at most 11 units toward the cut by the interval bound below. More explicitly, in the four complete pieces and the partial piece, there are at least 49 intrinsic survivors. At most 31 are removed by the real halo and exterior, and at most 11 by the reference exterior. Both matchings retain a common survivor. Everything to its left follows the pristine identity for its own earlier choices. Everything from its right neighbor onward depends only on the shared local input. The fifth common piece covers the preceding digit for the derivative at the join. Piece lengths are unchanged across phases, so the true and padded local outputs agree up to translation. The checker verifies that the reparse retains at least one shared complete piece before the new cut. Every piece contains a closing, so the displacement, destination state and charge are independent of the older history. A common translation preserves every comparison of parities.

For each such transition the charge is the upper bound derived in [the switch calculation](line36-halo-ledger.md). When $d=0$ it takes the larger of the two possible first-survivor cases. Over all histories and $d=0,\ldots,28$ there are 1,752,900 distinct edges. Integer relaxation from zero finds $V$ after 17 changing passes. Every edge satisfies the displayed inequality. [Checker](line36_left.cpp) · [Tile and checkpoint inputs](line36_left.py)

### Arbitrarily large debts

For every interval in every phase of the tiled region, let $L$ be its length and $b$ its balance (openings minus closings). Then
$$
 L-2b\le22.
$$
Every six successive complete pieces have $L-2b\le-4$. In checking the maximum for an arbitrary interval, one can delete six complete interior pieces while keeping both endpoint pieces and their phases. The remaining interval lies in at most seven consecutive pieces, including the case of an interval entirely inside one piece. The checker evaluates the maximum, 22, over these finite choices. In particular any reference suffix has debt at most 11.

Suppose $d\ge29$. All three remembered digits fail to survive. The debt $d_0$ at the cut lies between $d-3$ and $d+3$, so it exceeds the reference suffix debt. Counting backward in the protected prefix with empty exterior, let $i$ be the position of its $d_0$-th surviving opening. The bootstrap below guarantees its existence within the tiled region. Relative to the reference, $i$ is the leftmost survivor changed by the incoming debt. The interval $[i,x)$ has balance $d_0$, since the first of those surviving openings starts it and the remaining matched pairs are contained within it. Consequently $x-i\le 2d_0+22\le2d+28$.

All data strictly before $i+h$ still agree with the reference output, so $x'\ge i+h$ and $x'-x\ge-2d-27$. From $i$ through the three remembered digits all old survivor bits are zero. There is at most one closing in the newly exposed known output, at $i+h$. The charged case has positive $d$. In the notation of the switch calculation, $K'\le1$, the crossing digit is open, $[g\ne\beta]\le1$, $K\ge0$, and $\ell\ge d-1$. Thus $C\le3-d$. The left edge weight is at least
$$
 6(-2d-27)-24(3-d)-4=12d-238\ge110.
$$
This covers the entire range of $V$, whatever the destination state. No debt cutoff is imposed on the machine.

## Induction on the actual computation

After $t$ successful updates from the epoch-331 seed, summing the three inequalities gives
$$
 x_t-4A_t\ \ge\ 530-4\cdot7-110/6-4(45/6)=453\tfrac23.
$$
The terms proportional to $t$ cancel. To apply this estimate inductively, one must also show that the *next* sweep succeeds before using an inequality about its output.

At the start of the next sweep, $d_0\le A_t+1$. The protected tiled interval $[200,x_t)$ has balance at least $(x_t-200-22)/2$, which exceeds $A_t+1$ and 11 by the displayed margin. Thus it contains more than enough intrinsic surviving openings to absorb either the actual incoming debt or the reference debt. Both matchings leave a common surviving opening in that interval. Everything to its left, including the guard, has precisely the reference matching and the same total debt. The current sweep therefore uses its phase's safe header and completes in finite positive time. This argument also puts the large-debt anchor $i$ inside the tiled region. The last five complete pieces occupy at most 143 cells and a partial piece at most 29, so this cut also has the full finite-debt history. The true word width grows by $h+\epsilon$ and $x'\le x+h$, preserving the cap hypothesis for the next sweep.

The two certificates now apply to this additional true step, giving the same lower bound at time $t+1$. The seed establishes time zero. Induction supplies infinitely many successive finite checkpoints. Hence the blank machine never reaches B4.

## Reproduction

From the repository root, using Python 3.10 or later with assertions enabled and a C++17 compiler:

```sh
cd research/bb2x5
c++ -O2 -std=c++17 line36_right_cap.cpp -o /tmp/line36_right_cap
c++ -O2 -std=c++17 line36_left.cpp -o /tmp/line36_left
/tmp/line36_right_cap 50
python3 line36_left.py /tmp/line36_left
python3 line36_halo_ledger.py
python3 line36_physical.py
```

The two certificates rebuild the integer inequalities from the machine and tile descriptions. The last two checks compare the switch charge with concrete matching words and full sweeps, and the sweep formula with literal machine execution.
