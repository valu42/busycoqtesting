# The initial address forced by the moving edge of #397

Use the [29-bit return on the actual blank orbit](TRANSITIVE_SECTION_397.md). After sweep 64 the remaining physical suffix is empty. It receives the same 33 carries S every 1,024 sweeps. This note gives a coding of all successful edge histories and an additive coordinate for the actual blank history. Bits are listed from the head-facing end, least significant first.

## Extending a physical run to a fixed binary tape

On an infinite binary tape each carry acts as an invertible map preserving prefixes. Ask which initial fillings of the empty physical tail give exactly the physical bits, whenever they become occupied. At an edge growth labeled m, let x denote the unoccupied part of the *virtual* tape immediately after growth. Before growth, the previously unoccupied virtual suffix must be exactly the following word.

| Edge carry m | Physical bits appended | Required previous virtual suffix fₘ(x) |
|---|---|---|
| a | 1 | 0 c⁻¹(x) |
| b | 01 | 11 x |
| d | 001 | 000 c⁻¹(x) |
| f | 1001 | 1111 x |

These identities hold for every infinite x and on finite projections. Apply each carry to the required leading bits in the [sweep table](check_bb33.py). The outgoing action on the unknown suffix is c for a and d, and identity for b and f. Between consecutive growths all physical inputs stop inside the occupied prefix, so the corresponding virtual operations leave the unoccupied suffix unchanged. Therefore after births m₁,…,mⱼ the complete set of possible *initial* fillings is the cylinder

    fₘ₁ ∘ fₘ₂ ∘ … ∘ fₘⱼ (all infinite binary words).

Its prefix length is exactly the total number of physical bits grown. If the blank trajectory survives forever, its suffix grows without bound by the transitive-section theorem, and the nested cylinders specify a unique initial filling z. The fixed infinite trajectory starting at z agrees with the physical trajectory on every occupied cell at every step.

The identity c(00w) = 11 c(w) implies f_d = f_a ∘ f_b. Also f_f = f_b ∘ f_b. Thus every infinite string of safe labels has the same encoding as a word in just a and b, by replacing d with ab and f with bb. Conversely any abstract a,b word is a string of safe labels. This is a statement about extension compatibility. The source S determines which labels actually reach its physical edge.

Write K for this set of abstract infinite encodings. Its canonical labels are uniquely decodable. Read 0 as a, erase it, and apply c to the remaining bits. Read 11 as b and erase both. A leading 10 rejects the word. This follows from K = f_a(K) ∪ f_b(K) with disjoint leading digits. If N(k) is the number of distinct k-bit prefixes of K, then N(0)=1, N(1)=2, and N(k)=N(k−1)+N(k−2) for k≥2. The c⁻¹ permutation preserves the number of prefixes at each length. Thus N(k) is the Fibonacci number Fₖ₊₂. In particular K has zero Haar measure on the 2-adic integers.

In the metric where agreement on k leading bits gives distance at most 2⁻ᵏ, K has Hausdorff dimension log₂((1+√5)/2). Indeed the two branches reduce distance by factors 1/2 and 1/4, respectively. For the lower bound give each branch of length L probability 2^(−δL), with δ the stated dimension so the two probabilities sum to one. A k-bit cylinder determines complete branches up to at most one residual bit. Its mass is at most 2^δ · 2^(−δk). The matching upper bound follows from the prefix count.

## Conjugacy to addition

At depth k define θₖ(w) as the unique t mod 2^k for which Sᵗ(0ᵏ)=w. The fixed-width return is a single cycle at every depth. The θₖ therefore exist, are bijective, and commute with truncation. They give a tree isometry θ with θ(Sz)=θ(z)+1 on the 2-adic integers. In particular θ(K) has the same prefix counts and dimension as K.

If t complete copies of S have elapsed and the live physical word w has length k, its initial address is forced modulo 2ᵏ to be θₖ(w)−t. This residue is unchanged until the next birth, when it lifts uniquely to a residue at the new width determined by the birth table. Thus an infinite blank run would be the growing physical prefix of an adding-machine orbit with a single offset q=θ(z) in θ(K).

The first 128 copies on the actual blank tail give the following labels and force this 47-bit initial filling.

    bbbbbbbbbddbbbbbbddbd
    11111111111111111100010011000000000010001011111

The initial offset is **q ≡ 682,853 mod 2²⁰**. The [checker](birth_address_397.py) obtains the labels by sweeping the physical suffix, constructs the initial filling online, and runs a second copy of all 4,224 input carries on the fixed 47-bit tape, checking agreement with the physical tape after every carry. It then enumerates the fixed 20-bit orbit from zero to verify the offset.

## Consecutive d pairs

Consider the stronger hypothesis that births use b and f, with d occurring in adjacent pairs separated by at least one b or f, and with a b or f after every pair. This is an assumption about the order at the physical edge. After replacing f with bb we can use blocks b and p = ddb. The possible *initial fillings* now have a five-state encoder. Each entry gives the additional bits fixed at the head-facing end of the unknown initial suffix and the next encoder state.

| State | b | p = ddb |
|---|---|---|
| I | 11 → I | 00010011 → c |
| c | 00 → c | 10001011 → cf |
| cf | 00 → ce | 11101011 → cf |
| ce | 01 → cb | 10010011 → cf |
| cb | 10 → c | 00001011 → cf |

The state represents a chronological string of inverse carries, with I the identity. For a raw birth m, apply the state to the forced leading bits in the first table, output their image and retain the section of the state on these bits. Prepend c⁻¹ to this section for a or d, as specified by fₘ. The checker verifies the displayed transitions directly against the inverse sweep table with an unrestricted suffix.

At each state the two branches have different first bits. They fix two bits and eight bits, respectively. The same cylinder argument gives the abstract paired code dimension δ ≈ 0.232479, where 2^(−2δ)+2^(−8δ)=1. For the lower bound at most seven trailing bits of a cylinder remain outside its completely determined blocks. If infinitely many p occur, each contributes both digits, so the initial filling is not eventually constant. If only finitely many p occur, the table gives a constant tail, all ones if there were no p and all zeros otherwise.

Every forward and inverse carry maps eventually constant tapes to eventually constant tapes. The checker treats a constant input bit as fixed, follows each carry until it stops or enters a cycle, and verifies that the output on every such cycle is constant. Thus all Sʲ(0∞) for ordinary signed integers j are eventually constant. **Under the paired hypothesis, infinitely many d pairs imply that the blank offset q cannot be an ordinary signed integer.** This gives a consequence for the infinite orbit. The paired hypothesis and the identity of the next arriving edge label are unproved at unbounded depth.

Run `python3 birth_address_397.py` from this directory.
