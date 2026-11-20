# A directly sufficient global safety obligation for #758

**The blank-tape decision remains open.** This note gives one exactly specified
predicate problem whose verified invariant would prove halting, including
excursions that might otherwise never return. The current solver attempts
have not produced that invariant. No new blank checkpoint is claimed.

Keep the [known blank checkpoint](post36_ladder_758.md) and
[certified halting basin](TARGET_GAP_21_758.md):
$$
S_0=150124733170248900,\quad
H=(3^{307}-8282708212)/13959275,
$$
$$
B=H-160391744210493965542,\qquad U=H-3403055.
$$

## The global implication

`Reset(s)` represents $A(1,s)$. At ordinary odd/odd boundaries use
$$
\operatorname{Ord}(u,d):\quad
a=2u-4d-1\ge3,\quad c=2d+1\ge1,\quad h=u-2d\ge2.
$$
The mass is $W=2u+1$, or $2s+1$ at a reset. Starting from `Reset(S0)`,
use the complete live macros below and stop a reset in $[B,U]$.
Define `Bad` to mean a reachable reset with $s>U$ or ordinary endpoint
with $u>U$. Sources above the cap need no outgoing rule; **destinations
are never capped**, and a crossing endpoint still implies `Bad`.

**Sufficient theorem.** A checked inductive invariant containing the start,
preserved by every emitted live rule, and excluding `Bad` proves that the
blank orbit halts. Every live macro strictly increases its integer mass
coordinate, by between two and nine. An infinite live chain with all
coordinates at most $U$ is therefore impossible. Every other stop is an
explicit halt or an entry into the certified basin. Each macro takes at
most two counter calls, so an infinite unfinished excursion is also covered.

This checks live macro endpoints, not every raw half-step. A macro whose
second call halts is a successful stop even if its first call crosses the
raw mass cap. For example, $\operatorname{Ord}(14,2)=A(19,5)$ goes to
$A(12,11)$ and then halts; with $U=15$ the middle mass is already above
$2U+1$. Every infinite raw execution still supplies infinitely many live
macro endpoints, which is all the sufficient theorem requires.

## Exact grouped rules

From a positive odd reset, one actual $J$ gives
$\operatorname{Ord}(s+2,(s-1)/2)$. From a positive even reset, its opening
$I$ gives $\operatorname{Ord}(s+4,(s+2)/2)$. These openings increase mass.
Every even right counter on a reset-origin trajectory occurs at a reset;
the opening makes it odd again. No general even-right bulk rule is omitted
from a possible continuation of this start.

| Macro | Guard at an ordinary source | Destination |
|---|---|---|
| $J$ | $u\le3d+1$ | $\operatorname{Ord}(u+2,3d-u+1)$ |
| $E$ | $d$ odd, $u=3d+2$ | $\operatorname{Ord}(u+4,0)$ |
| Low $LR$ | $d$ even, $3d+2\le u$, $2u\le9d+9$ | $\operatorname{Reset}(u+5)$ |
| High $LR$ | $d$ odd, $3d+3\le u$, $2u\le9d+14$ | $\operatorname{Reset}(u+7)$ |

