# A transitive return on the blank orbit of #397

After 64 completed sweeps from blank, the entire suffix beyond the protected periodic prefix consists of these 29 bits, read from the head-facing end.

```
11100010001000111011111111001
```

These 29 bits first return to this word at the same input phase after 1,024 more sweeps. During the return, exactly 33 carries leave the word. In chronological order they spell

```
bcbcbebcbcbcecbcbcbcffdfffffaffbc
```

Here `abcdef` are `ca, cb, cc, cd, ce, cf` in the order used in the [sweep reduction](check_bb33.py). Call this word of carries S. The bits inside the 29-bit prefix evolve independently of the cells beyond it, so the outgoing stream is S repeated indefinitely, up to a halt. After pass 64 the remaining suffix starts empty. Thus deciding #397 from blank is equivalent to deciding the dynamic empty-edge problem for this specific periodic stream. The [checker](transitive_section_397.py) obtains the checkpoint, first return and outgoing word directly from the sweep table.

## One cycle on every fixed tail length

On a *fixed* prefix of k occupied bits, each individual carry acts by a permutation. On the first bit it either swaps 0 and 1 or leaves them alone. On the remaining bits it again acts by a carry or by the identity. Together these permutations give an automorphism of the infinite rooted binary tree. In this calculation one discards events leaving the fixed prefix. The real machine still uses its original rules at the empty edge.

For any such permutation g, let its activity at depth j be the parity of the number of nodes of length j at which g swaps the two children. This parity adds under composition, since each factor permutes the nodes being counted. If g is one cycle on level j, its action on the next level is one cycle exactly when its activity at depth j is odd. Indeed, one tour of all the length-j prefixes accumulates the swaps at all those prefixes. An odd total exchanges the two extensions of the initial prefix, doubling the period. Starting at the root gives an all-depth transitivity test.

| Depth | a | b | c | d | e | f | Parity for S |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 | 0 | 0 | 0 | 1 |
| Positive odd | 0 | 0 | 1 | 0 | 1 | 1 | 1 |
| Positive even | 1 | 0 | 0 | 0 | 0 | 0 | 1 |

Starting from the root row, add the activities of the outgoing carries for input bits 0 and 1, modulo two. An early stop contributes zero. This produces the second row, then the third, then the second again. The multiplicities of the six carries in S are (1,10,10,1,2,9). Their scalar product with each row is odd. Consequently **S permutes all the length-k binary words in a single cycle of length 2ᵏ for every k**.

## Consequences for the moving edge

Once k bits beyond the 29-bit word exist, sampling them every 1,024 sweeps at the return phase visits every k-bit word once per 2ᵏ samples, for as long as the run continues. Hence a nonhalting blank trajectory cannot exclude any fixed finite pattern at this particular location.

In fact **both halting carries reach every fixed cut** on an infinite blank run. This statement concerns a cut between occupied cells; danger occurs only when the cut is the current edge. In a whole cycle of 2ᵏ tail returns, each particular occurrence of a carry in S sees every possible k-bit word exactly once. Earlier carries in the same copy of S permute these words, preserving complete coverage. Write the multiplicities of carries leaving this cut in alphabetical order. They are exactly

| Occupied tail bits k | Outgoing counts in 2ᵏ returns |
|---|---|
| k = 2m + 1, m ≥ 0 | 3ᵐ × (21, 1, 1, 21, 1, 1) |
| k = 2m + 2, m ≥ 0 | 3ᵐ × (3, 21, 21, 3, 21, 21) |

To verify the formulas, start with the multiplicities in S. Count both one-bit successors of each occurrence, dropping each early stop. This takes any row (a,b,c,d,e,f) to (c+e+f, a, a, c+e+f, d, d). Applying the recurrence twice to either displayed base row triples the row. The distinction between a fixed cut and the moving edge is therefore essential even for the exact blank orbit.

Moreover, if exactly k such bits exist at a return and the machine survives the following 1,024 × 2ᵏ sweeps, **the suffix must grow during that interval**. Otherwise no carry could have reached the empty edge, since every edge event either grows the word or halts. A hypothetical extra occupied bit would then receive no event and stay fixed throughout the interval. But S raised to the power 2ᵏ fixes the preceding k bits and flips that next bit, by its level-(k+1) transitivity. This is a contradiction.

In particular, at pass 64 + 1,024(2ᵏ − 1) a surviving run has at least 29 + k suffix bits. The claim starts at k = 0. Each successive deadline adds 1,024 × 2ᵏ sweeps and is at the return phase, so the growth result proves the induction. An infinite blank trajectory must therefore make infinitely many extensions. To decide the machine one must still establish which carry reaches each *new* edge first. Transitivity alone supplies no order comparison between the growing and halting events.

Run `python3 transitive_section_397.py` from this directory. In addition to the finite certificate for the parity proof, it directly checks complete cycles through ten tail bits.
