# Line 33 · One aligned terminal block protects an arbitrary request batch

`1RB2LA0RB4LB1RA_1LA3RA1RA---0LA` · 2026-11-18 · mathematical argument and native checks, without formal verification

Let F be the ordinary A request from the [line 33 return rules](neglected33.md), C = 421, and D the four two-cell words 22, 21, 14, 24. A word K of pairs from D has a fixed alignment starting at its first cell. Blank exterior follows each finite tape word.

**Theorem.** Take **any** digit d in {1,2,4}, any K consisting of pairs from D, any r ≥ 1, and any finite n ≥ 0. Then F^n(d K C^r) completes ordinarily, with all n replies in A. If the output with a single copy of C is v, the output with r copies is exactly v C^(r−1). Its raw clock exceeds the one-copy clock by 3(r−1)(|v| − |d K C|).

This supplies a sufficient condition for an entire extension of the blank machine, including the one-cell shift that disrupts the original pair boundaries. The solitary input 2 shows why the terminal copy cannot be omitted from a uniform theorem. The blank recurrence prepends another 2 after every extension. Persistence of the hypothesis across infinitely many such shifts is the unresolved step.

The [timed blank trajectory](compress33.md) applies the recurrence to the actual machine. The [conditional risk calculation](reserve33-outlook.md) compares observed gain/loss signs on two disjoint portions of that trajectory and states what a probabilistic forecast would require.

## Moving one digit through an aligned register

For an aligned pair XY, the ordinary rules give F^s(XY w) = X′Y′ F^b(w) whenever the indicated suffix batch succeeds. The pair 22 is fixed and b=2s. The other three pairs trace 21 → 14 → 24 → 21, sending one request on the 21 → 14 leg. This gives both X′Y′ and b without inspecting w. A finite batch on the virgin tail gives a word V(s) made only of these last three pairs: F(empty)=21, and moving the remaining requests through that pair leaves strictly fewer requests for its child. The substitution theorem in the main report also gives F^s(C^r) = V(s) C^r.

During a shifted scan a remaining calculation has the form F^a(d F^s(K C^r)). Its initial values are a=n and s=0. For a=0 the inner calculation succeeds by the aligned rules and the finite virgin computation just described. For a>0 take the first pair of K, apply its s requests, and obtain X′Y′ followed by F^b of the remaining pairs. The first digit X′ is always 1 or 2. The following local reductions emit an aligned leading pair, with a single displaced digit to its right.

| Displaced digit and exposed pair | Reduction before batching the new leading pair |
| --- | --- |
| 2 X′Y′ | 2X′ is 21 or 22; keep all a requests and carry Y′ |
| 1 X′Y′ | First request changes 1 to 2; use a−1 requests on 2X′ and carry Y′ |
| 41Y′ | First request gives 22Y′; use a−1 on 22 and carry Y′ |
| 421u | First request gives 214 F(u); use a−1 on 21 and carry 4 |
| 422u | First request gives 222 F²(u); use a−1 on 22 and carry 2 |
| 424u | First request gives 221u; use a−1 on 22 and carry 1 |

Here u includes the pending b inner requests. The last three lines increase b by 1, 2 or 0 respectively. Batching the emitted leading pair gives a new outer count, and removes one input pair of K. The identities expand into the chronological local paths proved in the main report, so a finite successful evaluation covers every instruction. This two-count reduction was obtained in collaboration with the line 33 prefix investigation.

## A finite right edge

Once K is exhausted, expand the residual inner requests on C^r to V(s) C^r. Apply the same shifted scan to the pairs of V(s), with the new inner count initialized to zero. These pairs never include 22. If the outer count reaches zero during this scan, every remaining aligned batch succeeds.

When the outer count stays positive, the possible carry pairs in this second scan are particularly restricted. In each cell of the table the digit and integer describe the new displaced digit and inner count. The transition is independent of the positive outer count, as the table of local reductions shows.

| Current carry | Input 21 | Input 14 | Input 24 |
| --- | --- | --- | --- |
| (1,0) or (2,0) | (1,0) | (4,0) | (4,0) |
| (4,0) | (4,1) | (4,0) | (1,0) |
| (4,1) | (4,1) | (1,0) | (4,1) |

