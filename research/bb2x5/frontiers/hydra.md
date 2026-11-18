# Timed sweeps on lines 29 and 30

These are Daniel Yuan’s Bonus Cryptid and Hydra. Both already have much deeper community simulations. The published reductions describe a biased walk away from the halting condition. The two checkpoints here supply exact, reproducible clocks and complete physical configurations from blank. [Shawn Ligocki’s analysis](https://www.sligocki.com/2024/05/10/bb-2-5-is-hard.html) · [Bonus Cryptid trajectory](https://wiki.bbchallenge.org/wiki/Bonus_Cryptid)

| Line | Blank-tape raw steps (rounded) | Exact operations to replay | Current state |
|---|---:|---:|---|
| [29](runs/hydra-29.json) | 1.09706 × 10^1030 | 69,836 | B scanning a blank, with 1,225 threes to the right |
| [30](runs/hydra-30.json) | 2.85901 × 10^7045 | 329,461 | A scanning a blank, with 9,889 threes to the right |

## Sweep identity

Write a bar immediately before the scanned cell. Consider state A on a tape of the form `0^∞ 3^m |0 2 0^n W`. Let k = 3 on line 29 and k = 2 on line 30, and let g = k+1. When n ≥ k, the next 12+k instructions replace the local word `|0 2 0^k` by `3^k |3 2` in state A. None of those instructions scans either exterior cell. A then moves left over m+g threes. From that blank, the three-instruction rule `|0 3 → 3 |0` shifts the head right once for each of those threes. The result is `0^∞ 3^(m+g) |0 2 0^(n−k) W`. The head has moved k positions right. The raw cost is 12+k+4(m+g).

The accelerator takes q = ⌊n/k⌋ complete passes when it recognizes the finite run. Summing the costs over m, m+g, … yields q(12+k+4(m+g))+2gq(q−1). For the residue and all other tape shapes it uses the literal instruction, a contiguous same-state scan, or the three-instruction shift over a run of threes. This handles the exceptional line 29 returns on the physical tape. At operation 2,259 the replay reaches the community’s intermediate configuration A(1,287,547,464,911,049,659, 10) at exactly 1,894,603,970,741,566,467,769,886,232,237,213,051 defined instructions. [Reported intermediate configuration](https://wiki.bbchallenge.org/wiki/Bonus_Cryptid)

Line 30 reaches the same boundary as the separate 20,000-return normal-form replay. The physical run has state A on a blank, followed by `2 0^a 3^9889 2`, with an 11,703-bit zero-run length a. Both clocks, the two absolute positions (head and first 2), and every run length agree. The offline test reconstructs the normal-form record and checks its published digest. [Normal-form checkpoint at commit 680c696](https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/halting-outlook/hydra-results.json)

## Replay

From `research/bb2x5`, these commands reproduce both records, continue the first one, and run the checks.

```sh
python3 frontiers/hydra.py --line 29 --operations 69836 --checkpoint /tmp/hydra-29.json
python3 frontiers/hydra.py --line 30 --operations 329461 --checkpoint /tmp/hydra-30.json
python3 frontiers/hydra.py --line 29 --resume frontiers/runs/hydra-29.json \
  --operations 70000 --checkpoint /tmp/hydra-29-next.json
python3 frontiers/test_hydra.py
```

`steps_hex` is the raw clock. `head_hex` gives the absolute head position. Each tape stack stores pairs of a digit and its hexadecimal run length with the nearest run last. The right stack includes the scanned cell. Blank tape extends beyond both stacks. The tests replay the two finite local identities with unreadable boundary markers, compare the full configurations with the elementary interpreter, meet both earlier level-12 block checkpoints at their exact raw times, and reproduce the saved endpoints.
