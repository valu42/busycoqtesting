# Line 26 · what a finite automaton can certify

The exact machine is `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA`, line 26 of the November 3 list. The blank decision remains open. The argument below rules out a regular inductive invariant on the natural checkpoint tapes. It also excludes every possible first halting width through 151 and certifies more than 2.75 × 10²¹ defined instructions from blank.

The community tracker credits mxdys with the competing-overflows interpretation. The [tape derivation](research-log.md#line-26--one-inequality-decides-a-finite-halt) proves the elementary trips and their positive durations. The [first-danger criterion](column-frontier.md) proves the equivalence with the least fixed point used below. The present work adds the scalar representation, the two-tail argument, the limitation on regular invariants, and a time-stamped calculation. [Formal list](BB2x5_Rocq_holdouts_37.txt) · [Public status](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved)

## Coordinates and the scalar word

At an epoch A reads blank at coordinate $-n$. To its right are $n$ digits `4`, then $m$ pairs on `1,4`, then `3` and blanks. The two digits in pair $i$ encode $(1-u_i,e_i)$, with digit `1` for a set bit and `4` for a clear bit. Pack $u,e$ least significant pair first. Five instructions from blank give $n=1,m=0$. Two trips per epoch send $a,a,d,d$ over each two successive epochs. A fresh pair reached by a safe carry adds one pair. A dangerous $d$ reaching a fresh pair halts at B3. The all-ordinary model supplies virtual pairs $(u_i,e_i)=(0,0)$ above the real width. A safe operation passing all virtual pairs is a *wrap*, counted once. Until the first dangerous encounter with a fresh pair the models agree.

Put $P=b$ and $Q=d$. Two consecutive $P$ operations equal one $a$, including the number of wraps. The two $P$ operations toggle the lowest $u$ twice. An $a$ leaves that bit unchanged. Exactly one of the two $P$ passes that digit. It produces the same child operation as $a$, and $e$ stays fixed. Thus a gap containing $A$ letters $a$ and $B$ letters $b$ is exactly $P^{2A+B}$.

A cut $j$ is just after the first $j$ ordinary pairs. Their true initial states are $(0,0)$. At cut 3 the periodic ordinary word is `aaabbbd`, hence $(P^9Q)^\omega$. One **tick** is four original `aadd` cycles, or eight physical epochs. Their last trip supplies the tick's $Q$. At tick boundaries the lowest three ordinary pairs have returned to $(0,0)$.

In one ordinary pair entered by $P^gQ$, start with values $u,e$. Emit $(2-e)\lfloor(g+1-u)/2\rfloor$ copies of $P$. Replace $u$ by $u\mathbin{\mathrm{xor}}(g\bmod 2)$. Pass $Q$ exactly if $u=1$ or $e=1$, then replace $e$ by $e\mathbin{\mathrm{xor}}(1-u)$. The $P$ rule alone is the same computation before the $Q$. This gives all four initial states, including zero-length gaps. Let $W_j$ denote the infinite scalar word seen at cut $j\ge3$ in this ordinary process.

**Every phase occurs.** At the beginnings of ticks, the $k$ pairs immediately above cut 3 run through all $4^k$ possible states in a single cycle. In a traversal they send $9\cdot3^k$ copies of $P$ and $3^k$ copies of $Q$ to cut $3+k$. The case $k=0$ is the tick itself. Suppose the result holds at $k$. Both counts are odd. For any initial next pair, one traversal flips $u$. Over two traversals every occurrence of $Q$ sees both values of $u$, so $e$ flips an odd number of times while $u$ returns. Four traversals therefore visit all four next-pair states above each fixed lower state and return to the start. At any given token position the same argument applies to the cyclically shifted word, or by transporting the four states through its prefix, since each token acts as a permutation on the pair. Across its four visits a $P$ produces $2+1+0+0=3$ copies, and a $Q$ passes three times. This proves both assertions. In particular every finite low state has a continuation that occurs in the actual *ordinary* stream. Physical survival up to that phase is a separate question.

## A family of nonblank configurations that must halt

Temporarily start the packed process above cut 3 at $u=e=-1$. The bits of negative integers are eventually all ones. The following operations specify the limit of their finite low-bit projections. A $P$ decrements $u$ on the selected positions of $2e+1$. The least selected set bit stops it. Such a bit always exists because both masks are eventually one. Its highest changed digit goes from one to zero, so $u$ strictly decreases and stays negative. A $Q$ increments $e$ on positions of $\mathord{\sim}u$, a finite set. If it finds a selected zero it stops there and strictly increases $e$. If all selected positions were ones, it clears them and passes through every higher column. In both cases $e$ stays negative. Only finitely many bits change on each operation. These statements include an empty $Q$ selector.

On $(P^9Q)^\omega$ there are infinitely many such through-passes of $Q$. Otherwise after the last one the negative integer $e$ would strictly increase at every tick forever. Fix $r\ge1$ and stop after its $r$-th through-pass. Choose $k$ at least the greatest one-based stop depth of the finitely many $P$ operations in this interval. For every larger $k$ the same argument works. Start the lowest $k$ pairs all at $(1,1)$ and give them arbitrary upper pairs. The low-bit evolution agrees with the signed calculation, because each pair acts only on the stream going right. No $P$ reaches cut $3+k$ during the interval. At least $r$ consecutive $Q$ do. In the signed calculation all bits of $u$ above these $k$ positions stay one, so in fact every $Q$ crossing the cut in this interval is one of the through-passes. Transitivity puts this factor in $W_{3+k}$ for every sufficiently large $k$.

Suppose the physical tape above these $k$ pairs has $b$ further pairs, with arbitrary contents. During this interval no extension can occur. The upper $u$ stays fixed. Let $z$ count zeros of this upper $u$, and let $v$ be the binary integer formed by the corresponding digits of upper $e$, least significant first. The $(2^z-v)$-th arriving $Q$ reaches the fresh pair and halts. This follows by ordinary binary increment on just the $z$ eligible positions; when $z=0$ the very first $Q$ halts. In particular $r=2^b$ always suffices. The three fixed low pairs, followed by $k$ all-one pairs and **any** $b$ additional pairs, therefore give a genuine halting epoch, for suitably large $k$ depending on $b$. The input phase can be realized with $n=1$, or any $n=1\pmod 8$.

Here are small witnesses. A raw run with $n=1$ and $b$ ordinary zero pairs as its suffix initially reads `4` then `(14)^3 (41)^k (14)^b 3` to the right of the head. The literal interpreter uses the two rows of the original machine.

| $b$ | sufficient $k$ | tick by which all suffix assignments halt | defined raw steps for the all-zero suffix |
|---:|---:|---:|---:|
| 0 | 4 | 1 | |
| 1 | 8 | 6 | 8,680 |
| 2 | 15 | 58 | 665,166 |
| 3 | 32 | 6,793 | |

The starts in this table are nonblank. They also show that adding any fixed number of pristine upper pairs to an arbitrary initial occupied word cannot guarantee safety up to the next extension.

### No regular inductive safety invariant on these tapes

Consider a deterministic finite automaton reading the $m$ physical pairs in order from low to high at the aligned epoch checkpoints. A sufficient invariant would contain the genuine blank checkpoints and accept only configurations that can continue forever. Closure under each next tick together with safe, finite tick execution implies this latter condition by induction. Equivalently one can start the checkpoint sequence after the first safe tick, when the bottom three ordinary pairs exist.

Suppose such an automaton with $N$ states exists. Its claimed invariant implies the real machine runs forever. Take $r=2^N$ in the signed-tail construction and choose $k$ as there. By transitivity, at some genuine checkpoint the high $k$ pairs immediately above the fixed three all equal $(1,1)$. The time may be chosen greater than the first tick by periodicity. The real tape necessarily contains all these pairs because their $e$ digits are set. The automaton accepts that checkpoint. From its state after those $3+k$ input pairs there must be a path to acceptance. A shortest such continuation uses fewer than $N$ pairs, since a repeated state can be deleted. Those $b<N$ pairs form a well-defined alternative physical suffix. The same automaton accepts this tape, yet $2^b\le r$ incoming dangerous carries force it to halt before any extension. This is a contradiction.

The same proof works if the input includes the literal leading `4` run, the A head and the final `3`. Keep the entire real prefix, including its $n$, and take a shortest path in the graph with whole physical pairs as letters to a state accepting the prescribed end marker. This result applies to this tape encoding and these checkpoints. A certificate may retain an unbounded counter, computation history, or another mathematical representation. The argument settles neither alternative for the blank input.

## The complete tick is an 18-state finite transducer

This gives a direct forward or backward model on *all* finite upper tapes. Represent each physical pair above cut 3 by the digit $2u+e$, with the lowest pair first. After the first tick from the blank tape the bottom three pairs are ordinary zeros, $(u,e,m)=(8,16,5)$ in full coordinates, and the upper word is `21`. All subsequent aligned ticks have the same rule.

Start a scan with carry $(g,q)=(9,1)$. It denotes $P^g$ followed by a $Q$ if $q=1$. At each old digit perform the scalar pair rule at the start of this note, omitting the dangerous operation if $q=0$. Emit the updated data digit, and carry the surviving $P$ count and $Q$ flag to the next digit. The count never exceeds 10, since $(2-e)\lfloor(g+1-u)/2\rfloor\le 2\lceil g/2\rceil$. Closing the initial carry under all four digits gives exactly 18 reachable states.

At the old right end let $a=\lceil g/2\rceil$. Here $P^g$ allocates $a$ pairs and leaves $u=g\bmod2$, $e=0$ in the formerly pristine high counters. If $q=1$, the dangerous carry stops at displacement $g\bmod2$. It halts precisely if $a\le g\bmod2$, namely at terminal carries $(0,1)$ and $(1,1)$. Otherwise append $a$ zeros, set the $u$ bit of the first appended pair if $g$ is odd, and set the $e$ bit at displacement $g\bmod2$ if $q=1$. The physical pair rules justify the concrete steps before the right end. This final check includes every possible intermediate halt, since the tick contains only one dangerous arrival at cut 3. The driver compares all 341 upper words of lengths zero through four with eight literal physical epochs, and checks the true initial word and every endpoint through tick 4,096 against the root arithmetic.

For a backward computation, let $S_t$ contain every finite upper word that survives $t$ ticks. $S_0$ is the universal language. Given a deterministic automaton for $S_t$, run it on each newly emitted data digit and at the end on the appended suffix, rejecting either halting terminal carry. The resulting product automaton recognizes $S_{t+1}$. Partition refinement gives its minimal complete automaton. The first five positive horizons have 10, 34, 75, 135 and 229 states. Horizon 21 has 10,306. The checker compares the automaton against forward iteration for every short test input at each horizon.

There is no uniform state bound for these exact backward computations, regardless of the outcome on blank. For any $b$ let $t$ be the tick of the $2^b$-th signed through-pass and choose $k$ as in the negative-tail construction above. On inputs $3^k0^j$ precisely $2^b$ dangerous carries and no safe carry reach the upper $j$ pairs through tick $t$. Consequently $3^k0^j$ belongs to $S_t$ exactly when $j>b$. The $b+2$ prefixes with $0\le j\le b+1$ must leave distinct automaton states. For $j_1<j_2$, appending $b-j_1$ zeros makes the first fail and the second survive. In particular the pristine-suffix examples at $j=b$ halt at exactly tick $t$, producing finite halting times with no common upper bound on these nonblank tapes. [Transducer and backward checker](column_tick.py) · [Checks through horizon 21](tick-verification.txt)

## A one-tick safety test using digit counts

For a finite upper word write $S=\#0-\#1-\#3$, with the same digits $2u+e$ as in the transducer. **If $S\ge0$, the word survives the entire next tick.** To prove this, follow just those partial scans on which the dangerous carry is still present. The maximum possible score at each safe-token count $g$ is as follows.

| $g$ | 9 | 10 | 5 | 6 | 3 | 4 | 2 | 1 | 0 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| maximum $S$ | 0 | 1 | 0 | 1 | 0 | 1 | 0 | −1 | −2 |
| attaining prefix | empty | 0 | 01 | 010 | 0101 | 01010 | 010101 | 01013 | 010133 |

Start at $(9,1)$ with score zero. On each of the 36 possible single digits from these nine states, either the dangerous carry stops or the current row value plus the digit's score is at most the next row value. The listed witnesses attain equality at every state. The two halting terminal carries have negative bounds. The example `01013` halts at score −1.

There is an obstruction to promoting this to a globally nondecreasing additive score. Let $N(w)$ be the four digit counts of $w$. Three complete safe ticks are `111 → 3331`, `211 → 1110`, and `0312 → 23310`. Their changes in $N$ are $a=(0,-2,0,3)$, $b=(1,1,-1,0)$, and $c=(0,0,0,1)$. The true seed is `21`, whereas `0133` halts within one tick. Their count difference is $v=(-1,0,1,-2)$. Direct addition gives $a+2b+c+2v=0$. A linear digit score nondecreasing on all safe transitions has nonnegative dot product with $a,b,c$. It cannot also have positive dot product with $v$. This obstruction concerns the global one-tick inequalities and the stated seed. A phase-sensitive reserve, a later seed, or a bound over several ticks is a different problem. All four witness tapes are also checked by literal execution. [Checker](column_tick.py) · [Output](tick-verification.txt)

## The first dangerous arrival and a bound on its plateaux

Write $g$ for the number of $P$ before the first $Q$ in $W_j$. Then $p(j)=\lceil g/2\rceil$ is the number of extensions before that arrival. The least fixed point of $p$, if one exists, is the first halting width. In the word following the leading $P^g$, let $r$ count $Q$ up to the next $P$ and $s$ count $Q$ between that $P$ and the following $P$. Thus $r\ge1$, $s\ge0$.

* If $g$ is even, $p(j+h)=p(j)$ exactly when $2^h\le r$.
* If $g$ is odd, $p(j+h)=p(j)$ exactly when $2^h\le2r+s$.

Indeed the high pair counters just after $P^g$ are $u=g\bmod2,e=0$. With even $g$ the very next $P$ wraps. Until then $Q$ increments $e$ from zero one at a time. With odd $g$, each of the first $r$ dangerous operations skips the lowest bit and adds two. The next $P$ stops at the low one and clears it, and the next $s$ dangerous operations each add one. The second $P$ wraps. In both cases the highest column reached before this additional wrap is the index of the highest bit of the indicated final value of $e$. The first setting of that bit reached it on a $Q$. Every such $Q$ passes all lower columns. Monotonicity of total wraps then gives the two equivalences, including equality at powers of two.

Let $R_j$ be the maximum length of a run of $Q$ anywhere in the cyclic word $W_j$. Then $R_3=1$ and $R_{j+1}\le R_j+\lceil R_j/2\rceil$. Between the first and last $Q$ of a run at the upper cut, the lower input can contain at most one $P$. Two $P$ would toggle $u$ twice, causing at least one to emit. A single suppressed $P$ changes $u$ from one to zero. All preceding $Q$ pass and at most half the following ones, rounded up, pass. There are at most $R_j$ on each side. With no intervening $P$ the bound is immediate. Thus $2^h>3R_j$ ensures $p(j+h)>p(j)$, independent of the phase of the tail. For an arbitrary tick-aligned starting state with $k$ possibly active pairs above cut 3 and all higher pairs initially zero, $b$ pristine upper pairs with $2^b>R_{3+k}$ suffice until the next extension. Before the first arriving $P$ the high $e$ counts consecutive $Q$ from zero and the high $u$ stays zero. The transitivity argument covers every choice of the initial low $k$ pairs.

## A time-stamped bound from the actual blank tape

In the scalar recurrence attach to each $Q$ the tick that issued it. To construct the next period, make four copies of the preceding one, add the corresponding period lengths to their time stamps, and keep each surviving $Q$ at its original time. Between surviving $Q$, accumulate the number of emitted $P$. Above a chosen cut process these gaps by sparse binary subtraction. For $u=2H+l$, a gap $P^g$ toggles $l$ by $g\bmod2$ and subtracts $n=\lfloor(g+1-l)/2\rfloor$ from $H$ on the digits selected by $e$. Each wrap of this selected counter adds one extension. If $e$ has $s$ set bits, deposit the low $s$ digits of $n$ into the positions of $e$, giving $z$. Ordinary unsigned subtraction from $H\mathbin{\&}e$, followed by masking with $e$, implements the sparse borrow: every unselected digit starts at zero and transmits a borrow across it. Add $\lfloor n/2^s\rfloor+[(H\mathbin{\&}e)<z]$ wraps. The formula includes $s=0$. A $Q$ then stops at the first position where $u=e=0$ bitwise. Before the first arrival at the target, $e$ has at most target minus cut bits and $u$ at most one more. Both cut computations below fit in 64 bits.

| cuts $j$ | $p(j)$ | tick of their first $Q$ |
|---|---:|---:|
| 71, 72 | 142 | 1,268,654,660 |
| 73, 74 | 143 | 1,343,882,677 |
| 75, 76 | 144 | 1,380,832,725 |
| 77 | 147 | 2,465,019,328 |
| 78 | 151 | 4,636,999,907 |

The checker computes all overlapping first-arrival counts and times independently from cuts 16 and 17. The earlier fixed-point chain reaches $p(71)=142$. The exact finite scalar period at cut 15 has $R_{15}=4$. Iterating the run bound gives $R_{78}\le524409302061$ and $3R_{78}<2^{41}$. Hence $p(119)>p(78)=151$, implying **$p(142)\ge152$** by monotonicity. This excludes every possible fixed point through 151. The exact value of $p(142)$ is unknown here.

Before the first $Q$ at cut 78 there are 151 wraps. An earlier physical halt would therefore have had width at most 151, which has just been excluded. Before the final tick at least $N=8(4636999907-1)=37,095,999,248$ epochs have completed. In epoch $n$ both trips travel from the guard at $-n$ to at least coordinate zero and return to the guard. The leading `44` pairs pass, and a final unmatched leading `4` also reaches coordinate zero. Thus the two trips require at least $4n$ elementary instructions in total. Including the five-step entry gives **at least $5+2N(N+1)=2,752,226,320,489,425,129,509$ defined instructions from blank**. The exact number of steps to this event remains unknown.

The obstruction now is to show $p(j)>j$ for every later $j$ or to exhibit a fixed point. The long runs at other phases prevent a uniform constant bound on $R_j$. The first-arrival phase at each $j$, and the number of unused eligible upper digits at that phase, are more specific data than the worst case over all phases.

## Reproduction

Run from `research/bb2x5` with assertions enabled. Python 3.10 or newer and a C++20 compiler suffice. The optional `-march=native` selects hardware bit deposit where available. The portable implementation gives the same output. [Python checks](column_phases.py) · [Calendar checker](column_clock.cpp) · [Transcript](phase-verification.txt)

```sh
python3 column_phases.py
c++ -std=c++20 -O2 column_clock.cpp -o column-clock
./column-clock
```
