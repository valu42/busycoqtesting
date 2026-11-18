# Line 36 · when the data sweep becomes Rule 90

**Machine** `1RB2LA1LA4RA2LA_0LA3RB3LB2RB---`, undefined at B4. In the normalized sweep, state A scans a blank immediately left of a word of openings (physical 1) and closings (physical 2). The blank orbit starts with the empty word. During the forward scan each closing consumes the rightmost available opening to its left. Six excess closings in some prefix reach B4. In an ordinary data stretch the return writes a closing precisely where the bit “this opening survived” changes from the previous cell. The actual left header and terminal require their own rules. The derivation and the literal interpreter are in [the sweep notes](mixed-and-sweeps.md#4-parity-sweep-on-line-36) and [prior_sweeps.py](prior_sweeps.py).

The eventual Rule 90 theorem concerns the ordinary data dynamics with a finite set of closings surrounded by openings on both sides. The extent to which such a region remains protected from the actual boundaries is the outstanding question for the blank tape.

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

**Sharp window theorem.** For any r≥0, after at most r+1 sweeps, all closing distances at most 2r+1 are even, permanently. Successive even-site bits there evolve by multiplication by 1+X on their binary coefficient polynomial, truncating above the window.

In distance order, let x be the last particle of the first parity run, so every particle up to x has even distance. A cluster formed entirely from particles of one parity consists of consecutive occupied sites spaced by two. Its provisional endpoint is the last such site plus two; a gap of four or more starts a new cluster. In particular the last cluster of the initial even run reaches x+2. If the next odd particle lies at x+1, that cluster absorbs it and its endpoint moves at least two cells farther. Otherwise x+2 is an even output before the first possible odd output. The end of the initial even run therefore moves forward by **at least two distances on every sweep**, including when there are no odd particles. Starting from x≥0 proves the bound. In a cleared window, a consecutive run of even sites leaves just its first site and the next even site after its end, which gives the stated polynomial action. The two-particle seed with distances 0 and 2r+1 attains the time r+1: the last even particle advances by exactly two each sweep until it reaches 2r, and the odd cluster head stays at 2r+1 until the following sweep.

## Every finite bulk seed eventually follows Rule 90 everywhere

**Theorem.** For every nonempty finite seed, after finitely many boundary-free sweeps all particles have the parity of the leading particle in the moving frame. Subsequent evolution is exactly Rule 90 on the entire configuration. The empty seed is already fixed.

A parity run is a maximal consecutive portion of the ordered particle list with one color. A cluster outputs two particles having the color of its head. Thus the number of runs cannot increase, and if that number is unchanged in one sweep, every old run has contributed a cluster head. Otherwise the subsequence of heads would omit an entire run and could not have as many runs as before.

Suppose there are at least two runs and their number stays unchanged in a step. Let x denote the last particle of the penultimate run, y the first of the last run, and z the last particle of all. The final cluster head belongs to the last run. The particles from that head through z have one parity and spacing two within the cluster, so the new last particle is exactly z+2. The penultimate run contributed a head as well. Its final cluster reaches its own last particle x, giving provisional endpoint x+2 by the same spacing argument.

* If y≥x+3, this cluster ends at x+2 and y becomes a cluster head at the **same distance** in the output. Thus the new x is x+2 and the new y is y.
* Otherwise y=x+1, because the two runs have opposite parity. The cluster absorbs y and its new endpoint is at least x+4. Since the last run persists, this endpoint is the new last particle of the penultimate run.

Consequently z−x never increases while the run count is unchanged and it drops by at least two on every absorption of y. It is a nonnegative integer, so there can be only finitely many absorptions in an interval of constant run count. Such an interval cannot continue forever: after the final absorption, y would be stationary while x increased by two each sweep, forcing a new absorption. A run must disappear in finite time. Repeating with the strictly smaller number of runs proves the theorem. The particle at distance zero persists, which determines the surviving parity.

There is also an explicit global settling bound and a propagation-speed estimate. Let z be the largest distance, x the end of the initial even run and v the number of parity changes. At the start put b=(z+v−x)/2. This is a nonnegative integer: z has the parity of v and x is even. **The entire seed has one parity within b(b+1)/2 sweeps.**

To prove it, suppose the last cluster has q particles, starts at u, ends its input at z, and contains h parity changes. Any gap between consecutive particles of equal parity is at least two. A change of parity can shorten that gap by at most one. Thus z−u≥2(q−1)−h and the new largest distance z′=u+2q is at most z+2+h. The h changes after the head of this final cluster have no representatives in the output subsequence of cluster heads. Consequently v′≤v−h and **z′+v′≤z+v+2**. In physical coordinates this bounds the leftward reach of the finite seed after t sweeps by t+v₀−vₜ beyond its original leftmost particle. It also gives a uniform bound on the width between the initial even run's front and the last particle after subtracting their common drift.

The first even run advances by at least two, so b never increases. If its endpoint absorbs the first odd site, x′≥x+4 and b decreases by at least one. While any odd particle remains, its first distance y obeys y−x≤2b−1. Until absorption y stays fixed and x advances by two each sweep. Thus absorption takes at most b sweeps, including the absorbing one. Induction on b yields b+(b−1)+⋯+1 as claimed. In particular a seed of width w settles within w(w−1)/2 sweeps since b≤w−1. This argument gives a second proof of global convergence, including the cases of a single particle or an already uniform seed.

The proof gives a practical shortcut for an isolated finite seed: iterate clusters until a single parity remains, then apply arbitrary powers of Rule 90 by binary decomposition of the time. The finite-tape boundaries below determine where such an isolated calculation agrees with the physical machine.

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

Run `python3 parity_bulk.py` with assertions enabled. The script compares the independently derived cluster algorithm against finite padded TM data sweeps on all binary words of lengths 1 through 9, with independent elementary TM replay through length 4. It also checks the sharp window bound, the boundary example, and both possibilities for the last two runs during every transient from every seed of width at most 13 with occupied endpoints. [Observed output](parity-verification.txt)