At the physical end only four expressions require calibration. For (1,0), 1 C^r is the aligned word 14·21·C^(r−1). For (2,0), 2 C^r is 24·21·C^(r−1). For (4,0), one request on 4 C^r gives 2·21·C^r = 22·14·21·C^(r−1), after which all remaining requests are aligned. For (4,1), the expression is already 4·21·C^r = C^(r+1). Zero outer requests simply return the current expression. Thus every case succeeds with just one terminal C, establishing the first part of the theorem. The exact output and clock with extra copies follow by the proved C-substitution on that one-copy computation.

For s>0 the most significant pair of V(s) is always 21. Its last transition therefore selects either (1,0) or (4,1) if the outer scan reaches it. These two terminal expressions consume one aligned copy or add one. An outer batch can exhaust earlier; a proof using the two terminal phases must control that case as well.

## Which ternary pairs must become 22

Every scanned 22 in the input register emits 22 at its pair index regardless of the carry digit, inner count and positive outer count. For a displaced 1 or 2 the temporary leading pair after normalization is 22. With a displaced 4 the exact 422 rule also supplies a leading 22. Batched requests leave 22 fixed. Across successive completed shifted scans these positions therefore persist at the same indices in the new canonical registers.

The second scan has a sharper restriction. Put U = (1,0) or initial (2,0), V = (4,0), W = (4,1). Exactly **one** input at each carry state emits a ternary pair; the other two inputs emit 22.

| Carry | Sole input remaining ternary | Successor on that input |
| --- | --- | --- |
| U | 14 | V |
| V | 21 | W |
| W | 24 | W |

In particular, if the final 21 selects the losing (1,0) calibration, it came from U and emits a new 22. This connects a lost copy of C to a specific doubling pair in the new register, whenever both scans reach this final trit. A run of inputs that all remain ternary contains at most two nonzero trits (21 and 14); after reaching W it can only continue on 24, the zero trit. If a scanned portion has h nonzero trits and creates g doubling pairs, its g+1 intervening runs contain at most 2(g+1) nonzero trits. The g converted positions contain at most g more. Consequently **g ≥ ⌈(h−2)/3⌉**. The repeating inputs 14,21,14 from U attain one conversion per three nonzero trits and return to U. This controls conversion without any independence assumption. A proof must still relate the resulting doubling pairs to *future* terminal phases.

## A congruence between successive losing phases

Use the balanced ternary value of a virgin word V(M): 21, 14 and 24 represent +1, −1 and 0 respectively, in least-significant-first order. The pair cycle increases the value by one, including its carry from +1 to −1 in the next position. The virgin base case represents 1. Thus F^b(V(M) C^r) = V(M+b) C^r, and V(2) = 14·21.

Suppose the second scan reaches its final 21 in the losing state, with t ≥ 1 consecutive input trits at its end emitting 22. Write a for the outer request count remaining after the last trit. Every such doubling pair forwards twice the previous count minus twice the cost of its initial request, i.e. 2(a_old−1), except that a displaced 2 forwards 2a_old. The displaced 2 can occur only on the first trit of this *second* scan. Iterating over the t final trits gives **a ≡ 2 (mod 2^t)**. A different rule on the first of these t trits changes the result by a multiple of 2^t. In the losing calibration r≥1, the final register is therefore (22)^t followed by V(M) and C^(r−1), with **M = a+2 ≡ 4 (mod 2^t)**. The displayed t pairs may be preceded by further pairs.

If the next shifted scan crosses the same t positions, the first 22 forwards even inner and outer counts and leaves displaced digit 2. Every subsequent 22 doubles both counts and keeps that digit. At their right cut, both counts are therefore divisible by 2^t. In particular the integer whose ternary trits are processed there is **M+s ≡ 4 (mod 2^t)**. This restriction links two actual extensions whenever the specified scans and losing event occur.

For example, granting an arbitrary even outer count and even inner count at the last doubling pair would allow an exact repeated loss. For r≥1,

```
F²(2 F²⁰(V(20) C^r)) = (22)^4 V(20) C^(r−1).
```

Here V(40) consists of four 21 pairs. The outer counts after those pairs are 4, 6, 10 and 18. The remaining 18 requests act on 1 C^r = V(2) C^(r−1). The tail integer therefore resets to 20. But after installing four adjacent doubling pairs, the next two counts must both be divisible by 16; the proposed reset to counts 2 and 20 violates this physical constraint. At r=0 the first outer request in the artificial example returns B after 347 instructions. None of these counterfactual count choices is asserted to come from blank.

