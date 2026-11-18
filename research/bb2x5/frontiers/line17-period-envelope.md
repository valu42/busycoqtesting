# A deadline for line 17's next overflow

The deadline concerns the first visit to +12 from blank. The return can still reset or halt. The argument uses the [exact pulse table](../frontier-background.md), the [integer mark recurrence](../marked-register.md) and the [cut-403 rank and elementary-clock bound](../line17-edge-time.md). The calculation is in [line17_period_bound.py](line17_period_bound.py).

## The period seen from slot one

The cut-53 distinguished input is purely periodic from its first slot. Each subsequent pair through digit 402 starts with trit 1 and no pending pulse. Let its input have period length P and M marked slots. For a marked input at slot t and coefficient c, its starting trit is r=(t+c) mod 3. It emits one child mark when r is positive and updates c by 4(1+r). At consecutive marks a gap g updates the residue by r ↦ 1+g−r mod 3. All these maps are permutations. The composition over one period permutes the three residues, and the orbit of the distinguished first mark has length h in {1,2,3}. Each mark in a given position sees h distinct residues in those h copies.

Let D be the sum of 1+r over their hM marks. The mark recurrence gives a child period of length P′=(hP+4D)/3, containing exactly the surviving marks. In the first group every child time (t+c+5r)/3 is positive and at most P′, since the gain from its own burst alone is 4(1+r)≥5r. In the next group the parent time advances by hP, the coefficient advances by 4D, and the residues repeat. Its child marks are therefore exactly the first group's marks shifted by P′. This proves pure periodicity from slot one by induction. All these cuts contain marks because their first 26 bits contain marks at 5, 11, 17 and 23. Every period of length at least 23 therefore contains at least four marks.

At the chosen base cut the checker runs the actual finite prefix through H and 2H source sweeps. Equality of **all** prefix digit states at those boundaries makes the emitted P slots between them an eventual period. The purity proof above makes P a period of the whole ray, irrespective of whether its eventual period starts at a canonical boundary. Explicitly, shift any index forward by a large multiple of the known pure period to get beyond the transient, where adding P preserves its letter. The same shift returns that identity to the original index. The number of marks per P slots is invariant under rotating P slots of a periodic ray. The local pulse table gives one output mark exactly when half the interior instruction count minus the number of output slots is one. All three quantities add over pulses. Thus the difference of the two native run totals gives the period's mark count exactly.

## Length and marks over the homogeneous band

After i lifts let K base periods give one current period of length P, with M marks. Define A=3ⁱP/K. If h=3, each mark sees residues 0,1,2, so the next period has 2M marks and D=6M. If h=2 each mark sees distinct residues, so at least M survive and D≥3M. If h=1 at least one mark survives and D≥M+M′, because each survivor consumes at least two compounds. In the third case the checker can use four survivors when its length bound already forces P′≥23. In each case A increases by 4·3ⁱD/(hK), and the next period multiplier is hK.

A finite boundary can interrupt a burst. From the slot identity, starting at trit 1, the number of outputs for n inputs is floor((n+1+4C)/3), where C counts **consumed** compound pulses. On exactly khP parent slots this count is at most kP′, since C≤kD. On khP+2 parent slots all bursts started in those khP slots have completed, so the count is at least kP′. The additional two slots suffice even for a final burst of length three. All periods here are at least two slots because the pure word contains both a marked and an unmarked slot.

Two consequences are used. If the observed base prefix has length N, the corresponding observed descendant lies in the first ceil(N/(KP₀)) periods at depth i, where P₀ is the base period length. This follows by composing the upper finite-boundary inequality. Both its observed slots and its observed marks bound from below the length and mark count of each period after dividing by that number of periods and rounding up. In the other direction, (kh+1) parent periods ensure k whole child periods by the lower finite-boundary inequality. Iterating, at most K·ceil(R/P)+iK base periods suffice to realize rank R at depth i. Equivalently a conservative count is ceil(R·3ⁱ/A)+(i+1)K base periods. This includes unfinished bursts at every cut.

The checker enumerates the three possible lifts by dynamic programming. Write a for the number of single-period lifts and b for the number of double-period lifts. Then K=2ᵇ3ⁱ⁻ᵃ⁻ᵇ. For equal (a,b,lower mark count) it retains the smaller lower bound on A. All updates round down when bounding A. Once a state attains the selected cap its descendants retain at least the cap because A is nondecreasing. The calculation accounts for that group separately using K≤3ⁱ. It minimizes the certified input deadline over the intermediate cuts, using the established inverse R ↦ 3R−49 from there to cut 403. The remaining cut-403 target is 81,526,541. Finite prefix counts constrain the possible periods.

Finally the verified H-to-2H cycle converts the guaranteed base rank into a sweep deadline. The inherited raw instruction inequality includes the cost of reaching +12 inside its triggering sweep. The virtual execution agrees with physical instructions through that first arrival.

## Replay

From `research/bb2x5`, build the existing packed transfer and run the checker.

```sh
c++ -O3 -std=c++17 frontiers/line17_packed.cpp -lgmpxx -lgmp -o /tmp/line17-packed
python3 frontiers/line17_period_bound.py --packed /tmp/line17-packed
```

At cut 95 the base period is 1,175,942,592 slots with 146,990,340 marks. The resulting first-visit deadline is below 1.614 × 10¹⁶⁸ sweeps and 3.644 × 10³³⁷ elementary instructions. The [replay output](runs/line17-period-bound.json) records the exact integers.

The cut-99 replay sets `--cut 99 --period-epochs 1376809511370776442839236608 --finite-slots 200000000000`. It independently returns the actual cut-99 period of 4,181,088,728 slots and 522,648,729 marks. The [cut-99 result](runs/line17-period-bound-99.json) places the visit below 2.558 × 10¹⁶⁷ sweeps and 9.155 × 10³³⁵ elementary instructions.

### Using the tiled transfer trace

The optional `--trace` path uses the cut-95 replay as its anchor. That replay also verifies that exactly one base period has arrived after H sweeps. Every subsequent block of H sweeps produces exactly another base period, starting in the distinguished phase. The native decomposition at an arbitrary horizon may count some of those slots in its trailing partial word. The two directly checked aligned totals establish the sweep boundaries independently of where that decomposition splits its suffix. The tiled worker records each cut's prefix size, period size, copy count, suffix size and period mark count. For later lifts the checker requires zero prefix and at least one recorded period. A complete input period of at least three slots emits at least one slot. Consequently the empty output prefix forces the worker's cycle to begin at the initial digit state. If h copies of the previous period return to that state, exactly those h input periods emit one full child period from the distinguished start. This gives the next root period by multiplication by h.

The worker has at most six digit states. Its two copy counts k and k′ satisfy k′=floor(k/h). Over the cycle the number of compounds equals (3P′−hP)/4. Every parent mark contributes one compound plus its starting residue. A surviving mark has residue one or two. Thus the compound total lies between hM+M′ and hM+2M′. The checker requires that these exact tests determine h uniquely. It also verifies that the displayed period and suffix account for the observed number of slots. It then applies the same period-envelope calculation to the actual finite prefix in the counts file.

The recorded 10³⁰-sweep run uses [periods](runs/line17-1e30-periods.txt) and [digit counts](runs/line17-1e30-counts.txt) from the same blank-tape transfer. Replay its deadline with the command below.

```sh
python3 frontiers/line17_period_bound.py --cut 107 \
  --anchor frontiers/runs/line17-period-bound.json \
  --trace frontiers/runs/line17-1e30-periods.txt \
  --counts frontiers/runs/line17-1e30-counts.txt
```
