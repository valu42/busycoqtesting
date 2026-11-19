# Wily Coyote as one integer map

A sufficient condition to prove both #531 and #532 run forever from blank is that all iterates of the following single integer stay negative:

$$
n_*=-227\,089\,934\,777\,573\,210\,432.
$$

The map $F$ has no machine-state parameter. Its domain is the integers not divisible by three.

| Input, testing the exceptional value first | $F(n)$ |
|---|---|
| $n=-2$ | $-1$ |
| $n\equiv0\pmod8$ | $n+21$ |
| $n\equiv4\pmod8$ | $n-3$ |
| $n\equiv2\pmod4$ | $3+4F((n-6)/4)$ |
| $n\equiv3\pmod4$ | $2F((n+3)/2)$ |
| $n\equiv1\pmod4$ | $2F((n-9)/2)$ |

Starting at $n_*$, the sign condition holds through the last paired update at **$2^{256}$ blank sweeps**. The all-time sign condition and the actual blank outcomes remain open. This particular seed is at sweep 3,442,378. An earlier blank checkpoint just after sweep 1,168 has positive iterates.

## From two blank sweeps to one map

Use the four-mode [sweep reduction](check_bb33.py) with the protected prefix removed. Drive the suffix by alternating $s_0,s_1$, starting with 00. At the beginning and end of every pair the first two cells are 00. The two inputs they emit to the remaining tail are $s_3,s_2$. On a nonempty tail $s_3$ flips the first bit and stops. The following $s_2$ leaves that flipped bit in place and transmits exactly the carry a single $s_0$ would have emitted on the original bit. On the initially empty tail the first pair creates **001100**. The tail stays nonempty thereafter. Thus from sweep 2 onward, repeatedly apply $s_0$ to this six-bit seed.

Write a tail $v$ of length $\ell$ as a little-endian integer $z=\sum_i v_i2^i$. Put $B=2^\ell$ and $n=3z-B$. The rational $n/3$ has the binary digits of $v$ followed by $T=(10)^\omega$ in the 2-adic integers, since $1+4+4^2+\cdots=-1/3$. This encoding uses $B$ only to remember the physical edge.

On an infinite binary word the four carries are invertible maps of the binary tree. An input bit of $n/3$ is $b=n\bmod 2$, and the integer for the remaining tail is $(n-3b)/2$. Let $J(n)=n+3(1-2b)$ represent $s_3$, the first-bit flip. Consecutive carries $s_3,s_0$ agree with $s_2$ on the infinite word. If $F$ represents $s_0$, it follows that $s_2$ acts as $F(J(n))$. For $s_1$, an even input $2y$ gives $3+2J(y)$ and an odd input $3+2y$ gives $2F(y)$. Substituting in the two branches of $s_0$ gives the displayed recurrence. At $n=-2$ the digits are $(01)^\omega$ and $s_0$ sends them to $T$, giving $F(-2)=-1$. Recursive inputs decrease in absolute value for $|n|>9$. The finitely many nonmultiples of three in $[-9,9]$ reach a base case by inspection.

## Exact physical update, including every extension and halt

Let $v'=F(n)$. A halt occurs if and only if $v'\not\equiv n\pmod3$. Otherwise the following table gives the next actual pair.

