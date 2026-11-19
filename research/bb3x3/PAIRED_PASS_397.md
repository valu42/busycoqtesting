# Two-bit sweeps for #397

Write `A` for carry `ca` and `D` for carry `cd` in the [six-carry
reduction](check_bb33.py). From blank, start with the one-bit word `1`.
A full pass on `w` applies `A` and prepends a zero to its output if it
survives. The following two-mode rewrite gives the same result on every
finite word. Each row follows from reading the two displayed bits in the
six-carry table. The tail `v` is arbitrary and a halt propagates through
any enclosing prefix.

| Input | Output of A | Output of D |
|---|---|---|
| `00v` | `11 A(v)` | `00 A(v)` |
| `01v` | `10 D(v)` | `01 D(v)` |
| `10v` | `01v` | `10 D(v)` |
| `11v` | `00v` | `11 A(v)` |
| Empty | `1` | `001` |
| `0` | halt | halt |
| `1` | `001` | `11001` |

In particular `D = A²` as partial maps on finite words, including their
growing right edge. Apply the A column twice. On the first two rows the
second pass sees `11` or `10` and stops after complementing that pair.
On the next two rows the second pass sees `01` or `00` and sends the
indicated carry onward. The three short inputs give `001`, halt, and
`11001`, respectively. None of these identities needs an infinite tape
padding convention.

## Exactly which words halt on the next pass

Split the word from the head-facing end into pairs. The pass halts exactly
when both conditions hold.

1. An unpaired final bit remains and is zero.
2. No pair starting with one is the first pair or immediately follows
   a pair of equal bits.

Indeed, a continuing pair sends A precisely when its bits agree, and D
otherwise. Only an A can end the sweep early, and it does so precisely on
a pair starting in one. At the edge the two carries have the same halting
test. In particular every even-length word survives one pass.

Among all words of length `2n+1` with `n ≥ 1`, exactly `2 × 3^(n−1)`
halt on their next pass. Of the first pairs reached with A, one continues
with A and one with D. From A there is one continuing pair to either
mode. From D there are two to either. Thus the two counts remain equal
and their sum triples on every further pair. The trailing zero is forced.
This counts distinct starting words and makes no distributional
assumption about the blank trajectory.

## Deciding a run using only A and D

At a fixed cut in the word, consider an infinite input stream made up
entirely of A and D, with no new bit prepended there. **The suffix halts
exactly when its initial length is odd and its final bit is zero.**
This classifies arbitrary finite suffixes under that input restriction.

Replace each D with two As using the exact partial-map identity. Across
a pair starting in `xy`, a stream of `q` As passes

$$
(1+[x\ne y])\left\lfloor\frac{q+1-x}{2}\right\rfloor
$$

As onward, with D counted as two. Each A complements the pair. Over two
As there is exactly one overflow, sending A at an equal pair and D at an
unequal pair. For an odd leftover A the overflow occurs when the initial
first bit was zero. This also gives a way to pass any known power of A
through a prefix using one integer update per pair.

If the word has `n` complete pairs, an event reaches the edge within
`2^n` As, since each pair can pass at least one per two input As.
With odd length and final zero that first event halts. With odd length
and final one, an early stop preserves the last bit and an edge event
replaces it by `001` or `11001`. The final bit stays one and the length
stays odd. From even length the first edge event appends `1` or `001`,
entering the preceding safe case. These arguments also cover empty and
one-bit inputs. The actual blank-phase input stream includes other modes.

The blank question is whether iterating the prepended pair rewrite ever
enters this explicit halting language. Run `python3 paired_pass_397.py` to
check all finite words through length 13 against the original six-carry
table, the counting formula, and the first 256 full passes from blank.
