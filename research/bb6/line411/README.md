# BB(6) line 411 · bbchallenge ID 116372

The machine starts in A on a two-way tape of zeros. Its table is `1RB0LF_1RC1RB_0RD0RC_1LE1LF_1LD---_0LB1LA`. The project lists it at rank 432. Its blank-tape halting status remains open. [Pinned rankings](https://github.com/valu42/busycoqtesting/blob/175f2c272c1d5dfd1ff16f277839f19877cb2364/research/bb6/RANKINGS.md#L514)

At a boundary defined below, the machine halts exactly when its unread word starts with zero or more copies of `1001` followed by `1000`. A four-interface transducer handles arbitrary finite tape words and always returns. The only part left to decide is whether the blank orbit ever produces a word that satisfies the terminal test below. The executable proof uses Python integer arithmetic and checks the local rules against the transition table. The new results have been checked by their standalone verifier. A Rocq or Lean formalization of this reduction remains open.

## Reproduce

Run these commands in this directory using Python 3 with assertions enabled. The default checkpoint goes one macro step beyond the related machine's halt.

```sh
python3 line411.py
python3 line411.py --epochs 100
python3 line411.py --steps 300000
```

| Macro steps | Completed overflows | Lower bound on elementary transitions | SHA-256 of the reached configuration |
|---:|---:|---:|---|
| 12,418 | 374 | `10^227` | `e76aeeb8d94d8168c4669c302d991c5d7caf4d280c515403f8b8e7d5d2143dfa` |
| 300,000 | 3,338 | `10^2012` | `3e3bfc1d6742ae3b92cc8fe3aff1b3f608ec0f7092b7560f39706a0741bab9ab` |

The long row reaches mode L, left counters of 2 and 3,342 bits, and a right word of 323,754 bits. The digest covers the orientation, both integer values, and every symbol of that word. A separate simulator that executed each individual rightward excursion directly on tape obtained the same two digests. The count includes the initial 301 elementary transitions and the exact cost of the left sweeps. Every omitted right excursion executes additional transitions.

## Coordinates and left sweeps

Reflect the tape and rename the original states A, B, C, D, E, F to A, C, D, E, B, F. The new table is `1LC0RF_1RE---_1LD1LC_0LE0LD_1RB1RF_0RC1RA`. The unique undefined instruction is now B reading 1. All words below are written in physical left-to-right order in these reflected coordinates. A finite right word has an infinite zero continuation.

Let $P(a,b)=0^\infty 1^a(10)^b$. In $L(a,b,r)$ state D scans the last cell of $P(a,b)$ and the tape to its right is $011r$. In $R(a,b,r)$ the tape on the left is $P(a,b)101$ and state A scans the first cell of $r$. Direct execution of the blank machine reaches $L(11,5,10^\infty)$ after 301 transitions. Here the right suffix is a single 1 followed by zeros.

For odd $a\ge3$, these identities hold for every right suffix $v$.

| Input | Output | Elementary transitions |
|---|---|---:|
| $L(a,b,v)$ with $b>0$ | $R(a+4,b-1,v)$ | $2a+12b+6$ |
| $L(a,b,101v)$ | $L(a+4,b,1v)$ | $2a+12b+16$ |
| $L(a,b,11v)$ | $R(a+4,b,v)$ | $2a+12b+8$ |
| $L(a,0,00v)$ | $R(3,(a+3)/2,0v)$ | $4a+23$ |

The verifier constructs each finite tape and executes the original local transitions in the reflected coordinates. To cover arbitrary $a$ and $b$, it records the state and direction each time the head crosses a cut. If two cuts have identical ordered crossing sequences, the strip between them may be duplicated. Each entry into an inserted copy follows the same cell histories as in the original strip. Identical states and directions at the cuts join the histories in order. Both ends of the execution lie outside the inserted strip. The cost increases by the number of visits to its cells. This construction works for any number of copies and for disjoint strips independently.

The finite bases use $a=3,5,7$ and $0\le b\le4$ where the rule applies. Duplicating a two-cell strip at $a=7$ adds two to $a$. A disjoint two-cell strip at $b=4$ adds one to $b$. The checker compares initial and final tapes and costs after duplication, checks both crossing sequences, and rejects any access to the unspecified right suffix. The same construction verifies the uniform-left rules for the boundary test.

## The right side always returns

A right call starts with the head on the first symbol of its input and three known cells immediately to its left. It returns when the head first moves to the left of those three cells. The right input may be any finite-support word.

| Entry state and three cells | Possible return state and three cells |
|---|---|
| A, 101 | D, 011 |
| A, 111 | C, 111 or D, 000 |
| C, 100 | C, 111 or D, 000 or D, 011 |
| C, 110 | D, 001 |

To verify this table, supply two input bits after the three known cells. Follow the elementary transitions until the head either returns to the left or asks for a third input bit. In the latter case its last three cells and its state are one of the four entries. Substitute each allowed child return, record the resulting two output bits, and finish the local execution. For all 16 combinations of entry and input pair, there is at most one child call. It starts two cells farther right. Once the untouched remainder is blank, each entry closes within at most two more pairs. Induction from the last nonzero cell proves termination and the stated exits without assuming the table as an axiom.

Denote by $F(r)$ the resulting word from entry A, 101. Then $R(a,b,r)$ reaches $L(a,b,F(r))$ for every finite-support $r$. All these calls avoid the missing instruction.

## Complete boundary test

For a transparent version of the reduction, take the first left-sweep rule exactly $b$ times, pairing each application with a right call. This reaches $L(a+4b,0,F^b(r))$. In $L(a,0,r)$ the next $2a+6$ transitions produce $0^\infty 1^{a+5}$ immediately left of state A scanning $r$. Write $H(N,r)$ for this configuration. Its initial $N=a+5$ is even and at least eight.

### An orbit on one integer and one word

Start at $H(36,000110011)$. From the initialization above, five applications of $F$ to the single 1 give that word. In $H(N,w)$, strip the maximal prefix $(1001)^k$ of $w$, and call what follows the residual word. Continue reading zeros beyond the end of a stored word.

| Residual word | Next boundary or outcome |
|---|---|
| $0v$ | $H(2N+4,F^{N/2}(1^{4k}v))$ |
| $11v$ | $H(N+4k+4,F(v))$ |
| $101v$ | $H(N+4k+4,1v)$ |
| $1000v$ | Halt |

These cases exhaust the possibilities after the maximal prefix is stripped. Every nonterminal row takes a positive finite number of elementary transitions. Thus the original blank machine halts **if and only if** this orbit ever uses the last row. An infinite orbit proves nonhalting. The arithmetic stays integral since $N$ starts at 36 and remains divisible by four.

The same pair rules give a standalone description of $F$. Strip the maximal $(1001)^k$ as above. In the following identities $x$ is a single bit and $v$ is the remaining suffix.

| Residual word | $F(w)$ |
|---|---|
| $0v$ | $1^{4k+1}v$ |
| $11v$ | $0^{4k}11F(v)$ |
| $101v$ | $0^{4k}111v$ |
| $1000xv$ | $0^{4k}00011v$ |

The only recursion on the right removes a finite prefix ending in 11. The infinite zero continuation uses the first row.

### Why the terminal pattern is exact

Run the three-cell call A, 111 on $w$ and call its output $u$. Each leading `1001` induces a call of the same type four cells farther right. On the way back those four cells become `1111` for a C, 111 return or `0000` for a D, 000 return. This follows from the `10` case of A, 111 and the `01` case of C, 100. The 16 generated rows in the checker verify both cases and every terminal pair.

If the residual word is $0v$, the call returns C, 111 with $u=1^{4k+1}v$. The next $2N+3$ transitions reach $R(3,(N-2)/2,1^{4k}v)$. That right call and the ensuing $(N-2)/2$ left increments give exactly $N/2$ applications of $F$ in the first row of the orbit.

In the other three cases the call returns D, 000. D erases the $N-3$ ones on its left, passes a zero, and places E on the next blank. If the first 1 of $u$ has $z$ zeros before it, its distance from E is $N+2+z$. On a residual $11v$ the output starts $0^{4k}11F(v)$. On $101v$ it starts $0^{4k}111v$. In both cases E reaches the first 1, F reads the next 1, and A starts the next boundary with $N+4k+4$ ones. On $1000xv$ the output starts $0^{4k}00011v$. The first 1 is at odd distance, so B reads it and halts. These four cases also show that the call can never return an all-zero word.

The script's `--epochs` option follows this boundary test. One epoch ends at the first-row sweep. Its first six epoch endpoints agree, cell for cell, with direct execution of the original unreflected table after 956, 6,315, 30,790, 139,827, 579,226 and 2,338,973 elementary transitions. Starting from $L(3,0,000000001)$ instead reaches the undefined transition after 742 successful moves. The remaining proof obligation depends on which right words the *blank* orbit actually reaches.

## Batching calls and earlier work

For the long replay, the digit checker verifies seven elementary call identities on finite windows. A mode-0 digit is either 0000/0110, which carries into mode 0, or 0011/0111, which carries into mode 1. A mode-1 digit is 00/10 and carries into mode 0. The mode-1 word 11 stays fixed and forwards every call. The first word in each digit pair encodes zero. Processing $k$ inputs at a digit of value $d$ writes $(k+d)\bmod 2$ and forwards $\lfloor(k+d)/2\rfloor$. The replay batches only calls whose carry is absorbed by the verified prefix. It uses the total right transducer for individual calls outside that prefix.

The digit encoding and left-sweep forms come from `SBCv9.v`, module TM2. That module proves a halt for the different table `1RB0RF_0LC---_1LD1LC_0LE0LD_1RE1RF_0RC1RA`. Replaying it produces its published final 13,297 transitions. Line 411 continues through that configuration. The proof and the four-interface transducer here use line 411's own transition table. [Related Rocq proof](https://github.com/ccz181078/busycoq/blob/33209bc7dc282b38c8cd6be507bfc551fea56108/verify/SBCv9.v#L639)

Earlier work on this exact table gave Lean lemmas for individual sweeps, a kernel check through ten million moves, and a simulator run through one billion. Its public write-up lists the blank-tape status as open. The pinned ranking, fork register, upstream proof paths and pull requests, and public searches for the exact table and its HHH spelling yielded no prior blank-tape resolution in the search on 19 November 2026. [Earlier results and status](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/3c7d4736362e77b987beb5c043056b24994b5a60/holdouts/1RB0LF_1RC1RB_0RD0RC_1LE1LF_1LD---_0LB1LA/README.md)
