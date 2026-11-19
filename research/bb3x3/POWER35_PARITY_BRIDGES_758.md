# Absorbing parity intervals on the power-35 blank orbit

The blank tapes of #758 and #153 both reach $A(1,59{,}450{,}686{,}841{,}407{,}190)$. For #758 the raw time there is between $2.63885\times10^{48}$ and $3.95124\times10^{48}$ transitions. #153 reaches the same reset 50,707 transitions earlier. The proof follows the [power-35 grid](double35_frontier_758.py) from its known blank start and uses five shortcuts inside that grid. [Earlier exact blank reset and incoming clock](POWER35_INNER_SKIP_758.md)

At each listed entry cut, every one of the 5,001 possible incoming seeds either has the stated parity already or reaches it after one genuine first return. In each listed word the number of L operations is 3 modulo 4. Each L adds 5 or 9 to the mass, each J adds 4, and the final return adds 5. The total mass increase is divisible by four, so the seed gain is even. Hence the seed stays in the selected parity, increases on every complete return, and reaches the far end of that word. The limits are checked by replaying both endpoints of a fixed-parity interval. Along a shared prefix the first counter is nonincreasing with the input seed and the second is nondecreasing. This establishes the guards at all intermediate seeds. The checker also requires the first counter to stay above one until the ordinary return. [Guard and parity checker](power35_parity_bridges_758.py)

| Grid cut to cut | Absorbing parity | Word following the launch, before the return | Maximum seed gain | Forced reset beyond the word | Number of first returns from the entry strip to that reset |
|---|---|---|---:|---:|---:|
| 1686 to 1700 | Even | LLJJJLLLLL | 112 | | |
| 1701 to 1782 | Odd | LLLLJLLL | 106 | 58,943,610,593,404,820 | 4,088,827,510,217 to 4,088,827,510,274 |
| 1795 to 1800 | Odd | LLLLJLLJLLLLL | 126 | 59,032,949,564,004,206 | 228,847,291,387 to 228,847,291,435 |
| 1807 to 1883 | Even | LLJJJL | 94 | 59,450,686,841,407,190 | 4,236,857,452,209 to 4,236,857,452,267 |
| 1894 to 1904 | Odd | LLLLJLLJJL | 110 | | |

The three reset-count ranges give the exact minimum and maximum over all 5,001 entries. For a word containing $b$ bulks, its gain repeats when the seed increases by $2^{b+1}$. On a repeated residue the checker skips as many copies of the cycle as fit within the word, then evaluates the short suffix directly. At each of the three sharp upper boundaries it considers every possible last reset within one maximal gain below the boundary. All exits merge along 508, 745 and 758 distinct first-return edges, respectively. For the central clock calculation the original [mass-interval proof](FIFTH_BLANK_CLOCK_758.md) applies up through cut 1883. The bounded increases across the parity bridges satisfy its 100,000-seed overshoot limit.

```sh
python3 power35_parity_bridges_758.py --counts --clock
```
