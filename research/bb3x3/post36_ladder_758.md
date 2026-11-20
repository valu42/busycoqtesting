# A singleton continuation beyond the power-36 checkpoint

Both blank runs reach

$$
A(1,150124733170248900)
  =A(1,3^{36}+30097873249779).
$$

This extends the [completed power-36 bridge](power36_final_758.md), whose exact
endpoint is $A(1,3^{36}+112032)$. The new calculation follows that actual reset,
constructs common-word intervals when they are useful, and rejoins their possible
exits at an exact later reset. Two natural outward gates finish the recorded
flights. It does not construct a fixed grid over the next power interval.

This remains finite progress on the actual blank trajectory. It does not prove
eventual halting, nor provide an induction from one power of three to the next.

## The connected result

Write $P=3^{36}=150094635296999121$. All entries in the following table are offsets
above $P$.

| Pure bulk count $k$ | Gate entrance | Actual arrival | Gate far edge | Forced later reset |
| ---: | ---: | ---: | ---: | ---: |
| 25 | 3,962,815,934,218 | 3,962,815,934,236 | 5,944,302,372,446 | 5,944,302,402,078 |
| 21 | 20,063,907,693,858 | 20,063,907,693,967 | 30,097,873,208,166 | 30,097,873,249,779 |

The first connection begins at offset 112,032. The second begins at the first
row's forced reset. Each actual arrival lies strictly inside the indicated gate.
The gates then force the displayed later reset regardless of the phase with
which the actual orbit arrived.

The [receipt archive](post36_ladder_receipts_758.tsv) records the exact input and
output of each connection, its computational work, and its final gate. The
[Python verifier](post36_ladder_758.py) reconstructs both gate boundaries and their
complete exit mergers. With `--worker` it also regenerates both connection
receipts using the [singleton worker](post36_singleton_758.cpp).

| Connection | Literal return evaluations | Merger return evaluations | Successful local skips | Seed width skipped inside the connection |
| --- | ---: | ---: | ---: | ---: |
| Initial reset to $k=25$ | 333,633,888 | 94,110,914 | 74,705 | 3,889,186,524,136 |
| First forced reset to $k=21$ | 794,021,728 | 203,679,770 | 165,735 | 13,949,792,322,558 |
| Total | 1,127,655,616 | 297,790,684 | 240,440 | 17,838,978,846,694 |

These are work counts, not the number of first returns taken by the blank orbit.
The common-word skips stand for many additional returns. The last column also
excludes the two final pure-bulk gates. The initial connection runs, with ordered
sets for the mergers, took 22.15 and 50.02 seconds on one CPU in the working
environment. The optimized circular-bitset version reproduced both receipts
exactly; its separate first-link benchmark took 18.24 seconds. Replay time
depends on the machine and compiler.

## Exact outward gates at arbitrary powers

The gate construction transports the argument used in the
[power-292 cusp ladder](POWER_CUSP_758.md), with the exponent supplied as a
parameter. Let $P=3^m$ and let $d$ be even. The odd reset $P+d$ takes $J^m$ to

$$
(a_0,c_0)=(2P-1,d+2m+1).
$$

For a proposed odd number $k$ of bulk calls, compute the right counter and total
left decrement without imposing guards:

$$
q_i=\left\lfloor\frac{c_i+1}{4}\right\rfloor,
\qquad c_{i+1}=6q_i+5,
\qquad D_{i+1}=D_i+4q_i+3,
\qquad D_0=0.
$$

The complete word $L^kR$ is legal exactly when

$$
D_k\le 2P-1\le D_k+c_k.
$$

The left decrement of each bulk is its guard threshold. Thus the first
inequality certifies every proposed bulk, and the second certifies the final
return. Since $k$ is odd, the final left counter is even. Both $D_k$ and
$D_k+c_k$ are nondecreasing in the input offset. Two exact integer bisections
therefore find the first admissible even offset $l_k$ and the first subsequent
inadmissible even offset $h_k$.

The verifier also checks both endpoints of the even-seed word
$IJ^{m-1}L^2JL^3R$ over this gate. Ordered counters extend those guards to all
intermediate even seeds. The two words have positive seed gain at most

