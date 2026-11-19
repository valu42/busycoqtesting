# Rational directions after the cusp prefix for machine 758

Let \(K\subset[0,1]\) be the closed survivor set of the normalized direction map. Its inverse branches are \(x\mapsto x/3\) and \(x\mapsto(4x+5)/9\). The aligned directions below the [lifted targets](LIFTED_BASINS_758.md) have the form
\[
x=D h_d/3^e,\quad 1/3<x<1,\qquad D=13{,}959{,}275.
\]
Here \(e=15+r\) and the offsets \(d\) are even. This note treats the normalized direction. Each finite strict itinerary holds in the actual machine at a sufficiently large lift for fixed \(d\). Infinite agreement at a single lift does not follow.

**Across all positive aligned headers, there is a survivor if and only if \(K/5\) contains a rational \(a/4^p\) with \(p\ge1\) and \(a\) odd. If there is one, a header with \(d\equiv0\pmod{32768}\) already suffices.** A survivor of either kind would have a unique aperiodic address.

## From a header to a dyadic rational

Write \(L=K/5\subset[0,1/5]\). Its forward branches are \(J(y)=3y\) and \(P(y)=(9y-1)/4\). The last bulk of the common prefix acts on an even left counter \(a\) by \(a\mapsto a-4q-3\). Before that bulk \(a\equiv2\pmod4\): start the prefix at \(a=2\,3^m-1\equiv1\pmod4\) for the even family exponents \(m\), and each of the first eight bulks adds one modulo four. The intervening jump preserves residue one, and the next five bulks give residue two. Thus the last bulk produces \(a\equiv3\pmod4\) and \(h_d=(a+1)/2\) is even. The initial \(y=x/5\) therefore has even numerator over a power of three, including after reduction. Its first surviving branch must be \(P\), giving odd numerator and a factor of four in the reduced denominator. Each \(J\) removes one available factor of three from the denominator and each \(P\) removes up to two. After at most \(e\) blocks a survivor has reduced form \(a/4^p\) with \(a\) odd and \(p\ge1\). All further \(J\)'s preserve \(p\), and all further \(P\)'s increase it by one.

Any infinite surviving address from such a point must contain infinitely many \(P\)'s: an eventual pure \(J\) itinerary forces the value zero. Consequently the reduced denominator is unbounded and the orbit cannot repeat. An ultimately periodic symbolic address would repeat a point by uniqueness of the fixed point of its contractive period. Disjoint first-level intervals ensure uniqueness of the address.

## From a dyadic rational to a header

The exact header recurrence gives \(h_0=0\) and \(h_{32768q}=2Dq\). Set \(M=D^2/5\), an odd integer coprime to three. Given a surviving dyadic direction in \(L\), advance it until its reduced denominator is \(4^p\) with \(p\ge M\). Invert exactly \(p\) pair branches, inserting any number of inverse jumps. Use the inverse maps \(S(y)=y/3\), \(R(y)=(4y+1)/9\).

Reserve one final, outermost \(R\). Each of the other \(p-1\) operations can be programmed modulo \(M\) to apply either \(z\mapsto4z+1\) or \(z\mapsto4z+3\). Indeed \(S^i R S^j\), composed right to left, has slope \(4/3^{i+j+2}\) and translation \(1/3^{i+2}\). Choose \(i+j+2\equiv0\pmod{\operatorname{ord}_M(3)}\), and choose \(i\) so that \(3^{-i-2}\) gives the desired translation. Nonnegative exponents always suffice.

After \(k\) programmable operations the reachable values differ from the all-ones choice by the subset sums of \(2,2\cdot4,\ldots,2\cdot4^{k-1}\) modulo \(M\). At each stage the next summand is a unit. Translation by it preserves no nonempty proper subset of the cyclic additive group, so each stage increases the number of possible residues by at least one until every residue occurs. Thus \(p-1\ge M-1\) allows the value immediately before the outermost \(R\) to equal \(-1/4\pmod M\). The last \(R\) gives a residue of zero.

Just before this last \(R\) the value has the form \(b/(4\cdot3^v)\) with \(b\) odd. The final value is \((b+3^v)/3^{v+2}\), with positive even numerator divisible by \(M\). It lies strictly between \(1/9\) and \(1/5\) since the dyadic point has an aperiodic address. Additional multiples of \(\operatorname{ord}_M(3)\) in an inner jump run can make the displayed exponent \(e=v+2\) arbitrarily large without changing the modular calculation. Consequently the unscaled point is exactly \(2D^2q/3^e\) for a positive integer \(q\). It lies in \((5/9,1)\), so \(e\) is its alignment exponent for the offset \(d=32768q\). Each fixed such offset permits the established cusp prefix at sufficiently large lifts. No bound on the offset in the original finite target is implied.

## Scope

This equivalence isolates a rational-membership question. A normalized permanent survivor would give a rational with an aperiodic address for an affine rational-preserving Cantor set. Schleischitz's Theorem 4.3 gives periodicity under a unimodularity hypothesis, and Problem 3 asks whether it holds for general rational-preserving systems. The multiplier \(4/9\) falls outside that theorem. Neither the equivalence nor the general theorem proves escape for the machine's directions or decides blank entry. [Schleischitz, *On intrinsic and extrinsic rational approximation to Cantor sets*, Theorem 4.3 and Problem 3](https://arxiv.org/pdf/1812.10689)
