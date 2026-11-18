# A scalar return map for BB(2,5) holdout 4

On blank tape, `1RB3LA1LA1RA3RA_2LB2RA---4RB1LB` reaches its millionth return to the configuration A(6,b). At that return, the length b of the right-hand run has **2,855,427 binary digits**. The run from blank takes **more than 10^1,719,137 defined instructions**. Whether it eventually halts remains open.

A single integer suffices to compute successive returns. The inverse map gives a separate result about the possible halting targets. Exactly 16/2401 of the candidate exponents have a target with more than one immediate predecessor, in natural density. These predecessors can start from auxiliary tapes.

## Coordinates and return rules

The machine starts in state A at cell zero of an all-zero, two-way-infinite tape. Its undefined instruction is B2. Write C(a,k,b) for the physical state-A head immediately after the word 1 4ᵃ 1ᵏ and before the word 1ᵇ 2. Write A(a,b) for C(a,3,b). In B(a,b) the physical head is also in state A, after 1 4ᵃ 1ᵇ and before a single 1. All exterior cells are zero. Racheline introduced these two tape families and the principal A and B return rules. [Original analysis](https://wiki.bbchallenge.org/wiki/1RB3LA1LA1RA3RA_2LB2RA---4RB1LB)

Blank reaches B(2,7) in 93 defined steps. Let X=7a+3b+8 on a B configuration and write X=3k+d. The grouped B rules have the following scalar form.

| d | Next action |
|---:|---|
| 0 | Set X to 7k+1. |
| 1 | Set X to 7k+2. |
| 2 | Return to A(6,k−6). |

Indeed B(3q+1,s) reaches B(7q+s+1,7), B(3q+2,s) reaches B(7q+s+4,5), and B(3q,s) reaches A(6,7q+s−4) when 7q+s≥4. Every B reached here satisfies the last guard if its first coordinate is divisible by three. The initial second parameter is 7. A B-to-B step emits 5 or 7, and the only seed below 5 emitted by A is B(3a+4,2), whose first coordinate is 1 modulo 3. Starting from X=43 gives 43 → 100 → 233 → A(6,71). This first return takes 6,393 defined steps from blank.

From A(6,b), choose the largest n≥0 with Lₙ=8(3ⁿ−1)−n ≤ b. Call n the **width** and put p=3ⁿ. The A-to-A rule A(a,s) → A(3a+4,s−2a−3), for s≥2a+3, iterates exactly n times. It leaves A(a,u) with a=8p−2 and u=b−Lₙ, where 0≤u≤2a+2. The next outcome is exhaustive.

| Residual count u | B seed or halt |
|---|---|
| 2j ≤ 2a−4 | B(a−j−2,3j+7) |
| 2j+1 ≤ 2a−1 | B(a−j−1,3j+5) |
| 2a−2 | B(3a+1,5) |
| 2a | B(3a+1,7) |
| 2a+1 | Halt |
| 2a+2 | B(3a+4,2) |

The first row includes u=0. In that case the last two 4s and the finite suffix `111[A]2` suffice to reach B(a−2,7) in 46 defined instructions. The head stays to the right of the untouched prefix. For general j the pair rule C(a+1,k,s+2) → C(a,k+3,s), derived below, consumes j pairs and leaves that same endpoint rule with k=3j+3.

Define Hₙ=24p−n−11. The row u=2a+1 gives exactly b=Hₙ. For an ordinary even or odd row the B integer is X=56p+u+1=b+48p+n+9. The three exceptional B seeds, in increasing order of u, have X=168p−12, 168p−6, 168p. For u=2a−2 and 2a, one additional update of the ordinary scalar expression gives the actual seed. Thus the untimed runner needs only three cases.

1. At b=Hₙ the machine halts in this A phase.
2. At b=Hₙ+1 start the scalar loop with X=168p.
3. Otherwise start it with X=b+48p+n+9.

Iterate the B table until it emits the next A return. Every transition of the tape machine writes a nonzero symbol. On a B(0,s+4) → A(6,s) boundary, the A head sweeps left across a run of ones and writes on a virgin blank. Thus the occupied length strictly increases between consecutive B-to-A returns. At A(6,b) that length is 11+b, so b increases strictly.

## The millionth return

| Return from B | Width | Binary digits of b | b mod 1,000,000,007 |
|---:|---:|---:|---:|
| 1 | 2 | 7 | 71 |
| 1,024 | 1,886 | 2,994 | 705,696,753 |
| 30,000 | 54,111 | 85,769 | 912,921,932 |
| 1,000,000 | 1,801,571 | 2,855,427 | 611,727,417 |

Every candidate exponent below 1,801,571 has been passed permanently on blank. A future blank halt would require a subsequent A return with b=Hₙ.

Two timing rules give a lower bound for the computation. Their durations count defined elementary tape instructions.

* **Consuming a pair.** In C(a+1,k,s+2), the first scanned 1 sends A left across the other k ones. The anchor 4 becomes 3 and A restores the k+1 ones on its rightward pass, taking 2k+3 steps. Processing the next 1 similarly changes the anchor from 3 to 1 in 2k+5 steps. The result is C(a,k+3,s) after 4k+8 steps.
* **Consuming three 4s.** B(a+3,s) reaches B(a,s+7) in 12s+56 steps. To check the count, consider an anchor 3 or 4 followed by h ones. On a scanned 1 the reflection just used takes 2h+3 steps. On a scanned blank the five literal instructions A0, B0, B1, A2, A2 leave two new ones and put the head immediately to their left. Reflection across the old h ones takes a further 2h+1 steps. Starting with three anchors 444 and h=s, the successive operations are a one, a blank, a pair, a blank, and a one. Their durations are 2s+3, 2s+8, 4s+16, 2s+16, and 2s+13. The final head is on the last 1.

Suppose the last grouped B step into A(6,b) starts at B(3q,s). Its q triple reductions take 42q²+(12s+14)q steps, and b=7q+s−4. If s≤7 this alone gives at least 2(b−3)²/3 for b≥3. Otherwise this B came directly from an ordinary A endpoint after j pairs, so s is 3j+5 or 3j+7. The pair reductions have already taken 6j²+14j steps. Since b−3≤7q+3j, the two costs together are at least 2(b−3)²/3. Substituting b≥2^2855426 from the last row of the table gives the stated lower bound.

## How many immediate predecessors can a halting target have?

Here a predecessor of y means a value x such that the *next* B-to-A return after A(6,x) is A(6,y). The B endpoint must have X=3y+20. There is a unique inverse when X=7q+d+1 for d=0 or 1. The preceding scalar value was then 3q+d. With V=X+1/4 each inverse step satisfies Vprev=(3/7)V ± 2/7. Summing the geometric error shows that after t successful inverse steps the earlier X is the nearest integer to (3/7)ᵗ(X+1/4)−1/4.

For n≥6, **Hₙ has more than one predecessor exactly when X=3Hₙ+20 allows four successive inverse steps**. To prove this, every actual A seed lies in an interval [56·3ᵐ−12,72·3ᵐ] for some m. The three exceptional seeds use m one greater than the originating width. Every integer from 56·3ᵐ+1 through 72·3ᵐ−6 is an ordinary seed at width m.

The endpoint X=72p−3n−13 is itself an ordinary seed of width n. It is strictly above the exceptional seeds near 56p and below the next width's seeds. It gives one predecessor. After one, two, or three inverse steps, the leading coefficient 72(3/7)ᵗ lies in the gaps (24,56), (8,56/3), and (8/3,56/9), respectively, between the seed intervals in units of p. After four it equals 5832/2401, inside (56/27,72/27), corresponding to width n−3. In each case the distance from the nearest endpoint is greater than 1/5. The additive error from the term −3n−13, the inverse rounding, and the endpoint offsets is at most 3n+26 < p/5 for n≥6. Thus the first three inverses cannot be seeds, while a successful fourth supplies a distinct, ordinary predecessor.

At depth t each prescribed sequence of t inverse digits selects one residue modulo 7ᵗ. Adding 7ᵗ to a starting X adds 3ᵗ to its state after t inverse steps, so exactly one lift modulo 7ᵗ⁺¹ selects each specified next digit. There are therefore 2ᵗ surviving residues. When n increases by 6·7ʲ, X(n)=72·3ⁿ−3n−13 changes by −18·7ʲ modulo 7ʲ⁺¹, since 3⁶≡1 modulo 7. Consequently X(n) permutes the residues modulo 7ᵗ as n runs through the 7ᵗ lifts of any fixed class modulo 6. At t=4 this proves the density 16/2401. It concerns the number of immediate predecessors of targets. Deciding whether a chain of predecessors contains 71 is still necessary for a blank-tape result.

## Reproduction

From `research/bb2x5`, with a C++17 compiler, GMP development headers and Python 3.10 or later, run

```sh
c++ -O2 -std=c++17 line4_scalar.cpp -lgmpxx -lgmp -o /tmp/line4_scalar
python3 check_line4_scalar.py /tmp/line4_scalar
/tmp/line4_scalar 1000000
```

The runner defaults to return 1,024 and stops at the requested A configuration. It compiles a table for the 3⁷ possible low-order residues. During seven updates of 3⁷Q+r, or until an earlier return, the next digit depends only on the current offset and the remaining quotient coefficient is divisible by three. Each table entry therefore gives an exact affine function of Q.

The checker compares three complete tape configurations through step 172,248 against the literal interpreter, tests the executable at sampled returns against the two-coordinate A/B rules, and enumerates the four-digit inverse residues. The decimal residue in the results table is a compact comparison value; the runner performs the computation with full integers.
