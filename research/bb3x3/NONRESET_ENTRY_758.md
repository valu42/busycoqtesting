# A sufficient condition for entry from an ordinary counter state

An actual #758 or #153 trajectory halts if it visits any odd/odd counter state $A(a,c)$ satisfying

$$
 h=(a+1)/2\text{ even},\qquad 2\le h\le1,012,257,878,130,399,645,022,
$$
$$
 H-61,410,570,681,246,030,619\le u=(a+2c-1)/2\le H-3,403,055-2,488.
$$

Each such state reaches a reset **inside the scale-20 halting basin within 553 counter calls**. The rectangle contains exactly **15,540,833,493,142,897,670,509,585,877,006,658,765,429** distinct nonreset states. This gives a sufficient condition directly on a blank-orbit state; whether the blank trajectory reaches this rectangle is open. [Extended contiguous halting basin](HALTING_COLLAR_758.md)

## Return from the rectangle

Put $F=61,410,570,681,246,030,619$ and $L=3,403,055$. For an odd/odd jump the guard is $3h\le u+2$ and the update is $(h,u)\mapsto(3h,u+2)$. The upper bound on $h$ is the largest even integer at most $(H-F)/3^{248}$. Therefore the first 248 jumps are legal. The initial $h$ is at least two and strictly increases throughout the run, so these jumps cannot reach $a=1$. The maximal initial run has length $k\le292$ because $h\ge2$ and $2\cdot3^{293}>H-L-2488+2\cdot293$. The aligned coordinates are $h_*=3^kh$ and $u_*=u+2k$. In particular $h_*$ is even and $0<U-u_*\le F+594$, with $U=3^{307}/D$ and $D=13,959,275$.

At alignment the initial ideal direction is $h_*/U=Dh/3^r$, where $r=307-k\le59$. The proof of the [physical shadow](TARGET_SHADOW_758.md) uses the signed pullback for an ordinary word, $h_*-\lambda u_*=R(h_l-\mu u_l)+B$ with $0<R\le1$, $0\le B\le14$. All four guard comparisons agree if the distance $|h_*-\lambda U|$ is greater than $F+2600$. For the uniform comparison, a pulled-back positive guard at depth $l$ has odd numerator over a power $3^t$ with $t\le l+2$. Since $h_*$ is even, its difference from $\lambda U$ is nonzero. The zero inverse guard also has nonzero difference. Divisibility therefore gives

$$
 D|h_*-\lambda U|\ge3^{\min(k,307-l-2)} > D(F+2600) \qquad (l\le248).
$$

The four inequalities exclude the exceptional and terminal guards, including the decision after a first bulk inside a group. They cover every exponent in the range, including the first decision at alignment. The last legal jump gave $h_*\le u_*<U$, and the next physical jump is illegal, so the aligned direction lies in the return interval or begins with a pair. At the first group boundary $m\ge r$, a surviving direction is thus an odd multiple of five over $4^p$ with $m\in\{r,r+1\}$ and $1\le p\le\lfloor m/2\rfloor\le30$. This cut uses only the even integer $h$ and the initial alignment. [Dyadic cut proof](HIGH_PAIR_HEADERS_758.md)

For $p\le28$ the [dyadic search](DYADIC_SURVIVAL_758.md) identifies every tail longer than 188 elementary calls. For $p>28$ the [header progression search](ORDINARY_HEADER_COVER_758.md) proves that every eligible tail returns within 188 calls. Thus each unlisted tail has its last guard at depth at most $60+188=248$. For every listed tail, the [exact guard clearance](TARGET_BASIN_758.md) at $m\le60$ exceeds $F+2600$ all the way through the return. The longest such tail has 243 calls before the final guard. A bulk and ordinary reset finish either kind of tail. Counting from the original state gives at most $k+m+243+2\le553$ calls. The mass $W=a+2c$ strictly increases and gains at most nine per call. At return $W=2s+1$, so the reset seed satisfies $u<s\le u+\lfloor9\cdot553/2\rfloor=u+2488$. Both bounds place it in $[H-F,H-L]$, where it halts. [Dyadic tail exhaustion](DYADIC_SURVIVAL_758.md)

