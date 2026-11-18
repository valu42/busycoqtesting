# An exact word recurrence for line 6

The machine is `1RB---3LB4RB0LA_2LB3LA3RB4RA0RA`, the sixth entry in the November 3 formal list. Its undefined instruction is A1. Its blank-tape status remains open. The recurrence below removes the head coordinate and all A probes. Every probe on a finitely supported word either returns or halts in finite time. An infinite blank run would extend without bound in both directions. Its only internal halting test occurs in the rule for `30`.

## The recurrence

Write words in physical left-to-right order with an implicit infinite tail of zeros. From a fresh leftmost blank in A, let the tape immediately to its right be $w$. Initially $w$ is empty. The A0 instruction writes 1 and starts a B probe on $w$. Stop this probe on its first exit to the left, or at an undefined instruction. A return in A halts on the waiting 1. A return in B executes B1, writes 3, and arrives in A at a new leftmost blank.

Record a B return leaving $2v$ as `b(v)`, omitting the leading 2. Record an A return leaving $v$ as `a(v)`. A B probe that exits in B always leaves 2 on its first cell. A direct exit is B0. After a move to the right the cell contains one of 0, 1, 3 or 4, so the only instruction that can then exit left in B is again B0. The symbols written by moves to the left are 0, 2 and 3, so these suffice to represent every completed return word.

Let $F(w)$ denote this B probe. For the three two-symbol prefixes in the table, first evaluate $F(u)$. Words such as `23v` denote concatenation. Costs in parentheses count local defined steps in addition to the subordinate probe.

| Input | If $F(u)=b(v)$ | If $F(u)=a(v)$ |
|---|---|---|
| `32u` | `b(23v)` (+8) | `a(32v)` (+8) |
| `33u` | `b(33v)` (+8) | `a(00v)` (+4) |
| `30u` | `a(032v)` (+4) | halt (+2) |

The base rule is `F(0u) = b(u)` in one step. It applies to an empty stored word by implicit zero padding. In the remaining case $F(2u)$, evaluate $F(u)$ and then $F(v)$, where $v$ is the residual from the first result. Add both subordinate costs to the local counts below.

| First result | Second result | Result of $F(2u)$ |
|---|---|---|
| `b(v)` | `b(z)` | `b(23z)` (+9) |
| `b(v)` | `a(z)` | `a(32z)` (+9) |
| `a(v)` | `b(z)` | `b(3z)` (+5) |
| `a(v)` | `a(z)` | `a(0z)` (+3) |

A halt encountered during a subordinate probe propagates immediately. The next leftmost word is `32v` exactly on result `b(v)`. The cost of this epoch is the cost of the probe plus two defined instructions. The termination argument below justifies iterating this rule from the empty word.

### Derivation

* `32` sends B through the pair in four steps, leaving `04`. An A return takes four steps across `04`, leaves `32`, and exits in A. A B return guarantees the suffix is `2v`. B4 sends A onto that 2, A2 changes it to 3, and two B0 instructions exit left. This leaves `223v`. Repeating the argument shows that probing `(32)^k u` has the same outcome as probing `u`. On a completed return it costs an extra $8k$ steps. In particular `A` on `0(32)^k0` exits left in A after $8k+3$ steps and leaves `32(23)^k`, irrespective of the following cells.
* `33` sends B to the suffix in two steps and leaves `44`. An A return crosses both fours. For a B return, each 4 takes B4, A2 and B0. These leave `233v`. On `30`, the forward pass instead leaves `41`. An A return encounters the 1. A B return takes B1 and A4, leaving `032v`.
* The initial B2 on `2u` writes 3 and starts $F(u)$. If this yields `b(v)`, the head returns in B and the adjacent word is `3 2v`. B3, A2, B4 and A3 leave `04` and start $F(v)$. A B return takes B4, A2, B0 and B0, leaving `223z`. An A return takes A4, A0, B0 and B1, leaving `32z`. If the first result is `a(v)`, A3 on the initial 3 instead leaves 4 and starts $F(v)$. A B return takes B4, A2 and B0, leaving `23z`. An A return takes A4 and leaves `0z`.

