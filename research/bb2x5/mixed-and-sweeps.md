# BB(2,5) holdouts • continuation log

**Result, 18 November 2026.** The blank-tape halting status of every machine studied here remains unresolved. The strongest finite result is a lower bound of more than 10¹⁵⁰ defined transitions for the mixed counter on formal line 3. The other main results are exact left-half response periods, a halting criterion for two related machines, and a proof that a particular periodic-prefix argument on line 12 cannot work with arbitrary continuations. There is no completed blank-tape proof to formalize in Rocq.

All line numbers below are one-based positions in the November 3 text file. Each machine starts in A on cell 0 of an all-zero, two-way-infinite tape. The two rows in an encoding give A and B, each in read-symbol order 0 through 4. A triple gives write symbol, direction and new state. An undefined instruction halts on arrival. The sparse interpreter counts only defined steps. The accompanying copy of the 37 strings is used for the identity checks. [Formal list](https://wiki.bbchallenge.org/w/images/c/cc/BB2x5_Rocq_holdouts_37.txt) · [Wiki status and analysis credits](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Holdouts) · [Community tracker](https://docs.google.com/spreadsheets/d/1qiZ3PJb_q4j9kddm0zZMionJhYCI_uEHr1bSmsBOlZs/edit)

## 1. The mixed counter on line 3

**Machine** `1RB---0RB0LA2RA_2LB2LA3RA4LB0LB`. The undefined instruction is A1. mxdys supplied the counter interpretation. DrDisentangle's repository gives normal and short overflow rules and identifies an unclosed parity obligation. I used those ideas in the derivation below. The residual-word calculation, two longer overflow branches and finite lower bound are results of this investigation. Priority over unpublished work is unknown. [Wiki attribution](https://wiki.bbchallenge.org/wiki/1RB---0RB0LA2RA_2LB2LA3RA4LB0LB) · [Prior macro notes and proof attempt](https://github.com/rwst/bbchallenge/tree/main/1RB---0RB0LA2RA_2LB2LA3RA4LB0LB)

| Read | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| A | 1RB | halt | 0RB | 0LA | 2RA |
| B | 2LB | 2LA | 3RA | 4LB | 0LB |

### Coordinates and elementary operations

For X ≥ 1, write its binary expansion with the leading 1 removed. Replace each remaining bit 0 by tape symbol 2 and each bit 1 by symbol 3, most significant bit on the left. Prefix this string by 13 to obtain P(X). For example P(1) = 13 and P(5) = 1323. Let C(X,d,p,v) consist, from left to right, of P(X), a 2 scanned in state A, d pairs recording v in base three least significant digit first, and p extra twos. Digits 0, 1, 2 are respectively the pairs 22, 02, 42. All other cells are blank, d ≥ 0, p is 0 or 1, and 0 ≤ v < 3ᵈ. Position is specified up to translation. Write E(X,d) and O(X,d) for v = 0 with p = 0 and 1 respectively. The blank tape reaches E(1,0) in five defined steps.

If the right side returns a left-moving B into P(X), the machine increments X and returns to the original cut in A. Each 3 is changed to 4 by B, and the first 2 becomes 3 and sends A back over the 4s, turning them to 2s. If every bit was 3, the carry crosses the marker 3 and reads its 1. B1 writes 2 and moves left in A. The next blank and the rewritten 2 recreate 13 one cell further left, and A clears the 4s. Thus X increases even when the binary word grows. An A returning into P(X) erases trailing 3s to 0 until it reaches a 2. If it passes the marker 3, it halts on A1.

A rightward A pass on a pair 22 leaves 03 and continues in A. A leftward B pass on 03 leaves 24 and continues in B. A leftward A pass on 03 leaves 22 and continues in A, using A3, A0, B0, B1. These local rules include their exit steps.

### A word rule that also handles misaligned counters

Start with A at the first position of a finite sequence of tokens, read physically from left to right. A token may be a pair (2,c) with c equal to 2, 0 or 4, or the single symbol 4. Give a pair the value v = 0, 1 or 2 respectively. A successful probe enters the sequence in A and exits on its left in B. Specify a cut immediately after the tokens. The largest number of successive successful probes that avoid visiting the cut is computed from right to left. Start with N = 0. Across a pair set N to 3N+v. Across a single 4 set N to floor(N/2).

For the proof, in a pair the leading A2 sends B to c. Values 1 and 2 decrease immediately. For value 0, B2 leaves 3 and calls the next token in A. A successful return in B turns the 3 to 4. In all three successful cases B on the leading 0 restores it to 2 and exits left. Thus n probes require floor((n+2−v)/3) probes of the remaining tokens and leave digit (v−n) mod 3. At a single 4 the successive instructions are A4, B2 and B3, interleaved with two successful A probes of the rest. This restores 4 and exits left. Induction on the number of tokens proves the capacity formula and the updated tape, including zero tokens and n = 0. Each successful probe has finite positive duration. When paired with the binary increment above, n such probes add n to X. With only a partial string of t binary bits available on the left, the same argument applies up to the last increment that fits in those t bits. This is the only accelerated operation in the lower-bound calculation. Outside it the checker takes a literal TM step.

For an ordinary nonzero ternary counter this gives C(X,d,p,v) → C(X+v,d,p,0). The final pivot can serve as the cut when reading the d ordinary tokens. With even padding at zero, the A sweep on 2^(2d+1) reaches B0 at the far blank. B reverses, restores the last 0 to 2 and turns each earlier 03 into 24. Binary increment follows. This gives E(X,d) → C(X+1,d,1,3ᵈ−1) → O(X+3ᵈ,d).

### Odd overflow, including two trailing binary ones

At O(X,d) the pivot and right side are (22)^(d+1). The forward sweep leaves (03)^(d+1). A0, B0 and B1 create two extra twos and reverse in A. Reversing across the pairs leaves 2^(2d+4) and A scanning the last cell of P(X). Write X = 2^(k+1)Y + 2ᵏ−1 with Y ≥ 1, so that the last k ones have an explicit zero to their left. The result after erasing the ones is

    P(Y) [A2] 0^k 2^(2d+4).

If X = 2ᵐ−1, m ≥ 1, there is no such zero and A reaches the marker 1 and halts. For k = 0 the displayed word is E(Y,d+2). For k = 1 it is C(Y,d+2,1,1).

The k = 0 branch gives an exact stopping criterion for any run of even resets. Between consecutive O configurations on this branch the change is (X,d) → (X/2+3^(d+2),d+2). Define D = 17X − 2·3^(d+2). The next D is exactly D/2, and D has the same parity as X. Since 17 never divides 2·3^(d+2), D is nonzero. The number of consecutive even resets is exactly the exponent of 2 dividing D. In particular the first O(2,0) has D = 16, explaining the initial run of four even resets and proving that extrapolating this branch indefinitely must fail for every integer starting value.

There is also a direct reduction for k = 3. Write K(X,d) for A on the last symbol of P(X) with 2^(2d+4) to its right. Every O(X,d) reaches K(X,d) as above. From K(16Y+7,d), erasing the three ones gives P(Y) [A2] 000 2^(2d+4). The first zero probe increments Y and leaves 2200 followed by 2^(2d+4), with A scanning the first 2. The first 22 goes to 03 and the following 00 produces two 2s and reverses in A. The 03 then becomes two more 2s. This gives K(Y+1,d+2), with Y ≥ 1. In particular X = 2^(m+4)−25 for m ≥ 2 is another halting family, for any d.

Now let X = 8Y+3, Y ≥ 1, so k = 2. Put Z = Y+1 and n = d+2. The two zeros after the pivot have specific effects.

1. The first B0 probe and its return increment Y and change the initial 00 to 20. A2 and B2 at the pivot now write 03. A0 and B2 on the next two symbols write 13. The machine is in A at the beginning of an odd run of 2d+3 twos, with P(Z) 03 13 to its left.
2. The run becomes (24)^(d+1) 22 on the return in B. The new 13 becomes 24 by B3 and B1. The earlier 03 becomes 22 on the return in A. Thus A is on the last symbol of P(Z) and its right side is exactly 22 (24)^n 22.
3. If Z = 2ᵐ−1, the left pass reaches A1. Consequently **O(2^(m+3)−13,d) halts for every m ≥ 2 and d ≥ 0**. This family includes X = 19, where X itself has an explicit zero.
4. If Z = 4W+1, W ≥ 1, the left pass erases one 3. The resulting right side after the new pivot is 0 22 (24)^n 22. Splitting into ordinary digit pairs gives a 1, a 0, then n digits equal to 2, and a final padding 2. In particular **O(32W+3,d) → C(W,d+4,1,3^(d+4)−8) → O(W+3^(d+4)−8,d+4)**.
5. If Z = 2W, W ≥ 1, its low 2 is the new pivot. Including that pivot, the tokenization is two zero-valued pairs, a single 4, n−1 maximal pairs and one zero-valued pair. The capacity is U = 9(3^(d+1)−1)/2. After U successful probes the word from the pivot is (22)² 4 (22)^n. The next probe turns the first two pairs into 03s. The 4 calls the high pairs in A. Those pairs reach A0 at the far end and return in A, restored to twos with two extra twos. A is now on the 2 left by the divider, with 2n+2 twos to its right. This odd run returns in B, leaving (24)^(n+1) 22. Restoring the two low 03 pairs and incrementing the binary prefix gives C(W+U+1,d+5,1,3^(d+5)−1). Thus **O(16W−5,d) → O(W+U+3^(d+5),d+5)**.

All these arrows describe finite runs of defined elementary transitions, except for the identified final undefined instruction in a halting case. They need not be first returns. The cases in items 3–5 leave other Z values, and other trailing-one counts, to the general token rule and literal execution.

### Blank execution and obstruction

Directly executing from blank gives O(6947,8) at step 59,171. Since 6947 = 32·217+3, item 4 applies. After 113 further elementary steps the exact tuple is (217,12,1,531433), then ordinary probes reach O(531650,12). This explains where extrapolating the early short-overflow formula fails. The route from blank through 150 successive zero-counter checkpoints takes at least the integer printed in mixed-verification.txt, exceeding 10¹⁵⁰. The final checkpoint has d = 317 and p = 1. The 125,929 operations in that calculation consist of literal steps and applications of the capacity lemma. The lower bound counts one step per elementary operation and at least one per successful probe. It gives no upper bound on the execution time. The remaining problem is to classify the infinite sequence of resets from blank or exhibit a reachable halt. None of the halting families above has been reached from blank.

## 2. Two machines with the same exact blank-half input

| Formal line | Exact encoding |
|---|---|
| 21 | `1RB2RA3LA4LA2RB_2LA3RB---0RA1LA` |
| 22 | `1RB2RA3LA4LA2RB_2LA3RA---0RA1LA` |

Both halt at B2, and every instruction moving left enters A. The wiki lists longitudinal analyses for this pair and credits mxdys for notes on line 22. I derived the finite cell tables and the prefix obstruction below. [Wiki holdout notes](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Holdouts)

A rightward entry into one cell is a letter A or B. While inside that cell, record the states in which it issues rightward calls to its neighbor. After each such call assume a return in A. Stop when the original cell exits left or halts. The table gives the new cell symbol and the word it issued. An empty word is ε.

| Initial symbol | Enter A | Enter B |
|---|---|---|
| 0 | 3, BA | 2, ε |
| 2 | 3, ε | halt, ε |
| 3 | 4, ε | 3, ABA |
| 4 | 3, B | 1, ε |
| 1 | 3, A | 4, B on line 21 or 4, A on line 22 |

All entries follow by following the literal rules on one cell, including the return legs. Once the symbol is in {1,3,4}, this set is closed under both input letters. Thus a halting cell must have had B, B as its first two inputs.

The left half, x < 0, answers repeated entries from the right in state A with the infinite rightward-state word S = (BAABABABAAABA) repeated. The induction verifying this word matters because a finite trace leaves open the possibility of a subsequent different answer. Model cell −1, using the proposed S for calls into x < −1. That smaller half-line starts blank and is a translate of the original half. During the first fifteen external requests the numbers of subordinate calls are

    0 0 | 1 0 0 2 1 0 0 3 1 0 0 2 3

and the cell's symbols after the requests are

    1 2 | 0 1 2 2 0 1 2 2 0 1 2 2 2.

The emitted answers are BAABABABAAABABA. After the two initial requests, the cell, the output phase and the subordinate-input phase repeat after thirteen further requests consuming thirteen subordinate answers. The cumulative number of subordinate calls by external request j is strictly less than j, with j counted from one. Strong induction on j therefore justifies every use of the proposed sequence, including termination of every call. The verifier performs the analogous finite checks in the table below.

Drive cell 0 by A followed by S. Apply its one-cell table to obtain the input to cell 1, then repeat, stopping any stream at a detected halt. Under this construction the blank machine halts if and only if some fresh nonnegative cell gets the prefix BB. In one direction the cell table accounts for every actual halt, and the proven left half answers safely. In the other direction, the two B entries at the offending fresh cell issue no calls further right. A finite input prefix producing those entries is realizable by the finite strip ending at that cell, using its true left returns. No deeper excursion can precede the halt. Finite prefixes of the left source are available in finite time by the induction above. Infinite waiting in a deeper excursion is therefore harmless to this equivalence. What remains unresolved is whether the specified iterates of the **particular** periodic source ever begin BB. Widening the admissible inputs to independently chosen length-10 factors admits a spurious BB on both machines.

## 3. A periodic right-half driver on line 12

**Machine** `1RB4RB4RA1LA3LA_1LB2LA3RB2RB---`. The undefined instruction is B4. The wiki attributes a prior longitudinal analysis to dyuan. I grouped three successive tape cells into a block and checked its finite entry, exit and output transitions. A hypothetical right neighbor returns left in A. A wrong-state return is distinct from a halt. [Wiki holdout notes](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Holdouts)

Let P be the eight-letter word ABABBAAB. From a fresh 000 block, input A takes it to 210 and emits ε. The next A would halt internally and the next B instead takes it to 120, emitting ε. From 120, A emits A and ends in 333. All 27 states in {1,2,3}³ are closed under both letters. Starting at 000, the entire P emits its first seven letters and leaves 313. From 313 each further P returns to 313 and emits BABABBAA. Hence P repeated forever is an exact fixed input/output word. The suffix delayed during a partial period has length one to three after initialization. The true blank left source for line 12 is A followed by (BBBABABAABABBA) repeated. Its successive block images develop a long initial agreement with the fixed word. Infinite agreement on the blank orbit remains unproved.

There is a rigorous limit on any proof using only this agreement. From **every** one of the 27 ordinary block states and for **either** desired output letter there is a finite input which emits exactly that letter and finishes in an ordinary state. The checker enumerates the 54 witnesses using silent transitions and a final one-letter emission. The longest witness has eight letters. Concatenation can thus prescribe *any finite future output* of an ordinary block. Composing this observation gives the same control over a finite row of ordinary blocks.

Consider an arbitrary finite prefix of the periodic fixed word. Passing it through a blank block yields a strictly shorter prefix of the same word, as checked for one initial period and one steady period including all their prefixes. For input length at least three the end state is ordinary. Iterate until the remaining prefix has length zero, one or two. At length zero, choose AA to halt the fresh block. At length one the prefix is A, so append A. At length two it is AB, leaving 120. Send A to emit A and reach 333, then prescribe a second output A to halt the following fresh block. The control property propagates any of these prescribed finite extensions back through the earlier ordinary blocks. At the first AA halt the fresh block has made no calls farther right. Consequently **every finite prefix of the periodic driver has a halting extension when the external input is free**. The actual blank half-line supplies one fixed input. Its exact tail correlations are essential to using this representation.

## 4. Parity sweep on line 36

**Machine** `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---`. In the sweep representation A scans a blank just to the left of a contiguous word over {1,2} with blank exterior. The rightward phase matches opening 1 against closing 2 like parentheses. A prefix with six excess closings causes B4. In an ordinary data interval of the return word the closing symbol 2 marks a change in the bit indicating whether an opening survived. The previous log derives the boundary guards and header separately. The symbolic sweep and an independent literal interpreter are included in prior_sweeps.py. [Prior analysis credits in the tracker](https://docs.google.com/spreadsheets/d/1qiZ3PJb_q4j9kddm0zZMionJhYCI_uEHr1bSmsBOlZs/edit)

Between consecutive unmatched openings the intervening word is completely paired. Each interior gap of zeros in the survivor-bit sequence therefore has even length. In the derivative word, distances between successive closing symbols alternate between lengths of one-runs and lengths of zero-runs, with each internal zero-run of length at least two. A complete one-run plus the following zero-run consumes at least three cells and produces only two changes. Thus any interior interval of length L has at most 2L/3 + O(1) closing symbols. The constant comes only from the two end runs and can be bounded by four by discarding the at most two partial runs at each end of a partition into complete run pairs.

The restriction still admits failure after taking genuine sweep images. From the nonblank seed 1211112, the successive prefix minima are 0, −1 and −6. The third sweep reaches B4, after 160 defined transitions in total. On the blank orbit, at epochs 200, 400 and 700, words six epochs apart share left prefixes of lengths 310, 640 and 1,138 respectively. Their signed balances are 158, 340 and 604. If such a prefix were available inductively, the density estimate could bound the remaining suffix's ability to exhaust the guard. Matching decisions near the end of the prefix depend on the future suffix. I have no induction proving the required prefix growth. These samples and the auxiliary halt are independent of the line-3 result.

## 5. Other candidates and verification

The table records all ten left-half certificates used in the longitudinal search. A left-half certificate concerns repeated entry in the indicated state on the rightmost cell of an initially blank negative half-line. It imposes no claim about which state the positive half returns during the actual blank execution. The right-block representation requires its own proof. On line 20, for example, the second B in a fresh cell gives a leftward B exit under the restricted experiment. It is not the undefined instruction.

| Line | Exact encoding | Entry | Prefix | Repeating answers |
|---|---|---|---|---|
| 8 | `1RB4LA1RA1RB1LA_2LB3LA---4RA2RB` | A | ε | BBABA |
| 11 | `1RB2LA4LA1RA1LA_2LB3RB4RB---2RA` | A | ε | BBBA |
| 12 | `1RB4RB4RA1LA3LA_1LB2LA3RB2RB---` | A | ε | BBBABABAABABBA |
| 13 | `1RB3RA3RB4LA1LA_1LB2LA1LA---1RB` | A | ε | BABAB |
| 15 | `1RB3RB1LA2LA3RA_1LB2RA4RB0LA---` | A | BBBA | BABAABBABBABAAAB |
| 20 | `1RB2RA3LA4LA2RB_2LA---3LB1RA3RA` | A | BAAAB | ABA |
| 21 | `1RB2RA3LA4LA2RB_2LA3RB---0RA1LA` | A | ε | BAABABABAAABA |
| 22 | `1RB2RA3LA4LA2RB_2LA3RA---0RA1LA` | A | ε | BAABABABAAABA |
| 26 | `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA` | A | ε | BBAAAA |
| 31 | `1RB3RB---4RA2RA_2LA2RA3LB4LB1LB` | B | ε | ABAAA |

For lines 8, 11, 13, 15 and 31 the obstruction is control of future entries on the right, even after the left response is known. On line 26 the first event presented to a fresh counter column is the outstanding phase condition from the earlier investigation. On line 20 a wrong-state return invalidates the restricted entry model. I also inspected the aligned pair updates of `1RB---4RB2RB4LA_2LB3LA3LB0RA0RB` (line 9). The rightward replacements 22→00, 23→40 and 33→20 continue in A. Pair 32 turns back in B and the blank boundary initiates a different return. On `1RB2RA3LB---2LB_2LA0LA4RB0RB1LA` (line 17) I inspected blank frontier traces. The length-changing overflow remains unclassified in this work. [Prior discussion of line 17](https://wiki.bbchallenge.org/wiki/1RB2RA3LB---2LB_2LA0LA4RB0RB1LA)

Run `python3 mixed_and_sweeps.py` from the extracted directory with Python 3.10 or later. The script uses the standard library, verifies machine identities against the supplied list and prints the exact final tuple and finite lower bound. The literal TM tests are independent of the particular shortcut they compare. The larger bound also uses the mathematically justified shortcut. mixed-verification.txt contains the observed output. The preceding log and its original finite audit cover the other three matching sweeps and the line-5 arithmetic machine.
