# A six-valued invariant for Wily excursions

The negative blank-connected checkpoint `n_* = −227089934777573210432` has dihedral label equal to the identity. This label is constant on every step of its negative excursion. Together with the residue modulo three, it excludes asymptotically **eleven twelfths** of the [two-root sign-escape forest](WILY_EXCURSION.md), by generation. Infinitely many candidates retain the blank labels; the first is −62 at generation three. Their visitation from blank remains open.

## Computing the label

Use affine permutations `z ↦ sz+t` of the three residues, with `s` equal to 1 or −1. Products are ordinary composition: the right factor acts first. Associate these elements to bits and carries.

| Object | Permutation |
|---|---|
| Bit 0, denoted X | z − 1 |
| Bit 1, denoted Y | 1 − z |
| Carries s₀, s₁, s₂, s₃, denoted a, b, c, j | 1 − z, z − 1, z + 1, −z, respectively |
| Early stop | Identity |

For each input bit with label D and output bit D′, the incoming and outgoing carry labels obey `s D = D′ s′`. These are the eight entries of the sweep table. Read the digits of n/3 from least to most significant and multiply their labels from left to right. Stop at a multiple of four beyond which the digits alternate. Both `XYXY` and `YXYX` are identity, so every such cutoff yields the same product Q(n). Compute the digits by taking the low bit d and replacing n by (n−3d)/2; the two purely alternating tails have numerators −1 and −2.

Define K(n) = Y^(n mod 2) Q(n). When s₀ stops internally on the virtually completed word, Q(F(n)) = Y Q(n): propagate the initial carry through the product to its first stop, with the subsequent factors unchanged. The first bit flips on every s₀ update, so K(F(n)) = K(n). An unstopped carry in an alternating tail necessarily alternates between s₀ reading 0 and s₁ reading 1. It complements the alternating background and changes the numerator's residue modulo three. Thus every residue-preserving scalar step has the claimed invariant. In particular it applies throughout the negative excursion from the [blank checkpoint](WILY_INTEGER_MAP.md).

| Numerator | Residue | K, written as z ↦ |
|---|---:|---|
| Blank n_* and its last positive predecessor p_* | 1 | z |
| −8 | 1 | 1 − z |
| −16 | 2 | z − 1 |
| −26 = L(−8) | 1 | 2 − z |
| −7 = S(−8) | 2 | −z |
| −58 = L(−16) | 2 | z − 1 |
| −23 = S(−16) | 1 | −z |
| −62 = L(S(S(−8))) | 1 | z |

The sign of the permutation supplies a simpler binary test: each 1 contributes one reflection and each 0 a rotation. At four-digit alignment the alternating background has an even number of ones. Thus this component of K is the parity of all bits differing from the background, plus the low input bit.

On a singular scalar step the aligned product retains the inverse of the carry still active at its high end. On the residue-1 background `(01)∞` that carry is a, and on residue 2 it is b. Therefore K(F(n)) = K(n) a on a 1-to-2 change and K(F(n)) = K(n) c on a 2-to-1 change. A pair of flips starting at residue 1 multiplies K on the right by ac = j; starting at residue 2 it multiplies by ca = R, where R(z) = 2−z. Both reflections have order two. Consequently a complete virtual F-cycle has a multiple of four residue flips. On the full virtual orbit through the blank checkpoint the successive possible states (residue, K) are (1, identity), (2, Y), (1, j), (2, X), then back to (1, identity). Ordinary steps stay within their current state.

## The actual finite edge

In the scalar physical model the seed is `001100`. For its finite word w, use the actual product D(w), with no padding, and normalize it by Y to the parity of the number of scalar sweeps. At an interior stop the normalized product is unchanged. If carry e reaches a growing edge, its right multiplier is e⁻¹ D(extension). For modes s₀ and s₃ this is the same reflection R(z) = 2−z, from extensions `0` and `00`. For s₂, extension `1100` gives the identity multiplier. The initial finite product is X, so **every successful physical update stays in {X, XR} = {X,Y}**, including an s₀ correction. Compatible words can still halt; for example, the one-bit word `0` has finite product X and sends s₁ to the empty edge.

## Counting all sign-escape endpoints

The long lift L prepends `01` to the virtual word. The short lift S first flips the low bit and then prepends `1`. This follows directly from L(m) = 4m+6, and S(m) = 2m−3 for odd m or 2m+9 for even m. Define R(z) = 2−z. The 12 states (residue, Q) obey the following transfer table. Right factors account for restoring alignment to a multiple of four in the old alternating background.

| Old residue r | Long lift | Short lift |
|---:|---|---|
| 1 | (1, j Q j) | (2, c Q Y) |
| 2 | (2, j Q R) | (1, c Q c) |

