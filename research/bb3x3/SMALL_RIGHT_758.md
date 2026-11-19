# A small right counter forces a decision in the #758 halting band

Let $B=H-11{,}177{,}976{,}427{,}786$ and $U=H-3{,}403{,}055$. Every reset $A(1,s)$ with $B\le s\le U$ is known to halt. For **every** state $A(a,c)$ with $2B+1\le a+2c\le 2U+1$ and **every positive odd $c<2^{24}$**, either the machine halts or it reaches a reset in at most **844 ordinary counter calls**. Both parities of $a$ are covered. If the initial mass is at most $2U+1-7{,}592$, any such reset is in the known basin. [Verified reset basin](UNIVERSAL_758.md)

This excludes a right counter below $2^{24}$ from a hypothetical escaping blank orbit throughout the trimmed strip. Its right counter stays odd between resets. Consequently each pure bulk run starting in the strip has at most **750 consecutive moves** while its endpoint mass stays below $2H$. Indeed $c+7$ grows by at least $3/2$ at each bulk move, its initial value is at least $2^{24}+8$, and $(2^{24}+8)3^{751}>(H+7)2^{751}$.

## Interval proof

For each interval $l\le c\le h$ of odd right counters and each parity of $a$, the checker tracks the state with largest $a$ and smallest $c$ and the state with smallest $a$ and largest $c$. They enclose all eligible states in the opposite coordinate order. A bulk move has $q=\lfloor(c+1)/4\rfloor$ and sends $(a,c)$ to $(a-4q-3,6q+5)$ when $a\ge4q+3$. A jump sends $(a,c)$ to $(3a+2,c-a+1)$ when $a\le c$ and $a$ is odd. Both maps preserve the opposite coordinate order and preserve agreement on the parity of $a$.

The checker takes a common bulk if its smallest-$a$ endpoint qualifies, or a common jump if neither endpoint permits a bulk and the largest-$a$ endpoint qualifies for a jump. If neither endpoint permits a bulk and $a$ is even, the next call halts or returns to $a=1$. Any undecided interval splits in two. All accepted words end at this even decision, so no exceptional branch is needed.

For the long initial bulk run, put $x=\lfloor(c+1)/4\rfloor+3$. One bulk sends $x$ to $\lfloor3x/2\rfloor$ and decrements $a$ by $4x-9$. After $n$ bulk moves the total decrement is $8(x_n-x_0)-9n+4o$, where $o$ counts the odd $x_i$ for $0\le i<n$. A table applies this identity in groups of 12, as translating $x_0$ by $2^{12}$ translates $x_{12}$ by $3^{12}$ without changing these parities. The decrement increases monotonically with the initial $c$. Requiring the smallest initial $a$ to cover the largest total decrement certifies every individual bulk guard. The checker also tests all 4,096 table entries against the original scalar counter rules.

The disjoint bisection tree has 1,077,697 nodes and 538,849 accepted leaves. Every live call preceding the final decision adds at most nine to the mass, and a final return adds five. The upper clearance is therefore $843\cdot9+5=7{,}592$. The result about reaching a decision covers the untrimmed band as well. The top clearance matters. At mass $W=2U+1-5{,}448$, the state $A(W-2,1)$ first returns to $A(1,U+1)$ after exactly 786 calls. Its return falls just outside the universal basin.

Run the [verifier](check_small_right_758.py) beside the two-counter implementation.

~~~sh
python3 check_small_right_758.py
~~~
