# Line 6: matching, crossing histories, and the remaining decision

Formal line 6 is `1RB---3LB4RB0LA_2LB3LA3RB4RA0RA`. Its blank decision remains open. The [word reduction](line6.md) says it runs forever exactly if every B probe on a unary input of twos returns B. Write this probe as $F(2^n)$, its defined-step cost as $C_n$, and the time of left extension $e$ from blank as $T_e$. A probe can return B, return A, or halt internally. A completed B probe leaves physical tape `2v` and records residual $v$. An A probe result records the entire returned word.

## Which A replies actually threaten the blank run?

A checkpoint contains many positions where an independently started B probe would return A. Whether the blank computation requests B **at that position** matters. Starting a fresh B probe at every nonpadding position, always from its own pristine copy of the checkpoint, gave:

| Blank checkpoints tested | B returns | A returns | Internal halts | Replies outside the local rule below |
|---|---:|---:|---:|---:|
| Every extension from 1 through 376 | 270,826 | 3,065 | 0 | 12 |
| Extension 16,310 | 64,842 | 349 | 0 | 0 |

Let $U=(32\mid33)^*$. Every suffix beginning $U\,30\,U\,0$ returns A: both `32` and `33` preserve the subordinate tag, `0` gives B, and `30` changes B to A. Pad the stored word by zeros. Predict A for this pattern and B otherwise. At extension 16,310 even the narrower pattern $(32)^j30(32)^k0$ explains all 349 A replies. The longest suffix test there took 112,262,641 defined transitions at zero-based offset 18,004.

There are twelve genuine exceptions to that predictor in the early survey. Every one returns A, begins with `22`, and lies at offset $9h+1$ for the current maximal count $h$ of leading headers. The epochs are 113, 115, 117, 119, 178, 180, 289, 291, 324, 326, 371 and 373. At epoch 113 the hypothetical B entry at offset 10 returns A in 181 steps. In the actual root probe there are exactly four crossings at that cut:

| Probe step | 32 | 33 | 34 | 189 |
|---|---|---|---|---|
| Crossing | enter A | return B | enter A | return B |

The root returns B at step 207. After the header, its real input begins `32`. B on the first 3 sends A into the 2; the `32` reduction requests B beyond that pair. An independently launched B at the second cell is a different computation. The 376-epoch and 16,310-epoch observations leave the intervening epochs unclassified by this survey.

**How to use the header.** At any offset within H, follow the literal B probe until it stops or first requests the suffix. For offsets 0, 1, 2 it requests the suffix once in B; its local cost before that request is respectively 31, 28, 27. An A reply hits A1 immediately. A B reply returns B in respectively 17, 48, 13 further steps without visiting the suffix again. At offsets 3 through 8 the result is independent of the suffix:

| Offset | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---:|---:|---:|---:|---:|---:|
| Reply | B | B | B | A | B | B |
| Steps | 17 | 27 | 9 | 5 | 1 | 1 |

Thus prefixing H to a B-returning word adds exactly one A-returning suffix. At the last checkpoint 93 of the 349 A positions come from the headers and 256 from the remaining word. The checker replays both possible boundary replies and every suffix-independent trace.

**Next decision target.** On a successful epoch, isolate the actual requests on the residual after H has been stripped. At an exposed `30`, exclude an A reply from the subordinate probe; at the residual root prove a B return. The twelve exceptional positions are test cases for any rule predicting those requests. A useful falsification control is `322300003`. It is matched and admissible, and every suffix agrees with the local rule above. Its root returns B in 19 steps, yet the next checkpoint word `3223332003` halts internally in 36 probe steps. A proof of closure therefore needs more information than agreement with this predictor and the matching and admissibility conditions.

## Adjacent matching

Match adjacent `23` or `32` pairs without reusing a cell. Write $D(w)$ for the minimum number of uncovered twos. Read right to left and take any available pair. This gives a maximum matching: the rightmost eligible edge can replace any competing edge at its left endpoint in a maximum matching, after which its two vertices can be removed. Zeros separate independent subproblems.

The boundary profile of a scanned suffix is N (no available first cell), T (first cell is an available two), or S (available three). Prepending a zero gives N. Prepending a two to S gives N at zero cost; on N or T it gives T and increases $D$ by one. Prepending a three to T gives N and decreases $D$ by one; on S or N it gives S at zero cost.

**Closure.** Any completed $F(w)$ with residual $v$ satisfies $D(v)\le D(w)$. The change is at most $-1$ when the input has profile T. The following table certifies the bound. Each entry lists possible output profiles; each inherits the bound at the right.

