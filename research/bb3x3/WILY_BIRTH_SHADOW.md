# Coding the unallocated part of a Wily tape

For the actual blank Wily machines #531 and #532, nonhalting is equivalent to an infinite sequence of successful allocations. Each such sequence determines a unique infinite binary filling of the unallocated tape on which the ordinary, invertible sweep agrees with every physical update. A five-state machine reads that filling and recovers the sequence of corrective and ordinary allocations. This gives a proof route which allows infinitely many corrective allocations. The remaining condition is chronological: the real arriving carry has to request the token prescribed by the filling at every allocation.

## Pulling an allocation back through its sweep

Use the [single-sweep reduction](WILY_INTEGER_MAP.md). Digits are in head-facing order, least significant first. Write a configuration as an allocated word followed by an as-yet unknown right exterior. A successful arrival in mode 0, 2 or 3 creates the word 0, 1100 or 00 respectively. Mode 1 at the empty edge halts. Write these words as d_m and the invertible action of mode m on infinite rays as s_m. The only possible exterior immediately before such an allocation, if the exterior afterwards is x, is

$$ f_m(x)=s_m^{-1}(d_m x). $$

The inverse action preserves prefix agreement, so f_m multiplies distances in the binary prefix metric by exactly 2 to the power minus the length of d_m. Between allocations the exterior stays fixed. A finite list of actual successful modes therefore prescribes a cylinder of possible initial exteriors of exactly the total length allocated. For an infinite list these nested cylinders have one common point. Conversely, if the arriving modes and the successive exteriors satisfy these identities at every edge reached, the virtual sweep writes exactly the physical tape at each step. This follows by induction, including every intervening sweep that stops inside.

The [four carry rules](check_bb33.py) give the exact simplifications

$$ f_3(x)=10x,\qquad f_2(x)=1010x=f_3(f_3(x)),\qquad
f_0(x)=1s_2^{-1}(x). $$

Every infinite allocation history therefore has an exterior beginning in 1. Removing that initial 1 reduces the allocation code to two prefix contractions. Let A stand for mode 0 and let B stand for mode 3. A mode 2 contributes BB. For a subsequent exterior 1y, the preceding exterior is 1 followed by the corresponding map below, applied to y:

$$ U(y)=1s_1^{-1}(y)\quad(A),\qquad V(y)=01y\quad(B). $$

For U use the mode-2 rule on a leading 1. The two images are disjoint since they start with different bits. Every infinite A/B word gives a unique filling. This coding alone does not distinguish a single physical 2 from two successive 3s. Their common pullback explains exactly that ambiguity.

## Five viable states

Skip the compulsory 1, then read the remaining bits from low to high. The table shows the next state and, in parentheses, the token completed on that bit. Start in E. A dash rejects the prefix.

| State | Read 0 | Read 1 |
|---|---|---|
| E | L | S (A) |
| L | — | E (B) |
| M | S (B) | — |
| S | J (A) | M |
| J | M | J (A) |

To derive the table, keep a chronological word of carries to apply to the remaining raw bits. At a token boundary, a decoded 1 consumes A and adds mode 1 to undo its inverse. A decoded 0 begins B and requires a decoded 1 next. Pass each new raw bit through the pending carries in order and retain only the live output carries for the next bit. The pairs (pending word, waiting for the second bit of B) reachable from the empty word are E = (empty, no), L = (empty, yes), M = (0, yes), S = (1, no) and J = (3 1, no). The four carry rules now yield every entry. Each accepted infinite path completes a token at least every two bits. The pullbacks prove both directions of the decoder.

In particular the number of distinct complete code prefixes of raw length k, after the compulsory 1, is the Fibonacci number F_(k+1), with F_1=F_2=1. These prefixes come from compositions of k with weights 1 and 2. The Hausdorff dimension of the abstract filling set in the binary prefix metric is log₂ φ, where φ is the positive root of φ²=φ+1. For example, assign independent token probabilities φ⁻¹ and φ⁻². A complete prefix of weight k then has measure φ⁻ᵏ, and any viable k-bit prefix ends at most one bit past a complete token. These bounds give the lower dimension estimate; the prefix counts give the matching upper bound.

## Three kinds of periodic tail

The following equivalences apply to the unique filling of any infinite physical allocation history, or to any infinite abstract token history. For the exact integer values, identify a ray with its little-endian 2-adic integer.

