# The actual fifth mark at cut 403

The first five marks at cut 403 occur on slots **5, 11, 17, 23 and 29**. Slot numbering starts at one. The sixth can occur no earlier than slot 33. At the `10^30`-sweep checkpoint, the physical machine had still sent zero slots to this cut. The checkpoint already fixes the five positions. The established minimum of 65 cut-403 slots before the first visit to +12 places all five within the ordinary physical execution. [Checkpoint](runs/line17-1e30.json) · [Literal suffix check](line17_slot_floor.py)

## Reading the checkpoint

At an ordinary sweep boundary record each digit's trit and its incoming pending flag, stored in the pair immediately to its left. Give the root only unmarked slots after this boundary. Every digit receives infinitely many plain slots on this auxiliary input, since any three slots emit at least one child slot. All pending bursts therefore finish. Each digit sees only finitely many additional marks, since each received mark and any initial pending burst can emit at most one child mark. This calculation reads at most three unmarked slots beyond the last known mark at each digit.

For a fixed initial trit and pending state, deleting all marks after any selected mark leaves an initial segment of the child mark positions unchanged. From the integer recurrence, each child mark time depends only on the incoming marks up to its parent, including the parent's virtual burst completion. Later input marks are separated and cannot interrupt an active burst. The same argument applies to a pending burst at the checkpoint. Apply it at every cut. Every mark found by completing these pending bursts belongs to the beginning of the actual subsequent mark sequence on the ordinary source. The auxiliary input supplies no new root marks. The real root supplies its next mark on relative slot 2.

For a bound on the next additional mark, let `L` be the earliest possible additional parent and `c` the coefficient after all known bursts. Every subsequently surviving parent has slot `t ≥ L`, coefficient at least `c` and residue `r ≥ 1`. Its child time `(t+c_current+5r)/3` is at least `ceil((L+c+5)/3)`. Apply this at each digit with the mark-separation constraint. Spacing is at least four from cuts 53 through 403, as checked in the [suffix analysis](line17_slot_floor.py). The result is a certified initial segment even at a cut which the finite checkpoint itself has not yet reached.

The [checker](line17_drain.py) validates the saved checkpoint, evaluates each digit both by the mark-time recurrence and by individual pulse-table transitions, and compares the predicted future marks with direct continuation for 40 short sweep prefixes across seven digits. At the previous `6 × 10^28`-sweep checkpoint it recovers the four marks through slot 23 and excludes slots 24–26. At `10^30` it recovers the fifth mark and excludes slots 30–32. The calculation leaves open whether slot 33 is actually marked. [Output at `10^30`](runs/line17-drain-1e30.json)

## A separate three-case check

At cut 168 the finite `10^30`-sweep run has received 29 slots, of which five are marked. The preceding row reports 68 internal moves, and the local pulse table gives `68/2−29 = 5` output marks. The first four are the established positions through slot 23. The four-slot spacing leaves three possible positions for the fifth. The clear trit-1 digit produces the following counts in its 29 input slots. [Digit counts](runs/line17-1e30-counts.txt)

| Fifth parent slot | Final trit | Pending | Outputs | Probes | Internal moves |
|---:|---:|---:|---:|---:|---:|
| 27 | 1 | 0 | 27 | 60 | 62 |
| 28 | 2 | 0 | 28 | 62 | 66 |
| 29 | 1 | 1 | 27 | 59 | 62 |

The final row matches the saved digit. At a clear trit-1 digit, an initial list of marks at `5,11,…,6k−1` gives the same initial child marks. Each listed parent reaches trit 2, emits its mark on the second pulse of its three-pulse burst and returns to the same phase before the next listed parent. This also applies to the unfinished fifth burst at cut 168. Every digit from cut 168 up to 403 starts clear at trit 1 in the original register, so all five positions persist. [Register derivation](../frontier-background.md)