| Input | B result | A result | Upper bound on change |
|---|---|---|---:|
| N | N, T, S | N | 0 |
| T | N, T, S | N | −1 |
| S | N, S | N | 0 |

Induct on the finite derivation in the word reduction. For each row of its probe equations, take the bound for the subordinate call and add the cost of prepending the output prefix minus the cost of prepending the input prefix. For the two-call equation add both bounds, equating the intermediate profiles. A first A forces a second B by the reduction's A-residual lemma. The base call deletes a leading zero. [The checker](line6_matching.py) exhausts precisely these finite cases against the displayed table.

Consequently all blank checkpoint words are tiled by `0,3,23,32`: the empty word is matched, and a successful epoch prepends the matched pair `32` to a matched residual. Every completed probe $F(2^n w)$ on a matched tail $w$ also leaves a matched residual. For $n=0$ use closure. For $n+1$ the first call leaves a matched residual by induction, the second preserves matching by closure, and its output prefix is `23`, `32`, or `3`. This applies even if some earlier blank epoch failed.

At extension $e$ the tape contains exactly $e$ twos and therefore at least $e$ threes. Its rightmost nonzero coordinate is at least $e$. With $h$ leading copies of `H=322323300` the lower bound is $e+3h$. Each header contributes nine cells with three twos, and its terminal zeros isolate the fully matched remainder.

## A crossing history measures the change in twos

At a cut, pair each entry to the right with its return to the left. Write a pair as request state followed by reply state. A completed request on clean tape (digits 0, 2, 3) leaves clean tape. Keep a flag indicating whether the first cell to the right of the cut is a two.

| Pair | Change in number of twos to the right | New flag |
|---|---:|---|
| AA, BA | +1 | false |
| BB | +1 | true |
| AB | −1 if flag was true, +1 otherwise | toggle |

For B entry this follows from the two-count identities and the possible first digit of an A residual. For A entry on 2, the single A2 instruction removes that two and returns B. On 0, A0 sends B right: only a B reply completes, and B1 returns A leaving 3. On 3, A3 sends B right, leaving 4. An A reply crosses the 4 in A; a B reply leaves `2v`, and B4, A2, B0 complete a B exit leaving `23v`. These cases give the stated changes. At first entry into each cut of a unary run the suffix is pristine. Subsequent entries follow completed requests, so cleanliness holds at every request boundary.

Let $m_i$ sum the signed changes at cut $i$, counting the initial B request at the root as a conceptual entry. Let $p_i$ count the final twos in the first $i$ cells. The initial suffix has $(n-i)_+$ twos and the final tape has $n+1$. Thus

$$m_i=n+1-p_i-(n-i)_+.$$

For $i\ge1$, $p_i\le 1+\lfloor i/2\rfloor$. For a B return discard the possible exceptional leading two; among the remaining $i-1$ cells only one matched pair can straddle their right edge. An A return satisfies the same bound. Hence $m_i\ge\lceil i/2\rceil$ through cut $n$ and $m_i\ge n-\lfloor i/2\rfloor$ beyond it. Each pair costs two moves away from the root, each contributes at most one to the sum, and the root exit costs one real move. The lower bounds on cuts 1 through $2n-1$ sum to $n(n+1)/2$. In particular

$$C_n\ge n(n+1)+1,\qquad T_e\ge e^2+2.$$

The first inequality applies to every completed unary probe (A or B). The second applies at each reached blank extension, using $e=n+1$ and $T_e=C_n+n+2$. An internal halt has an incomplete history and is outside the first inequality.

## Repeated cuts cannot decide a unary probe

In any completed unary probe, the $n+1$ paired histories at cuts $0,\dots,n$ are all different. Suppose two cuts agree. Duplicate the intervening strip of $d>0$ initial twos, including its local cell traces. The matching cut histories splice: run the trace of each region until the next crossing and resume the next region with its matching state. Each visit consumes a trace event. At the root interpret the first entry as the initial state. Complete matching transcripts force the same final left exit and tape, with an extra copy of the strip's final contents. This argument works with arbitrarily many copies. Comparing the two-count after one duplication, the extra strip must finish with exactly $d$ twos, since every completed probe has gained one two. Four copies would then leave a run of at least four twos. Even after dropping a possible leading physical two the matched residual would contain three consecutive twos, which cannot all be matched. This rules out the repeated-cut approach for all widths.

## Removable headers with a single B request and reply

Consider a clean finite header $P$ that receives one B request, passes one B request to its suffix, takes one B reply and returns B. Let $P'$ be the resulting contents restricted to those cells. Preservation at the next epoch requires `3` followed by $P'$ to equal $P$ followed by `3`. The only such words are powers of H.

