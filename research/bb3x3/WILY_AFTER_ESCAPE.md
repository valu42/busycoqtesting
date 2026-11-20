# What follows a first positive Wily escape from blank

**If the blank-connected negative excursion of #531 and #532 ever reaches a first positive scalar state, both machines complete at least 120,075,937 more paired updates. The scalar stays positive throughout the first 98,303 of them.** Each paired update represents two completed original sweeps. The longer guarantee permits subsequent sign changes and uses the actual physical correction and allocation rules. The existence of that first escape and the ultimate blank outcomes remain open.

As an unconditional corollary, the actual blanks complete at least **2^256 + 240,151,876 original sweeps**. Their scalar is negative at the previously verified 2^256-sweep checkpoint. Every step up to and including a first positive entrance is safe. Such an entrance can occur no sooner than the next paired update, and if it occurs both machines then complete the additional 120,075,937 pairs. If it never occurs, they run forever. This corollary uses the earlier checkpoint and the all-width argument below.

The bound 120,075,937 is sharp for the prefix-cycle and invariant test below. There are arbitrarily large alternate negative-to-positive transitions that satisfy both blank labels, agree with the blank orbit to any prescribed finite precision, and halt on the next update after the bound.

## What the first positive word must look like

Use the [integer map](WILY_INTEGER_MAP.md) and write `e<0` for the last negative scalar and `p=F(e)>0`. During the negative segment from the recorded checkpoint the physical bucket stays canonical. It starts canonical. An internal step retains the physical width, and the canonical width cannot decrease on a negative step. Either continuing extension ends with high 00, which forces the enlarged physical bucket to be canonical. A negative correction or halt would require the exceptional inputs already excluded in that segment.

For every negative escape, the canonical word for `p` has one of these forms, written low bit first.

| Root of the negative escape | Canonical positive word | Physical word at entry |
|---|---|---|
| −8 | `v 111` | `v 111` |
| −16 | `v 11` | `v 11 10` |

Here `v` is any concatenation of tokens 0 and 10. Indeed, the two roots map to 13 and 5, represented canonically by 111 and 11. The output lifts prepend precisely the tokens 10 and 0. The escape updates stop internally because their outputs are positive. For root −16 the physical bucket at `e` is four times the canonical bucket at `p`, so the physically present padding is one virtual pair 10.

The certified magnitude bound from blank is `|e|>2^765`, so the first 96 bits are within this token prefix. They contain no adjacent ones. In addition `p≡1 (mod 3)` and its [dihedral label](WILY_DIHEDRAL.md) is the identity. Both facts persist from the signed blank checkpoint because no intervening scalar step has changed residue. The sign-crossing step preserves residue as well.

## Checking all phases and all lengths of the remaining word

At width 96 the low physical prefix of the checkpoint lies on a cycle of length `2^42`. Exactly 6,796 of its phases have no adjacent ones. For each such phase the checker recovers every arrival at the 96-bit cutoff during each claimed interval. Low cells evolve independently of all higher cells, also after physical corrections.

The enumeration extends a prefix one bit at a time, as in the [blank orbit sieve](wily_orbit_sieve.py). A new bit doubles the old period precisely when it flips an odd number of times per old cycle. Its value at any phase comes from the parity of the preceding arrivals that flip it. Thus each retained phase lifts to its possible child phases without traversing the full clock. To recover chronological times, invert emission ranks through the columns. Runs of 1 or 2 emit on every input. Runs alternating 0 and 3 emit exactly on their 0 slots. Each inversion gives the global input slot of the selected emission, and successive inversions reach the original clock.

For a fixed low prefix, let `u` be the finite list of its outgoing carries up to the horizon, in chronological order. If the prefix ends in 1, first consume the obligatory 0 completing that token. The remaining high prefix can be any word in the tokens 0 and 10. To check all lengths, track the triple consisting of the remaining arrival list, the digit-product label so far and the width modulo four. For each of the two tokens, propagate the ordered arrivals through its bits literally and update the product and width. The list length cannot grow. This yields a finite graph, and complete graph search checks both possible tops at every reachable vertex.

Place a top of two or three ones, retaining only the odd canonical widths, as required by residue 1. Complete the digit product with enough virtual bits from 101 to reach four-bit alignment and retain the identity label. For the 98,303-update claim, every surviving stream stops internally and leaves the highest canonical digit 1 after every arrival. An unchanged highest one suffices for a positive numerator. For the 120,075,937-update claim, process the entire remaining stream on the *physical* upper word in the table. A mode 0, 2 or 3 at the edge allocates its actual extension. None of these completions reaches a halting mode 1. The finite-state checks concern an unbounded set of possible positive entrance widths.

## An exact family at the limit

Let `D` be the 96 low bits of the little-endian integer `0x555455454202808208a48050`. For any `d≥0`, take the canonical positive word

```text
D (10)^d 00 111.
```

The low word `D` ends in 0 and has no consecutive ones, so each listed word comes from the root −8 escape and needs no physical padding. Its width is odd. The checker verifies its identity label for even and odd `d`: two added pairs contribute the identity product and leave four-bit alignment unchanged. Write `p_d` for its scalar and `e_d=F⁻¹(p_d)`; then `e_d<0` and the transition to `p_d` is a genuine physical step at the same canonical width.

On the 96-bit blank cycle, `D` occurs exactly 121,797,128 updates before the checkpoint phase. Starting from that phase, the first three arrivals to the next cell are as follows, with offsets zero-based.

| Update offset | Mode |
|---:|---:|
| 119,977,633 | 1 |
| 120,075,937 | 0 |
| 120,076,522 | 1 |

The next arrival occurs at offset 4,151,058,666. The first two arriving modes in order, 1 and 0, pass through a pair 10 as the identical ordered stream 1 and 0. They therefore do so through every displayed repeat. On the fixed top 00111, the first mode stops internally. The second mode reaches the empty edge in mode 1. Thus the alternate tapes complete precisely 120,075,937 updates after the escape, and halt on update 120,075,938.

These entrance states approach a specific integer on the blank's actual *virtual* orbit. For

```text
q = 3D − 2^96 = −3627667079787141984845584
```

the virtual bits are exactly `D (10)∞`. By the low-prefix phase calculation, 121,797,128 iterations take its low 96 bits to the checkpoint bits. During that interval only the displayed three events 1,0,1 reach the higher bits. On the alternating tail they send its numerator −1 successively to −2, −1 and −2, which is the checkpoint's actual high numerator. This proves `F^121797128(q)=n_*` as an exact integer equality. Equivalently, the explicit numerators are `p_d=q+53·2^(96+2d)` and `e_d=F⁻¹(q)−15·2^(96+2d)`. The first formula sums the displayed digits. For the second, the inverse sweep transmits the same carry through the shared low 96 bits. The carry at that cutoff is inverse mode 0. Through each 10 it writes 01 and passes inverse mode 0 again. Thus the difference from the inverse reference scales by four per pair; at zero pairs the checker gives the factor −15. For every fixed precision, all sufficiently large `p_d` share that many low bits with `q`, placing them on the actual blank prefix cycle at that precision. Their predecessors likewise share the blank cycle by invertibility. The examples need not have the blank's full ordered past. In particular the proof does not identify any of them with a future first escape.

Run `python3 wily_after_escape.py` to verify both uniform bounds, the rank calculations, the virtual predecessor and the alternate family.
