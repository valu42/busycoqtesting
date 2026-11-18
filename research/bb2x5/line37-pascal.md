# A Pascal recurrence at the right boundary of line 37

The machine `1RB2LA3LA4RA1LA_0LA3LB3RB1RB---` is line 37 in the November 3 dataset. Use the epochs of `prior_sweeps.py`. State A scans a blank directly to the left of a finite word over 1, 2 and 3. Symbol 2 opens a pair, 1 closes one, and 3 is neutral. A second unmatched closing in one sweep reaches the undefined instruction B4.

Every fixed distance from the right edge eventually belongs to a linear cellular automaton **if the blank computation continues**. Its update is Pascal's recurrence modulo two. The resulting boundary condition complements the [finite-prefix nonhalting criterion](line37-header.md). The community tracker lists this machine as cellular-automaton-like. The starting point here is the repository’s existing matching sweep. [Community classification](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved) · [Sweep implementation](prior_sweeps.py)

## One successful sweep

Index digits by their distance from the **right** end, starting at zero. The rightmost digit of every nonempty blank-orbit epoch is 2. It is an unmatched opening, so the return pass appends another 2. Let `s[j]` be the bit indicating that the opening at index j survives matching. Scanning the old word from right to left, begin with debt zero. A 1 increases the debt. A 2 decreases a positive debt, or survives when the debt is zero. A 3 leaves the debt unchanged.

Define the tape digit D(left,right) by this table.

| Left bit | Right bit | Digit |
|---|---|---|
| 0 | 0 | 2 |
| 0 | 1 | 1 |
| 1 | 0 | 3 |
| 1 | 1 | 2 |

If the sweep succeeds, the new digit at distance j, for 1 ≤ j < the old length, is D(s[j],s[j−1]). Indeed the outward pass leaves each survivor as a 3 and every other old data digit as a 1. An unmatched closing may trigger the one allowed guard reset. At that point all earlier openings already have partners and the reset fills this earlier data with 1s. Its extra wall and header lie to the left of the old data when words are aligned at their right ends. On the return pass a survivor 3 produces a carry of one and a nonsurvivor 1 produces zero. Applying the incoming carry from the left yields exactly D. The appended rightmost 2 gives the index shift in the formula.

Thus any given nonempty right suffix with terminal 2 has a deterministic next suffix of the same length through each successful sweep. This includes a sweep with a guard reset in its interior.

## Three-cell blocks

On odd epochs group the word in triples, starting at its right end. Call a triple complete for the recurrence when its digits in right-to-left order are (2,a,2), with arbitrary center a. Consider k consecutive such triples at the right end. Let a₀ denote the rightmost center. Put bᵢ = [aᵢ=2] and set b₋₁ = 1.

Each triple clears its own matching debt, with none transmitted to the next triple to its left. The three survivor bits, right to left, are (1,bᵢ,[aᵢ≠1]). After the next sweep the three corresponding digits from right to left are

| Position in triple | Intermediate digit |
|---|---|
| Right | 3 if the previous center aᵢ₋₁ was 1, otherwise 2 |
| Middle | 2 if aᵢ=2, otherwise 1 |
| Left | 3 if aᵢ=3, otherwise 2 |

Use a virtual previous center of 2 for the rightmost triple. At its right boundary, intermediate triple i receives matching debt [aᵢ₋₁=3], equal to zero for the virtual center. Its rightmost digit absorbs that debt if present. Its survivor bits are therefore (bᵢ₋₁,bᵢ,bᵢ). It passes exactly [aᵢ=3] units of debt leftward. These three facts also follow by checking the three possible centers in order from the right boundary.

After the second sweep the triples again have shape (2,a′ᵢ,2), with a′ᵢ = D(bᵢ,bᵢ₋₁). In particular, hᵢ = 1−bᵢ follows

    h′ᵢ = hᵢ XOR hᵢ₋₁,    h₋₁ = 0.

The formula gives the exact center digit, including the distinction between 1 and 3. In each phase let P denote the prefix strictly to the left of these k triples. Then the suffix can create zero additional unmatched closings on the odd phase and at most one on the intermediate phase. More precisely, if P has height H, the minimum height over the appended suffix is H at the odd phase and H−[aₖ₋₁=3] on the intermediate phase, including the cut itself. The guard therefore needs to be checked only on P and against this one explicit value.

## Every fixed triple joins

At epoch 7, after 151 elementary transitions from blank, the word in ordinary left-to-right order is `2221313222212`. Its first two triples from the right are (2,1,2) and (2,2,2). The rightmost bit h₀ is one and remains one.

Take any three cells T immediately to the left of a suffix covered by the recurrence. They can start with arbitrary digits. For a list of cells read from right to left, write F(T,s,d) for the output of processing them with a right-neighbor survivor bit s and incoming matching debt d. At each digit x, let u = [x=2 and d=0], output D(u,s), update d to max(0,d+[x=1]−[x=2]), and set s to u. If a is the center of the outermost triple already covered, two successive sweeps act on T by

    G(T,a) = F(F(T, [a≠1], 0), [a=2], [a=3]).

For any of the 27 choices of T, G(T,3) is one of (2,3,1), (2,3,2), (2,2,2). Applying G to any of these with any next input center returns a triple of the required shape (2,x,2). The exceptional intermediate triple (2,3,1) returns (2,2,2) with center 1 or 3 and (2,1,2) with center 2. The other two triples are already covered by the closure calculation. The verifier enumerates all 81 cases.

Whenever hᵢ₋₁ is one, hᵢ toggles. Starting with h₀ constantly one, induction gives infinitely many toggles at every subsequent covered site on an infinite orbit. At every toggle from zero to one, the old pair of b bits is (1,0) and D(1,0)=3. Thus each covered center with i≥1 takes value 3 infinitely often. Successful sweeps increase the word length, so eventually the three external cells exist. The next occurrence of 3 and one further update absorb them into the covered suffix. Induction beginning at epoch 7 proves the assertion for every fixed distance. Equivalently, each finite target suffix is reached or the machine halts first.

Once k triples are covered, their bit vector evolves by I+S over the field with two elements, where S shifts right-boundary bits one triple toward the left, inserting zero. Its minimal period, in pairs of sweeps, is the least power of two at least k. For a power p of two, (I+S)^p = I+S^p. For p≥k the shifted vector vanishes, while for p<k its bit at index p is h₀=1. Since the least period divides the first such power, these tests establish minimality. The full centers also have that period after one update since they are determined by the previous bit vector and determine the current one.

The period also bounds the time to absorb another triple. With k≥2 triples covered, the outermost center takes value 3 among the next p updates, where p is the least power of two at least k. Two more updates suffice to absorb the next triple even from arbitrary digits. Three spare cells exist at the epoch-7 seed, and each pair of successful sweeps adds at least four cells. Thus for any K≥2, by epoch 7 + 2·Σ( p(k)+2 ), with the sum over 2≤k<K, either a halt has occurred or at least K triples have joined. This gives a quadratic worst-case time bound in K.

Run `python3 line37_pascal.py` in this directory. The checker uses the literal tape interpreter for the first 32 blank epochs, checks the suffix update on every successful word of length at most seven ending in 2, and verifies the finite triple rules. At epoch 1001 it finds 372 complete triples covering 1,116 of the 2,271 digits from blank.
