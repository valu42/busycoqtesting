# Line 23 · the three-cell return and two spliced tapes

Use the line 19 transition table starting in **B** on blank, which is the reflected, relabeled line 23 blank orbit. The suffix U begins immediately to the right of the scanned 3 when a new B3 guard starts. A lethal guard sends B, B, A into U and receives A on all three calls. [Machine correspondence](line19-pair.md) · [Guard criterion and blank counts](spaghetti-guards.md)

**If U starts with `022` or `320`, this guard cannot receive three A replies.** The first B returns A with the original three cells rewritten to `222`, without visiting their exterior. The second B on `222` sends one B to the next cell. If that child returns A the second call returns B. If it returns B the second call returns A and leaves `020`. Now the third A returns B in exactly seven instructions, leaving `232` and again staying within the three cells. A child that never returns leaves that guard pending. These paths account for arbitrary tape beyond the first three cells. The proof gives a specific target for the blank orbit: exclude guard launches outside these safe initial patterns, or handle any others separately.

## Histories that a local test merges

Choose two configurations from the actual normalized-B blank run. Translate each so its head is at zero. Copy the cells strictly left of zero from the first configuration and all cells from zero rightward from the second. In both examples the sources have control B and have just moved right.

| Effect of the splice | Left source steps and head | Right source steps and head | Matching cells about the join | Outcome on the spliced tape |
|---|---|---|---|---|
| A3 halt | 365, −1 | 645, +7 | −4 through +3 | Halts at −6 after 308 steps |
| Third A on `022` | 10,055, −9 | 107,420, +136 | −10 through +9 | A `3233` launch begins at 1,286; the third A sees `022` and returns B |

For the first splice, A scans `03` at step 127 and the root at −6 sends its first B into `3023…`. The three replies reach −6 at 302, 304, and 306, all in A. The third call entered `223…`. Two more defined instructions place the head on the undefined A3. Under reflection the physical line 23 machine on the corresponding spliced tape halts at +6 on B4.

For the second splice, the root at −15 receives A at 1,733 and A again at 1,739. Its third call starts at 1,740 with `022…` in U and returns B at 1,751. This physically realizes the `3233` launch that survives some local filters. Both source configurations come from blank; each splice combines different histories.

For a matching interval with l cells to the left and r to the right, a contiguous factor that includes a mismatch on both sides needs at least l+r+2 cells. Every shorter factor of the spliced configuration therefore occurs in at least one of its genuine sources, including factors that mark the state, scanned cell and direction. Consequently a test that accepts any tape whose individual factors of length at most 9 occur on this orbit accepts the first splice, which halts. The same per-factor test through length 21 accepts the second, which violates the observed third-entry pattern. The first source heads even agree modulo 8. These witnesses show why a decision based on those factors alone would lose information about how the two tape halves were produced.

From `research/bb2x5`, `python3 frontiers/check_line23_splice.py` verifies the strip paths directly from the transition table, rebuilds all four source configurations from blank and runs both complete spliced tapes. [Executable checks](check_line23_splice.py)