| Status at the physical edge | Possible $v'$ (inclusive) | Next $(n,B)$ |
|---|---|---|
| The carry stops internally | $[-B,2B-3]$ | $(v',B)$ |
| $s_3$ reaches the edge | $[-4B,-B-3]$ | $(v',4B)$ |
| $s_2$ reaches the edge | $[-7B,-4B-3]$ | $(v',16B)$ |
| $s_0$ reaches the edge | $[-28B,-25B-3]$ | $(v'+26B,2B)$ |

To verify the table, run each possible arriving carry on the virtual $T$. The four outputs for $s_0,s_1,s_2,s_3$ respectively have numerators $-28,-2,-7,-4$ over three. Their binary words are $001100T$, $(01)^\omega$, $1100T$ and $00T$. If the first $\ell$ output bits encode $z'$, the image numerator is $3z'+Bc$, where $c$ is the listed integer. Only $s_1$ changes the residue modulo three, and the actual machine halts there. For $s_0$ the physical rule appends one zero, whose new virtual completion is $0T$ with numerator $-2$. This accounts for the correction $26B$. The other continuing extensions already have their physical virtual completions.

The six-bit seed gives $(n,B)=(-28,64)$. After 583 scalar iterations an $s_0$ edge correction gives $(-318\,922\,769,2^{29})$. By iteration 1,721,188 the run reaches $(n_*,2^{69})$ on an $s_3$ extension, at full sweep 3,442,378. The [checker](wily_integer_map.py) obtains this same pair independently from the compressed sweep trace.

## The exceptional inputs and the sign condition

Following just the recursive input in the definition of $F$ ends either at $-2$ or at a multiple of four. A residue change modulo three occurs precisely in the first case. Its full inverse tree has root $-2$ and lifts
$$
L(m)=4m+6,\qquad
S(m)=\begin{cases}2m-3&m\text{ odd},\\2m+9&m\text{ even}.\end{cases}
$$
One lift fixes $-2$, and the other gives 5. All remaining inputs in this tree are positive and at least 5. An $s_0$ edge correction also requires a positive input when the word is nonempty. The only transition that sends $s_0$ out of its last cell reads a 1, so the most significant physical bit must be 1 and $n\ge B/2$.

The single-generator map $F$ is injective: at every tree level an output bit uniquely recovers the input bit and the next carry, because the bit rule for each fixed carry is a permutation. In particular the only preimage of $-2$ is 5, since $F(5)=-2$. An orbit starting at $n_*$ that stays negative can therefore neither encounter a halting input nor need an edge correction. This proves the stated sufficient condition.

There is a direct description of the inputs that could invalidate this sign condition. For $n<0$, one has $F(n)>0$ if and only if its recursive descent first reaches a multiple of four equal to **$-8$ or $-16$**. The recursive output lifts $3+4y$ and $2y$ preserve the sign of nonzero $y$. A negative input descends through negative integers except that $-1$ can reach 1, with $F(-1)=-28$. The only negative base inputs with positive image are $-8$ and $-16$. Their two inverse trees under $L,S$ consist entirely of negative integers (each stays at most $-7$). Thus the sign question is equivalent to whether the forward $F$ orbit of $n_*$ meets either of these explicit trees.

Each of the three exceptional forests above is sparse. For the positive descendants of 5, a word with $i$ long lifts and $j$ short lifts has value between $2\cdot2^{2i+j}+3$ and $14\cdot2^{2i+j}-9$, by induction on the two lifts. Distinct paths give distinct descendants: the long lift is even, the short lift is odd, and its inverse is unique. There are Fibonacci-many compositions of total weight $2i+j$. Consequently the number of halting inputs up to $X$ is $\Theta(X^{\log_2\varphi})$, where $\varphi=(1+\sqrt5)/2$. The same order applies to the negative sign-escape trees in $[-X,0)$. For a negative root $m$, the quantity $u=-m$ evolves by $4u-6$ or $2u+3$ (odd $u$) or $2u-9$ (even $u$). After a fixed finite number of lifts all branches have $u>9$, and the same constant-factor bounds in terms of $2^{2i+j}$ follow. Sparsity alone does not decide the forward orbit.

## A negative escape always has a positive predecessor

For any integer $y$ in the domain, let $B(y)$ be the smallest power of two such that $-B\equiv y\pmod3$ and $-B\le y\le 2B-3$. For $y<0$, the size condition is simply $B\ge |y|$. The buckets in either fixed residue class grow by a factor of four.

**Order on negative excursions.** If $x,y=F(x)$ are negative and $x\ne-2$, then $B(x)\le B(y)$. To see this, represent $y$ at any admissible width $B\ge |y|$ and invert the sweep. The inverse virtual suffix numerators on $T$ are as follows.

| Inverse carry at the far edge | 0 | 1 | 2 | 3 |
|---|---:|---:|---:|---:|
| Numerator of its preimage of $T$ | $-2$ | $2$ | $1$ | $-4$ |

These entries follow by reading the infinite-word carry rules backwards: $s_0$ sends $-2$ to $-1$, $s_1$ sends 2 to $-1$, $s_2$ sends 1 to $-1$, and the first-bit flip sends $-4$ to $-1$. As throughout this note these numbers are numerators over three. An internal preimage has $x\ge-B$. Reverse carries 1 and 2 produce positive preimages. Reverse carry 3 requires the highest written bit to be 1: only $s_1$ reading 0 emits 3, and it writes 1. That would imply $y\ge B/2$. Reverse carry 0 requires the highest bit of the preimage to be 1: only $s_1$ reading 1 emits 0. With $z$ the preimage's allocated bits one then has $x=3z-2B\ge -B/2$. This proves $x\ge-B$. The zero-width case $B=1$ consists only of the exceptional output $y=-1$. Since the sole negative input changing residue is $-2$, the bucket comparison follows.

For any negative escape $e$ with $F(e)>0$, its backward trajectory reaches a positive predecessor. Until that point it remains in $[-B(e),-1]$. The only exceptional backward transition $-1\mapsto-2$ reaches 5 on the following step; if this transition occurs here then $B(e)\ge2$. The segment cannot repeat a negative state, because the resulting cycle would have to contain $e$ and its positive image. There are at most $\lceil B(e)/3\rceil$ integers of the original residue in that interval. Thus a positive predecessor occurs within $\lceil B(e)/3\rceil+2$ steps. In particular a putative first future escape cannot have a known positive predecessor closer than the already established negative part of its backward trajectory.

There is a corresponding order on positive excursions. Each positive input that changes residue has negative output, since its halting descent ends at $-2$ and the output lifts preserve negativity. From a positive $x$ represented at $B(x)$, all three continuing edge extensions have negative virtual images. A positive successor therefore stops internally, keeping its residue and fitting the old bucket. It follows that $B(F(x))\le B(x)$ on consecutive positive states. If a positive segment starts immediately after a negative state, it must end: a positive cycle would contain its negative predecessor, by injectivity. Its first return to negative has value at least $-28 B(x)$ when $x$ is the segment's first positive input. This bound concerns the positive segment; a later negative segment can increase its bucket.

### Exact changes of bucket at a sign crossing

Every sign crossing belongs to one row of this table. Read the recursive input branch downwards and stop at the first listed root before continuing past zero. Conversely, lift the root using $L,S$ while keeping each lifted *input* of the initial sign.

| Input-to-output signs | Root $r$ | $F(r)$ | $B(F(x))/B(x)$ for this row | Residue |
|---|---:|---:|---:|---|
| Negative to positive | $-8$ | 13 | 1 | Preserved |
| Negative to positive | $-16$ | 5 | $1/4$ | Preserved |
| Positive to negative | 1 | $-14$ | 16 | Preserved |
| Positive to negative | 2 | $-109$ | 64 | Preserved |
| Positive to negative | 5 | $-2$ | $1/2$ | Changes |

The first two roots are the sign escapes already established. A positive base input has positive image. For the three recursive input branches, the only positive inputs leading to a negative recursive argument are 1, 2 and 5. The output lifts preserve sign, giving the last three rows.

To verify that the ratios persist, write a canonical input as $x=3z-B$. When its width is at least two, its highest pair in head-facing order differs from the padding pair $10$; otherwise the previous bucket already represents it. For a long lift the new capacity and digits are $4B$ and $4z+2$ on input, and $4B'$ and $4z'+1$ on output (where $F(x)=3z'-B'$). These additions merely prepend two low bits. A short lift gives input capacity $2B$ and digit integer $2(z\mathbin{\mathrm{xor}}1)+1$: it flips the old lowest bit and prepends a 1. On output the short lift just prepends a 0. Thus at widths at least three, the highest pair and canonical status are preserved, and capacities scale by four or two on both sides. For the smaller widths, the only input roots requiring a direct check are 1, 2 and 5. Their positive immediate children are 10 for root 1, 14 and 13 for root 2, and 26 and 7 for root 5, with the same ratios as their parents. (The omitted short child of 1 is negative.) On the output side $-2$ first lifts to $-5$ or $-4$, with capacities 8 and 4; output widths at least two already suffice thereafter. This proves the table.

If a positive $p$ enters a negative interval without a residue change and $q$ is the next positive value, then **$B(q)\ge4B(p)$**. Its first step expands the bucket at least sixteenfold, the negative interval cannot shrink it, and the last step reduces it by at most a factor of four.

### A family with a long wait for the preceding positive state

For $k\ge1$, the negative escape
$$e_k=11-48\cdot4^k$$
has its first positive predecessor exactly $d_k=2\lceil 2^{k+1}/3\rceil$ inverse updates earlier. In particular there is no uniform $o(\sqrt{|e|})$ upper bound for all negative escapes.

Starting at $-8$, applying $L$ exactly $k$ times gives $-6\cdot4^k-2$. Three short lifts then give $e_k$, proving it is an escape. Its canonical bucket is $B=4^{k+3}$. The allocated digits of $z=(e_k+B)/3=(11+4^{k+2})/3$ in head-facing binary order are $10$, then $01$, then $k$ copies of $10$, then the upper pair $00$.

Drive the inverse sweep by $s_0$ every step, writing a silent time slot when a carry stops before reaching the next cell. Inverting the original bit table through the first six bits **100110** gives exactly three live slots per period of eight. In one-based numbering the slots are $(4,6,8)$, all carrying inverse mode 1. Every additional pair $10$ passes precisely every second such live input, with inverse mode 1 again. At its first cell the successive live inputs emit 3,0 alternately; the initial zero at its second cell suppresses each 3 and sends 1 on the following 0. Silent slots do not change either cell. Thus slots $(a,b,P)$ in a period of length $P$ become $(b,P+a,2P)$. By induction the first two slots are $2\lceil P/6\rceil$ and $2\lceil P/3\rceil$, with $P=2^{k+2}$; the identity for the second slot at each doubling follows since $P$ is a power of two. No earlier inverse sweep touches the upper $00$, so the scalar remains negative. This first live inverse 1 applied to $00T$ has numerator 13, making the next scalar positive regardless of the lower bits. This gives the exact delay above.

## An obstruction to a bounded zero-tail reference for the blank orbit

There is no width $j\ge0$ and no finite-support binary reference tape agreeing with the low $j$ bits of $n_*/3$ whose entire $s_0$ orbit remains supported on those $j$ bits. The same obstruction applies at every phase of the actual low-prefix orbit. In particular, the [periodic reference construction](WILY_SHELL_CONE.md) with an orbit confined strictly below the matching width cannot capture this blank start.

To verify the obstruction, observe that an occupied reference prefix with zeros everywhere above it can emit only $s_2$ or silence at the cutoff if every phase stays inside. Any of $s_0,s_1,s_3$ writes a 1 on the first exterior zero, and a sweep visits the cell only once. The sequence of carries at the cutoff is determined entirely by the low $j$ bits; the low-prefix update under $s_0$ is a permutation.

For $0\le j<30$, compute the complete primitive period of these carries from $n_*$ using the one-cell period rule. At $j=0$ the period contains mode 0, at $j=1$ it contains 1 and 2, and at every $j=2,\ldots,29$ it contains all four modes.

For every larger $j$, one past scalar sweep supplies a witness simultaneously. The integer $h=2\,031\,034\,478$ satisfies $F(h)=-318\,922\,769$. The verified path from this last value to $n_*$ consists of 1,720,605 uncorrected $F$ steps, so $h$ is a strict virtual predecessor. Reading the first 30 bits of $h/3$ in mode 0 leaves mode 1 on the numerator $-1$. The next bit leads to mode 0 on $-2$, then to mode 1 on $-1$ again. Hence the carry from that sweep at each width $j\ge30$ is 0 or 1. Since its low $j$-bit input recurs in the finite permutation cycle of the blank prefix, each such cutoff has a forward phase with a non-$s_2$ arrival. This argument excludes bounded references of the stated type; it does not decide the actual blank orbit.

## Other integer orbits can have arbitrarily large finite periods

Write $A=$ **0000000001101110101100001001100001** in head-facing bit order. Let $M$ be 11 followed by $A$ without its first bit. For every $k\ge0$, the 2-adic word $AM^k(01)^\omega$ is a rational of the form $n/3$ and has **exact** $F$-period $2^{12+11k}$. For $k=0$ the integer is $-7\,328\,996\,864$. Direct iteration returns it for the first time at 4,096 and changes residue four times. A global argument that excludes finite cycles for all integer seeds would fail for this family.

Here is a finite certificate for the formula. For an initial tape prefix, record its *least* return time $p$, the primitive period $w$ of its outgoing carries and the number $c$ of copies of $w$ emitted before that return. To extend the prefix by one bit, double $p$ and $c$ exactly when that cell flips an odd number of times in the $c$ copies. The outgoing word follows from the literal carry table; each input 3 suppresses one emission. Any return of the extended prefix must first return the old prefix, proving that this rule retains the least return time.

| Bits appended | Incoming $(w,c,p)$ | Outgoing $(w,c,p)$ |
|---|---|---|
| $A$ | $(0,1,1)$ | $(01,2,4096)$ |
| $M$ | $(01,2,p)$ | $(01,2,2048p)$ |
| 01 | $(01,2,p)$ | $(01,2,p)$ |

Applying the three finite rows gives the claimed period for every finite prefix containing $AM^k$ and ending after complete pairs in the alternating tail. Thus the entire infinite word returns at that same time. The physical blank is a different input; even for the listed alternates a virtual residue change is a halting event only when the physical and virtual states still agree.

## Checking the sign along the blank run

The finite sign conclusion follows without iterating $F$ trillions of times. From old suffix width 69 onward each of the 350 observed extensions through $2^{256}$ sweeps receives $s_3$. The very next arrival at that same old edge is $s_0$, except at the final extension where there are no further arrivals before the cutoff. The $s_3$ creates 00. No sweep changes those two cells before the next arrival. That $s_0$ traverses both of the zeros in one sweep and reaches the new edge in mode $s_3$, immediately creating the next 00. Thus the two highest bits remain zero at every completed sweep from 3,442,378 to $2^{256}$. Hence $z\le B/4-1$ and $n\le-B/4-3$ at every paired update in the certified interval.

At the last checkpoint the trimmed width is 767 and the high bits are 00, so $B(n)=2^{767}$: the strict inequality $|n|>2^{765}$ excludes the previous bucket. By the order on negative excursions, **any first positive escape after this checkpoint must start at an input $e$ with $|e|>2^{765}$**. The exceptional $-2$ cannot interrupt this argument, since its unique predecessor is 5.

At $2^{224}$ sweeps the Python stream verifier found 671 total suffix bits and 301 late extensions. At $2^{256}$ sweeps the packed [C++ verifier](wily_blank_sign.cpp) found 769 total suffix bits, including the two fixed low bits. It checks the carry and next-arrival condition on every late extension. The SHA-256 of the 769 ASCII digits before the output newline is `f0ac9e6cda66dec901cf94a99712f66b3b839bee692ab8ff7e9265455556e903`. The chronological raw-step bound for each encoding is $2^{255}(2^{256}+1)>6.7039\times 10^{153}$. This lower bound concerns both actual blank trajectories.

Run the scalar, stream and packed checks with:
```sh
python3 wily_integer_map.py --power 192
g++ -std=c++17 -O3 wily_blank_sign.cpp -lgmpxx -lgmp -o wily_blank_sign
./wily_blank_sign 256 > suffix.txt
python3 -c 'import hashlib; print(hashlib.sha256(open("suffix.txt","rb").read().strip()).hexdigest())'
```
