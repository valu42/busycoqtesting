# Line 411 beyond the first 180 million sweeps

**Blank-tape status: open.** The table is `1RB0LF_1RC1RB_0RD0RC_1LE1LF_1LD---_0LB1LA`, ID 116372. Starting in A on zeros, it executes at least 180,000,000 complete regular sweeps and more than $10^{108000000}$ elementary transitions. A different family of tapes reaches its halt on the sixth boundary check. Both statements use the same transition table. The [original derivation](README.md#complete-boundary-test) defines the boundary $H(N,w)$, the right call $F$, and the reduction from the blank initial tape.

## Reproduction

Run in this directory with Python 3 and assertions enabled. The prefix checker uses only the standard library. Its input is the complete run-length encoded checkpoint, with SHA-256 checked before use.

```sh
python3 identities.py
python3 prefix411.py checkpoint-500000.z
```

To rebuild that checkpoint from the blank start, compile the C++17 evaluator with GCC or Clang. The replay checks each stored digest it passes. The compressed file may vary with the zlib version. The digest is over the uncompressed data.

```sh
c++ -std=c++17 -O3 -fPIC -shared sweep_power.cpp -o sweep_power.so
python3 sweeps.py --epochs 500000 --output rebuilt.z
python3 prefix411.py rebuilt.z
```

| Regular sweeps | Boundary checks | Stored right-word cells | SHA-256 of complete boundary |
|---:|---:|---:|---|
| 100,000 | 100,035 | 230,331,731 | `c109d1e574336f606ea1cbcd69f1f276d9ee18c0cde6f7d10626789be40e7d96` |
| 150,000 | 150,035 | 653,297,327 | `464631aba678b44b44b72ac0d19a4f497caad32813363c8f954a850472e099ea` |
| 500,000 | 500,041 | 4,509,007,619 | `191096ad5842098c978379eb43975731ee269bf7d0a605dda9347417a190b230` |

At sweep 500,000 the left integer has 500,006 bits. The right word has 497,346 runs. Its first four runs are four zeros, 355,378 ones, three zeros and 65,463 ones. Starting with the first 4,800 runs, the prefix checker reaches sweep **180,000,000** at boundary **180,000,057**. The certified right word there begins with four zeros followed by **at least 1,321,824 ones**. Everything after a certified prefix may vary. The distant calculation makes no assertion of a complete final tape.

The earlier four-interface evaluator agrees at its published checkpoints through sweep 3,338. A separate explicit-word power implementation agrees through sweep 14,500. A sparse-tree replay from blank independently matched the full configurations through sweep 150,000. A second check starts the prefix method at sweep 100,000 with 150 known runs. It reproduces the count and the certified prefix of the full 500,000-sweep checkpoint. The exact-power and prefix implementations use different algorithms. These are executable mathematical checks. The new long calculation has no Rocq or Lean kernel certificate.

## Two safe returns and a halting family

Write $Q(s,u)=H(8s-4,000011u)$ for integral $s\ge2$. Put $A_j=F^{2j}$ and define $B_j$ by $F^{2j}(1x)=1B_j(x)$. For this definition, two calls always restore an initial one. On `11` a call fixes those two ones and acts once on the suffix. On `101` it produces `111`. On `100` it produces either an initial zero or at least three initial ones by the four right-call rules. In the first case the next call starts with one, and in the latter case it preserves the initial pair. This proves the assertion for two calls and hence for all even powers. Composition of $B_i$ and $B_j$ gives $B_{i+j}$. Also $A_j(1x)=1B_j(x)$ and $B_j(1x)=1A_j(x)$.

1. **A leading one buys a regular sweep.** For any suffix $x$,
   $Q(s,1x)\longrightarrow Q(2s,F^s(x))$.
   Indeed the sweep applies $F^{4s-2}$ to `000111` followed by $x$. Two calls give `000011` followed by $F(x)$. Every further four calls preserve that prefix and send one call through it.
2. **Three zeros followed by four ones buy five boundary checks.** For even $s$ and arbitrary $x$,
   $Q(s,0001111x)\longrightarrow Q(8s+1,F^{4s}(B_{s/2}(F^{s/2}(x))))$.
   The three regular sweeps and two exceptional returns are detailed below.
3. **A nine-bit suffix forces a halt.** For either bit $b$ and arbitrary $x$, $Q(s,0010000b1x)$ halts. On the first sweep the prefix becomes `11111111100011`. Four exceptional returns change it successively to `111111000111`, `1111100111`, `11000011` and `100011`. The sixth check sees `1000` and reaches the undefined instruction. At $s=2$ the first sweep needs six right calls. Increasing $s$ by one adds four calls that preserve its output prefix and send one more call into the suffix.

Here each row of the five-check return applies its suffix operation to the result of the previous row.

| Branch taken | New left integer | Known new right prefix | Operation on the remaining suffix |
|---|---:|---|---|
| `0` | $16s-4$ | `000000001111` | $F^{s/2}$ |
| `0` | $32s-4$ | `00011000111` | $B_{s/2}$ |
| `0` | $64s-4$ | `1111000111` | $F^{4s-1}$ |
| `11` | $64s$ | `11100111` | identity |
| `11` | $64s+4$ | `000011` | $F$ |

The base case is $s=2$. Increasing $s$ by two adds 8, 16 and 32 calls to the first three rows, respectively. On the three output prefixes these increments transmit $F$, $B_1$ and $F^8$ and restore the same prefixes. This proves all even cases by induction. [The identity checker](identities.py) verifies every finite base and increment by rewriting the four $F$ equations with the trailing variable $x$ untouched.

## Computing a full sweep

A right word is a string of binary digits in two modes until the first unrecognized group. At the root, `00` and `10` encode a low digit. Extended groups `0000` and `0110` continue the number. Groups `0011` and `0111` close it, returning to the root. Within each pair the second spelling encodes one. At the root `11` forwards every call. The underlying one-call identities are verified against the literal machine by [line411_rules.py](line411_rules.py).

Here is how [sweep_power.cpp](sweep_power.cpp) handles noncanonical input rather than treating it as a digit. Let $m$ digits of an open number have been read. Add their value to the incoming count to form $S$. If $S<2^m$, write its $m$ low bits in the open format and retain the unread suffix. Otherwise a carry reaches the next group.

| Next group | Action |
|---|---|
| An ordinary extended digit | Add its value at weight $2^m$. On closure write all the low digits and forward the quotient. |
| Starts with `1` | At $m=1$ replace the root by `11` and forward $S-2$. For $m>1$ close the existing number, write the low $m$ bits and forward $\lfloor S/2^m\rfloor-1$. The first bit of the next group stays unread. |
| `0001` or `0010` | Extend by a zero-valued digit. The former closes the number, the latter leaves it open. |
| `0100` or `0101` | Emit $4m$ ones, consume the first two bits of this group, set its third bit to one and forward $S-2^m$ starting at that changed bit. |

Separately, root `01` becomes `11` and uses up one call. The special cases follow by applying the residual-word equation once on the first overflow: the low open number is then `10(0110)^(m-1)` immediately before the carry and the residual bits select its output. In fact the all-one digit word is $(1001)^{m-1}10$. If the next bit is one, the residual `101` gives $0^{4m-4}11$ followed by the untouched next group. For `0001` and `0010` the residual `1000` produces $0^{4m-4}$ followed respectively by `000111` or `000110`, the two stated extended encodings of $2^m$. For `010b` the residual after stripping $m$ copies of `1001` is `0b`, giving $1^{4m+1}b$. Ordinary binary addition handles the remaining calls. The native replay compares 1,600 randomly chosen powers with the earlier implementation before starting from $H(36,000110011)$.

## Certifying a distant boundary using a finite prefix

For $Q(s,1^m x)$ with even $s$, consume $m$ leading ones using the first return above. The $j$-th operation on $x$, indexed from zero, uses $2^j s$ raw calls. It is an unshifted call if $m-1-j$ is even and a call on `1` followed by the current suffix, removing that preserved leading one, if it is odd. This follows by pulling the operation past each of the remaining ones using the two identities for $A$ and $B$.

[The prefix checker](prefix411.py) handles these counts directly. It applies the four defining equations of $F$ to a short packet $p$ and an arbitrary tail $x$. A successful local row has the form $F(px)=qF^c(x)$ with $|q|=|p|$ and $c\in\{0,1\}$. Once a packet word repeats, both the period and the number of calls forwarded per period are exact. Suppose the incoming count is $a+2^d t$ for unknown $t\ge0$. If $a$ reaches the period and its length $P$ divides $2^d$, every possible count writes the same packet. If each period forwards $v$ calls, increasing $t$ by one adds $(2^d/P)v$ to the outgoing count. Its power-of-two divisor gives a conservative modulus for continuing into the next packet. If a finite packet cannot justify an output the unproved suffix is dropped. The full checkpoint supplies the initial lower bound and low bits of $N$. Its subsequent updates preserve those bounds.

There are two ways to omit the remaining growing powers. A block $C_h=0^{4h+3}111$ uses a closed $h+2$ digit number in both alignments. For the shifted alignment, the final one remains after the number closes. Both $A_k$ and $B_k$ preserve $C_h$ and forward the corresponding operation with index $k/2^{h+2}$ whenever the division is exact. Leading ones switch the two operations. Concatenating these blocks gives a common period for a whole known prefix. More generally, the checker parses both the prefix and the same prefix preceded by one. If each ends at the root, each digit costs one bit of divisibility and each `11` costs zero. A final unpaired one costs one further bit because an even outgoing power preserves that one. When the current valuation suffices in both alignments, all later powers in this group preserve the prefix as well.

For the elementary-transition bound, immediately before regular sweep $e$, $N\ge40\cdot2^{e-1}-4$. This follows from $N=36$ at the start, $N\mapsto2N+4$ on regular sweeps, and the positive increases on exceptional returns. This sweep executes $b=(N-2)/2$ left increments. From the [exact left-sweep cost](README.md#coordinates-and-left-sweeps), the $j$-th costs $12b+12-4j$ for $0\le j<b$. The sweep alone therefore exceeds $8b^2>2^{2e}$. Taking $e=180000000$ and using $2^{10}>10^3$ gives the stated bound.

The remaining question concerns one specified initial tape. The blank orbit must either reach a terminal prefix or stay inside a family of prefixes with a proved successor for every member. The finite certificate and the unrestricted halting family leave that question open.
