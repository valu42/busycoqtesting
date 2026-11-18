# Line 26 at successive dangerous-carry records

The blank run of `1RB2RB4LA2RA1LA_2LA4RA3LA---3RA` reaches width **205** at tick **1,145,205,194,028**. Every potential halting width through 205 is excluded. The decision for all widths remains open. The following exact recurrence gives one integer to bound per new record. [Physical reduction](column-frontier.md) · [Earlier checkpoint and clock](column-time.md)

## The record-gap criterion

Use full zero-based physical pair indices. At cut 3 the ordinary blank calendar supplies nine safe tokens P followed by one dangerous token Q each tick. Continue the ordinary rules on an infinite initially zero tail. A wrap of P allocates one physical pair. The physical and ordinary runs agree until Q would enter an unallocated pair. Call a Q stop at index j a record if it is deeper than every earlier Q stop. No physical failure can first occur at a repeated or shallower stop since allocation is monotone.

After a record, let W be cumulative allocation and C=W−j. Pair j now has bits (u,e)=(0,1). Higher pairs have (0,0): before their first Q the safe transfers through a virgin suffix come in twos, except for a possible single toggle immediately below the new stopping site. Equivalently, the seed and the following induction establish this shape at every record. At tick 1 the first Q stops at j=4 with W=5, so C=1.

Let b be the number of P arriving at j strictly after its record Q and before the next Q arriving there, including safe tokens earlier in that next Q's tick. All such next arrivals exist by [finite-cut periodicity](column-phases.md). At pair j the b safe tokens toggle u and emit c=ceil(b/2) safe tokens into the virgin suffix. Its first, third and subsequent odd-numbered safe inputs wrap, giving ceil(c/2)=ceil(b/4) new allocations. The next Q at j passes because e=1. If c is even it stops at j+1. If c is odd it passes that site and stops at j+2. Earlier Qs cannot create a new record. After this Q the stopping site again has (0,1) and all higher sites have (0,0). The following digits are left below it, with digit=2u+e and low index first.

| Gap b | New digits from j | Increase in j | Increase in W | Change in C |
|---|---|---:|---:|---:|
| 4a | 0 | 1 | a | a−1 |
| 4a+1 | 3, 2 | 2 | a+1 | a−1 |
| 4a+2 | 0, 2 | 2 | a+1 | a−1 |
| 4a+3 | 3 | 1 | a+1 | a |

Thus **ΔC=floor((b+1)/4)−1**. Only b=0,1,2 cost a unit. Gaps 3 through 6 break even. Larger gaps buy at least one unit. A gap cannot cost more than one. From the seed C=1, blank nonhalting is equivalent to every prefix sum of these changes being nonnegative. The first negative prefix reaches C=0 exactly and the physical Q reaches the undefined B3. This criterion uses the actual chronological gaps at successively changing cuts.

### A sufficient prefix average

Let Bₙ be the sum of the first n actual record gaps and Rₙ the sum of their residues (b+1) mod 4. Summing the exact changes gives **4(Cₙ−1)=Bₙ−3n−Rₙ**. Since Rₙ≤3n, an all-depth proof that **Bₙ≥6n for every n** would settle blank nonhalting. This allows short losing windows and uses one fixed numerical threshold. The least observed prefix average Bₙ/n is **7.5**, attained at n=2. At n=61 the sum is 715, the residue sum is 104 and the margin is 108. A dip below an average of six would require returning to the residue-sensitive test.

## The relevant phase is fixed at every depth

In the ordinary calendar at full cut j, write gⱼ for the number of P before its **first** Q, and bⱼ for the number of P between its **first and second** Q. Read across the periodic boundary where necessary. Both are defined even if the physical machine were eventually to halt.

**A cut j≥3 is a record stop exactly when gⱼ is even. At every such cut the gap in the margin recurrence is exactly bⱼ.** Before the first Q reaches j, its e bit is zero and its u bit has toggled gⱼ times. An even gⱼ stops the first Q there. An odd gⱼ passes it, so a later stop at j can never set a record. This pins the relevant phase to gap index 1 at every record, including records beyond the computed trace.

