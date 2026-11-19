# BB(6) line 33 · ID 9146 · blank-tape outcome open

`1RB0LF_1LC0RB_0LD1LA_0RA1LE_0LA0RA_1LA---`, started in A with a two-way blank tape. This is permanent line 33, fresh rank 332 in the linked revision. [Pinned rankings](https://github.com/valu42/busycoqtesting/blob/175f2c272c1d5dfd1ff16f277839f19877cb2364/research/bb6/RANKINGS.md) · [Original list](https://wiki.bbchallenge.org/w/images/5/5e/BB6_holdouts_608.txt)

Fractal Geometry Explorer proved in Lean that the blank run reaches a particular tape at step 1,842,640,229. Their simulation also reported a different tape shape at 4,516,954,072. The derivation below covers the transition between them for an infinite family of counter values, identifies the following return, and gives a sufficient condition for halting. A direct interpreter checked the complete tape through step 10,536,838,532. A separate accelerated calculation made more than $10^{2387}$ defined transitions from blank. The question of eventual halting remains open. [Earlier proof and reported checkpoint](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0LF_1LC0RB_0LD1LA_0RA1LE_0LA0RA_1LA---/README.md) · [Prior Lean theorem](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0LF_1LC0RB_0LD1LA_0RA1LE_0LA0RA_1LA---/lean/Round.lean#L178)

## A sufficient condition for halting

In each displayed word the head starts in A on the first bit and everything to its left is blank. Put $P=10$, $Q=110$, $T=1110$, and $U=11110$. Juxtaposition concatenates bits. Let $S$ be an arbitrary right-hand tape, and define

$$W(a,b,m,c;S)=P^a Q P^b T P^m Q P^c\,0P S.$$

**If $a,m\ge1$, $b\ge0$, and $c\ge2b+5$, then the machine starting at $W(a,b,m,c;S)$ reaches F reading 1, for every suffix $S$.** F1 is the sole undefined instruction.

| Starting conditions | Reached configuration | Defined transitions |
|---|---|---:|
| $a,m,b\ge1$, $c\ge2$ | $W(a+3,b-1,m+1,c-2;QS)$ | $14a+8b+14m+8c+79$ |
| $a,m\ge1$, $b=0$, $c\ge2$ | $P^{a+3}U P^{m+1}Q P^{c-2}\,0P QS$ | $14a+14m+8c+79$ |
| Start at $P^a U P^m Q P^c\,0P S$, with $a,m\ge1$, $c\ge3$ | F1 | $6a+28m+16c+90$ |

Apply the first row $b$ times. After $i$ sweeps the two decreasing gaps have lengths $b-i$ and $c-2i$. At $i=b$ at least five pairs remain in the right gap. The second row creates the four adjacent ones of $U$ and leaves at least three pairs. The third row reaches F1. The checker treats $S$ as an inaccessible tape boundary throughout these three local derivations. [Symbolic rules and their clocks](line033_tail.py)

## How the blank run passes this test

Write $D(m)=1P^m1P^9\,0101101$ followed by blank tape. Use the published round notation $RS(N,D(m))=P^4 QP^N\,10010\,D(m)$, and define $X(B,M)=W(4,B,M,6;Q^2P0^\infty)$.

For all natural $j,m$, the following transition takes exactly $116j^2+534j+14m+689$ defined steps.

$$RS(4j+3,D(m))\longrightarrow X(6j+8,3j+m+6).$$

The published first sweep and $2j$ counting sweeps leave $P^{6j+7}QP\,10010\,(QQ)^j QD(m)$. Their respective costs are $32j+133$ and $350j+58\binom{2j}{2}$. The checker derives the conversion from this word to $X$ in $210j+14m+556$ steps. This accounts for the entire run between the two endpoints. [Published counting lemmas](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0LF_1LC0RB_0LD1LA_0RA1LE_0LA0RA_1LA---/lean/Round.lean#L109)

Starting from this $X$, three sweeps reduce its right gap from six to zero. Two auxiliary rules handle the exit. For $a,b,m\ge1$, the right-gap exit sends $W(a,b,m,0;S)$ to $P^{a+3}QP^{b-1}\,0P QP^{m-1}TQS$. For $a,d\ge1$ and $b\ge2$, a sweep sends $P^a QP^b\,0PQ^d S$ to $P^{a+3}QP^{b-2}\,0PQ^{d+1}S$. Applying the exit once and the second rule $3j+2$ times gives

$$P^{9j+22} Q\,0P\,Q^{3j+3} P^{3j+m+8} T Q^6 P0^\infty.$$

The next return depends on the parity of $j$. In the odd case it re-enters the family in the halting test.

| Parameter | Reached right tape |
|---|---|
| $j=2v+1$ | $W(4,18v+29,9v+10,6v+m+10;P^{12}0^\infty)$ |
| $j=2v$ | $P^4 QP^{18v+20}\,0P^{9v+7} QP^{6v+m+7}\,0P^{13}0^\infty$ |

It follows that $RS(8v+7,D(m))$ **halts whenever $m\ge30v+53$**. For example, a literal replay from $RS(7,D(53))$ reaches F1 after 55,945 defined transitions. That input starts on the specified nonblank tape.

There is a uniform reason that one source of actual blank-run configurations avoids this halting condition. Start at the published short-tail round with $N=32z+17$. The published branches A and D give $RS(72z+47,D(60z+38))$. In the odd row above this means $v=9z+5$. Its left and right gaps are $162z+119$ and $114z+78$. After $57z+39$ sweeps, the right gap is empty while the left still has $105z+80$ pairs. This holds for every natural $z$. The observed blank trajectory takes this route at $z=266$, starting with $N=8529$. [Published branches and blank entry](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0LF_1LC0RB_0LD1LA_0RA1LE_0LA0RA_1LA---/lean/Round.lean#L126)

| Defined steps from blank | Head coordinate | Entire right tape, blank after the displayed word |
|---:|---:|---|
| 1,817 | −53 | Published short-tail round, $N=13$ |
| 1,842,640,229 | −70,403 | $RS(19199,D(15998))$ |
| 4,516,954,072 | −118,412 | $X(28802,30401)$ |
| 10,536,838,532 | −190,436 | $W(4,43211,21601,30402;P^{12}0^\infty)$ |

State A scans the first bit at each checkpoint. The separate C++ interpreter executed every transition from coordinate zero and compared all tape cells in its buffer at each checkpoint. It checks the head bounds on every move, so all cells outside the buffer are known blank. In the last row it would take a right gap of at least 86,427 for the sufficient halting condition to apply. The actual gap of 30,402 runs out after 15,201 sweeps, with 28,010 pairs still in the left gap. The exact clock then reads 27,784,698,785. [Direct interpreter](line033_literal.cpp)

## Replay and scope of verification

Run these commands from this directory. The Python checker uses the two symbolic-machine modules from the pinned Fractal Geometry Explorer checkout. Its local rules are checked in Python. The Lean kernel result cited above belongs to the earlier work.

```sh
git clone https://github.com/fractal-geometry-explorer/busy-beaver-explorer.git explorer-9146
git -C explorer-9146 checkout --detach c409c4b292369cb404e939753004bd1216fa3333
PYTHONPATH=explorer-9146/tools/py python3 line033_tail.py --cross-check
c++ -O3 -std=c++17 line033_literal.cpp -o line033-literal
./line033-literal
```

A symbolic power denotes any nonnegative number of copies. Each accelerated crossing checks a literal run on one copy of a finite word and its carried boundary bits. The run exits the block on the opposite side in the same state with the carry restored. Concatenating copies proves the crossing for every multiplicity, including zero. Literal moves handle the boundaries. The first part of the checker verifies eight such derivations against their complete expected output words, suffixes and step counts. [Underlying crossing algorithm](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/tools/py/bbtools/symtm.py)

For the blank replay, a token $k$ means $1^k0$. The checker records repeated tokens and derives a sweep with independent natural variables for the long runs. A batch repeats that sweep only when the symbolic output has the same token sequence, every variable is translated by a constant preserving its residue, and the required lengths stay nonnegative for every application. The elapsed clock is the sum of the resulting arithmetic progression. The literal seed at step 1,817 is regenerated from blank.

The first grouping used 60,000 batches. A second grouping with different length cutoffs used 104,574 batches to reach the same number of edge returns. Both produced the same exact 7,930-bit clock and the same full tape. They share the symbolic crossing code. The C++ replay provides an independent check through the four checkpoints above.

| SHA-256 input, ASCII without a trailing newline | Digest |
|---|---|
| Exact clock in lowercase hexadecimal | `e1c2b2300a277fb618949a0c75a10f158b88afae1f0ee1661e36dc22628942c0` |
| Full token sequence as comma-separated `token:hex-length` pairs | `87ddf3368c1a3d023f0ae0351c175e1eaedfd04711a8018e0ab00f7ad840dbf9` |

The unresolved step is to cover **every** later return from the blank orbit with safe rules, or to exhibit a reachable halt. A second literal control shows why the current gap comparison alone cannot supply that induction. Start instead at $W(4,32,1,4;P^{12}0^\infty)$. The right gap empties after two sweeps with thirty pairs still in the left gap, yet this input reaches F1 after 45,292 defined transitions. The comparison proved above applies to one family of returns. Other tail shapes arise. An infinite-progress proof would also have to show that its rules always supply another positive number of defined transitions.

## Prior-art check on November 18, 2026 UTC

- The live register listed line 33 as `OPEN`. Before this claim, the fork's claim board, branch names and pull requests showed no decision for ID 9146. The fork itself directs investigators to the earlier partial result. [Register](https://github.com/valu42/busycoqtesting/blob/06c3c4ffba3c8010913b1829bf7376296d5816dd/research/bb6/MACHINES.csv#L34) · [Fork proof queue](https://github.com/valu42/busycoqtesting/blob/06c3c4ffba3c8010913b1829bf7376296d5816dd/research/bb6/PROOF-QUEUE.md)
- I checked titles, descriptions and changed filenames for upstream BusyCoq PRs 1 through 102. Among the 260 distinct six-state tables printed in those fields, none matched under any of the 720 state permutations, with either tape orientation. I also checked the complete table strings in both BB(6) catalogues in DeepMind's Cryptids repository, and searched GitHub code, issues, commits and the public web using the table, its `HHH` spelling or its ID. Filename and text comparisons cannot identify arbitrary proofs encoded under unrelated descriptions. [BusyCoq PRs](https://github.com/ccz181078/busycoq/pulls?q=is%3Apr) · [Cryptids catalogue](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/README.md) · [Acceleration catalogue](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB6/Accelerations/README.md)
- The published annotated spreadsheet snapshot leaves the outcome blank and classifies the machine as “Chaotic Fractal Type 1.” An independent holdout list includes the exact table as open. Fractal Geometry Explorer's machine-specific status page explicitly identifies the missing blank-tape decision. [Annotated row](https://github.com/Dojo-1/cryptid-verifier/blob/341f04a8bf6bfb39a8f74ad9ba9463e0a7073530/analysis/appendix-c-leads/bb6-annotated.csv#L624) · [Independent open list](https://github.com/JacobRSchwartz-AI/bb6-holdouts/blob/63900f2af164bd2a91d24257f506f70fceed1640/data/open.txt) · [Machine-specific status](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0LF_1LC0RB_0LD1LA_0RA1LE_0LA0RA_1LA---/status.json)
- Line 39 is the one other row in the 608-machine register with an isomorphic table. The reflection and state map send line 33's start to **D** on line 39's table. Line 39 starts in **A**. The register lists both as open. [State map and comparison](https://github.com/fractal-geometry-explorer/busy-beaver-explorer/blob/c409c4b292369cb404e939753004bd1216fa3333/holdouts/1RB0LF_1LC0RB_0LD1LA_0RA1LE_0LA0RA_1LA---/README.md#related-machines)

I found no public blank-tape decision for this machine. The search cannot establish priority over private or unindexed work.
