# Reconstructing an ordinary #758 history from its jump and bulk directions

Let J denote one odd/odd jump and L one ordinary bulk move on an odd right counter. L ignores which of its two residue branches was taken. At odd/odd boundaries let P=LL, W=a+2c, u=(W−1)/2, and d=(c−1)/2.

* A prescribed past word of arbitrary length ending at a known configuration has **at most two** ordinary origins. One earlier mass distinguishes them. For a fixed mass at the end we can count the compatible ternary residues exactly, even when all the bulk residues have been erased.
* At a fixed starting mass, **1,870 future elementary directions** identify at most one configuration that follows them with W≤2H+1 throughout. With a single preceding direction, **1,082** suffice. Here H is the known halting reset seed.
* When two preceding directions are given and the last is J, the exact worst-case lookahead is **783 calls**. There are two configurations with a JJ past that execute the same 782 subsequent moves.
* There are two distinct starting configurations at the same mass below H in u that follow the **same 812 future directions**. One is on the known excursion from the test seed 3²⁹²+4,742. The earlier jump distinguishes the two.

These results give a decoder if a putative crossing word is supplied. They leave open which word the blank run takes at the halting interval.

## Inverting a prescribed coarse word

On its ordinary branch L sends (a,c) to (a−4q−3,6q+5), with q=⌊(c+1)/4⌋. At the result (b,f) there are at most two predecessors. They require f=6q+5 and are (b+4q+3,4q−1) and (b+4q+3,4q+1). They have the same left counter and right counters differing by two. Call such states siblings. The inverse of J, when integral, is ((b−2)/3,f+(b−2)/3−1). It preserves the sibling relation. Among two siblings at most one has its right counter congruent to 5 modulo 6, so only that one can have an incoming L. Induction in reverse order gives at most two possible states at each time. Filtering for the original nonnegative counters and guards can only delete states. This costs a linear number of integer-arithmetic operations in the word length. A surviving pair of siblings differs in W by four, so even the earlier W modulo 3 selects at most one. Replaying the selected origin also recovers every erased bulk residue.

Here is the exact arithmetic count before imposing physical guards. Fix the terminal u and a word of j jumps and p pairs in any order. Put e=j+2p. Count distinct terminal residues d modulo 3ᵉ.

| Required information about the earlier mass | Number of residues |
|---|---:|
| Earlier mass unspecified, p=0 | 1 |
| Earlier mass unspecified, p≥1 | 2²ᵖ⁻¹ |
| Earlier mass exactly u₀ | binomial(2p,t) if t=(u−u₀−2j−5p)/2 is an integer in [0,2p], zero otherwise |

To verify the count, distinguish the low L with incoming c=1 modulo 4 from the high L with incoming c=3 modulo 4. They add 5 and 9 to W, respectively. The total increment in u is 2j+5p+2t for t high moves. Every choice of the 2p high/low labels corresponds to exactly one residue of the terminal d. Indeed the four [paired formulas](CUT_DENSITY_758.md) send (u,d) to (u+v,(9d+b)/4). J sends it to (u+2,3d−u+1). Once the labels and terminal u are known, every intermediate u is fixed. Composition has 4ᵖd_final=3ᵉd_initial+K for an integer K. This gives exactly one ternary residue because 4 is invertible modulo 3ᵉ. Conversely this congruence enforces every inverse denominator, by successive division by 3 or 9 starting at the end. At each P it also forces its prescribed input modulo four, as 9d_old=4d_new−b.

A fine labelling with a bulk has exactly one partner in its residue. At the earliest elementary L substitute the other sibling input and leave all later states unchanged. All earlier moves are Js, whose inverse integrality and left parity depend only on the left counter. Thus both signed-integer histories exist. The width-two decoder rules out a third. Exactly one of these two labelled histories takes the earliest L high. At fixed t there are therefore no collisions, giving the binomial count in the table. At a physical mass these residue sets are necessary. The inverse margin argument in [CUT_DENSITY_758.md](CUT_DENSITY_758.md) supplies sufficient interior guards when there is space for the word.

## How long can two distinct configurations share a future?

Take two odd/odd configurations at the same u with d₁<d₂. On a common word put A=a₁−a₂ and C=c₂−c₁. Initially A=4(d₂−d₁), C=2(d₂−d₁). Common Js and Ls preserve these nonnegative orders. J sends the gaps to (3A,C+A). L sends them to (A+4h,6h), where h=⌊(c₂+1)/4⌋−⌊(c₁+1)/4⌋≥C/4−1/2. The half-unit bound uses odd right counters. For D=min(A,2C), these inequalities give

$$
 D'\ge 3D\quad(J),\qquad D'\ge 3D/2-6\quad(L).
$$

