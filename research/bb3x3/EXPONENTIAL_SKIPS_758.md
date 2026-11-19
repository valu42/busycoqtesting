# Exact skips across exponentially many resets of #758

For every $m\ge20$, two explicit intervals near $P=3^m$ and $2P$ admit an exact skip. Given any starting reset in either interval, the [checker](power_skip_758.py) computes the first reset above the interval, the number of complete first returns, and the elapsed raw transitions. It needs at most 320 evaluations of a fixed return word, independent of $m$. From the lower endpoint the number of first returns skipped grows at least as fast as a constant times $3^m/m$. Integer sizes and the cost of arithmetic grow with $m$.

| $m$ | Interval | First returns from the lower endpoint, rounded | Elapsed raw transitions, rounded | Return-word evaluations |
|---:|---|---:|---:|---:|
| 34 | Below $2P$ | $4.389\times10^{13}$ | $7.849\times10^{46}$ | 79 |
| 292 | Below $P$ | $4.026\times10^{134}$ | $5.226\times10^{413}$ | 25 |
| 292 | Below $2P$ | $7.049\times10^{135}$ | $1.973\times10^{415}$ | 17 |
| 1000 | Below $2P$ | $1.317\times10^{473}$ | $1.480\times10^{1428}$ | 36 |

These are trajectories from specified reset seeds. The actual blank run at $m=292$ has yet to be connected to either interval. The $2P$ interval at that scale is above the leading halting candidate.

## Where the rule applies

Write $A(a,c)$ for the two-counter configuration, and call $A(1,s)$ a reset. Set $z=s+2m$. The admissible inclusive intervals are
$$
\lceil1458P/1475\rceil+1000\le z\le P-1000,\qquad
\lceil9P/5\rceil+1000\le z\le2P-1000 .
$$
Here $J$ is the odd/odd jump, $L$ an ordinary bulk move, $R$ the return to $a=1$ and $I$ the first move from an even seed. The following are complete first-return words throughout the indicated intervals.

| Start | Below $P$ | Below $2P$ |
|---|---|---|
| Odd seed | $J^{m-1}LR$ | $J^mLR$ |
| Even seed | $I J^{m-1}LLJLLLR$ | $I J^{m-1}LR$ |

Both parity words advance the reset parameter by at most $2m+29$. Each interval spans a fixed positive fraction of $P$, up to the displayed additive margins. This gives the lower bound on the number of returns from its lower endpoint. [Counter rules and timing](timing_758.py) · [Power-gate definitions](POWER_GATES_758.md)

## Proof for all exponents

For $k$ jumps starting with $u=a+1$, the final counters are $3^ku-1$ and $c-u(3^k-1)/2+2k$. Positivity of the final right counter guarantees that every jump guard held, since an individual jump gives $c'=c-a+1$. The parity of both counters stays odd. The even-seed opening produces $A(3,s+3)$.

At the end of the initial jumps the counters differ by at most three in each coordinate from $(x,z-x/2)$, where $x=4P/3$ for even starts, $2P/3$ for odd starts below $P$, and $2P$ for odd starts below $2P$. In the ideal coordinates a bulk sends $(a,c)$ to $(a-c,3c/2)$ and a jump sends it to $(3a,c-a)$. A coordinate error at most $e$ thus becomes at most $2e+7$ or $3e+2$, respectively. The bulk's two integer formulas depend on $c$ modulo four and toggle the left parity. The interior jump in the long even-seed word occurs at odd left parity. Its last bulk produces even left parity, as does the single bulk on the short words.

Along each row the checker verifies that ideal coordinates exceed the corresponding error bounds by enough for $a>1$, $c\ge1$, and each stated guard. For a bulk the sufficient margin is $a-c>2e+4$. For a jump or return it is $c-a>2e$. Each margin is affine in $(P,z)$. On each of the two lines bounding an interval the margin is positive at $P=3^{20}$ and has nonnegative slope, checked exactly over the rationals. Interpolation in $z$ proves the guards throughout every interval for all larger $P$. This also rules out earlier resets.

## How the computation skips the returns

Each word has at most five bulks. Changing a seed by an integer multiple of 64 preserves the parity and the residue of the right counter modulo four at each bulk. Before the fifth bulk the incoming change is still divisible by four. A jump costs no binary precision and a bulk can consume one bit. On a fixed residue, each intermediate counter is affine in the seed. The mass gain, and hence the seed increment, is constant. Summing the exact branch cost polynomials gives a raw clock of degree at most two on that residue. The long initial jump run has a closed geometric sum. [Raw jump sum](TARGET_CLOCK_758.md)

After at most 64 first returns a seed residue repeats or the interval ends. A repetition gives a cycle with positive stride divisible by 64. Later cycles visit exactly the same residues in the same order until the interval boundary. The cost of an entire cycle is quadratic in its copy index. Three evaluations determine that polynomial, whose sum over any number of copies is computed with integer binomial coefficients. A final partial cycle identifies the exact exit. The transient, three sampled cycles and the remaining partial cycle require at most $5\cdot64$ return evaluations.

The skip can also follow the first change of word at either power. At the doubled gate one attainable exit exhibits every finite prescription of subsequent ordinary branches as the exponent varies, even within a fixed congruence class. This explains the advantage of generating rules from the actual local guards. The general interval algorithm gives a bound of $O(X^{0.881})$ individual first-return evaluations across $[X,3X]$ when the returns exist. Each unresolved excursion still has to be evaluated. [First word change](POWER_BOUNDARY_758.md) · [Variation with exponent](POWER_PHASE_LAW_758.md) · [General skip theorem](ANNULAR_SKIP_758.md)

## What would decide the blank machine?

The mass $a+2c$ grows by only four to nine per continuing counter update. Even a simulator that performs each such update in one operation needs at least $4.76\times10^{138}$ of them to reach $A(1,H)$ from blank. The skips above bypass that obstacle inside their intervals. At a change of word both the residue map and its clock polynomial can change. There is no proved rule covering the whole intervening gap from a known blank checkpoint to the halting basin.

There is a finite stopping point for testing this particular target. Both direct seeds halt at an input of mass $V=2H+1258$. Each live update gains at least four in mass, so from the initial mass two, within $\lfloor(V-2)/4\rfloor+1<1.0724\times10^{139}$ calls the machine must halt or reach a mass above $V$. At the first crossing the mass is at most $V+9$. The angular clock bound shows either event occurs within $8.206\times10^{416}$ raw transitions. Once the mass has passed $V$, the machine can never reach this particular terminal. Its fate at larger masses could still be open. [Horizon verifier](basin_clock_758.py) · [Angular clock proof](ANGULAR_CLOCK_758.md)

The largest uninterrupted interval currently known to force a halt contains 362,166,436,260,267 reset seeds. Proving that the blank run visits just one of them is sufficient. Another route is to join successive powers by skipping whole intervals and checking the gaps. Since the mass increases, following the maximum outgoing seed is unsafe: a valid proof tracks the actual exit or encloses **every** possible exit in the next verified input interval. [Halting intervals](LOWER_SCALE_GATES_758.md) · [Near-target power gate and remaining gap](POWER_TARGET_BRIDGE_758.md)

Run `python3 power_skip_758.py` from this directory to check the all-exponent inequalities, compare small stretches with literal execution, and reproduce the examples.