There is a second, depth-by-depth version of the target. Start with g₃=9. When gⱼ is odd the first Q passes, and the initially zero pair has sent gⱼ+1 safe tokens. When gⱼ is even the first Q stops after emitting gⱼ safe tokens from the initial safe run. The next bⱼ inputs emit ceil(bⱼ/2) more, then the second Q passes. Hence

* for odd gⱼ, gⱼ₊₁=gⱼ+1;
* for even gⱼ, gⱼ₊₁=gⱼ+ceil(bⱼ/2).

The virgin tail allocates on alternating safe inputs, starting with the first, so p(j)=ceil(gⱼ/2). Consequently nonhalting is equivalent to **gⱼ−2j≥1 for every j≥3** (the seed covers the lower cuts). This formulation requires just the first two gaps at each cut and has no unknown phase variable. It also gives a direct check of the trace: its row beginning at depth 94 gives g₉₄=400 (the stop is a record and p(94)=200), b₉₄=14, g₉₅=407, and g₉₆=408.

## A candidate induction and a phase counterexample

The 61 observed transitions give the following smallest net changes over all contiguous windows of each length.

| Records in a window | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| Minimum net change in C | −1 | −2 | −2 | −1 | −1 | +1 |

The five gaps 1, 0, 14, 4, 0 from depth 33 to 40 lose one unit. All 56 six-transition windows gain at least one. A sufficient open statement is that **every successive disjoint six-transition block starting at the verified depth 96 has nonnegative net change**. At that record C=108, and the first five transitions in a block can consume at most five. Negative six-blocks would disprove this particular induction without necessarily threatening nonhalting.

One can test a single six-block using at most 2,047 chronological Q-gaps at its starting cut. On the suffix beginning at the current record, the packed e integer starts at 1. Safe input preserves e. A Q sets a zero bit while clearing only some lower bits, increasing e by at least 1. Before the sixth new record its support can reach at most relative index 10, since each of the first five records advances at most two. Thus e is at most 2¹¹−1 until that sixth record. This bounds the input horizon at one anchored phase. It does not bound the number of record phases that need controlling.

A full cyclic period at any cut from 3 up has mean gap 9, so averaging floor((b+1)/4)−1 over its Q phases gives at least 3/4. Successive records sample selected phases at different cuts. For a concrete test, take the 27-gap calendar at cut 6. Place the normalized post-record suffix there and feed six records. Starting at the true phase (zero-based next gap 1), the margin gains 13. Starting at gap 14 of the same period, it loses 4. Any proof from a uniform six-record bound therefore needs a restriction on the reachable starting phases, or an accounting argument allowing losses across blocks. [Executable phase comparison](check_column_records.py)

## Exact physical continuation

| Tick of new record | Previous j | Safe gap b | New j | Allocated W |
|---:|---:|---:|---:|---:|
| 71,469,766,019 | 85 | 18 | 87 | 178 |
| 91,643,793,603 | 87 | 4 | 88 | 179 |
| 256,066,031,332 | 88 | 14 | 90 | 183 |
| 417,330,388,585 | 90 | 13 | 92 | 187 |
| 442,757,596,900 | 92 | 0 | 93 | 187 |
| 602,246,348,619 | 93 | 51 | 94 | 200 |
| 973,376,362,892 | 94 | 14 | 96 | 204 |

At the last record tick the exact clock is 181,912,616,417,007,775,091,148,375 instructions. A scans the blank at −7,787,010,903,137. The pair counters are u=`0xa9b77faebadafeeee7f315f0` and e=`0x121350c228008e80e01a31540`. The terminal 3 is at coordinate 409. The [tape convention](column-time.md) and these counters specify every cell. The physical weighted visit sum is 112,911,659,423,772. [Full trace](column-records.txt) · [Checksummed checkpoint](frontiers/runs/line26-record96.json)