## Every probe on a finitely supported word terminates

Let $N(w)$ count occurrences of 2 in $w$. Induction on any completed derivation gives the following identities.

* If $F(w)=b(v)$, then $N(v)=N(w)$.
* If $F(w)=a(v)$, then $N(v)=N(w)+1$, and $v$ starts with either `0` or `32`.

For the first three pair rules, compare the number of twos in the old and new prefixes. In the `30` rule a B result becomes an A result and the new prefix gains one 2. In the `2u` table the first and second results each contribute one surplus 2 precisely when they are A. The four new prefixes `23`, `32`, `3` and `0` contain respectively one, one, zero and zero twos. Subtracting the initial 2 yields the stated identities in all four cases. Every A result in either table explicitly starts with `0` or `32`.

In fact every A residual has the form `(32)^j 0s`. Each A entry in the tables either adds a leading 0 or prepends `32` to a subordinate A residual, proving the claim by induction on the derivation. The boundary of a finitely stored word supplies implicit zeros. The next probe therefore gives exactly `b((23)^j s)` in $8j+1$ steps by the `32` and base rules. In the two-call table a first A result consequently forces a second B result. The displayed A/A row describes a conditional local trace with an unreachable pair of subordinate results. No additional probe into $s$ is required in this branch.

Now induct lexicographically on $(N(w),L(w))$, where $L(w)$ is the length after trimming trailing zeros. The base rule on 0 terminates immediately. The first recursive call in every other rule strips a prefix. It decreases the number of twos or preserves that number and strictly shortens the stored word. A first-call halt propagates. In the sole two-call rule, on input `2u`, consider the remaining call after $F(u)$ returns.

* A first result `b(v)` gives $N(v)=N(u)<N(2u)$, so the induction hypothesis applies to the second call.
* A first result `a(v)` with a leading 0 gives an immediate base case. Otherwise $v=32s$, with $N(s)=N(v)-1=N(u)$. The induction hypothesis applies to $F(s)$, after which the `32` rule finishes $F(v)$.

This exhausts the cases. Each completed B probe increases the physical number of twos on the tape by one, since a B result omits a physical leading 2 and an A result stores the full word. Thus, on any completed left extension $n$ from blank, the head is at $-n$ and the tape contains exactly $n$ twos. The remaining decision is whether the recurrence from the empty word ever halts internally or returns A to the fresh leftmost marker. If neither event occurs, it reaches arbitrarily far left.

It must also extend to the right. Say that a word is admissible when it avoids both `02` and `222`, including its implicit tail of zeros. For any completed call on an admissible word, the residual is admissible and a B residual never begins `22`. Prove the two assertions together on the finite call tree. In the base rule the residual follows an initial 0, so it cannot begin with 2. All other B residuals have a new prefix `23`, `33` or `3`; their joins preserve both exclusions. A new prefix `32`, `00` or `0` on an A residual is followed by a subordinate A residual, whose leading `0` or `32` makes the join admissible. The sole remaining A case prefixes `032` to a B residual, which cannot begin with `22`. In the two-call rule the first residual is admissible by induction, so the claim applies to the second call as well.

The blank word is admissible, and a successful epoch prepends `32` to a B residual, again preserving admissibility. Every run of twos at a later blank checkpoint has length at most two and is preceded by a 3 because the word starts with 3 and forbids `02`. There are therefore at least $⌈n/2⌉$ threes at extension $n≥1$. Its word begins at coordinate $-n+1$, so the rightmost nonblank cell is at or beyond $⌈n/2⌉$.

## A criterion on unary words

The blank machine runs forever exactly when $F(2^n)$ returns B for every $n≥0$. The totality proof makes each of these individual tests finite. More precisely, suppose the tests through $n$ all succeed, and write their last result as $b(v)$. The blank checkpoint at extension $n+1$ has word `32v`. Its time is the defined-step cost of the single probe $F(2^n)$ plus $n+2$.