Write V=2H+1. Whenever D≥16, D−12 is at least four and grows by a factor of at least 3/2 on every subsequent letter. Since D≤V this allows at most 789 further calls, using 4(3/2)⁷⁹⁰>V.

An initial L can merge the two right counters even though the left counters still differ. The following bounds account for this small-gap behavior.

1. A run of Ls has length at most 786. In each L, c+7 grows by a factor of at least 3/2. Its initial value is at least 8, its final value at most V/2+7.
2. Suppose C=6, and each of n next Ls leaves C=6. For the smaller right counter every such step requires c=3 modulo 4, and sends c+13 to 3(c+13)/2. The starting c+13 must be divisible by 2ⁿ⁺¹ for n≥1 because at each input it is divisible by four. Its final value is at least 2·3ⁿ and at most V/2+13. Consequently n≤291.
3. Before the first J there are at most 786 Ls and A≥4. Immediately after that J we have A≥12 and C≥4, even if C had fallen to zero. A further J brings D to at least 24. A further L gives A≥16 and C≥6. In the latter case C is a multiple of six, so either D≥16 already or C=6. In the C=6 case the chain of preserving Ls has length at most 291, and the next letter gives D≥16. For J this follows from the jump gap formula. For L leaving that chain it follows from C′≥12.

A common prefix has at most 786+1+1+291+1+789=1,869 elementary calls. All upper bounds also cover words ending partway through the argument.

If both configurations share the immediately preceding direction, their d values are congruent modulo three. An incoming J gives d≡−u and an incoming L gives d≡2. Thus d₂−d₁≥3, so initially A≥12 and C≥6. If the difference is at least four then D≥16 already. If it is three, C=6 and at most 291 preserving Ls and one exit are needed for D≥16. Therefore the common future allows at most 291+1+789=1,081 calls in this case.

## A sharp bound after two directions ending in a jump

When the last of two preceding letters is J, the known cut mass fixes the immediately previous mass coordinate, and the earlier of the two letters fixes the preceding d modulo three. Since the last J gives d_new=3d_old−u_old+1, all candidates now share one residue modulo nine. This reasoning covers both JJ and LJ. In the latter case J still starts at an odd/odd boundary and the preceding individual L ends there.

Suppose two distinct candidates follow 783 common future letters. Initially their gap in d is at least nine, hence A≥36 and C≥18. For a common L, use the integer bound h≥⌊C/4⌋. After one, two, or three leading Ls, respectively, this gives C≥24, 36, 54 and A≥52, 76, 112. Thus the lower bounds on D after zero through three leading Ls are 36, 48, 72, 108.

If the first J follows k=0, 1, or 2 Ls, let G be the corresponding bound 36, 48, or 72. At the end, D−12≥(3G−12)(3/2)⁷⁸²⁻ᵏ>V in each case. If the word begins LLL and later uses a J, then D−12 starts the remainder at least 96. Each L multiplies this quantity by at least 3/2 and each J by at least 3. Therefore its final value is at least 192(3/2)⁷⁸⁰>V. Finally, if all letters are L, the larger starting c is at least 19. The monotone recurrence c↦6⌊(c+1)/4⌋+5 starting at 19 exceeds H after 783 iterations. This contradicts c≤V/2. All inequalities use integers in the checker.

The lower bound is attained at one explicit mass. Take u=9⌊(H−10,000)/9⌋ and d=0 or d=9. Both configurations have two legal preceding Js. At both, the next 782 moves are Ls within the bound W≤2H+1. Their next directions differ. Thus the uniform number 783 is optimal when a two-letter past ending in J is provided.

## A fixed-mass ambiguity lasting 812 calls

Start the [published reset example](RESET_WORDS_758.md) at s=3²⁹²+4,742 and perform the first 292 jumps. The resulting odd/odd state has u=s+584 and d=2,663. At this same u the adjacent d=2,664 follows the same 812 elementary directions, with a distinct endpoint. The d=2,662 state first differs at call 775 and d=2,665 first differs at call 779. For fixed initial u and a given common prefix, compatibility is an interval of integer d. Indeed intermediate d have left and right counters between those of the endpoints in opposite orders. The J guard a≤c and the L guard a≥4⌊(c+1)/4⌋+3 then hold between any two successful endpoints, with the common left parity at each step. Thus after 779 future directions the exact possibilities are 2,663 and 2,664. The preceding J selects 2,663 modulo three. Starting from the final configuration and reversing all 812 letters instead returns exactly two origins, at u and u+2.

Run the checker beside the repository's original counter map:

```sh
python3 coarse_reconstruction_758.py
```

It enumerates all 62 word/mass combinations with at most four complete blocks at two mass residues, checks 3,919 physical forward prefixes and their claimed inverses, checks the sharp 783-call bound and its 782-call witnesses, evaluates the other uniform length bounds using integer arithmetic, and verifies both ends of the 812-call example.
