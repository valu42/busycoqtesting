# Postponing a single safe edit in machine 31

The blank verdict for `1RB3RB---4RA2RA_2LA2RA3LB4LB1LB` is open. Let $P=\mathtt{AABAA}$ be its repeating physical root input. Number requests from one. Change a single A to B and retain the genuine infinite schedule thereafter. Editing request one gives literal A2 at the origin on request two. For any other eligible request $n$, let $S_n$ be the edited word with the three preliminary As used in the [fourth-letter reduction](line31-phase.md#deriving-the-transformation). These are experiments on the positive half with a supplied driver.

**Unbounded safe edit dates would prove blank nonhalting.** A hypothetical blank halt would happen during a finite root request. Every edit after that request would agree with the genuine run up to the halt. The evidence below gives six safe dates, an exact rule for postponing them, and halting counterexamples to iterating that rule without a further hypothesis.

## Which edits reach the fixed stream?

Write $C=\mathtt{AAAABBA}$. Its infinite repetition is fixed by the two-cell map $F=T_2\circ T_0$. The following edits reach $C^\omega$ with fourth letter A on every previous iterate.

| Request changed | 2 | 4 | 46 | 104 | 211 | 246 |
|---|---:|---:|---:|---:|---:|---:|
| First fixed iterate | 2 | 4 | 9 | 9 | 11 | 11 |

The witnesses compare complete infinite words. To compute $T_p(uv^\omega)$, transform the finite prefix $u$, then transform one or three copies of $v$ from the resulting phase until it returns. Reduce the periodic part to its shortest period and move its start left as far as its letters allow. The comparison respects the origin. As a control, the same substitution at request 36 reaches literal A2 at +34 on request 5,386.

**These are all the safe captures through iterate 32, for edits at any date.** For each even cut through +64, feed the genuine word until its finite history first disagrees with $C^\omega$. The last such disagreement occurred on request 6,728,465. Any later edit preserves a mismatch at every one of these cuts. For every eligible date up to and including that request, the checker branches from the genuine phase and history of every cell, feeds B, and resumes the periodic driver. A single mismatched output letter excludes equality at its cut. Acceptance requires an entire verified periodic tail and every earlier fourth letter A. A finite sample that still matches is retried with a larger budget. At this depth zero cases remained undecided. Captures deeper than this and infinite safe orbits outside this fixed stream remain possible.

## An exact rule for shifting the edit

After the preliminary As, the ordinary cell phases are $0,0,2,2,1,1$, followed by repeating $0,2$. No preliminary letter reached +6. For an even $x\ge6$, let $K_x$ be a number of genuine five-request groups returning all phases below $x$ to their starting values. Let $Q_x$ be the complete word emitted into cut $x$ by those groups. The checker builds $K_x$ by taking one input period when the current phase closes and three otherwise.

For every eligible $n$ and every $k\ge0$,
$$F^{x/2}(S_{n+5K_x k})=Q_x^k F^{x/2}(S_n).$$

Indeed, delaying the edit prefixes its physical source with $k$ copies of $P^{K_x}$. Each copy emits $Q_x$ and restores every upstream phase. The original edited source then starts from exactly the same upstream state. At $x\ge6$ there is no preliminary word ahead of the inserted copies. For the cuts used below, one genuine block already supplies fourth letter A at every earlier even cut, as the checker verifies.

Two actual coincidences help explain the safe dates. Juxtaposition of a finite prefix and a parenthesized repeating block specifies the whole stream.

* Edits 4 and 46 reach the identical stream $\mathtt{AA}(\mathtt{AAAAB})^\omega$ after one and six applications of $F$, respectively.
* Edits 211 and 246 reach $\mathtt{AAAABAAAA}(\mathtt{AAB})^\omega$ after seven applications. Thus the two dates $211+98{,}415k$ and $246+98{,}415k$ have the same verdict for every $k\ge0$. This follows from the shift rule at +14. Request 281, another 35 later, has a seventh iterate with primitive period 544. Moving the original pair forward one complete return gives edits 98,626 and 98,661. Both halt at +68 on physical request 1,301,444 into +14.

At +22 all six base edits have reached $C^\omega$. Here $K_{22}=1{,}594{,}323$ and $|Q_{22}|=74{,}190$. Consequently **all six dates shifted by the same $7{,}971{,}615k$ have the same verdict**, determined by the single input $Q_{22}^k C^\omega$ at +22.

| Shift trial | Outcome of the altered driver |
|---|---|
| Move edit 2 to 407 by one complete return below +6 | On physical root request 23,727, A2 occurs at +38. This also replays directly from the supplied root letters. |
| Add 7,971,615 to each of the six dates ($k=1$ at +22) | All six halt at +134. The finite prefix at +132 begins with physical ABABAA. The triggering physical request into +22 is 280,522,975,080. |
| Add 15,943,230 to each of the six dates ($k=2$ at +22) | All six halt at +136. |
| Add 23,914,845 to each of the six dates ($k=3$ at +22) | All six halt at +80. Replaying the literal instructions from a virgin suffix at +22 gives A2 on its physical request 2,082,606. |

For the $k=1$ clock, the fourth aligned letter at +134 appears on the 280,522,900,893rd letter of the fixed tail. Adding the initial $74{,}190$ letters and removing the three preliminary As gives the stated request into +22. The two replay commands below bracket this arrival by a single letter. These halts use the edited sources.

### Every whole-period shift through cell +100

**Exactly 29 positive values of $k$ produce a halt at or before +100.** The table gives the first failing cell for each. The largest exceptional $k$ is 383. At every $k\ge384$, all six altered drivers clear +100.

| First A2 | Values of $k$ |
|---:|---|
| +80 | 3 |
| +84 | 15, 18, 23, 28–31, 34–38, 42–47, 49, 55 |
| +86 | 33 |
| +92 | 26 |
| +94 | 50 |
| +96 | 7 |
| +98 | 188 |
| +100 | 110, 339, 383 |

To cover the infinite range of $k$, first feed only the true prefix $Q_{22}^k$ at +22. At $k=1{,}216$, all even cuts through +100 have already received their fourth A. Every longer prefix retains these entries. The checker compares $Q_{22}^k C^\omega$ separately for $1\le k<1{,}216$. For each case it either observes a fourth B, verifies a fourth A through +100, or proves exact equality with the fixed stream. Zero cases ran out of tail letters. The same argument restricted to +80 needs only 15 complete periods, and $k=3$ is its sole exception.

An independent replay of the literal tape instructions opens +100 in state A on physical request **90,190,513** into +22 for $k=1{,}216$. For the last exception, $k=383$, the tape instead reaches the undefined A2 at +100 on request **231,475,923**. For $k=7$ it reaches A2 at +96 on request 80,748,812.

There is an infinite set of shifts with a known finite guarantee. For every $k\ge 46{,}490{,}459{,}308$, all six changes occur after the [blank checkpoint](frontiers/runs/line31-phase.json). Indeed, $K_{22}=3^{13}$ and the checkpoint covers $40\cdot3^{32}+10^9$ root groups. All these shifted drivers have therefore cleared every possible halt through +180 before the edit takes place. Their behavior from +182 onward is open.

### When one capture would decide the blank run

**A single sufficiently late capture could settle the blank machine.** Suppose an edited stream safely reaches $C^\omega$ at cut $x$, and the genuine input before the edit has already emitted $|Q_x|+7$ letters there. The two streams agree on this entire prefix. In particular the seven letters starting at index $|Q_x|$ repeat the first seven, so rotation by $|Q_x|$ preserves $C$. Its primitive length is seven, hence $7\mid |Q_x|$. The first $|Q_x|$ letters now show that $Q_x$ is a power of $C$ and the entire genuine stream at this cut is fixed. All upstream fourth letters have already arrived, and agree with the safe edit. For $|Q_x|\ge7$, a certified capture with $n>10K_x$ would meet this finite test.

A second capture at the *same cut* after delaying by a positive whole return would itself decide the genuine machine. Equality $Q_x^k C^\omega=C^\omega$ forces the genuine stream $Q_x^\omega$ at that cut to be $C^\omega$. Thus a search that succeeds by reaching the fixed stream farther and farther to the right needs control of the inserted word as it passes through additional cells.

There is also an obstruction independent of any search depth. Suppose a proposed rule takes two unbounded sequences of dates $a_i,b_i$ tending to infinity and gives $F^{d_i}(S_{b_i})=S_{a_i}$ with $1\le d_i\le D$. Some fixed $d$ occurs on an infinite subsequence. Each $T_p$ emits at least once per three inputs, so finite prefixes of $F^d(w)$ depend continuously on finite prefixes of $w$. Both edited sequences converge to the genuine seed $S$, forcing $F^d(S)=S$. But $S$ differs in just its first letter from a purely periodic word, while $F(S)=(\mathtt{AAAABAAABB})^\omega$ is purely periodic. Every further iterate of a purely periodic stream stays purely periodic. This rules out a bounded-step recurrence returning to the root form of the edited words. The bridge at +14 compares two transformed words and avoids that obstruction.

## When can the moved B restore the comparison phases?

The uniform genuine seed differs from $V^\omega$, $V=\mathtt{BAAAA}$, only at its first letter. An A-to-B edit consequently moves the first B of the comparison to absolute letter $n+3$. At edit 2 both five-letter histories, AAAAB and BAAAA, leave exactly the same vector of ordinary phases on the infinite strip.

One plausible way to repeat this is to require the phases of the edited and comparison runs to agree again at the same absolute time immediately after the edit. **Agreement through the first 59 ordinary cells occurs exactly when**
$$n\equiv 2\pmod{5\cdot3^{34}}.$$
The first later date satisfying this test is 83,385,908,498,332,847. It is a necessary test for exact phase restoration. Five of the six safe edits already show that a run can reach the fixed stream by other routes.

There is an infinite construction for agreement on finite strips. For any width $h$, let $M$ be a common multiple of the two group-return times below that cut. Then edit $2+5M$ restores agreement on all $h$ phases. These dates can grow without bound. The matching phases describe the future after the moved B. They leave the first four entries already delivered to each cut unconstrained. Even the edit at 407 matches the first six phases and later halts at +38.

In fact a phase-only test can lose a halt inside the very strip it checks. Start after the same three introductory As and compare the supplied physical drivers $(\mathtt{ABABAA})^\omega$ and $(\mathtt{ABBAAAA})^\omega$. The first halts at +2 on request six, and the second is a proved safe cycle. In the ordinary word model, any root block repeated $3^h$ times restores the first $h$ phase digits: three copies return the first digit and give a repeated block on the remaining strip, so induction applies. After $42\cdot3^h$ root requests the two phase vectors therefore coincide through width $h$, even when $h>2$.

Here is the derivation of the edit congruence. Finite-width phase updates by a given letter are bijective. The previous first digit is determined from its new value and the root letter. This recovers the outgoing letter, or silence, and successively determines every previous digit. On the comparison side the first two paired images have primitive periods ABBA and $C$. Thereafter the odd intermediate period is BAABAA, and $F(C^3)=C^2$ as finite words with both phases restored. Counting the initial cells and the period multiplicities gives a return time on the first $h$ phases of $3^{\max(0,\lfloor(h-2)/2\rfloor)}$ source groups.

Enumerate one joint cycle of $5\cdot3^8$ dates on the first 13 cells. The only agreement is date 2, and both starting states return at the end of the cycle. A candidate therefore has $n=2+5k$ with $3^8\mid k$. On the genuine side this means applying $k$ full groups, followed by the same A and edited B as at date 2. By bijectivity, returning to the date-2 phase vector through a cut is equivalent to the genuine groups restoring those phases. If the comparison side returns and the genuine side does not, equality at the edit is impossible.

For each $v=8,\ldots,31$, the checker finds a width $h\le56$ at which $3^v$ groups restore the comparison. The genuine cut count over $3^{32}$ groups is not divisible by $3^{32-v}$ at that width. The counts come from dividing the [40-cycle ledger](frontiers/runs/line31-phase-rows.txt) by 40. A genuine return after $3^v$ groups would divide the long run into $3^{32-v}$ identical pieces, contradicting the count. All finite-strip return times are powers of three, since one further cell multiplies the previous period by one or three. This excludes every $k$ with exactly $v$ factors of three.

The [cut-56 period](line31-phase.md#period-growth-and-a-finite-field-form) has length $L=53{,}427{,}204{,}485$ and displacement $d=L-2(15{,}648{,}460{,}017)$. Its restoration time below +56 is exactly $3^{32}$ groups because this length is indivisible by three. At +56, $d$ is nonzero modulo three, so the next return takes $3^{33}$ groups. The succeeding displacement is $L$, again nonzero, giving $3^{34}$ groups. The next displacement is $2L+d$, divisible by three, so the phases through cell +58 close after the same $3^{34}$ groups. The comparison already returns at all these widths for $v=32,33$. This excludes those two valuations and proves both directions of the congruence.

## Reproduction

Run these commands in `research/bb2x5` with Python assertions enabled.

```sh
c++ -O3 -std=c++20 -fopenmp line31_phase.cpp -o /tmp/line31-phase
export OMP_NUM_THREADS=4
python3 line31_edits.py --engine /tmp/line31-phase --long-replay
/tmp/line31-phase --capture-edits 32 6800000 750000 4000000000
/tmp/line31-phase --postpone-edit 22 1 280522900892
/tmp/line31-phase --postpone-edit 22 1 280522900893
/tmp/line31-phase --postpone-edit 22 2 1000000000000
/tmp/line31-phase --postpone-edit 22 3 3000000
/tmp/line31-phase --postpone-band 22 100 1216 10000000000
/tmp/line31-phase --literal-shift 22 100 1216 90190513
/tmp/line31-phase --literal-shift 22 100 383 231475923
```

The OpenMP flag is optional and parallelizes the independent edit dates. The Python replay also compares the native classifier with direct infinite-word transformations on small cases. The capture search takes pair depth, last allowed edit date, initial future-letter budget and maximum future-letter budget. It reports every capture and any unresolved dates. It exits successfully only when every candidate is decided and the genuine prefix has supplied a mismatch at every requested cut. The postponement test takes cut, number of inserted periods and finite tail budget. The shorter of the two adjacent budgets exits with status 2 and names +134 as the first unchecked cut. The longer one prints the failing prefix and its parent.

The band check takes starting cut, last even cell, upper bound on the number of true periods needed to cover that cell, and fixed-tail letter budget for the remaining shifts. It finds the first adequate number of true periods by binary search. Its halt coordinates refer to a virgin suffix at the starting cut. The earlier fourth letters for the published +22 family are verified above.

The literal check takes starting cut, target cell, shift count and physical request limit. It drives a blank suffix with the aligned word after removing the three introductory As. It reads the machine's instruction string directly and stops at A2 or the first A0 at the requested cell.

The remaining constructive question is whether $Q_{22}^k C^\omega$ is safe at every depth for an unbounded sequence of $k$, or whether another family of edit positions supplies such a sequence. At any fixed final cell, sufficiently long true prefixes determine all of its preceding fourth letters. The table through +100 gives the complete exceptional set at that depth. As the final cell increases, this set can grow. In particular $k=1$ and $k=2$ first enter it at +134 and +136 respectively. A proof along this route must control which shifts survive every depth.
