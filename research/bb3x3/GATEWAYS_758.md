# Four halting intervals below H

**All 4,471,190,571,115 reset seeds from H − 11,177,976,427,786 through H − 6,706,785,856,672 halt.** This interval gives a sufficient condition for deciding the blank orbit. At its first crossing of mass above $2(H-6{,}706{,}785{,}856{,}672)+1$, a reset in the preceding **993,597,904,692** map updates suffices. Blank reachability remains open. The intervals below give four crossings at which to apply the test. The distance is $d=H-c$ at a reset $A(1,c)$. Both endpoints are included. [Definition of H and the counter rules](RANKINGS.md) · [Established halting interval](COVER_758.md)

| Far distance | Near distance | Consecutive halting reset seeds | Sufficient recent-reset bound in map calls |
|---:|---:|---:|---:|
| 15,333,300,998 | 9,199,980,604 | 6,133,320,395 | 1,362,960,087 |
| 137,999,708,986 | 82,799,825,392 | 55,199,883,595 | 12,266,640,798 |
| 1,241,997,380,866 | 745,198,428,520 | 496,798,952,347 | 110,399,767,188 |
| 11,177,976,427,786 | 6,706,785,856,672 | 4,471,190,571,115 | 993,597,904,692 |

## How the reset intervals reach a halt

In each row every even seed follows the word $I J^{291} L L J L L J L R$. Every odd seed follows $J^{292} L^8 J L^6 J^k L R$ with $k=264,262,260,258$ in row order. The checker replays the original counter rules at both endpoints of each parity. Along a common ordinary word, increasing the seed makes the first counter nonincreasing and the second nondecreasing. Each guard between the two endpoints therefore holds on the entire interval of that parity. This also certifies the absence of an earlier reset on these particular words. [Endpoint comparison](COVER_758.md)

Write $W=a+2c$. Each even seed returns with an increase of at most 615 in the reset parameter. On the odd word, the $293+k$ jumps contribute four each to $W$, the fifteen bulk moves contribute at most nine each, and the return contributes five. The increase in $c$ is at most $656+2k$. All returns advance $c$ strictly. Hence every seed in the row eventually crosses its near edge at a reset, no more than 5,000 seeds above that edge.

Each finite bridge starts by admitting every reset whose distance lies in $[f-5{,}000,f]$. It proves that each admitted trajectory halts or reaches a reset at a distance in $[n-5{,}000,n)$. The rows of the bridge calculation compose because the entire outgoing interval is admitted by the next segment. Four short segments connect the near edges in the table to this shared chain. Its final segment runs from distance 10,000,000,000 to 64,000,000, with possible exits at distances 63,999,567 and 63,999,631. Both belong to the previously verified halting interval. An earlier halt along the bridge also suffices.

The worker divides a segment into intervals. When the odd endpoints have the same jump batch and the same remaining word through an even nonbulk state, it bounds the increase in $W$ for every seed. A terminal branch can end the trajectory there. Every continuing reset increases $c$ and stays within the computed bound. The worker replaces the incoming possibilities by all possible exits within that bound. Where this test fails it subdivides, and below a width of 250,000 it traces the possible input states individually. Any intervening visit to $a=1$ before the selected later reset preserves this argument. The calculation requires a later halt or a bounded reset, and every continuing step increases $W$.

All odd seeds in a segment share $J^{292}L^8JL^6$. The reference worker checks this prefix at both endpoints, including the legality of the initial jumps. For efficient repeated traces it stores the first counter and the mass gain at the end of this prefix for each even distance residue modulo $2^{15}$. A translation of the input by $2^{15}$ preserves the residues through all fourteen bulk moves. Each bulk divides the varying coordinate by at most two. The resulting displacement of the first counter is affine and independent of the chosen residue, and the mass gain stays the same. The worker computes the displacement using arbitrary-precision integers and checks the signed bounds for every residue. [Reference implementation](gateway_758.cpp)

## What an infinite blank orbit would have to do

Consider a row whose reset interval is $[B,U]$ with width $w=U-B+1$. Every continuing step increases $W$ by between three and nine. An infinite blank orbit would cross $W>2U+1$. Its most recent reset strictly before that crossing would have parameter at most $B-1$, because every reset in $[B,U]$ halts. The required mass increase would be at least $2w+1$. Consequently a reset in the preceding $\lfloor 2w/9\rfloor$ calls rules out this infinite trajectory.

The same even word holds on all even resets from $\lceil998H/1000\rceil$ to $H$, again by checking endpoints. Thus the most recent reset could be even only if it lay below that entire corridor. Otherwise the next reset, at most 615 higher, would occur before the crossing. This gives a separate restriction on a proposed bypass using an even last reset.

## Reproduction and resumption

Use Python 3.10 or later, GMP with its C++ bindings, and a C++17 compiler on a 64-bit LP64 system. The default run checks the smallest row. `--scale 13` checks all four. The cache keeps successful segment receipts for the same worker executable, so repeating the command resumes interrupted work. Omit `--cache` to replay every segment afresh. Several jobs can run independently. [Gateway verifier and segment schedule](check_gateway_758.py)

```sh
c++ -O3 -std=c++17 gateway_758.cpp -lgmpxx -lgmp -o gateway_758
python3 check_gateway_758.py --scale 13 --jobs 4 --cache /tmp/bb33-gateway-receipts
```

## How much residue information survives the even corridor?

For the common even word, translation by 64 preserves the starting residue at each of its five bulk moves. It therefore translates the next reset by exactly 64. The single-return image consists of 15 odd residue classes modulo 64 in the interior of this corridor. Its projection contains every odd class modulo 4, 8 and 16.

After allowing one further return in other parts of the same even corridor, **every odd residue modulo $2^{380}$ occurs**. For $k=0,\ldots,31$, the verifier checks endpoints around $H-\lfloor H/(2300\cdot3^k)\rfloor$ on intervals of radius $2^{380}$. Even seeds take the common even word. Their odd outputs take the row's odd word with exponent $k$ within the enlarged endpoint interval. Across its fifteen bulk moves, knowing the starting residue modulo $2^{16}$ suffices for every mass increment. After the first fourteen bulk moves the odd first counter is 3 modulo 4, so the last bulk move's high-residue flag flips exactly when $k$ is odd. Increasing $k$ by two thus adds four to the return increment. Exhausting these small residue calculations gives all 32,768 odd classes modulo $2^{16}$ after one or two returns. Translating an input by a multiple of $2^{16}$ preserves both increments on the verified blocks. Each block is wider than $2^{380}$, which lifts the result to the stated modulus. These are possible inputs from across the corridor. Determining the residue of the actual blank orbit requires information about its history. [Residue verifier](check_corridor_residues_758.py)

```sh
python3 check_corridor_residues_758.py
```