**The next 107 new deepest stops are guaranteed safe**, regardless of their gaps. Their existence in the ordinary calendar follows from finite-cut periodicity, and the current margin is 204−96=108. After any prefix of at most 107 more records the margin is still at least one. Intermediate stops are shallower. Failure on the 108th new record would require every one of its 108 gaps to be 0, 1, or 2.

## Continuing past the last record

Every future record passes cut 74. Two calendars, restarted from the record-96 tape at cuts 17 and 18, give identical safe counts and root ticks for the next 215 dangerous arrivals at cut 74. The starting tick ends in a passing Q at each input cut, so no input gap straddles the restart. A separate replay applies those 215 messages to the actual upper pairs. The 108th arrival, at tick 1,052,754,703,428, has width 205. The 215th, at tick **1,145,205,194,028**, still has width 205, and its Q stops at pair 75. None of these Qs reaches pair 96. Exactly four P have reached pair 96 since its first Q. [Cut-74 messages](column-cut74.txt) · [Full physical endpoint](frontiers/runs/line26-width205.json)

The new exact raw clock is **251,807,027,794,701,522,123,671,715** defined elementary instructions. At this tick A scans the blank at **−9,161,641,552,225**, and the terminal 3 is at coordinate 411. The physical weighted visit sum is **132,843,802,436,645**. The machine-readable endpoint contains both complete tape counters and a checksum.

To exclude width 205 itself, let p(j) count allocated pairs at the first dangerous arrival to pair j in the ordinary model. We have p(95)=p(96)=204. The tape reaches width 205 before the first Q at cut 97, hence p(97)≥205. The [plateau bound](column-phases.md#the-first-dangerous-arrival-and-a-bound-on-its-plateaux) gives R₁₅=4 and Rⱼ₊₁≤Rⱼ+ceil(Rⱼ/2), hence R₉₇≤1,162,530,373,997,618 and 3R₉₇<2⁵². Therefore p(149)>p(97)≥205 and p(205)>205 by monotonicity. A halt at width 205 would require p(205)=205. Monotone physical allocation excludes every smaller eventual halting width as well.

## A lower bound beyond the fully timed tape

At the timed endpoint the next record gap b₉₆ has already accumulated four P. Its final value is therefore at least four, and the first future record has nonnegative margin change. At that new record the margin is at least 108. Each later record can cost at most one, so **the next 108 record stops after the latest checkpoint are guaranteed safe**. The finite calendars guarantee those records exist in the ordinary model.

Counting only the next 108 Q at cut 60 gives the last at tick **1,146,515,029,924**. Every new record must pass cut 60, so all ticks through that one succeed. The initial tick ended with a Q at pair 75 and therefore aligns with both low calendars used to count these arrivals. For this many successful ticks T the [explicit raw lower bound](column-time.md#bounds-that-hold-beyond-the-computed-checkpoint) exceeds 192T², since the positive linear term exceeds the low-pair correction. The resulting unconditional lower bound is **252,383,369,057,593,078,165,588,992 defined instructions**. The exact physical tape and clock are given at the earlier tick above.

## Reproduction

From this directory run

```sh
c++ -O3 -std=c++17 column_records.cpp -o /tmp/line26-records
c++ -O3 -std=c++17 column_raw_time.cpp -o /tmp/line26-clock
python3 check_column_records.py --records /tmp/line26-records --clock /tmp/line26-clock --extended
python3 frontiers/scoreboard.py --check
```

The fast check (omit `--extended`) independently runs the packed-counter equations through the first 200,000 ticks, compares short physical trips with literal transitions, and checks the trace, phase example, and checkpoint arithmetic. Extended mode regenerates the deep records, the continuation messages, and both fully timed tapes using two calendar cuts. The record enumerator and weighted clock share the low calendar and use different upper transfer implementations. These are finite computational checks. No kernel-checked blank decision is claimed.
