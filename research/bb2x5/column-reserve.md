# Two exact accounts of the first dangerous carry on line 26

Use the aligned upper words of `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA`. A digit is $2u_i+e_i$, low pair first. A tick sends $P^9Q$ into the upper word. The same rules apply when an arbitrary initial low prefix has emitted $P^g$ before its first $Q$. Safe arrivals allocate pairs at the right end. An unabsorbed dangerous arrival at the fresh pair reaches the undefined instruction B3. [Physical and scalar dynamics](column-phases.md)

## A test for any incoming gap, including allocations

Scan a finite word from low to high, initially with $r=c=0$. At a digit with $e_i=0$, the bit of $g+c$ at position $r$ must equal $1-u_i$ for $Q$ to pass. Failure of this test means the tick survives. After each passed digit, update
$$
 c\gets c+(1-u_i)2^r,\qquad r\gets r+e_i.
$$
If all the bit conditions pass, the original $P^g Q$ halts exactly when $g+c<2^{r+1}$.

Indeed the incoming safe count at each position is $h=\lfloor(g+c)/2^r\rfloor$ as long as the dangerous flag survives. Digit 0 requires odd $h$ and sends $h+1$. Digit 2 requires even $h$ and sends $h$. Digit 1 always passes and sends $\lceil h/2\rceil$. Digit 3 always passes and sends $\lfloor h/2\rfloor$. These four cases prove both the bit condition and the recurrence. At the end the fresh-pair test is $h\le1$, which includes cells allocated during this gap. In particular a 0 immediately following a 0 or 2 blocks the dangerous carry at or before the second digit for every initial $g$.

For any prescribed low word $w$ of length $k$, its first passing $Q$ occurs within $2^k$ ticks. A column cannot suppress two successive input dangers. Let $g$ be the total number of $P$ it sends before that first passing $Q$. Placing $b$ digits 3 above $w$ makes the first $Q$ halt **if and only if** $g<2^{b+1}$. Each of the 3s halves the count rounded down and passes the dangerous flag. The end test is $\lfloor g/2^b\rfloor\le1$. An earlier $P$ may already have allocated a cell in the equality range $2^b\le g<2^{b+1}$. Thus the $0^{75}3^9$ example has a shorter companion $0^{75}3^8$ with exactly the same halting tick. Likewise $0^{81}3^8$ halts at tick 54,306,954,019 since $p(84)=173$. These are nonblank examples.

For arbitrary low data, transitivity places its starting state at a tick boundary of the ordinary cut-$3+k$ periodic orbit. Its initial safe count is at most the circular maximum $G_{3+k}$. The proven estimate $G_{3+k}+1\le10(3/2)^k$ therefore supplies a halting completion for **every** prescribed low word, with at most $\lceil\log_2(10(3/2)^k)\rceil$ additional columns. [Gap bound and blank-checkpoint permutations](column-traps.md)

## Change in a dyadic sum under the two operations

For a word of width $m$ put $r_i=\sum_{l<i}e_l$, $r=\sum_l e_l$ and
$$
 F=2^{-r}\sum_{i=0}^{m-1}(1-u_i)2^{r_i}
  =\sum_{i:u_i=0}2^{-\sum_{l\ge i}e_l}.
$$
Equivalently scan the digits with $F\gets(F+1-u_i)/2^{e_i}$, starting from zero.

**Safe tokens.** Send $P^g$ through a segment and let $h$ be its output safe count. On one pair, if the counts are $p,p'$ and the updated bit is $u'$, then $p=2^e p'+u-u'$. This is the quotient and remainder rule for the sparse subtraction. Multiplying by $2^{r_i}$ and summing cancels all the interior counts. On the fixed segment the result is exactly
$$
 F_{\rm after}-F_{\rm before}=g/2^r-h.
$$
At the physical right end, $h$ safe tokens allocate $a=\lceil h/2\rceil$ new pairs. Their $e$ bits are zero and all their $u$ bits vanish except the first if $h$ is odd. The added contribution to $F$ is $a-(h\bmod2)$. Hence on the complete growing tape
$$
 (m+F)_{\rm after}-(m+F)_{\rm before}=g/2^r .
$$

**Dangerous token.** Before a $Q$, $F\ge1$ guarantees that it stops inside the actual word. If it passed, every site with $u_i=0$ would have $e_i=1$. Those sites contribute distinct powers from $2^{-1}$ through $2^{-r}$, whose sum is strictly less than one.

When $Q$ stops at $j$, let $i_1<\cdots<i_s<j$ be the earlier $u=0$ sites, all of which had $e=1$. For old suffix counts $N_i=\sum_{l\ge i}e_l$, the exact change is
$$
 \Delta F=-2^{-N_j-1}
     +\sum_{v=1}^s(2^{s-v}-1)2^{-N_{i_v}}\ \ge -\tfrac12 .
$$
The stopping site gains an $e$ bit, halving its contribution. At $i_v$ the suffix loses $s-v+1$ bits and gains one, while contributions beyond $j$ stay fixed. If $Q$ passes the whole finite segment under ordinary matching, all selected $e$ bits are cleared and $F$ cannot decrease on that segment.

These identities concern genuine physical steps whenever the danger stops. The signed-tail family $3^k0^b$ can have $F=b$ and still eventually halt, for arbitrarily large $b$ and suitable $k$. Thus the one-step threshold $F\ge1$ cannot on its own be made an all-time safety threshold by raising its constant. Controlling the cumulative loss at actual stopping positions, relative to true extensions and the changing $r$, remains open. [Signed-tail construction](column-phases.md#a-family-of-nonblank-configurations-that-must-halt)

Run `python3 column_reserve.py` from this directory. The checker tests the identities as exact rationals, verifies the bit conditions and compares short physical words with the literal machine. [Source](column_reserve.py) · [Output](reserve-verification.txt)