For $n=0$, the B probe on the blank takes one step, and the first left extension has word `32` at step 3. For the induction step compare $F(2^{n+1})$ and the actual next checkpoint probe $F(32v)$. In the unary test the first call gives the assumed $b(v)$, so both probes now reduce to the same call $F(v)$. On a B result both give a B result with prefix `23` attached to the same residual. On an A result both give an A result with prefix `32`. An internal halt of $F(v)$ propagates to both. Thus a first failing unary test detects the epoch in which the blank machine halts. On success the unary probe includes nine local steps in addition to its two subprobes. The blank epoch includes eight local probe steps and two outer steps in addition to $F(v)$. The time offset therefore increases by one, as claimed. Which unary inputs, if any, fail this test remains open.

## A direct test at a blank checkpoint

At extension 2 the blank word is `3223`. All later completed checkpoints have the form `3223w`. Write $G(w)=F(23w)$. If $G(w)=b(v)$, applying the `32` rule to the checkpoint gives $b(23v)$ and the next checkpoint is `3223v`. Thus the machine iterates the residual of $G$ starting from the empty word, halting on its first A result or internal halt.

The tag of $G(w)$ has a shorter test. Read the first symbol, treating the empty stored word as starting with 0, and let $z$ be the remaining word. In all rows below an internal halt in any requested probe propagates.

| Leading symbol of $w$ | When $F(z)=a(v)$ | When $F(z)=b(v)$ |
|---|---|---|
| 0 | halt | B |
| 2 | B | Replace $w$ by $v$ and repeat the test |
| 3 | B | Return the tag of $F(v)$ |

For a leading 0, the first call in the `2` rule for $F(230z)$ is $F(30z)$. It either halts or returns A, and a first A forces a second B as proved above. For a leading 2, the first call is $F(32z)$. Its A case again forces a second B. Its B case leaves `23v` for the second call, giving exactly $G(v)$. Here $N(v)=N(z)<N(w)$, so the loop is finite. For a leading 3, the first call is $F(33z)$. Its B result leaves `33v` for the second call, which has exactly the tag of $F(v)$. This proves the table. In particular, reaching an A result requires eventually reading a 3 whose suffix produces B and then A on two consecutive probes of the residual. A first halt may occur earlier, as specified by the table.

## A prefix that persists on the blank orbit

Set `H = 322323300`. A B probe into `Hu` reaches $u$ in B in 31 steps and leaves `040434441` on the nine cells of H. A return in A immediately encounters the final 1. A return in B takes 17 more steps on those nine cells, exits in B and leaves `223233003`. The two finite traces stay inside the header except for their endpoint crossings. In particular the 17-step trace leaves the whole subordinate word intact.

After B1 rewrites the fresh marker, `3` followed by `223233003` is exactly `H3`. If a successful epoch sends $u$ to $u′$, the corresponding epoch sends $Hu$ to $Hu′$ in 48 additional steps. If the epoch on $u$ halts, so does the epoch on $Hu$. By induction the number of complete leading H copies can never decrease between completed left extensions. The first three increases occur at the checkpoints below.

| Left extension | Defined step | Number of leading copies |
|---:|---:|---:|
| 5 | 169 | 1 |
| 329 | 3,310,143 | 2 |
| 376 | 4,808,934 | 3 |

At extension 5 the residual after removing H is `032032`. The prefix by itself admits halting continuations. For every $k ≥ 0$, the auxiliary word `H^k3` halts in exactly $31k+6$ defined steps from the fresh A0 checkpoint. Indeed the final B probe on the single 3 and its blank tail returns in A after five steps. This covers arbitrary prefix multiplicity and leaves open the behavior of the specific residual from blank.

Run `python3 line6.py` in this directory. It checks all 3,280 words of stored length at most seven against the independent literal interpreter, including halts, words on return and defined-step counts. It also checks every full blank checkpoint through left extension 376, the complete header traces and the reported prefix counts.
