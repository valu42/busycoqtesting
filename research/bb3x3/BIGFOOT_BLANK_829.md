# Bigfoot from blank

Bigfoot (#829) reaches Ligocki’s unshifted configuration
$B(a,x)=A(a,2x+1,2)$ with $(a,x)=(2,0)$ after 69 raw transitions.
Only a decrement from zero halts. The [evaluator](bigfoot_blank_829.cpp)
checks the minimum counter at every macro-step, including steps inside its
accelerated blocks. [Original reduction and published 24-million-step checkpoint](https://www.sligocki.com/2023/10/16/bb-3-3-is-hard.html)

The blank tape survives **at least 357,932,683 macro-steps and more than
$2^{148,552,130}$ raw transitions**. The evaluator directly follows the first
268,435,456 macro-steps. At that checkpoint the counter is 44,748,613 and
the length $x$ has 111,410,782 bits. The ultimate behavior remains open.

| Macro-steps from $B(2,0)$ | $a$ | Minimum $a$ | Bits in $x$ | $x$ mod 1,000,000,007 | $x$ mod 1,000,000,009 |
|---:|---:|---:|---:|---:|---:|
| 256 | 39 | 2 | 108 | 531,997,034 | 156,324,105 |
| 24,000,000 | 3,999,888 | 2 | 9,960,901 | 105,192,432 | 978,584,378 |
| 268,435,456 | 44,748,613 | 2 | 111,410,782 | 246,577,988 | 698,941,257 |

The two odd phases in each group of four can only preserve or increase $a$.
The two even phases can lose at most one apiece. Therefore the last checkpoint
pays for another $m=22,374,306$ whole groups and three more steps. At the end
of the $m$ groups the length exceeds $(256/81)^m 2^{111,410,781}$, by the
growth bound below. The tape then contains $2(2x+1)$ ones in its length block,
and a raw transition can write at most one nonblank cell. The integer
inequality $256^{50}>2^{83}81^{50}$ yields the advertised raw bound because
$111,410,783+\lfloor 83m/50\rfloor=148,552,130$.

## Evaluating a finite blank orbit

After four macro-steps the state is again in $B$. For $x=81q+r$, the new
length is $256q+s_r$, with the same four counter changes as from $r$.
In one macro-step, adding $6t$ to the input length $b$ preserves the branch
and adds $8t$ to the output. Starting with a change of $2\cdot81q$ in $b$
and applying this identity four times gives the claimed change of $256q$ in $x$. The first two macro-steps have odd $b$, and the last two have even
$b$. The evaluator checks the phase and strict growth $81s_r>256r$ on the
81 residue classes.

Induction gives a block rule for any $n$. If $x=81^n q+r$, then $n$
four-step blocks trace the same counter changes as they would from $r$,
and the final length increases by $256^nq$. The program splits $n$ in two,
applies the rule to each half in chronological order, and restores the
discarded high part with a bit shift. Its leaf table covers two four-step
blocks and stores both the gain and the minimum partial sum. For successive
walks with summaries $(g_1,m_1)$ and $(g_2,m_2)$ the combined minimum is
$\min(m_1,g_1+m_2)$. Hence the minimum detects a halt even if the formal
walk would recover by the end of the block.

Compile on a 64-bit system with GMP. The argument counts Ligocki macro-steps
and accepts positive multiples of 16 through $2^{40}$.

```sh
c++ -O3 -std=c++17 bigfoot_blank_829.cpp -lgmpxx -lgmp -o /tmp/bigfoot
/tmp/bigfoot 256
/tmp/bigfoot 24000000
/tmp/bigfoot 268435456
```

## Which part of the blank seed still matters?

There is an exact calculation for the fraction of extensions of **any finite
blank prefix** that eventually hit the halting branch. Measure extensions by
choosing successive ternary digits of the initial $x$ independently and
uniformly. This is the uniform (Haar) measure on the 3-adic integers. At a
finite horizon the fraction also equals the fraction of ordinary integer
residue classes modulo the corresponding power of three. The fixed blank
seed has $x=0$ at every precision, so this calculation does not decide it.

In each four-step group the residues $b\bmod6$ are independent and uniform
over the three odd, odd, even and even choices in order. Indeed, fixing the
previous branches fixes one successive ternary digit per step. Adding
$2\cdot3^j t$ to the starting $b$ changes the $j$th iterate by
$2\cdot4^j t$ with its phase and all earlier branches preserved. The next
ternary digit thus visits all three allowed residues exactly once. After
a fixed whole-group prefix the high digits still range uniformly because
the length lift is multiplied by a power of 256, a unit modulo three.

At the beginning of a group with current counter $a$, the eventual halting
fraction for these extensions is
$$
P(a)=A r^{a+1}+(1-A)s^{a+1},
\qquad A=\frac{1-V(s)}{V(r)-V(s)},
$$
where $r=\sqrt6-2$, $s$ is the unique real root of
$s^3+3s^2+12s+2=0$, and $V(z)=(1+z+z^{-1})/3$.
For example, $P(2)\approx 0.0832862032012774$ for the full seed class.

To see this, put $U(z)=(2+z)/3$. The four generating functions for one
counter increment are $U,U,V,V$. For either $z=r$ or $z=s$ their product
is one because $U(z)V(z)=1$ or $-1$, respectively. With phases numbered
$0,1,2,3$ before each step, the function $z^{a+1}$ times the phase factor
$(1,UV^2,V^2,V)$ therefore equals its expected value after the next step.
Upon first reaching $a=-1$ the phase is either 0 or 3. The displayed
mixture equals one in both terminal phases by the choice of $A$. Before
halting it stays bounded since $|r|,|s|<1$. On every surviving path
except a measure-zero set the counter tends to infinity by the strong
law of large numbers for the independent four-step gains, whose mean is
$2/3$. Stopping at a halt or at a finite horizon and taking the limit
gives $P(a)$.
