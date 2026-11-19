# An integer reachability query for the blank-tape halting target

An **unsatisfiable** result on the ordinary crossing query below would prove that #758 and #153 halt from blank. The query has 12 midpoint levels by default and checks for 4,096 ordinary calls on each side of one exact mass crossing. A satisfiable result describes a possible crossing from an arbitrary counter state. A second query starts on the actual blank orbit and tests for a halt up to the known terminal mass. The full-size queries remain unresolved. [Generator](cut_reachability_758.py)

## Why ruling out one local crossing would decide blank

Let $B=H-64,916,341,784,245,418,891$ and $U=H-3,403,055$. Every reset with seed in $[B,U]$ halts. Put $M=2\lfloor(B+U+1)/2\rfloor+1$. This is the threshold computed by the generator. An infinite blank run crosses it with mass $W=a+2c$ between $M$ and $M+8$, since a live counter call gains between four and nine in mass. [Halting basin](HALTING_COLLAR_758.md) · [Mass bounds](MASS_CLOCK_758.md)

Let $k=2^j$. For any $j$ from zero through 62 the states within $k$ calls on either side of this crossing stay in the basin's mass band, with room for the exceptional branch. Indeed $M-9k\ge2B+1$ and $M+8+9k\le2U+1-5458$. The initial blank mass lies more than $9k$ below the threshold, so the past segment exists. At these masses a regular reset would enter the basin. An exceptional call forces a reset within 787 calls and a mass gain of 5,458. A reset with even right counter is also already covered. An escaping run would therefore use only odd/odd jumps and strong bulk moves, with neither endpoint of a move at a reset. A move ending at $a=0$ also forces a reset on the next call because its right counter is odd. The query enforces these conditions on both sides of the cut and permits every integral crossing state in the mass window. [Exceptional return identity](CUT_758.md)

The central window admits an explicit integer witness with **392 ordinary calls before and 392 after**. Start the strong bulk recurrence at $c=1$, accumulate the mass gain $g$ of 392 bulks, and choose $a=M-g-2$. These first 392 bulks land exactly at mass $M$. Replaying all 784 calls verifies every guard, with no reset. Thus no symmetric test of length at most 392 per side can prove the claim by excluding all arbitrary crossing states. The witness's ancestry from blank is unknown.

## Checking a long path with one transition definition

For two states $x,y$ let $R_0(x,y)$ check one legal update. For each further level use

$$R_{j+1}(x,y)\iff \exists z\ \forall b\in\{0,1\}: R_j(\operatorname{ite}(b,z,x),\operatorname{ite}(b,y,z)).$$

The same midpoint $z$ must witness both halves. Induction gives exactly $2^j$ updates, with one reference to the preceding definition at each level. The ordinary query asks for a state in the crossing window with an $R_j$ predecessor and an $R_j$ successor. All coordinates are unsigned 466-bit integers. The mass comparison widens them by two further bits before addition. Bounding the admitted input mass also prevents overflow on every taken arithmetic branch. The encoding retains the residue tests of the original machine.

The terminal query uses the full two-counter map, reserves $(0,0)$ as an absorbing halt, and disallows live inputs above $V=2H+1258$. It starts from the blank-connected reset $A(1,3^{36}+112,032)$. Since every live call gains at least four, after $1+\lfloor(V-W_{\rm start})/4\rfloor$ calls the orbit has halted or crossed $V$. In 462 midpoint levels it can reach the absorbing endpoint exactly when it halts by that cutoff. A negative answer to this query would leave later halting open. [Blank reset](POWER36_FOLLOWON_758.md) · [Finite horizon](EXPONENTIAL_SKIPS_758.md)

## Check and run

The checks below compare both one-step relations and their two- and four-step compositions with literal counter updates. The one-step checks cover every $(a,c)$ with both counters from 1 to 10. Compositions use selected starts. Each test asks whether any endpoint disagrees. The expected answers are six occurrences of `unsat`.

```sh
python3 cut_reachability_758.py checks | z3 -in
python3 cut_reachability_758.py ordinary --depth 12 > crossing.smt2
python3 cut_reachability_758.py terminal > terminal.smt2
```

The default crossing formula is 3,545 bytes. Z3 returned `unknown` in a ten-second attempt. The full terminal trial exited without an answer under a 1.2 GB virtual-memory cap. The compact encoding reduces the size of the input; it gives no comparable upper bound on solver work.
