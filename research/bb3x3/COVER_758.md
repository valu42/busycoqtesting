# A backward induction for holdouts #758 and #153

The remaining goal is halting from a blank tape. In the shared two-counter map, #758 reaches A(0,1) and then A(1,3). #153's blank orbit subsequently joins #758's. A halt anywhere on the #758 blank orbit decides both machines. The published reduction, the exact transition function and the earlier checks are available here. [Lean specifications](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB33/README.md) · [check_bb33.py](check_bb33.py) · [ranking](RANKINGS.md)

This proof supplies the inner 60,596,946 seeds of the larger verified interval. The later cover extends it to 11,177,973,024,732 consecutive seeds. [Combined proof](UNIVERSAL_758.md)

## Sufficient condition for a full decision

Set H = (3³⁰⁷ − 8,282,708,212) / 13,959,275, L = H − 12,000,000 and U = H − 3,403,055. The earlier verifier checks that every A(1,c) with L ≤ c ≤ U reaches the halting target A(1,H). Below L, consider this obligation for a given c:

> A(1,c) halts, or reaches some A(1,r) with c < r ≤ U.

If the obligation holds for every integer from a lower endpoint B through L − 1, then every A(1,c) with B ≤ c ≤ U halts. The proof is descending induction on c. A certificate with B = 3 would decide the blank machine. In this argument a successful return to a = 1 may be later than the first such return. A return above U reported for that chosen stopping rule does not exclude a halting continuation.

## Why two endpoints can certify a block

Starting from A(1,s), s ≥ 3, one map call yields (5,s) for odd s and (3,s+3) for even s. For a fixed parity of s the first coordinate is constant and the second increases with s. For the rest of a pass c is odd. Put q = ⌊(c + 1)/4⌋.

| Condition, in priority order | Action | Increase in a + 2c on continuation |
|---|---|---:|
| a ≥ 4q + 3 | **L** sends (a,c) to (a − 4q − 3, 6q + 5) | 5 or 9 |
| Otherwise, a even | Halt if a > c, otherwise return to A(1,a/2+c+2) | 5 on return |
| Otherwise, a ≤ c | **J** sends (a,c) to (3a + 2,c − a + 1) | 4 |
| Otherwise | **E** sends (a,c) to (3c + 8,1) | 8 |

The L rule combines the two odd-c bulk cases. In both c = 4q − 1 and c = 4q + 1 the original rules give the same update when a ≥ 4q + 3. For odd a, the remaining case E requires c = 4q − 1 and a = c + 2. For even a outside L, the other possible cases are precisely the halting tests or the return in the table. [Published rules](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA#A(a,_c)_Rules_and_Timings)

Along a shared word in L and J, increasing the initial parameter s makes a nonincreasing and c nondecreasing. Each step preserves these orders, and a has the same parity across the block. The L guard is therefore a lower interval of s. For odd a, the J guard is an upper interval. E occupies their complement. If both endpoints take E, the identities a = c + 2 and the opposite coordinate orders force both endpoint configurations to be identical, so the entire block coalesces. For even a, all seeds outside L halt or return.

Consequently, if endpoints of the same seed parity execute the same L/J/E word up to an even-a state outside L, every intermediate seed of that parity follows the word and then halts or returns. Start with the exact cost of the first call in units of a + 2c, then add the upper bound in the table for every letter and 5 for the final return. If the total is G, every returning seed satisfies r ≤ s + ⌊G/2⌋. Positive mass increments imply r > s. Testing the largest s in the block suffices. Individual seeds can use their exact stopping result if the upper bound is too loose.

## Reproducing and resuming

Place [cover_758.py](cover_758.py) beside check_bb33.py and use Python 3.10 or later. The first command verifies the input halting basin. The second certifies the obligations for the next four million integer seeds below it. Together they prove that all A(1,c) in the inclusive interval [H − 16,000,000, U] halt. Some may halt before reaching H.

```sh
python3 check_bb33.py --full
python3 cover_758.py
```

The default cover completes in 1 block for even seeds and 18,666 blocks for odd seeds. The longer run below also completed. It checked the full range from H − 64,000,000 through H − 12,000,001 using 1 even block and 303,799 odd blocks. Combined with the input basin, this certifies halting on [H − 64,000,000, U], an inclusive interval of **60,596,946** seeds.

```sh
python3 cover_758.py --far 64000000 --node-limit 2000000
```
 The checker splits blocks only between same-parity seeds and processes the higher half first. Both parities must cover the interval for the induction. The endpoint simulations are cross-checked against the original two-counter transition on small seeds, including exact and exhausted call budgets.

```sh
python3 cover_758.py --near 16000000 --far 20000000
python3 cover_758.py --near 64000000 --to-blank --node-limit 200000
```

Continue from a printed joint distance D by setting `--near D`. The history must have already certified all distances between the original boundary and D. An arbitrary `--near` value verifies only the specified return obligations. The exit code is zero on completing the requested interval and one on an incomplete run. Node and step limits are deterministic. A stopped run reports only its covered suffix and identifies which obligation remains. No run reported here reaches c = 3.
