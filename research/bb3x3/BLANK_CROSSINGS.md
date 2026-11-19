# Following the blank orbit across the smaller #758 candidate halts

**The blank orbit passes all three candidate pairs.** The table below gives the actual consecutive reset parameters across each pair. The published list numbers them 59 through 64. This forward calculation starts with just the blank machine and does not assume the earlier community simulation checkpoint. [Published list](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA#Large-scale_behavior)

| Smaller candidate K (the other seed is K+2) | Last reset before the pair | First reset after the pair |
|---:|---:|---:|
| 1,326,438,094,216,110 | 1,326,438,094,216,093 | 1,326,438,094,216,160 |
| 2,031,355,966,425,479 | 2,031,355,966,425,440 | 2,031,355,966,425,520 |
| 3,335,436,339,933,243 | 3,335,436,339,933,147 | 3,335,436,339,933,383 |

The prefix runs directly from reset 3 through 100,008. Then 2,435 windows cover the route from the cut at 100,003 to the cut at 1,059,491,543,272,883. Each guarantees a reachable reset in the next 5,001-seed window. The full chain passed, as did a further 42 windows ending at 1,080,000,000,055,450. The three candidate legs covered 493, 1,410, and 2,609 windows respectively. The shorter exact second-leg calculation is described below. The arithmetic jump beyond the third pair then gives a reset at **3,706,040,377,703,662**. The raw #758 clock there is at least **128,304,258,885,534,870,403,095,083,187,223,412,954,676,935**. The raw #153 clock is smaller by 50,707. [Jump beyond the third pair](JUMP_AFTER_THIRD.md) · [Lower bound up to the third pair](MASS_CLOCK_758.md)

## How a window advances the orbit

Let a reset mean any state A(1,s) of the two-counter map, including an intermediate visit to a = 1 during a longer calculation. The C++ checker takes two cut positions, start and end, with end > start. Its claim is that **every reset in [start,start+5,000] reaches some reset in [end,end+5,000]**. Checking consecutive pairs of cuts therefore advances a known blank-tape reset without reconstructing its entire intervening orbit.

At all times the checker stores a set containing at least one reachable reset for each input. Initially this set is the whole incoming interval. For a block [l,h], all stored reset parameters are at least l. Two operations preserve coverage.

* When both parities in [l,h] have continuing endpoint certificates, let g be the larger certified first-return increment bound. The [monotone branch argument](CONFLUENCE.md) proves that every seed s in [l,h] has a strictly increasing next reset at most s+g. Each trajectory starting inside the block must leave it and its first exit belongs to [h+1,h+g]. Retain any former possibility already above h. The checker encloses both sets in the interval from h+1 to the larger of h+g and the former maximum.
* When a block of width at most 250,000 does not have certificates for both parities, expand any stored interval into its exact integer members. Replace each parameter at or below h with its exact first return, stopping at the first subsequent visit to a = 1. Equal reset states can be merged. A possible halt or an exhausted step budget fails the certificate. Success leaves all stored parameters above h.

Larger blocks that lack endpoint certificates split into consecutive halves. A valid parity certificate for the parent remains valid on a child. If the current minimum already exceeds h, no work is needed. At the final cut the executable verifies both bounds of the outgoing window. It uses signed 64-bit counter arithmetic on cuts at most 10¹⁷. Every continuing map call increases the mass a+2c by at most nine, and both the endpoint and direct-call loops have explicit limits. Their intermediate expressions stay within the signed 64-bit range on this domain.

The initial J batch uses a+1 → 3(a+1). It performs k updates only when (a+1)3ᵏ ≤ 2c+(a+1), a sufficient condition for every update to be legal. The starting left counter is 3 or 5, and it increases throughout the batch, so it cannot hide a reset. The direct pass tests a = 1 before taking the next ordinary update. In an endpoint certificate, an earlier internal reset also suffices since the strictly increasing mass there is bounded by the mass at the certified later reset.

For each candidate K the final cut is K−199,000. The original, unbatched map traces every one of the 5,001 possible incoming starts until its first reset above K+2. Each reaches one of the following offsets.

| Candidate K | Possible reset offsets above K | Distinct first-return edges traced |
|---:|---|---:|
| 1,326,438,094,216,110 | +50 | 6,808 |
| 2,031,355,966,425,479 | +3, +9, +13, +19, +25, +29, +35, +41, +45, +51, +57, +61, +67, +73, +77 | 44,461 |
| 3,335,436,339,933,243 | +140 | 11,454 |

For the first pair, every input's crossing return goes from K−17 to K+50. For the third it goes from K−96 to K+140. For the second, an earlier gate selects the exact phase among the 15 possible local exits. Its actual crossing goes from K−39 to K+41. The full original second-leg chain covered 1,410 windows. The driver uses its first 1,203, then one additional window and an exact calculation of 1,231,496,337,447 returns. [Second crossing proof](EXACT_SECOND_758.md)

These three local calculations stand independently. Connecting a given row to blank also requires successful completion of every preceding cut from a known blank-tape reset. Once a trajectory has crossed K+2, strict reset growth excludes future visits to either K or K+2. The corresponding terminal is excluded by the [exhaustive last-reset calculation](TERMINALS_758.md).

## Keeping the parity of the certified return

In [the parity variant](cross_758_fast.cpp), the h-return at the end of a certified branch word has a known parity. Writing W = a+2c, each bulk move increases W by 5 or 9. Those charges are congruent modulo four. Every other charge in the endpoint certificate is exact. If the checker reports the bound g, the charge to that h-return is congruent to 2g modulo four. Thus the ending reset parameter has parity (s+g) modulo two. This parity statement concerns the certified h-return, which may occur after an intermediate first reset.

The variant takes the parities present among the current candidates in a block and closes that set under the certified parity transitions. If all reachable classes have a certificate, successive choices of these legal h-returns increase the reset and eventually leave the block. The last transition from a class of parity p and bound g yields an exit of parity (p+g) modulo two between h+1 and h+g. Candidates already above h are retained. A certified class with even g can also be advanced in this way when another class needs direct tracing, because each selected return stays in the same class. This allows exact proofs to discard entire parity classes whose trajectories are unnecessary for the stated reachability conclusion.

The default checker batches shared prefixes of exact returns. A scalar checker can independently verify any window that it accepts. [Prefix identities and audit](RETURN_PREFIX_758.md)

## Reproduction

Use Python 3.10+ and GCC or Clang with C++17 support. Specify `--reference` to run only the scalar C++17 checker. From this directory run the following command. The driver checks the blank entry, compiles the window checker, verifies both endpoints for each outgoing window, and replays the narrow candidate crossings with the unbatched counter map. Each section can also be rerun independently with `--section prefix`, `bridge`, `first`, `second` or `third`. Use `--chunk N` with a named section to check one zero-based window.

```sh
python3 check_blank_crossings.py --jobs 4
```