Here are details for checking completeness. Encode AA, AB, BA, BB by $a,b,c,d$. A node consists of an initial digit and a transcript on its left. The digit after processing that transcript must equal the initial digit of the following cell, by the preservation equation. A transition emits the transcript on the right. The initial and terminal node is $(3,d)$. For one left request the complete local possibilities (final digit, emitted transcript) are:

| Digit | a | b | c | d |
|---|---|---|---|---|
| 0 | 3,d | — | — | 2,empty |
| 2 | — | 3,empty | 0,cc / 3,cdad / 0,da / 3,dbad | 2,cdb / 2,dbb |
| 3 | 0,c / 3,dad | 2,db | 0,a / 3,bad | 2,bb |

These rows follow by executing a cell, branching on both replies after each request to the right. Each right move advances along the finite rewrite chain from 2 through 3,4,0 to 1. Concatenate the outputs for a longer left transcript, carrying its updated digit. An empty right transcript cannot lead to the required suffix visit.

Put $X=db$, $Y=bb$. The forced start is $(3,d)\to(2,Y)\to(2,X)$. At $(2,Y^kX)$ the alternatives are $(3,X^kcX)$ and $(3,X^{k+1}b)$. The latter advances to $(2,Y^{k+1}X)$. The former goes to $(3,Y^ka)$ or $(3,Y^kbadY)$. The second dies; the first goes to $(0,X^kc)$ or the dead $(3,X^kdad)$. The prefix reductions used here are $X$ on 3 emitting $Y$, $Y$ on 3 emitting $X$, and $Y$ on 2 emitting $X$, each restoring its digit. The node $(0,X^kc)$ dies for $k=0$. Otherwise it gives $(0,Y^{k-1}a)$ or the dead $(3,Y^{k-1}bad)$. Only $k=1$ allows the former to proceed, with $(0,a)\to(3,d)$. Reading the digits up to that first return gives exactly `322323300`. Iteration gives all powers; the existing literal H trace supplies the converse. Headers that communicate with the suffix more than once require another analysis.

## Blank replay and a discriminator for the next proof

All 16,311 words from extension zero through 16,310 were distinct after removing every complete leading copy of H. Only extensions 3 and 6 tied on residual length and two-count: their residuals are `3223332` and `3232032`. At extension 16,310 the step count was 10,087,506,894, with 93 headers and 64,354 residual cells. This reproduces the existing checkpoint; the new observation is the comparison of all intermediate residuals. The final 65,191 ASCII digits have SHA-256 `71c87c3476550d0ede4477ff7ae1776ae0940f77da91a99367e6948e5c62834b`.

Two matched words isolate what an order-sensitive argument must explain. Both have prefix `3223`, the same zero positions, and identical tile counts within each nonzero interval. Starting a B probe, swapping just the indicated adjacent tiles reverses its reply.

| Left part | Swapped tiles | Right part | Reply | Steps |
|---|---|---|---|---:|
| `32233232320032` | `23 32` | `3232320032` | A | 511 |
| `32233232320032` | `32 23` | `3232320032` | B | 885 |

The first gives an actual halt on A1 at step 512 from a fresh A0 immediately before the word. The A run only reads the displayed 28 cells and seven further zeros. Any suffix after those seven zeros gives the identical A trace. In particular, put `30` in front of that 35-cell prefix: a B probe entering this 37-cell pattern **halts internally after 513 defined steps**, regardless of the rest of the tape. The B control likewise holds for every suffix after eleven following zeros. Both examples are auxiliary inputs. To narrow the blank decision, track the order of the two tiles in the residuals that reach a `30` call: that rule halts precisely on an A reply. A proof also needs a B reply at the outer root of every unary probe.

### Reproduction

Run from this directory with assertions enabled:

```sh
g++ -O3 -std=c++17 line6_residual.cpp -o /tmp/line6-residual
python3 line6_matching.py --binary /tmp/line6-residual --suffix-epochs 376
/tmp/line6-residual 16310 --suffixes > /tmp/line6-residual.txt
```

The Python check verifies finite closure and the traffic identity at every visited cut on literal unary runs of widths 0 through 100. It compares all 5,151 interior-or-endpoint histories against fingerprints accumulated independently from blank epochs. The C++ replay caches exact exits from five-cell blocks. Interior cuts for width $n$ inherit the width $n-1$ trace and append the new epoch's crossings, by the unary reduction. Each new root has history BB. Differing fingerprints certify inequality; equal fingerprints would require exact replay. The full pass distinguishes 723,120,429,115 pairs of histories within probes. These are computational cross-checks and the proofs above have not been formalized in Rocq.