For even $h$, the original state is $a=2h-1$, $c=u-h+1$, with odd $c$ exactly when $u$ is even. There are 30,705,285,340,621,312,539 allowed even masses and 506,128,939,065,199,822,511 allowed left coordinates independently.

```sh
python3 nonreset_entry_758.py
```

## A criterion covering both counter parities across the wider mass band

Write $w=\lfloor(a+2c)/2\rfloor$. Every counter state with $1\le a\le9,576,859$ and

$$
 H-F+30\le w\le H-L-2492
$$

also halts, for either parity of either counter. The [earlier axis calculation](AXES_758.md) obtains a larger left-counter cutoff at the central crossing. This criterion is uniform over the newly joined scale-20 band.

For odd $a,c$ let $h=(a+1)/2\le14,365,290$. The even case for $h$ is the rectangle above. For odd $h$, write $h=3^j v$ with $3\nmid v$. If $v=1$, reverse $j\le15$ jumps to $A(1,w-2j)$, a reset in the basin. Every inverse jump is valid: its predecessor is a positive odd/odd state and its forward jump has output $h'\le u'$. Thus the given descendant halts too.

For the remaining odd $v$ let $e$ be the least integer with $3^e>Dv$. The ideal direction after the physical launch is $Dv/3^e$. Indeed the last legal jump and the first illegal one are those selected by comparing the successive $3^i h$ to $U$. At the transition this comparison differs from $U$ by at least $3^i/D$, since $Dv$ is never a power of three; this is larger than the shift from $U$ to the physical mass. More explicitly, $r=e+j$ is the least exponent with $3^r>Dh$ and $r\le30$. At $k=307-r$, $U-3^kh\ge3^k/D>F+2600$ and $3^{k+1}h-U\ge3^{k+1}/D>F+2600$. The successive jump tests are monotone, so the launch takes precisely $k$ jumps.

The [integer enumeration](small_odd_entry_758.cpp) checks every one of the 4,788,429 possible odd primitive $v>1$ up to 14,365,290. All these directions reach the open ordinary-return interval without an exact guard contact, within 91 elementary calls. The first $v$ attaining 91 is 8,818,939. The nonzero pulled-back guard at any reached depth therefore has aligned clearance at least $3^{\min(k,307-91-2)}/D>F+2600$ by integer divisibility, regardless of the parity of $h_*$. This certifies the ordinary return inside the basin. For $a,c$ odd, this argument in fact applies through $a=28,730,579$ across the same trimmed band.

For odd $a$ and even $c$ the first call gives odd/odd counters with left coordinate $3a$ and $u'=w+4$. The stated limit on $a$ ensures $h'=(3a+1)/2\le14,365,290$, and the extra four units of upper clearance cover this call. For even $a$ the original $c$ is larger; even $c$ gives an immediate halt, while odd $c$ gives a reset at $s=w+2$. Both cases are settled.

```sh
c++ -O3 -std=c++17 small_odd_entry_758.cpp -lgmpxx -lgmp -o /tmp/small-odd-758
/tmp/small-odd-758
```

## Testing a large left counter at the crossing

This also applies to a left counter with up to 140 digits. At an odd/odd state set $h=3^j h_0$ with $3\nmid h_0$. If $h_0$ is even and $h_0\le1,012,257,878,130,399,645,022$, the state halts whenever

$$
 H-F+584\le u\le H-L-2488.
$$

Indeed $h\le u<H<3^{293}$ gives $j\le292$. Each inverse jump changes $(h,u)$ to $(h/3,u-2)$ and is a legal predecessor: its forward guard is equivalent to $h\le u$ and its right counter is positive and odd. The inverse chain ends in the rectangular halting set above. The same argument works with odd $h_0\le14,365,290$ by the primitive-direction calculation (or a basin reset for $h_0=1$). At the central crossing this enlarges the previously available primitive-coordinate test for the even $h_0$ class. [Earlier inverse-jump test](AXES_758.md)

The [odd primitive coordinate tests](ORDINARY_HEADER_COVER_758.md) cover coordinates through 211,637,975,937,205 with 263 possible exceptions and give a check across the full left-coordinate range.
