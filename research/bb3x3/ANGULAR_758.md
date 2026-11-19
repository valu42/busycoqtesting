# A blank-reachable test of angular and modular invariants for #758

The true blank trajectory reaches the state with a = 1,408,855,846,243,751 and c = 375,573,977,278,745. Its next reset occurs **22 map calls later**, at second counter **1,080,001,900,400,671**. If the two counters are represented by their exact mass, their residues modulo a fixed integer, and one of 1,024 angular bins, the same reachable state can instead begin an infinite path in that representation. This rules out a proof of the basin crossing based solely on the cells and elementary transitions specified below.

The witness comes 771,519,141 calls after the [certified common blank checkpoint](FRONTIER.md). Write W = a + 2c. For each positive modulus M ≤ 32,000,000,000 whose power-of-two factor is at most 2¹⁷, retain the following data about the current state:

* the **exact** integer W;
* both a and c modulo 2M;
* the angular bin floor(1024(c−1)/(W−1)) for W > 1.

Two cells are connected whenever some integer input in the first cell takes the published live transition to the second. An invariant consisting of whole cells and preserved by these edges must contain every cell on every path from a reachable cell. The result applies, for example, to M = 2¹⁷·3¹¹ and to M = 3²². The exact mass still identifies the crossing of the verified halting band.

## The entry state

At an odd mass put u = (W−1)/2 and d = (c−1)/2. The witness has

```
u = 1,080,001,900,400,620
d =   187,786,988,639,372
floor(1024d/u) = 178
529d − 92u + 900 = −20,857,846,628,352.
```

The last integer is divisible by 2¹⁷. The true continuation follows four copies of BBJ and then departs from that word. B here denotes one ordinary bulk move on a second counter congruent to 1 modulo 4. [Published counter rules and model](RANKINGS.md) · [Prior two-sided BBJ calculation](cut_residues.md)

## Constructing the infinite path through integer transitions

Set t(u) = (92u−900)/529. Under BBJ the map takes (u,x) to (u+7,(27x−4u+44)/4), and carries t(u) exactly to t(u+7). The rational t(u) has a residue at every power of two because 529 is odd. Its residue modulo 4 is zero.

Let r be the exponent of two in M. At the start of each BBJ period keep a cell of bin 178 whose second counter corresponds to d modulo M and satisfies d ≡ t(u) modulo 2ʳ. This holds at the displayed blank witness. For each period choose an integer x in [t(u),t(u)+4M) solving both congruences

```
x ≡ d       (mod M)
x ≡ t(u)    (mod 2^(r+2)).
```

Their compatibility modulo 2ʳ implies a solution every 4M integers. At fixed W, changing d by a multiple of M preserves both counters modulo 2M. In particular the integer x belongs to the specified residue cell.

For every u at least the witness value and every allowed M, the whole interval [t(u),t(u)+27M] lies in angular bin 178. The exact inequalities follow from 178/1024 < 4/23 < 179/1024 and the numerical bounds checked at the witness. Thus x has the required starting bin. Since x is a multiple of four and 9x ≤ 2u−12, the two B moves are legal. They give u₁=u+5 and d₁=(9x+20)/4. The inequalities (u+4)/3 < d₁ < (u+4)/2 give the next odd/odd J move. The verifier checks all these inequalities uniformly, including the monotonicity of their margins with u. Both bulk moves occur strictly inside their region, with intermediate first counter greater than one.

The endpoint's distance above t(u+7) is 27(x−t(u))/4 < 27M, so its bin is again 178. Its residue modulo 2ʳ agrees with t(u+7), by the extra two binary digits chosen at the start. Its actual residues modulo 2M specify the next cell. This constructs the next period for every u along the path. All three elementary edges of each period are witnessed by a single integer execution. Between periods one is free to choose another integer representing the same cell. No period resets and the mass rises by 14 each time, so this abstract path crosses the entire halting band. The deterministic blank run's short return and this alternative continuation are distinguished by the discarded exact coordinate.

## Reproduction

Run [check_758_angular.cpp](check_758_angular.cpp) with assertions enabled. It replays the reachable witness from the certified checkpoint, checks the exact next reset and verifies the endpoint arithmetic for the uniform bounds.

```sh
c++ -O3 -std=c++17 check_758_angular.cpp -o /tmp/check_758_angular
/tmp/check_758_angular
```