In particular each letter separately permutes the 12 states. From every state all 12 states occur after six lifts, as the [checker](wily_dihedral.py) verifies by direct enumeration. The normalized six-step transition matrix is therefore doubly stochastic and every entry is at least 1/64. Subtracting 1/64 from every entry leaves a nonnegative remainder with row and column sums 52/64. Repeated six-step application thus converges to the uniform distribution. The roots have disjoint descendant trees, since the two lift types have different parities, invert uniquely, and all nonroot descendants fail the roots' multiple-of-four test. Hence weighting paths equally counts distinct endpoints at each generation.

After a long lift the endpoint is even, so the blank tests require state (1, identity). After a short lift it is odd, so they require (1, Y). Each lift type preserves uniformity. The limiting passing fraction among all endpoints is exactly 1/12. The first ten positive generations have respectively **0, 0, 1, 2, 6, 9, 21, 36, 82, 165** endpoints passing. This count makes no distributional assumption about the blank orbit.

## Why the bit-product construction gives the dihedral group

Allow arbitrary group elements x,y for the two bits, and a,b,c,j for the four carries. Impose the eight local sweep equations only. The two j rules give y = jx and j² = 1. Write j_i = xⁱjx⁻ⁱ. From the b rule on 0 and the a rule on 0 we obtain b = j₀j₁ and a = j₀j₁j₂. From the b rule on 1 we also have a = j₋₁j₀j₋₁. The c rules give cx = xc and c = a j₀. In particular c = (j₋₁j₀)², hence (j_i j_(i+1))² = c at every shift.

Each j_i inverts c by conjugation, since it inverts the adjacent product whose square is c. But c = j₀j₁j₂j₀ also gives j₁j₂ = j₀cj₀ = c⁻¹. Thus every adjacent product equals c⁻¹, and squaring gives c³ = 1. Now b = c⁻¹, a = cj, and xjx⁻¹ = j c⁻¹ = c⁻¹jc. Consequently cx is central, and the whole group is generated by this central element, c of order dividing three, and the involution j inverting c. The explicit affine permutations above realize the full order-six dihedral group. One can independently attach a free integer length to each bit and zero length to every carry. These assignments realize the direct product of the dihedral group with an infinite cyclic length factor, so there are no further universal group labels of this multiplicative one-bit type. The length factor cancels in a fixed-width comparison.

## Rigidity for finite-range additive charges

Consider an additive charge with values in any abelian group. Each summand may be an arbitrary function of a bounded window of bits, and may depend on the digit position. Define differences by summing against the corresponding alternating reference so the sums are finite. Suppose its change on every internally stopping scalar step depends only on a bounded prefix. Apart from a bounded-prefix contribution, the only such charges are a single coefficient times the parity of the differing bits; that coefficient must satisfy 2a = 0. The same conclusion holds when requiring the change rule only for negative input and output.

To see this, expand every local function in multilinear monomials in its binary variables by inclusion-exclusion and collect terms with the same participating positions. Constant terms cancel on comparison. A stopping s₃ can be put at any sufficiently large position i: start s₀ on 1, hold s₂ for arbitrarily many zeros, then read 1 and 0. Carry s₃ flips precisely bit i and leaves every higher bit unchanged. Those higher bits can be prescribed arbitrarily over any finite window. Changing a still higher background one to zero, beyond the inspected region, can force both numerators negative without changing the computed difference.

For a greatest remaining interaction span k > 0, vary bit i+k. In the charge difference the only terms which can then change include both i and i+k: an earlier changed bit is too far away, and every later bit is unchanged. The coefficient of the far bit is therefore the signed sum of the monomials on the freely chosen intermediate bits, with the sign determined by bit i. It must vanish for every intermediate assignment. Boolean inclusion-exclusion shows that each of its coefficients vanishes. Apply this argument at every sufficiently high i, then descend in k to remove every interaction away from the bounded prefix.

Write a_i for the remaining site weights. Varying just the bit flipped by the terminal s₃ shows 2a_i = 0 at every sufficiently high i. At those positions all flips therefore contribute a_i in either direction. For a carry already at position i, the total charge change above it must be independent of the stopping continuation, by fixing the prefix that brought it there. Every carry can be brought to every sufficiently high position using the s₂ zero loop. The two successors of s₂ show that the future contributions of s₂ and s₁ are a common constant c independent of position. The contributions from s₃ and s₀ at i are then a_i and a_i+c. The two possible successors of s₁ now give c = a_i+a_(i+1) = a_i+a_(i+1)+c, forcing c = 0 and a_i = a_(i+1). Conversely the parity telescopes: the incoming weights of s₀,s₁,s₂,s₃ are (1,0,0,1), and each weight is the bit-flip indicator plus the outgoing weight modulo two. This proves the stated classification. It imposes no restriction on unbounded interactions, nonadditive quantities, or one-sided inequalities.

Run `python3 wily_dihedral.py` in the research directory.