For $r=d\bmod4$, a pair has
$$
u'=u+v_r,\quad d'=(9d+b_r)/4,\qquad
(v_r,b_r)=(5,20),(9,35),(7,26),(7,29).
$$
Its guard is $h'=u'-2d'\ge1$. The positive final left counter proves that
both positive bulk decrements were available, hence both physical guards.
If $h'=1$, its destination is `Reset(u')`; otherwise it is `Ord(u',d')`.
The even-left midpoint cannot be a hidden reset. The $LR$ guards also
include a final bulk left counter of zero, which the scalar rules allow.

The following are exactly the omitted ordinary sources, for $d=4q+r$.
Each halts on its second scalar call. The intervening integer ranges are
precisely the $J,E,LR,P$ guards, proving completeness of the partition.

| $r$ | Halting values of $u$ |
|---:|---|
| 0 | $18q+5$ |
| 1 | $18q+12,18q+13$ |
| 2 | $18q+14,18q+15$ |
| 3 | $18q+21$ |

## Two proved additions for invariant discovery

The strengthened problem restricts ordinary sources by the following
inductive provenance condition $P_2$, with $h=u-2d$:
$$
h\in\{2,3,6\}\ \lor\ d\equiv2,5\pmod9\ \lor\ h\equiv0\pmod9
\ \lor\ h+3d\equiv9,18\pmod{27}
\ \lor\ (d=0\land h\equiv3\pmod6).
$$
It implies $P_1$: $h=2$, or $3\mid h$, or $d\equiv2,5\pmod9$.
Under $J$, these three cases give respectively $h'=6$, $9\mid h'$, or
$h'+3d'=3(d+1)\equiv9,18\pmod{27}$. Every pair gives
$d'\equiv2,5\pmod9$. An $E$ gives $d'=0,h'\equiv3\pmod6$.
The reset openings have $h=3$ and $h=2$. This proves the induction for
every positive reset origin; it does not rely on a residue census.

It also stops ordinary sources satisfying a proved carry-to-basin condition.
For odd $b\ge1$, put $r=(3/2)^b$, $c=2d+1$, $W=2u+1$. If
$$
3r(c+7)\ge W+9b+21,\qquad
2r(c+13)\le W+5b+26,
$$
then all $b$ bulks and the following reset are legal, with output in
$$
\left[u+\frac{5b+5}{2},\ u+\frac{9b+5}{2}\right].
$$
This follows from the [bulk bounds](UNIFORM_PARITY_PASSAGE_758.md):
$r(c+7)-7\le c_b\le r(c+13)-13$ and $5b\le W_b-W\le9b$.
The displayed inequalities imply $0\le a_b\le c_b$. Positive decrements
prove every earlier guard and exclude an earlier reset; $a_b$ is even.
The source is stopped **only if the whole output interval lies in $[B,U]$**.
These sufficient conditions leave other bulk passages undecided.

The target generator includes the 393 odd lengths $1\le b\le785$.
Indeed $c_b+7\ge8(3/2)^b$, and $8\cdot3^{787}>(U+7)2^{787}$;
a 787-bulk run cannot finish with a reset at most $U$. This bounds the
list of sufficient stopping conditions, not the execution. All remaining
sources keep their original exact rules. Every destination and both `Bad`
rules are unchanged. Clearing $2^b$ makes each condition linear in $u,d$.

## Checks, solver status, and reproduction

The [portable generator and auditor](global_safety_758.py) uses Python's
standard library and the repository's scalar map and pair constants. Its
default checks compare every macro with scalar execution, check provenance
preservation and selected long carry passages, and verify structurally that
strengthening changes only the justified source conditions. The quantified
claims above follow from their proofs, rather than these examples.

Both controls use an empty basin, encoded by $B=U+1$. Seed 12 has the
complete live endpoint chain
$$
\operatorname{Reset}(12)\to(16,7)\to(18,6)\to(20,1)
\to(29,11)\to(31,5),
$$
then halts in two calls. This finite set is an explicit inductive invariant
for cap 31; cap 29 has the concrete crossing to $(31,5)$.

The full-target baseline run with Z3/Spacer 4.13.3 returned `unknown` at a
30-second limit. The strengthened run also returned `unknown` at a
45-second limit. Neither result proves reachability, unreachability, or a
mathematical obstruction to this approach. A safe small-instance invariant
was extracted and separately rechecked against every Horn clause with a
quantifier-free integer-arithmetic solver; the crossing control supplies
the opposite outcome. **No full-target invariant was obtained.**

```sh
python3 global_safety_758.py
python3 global_safety_758.py --emit toy-safe > /tmp/toy-safe.smt2
python3 global_safety_758.py --emit toy-cross > /tmp/toy-cross.smt2
python3 global_safety_758.py --emit target > /tmp/target.smt2
python3 global_safety_758.py --emit target --strengthened > /tmp/target-strong.smt2
```

The emitted query is reachability of `Bad`. A proposed `unsat` answer must
come with an invariant whose initial-state, rule-preservation, and exclusion
conditions are checked. A `sat` crossing is not a nonhalting proof: the
trajectory may halt later, as the small crossing control itself does.
