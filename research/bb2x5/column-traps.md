# Line 26 admits halting tapes with an arbitrarily large digit-count margin

The machine is `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA`. All tapes here use the aligned checkpoints above the three ordinary low pairs. Each upper digit is $2u_i+e_i$ in low-to-high order. Eight physical epochs constitute one tick. The initial state A scans blank just left of the tape. The three low pairs and upper word are followed by the physical end marker 3. The leading run of 4s may have any length congruent to 1 modulo 8. The [physical encoding and tick rules](column-phases.md) specify these checkpoints completely.

## An obstruction to using digit multiplicities

The first three aligned nonempty upper words from the true blank are `21`, `1100`, and `332100`. The word `010233` has exactly the same multiplicities as `332100`, with two 0s, one 1, one 2 and two 3s. It reaches the undefined instruction B3 on its next tick. The scalar carry starting at $(9,1)$ retains its dangerous flag throughout its six digits and ends at $(1,1)$. Both words can be given the same physical guard length, width and epoch number. Thus an inductive safety certificate covering the third blank checkpoint cannot depend on these data and the four digit counts alone. This includes nonlinear functions of all four counts. The two digit orders are explicitly replayed from the transition table.

## A family that halts at an exact ordinary first arrival

Take $k$ initial zero digits in the upper word. Let $g$ be the number of safe tokens $P$ sent through those digits before the first dangerous token $Q$ emerges. This is the leading gap of $W_{3+k}$ from the [ordinary blank model](column-frontier.md), including all the $P$ that precede the $Q$ in its own tick. It arrives in at most $2^k$ ticks. Each column suppresses at most one of any two successive incoming $Q$, as proved below. Set $b=\lceil\log_2(g+1)\rceil$. The finite upper word
$$
 0^k3^b
$$
**halts on that very first $Q$**. In the last $b$ columns the high $u,e$ initially both equal $2^b-1$. Before the designated $Q$, only $P$ reaches them. All positions of their $u$ counter are selected by the all-one $e$, so its value decreases from $2^b-1$ by exactly one per arrival. Since $g\le2^b-1$, all $g$ arrivals stop within these columns, with no extension. The first $Q$ then finds $e_i=1$ everywhere in the high suffix and passes every one of its columns. The next pair is fresh and its physical B3 instruction is undefined. All earlier operations finish in finite positive time by the pair rules. This also handles $g=0$, with an empty high suffix.

For example take $k=75$. The independent calendars give $p(78)=151=\lceil g/2\rceil$ and first arrival at tick 4,636,999,907. Both possible $g$ need exactly nine high columns. The upper word $0^{75}3^9$ therefore halts at precisely that tick with digit-count score $S=\#0-\#1-\#3=66$. Its initial tape differs from the true blank. [Calendar and physical-time convention](column-phases.md#a-time-stamped-bound-from-the-actual-blank-tape)

More generally, insert an arbitrary collection of 1 and 3 digits in place of the high block and append any number of 2 digits. If the number encoded by the high $u$ bits within the 1-and-3 block is at least $g$, the same argument applies. These digits all have $e=1$. Each appended 2 has $u=1$ and passes the arriving $Q$. For fixed high multiplicities, putting all 3s at the most significant end maximizes the available countdown.

This also gives a later obstruction using the actual blank run. At tick 4,096 the four digit multiplicities are $(43,7,3,6)$, with score 30. Arrange them as $0^{43}1^7 3^6 2^3$. The first $Q$ above its 43 low zeros comes at tick 305,189, preceded by exactly 172 safe tokens. The 13-digit middle block has $e$ all ones and initial $u=63\cdot128=8064$. It stops all 172 safe tokens. The three final 2s pass the first $Q$ and the tape halts. Thus starting an invariant at the 4,096th blank tick still precludes using only width, time and digit multiplicities. The checker computes both the actual multiplicities and the complete arrival calculation from the root operations.

## Why the score is unbounded

Let $G_j$ be the largest number of consecutive $P$ between two surviving $Q$ in the full periodic stream $W_j$. There are no two consecutive suppressed input $Q$ at one column. Suppression requires $u=e=0$ after the safe tokens, flips $e$ to one, and the next $Q$ passes. If no $Q$ is suppressed within an upper gap, a lower gap of length $a$ emits at most $a+1$ safe tokens. If one is suppressed, consider the two lower gaps $a,b$ bordering that suppression. In the first, $e=0$ and $u$ ends at zero. The lower $P$ count is even from starting $u=0$ or odd from starting $u=1$. These cases emit $a$ and $a-1$, respectively. The second gap begins at $u=0,e=1$ and emits $\lceil b/2\rceil$. Thus
$$
 G_3=9,\qquad G_{j+1}\le G_j+\lceil G_j/2\rceil,\qquad
 G_{3+k}+1\le10(3/2)^k .
$$
The leading gap is covered by the same bound since the preceding periodic representative ends with a surviving $Q$. The score of the halting tape constructed above consequently satisfies
$$
 S=k-b\ \ge\ (1-\log_2(3/2))k-1-\log_2 10.
$$
It tends to positive infinity. A nonnegative score guarantees a single safe tick, yet no fixed threshold on that score alone guarantees indefinite continuation. The exact output time in the construction is its first $Q$, unlike the family based on arbitrarily long runs of $Q$ at other phases.

## A binary description with two generators

Interleave the bits as $u_0,1-e_0,u_1,1-e_1,\ldots$ and place a virtual zero immediately to the left. For $P$ select even positions whose preceding bit is zero. For $Q$ select odd positions whose preceding bit is zero. Either operation performs a binary decrement on the selected subsequence in low-to-high order. The first selected one is cleared and every earlier selected zero is set. If there is no selected one, every selected bit is set and the carry passes through. This is the original sparse subtraction for $P$. Complementing the selected $e$ bits turns the original addition for $Q$ into exactly that decrement.

Write $X$ for the operation on the current parity with an eligible first digit, and $Y$ for the opposite parity. On a word with first bit $v$ and remaining tail $w$ their complete actions are
$$
 X(0w)=1Y(w),\qquad X(1w)=0w,\qquad
 Y(0w)=0X(w),\qquad Y(1w)=1X^2(w).
$$
Indeed $X^2(vw)=vY(w)$ for either $v$. If the first bit is one under $Y$, the following position cannot be selected. It must skip that position unchanged, exactly as $X^2$ does. One tick acts by nine $X$ operations followed by one $Y$. The ordinary blank upper ray is $(01)^\omega$. The paired-counter formulas identify $Φ(u,e)=(2\,\mathord{\sim}e,\mathord{\sim}u)$ with insertion of one leading zero in this binary word. It converts $P$ into $Q$ at the same stopping depth and $Q$ into two $P$ operations. The first of those stops one column farther away, or passes right through, and the second stops at the new bottom cell. Applying $\Phi$ twice gives $(2u,2e+1)$. Here $\mathord{\sim}z=-1-z$ is bitwise complement with sign extension.

The binary form retains bit order and gives short recursions for composing arbitrarily many ticks. A use of these recursions in a blank decision would still have to control physical right-end allocation and the first dangerous arrival there. [Counter and literal checks](column_phases.py) · [Observed output](phase-verification.txt)

The [exact carry accounting](column-reserve.md) gives the sharp all-one suffix threshold for any prescribed low word, an order-sensitive first-arrival test, and the change of a dyadic sum under each type of token.

Four count-preserving replacements give a stronger obstruction for every function of all ordered-pair counts. The same certificate also derives the unique physical predecessor of any checkpoint that has one. [Ordered subsequences and the inverse map](column-order.md)
