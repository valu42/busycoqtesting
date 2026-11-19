# The fourth candidate belongs to an infinite family

For every $m=34+60j$ with $j\ge0$, put $P=3^m$ and

$$K_m=\frac{162P-1528}{155}-2m.$$

Both $(1,K_m)$ and $(1,K_m+2)$ reach the same terminal, beginning with the previously isolated fourth candidate $K_{34}=17,430,344,744,167,562$. Every member also has a macroscopic interval of earlier resets from which the orbit passes the pair alive. This gives explicit recurring terminals and an obstruction to hitting them from below. Reachability from the blank start requires separate evidence for each scale.

## Terminal pair

Write $Q=P/3$. The even opening I and $m-1$ J moves take seed $s=K_m$ to

$$(a,c)=(4Q-1,\;s-2Q+2m+3).$$

The right counter is positive here and after every earlier J. The next four moves are C, C, J, B, where C and B denote bulk moves on $c\equiv3$ and $c\equiv1\pmod4$. For $s+2$, the first bulk is B, with both seeds reaching exactly the same state. The gap $G=a-c$ after the last move satisfies

$$8G=486Q-155s-310m-1520=8.$$

The final $a$ is even, so gap one is a terminal. The seed is an even integer since the numerator is even and divisible by 155 in this exponent class. The congruence $3^{60}\equiv1\pmod{155\cdot16}$ preserves the low four bits of $Q$ and $s+2m$ at every later member. Three bulk moves therefore retain their required input residues. Substituting $s$ leaves counters affine in $Q$, with constants independent of $m$. For the successive C, C, J, B guards the slopes of $a-c$ have signs $+,+,-,+$. All counter slopes are positive. The two final slopes are equal to $324/155$. Checking the smallest $Q$ verifies the constant terms and all guards throughout the progression.

The [finite inverse-forest checker](terminal_forest_758.py) finds exactly the two claimed last resets for each of the five family members before the distinguished terminal $H$.

| $m$ | Inverse states | Greatest depth |
|---:|---:|---:|
| 34 | 255 | 43 |
| 94 | 851 | 109 |
| 154 | 1,375 | 159 |
| 214 | 1,907 | 233 |
| 274 | 2,713 | 288 |

At $m=154$ there are also genuine earlier resets. Starting at either $K_{154}-664$ or $K_{154}-662$ gives $K_{154}$ on the very next first return, as the original unbatched checker verifies.

## Missed interval at every member

Set $z=(s+2m)/P$. Every reset with $1.0430\le z\le1.0438$ passes $K_m+2$ alive.

* Every odd input in $1.0430\le z\le1.04517$ follows $J^mL^7R$. Each L charges 5 or 9 units of $a+2c$. The $m$ J moves charge 4 each and R charges 5. The reset increment is positive and even. All resets stay odd through the crossing of the two even candidates.
* Every even input in the smaller interval follows $I J^{m-1} L L J L L J J J L R$. Its five L moves force an odd reset increment bounded above by $2m+35$. The return enters the odd interval strictly below $K_m$. The distance to $K_m$ at the right endpoint is already enough at $m=34$ and increases geometrically thereafter.

The homogeneous counters after the initial prefix are $(2,z-1)$ for an odd seed and $(4/3,z-2/3)$ for an even seed, in units of $P$. Their true counters differ from $P$ times these expressions by at most three. Each L maps the homogeneous counters to $(a-c,3c/2)$ and J maps them to $(3a,c-a)$. Replacing a previous error bound $e$ by $3e+7$ bounds the exact corrections in either coordinate. All positivity and strict branch inequalities are affine in $z$, so it suffices to test the rational interval endpoints. The [checker](fourth_family_758.py) verifies that the margins exceed the rounding errors even at $P=3^{34}$. This proves an interval with at least $0.0008P-1$ integer seeds at every family member.

Run the arithmetic and inverse-forest checks with `python3 fourth_family_758.py`.
