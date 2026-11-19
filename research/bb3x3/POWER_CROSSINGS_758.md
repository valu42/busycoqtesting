# Crossing the fourth halting pair on the blank orbit of #758

The four links below join the known reset at the doubled power of three, $2\cdot3^{32}+41{,}023$, to the fourth candidate pair $K,K+2$, where $K=17{,}430{,}344{,}744{,}167{,}562$. At the pair the consecutive reset parameters are **17,430,344,744,167,527** and **17,430,344,744,167,627**, or $K-35$ and $K+65$. Both halting seeds are consequently bypassed. Its only possible last resets are the two skipped seeds. The [post-crossing calculation](FOURTH_GATEWAY_758.md) then advances the orbit to a common reset at **18,378,934,934,402,308**.

| Starting reset | End cut | Verified windows | Reset reached from the end cut |
|---:|---:|---:|---:|
| 3,706,040,377,744,705 | 5,558,504,660,484,436 | 1,853 | 5,559,060,566,642,762 |
| 5,559,060,566,642,762 | 10,006,309,019,799,870 | 2,224 | 11,118,121,133,201,395 |
| 11,118,121,133,201,395 | 16,484,970,113,975,417 | 2,684 | 16,677,181,699,675,672 |
| 16,677,181,699,675,672 | 17,354,320,242,804,343 | 339 | 17,430,344,744,167,627 |

The starting reset follows from the earlier [blank crossing](BLANK_CROSSINGS.md), the [jump beyond the third pair](JUMP_AFTER_THIRD.md) and the merger of all 36 exits at the doubled power. Each window certifies that **every** reset from its starting cut through 5,000 above the cut reaches a reset in the corresponding 5,001-seed interval at its end. These windows compose by inclusion. The first leg uses strides of $10^{12}$, and the others use $2\cdot10^{12}$. Each last stride stops at its stated cut. The first three end cuts lie inside [power-gate corridors](POWER_GATES_758.md). Endpoint guards verify the corridor from the end cut, and the 20, 37 and 5 possible exits, respectively, merge at the reset in the last column.

## Selecting the fourth crossing

Put $B=17{,}354{,}320{,}242{,}904{,}343$. The last cut is $B-100{,}000$. All 5,001 incoming possibilities coalesce at $A(1,17{,}354{,}320{,}242{,}846{,}420)$ along 7,963 distinct first-return edges. The following 424 first returns reach $A(1,B+109)$, and the next reaches the odd seed $B+208$. The [fourth-candidate corridor](FOURTH_GATEWAY_758.md) gives a common odd first-return word through $K+1$. Its seven bulk updates make its exact gain periodic in the seed modulo 256. From $B+208$, the path takes one return before entering an eight-return period of total gain 768. The checker skips 98,990,236,018 additional complete periods. The first reset above $K+2$ follows **791,921,888,157** first returns after $B+208$.

Literal replay from each of $K$ and $K+2$ gives the same terminal input $A(11{,}620{,}229{,}829{,}445{,}098,11{,}620{,}229{,}829{,}445{,}097)$, whose 39th call from either seed halts. The [inverse rules](TERMINALS_758.md) exhaust 255 reverse states to depth 43. The only last resets are $K$ and $K+2$, both at depth 38. Strictly increasing reset parameters exclude both after the displayed crossing.

## Reproduction

The [window report](power_crossings_758.tsv.gz) identifies the engine and six output fields of each successful window. The [driver](check_power_crossings_758.py) checks that the 7,100 rows form the four stated grids. Its default command recompiles and reruns the C++ windows, verifying the exit inclusion of each one. General and even-only engines may certify different supersets of possible exits. Both establish the same inclusion. The report's blocks and calls measure computational work, and the even-only engine can normalize an odd reset in the same operation. The report-only command checks the archived bounds and gate mergers without redoing the C++ calculations. [Exact fourth crossing and ancestry](exact_fourth_758.py)

Two optional side windows end just before the [short exceptional-branch candidates](EXCEPTION_TERMINALS_758.md). Each begins on a grid certified above. The first, from 5,494,040,377,744,705 to 5,494,990,037,891,759, selects the actual power-33 phase. All starting seeds in the outgoing window merge along 7,525 distinct edges. After 381 returns they reach an even reset inside the power-33 corridor, where the odd subsequence repeats modulo 64 after four first returns of total gain 320. The last odd reset before $3^{33}-70$ is $3^{33}-216$ and the next odd reset is $3^{33}-54$. The second side window, from 15,798,121,133,201,395 to 15,799,435,294,410,882, reaches a cut from which elementary first-return replay excludes both members of the middle exceptional pair. Both side windows have their six archived fields in the [phase verifier](exception_power_phases_758.py).

```sh
python3 check_power_crossings_758.py --jobs 4
python3 check_power_crossings_758.py --report-only
python3 check_power_crossings_758.py --report-only --exception-phases
python3 check_power_crossings_758.py --leg fourth --chunk 338 --engine general
python3 exact_fourth_758.py
```

## The open link after the fourth pair

From the post-crossing reset at 18,378,934,934,402,308, a reset in the window beginning at 30,018,927,059,399,750 would suffice to reach $2\cdot3^{34}+32{,}211$. The simple even word of this doubled-power gate starts at 20,012,618,039,599,810, and the odd word starts at 30,018,927,059,399,751. On the two-trillion grid between the checkpoint and the window, **4,777 of 5,820 windows have an entirely symbolic crossing proof**. The other 1,043 stop at a request for a direct trace. These separated successes do not yet connect the two checkpoints. The [survey](survey_next_power_758.py) can print the unresolved zero-based indices. A success verifies both exit bounds with the ordinary crossing code. The build flag stops that code before its first direct call.

```sh
python3 survey_next_power_758.py --list-hard
```