| Eventual raw bits | Eventual decoded tokens | Exact late exterior |
|---|---|---|
| Alternating 10 or 01 | B only | (10) repeated forever at every late token boundary, including the initial 1 |
| All zero | Alternating A,B | 7 before A, 29 before B |
| All one | A only | −5 before every A |

For the forward implications feed each periodic bit sequence through the five-state table from each viable state. In the eventually-zero case the only surviving cycle is M, S, J, M. In the eventually-one case it is J, J. For either phase of the alternating sequence the eventual output is one B per two bits. The reverse implications follow by uniqueness of nested pullbacks. In particular f₀(29)=7, f₃(7)=29 and f₀(−5)=−5. These equalities hold on the entire rays by the carry rules. For example 29 starts 10111 followed by zeros and s₂ sends 3 to 29. The ray −5 starts 1101 followed by ones; s₂ sends its tail −3 to −5. A finite earlier token prefix preserves the three respective eventual bit types: inverse carries on an all-one suffix stop, on an all-zero suffix they stop or settle in mode 2, and on an alternating suffix they stop or keep alternating the input phase, as the table of four carries verifies.

Thus a nonhalting growing run has finitely many corrections if and only if its associated filling is eventually alternating. Infinitely many corrections include two distinct simple possibilities as well as nonperiodic schedules. An arbitrary accepted filling need not match the actual arrivals.

## What the blank tape adds

A mode-0 edge correction occurs at update 583, producing the 29-bit trimmed word

```
10100101010100010010101000100
```

Its primitive arrival period, with the actual starting phase, is

```
222030111101130321301012
```

Every blank run that continues forever must grow without bound. If it makes infinitely many corrective allocations this is immediate. Otherwise consider its last correction, which exists because one occurred at update 583. Immediately after every correction the actual word followed by the alternating exterior is the virtual image of a singular sweep, one which reaches every finite cutoff. Indeed on the previous word followed by 11 and then the alternating exterior, mode 0 at the former edge writes 0 followed by the alternating exterior; the continuing carry there changes its phase forever. The detailed [correction identity](WILY_PHYSICAL_CORRECTIONS.md) is F(p+6B). At every cutoff the input prefix of this past sweep recurs in the finite prefix permutation. Thus a future sweep reaches that cutoff. With no further correction the virtual and physical allocated words agree at every subsequent step until a halt. A forever-bounded successful physical tape would contradict a future arrival at its final cutoff.

This argument gives an explicit deadline at *each* width, even allowing later corrections. At any time after the first correction, choose the most recent correction and its canonical alternating completion. Up to the current state this completion and the physical evolution agree as infinite words with the current canonical padding. At trimmed width k, an arrival at k occurs within at most the current prefix's finite period many further updates. The [global period bound](WILY_TAIL_GERMS.md) makes that deadline at most 2^(1+floor(2k/3)). Until the first such arrival there is only internal evolution. The arrival either grows the tape or halts. Summing these deadlines gives O(2^(2k/3)) updates from the first correction to a halt or an allocation beyond k, for k at least 29. Thus on any infinite continuation the trimmed width is at least (3/2) log₂(t) − O(1) at update t. This lower bound and the [sublinear upper bound](WILY_GROWTH_RATE.md) concern the same reduced tape.

For this specific blank state the infinite chronological condition can now be stated without a bounded-width alternative. Start with the displayed period at an empty edge. There must exist an infinite filling 1y accepted by the decoder. At each next arrival, the next decoded tokens must be A for 0, B for 3, or BB for 2. Carry 1 fails. Consume the matched tokens, allocate the actual extension, rotate the arrival stream past its first event, and pass it through the new cells to get the next edge stream. Equivalently one may use the successive remainders of the exterior under the pullbacks. An infinite match is necessary and sufficient for the two actual blank machines to run forever. Specializing to the one proposed filling (10) repeated forever gives the shorter [24-letter first-symbol test](WILY_PHYSICAL_CORRECTIONS.md), which would already suffice.

At the later trimmed-width-69 checkpoint the [independent replay](WILY_INTEGER_MAP.md) reaches trimmed width 767 with 349 further mode-3 allocations. Thus any successful infinite continuation from that checkpoint has an exterior beginning with the certified prefix (10) repeated 349 times; longer agreement is possible. No all-depth match for the 24-letter driver is established here.

Run `python3 wily_birth_shadow.py` to derive and check the transition table, compare finite codewords in both directions, and verify the periodic cycles and allocation identities.
