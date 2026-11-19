# Raw time at the fourth blank checkpoint

The blank machine #758 reaches the reset $A(1,18{,}378{,}934{,}934{,}402{,}308)$ after between **7.528 × 10⁴⁶ and 1.119 × 10⁴⁷ raw steps**. The #153 clock is exactly 50,707 steps smaller. These bounds time an event that both machines demonstrably reach. Neither machine has a proved halting time from blank. [Blank crossing certificates](POWER_CROSSINGS_758.md) · [Exact final segment](fourth_clock_758.py) · [Verifier](crossing_clock_758.py)

| Clock at the reached reset | Lower bound | Upper bound |
|---|---:|---:|
| #758 | 75,287,784,527,483,315,086,258,653,649,976,784,825,150,292,446 | 111,828,955,391,337,651,168,241,433,086,744,445,106,293,997,533 |
| #153 | 75,287,784,527,483,315,086,258,653,649,976,784,825,150,241,739 | 111,828,955,391,337,651,168,241,433,086,744,445,106,293,946,826 |

## Timing a whole interval of reset seeds

Write $r(z)$ for the parameter of the first blank-orbit reset at or beyond $z$ in the sections under consideration. Reset parameters strictly increase. For a section split at cuts $z_i$, time from $r(z_i)$ to $r(z_{i+1})$ counts consecutive disjoint portions of the same orbit.

Inside each of the four archived crossing grids, $r(z)\le z+100{,}000$ holds even at a new cut inside a window. To see this, consider the chain of selected returns that witnesses passage across the original window. In the general worker a symbolic return consists of the opening, fewer than 40 initial Js and at most 10,000 individual updates. The plain exact worker uses at most 5,000 updates after the opening batch. The cached exact worker's two prefixes add at most 128 and 256 updates, followed by at most 4,500, or it falls back to the plain budget of 5,000. In the even worker, the launch takes fewer than 40 updates, then at most 256 cached phases and 5,000 further phases each use at most two updates, with one final reset and an optional odd-to-even normalization of at most 73 seed units. The symbolic version of the same normalization adds at most 73 to the general bound. Each elementary update increases $W=a+2c$ by at most nine, and a reset gain is half the mass gain. Thus every selected increment is below 100,000. Any earlier intervening reset only reduces the gap. In the three short-word power-gate corridors following these grids, the common ordinary words give the same bound directly. The small coalescence gaps around gate exits are left to the global clock estimate. [Grid and gate verifier](check_power_crossings_758.py) · [General symbolic worker](reset_cover_758.hpp) · [Cached worker](return_prefix_758.hpp) · [Even worker](even_power_prefix_758.hpp)

For a half-open interval $[l,h)$, run the smallest and largest seeds of one parity together. Once the first move fixes the left coordinate, it is nonincreasing and the right coordinate is nondecreasing as a function of the seed throughout a common ordinary word. At each call, verify the guards at the two endpoints and check that the intervening left coordinates of this parity cannot include an early reset. Stop on a common even-left return. Failures subdivide the interval up to eight times. An unresolved piece contributes only the global upper estimate.

For every verified call, bound its raw cost below by $3m^2$, where $m$ is the smallest possible value of $\min(a,c)$ in the endpoint rectangle. Bound its cost above by $3M^2+30W_{\max}+65$ using the largest possible value $M$ of that minimum and the largest rectangle mass. The clock polynomials imply both inequalities. Sum the bounds along the common word. Gain in $W$ is 8 for the even-seed opening, 4 for each J, 5 for a return and 5 or 9 for a bulk. Divide summed mass gains by two to get lower and upper bounds on the first-return seed increment. The two bulk charges agree modulo four, so the output parity is fixed for each input parity. [Ordered-word argument](CONFLUENCE.md) · [Raw branch costs](timing_758.py)

On a fixed parity loop, use the lower cost divided by upper seed gain and the upper cost divided by lower seed gain. For alternating parities, group the returns in pairs and add the corresponding costs and gains before taking the ratios. If both parities lead to the same parity, discard at most one transient for the lower bound and add its maximum cost for the upper bound. An alternating interval can likewise leave one unpaired return. Since the distance from $r(l)$ to $r(h)$ lies between $h-l-100{,}000$ and $h-l+100{,}000$, these ratios bound the total time spent there without selecting a particular seed or residue.

## Adding the clock on uncovered portions

Let $S(W)=11W^3/1058+9W^2+30W$. The angular potential $P$ gives, on a continuing call with mass gain $g$, the inequality
$$
t+W^2(P'-P)\le (33/1058)gW^2+56W+65.
$$
Since $|P'|\le 1/2$ and $g\le9$, replacing $W^2 P'$ by $(W+g)^2P'$ on the left enlarges the right by at most $9W+41$. The result is at most $S(W+g)-S(W)$ since $g\ge4$. Summing telescopes. At resets of mass $W\ge23$, the odd-phase potential is linear on the first cell and $W^2P(1/W)=(5913\cdot23/146004)W$ increases with $W$. Thus between two such resets, raw time is at most $S(W_{\rm end})-S(W_{\rm start})$. The initial blank map configuration has nonpositive potential and consumes two entry steps. [Angular upper certificate](ANGULAR_CLOCK_758.md)

Begin with $2+\lfloor S(1+2\,\mathrm{MERGER})\rfloor$ as the upper bound through the entry to the exact fourth segment. For a verified interval, subtract any guaranteed saving relative to the generic difference in $S$. For the lower bound, start with the proved raw clock through the exact jump beyond the third pair, sum the interval lower bounds, then add the exact time from the fourth merger to the stated checkpoint. The same exact final duration also goes into the upper bound. Run `python3 crossing_clock_758.py` from this directory with the other research checkers present. [Third-pair jump](JUMP_AFTER_THIRD.md) · [Fourth-pair clock](fourth_clock_758.py)
