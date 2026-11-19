# The exact crossing selected below the fifth halting pair

Let $K=40,486,323,621,582,648$. Every reset $A(1,s)$ in the interval
$$
39,752,584,607,270,532\ \le s\le\ 40,386,323,621,587,648
$$
reaches the same reset at **$K-198,990$**. Exactly 1,054 further first returns give consecutive resets **$K-98$ and $K+118$** at the crossing. Both $K$ and $K+2$ halt if used as starting resets. The [connected window proof](FIFTH_BLANK_CROSSING_758.md) now proves that the blank orbit enters this interval and takes the stated crossing.

## Synchronization

Write $B$ for the lower endpoint and $C=K-10^{14}$. The [two parity words](MIXED_TERMINALS_758.md) increase the reset parameter by at most 99 throughout $[B,C+5,000]$. Each starting point therefore reaches $[C,C+5,000]$. The existing transfer from there reaches $[K-10^{11},K-10^{11}+191]$. Applying the same [window checker](cross_758_fast.cpp) to all 5,001 possible starts at $K-10^{11}$ gives the singleton $K-198,990$. The new transfer used 7,793 symbolic blocks and 20,501,371 individual first returns. Literal replay from the singleton gives the stated crossing. The exact [checker](fifth_crossing_758.py) replays both transfers when given a compiled worker.

## What reaching this pair from blank would require

A trajectory starting below $B$ that reaches either candidate as a reset must cross the entire interval without visiting a reset there. There is also a long stretch where it must avoid the exceptional rule E. Write $W=a+2c$ for its mass,
$$
W_0=79,694,553,903,668,291,qquad W_1=2(C+5,000)+1-94\cdot9.
$$
Every E at $W_0\le W\le W_1$ gives a reset in the bypass interval within 94 elementary updates. Indeed the E input is $(c+2,c)$ with $c\equiv3\pmod4$, so $W\equiv11\pmod{12}$. The post-E state is $(W+6,1)$. From there the exact word is $L^{88}JL^3R$. The verifier checks both extreme permissible masses. As the starting $W$ increases along the common word the left counter is nondecreasing, the right counter nonincreasing, and both parities are fixed at each step. The bulk, jump and return inequalities at the endpoints then establish all intermediate guards. The final reset mass is between $2B+1$ and $2(C+5,000)+1$ because each update adds at most nine. The preceding possible E mass $W_0-12$ fails this particular word.

The passage from the first state with $W\ge W_0$ to the first with $W\ge W_1$ therefore contains only ordinary calls. Each mass overshoot is at most eight. After dropping incomplete bulk pairs at the ends there are at least **59,894,074,417,007 consecutive ordinary blocks**. Apply the [word-count theorem](FACTOR_COMPLEXITY_758.md) with $T=7,700,000^2$, $n=66$ and mass-coordinate upper bound $K$. The verifier checks $3^{66}>9TK$ and that at least $T+66$ blocks fit. Consequently a blank trajectory reaching this specific candidate pair must realize at least **7,700,000 distinct length-67 fine words in one ordinary excursion**. This necessary condition leaves the fifth crossing on the blank orbit unresolved.

Run from the BB(3,3) research directory with a C++17 compiler and Python 3.10 or newer.

~~~sh
c++ -O3 -std=c++17 cross_758_fast.cpp -o cross_758_fast
python3 fifth_crossing_758.py --worker ./cross_758_fast
~~~
