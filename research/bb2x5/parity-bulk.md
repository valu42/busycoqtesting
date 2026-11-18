# Line 36 · when the data sweep becomes Rule 90

**Machine** `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---`, undefined at B4. In the normalized sweep, state A scans a blank immediately left of a word of openings (physical 1) and closings (physical 2). The blank orbit starts with the empty word. During the forward scan each closing consumes the rightmost available opening to its left. Six excess closings in some prefix reach B4. In an ordinary data stretch the return writes a closing precisely where the bit “this opening survived” changes from the previous cell. The actual left header and terminal require their own rules. The derivation and the literal interpreter are in [the sweep notes](mixed-and-sweeps.md#4-parity-sweep-on-line-36) and [prior_sweeps.py](prior_sweeps.py).

The following results concern the ordinary data dynamics with a finite set of closings surrounded by openings on both sides. The extent to which such a region remains protected from the actual boundaries is the outstanding question for the blank tape.

## Exact particles and parity domains

Let C be the finite set of closing positions on the integer line. Match its elements from left to right to the nearest unused opening on their left. Let M be the set of matched openings and B=C∪M. The zeroes in the survivor mask are precisely B. The next set of closings is therefore

**F(C) = B △ (B+1),**

where +1 shifts a set one cell to the right and △ denotes symmetric difference. Each maximal interval [a,b] of B produces exactly a and b+1. Such an interval has even length 2q and contains q closings. Indeed a match cannot cross an unused opening, which splits the intervals, and every cell within an interval is matched. Its last cell b must be a closing.

Color a closing by its position modulo two and count color changes in the ordered list of closings. Under F this count never increases. Each matched interval replaces all its closings by two positions of the same color, opposite to the color of its last closing. The sequence of new colors is obtained by taking an ordered subsequence of the old colors, flipping all of them and duplicating each. None of these operations adds a change. In any interval containing closings from s+1 successive color runs, closings minus openings is at most s+1. Partition the interval into pieces containing one color of closings each. In a consecutive sequence of cells, one parity can occupy at most one more cell than the other. Thus a seed with at most four color changes never develops a six-deficit interval under *any* number of boundary-free sweeps.

If C has no adjacent elements, every closing consumes the immediately preceding opener. Substitution in the formula gives F(C)=(C−1) △ (C+1). If all elements of C have one parity, this remains true forever, with the parity flipping on each sweep. This is the elementary cellular automaton Rule 90. In particular 2ʳ sweeps give the symmetric difference of just the two translates by ±2ʳ, by repeated squaring over the field with two elements.

## A finite-window theorem for an arbitrary finite seed

Suppose C is nonempty. Its rightmost closing moves right by one each sweep. Measure distance j to the left of that closing, so the leading particle always has j=0. In this moving frame the following rule is exact.

* Read the distances in increasing order. Start a cluster at the first unread j and set b=j+2.
* While the next distance is at most b, consume it and increase b by two.
* Emit j and b, then repeat with the next unread distance.

To derive the rule, scan a matched interval from right to left. Its first cell is a closing. Each of its q closings consumes one cell itself and one opening, giving interval length 2q. A new closing inside that interval or immediately adjacent on its left joins the same maximal interval and adds two cells. A gap of at least one unused opener ends it. Shifting the origin with the new leading particle puts the two emitted endpoints at j and j+2q. In particular, all output distances at most J are determined by the input distances at most J. An unseen closing can only extend or start a cluster whose changing endpoint already exceeds J.

**Theorem.** For any r≥0, after at most (r+1)(r+2)/2 sweeps, every closing at distance at most 2r+1 has even distance. This persists for all later sweeps. Inside the cleared prefix, the subsequent dynamics is linear.

Prove this successively for odd positions s=2r+1. Once smaller odd positions are permanently empty, the even sites 0,2,…,2r evolve autonomously. Their bits form a polynomial A(X) modulo Xʳ⁺¹. One sweep multiplies A by 1+X: consecutive occupied even sites form a cluster, leaving its first site and the first even site after the run. No later input can affect a lower output distance. In particular A(0)=1 forever.

If an odd particle is present at s when distance 2r is occupied, it belongs to the even cluster immediately to its right and is erased at the next sweep. After s becomes empty it stays empty, since an odd endpoint at s could only come from an odd cluster head at or before s. Some time t in 0,…,r has site 2r occupied. Its bit is the coefficient of Xʳ in (1+X)ᵗA. As t ranges from 0 through r these coefficients form the product of the binomial matrix (binom(t,k) mod 2) with the vector (Aᵣ,Aᵣ₋₁,…,A₀). The matrix is triangular with unit diagonal and the last component of that vector is 1, so the coefficients cannot all vanish. At most r+1 further sweeps therefore clear s permanently. Summing from 0 through r proves the bound, including r=0. This theorem is local in the moving frame. It does not assert a uniform clearing time for the entire growing support.

## Restoring both boundaries of the actual tape

The same clusters give an exact sparse update of the finite tape word. For this update j=0 means the **last data cell** of the finite word, whether open or closed. Keep its length L and the set of closing distances j. Run the cluster construction above with these distances. An emitted pair (a,b) describes the interval of virtually matched input cells a≤j<b. Set D=max(0,bₗₐₛₜ−L), using zero when there are no clusters. This is exactly the number of unmatched closings in the physical word: the virtual matching has borrowed that many additional opening cells beyond its left end. Thus D≥6 reaches B4. Below that threshold, the following update realizes one complete TM epoch.

1. Put g=1,3,2 for D modulo 3 equal to 0,1,2 respectively. The raw left header is the single cell g when D<3, and the sequence 1,3,3,4,g,2 otherwise. Write h for its length. These are the guard rows in the literal sweep derivation.
2. Let t=1 if L>0 and j=0 is open, and t=0 if it is closed. The final open always survives because nothing follows it. For L=0 take t=0. The new length is h+L+t; if t=1, put a closing at new distance 0.
3. For each cluster (a,b), each of a−1 and b−1 that lies in [0,L−2] gives a new closing at that distance plus t. These are precisely the ordinary changes in the survivor bit when comparing a cell to its neighbor on the left. For the first data cell j=L−1, use the header carry as its left neighbor instead. Its survivor bit is 1 exactly when the last interval ends strictly before L (or the nonempty data contains no closing). Add the closing if this bit differs from the indicator that the final header digit equals 3.
4. Process the raw header from left to right, initially with a clear carry. A raw digit v writes a closing if the bit [v≠2] differs from the old carry, and sets the carry to [v=3]. Header position i, starting at zero, has new distance h+L+t−1−i.

This is the function `finite_sweep`. It is also an exact iteration from blank starting with (0,∅). The bulk endpoint rule alone would use the wrong neighbors at both tape ends.

A consequence for the true blank run is that, from epoch 2 onward, the last cell is closed at every even epoch and open at every odd epoch, for as long as the epochs exist. The initial words are empty, 2 and 22. For any nonempty word ending open the return appends a closing. For length at least two ending closed, the last two cells have both been matched: a penultimate opening is consumed by the final closing, and a penultimate closing is itself matched or uses the guard. Their survivor bits both vanish, so the new last cell is open. Every successful epoch adds at least one cell, which maintains the length hypothesis. In particular after N≥2 completed epochs the length equals N+⌊(N−2)/2⌋+5R, where R counts resets with D in {3,4,5} during epochs indexed 2 through N−1. This identity leaves the future reset sequence undetermined.

## Connection to the remaining holdout

The bulk identity agrees with the true data sweep whenever the matched intervals under examination are separated from both boundary operations by surviving openings. Padding an arbitrary finite seed with sufficiently many openings gives an exact one-sweep comparison on its whole ordinary interior. The real header can nevertheless inject three new parity changes in a single epoch. For example, the normalized tape word `1121` returns as `222122`, increasing the count from zero to three. That is an auxiliary finite-tape example. A proof for blank would have to bound the parity changes or their effects near the *real* guard, or account for the incoming boundary particles explicitly.

Run `python3 parity_bulk.py` with assertions enabled. The script compares the independently derived cluster algorithm against finite padded TM data sweeps on all binary words of lengths 1 through 9, with independent elementary TM replay through length 4. It also checks the clearing bound, linear evolution afterward, and the boundary example. [Observed output](parity-verification.txt)
