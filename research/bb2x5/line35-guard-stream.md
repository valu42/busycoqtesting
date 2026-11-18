# An exact halt test for line 35

Line 35 is `1RB2LA4RA1LA3LA_0LA3RB3LB2RB---`. Start in A on the two-way blank tape. **From epoch 5 onward, a sweep reaches B4 exactly when the debt entering the first eight cells is at least six plus their opening-minus-closing balance.** This statement holds for every reached epoch, including the first one with large incoming debt. The blank-tape decision is open. The remaining task is to exclude that inequality for every blank sweep or exhibit one reached sweep satisfying it. [Sweep semantics and Pascal suffix](line35-pascal.md) · [Executable checks](line35_guard_stream.py)

## Proof at the eight-cell cut

An epoch starts with A scanning the blank immediately left of a finite word. In physical digits, 1 opens, 2 closes and 3 is neutral. The guard halts on the sixth unmatched closing. Every successful sweep takes a positive finite number of instructions. For a word $W$ let $b(W)$ count openings minus closings, and let $h(W)$ be the greatest excess of closings in any prefix, including the empty prefix. A right-to-left scan with incoming debt $d$ leaves debt

$$H(W,d)=\max\{h(W),d-b(W)\}.$$

Indeed, each closing increments debt and each opening decrements it down to a floor of zero. Composing these updates gives the displayed maximum, or equivalently one can maximize the deficit over prefixes of a concatenation. Thus for an eight-cell prefix $P$ with $h(P)<6$, the exact threshold for a halt is $6+b(P)$.

It remains to prove that a different prefix, already capable of halting internally, can never appear. The literal machine reaches `213111112` at epoch 5 after 97 instructions, with the head at −5. Start the following finite closure with its first eight cells. For each prefix, mark its surviving openings by a right-to-left scan with debt $d$. The old sweep rule writes $D(l,r)$ at each ordinary cell, where equal adjacent survivor bits give 1, the pair $(0,1)$ gives 2, and $(1,0)$ gives 3. Prepend the actual guard header and take the first eight digits. This successor depends only on $P,d$. Every successful incoming debt is among $0,\ldots,5+b(P)$ by the formula above. The enumeration visits every such case.

| First halting incoming debt | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Number of prefixes | 4 | 6 | 5 | 24 | 6 | 13 | 9 | 2 | 2 |

The graph closes on 71 prefixes and 561 distinct edges, from 616 successful prefix/debt pairs. Every prefix has $h(P)\le2$. Induction over the actual successful sweeps proves membership up to and including a first failing epoch. The checker independently runs all 616 inputs and the first failing debt at each of the 71 prefixes on the literal machine. For these individual replays, $P\,2^d12$ realizes exactly the required suffix debt. Actual blank reachability of a sequence of such inputs requires a consistent evolving tape.

At debt five the four vulnerable prefixes are `13232312`, `21323213`, `21323231`, and `23213123`. In the blank sweeps from epochs 5 through 25,000, exactly 32 prefixes and 35 prefix/debt pairs occurred. The only member of the four to appear was `23213123`. It occurred 281 times, always with debt two. The smallest gap to the halting threshold was three, first at epoch 46. These are finite observations.

