# Following the blank orbit across the smaller #758 candidate halts

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

These three local calculations stand independently. Connecting a given row to blank also requires successful completion of every preceding cut from a known blank-tape reset. Once a trajectory has crossed K+2, strict reset growth excludes future visits to either K or K+2. The corresponding terminal is excluded by the [exhaustive last-reset calculation](TERMINALS_758.md).

## Reproduction

Use Python 3.10+ and a C++17 compiler. From this directory run the following command. The driver checks the blank entry, compiles the window checker, verifies both endpoints for each outgoing window, and replays the narrow candidate crossings with the unbatched counter map. Each section can also be rerun independently with `--section prefix`, `bridge`, `first`, `second` or `third`. Use `--chunk N` with a named section to check one zero-based window.

```sh
python3 check_blank_crossings.py --jobs 4
```
