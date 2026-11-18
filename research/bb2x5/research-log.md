# Four BB(2,5) holdouts · 18 November 2026

I did not decide a blank-tape machine. Two new reductions narrow the question on lines 26 and 2. For line 26 a three-integer recurrence gives an exact inequality equivalent to halting. For line 2 a fixed boundary replaces the entire growing negative part of the tape. The remaining two sections record obstructions to proposed proofs on lines 17 and 10.

The numbers in this report are one-based **positions in the formal file**. Its 37 strings are distinct. Each row is in read-symbol order 0,1,2,3,4. The initial head is in A at 0 on a two-way infinite zero tape. A transition writes the specified digit, moves once and enters the specified state. Arrival at an undefined entry halts. The public wiki credits mxdys for the November 3 formal list. I found no subsequent public decision for these four exact encodings in the sources checked on November 18. The community tracker credits mxdys with the two-overflow analysis on line 26. The wiki records Racheline’s overflow-counter analysis on line 17. This report extends the earlier pair and frontier calculations in this investigation. Priority over unpublished analysis is unknown. [Formal dataset](https://wiki.bbchallenge.org/wiki/Holdouts_lists#BB(2,5)) · [Status and prior analyses](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved) · [Community tracker](https://docs.google.com/spreadsheets/d/1qiZ3PJb_q4j9kddm0zZMionJhYCI_uEHr1bSmsBOlZs/edit) · [Racheline's machine](https://wiki.bbchallenge.org/wiki/1RB2RA3LB---2LB_2LA0LA4RB0RB1LA)

| Formal line | Established in this round | Remaining obstruction |
|---:|---|---|
| 26 | Exact three-integer overflow test and a quantity that cannot increase between enlargements of the tape | Comparing the counter with its capacity when the tape grows |
| 2 | Exact fixed-cut requests, a 2,400-extension blank checkpoint and restrictions on exceptional returns | Which requests eventually return A, halt internally or run forever |
| 17 | An unconditional post-overflow disjunction and a conditional 242-step halt compatible with 32 genuine periods | The continuation of the specific periodic stream through 350 identical digit pairs |
| 10 | An exact recurrence for the cyclic periods at all reachable distances | Which cyclic starting position the blank run selects |

## Line 26 · one inequality decides a finite halt

**Encoding** `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA`. The only undefined entry is B3. Start the following total arithmetic process at (u,e,m)=(0,0,0) and apply the letters of (aadd) repeatedly. Bit positions are numbered from zero, least significant first. The blank machine halts **if and only if** a cycle ends with e ≥ 2ᵐ. This section gives the derivation and the remaining mathematical question.

### The tape and its two trips

After five defined steps the head is A at −1 with the word 43 in cells 0 and 1. More generally an epoch starts with A at −n, n ≥ 1, followed immediately by n copies of 4, then m pairs of digits from {1,4}, and one terminal 3. Both exterior tails are blank. Within each data pair write o and v for its first and second bit, coding 1 by 1 and 4 by 0.

A0 on the blank writes 1 and sends B right. Starting with B at the first cell of an aligned pair, the following table gives its action. A rightward exit calls the next pair in B, and the return from it is in A.

| Pair | Suspended pair before going right | Pair after returning left in A |
|---|---|---|
| 11 | 42 | 14 |
| 41 | 32 | 41 |
| 44 | 22 | 44 |
| 14 | Turns immediately | 11 |

The forward paths through these rows use B1 A1, B4 A1, B4 A4 A3 A1, and B1 A4 A4 respectively. On return, 42 uses A2 A4, 32 uses A2 A3 A4 A2, and 22 uses A2 A2. A terminal 3 in the first position of a pair gives B3. In the second position, 13 becomes 1443 and 43 becomes 4143. After B on the first position both paths use A3 A0 B0 A1 B2 A2 A2. The return across the first position takes A4 for the first case or A3 A4 A2 for the second. At the left guard the first trip returns to A1, which writes 2 and sends B again. The second returns to A2, which writes 4 and moves left onto a fresh blank. Thus every trip over the finite word takes positive, finite time and either stops at the stated undefined entry or finishes its return.

When n is even, the trip enters each data pair in its first position. It increments the second bits whose first bit is 1 in least-significant-first order. Call this carry d. When n is odd, the alignment shifts by one. It increments the first bits whose preceding second bit is 1. Carry a denotes a preceding bit of 0, and b denotes a preceding bit of 1. A cell reached by a surviving safe carry sends its own second bit as the type of the next carry. The preceding bit at the start is 0. Each epoch makes two identical-parity trips and increases n by one. The source therefore sends a,a,d,d in that order, repeatedly.

For d at a column with o=0, pass d unchanged. For o=1 toggle v, passing d exactly if the old v was 1. For a or b, toggle o on b alone. Emit the old v as a or b whenever the input was a or the old o was 1. Otherwise the carry stops. These rules also follow by substituting the four physical pairs in the table. A fresh column reached by d halts. A fresh column reached by a or b consumes the carry and extends the data by one pair with (o,v) equal to (1,0) or (0,0), respectively. These extensions are precisely the terminal cases 43 and 13 at the shifted alignment, retaining the preceding digit.

### Two integers for the column bits

Set uᵢ=1−oᵢ and eᵢ=vᵢ. Pack each into a nonnegative integer with zero bits at positions i ≥ m. This convention allows the formulas below to continue beyond a hypothetical halt. Up to the first overflow they give the concrete column configuration after every trip.

* On d, choose the least index k with uₖ=eₖ=0. Toggle the bits eᵢ for i ≤ k at which uᵢ=0. Leave u and m alone.
* On a, put s=2e. If u and s share a set bit, take the least such index k and toggle in u the bits selected by s through k inclusive. Leave e and m alone.
* If u and s have disjoint set bits, replace u by u OR s and increase m by one. Leave e alone.

For d the selected low bits are a binary increment with carry. At k=m the concrete machine instead reaches B3, and the arithmetic model sets bit m of e. Earlier flips stay below m. For a, a continuing carry arrives at column i as b exactly when i>0 and e at i−1 was set. Thus s lists all positions at which u is toggled. The first selected u-bit equal to 1 stops the carry. When there is none it reaches the fresh column and m increases. At the old m its type is b precisely when bit m of s is set, which writes exactly the new high bit of u in the last rule. This proves the correspondence by induction on the trips. On d the new e strictly exceeds the old e. The two consecutive d operations in a cycle use the same m, so checking the inequality at the cycle end captures an overflow on either trip.

There is a shorter cycle formula. At cycle boundaries u=4U and e=2E. Put S=E with its lowest set bit cleared, taking S=0 if E=0. Decrement U on the positions selected by S. In other words, toggle selected positions through the first shared 1, or set all selected bits if there is none. In the latter case increase m by 1, or by 2 if E=0. Next increment E on positions outside the mask 2U, using the **updated** U. To prove the compression, two decrements on one selector leave its lowest selected bit unchanged and borrow once into the remaining positions. With an empty selector both a's extend. Two d increments skip position zero, which always has u₀=0, and increment once through the remaining eligible bits. Starting from zero this proves the stated divisibilities as well. In this representation the test is 2E ≥ 2ᵐ.

### What can already be proved for all time

In the total arithmetic recurrence e increases on each d and stays fixed on a. Indeed its highest changed bit goes from 0 to 1. Hence e is unbounded. Also m grows without bound. If m did not increase again after some time, each subsequent a would strictly decrease u, because its highest changed bit would go from 1 to 0. Each d leaves u unchanged. This is impossible for a nonnegative integer and infinitely many a's. Quantitatively, from any state at most u+1 more a's are required for another increase in m.

A stronger bound holds between successive increases of m. In the paired coordinates put V=E+U². On a cycle that does not increase m we have U′<U. The increment of E outside the mask C=2U′ is exactly 1+(C modulo 2ᵏ), where k is the least index with Cₖ=Eₖ=0. In fact only the unblocked ones below k are cleared. Hence E′−E≤1+2U′≤U²−U′². This proves that **V does not increase during a run of cycles with m fixed**. If 2V<2ᵐ at a checkpoint, every remaining cycle at that same m is safe, however many cycles it takes for m to increase. At the 131,072-cycle checkpoint V=13,708,448,235,655,927,296, below 2⁷³. The stronger condition is not an invariant at increases of m. Already at cycle six, (U,E,m)=(10,10,7) gives V=110>64, even though the run is safe.

These arguments do not order the two growth events. For example the alternative external word adad reaches e=2ᵐ at its fourth token. Repeating ad still makes m unbounded by the same proof. The machine supplies aadd. For that source I checked the inequality at every trip through 131,072 four-trip cycles, where (u,e,m)=(14,809,968,640, 81,588,923,392, 74). A forward search recording only short consecutive groups of column states also admitted dangerous carries after merging different configurations. I have neither an induction proving e<2ᵐ at every cycle nor a violating cycle on the real source.

## Line 2 · an exact left half and the origin of exceptional returns

**Encoding** `1RB---4LB0LA4RA_2LB2LA3RA4LB0RB`. The only undefined entry is A1.

| Read | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| A | 1RB | halt | 4LB | 0LA | 4RA |
| B | 2LB | 2LA | 3RA | 4LB | 0RB |

A request in state Q at a fixed cell enters from its left, and stops on the first step leaving that cell to the left. The response is the exit state. A request into the adjacent cell on the right will be called a child request. A finite returned request is one uninterrupted piece of elementary execution. It may also encounter A1 or run forever.

### A fixed cut replaces all visits to the negative half

Condition on the first n successful left extensions. At the next epoch the head in A scans the virgin cell −n, and cells −n+1 through 0 contain the first n symbols of (242) repeated indefinitely. The unknown right half starts at coordinate 1. The claim holds for n=0 on blank.

A0 writes a temporary 1 and sends B across this prefix. On a full triple 242, B on the first 2 sends A onto 4, A4 sends A onto the last 2, and A2 returns in B. B4 sends B onto the last digit, now 4, and another B4 sends B rightward, leaving the triple 300. A B response crosses 300 as B0, B0, B3, restoring 422 and exiting left in B.

Write n=3k+r. After the k triples the residual prefix is empty, 2 or 24. The empty prefix transmits B to the fixed right half. On residual 2, B2 sends A to it. A B response crosses B3, leaving 4 and exiting B. On residual 24, B2 sends A onto 4. Each A response at that 4 launches A again until a B response arrives. B4 then makes one B request. A B response here crosses B0 and B3, leaving 42 and exiting B. A completed A-to-A request always leaves its initial cell equal to 2, as the table in the next section shows. Thus the first A of this residual can require at most one retry, which executes A2.

In the normal cases B1 at the guard writes 2 and steps left in A. The new prefix is a leading 2 followed by k copies of 422 and the residual output (empty, 4 or 42). This is the required prefix of (242) of length n+1. Induction proves that the fixed cut sees **B, A, A with a possible retry, B** every three successful extensions. Only the second A of these four requests permits that retry.

The failure cases can be decided as far as any required suffix response. An A response to the first A of the four is sufficient for finite halting. B2 in the residual left a 3, so A3 leaves 0 and exits left in A. If this reaches the guard, the machine halts. Otherwise it enters the last cell of the next suspended 300. The complete handler for A entering 300 is as follows.

1. A0 on its last digit sends B to the right. An A response now hits its 1 and halts.
2. A B response writes 2 through B1 and moves left in A onto the middle 0. A0 there sends B onto the last 2. B2 sends A right. If A returns, A3 erases the last digit and A meets the middle 1, halting.
3. A B response instead crosses B3, B1, A3. It leaves 024 and exits left in A. When the suffix begins with a zero, the two requests in this handler are just B0 then A2 on that one cell. Both return B. Each successive enclosing 300 therefore releases another A to its left in finite time. A reaches the guard 1.

In the first-A failure the erased residual already provides the required zero, so none of these handlers calls the unknown suffix again. For an A response to the first B of the four, n=0 halts at once. For k>0 the innermost 300 demands the diagnostic B and possibly A above from the suffix. For an A response to the final B of the four, the residual 24 has a 0 suspended on its right. A0 sends one extra B to the suffix. An A answer halts at its 1. A B answer crosses B1 then A3, leaves a leading 0, and the enclosing handlers terminate at the guard. Divergence inside any demanded call remains divergence of the original execution.

The direct two-way interpreter reaches A at −2400 after exactly **27,064,000 defined steps**, with (242)⁸⁰⁰ up through coordinate 0. Its rightmost visited cell is 3979. An independent simulation at the fixed cut gives the identical 3979-cell right tape, with one flexible retry in the very first cycle. A later A1, an indefinitely running right request, and indefinite successful extension are all still possible.

### Which tapes an A response can leave

For a right half initially consisting of a finite word over {2,4} followed by virgin zeroes, every completed request begins its next request with 0, 2 or 4 on its initial cell. To see this, work from the elementary table.

* On 0, B writes 2 and exits B. A calls B, leaving 1. An A response halts, and a B response writes 2 and exits A.
* On 2, A writes 4 and exits B. B sends A to the child. A B response leaves 4 and exits B. An A response leaves 0 and exits A.
* On 4, A first sends A until it receives B. B on 4, whether initial or reached this way, writes 0 and sends B. A B response leaves 2 and exits B. An A response launches a second B through A0. A second A response halts, and a B response leaves 2 and exits A.

These statements describe chronological paths including all intermediate instructions. They imply that every completed A-to-A request leaves 2 in its first cell. In particular a retry in the first clause for digit 4 finishes through A2.

Let b(w) be the resulting right tape if a B request on w returns B. Define the partial operation F(w)=2 followed by b(w). Define G(w)=22 followed by w. Regard all words as having an infinite zero tail. Let D be the smallest family containing 22 and closed under G and every defined F. Every completed A-to-A request leaves a word in D. Every completed B-to-A request leaves either a word in D or 0 followed by a word in D.

For the proof, induct on the number of elementary transitions elapsed at the response, including responses to nested requests. A virgin A0 has a virgin child whose B0 immediately returns B, so it leaves 22. A previously used cell beginning a request on 0 could have acquired that normalized 0 only by a B request on 2 whose child returned A to A. Its tail is then in D by the induction hypothesis and cannot change before this cell is reentered. A successful A-to-A request on this 0 therefore leaves F of that tail. A B-to-A request on 2 leaves the same kind of tagged word 0D. Finally, a return in A from an initial 4 used a child B-to-A return followed by a B-to-B return. If the child's first result was w in D the outer word is F(w). If it was 0w, the second B is B0, and the outer word is G(w). This exhausts all completions and requires no assumption that all requests finish. The initial clean-word condition rules out a preexisting interior zero with arbitrary data to its right.

The tempting strengthening that B always returns B on D is false. From 22, apply G,G,F,F in that order to obtain **24244442**. Its next B returns **A after 125 elementary steps**. The existence of this word in the overapproximation gives no blank run reaching it. There is also a physical restriction on directly propagating an A response from a virgin cell j≥1. Suppose the virgin A at j returns 22 and two cells to its left produce G(22) by the tagged branch above. The request at j−2 that produces this G must have entered in B. If it entered in A, the 4 there would first need a completed A-to-B request at j−1 leaving 2, immediately before sending B there. Only an A request starting on 4 at j−1 can leave 2 and return B. That request would already have visited j. This contradicts virginity. Thus taking generators independently loses a constraint from the nested call history.

### A uniform period theorem for ordinary cells

Under the condition that all child responses are B, a 2 or 4 toggles on every request and always returns B. Encode 2 as phase 0 and 4 as phase 1. In phase 0 the child word is empty on A and A on B. In phase 1 it is AB on A and B on B. An input word therefore acts on an array of n bits, updating the first phase and sending the child word down the array. The map is a permutation by induction on depth, since the root either keeps or flips its bit and the child actions are permutations.

If the length of the input word is odd, every orbit on n bits has length 2 raised to ⌈n/2⌉. If both letter counts are odd, every orbit has length 2 raised to ⌊n/2⌋. At n=0 both assertions give 1. In the first case the root flips. Across two traversals each occurrence sees both phases, and contributes one A and one B to the combined child word. Its two counts are therefore both odd. The root must make a pair of traversals to return, after which induction applies to the child. In the second case the root stays fixed. On A the length emitted is even and on B it is odd, independently of phase. The one-traversal child word thus has odd length. Induction applies without the root doubling. This establishes the orbit lengths at every width. The first virgin A-to-A return already falls outside the ordinary response hypothesis.

## Line 17 · the next branch reads two bits

**Encoding** `1RB2RA3LB---2LB_2LA0LA4RB0RB1LA`. The earlier concrete checkpoint at step 2,308,940 has 424 data digits. Its established finite counting phase reaches virgin coordinate 12 in B, then after 55 more instructions A is at −1 above an unknown symbol s. At the cut before zero-based digit 418 the incoming binary mark stream starts 01000000, and successive marks are separated by at least three slots. Positions within this stream are numbered from 1. Marks trigger the bursts in the earlier pair transducer. The included function right_events explores the remaining six literal tape pairs up to the first right extension, branching whenever the mark spacing allows it.

| Mark at slot 9 | Mark at slot 10 | s |
|---:|---:|---:|
| 1 | 0 | 1 |
| 0 | 1 | 0 |
| 0 | 0 | 4 |

Mark spacing forbids marking both positions. Conditioning the finite exploration on each row gives exactly the singleton shown. A branch at this cut is still a conditional statement about the blank orbit.

The finite exploration can be moved two cuts farther left to obtain an unconditional statement on the blank execution. At cut 415 the known initial marks are 0000001000. Explore triples consisting of the actual tape suffix, the incoming pending-burst bit and the mark cooldown, also tracking progress through the known prefix. A permissible next bit determines a raw U or C pulse. Execute it on the suffix up to return or first crossing into cell 12. This exhausts 411 pre-crossing states and 32 distinct suspended words. From B at 12, literal execution on each word reaches −8 without encountering A3. The 29 exits in B take 62 to 126 steps after the visit to 12, and the three exits in A take 132 to 200 steps. Counts in this paragraph are counts of distinct suspended words, with no probabilistic interpretation.

At cut 414 the known prefix 010001000 gives 1,352 pre-crossing states and 71 suspended words. Sixty-two exit at −10 in B in 64 to 152 steps, and seven exit there in A in 134 to 338 steps. The other two halt on A3 at −4. The exact 21-symbol words in cells −9 through 11 at the first visit to 12 are `040242440444040444444` for the 242-step halt and `040244044444040444444` for the 288-step halt. Within the reachable enlarged set this is a necessary and sufficient test for halting before −10. Thus the actual blank execution has reached −8 within 200 steps of its first visit to 12. By 338 steps it has either visited −10 or halted at −4. These searches only use the proven cut prefixes from the earlier digit calculation. The verifier exhausts all reachable finite states of each enlarged problem and checks every resulting raw path. A B exit has visited at most 12 and an A exit has also visited 13.

There is a constructive obstruction even across arbitrarily many intervening homogeneous pairs. For a digit beginning with trit 1 and no pending burst, start the marks at slot 5. The first four ordinary inputs give one output and reach trit 2. At a mark with trit 2, the three consecutive burst inputs emit 00, 01, 0. The mark in this output is penultimate. If the distance D to the next start is a multiple of three and D≥6, the intervening ordinary slots restore trit 2. The corresponding output gap is D/3+4. Thus an output gap g≥6 can be prescribed by input gap 3g−12. Across k such digits use input gaps 6+3ᵏ(g−6). This also preserves any fixed initial number of gaps equal to 6.

At cut 403, specify starts at 5,11,17,23,29 and let subsequent gaps be constantly 6, 13 or 17. Pass each stream through the 15 actual digit states 403 through 417. The initial ten bits at cut 418 become 0100000000, 0100000001 or 0100000010, giving s=4,0,1 respectively. The gap construction pulls each example back through the 350 intervening homogeneous cells. The mark at 29 is chosen in this construction. Only 5,11,17,23 were proved at cut 403. At cut 53 the actual fifth mark is at 27. The cut-53 stream on blank is a specific periodic sequence with least period 147,740. Its two decisive descendant bits remain unknown.

One such continuation actually reaches the undefined instruction without ever returning to the left of cut 403. Keep the same first five marks and set the gap after slot 29, and every subsequent gap, to 56. Slot 6,513 at cut 403 first sends B into coordinate 12. For comparison, one sufficient input prefix at cut 412 is `01000010000000100100100`, with marks at positions 2,7,15,18,21. It selects a halting branch before the machine exits that slice. At that instant the 43 cells from cut 403 through the old terminal read `4444444444040444444404040242440444040444444`. Starting with B at 12, exactly 242 defined steps later the machine is at −4 in A scanning 3. This is a literal halting branch with no dependency on the tape to its left during those 242 steps. The preceding gap construction also gives compatible upstream inputs through all 350 homogeneous pairs. Whether the specific periodic input arising from the blank checkpoint produces a halting branch remains unresolved.

### Matching the first 32 genuine periods

The preceding witnesses can be strengthened to agree with the actual cut-53 stream on its **first 4,727,680 slots**, including the fifth mark at 27. This is a result about arbitrary continuations of a finite prefix. The exact period repeating forever at cut 53 excludes the constructed continuations.

Here is an event calculation which avoids enumerating the very long gaps. At a homogeneous digit, q ordinary inputs from trit v emit ⌊(v+q)/3⌋ zeros and leave trit (v+q) modulo 3. A mark at time t from trit v starts a burst of v+1 inputs, ending at t+v. It emits 2v+1 slots. When v>0 its one output mark is at position 2v within this block. The trit at the end is 2. Since valid marks have spacing at least three, later input marks cannot disturb these results. In particular, marked descendants of any finite initial list can be calculated without knowing the next mark.

Take the 590,976 marks in 32 copies of the genuine cut-53 period. After 35 homogeneous digits, the descendants of these specific marks are exactly 5,11,17,23. At each of those 35 layers retain the index L of the last input slot of the last burst and the total number B of output slots through that burst. This finite calculation is reproduced in mark_prefix.py.

There are now 315 homogeneous layers left, starting at cut 88. Add a fifth mark there at distance 6+5·3³¹⁴ from mark 23. In the next 314 layers its distance is successively contracted by D ↦ D/3+4 until it is 11. At the last layer a gap of 11 from a trit-2 mark makes the next marked burst start at trit 1. Its output gap is 6, putting the fifth mark at slot 29 of cut 403.

To prescribe subsequent gaps g of 6, 13, 17 or 56 at cut 403, use constant gaps 3g−8 after the fifth mark at the input of the last layer. Each later burst then starts at trit 1. After its two burst slots, the number of ordinary slots until the next mark is 3g−10, and those emit g−3 zeros. Counting the trailing zero after one emitted mark and the first two slots of the next burst gives the output gap g. Pull those input gaps back through the other 349 layers by D ↦ 3D−12, each time using trit-2 bursts. Hence every gap following the added cut-53 mark can be the constant 6+3³⁴⁹(3g−14).

It remains to place the first added mark at cut 53 without disturbing the already specified 32 periods. Pull its desired position X at cut 88 backwards across the 35 stored pairs (L,B), in reverse order. Put j=X−B−4 and replace X by L+3j+1. This schedules 3j ordinary inputs after the last burst, then starts the new burst at trit 2. Its output mark is exactly at B+j+4. Direct integer evaluation gives j≥1 at every layer and a final X greater than 4,727,680. All intervening unmarked slots of the prescribed 32 periods are thus respected. The checker independently propagates the 590,976 known marks followed by 120 of the constructed marks through all 350 digits for each g. For g=56 the 120th added mark reaches past slot 6,513 at cut 403, so the previously exhibited concrete halt is already forced. The other gaps give the three different edge symbols.

## Line 10 · exact periods lose the distinguished starting point

**Encoding** `1RB2RB3LA4LA1LA_2LB3RA---4RA1RB`. The earlier edge test halts precisely when three A entries precede the first B on a fresh edge initialized to 3. At coordinate 3 the true input is (BAA) repeated. Ordinary occupied cells cycle through three phases. An A increments phase and emits B only from phase 0. A B decrements phase and emits A from phase 0 or 1, and BB from phase 2. Upon a successful extension, the edge consumes its opening B, AB or AAB, then transforms the remaining periodic stream through one or two ordinary cells with known initial phases.

Write a,b for counts in a period representative. For (BAA) these are (2,1). Whenever they are congruent to (2,1) modulo 3 the phase advances one position per traversal. During three traversals each input occurrence visits every phase. The output counts are therefore (2b,a+2b), again congruent to (2,1) modulo 3. Starting in another phase rotates the output period because the three traversals contain all phases. Rotating the input has the same effect up to an initial choice of phase, which is already immaterial to the cyclic word. Consuming an initial finite prefix before transforming the stream also only rotates its period. Induction over physical cells gives a cyclic representative independent of the successful extension choices. Its lengths satisfy L₃=3, L₄=6 and Lₓ₊₂=2Lₓ₊₁+2Lₓ. No minimality of the representative is needed for this conclusion.

At coordinate 15 the representative has length 409,152. Counting cyclic starting positions with multiplicity gives 19,024 that begin AAA, and 1,023 distinct ten-letter factors out of the 1,024 possible. AAA occurs already in the coordinate-5 period, though the actual run safely passes that edge. The obstruction is the specific starting position chosen at successive edges.

## Reproduction

Run the following from the extracted directory, with ordinary Python assertions enabled.

```sh
python3 verify.py
```

The checks succeeded using Python 3.12.14 and its standard library. The transcript is in verification.txt. The companion frontier-background.md gives the derivations of the earlier line-17 checkpoint, mark dynamics and line-10 edge test. The two prior Python modules provide the literal tape semantics, pair/column checks and mark tables used by the new verifier. The packed counter is compared against the independent column model on every digit word through four columns and against concrete tape epochs on the real machine. The line-2 literal run uses no macro transitions. The branch checks on line 17 are finite exhaustive searches over an enlarged set of inputs. No Rocq blank-tape theorem was produced.