There is also an exact test for the untreated middle. Write the tape as $P M R$ when a complete Pascal suffix $R$ starts beyond the cut. Its debt $u=h(R)$ is zero on the covered odd phase and at most one on the intermediate phase. Set $T=6+b(P)$. The sweep halts if $h(M)\ge T$. The **only additional case** is $u=1$, $h(M)=T-1$ and $b(M)=1-T$. This follows by testing $\max(h(M),u-b(M))\ge T$ and using $h(M)\ge-b(M)$. On the odd phase, an actual halt must already be forced before the covered suffix begins. [Pascal suffix interface](line35-pascal.md#the-two-cell-boundary-and-the-triples)

### A sufficient test using the left quarter

The parallel middle-word proof shows that every length-$l$ interval with five ordinary ancestors has excess closings at most $\lfloor(l+25)/8\rfloor$. Its independent checker gives a 177-state certificate. Combining it with the exact guard gives a shorter induction target. For width $n$, take $20\le x\le n-5$, let $S=W[0,x)$, and let $u$ be the debt of the last five cells (zero or one). At epochs with five preceding sweeps, **the guard is safe if**

$$h(S)\le5\qquad\text{and}\qquad x+8b(S)\ge n-27+8u.$$

Every prefix of the intervening $n-5-x$ cells has sufficient ordinary ancestry. Its deficit is bounded by $\lfloor(n+20-x)/8\rfloor$, and adjoining the last five cells increases that bound by at most $u$. The second inequality above is exactly the integer rounding of $b(S)+5\ge\lfloor(n+20-x)/8\rfloor+u$. The first protects the portion before $x$. This calculation also allows $x$ to vary among epochs. [Five-sweep bound, its proof and the stronger quarter test](https://github.com/valu42/busycoqtesting/blob/a36336f7345a582cc150c1ae4789b4be522f2aa9/research/bb2x5/line35-middle.md)

For $x=\lceil n/4\rceil$ the last failure of this sufficient test in our replay was epoch 443. Both inequalities held at every epoch from 444 through 25,000. The smallest margin in the second was 16 at epoch 495. The stronger published quarter test covers 524 through 150,000 and implies this one because $b(W[0,8))\ge-1$ throughout the prefix graph. **An induction maintaining these two quarter inequalities from epoch 444 would resolve line 35.** The initial segment is already checked from blank. [Parallel blank replay](https://github.com/valu42/busycoqtesting/blob/a36336f7345a582cc150c1ae4789b4be522f2aa9/research/bb2x5/line35-middle.md#applying-the-bound-to-blank)

### A condition on surviving runs in the preceding tape

There is also a way to test for a first halt one sweep earlier, using only the positions of surviving openings. Take a successful epoch from epoch 5 onward. Let $A$ be its physical header and $v$ the virtual left survivor, as tabulated below. In the old word, number positions starting at one. Let $i_r$ be the position of the $r$-th change from survivor bit 0 to bit 1, using $v$ immediately before position one. **The following sweep halts exactly when some $3r-i_r\ge 7+b(A)-v$.** The respective thresholds for guard debts 0 through 5 are $5,7,7,7,9,9$.

In the first $i$ ordinary successor digits, let $r$ count such rises and let $s$ be the last bit. There are $r+v-s$ falls. Each rise writes a closing, every fall writes a neutral, and every other digit opens. The balance of the header and these digits is therefore $b(A)+i-3r-v+s$. A first descent to −6 must be on a closing, where $s=1$ and $i=i_r$. The header itself has deficit at most one. The genuine terminal pair is $O C$, whose closing is matched immediately, so the final appended digit cannot cause a first descent to −6. This proves the criterion. One possible proof of nonhalting is a bound on the cumulative number of short gaps between successive surviving runs from the left boundary. The positions must come from the actual preceding tape.

## An exact recurrence for the blank orbit

Number cells by distance from the right end, starting at zero. At a fixed index list the outgoing debt and survivor bit in successive epochs. Encode debt zero by letter 0 or 1 according to the survivor bit. Encode positive debt $d$ by $d+1$. A fixed column can be run forward virtually by the triangular suffix rule even if the full machine later halts. Its predictions agree with the physical machine as long as that epoch is reached.

Let $Z_t$ be the stream beginning at epoch $t$ of the **then leftmost** column. The rightmost cell is always a closing, so $Z_1=222\ldots$. A leading letter at least 7 means that this sweep reaches B4. For a smaller leading letter $a$, decode its guard debt $H$ and survivor bit $s$. New columns consume the stream of their immediate right neighbor. The single-column transducer $M_q$ with initial physical symbol $q$ reads a letter with debt $d$ and right survivor bit $r$. It computes $u=[q=1\ \text{and}\ d=0]$, emits the letter for $(\max(0,d+[q=2]-[q=1]),u)$, and changes its symbol to $D(u,r)$. [Shared transducer implementation](line37_stream.py)

| Old guard debt $H$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|---:|
| Physical header, left to right | `2` | `1` | `3` | `1323` | `1313` | `1331` |
| Virtual left survivor $v$ | 1 | 1 | 0 | 0 | 0 | 0 |

Delete the first letter of $Z_t$. Apply $M_{D(v,s)}$ to the remaining stream, then apply the transducers for the header digits **from right to left**. The result is $Z_{t+1}$. The old right-indices simply advance one epoch. The first new index contains the converted old leftmost digit, with the remaining new indices filled by the header. Induction gives an equivalent blank-tape decision problem. A halt occurs exactly when an iterate from $222\ldots$ starts with a letter at least 7. Each iterate is exactly representable by a finite prefix and period, since the transducer has three states. The guard schedule is computed at each step.

### Where a dangerous letter can occur

For *every* reached fixed column its virtual stream eventually consists entirely of letters 0, 1 and 2. This conclusion also holds if a later physical sweep halts. For indices zero and one use the permanent right pair from epoch 5. For $j\ge2$, let $k=1+\lfloor(j-2)/3\rfloor$ and take the first odd epoch $T_0\ge\max(5,t)$ for a column sampled starting at $t$. Run the right-index dynamics on the first $2+3k$ cells. Any missing cells at their left end can be filled arbitrarily because they cannot affect $j$ or a cell to its right. This finite evolution is defined independently of future guards. At $T_0$ the first Pascal triple is clean. By the [neutral-center waiting bound](line35-pascal.md#exact-waiting-time-for-a-neutral-center), all $k$ triples are clean by epoch

$$T_0+2\sum_{i=1}^{k-1}\big(i+2^{\nu_2(i)}+2\big).$$

Checking the nine combinations of a center and its neighbor shows that the outgoing debt **at each of the three cells** of a clean triple is at most one in both half-steps. The repeating tail of the column has period dividing $2\cdot2^{\lceil\log_2(k+1)\rceil}$, since after one more paired update the ternary centers are determined by the preceding Pascal bit vector. A prospective dangerous letter must lie in the transient of its own column. The newly born leftmost column changes at every epoch, so these individual bounds leave a uniform induction to prove.

## What a chronological invariant must distinguish

One can calculate the sharp tolerance for the next sample of a fixed old column after **any** finite history. Begin with an empty strip between the column and the left guard. For each history letter, pass it through the strip's current symbols from right to left, advancing each symbol with $M_q$. If the output is safe, add the new columns prescribed by the recurrence. The strip $S$ obtained at the end depends only on that history. The exact next halting debt entering $S$ is zero if $h(S)\ge6$, and $6+b(S)$ otherwise. This follows from $H(S,d)$. In particular, after one safe leading letter the following thresholds are exact.

| Leading letter | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Debt in the second sample that makes the next sweep halt | 5 | 6 | 7 | 7 | 7 | 9 | 9 |

This gives seven explicit classes of forbidden *anchored pairs*. Excluding them for every true iterate would decide line 35. The table concerns debt in the second sample, so a threshold of five there means letter six. For any $L$ initially successful updates, the strip has at most $5L$ cells. Changing just sample $L$ (offsets start at zero) to debt $6+5L$ forces a halt on that sweep even if all later letters are copied from the original stream. This algebraic example permits arbitrary stream input. The following small obstruction has a literal tape realization.

At epoch 181 the blank word has width 367. Its then-leftmost column begins `0 2 3 1 1 0 1 1`. After the first seven samples the newly generated strip at epoch 188 is `23213123231232`, with balance −3 and internal deficit 3. The real eighth sample is letter 1, debt zero. Replacing it with letter 4, debt three, gives guard letter 7 and reaches B4. Two genuine blank streams supply the alternate letter.

| Donor column at birth | Donor offsets | Genuine letters | What survives the splice |
|---|---|---|---|
| Epoch 1,204 | 512–516 | `1 1 0 1 4` | The four letters before the join match. Every contiguous window of length five in the spliced stream occurs in one of the two genuine streams. |
| Epoch 3,118 | 451–452 | `1 4` | The preceding letter matches. Both the donor birth and the changed offset match the recipient modulo 89. |

A description that accepts all true iterates using only their pooled length-five windows and genuine first seven letters accepts the first splice. Merely tagging the last pair with these two residues modulo 89 admits the second. The donor streams and the recipient come from the actual blank computation. The 27-cell physical tape `311123111121112111212112112` realizes the combined eight-sample history. Its first eight digits also agree with the true epoch-181 word. Started with A on the blank immediately before it, the literal machine executes 1,169 defined instructions and reaches B4 at coordinate −9 on the eighth sweep.

There is an infinite family behind this obstruction. For every power of two $k\ge2$, an explicit right extension of any normalized word that survives $2k-1$ sweeps can preserve the entire original word and all those guard readings, then force B4 on the following sweep. [Construction and proof](line35-delayed-debt.md)

The [28-cell closure and five-sweep interval theorem](line35-chronological-strip.md) extend the guaranteed left prefix and bound how often a long interval can have nonpositive balance. Repeating a block of ten genuine blank digits at epoch 83 tests the missing restriction on multiplicity.

**Next proof obligation.** Prove that the actual finite transients generated from $222\ldots$ always avoid the seven anchored pairs above, or generate a violated pair from that seed and replay the corresponding blank sweep. An invariant that follows the parental column through its birth and subsequent samples must in particular explain why epoch 181 supplies letter 1 at offset seven despite both donor histories. The independent `35-MIDDLE` campaign has bounded the intervening spatial word, giving the [quarter-tape induction target](#a-sufficient-test-using-the-left-quarter). [Live claims](ROADMAP.md#claim-board)

Run `python3 research/bb2x5/line35_guard_stream.py` from the repository root. It checks the literal guard graph, compares chronological forecasts to independent word sweeps, tests 10,034 finite-history cases, and replays the blank observations and the splices. [Checker](line35_guard_stream.py) · [Verification transcript](line35-guard-stream-verification.txt)
