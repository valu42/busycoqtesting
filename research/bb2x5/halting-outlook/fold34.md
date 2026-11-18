# Line 34 · transport of debt across two sweeps

For `1RB2LA4RA1LA3LA_0LA2RB3RB2LB---`, a large old debt leaves a long run of **openings** on the following tape. Debt can cross that same stretch again only if the new debt is even larger at its far end. A complementary exact test detects a dangerous cut one sweep earlier, from the spacing of the starts of runs of surviving openings. The two identities below hold for every successful sweep subject to the stated boundary conditions. Neither establishes that the blank machine runs forever.

## Conventions and inherited results

Let a cut $a$ mean the position immediately before cell $a$, indexing from zero at the first data cell. The guard is outside the word. Symbols $O,N,C$ are $1,2,3$. Let $d(a)$ be the largest excess of closings over openings in any prefix of the suffix beginning at $a$. Let $s_i$ be one if the opening at cell $i$ survives greedy matching and zero otherwise. A successful sweep inserts a header of length $h=1$ or $5$, so the new index of the same physical cell $i$ is $h+i$. Write $d'$ for the successor's cut debts. The data digit written there is $D(s_{i-1},s_i)$, equal to $O$ for equal bits, $C$ for a rise, and $N$ for a fall. Use the header's outgoing carry as $s_{-1}$. Any appended digit is neutral. From epoch ten, a real sweep reaches B4 exactly when $d(12)\ge6+b(P)$, where $P$ comprises its first twelve digits and $b(P)$ is openings minus closings. [Machine sweeps](../prior_sweeps.py) · [Guard theorem](line34_left.md) · [Timed physical audit](target34.md)

## A monotone folded coordinate

Suppose an interval of the old word is ordinary output from the previous epoch. Let $p_j$ be the previous epoch's survivor bit which generated the *left* side of the old digit at cut $j$. Thus $p_{j+1}-p_j$ is $+1$ at $C$, $-1$ at $N$, and zero at $O$. Define $X(j)=j+p_j-d(j)$. For every cell in the interval,

$$X(j+1)-X(j)=3[\text{cell }j=C]+s_j.$$

Indeed, the change of $d$ from left to right is $[O]-[C]-s_j$, directly by matching. Substitution gives the displayed identity. In folded coordinates, a closing advances three units, a surviving opening advances one, and the other cells advance zero. If $u_r$ runs through surviving openings in this region in physical order, $d(u_r)=0$ and $u_r+p_{u_r}-r$ is constant modulo three. Only two residues of $u_r-r$ occur there. This conclusion is about the rank of actual survivors.

In a complete zero-run between two groups of surviving openings there are $q$ old closings and exactly $q$ old matched openings. A match cannot cross a surviving opening. Let $z$ be the run length and $p_{\rm L},p_{\rm R}$ its boundary bits. Then

$$z=3q+p_{\rm L}-p_{\rm R}.$$

In particular, a one-cell zero-run surrounded by survivors is an old neutral. It has $(p_{\rm L},p_{\rm R})=(1,0)$.

## A positive debt erases its interval in the next sweep

Suppose $0<a<|W|$ and $d(a)=k>0$. Let $b$ be the position of the first surviving opening at or to the right of $a$, or use $b=|W|$ when there is none. Then $d(b)=0$. All bits $s_a,\ldots,s_{b-1}$ vanish. Also $s_{a-1}=0$ because any opening immediately to the left of the cut would have been canceled. Consequently **all** successor cells in $[h+a,h+b)$ are $O$, and

$$d'(h+a)=\max(0,d'(h+b)-(b-a)).$$

If $b$ is the right end then $d'(h+a)=0$. The old interval has deficit exactly $k$, by summing the reflected matching update from $a$ to $b$. For an interval inside ordinary derivative output its length is at least $2k-1$ because closings and neutrals alternate. After two ordinary generations and for $k\ge2$, the counting argument in the guard report improves this to $5k-7$. Thus if $k=6$ and the new debt is positive at the same material cut, at least 23 more units of new debt must be present farther right. In particular a positive global maximum of successor debt in the ordinary region cannot occur at the material image of a cut that previously had positive debt. A fixed left-origin cut changes material cell at each epoch. To apply this law to successor cut 12, the old cut is $12-h$.

## Every fixed material cut has debt-free epochs

The erasure identity gives an all-time restriction on **consecutive** positive debts. Follow a fixed physical cut that already lies strictly inside the data. Its indices satisfy $a_{t+1}=a_t+h_t$. Let $L_t$ be the number of consecutive openings immediately after it, before processing the old word. If $d_t(a_t)=k>0$, all those openings are canceled, and the debt immediately after them is $L_t+k$. Apply the erasure law from that second cut. All the old $L_t$ openings also turn into openings because neither their bits nor their left neighbor survive. Thus the next word has

$$L_{t+1}\ge L_t+B(L_t+k).$$

Here $B(u)=u$ always suffices. A word of deficit $u$ needs at least $u$ cells. Use $B(u)=2u-1$ in ordinary output, or $B(u)=\max(2u-1,5u-7)$ when the interval is clear of both ancestral headers. This last condition automatically holds once the material cut has been in the data for two more sweeps. Any appended terminal neutral can be trimmed from a positive-deficit witness.

In particular $L_{t+1}\ge 2L_t+1$ throughout any positive streak, even without the folded estimate. If $R$ material cells initially lie to its right, at most $R+n$ cells can lie to its right after $n$ more sweeps. The far edge appends at most once per sweep. A streak of $n$ positive input epochs requires $2^n-1\le R+n$. **Therefore no fixed material cut can carry positive debt forever on an infinite run.** Every such cut returns to zero infinitely often, and the gap between debt-free epochs is logarithmically bounded in the tape length to its right at the start of the gap.