$$
G_k=\max\left(2m+29,\left\lfloor\frac{4m+9k+5}{2}\right\rfloor\right).
$$

Consequently every reset in $[P+l_k,P+h_k)$ eventually reaches a reset in
$[P+h_k,P+h_k+G_k)$. The two recorded gates have $G_{25}=187$ and $G_{21}=169$.
Their complete exit strips coalesce in 1,036 and 1,112 distinct first-return
evaluations, respectively. These small mergers use the independent Python
`first_return` implementation.

`pure_interval(m,k)` and `gate(m,k)` are reusable beyond exponent 36. Their
explicit domain check requires $m\ge20$, positive odd $k$, and the resulting
gate strictly inside the first one percent above $P$. The two recorded gates
satisfy that condition. The construction does not assert that gaps between
arbitrary gates are already connected.

## Finding and leaving a useful word interval from one reset

The worker maintains an exact current reset. It first asks whether the existing
ordered-counter checker `Cover.bound` certifies a common word over a proposed
interval of 250,001 seed positions, or the remaining smaller interval before
the next gate. If the word changes output parity, it checks the other parity as
well. Closing this graph on two parity classes requires at most two scans.

When the required words are available, exponential expansion followed by integer
bisection finds a farther certified endpoint. Every endpoint used for a skip is
checked successfully. Soundness does not require that a failed probe remain
failed at all larger endpoints.

The checker selects the reset at the end of its common counter word. This need
not be the first reset: an earlier left counter of one is harmless, because the
ordinary counter evolution can continue from it. This distinction matters for
the parity closure and the exit enclosure. Literal evaluations and the final
mergers do use first returns.

Let $C_p$ be the checker's seed-gain bound on input parity $p$. Along the selected
word the mass $a+2c$ increases by 4 at a jump, by 5 or 9 at a bulk, by 8 at an
exceptional move, and by 5 at the final return. The checker uses 9 for every
bulk. Each difference between an actual bulk charge and its upper charge is a
multiple of four. Therefore the selected seed gain has the same parity as
$C_p$. The reachable-parity closure is sound, including words with an earlier
reset.

All selected gains are positive. Iterating the certified words must leave the
finite interval. For an inclusive right endpoint $b$, a final input of parity
$p$ contributes only exits of parity $p+C_p$ in $[b+1,b+C_p]$. The worker forms
the union of those short strips, advances their least live reset, and deduplicates
successors. If every candidate merges into one reset within 16,384 evaluations,
the actual orbit reaches that reset, so the worker replaces its exact singleton
by this proved destination.

A failed word probe or failed merger leaves the original exact singleton
available. The worker then follows its literal first returns to the next probe
position. Hypothetical merger evaluations never replace the actual orbit unless
the entire exit set has coalesced. This avoids propagating the 5,001 arbitrary
incoming seeds used by the previous fixed-window method.

## Arithmetic and independent checks

The exponent-36 launch formulas are fixed throughout the supported worker
interval $[P,P+\lfloor P/10\rfloor]$. The worker reuses
[`PackedReturn`](packed_return_758.hpp), with three bulk pairs per packed stage.
Its mass ceiling is the interval's high endpoint plus 100,000; the existing
compile-time check proves that the exact shifted numerator fits in an unsigned
64-bit word. The bounded stage construction and continuation loops add less
than this mass allowance. Input checks reject links outside that launch interval.

The worker's `--audit` compares 10,000 packed returns with literal C++ counter
calls, covering both the power cusp and the full supported interval. The Python
wrapper adds an independent whole-flight test: starting at the proved blank
checkpoint, the adaptive worker reaches $P+10102544$ when asked to pass
$P+10000000$. Direct `champion_step` replay reaches exactly that same reset after
41,861 first returns and 3,528,168 scalar counter calls. These are counter calls,
not raw Turing-machine transitions. An independent undefined-behavior-sanitized
build passed both the packed-return audit and this short adaptive connection.

### The circular merger set