Divisibility alone also admits spurious trajectories. Direct normalization gives F⁴(2 F⁴(V(4) C^r)) = 14·22·22·V(4)·C^(r−1) for r≥1. The two final doubling pairs are preceded by 14, and the same incoming counts (4,4) meet their divisibility requirement. At r=0 the fourth outer request encounters a physical B3 after 137 instructions from its entry. The prefix dynamics would have to deliver those counts again at the new cut for this loss to repeat.

More generally consider two successive losses whose integer words at the respective last-register cuts consist entirely of 21. Suppose the first such word has even length L≥4 and a positive outer count processes every trit. Its L output pairs all double. If the next word also consists entirely of 21, its value is (3^L′−1)/2 and the previous congruence requires 3^L′ ≡ 9 (mod 2^(L+1)). The order of 3 modulo 2^(L+1) is 2^(L−1): for m≥1 the exponent of two in 3^(2^m)−1 is m+2 by factoring the next square, since 3^(2^m)+1 is 2 modulo 4. Therefore L′ ≡ 2 (mod 2^(L−1)). When the initial carry at the first last-register cut is 2 and its outer count n is positive and even, its new integer is 2^L(n−1)+4 > 4. The choice L′=2 then cannot supply the required value. Even this highly repetitive family of hypothetical negative phases must grow quickly. General ternary trit patterns remain unrestricted by this special calculation beyond the stated dyadic congruence.

## A fixed cut on the actual register

If a pair receives the same positive outer count a, displaced digit d and inner count s on successive completed scans, it settles after at most two updates. A 22 is fixed. For the other three digits, adding s is a permutation of the three phases. Exactly one normalized phase can emit a ternary digit: 14 for d=1 or 2 and 21 for d=4. Hence at most one input ternary digit can survive. If it emits itself, it is fixed. If it emits a different ternary digit, that digit converts to 22 on the next scan. The first j pair positions can therefore settle within 2j updates from fixed root counts, provided they exist in aligned registers and the successive scans keep reaching them with a positive outer count.

There is a scalar check on any already steady pair. Set H = a+s−[d=1]. At a 22 the formulas give H′=2H. At a fixed ternary digit they give **3H′=H+2**. To see the second identity, use the value rule b+value(in) = value(out)+3·calls for b requests on a ternary digit. Apply it first to the s inner requests and then to the outer requests on a pair initialized at 21. The inner input equals the final outer digit at a fixed pair, so its value cancels. With d=1 or 2 the normalized inner digit is 14, the new displaced digit is 4 and the outer batch loses one initial request precisely on d=1. With d=4 the inner digit is 21, the outer batch loses one request, and the 421 reduction adds one inner call. Both cases give the displayed identity. In particular a ternary digit can persist only at H≡1 modulo 3.

From the [extension-33 checkpoint](neglected33-checkpoint.json), the next symbolic scan already emits its first **7,242** pairs unchanged. Only indices 62 and 3,078 (zero-based) are ternary, respectively 14 and 24. At their full prefix's right cut the displaced digit is 2 and the outer and inner counts have bit lengths 7,237 and 7,177. The next pair, 14, emits 22. The supplied check reads the complete stored tape and verifies every pair update and scalar identity. Thus on each subsequent ordinary extension the same fixed prefix can be stripped, leaving the same pair of exact counts acting on the evolving suffix. Those large positive counts do not furnish a fixed-cut proof of termination or nontermination.

## Why the exact number of outer requests matters

A counterfactual experiment preserves one prepend per stage and uses the same positive batch size at every stage. Start with the actual extension-3 y = 2221421, but replace the single outer request by **four**. After two such stages the words are 222242421421 and 2222222222414211421. From the latter word the first A request of the next batch reaches B3 at coordinate 13, after 203 defined instructions with coordinate zero at the first digit. The first two batches used 76 and 688 defined instructions respectively, excluding prepending the digit. Thus even a constant rate and an unchanged order of operations allow a physical halt in this enlarged model. The actual blank driver always sends one request.

## Verification and next step

Run the following beside [reserve33.py](reserve33.py). It checks 864 two-count identities on complete output words, all four carry states, and 5,355 shifted batches. The latter comparisons include the full output and exact clock against single-copy substitution. Physical checks of the underlying F rules, full tapes and clocks are in the [main report](neglected33.md).

```sh
python3 reserve33.py
```

The next proof target is the cumulative number of terminal (1,0) outcomes relative to (4,1) outcomes, together with stages where the scan exhausts early. The three-state transition table applies to the actual most-significant ternary pairs, so the count must use their generated order. The theorem supplies no distribution for that order or stopping time.