The two-generation bound sharpens this substantially. Starting with $L=0$ and using only $k\ge1$, the successive lower bounds for $L$ are $1,4,22,130,778,4666,27994,167962$. For $n\ge2$ this is $(18\cdot6^{n-2}+2)/5$. The moving head and left guard make cut 12 a *different physical cut on each epoch*. The fixed-material theorem allows an isolated fatal pulse there. It is also conditional on the existence of the successive sweeps; a final failing input has no normalized successor.

Across the first 50,000 blank sweeps the longest observed streak at any material cut tracked inside the ordinary region (normalized index at least eleven, starting at epoch 13) was two. At blank epoch 14,117 the unique cut with debt six was 12,645. It produced 38 consecutive openings. The next debts at the near and far ends were zero and one. The statistic of two is not a general restriction. On an explicit padded 135-cell nonblank interior, the same physical cut has debts $1,1,1,1,0$ and opening lengths $0,1,4,22,130$ at successive boundaries. On another 42-cell interior, three successive positive debts begin only after four preparatory sweeps. The checker gives both tapes and verifies every configuration and raw count against literal execution, to steps 5,432 and 2,391 respectively. Neither tape is a blank checkpoint.

## An exact test one epoch before B4

Let $a=12-h$, with the old word long enough to contain this cut. List the old positions $b_1<b_2<\dots$ at or to the right of $a$ where the survivor bit rises, including a rise at $a$ itself. These are the starts of the runs of surviving openings. The successor cut debt is exactly

$$d'(12)=\max\bigl(0,\max_{i\ge1}\{3i+s_{a-1}-2-(b_i-a)\}\bigr).$$

The empty list gives zero. A nonempty prefix realizing positive maximum excess can end at a closing, since removing trailing openings or neutrals never reduces excess. At the $i$th such closing the interval contains $i$ rises and $i+s_{a-1}-1$ falls, by telescoping the bits. Its length is $b_i-a+1$. Subtracting its opening count from its closing count gives the formula, including cases where the first old cell is within an existing run. The header and any appended neutral never add a closing after the old right edge.

Equivalently, put $P_i=d'(h+b_i)-1$. Between successive starts the new word is $C O^{x-1} N O^{z-1}$, where $x$ is the length of the old survivor run and $z$ the length of the following zero-run. Reflection at zero gives

$$P_i=\max(0,P_{i+1}+3-(b_{i+1}-b_i)).$$

For the final start, $P_i=0$. A **positive** increment is exactly $+1$ and requires $x=z=1$. Away from the header this is a singleton survivor run, then one old neutral, then another surviving opening. A spacing of three contributes zero. Larger spacings pay down debt. In folded coordinates the increment is $3(1-q)-x+p_{\rm R}-p_{\rm L}$, so the phase terms telescope over consecutive complete groups when the old derivative bit is constant along each surviving run. It is constant there because all cells of that run are old openings.

This also gives a precise all-time proof target. Whenever the successor has reached epoch ten and has twelve cells, let $P'$ denote the successor's first twelve cells. A future B4 on the *immediately succeeding sweep* is equivalent to some old run start satisfying

$$b_i-a\le 3i+s_{a-1}-2-(6+b(P')).$$

An all-time lower bound on these spacings relative to rank, with the physical seed and changing balance included, would settle line 34. The bound has not been proved.

## Measured margins and an altered control

The script records the integer slack between the halting threshold and every candidate score. A margin of zero suffices to reach B4. Candidate ranks within a single sweep are strongly correlated partial sums. Their counts do not supply halting probabilities. In 50,000 blank sweeps, the smallest margin was four, at the second run start of input epoch 50. For ranks 17–32, 33–64, and 65 onward the minima were 25, 61 and 127. In the later segment starting at epoch 12,000 these three minima were 32, 65 and 127. The last band had minimum 137 in the first 12,000 sweeps and dropped to 127 at epoch 14,792. There was just one positive-to-positive transfer into cut 12 after the input word reached width 16, from input epoch 36 with old and new debts both one. These are observations on specified finite segments. [Executable checks](fold34.py) · [Verification output](fold34-verification.txt)

The inherited 493-copy altered orbit gives a long-range test of the criterion. At input epoch 853, predicting epoch 854, the first 64 run-start scores have maximum 1 on both the genuine and altered tapes. The threshold is 12 in both. On the blank tape the overall peak stays at 1. On the altered tape the score first reaches 12 at rank **4,065**, material position **12,192**. Its following sweep reaches B4. Thus a finite band of early starts misses a real halt in this explicit continuation. The splice was introduced at epoch 839 on the altered tape. It has no demonstrated realization on the blank orbit. [Physical witness and literal checkpoint checks](line34_right.md)

To reproduce, run from the repository root with Python 3.10 or later, NumPy and assertions enabled.

```sh
python3 research/bb2x5/halting-outlook/fold34.py --epochs 50000
```

The checker exercises all 9,841 words through width eight. For every successful first sweep it checks the formula at all material cuts and compares the entire tape, absolute head, state and raw clock to the literal interpreter. It also checks the folded-coordinate increment, protected opening stretch, interval recurrence, applicable second-generation gap identity, and the altered control. The longer run uses the existing timed sweep; the new run-start calculation is a diagnostic cross-check. No formal proof assistant has verified these results.

A next proof search could group the old intervals by their exact closing count $q$, survivor-run length $x$ and incoming phase, then bound positive cumulative increments paid for by later spacings. Such an argument must explain why a blank orbit cannot sustain the increments for thousands of ranks as the altered orbit does, and must retain both the exceptional header and the final neutral.