The optimized merger stores the live points in 65,536 circular bit positions and
tracks their full integer minimum and maximum. The initial exit enclosure has
span below 45,100: `Cover.bound` has fewer than 10,000 continuation calls, each
with mass charge at most 9. A packed first return gains at most

$$
74+9(256+5000)+7=47385
$$

seed units, from the launch, at most 256 planned ordinary blocks, at most 5,000
continuation blocks, and the final return. These are implementation bounds, not
typical gains.

If the current least seed is $x$, deleting it and inserting a successor in
$(x,x+65536)$ preserves a live span below 65,536. Reduction modulo 65,536 is
therefore injective on the live set. The implementation checks both the inserted
return gain and the full live span, so a violated assumption stops the verifier
before any circular alias can be accepted. Full coordinates determine the order
when scanning across a word boundary or a full ring boundary.

The audit forces 10,000 updates across these boundaries, including duplicates,
and compares them with an ordered-set reference. It also checks rejection of a
span of exactly 65,536. Compiling with `-DPOST36_SHADOW_REFERENCE` additionally
keeps a reference `std::set` during every actual merger and checks the two
representations after each insertion and removal. The combined shadow and
undefined-behavior-sanitized build passed the short independent Python flight.

### Probe-width and residue-cycle checks

The first complete link was replayed with three probe widths:

| Probe width | Ordered-set seconds | Circular-bitset seconds |
| ---: | ---: | ---: |
| 125,000 | 29.12 | 19.87 |
| 250,000 | 22.15–23.06 | 18.24 |
| 500,000 | 23.90 | not measured |

All three widths produced the same gate arrival. Smaller probes reduced literal
evaluations but increased the number of merger evaluations. The recorded worker
retains the measured 250,000 choice. All attempted mergers succeeded on this
first link, for each tested width. A residue-cycle fallback triggered only by a
failed merger therefore has no work to do on that connection. The known short
even word returns to the difficult odd class, whose many initial bulks also make
the residue modulus much larger than in the short-word corridors farther from
the power. No residue-cycle extrapolation is used in these new receipts.

## Reproduction and inherited dependencies

From `research/bb3x3`:

```sh
c++ -O3 -std=c++17 post36_singleton_758.cpp -o /tmp/post36_singleton_758
python post36_ladder_758.py --audit-worker /tmp/post36_singleton_758
python post36_ladder_758.py --from-blank --worker /tmp/post36_singleton_758
```

The stronger optional representation and arithmetic audit is:

```sh
c++ -O2 -std=c++17 -DPOST36_SHADOW_REFERENCE -fsanitize=undefined -fno-sanitize-recover=all post36_singleton_758.cpp -o /tmp/post36_singleton_audit_758
python post36_ladder_758.py --audit-worker /tmp/post36_singleton_audit_758
```

The last command regenerates the two new connection receipts and reconstructs
both final gates. `--from-blank` also runs the inherited
[`power36_final_758.verify()`](power36_final_758.py), which validates the complete
prior receipt coverage, the symbolic intervals, and the power-36 gate merger.
It does not regenerate all older crossing archives; their separate replay
commands remain in the earlier proof notes.

Without `--worker`, the new verifier checks the archived connections' chaining
and reconstructs the gates, but does not rerun the connection computations.
An independently useful gate can be reconstructed with, for example:

```sh
python post36_ladder_758.py --exponent 36 --gate 25
```

## Why the old trajectory cannot simply be multiplied by three

The previously verified power-35 trajectory supplies useful word geometry, but
its exact reset sequence does not become the new sequence by scaling. Consider
the tempting componentwise affine map
$T(a,c)=(3a+\alpha,3c+\beta)$. Commuting with the jump's left-coordinate rule
$a\mapsto3a+2$ requires $\alpha=2$. Preserving the reset section $a=1$ instead
requires $\alpha=-2$. No fixed translation of that form has both properties.
The fixed additive mass charges are the underlying obstruction.

The present construction transports common-word inequalities and the gate
proof, then verifies the new intervening orbit. It does not transport the old
orbit itself, and it does not remove the remaining gap to the known halting
basin.
