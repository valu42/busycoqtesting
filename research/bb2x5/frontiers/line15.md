# Line 15 and the first five calls to a fresh strip

At 35,000 periods the blank machine has executed **344,289,925,484 defined instructions** and returned to coordinate zero in B. Its negative half accounts for 68,600,525,016 instructions and the nonnegative half for 275,689,400,468. The [checkpoint](runs/line15-strips.json) stores every nonnegative cell through the last seven-cell strip. The period count determines the negative tape through the existing [left-half certificate](../mixed-and-sweeps.md#5-other-candidates-and-verification).

The [latest full checkpoint](runs/line15-next.json) reaches **20,331,546,024,060 steps** at 245,000 periods, beyond the community-reported 20-trillion-step lower bound. The negative half contributes 3,361,403,675,016 steps and the nonnegative half contributes 16,970,142,349,044. At the cut the head is at zero in B. The nonnegative tape begins with 5,142,098 consecutive digits in {1,2} and ends in `0111`. The run tracked the first five requests at each newly reached nonroot strip. The boundary contains 734,586 seven-cell strips, including the root and a final strip with four requests. [Community report](https://wiki.bbchallenge.org/wiki/BB%282%2C5%29#Unsolved)

## Seven-cell return model

Consider a seven-cell strip entered at its left end. Each time the head leaves to the right, record the entry letter sent to the next strip, suspend the call, and provisionally resume on the strip's rightmost cell in A. A completed call must return A at the left end. The worker accounts for every original instruction inside the strip, including those that issue or finish a call. It passes the outgoing letters, in order, to a fresh computation on the next strip. A finite batch is accepted only when the last strip issues zero calls. Induction back from there realizes all provisional A replies on the actual tape. A candidate B return or undefined instruction instead triggers chronological bisection to a single period, which the Python driver replays literally on the positive tape. A confirmed B4 or a B return across coordinate −1 saves its own physical event checkpoint.

On the negative side each genuine A return elicits the next letter of `BBBA` followed by repetitions of `BABAABBABBABAAAB`. The initial positive entry is A. For a positive group count g a saved boundary includes 4+16g completed negative returns. It excludes the next positive excursion.

For the two observed startups, the literal seven-cell table gives the following results, conditional on A replies from the child.

| Initial strip | Inputs | Final strip | Calls to the right | Local steps |
|---|---|---|---|---:|
| 0000000 at coordinate zero | ABBBA | 2221222 | AAAB | 73 |
| 0000000 at a later cut | AAABB | 2122222 | AAAB | 91 |

A strip of seven digits in {1,2} stays in that set and returns A under either input, provided its child replies A. The worker checks all 256 single-call cases before composing eight-letter packets. It processes every other state literally. Actual B returns *inside* the strip are ordinary machine instructions and are included in these costs.

The fresh-strip table identifies a specific proof obligation. If every subsequent occupied cut sees an initial segment of `AAABB` until its fifth call and actually begins `AAABB` when that call arrives, then its entire startup is safe and each completed later call lies in the closed mature table. Apply the strip invariants in chronological order, including suspended calls. At any finite machine time each issued rightward letter comes from the actual stream, and every completed reply from its child is A. An indefinitely suspended call cannot itself reach an undefined instruction while these conditions hold. Thus a blank nonhalting proof could follow from establishing this prefix property. The finite driver accepts other safe startups as well.

Only four of the five required letters are automatically supplied by the preceding startup. For example, feeding a fresh seven-cell strip `AAABBBABABAAB` with A child replies produces `AAABA`. An independent input `AAB` to a virgin seven-cell strip returns B on the third call before ever touching a child. Neither example is a blank-orbit observation.

After the root startup, this condition determines the entire *shape* at a completed period. A nonroot strip produces no child calls on its first four inputs `AAAB` and ends in `2210111`. Its fifth input B produces all four calls `AAAB` during that single return and ends in `2122222`. Hence every occupied interior strip is mature and the last has received exactly four calls. At 35,000 periods the explicit prefix audit finds one root, 74,011 nonroot strips beginning `AAABB`, and one final strip with just `AAAB`. A failure of this sufficient condition would first appear as an A on the fifth call to a fresh nonroot strip.

## Which parent inputs send A on the fifth call?

After a nonroot parent receives `AAABB`, it is in state `2122222` and its child has received `AAAB`. The next nonempty output from that parent determines the child's fifth letter. Starting in `2122222`, execute each of A and B using the literal strip table. Continue only along silent transitions. This gives 26 reachable states and an acyclic graph, so some output arrives within 22 further parent requests. The shortest continuation first emitting A is `BABABAAB`. Either `AB` or `BB` first emits B in two requests.

The graph gives the complete set of 38 minimal continuations first emitting A. In the following expression, juxtaposition concatenates words and `|` denotes alternatives.

```text
U = BA | AAAB
Z = B | AAAB | AAAAAAB
D = U BA ( U ( AB | AAA | (AAB | BBBAA) Z ) | BBA Z )
```

A parent continuation sends the exceptional fifth A precisely when it begins with a word in D. There are also 82 minimal continuations first emitting B. The [finite graph checker](check_line15_fifth.py) enumerates every silent path and compares the A language with D. Among the 16 rotations of the negative driver's period, rotation 12 (zero based) begins with `AAABBABAAB` in D. Thus merely recognizing a factor of that period can admit an A that its distinguished starting position excludes.

For two cuts, keep the ancestor's physical strip and the intermediate child's phase. Until the intermediate fifth letter arrives, the child is the `AAAB` fringe. An A at that point is a separate failure. A B matures it, and later emissions from the ancestor feed its actual `2122222` state. Stop on the first output from this mature child. Each row starts immediately after the ancestor's five startup calls. The bounds count subsequent requests.

| Starting ancestor | Cuts ahead | Silent states | Maximum further requests | Shortest continuation sending fifth A at target |
|---|---:|---:|---:|---|
| Root, after ABBBA | 1 | 27 | 21 | AAAAB |
| Root, after ABBBA | 2 | 833 | 253 | AABBABBABB |
| Interior, after AAABB | 1 | 26 | 22 | BABABAAB |
| Interior, after AAABB | 2 | 834 | 254 | AABBB |

The actual root period starts with `BABA`, which sends the fifth B to coordinate 7. Its prefix `BABAABB` sends the fifth B to coordinate 14. At 35,000 periods every reached nonroot strip agrees, through its available letters, with the ten-letter anchor `AAABBABBAB`. Its image is `AAABBABBA`, whose own image is `AAABBA`. This anchor therefore settles the fifth B at two successive descendants. From coordinate 14 onward the measured common prefix is `AAABBABBABBABA`. At coordinates 14 and 14,707 the fifteenth letters are respectively A and B. Its first 13 letters already settle three descendants, whose images have lengths 12, 9 and 6.

Preserving an anchor across indefinite depth needs an additional restriction on its continuation. The input `AAABBABBABABBA` has the ten-letter anchor and emits `AAABBABBAA`, differing at position 10. The input `AAABBABBABABBAB` has the same anchor, emits `AAABBABBAAAB` at the next cut and `AAABBABA` at the cut beyond that, differing at position 8. Even the fourteen-letter anchor admits `AAABBABBABBABAABAABAB`, whose image `AAABBABBABBAA` differs at position 13. These counterexamples use A replies at the aligned cuts and agree with the admitted startup at each intermediate cut.

## A halting continuation when the source is allowed to vary

The 35,000-period checkpoint starts with **518,087 digits in {1,2}**, followed by `0111` and blank exterior. Allowing control of the incoming state at coordinate zero after that checkpoint admits a halt. This gives a concrete restriction on proofs that replace the actual left driver by arbitrary A/B choices.

* On the actual fringe `0111`, supply `AAABABAABBBAB`. Twelve calls return A. The thirteenth reaches the real undefined instruction B4 at absolute coordinate 518,092. The fringe has executed 121 instructions in total and its nonnegative word relative to its start is `3323441111`.
* To realize this input through the preceding digits, a single mature cell can emit either requested letter with no extra output. From digit 1, external B emits A and ends in 1, while external A emits B and ends in 2. From digit 2 first supply A, which silently changes it to 1, then use the same rule. All completed calls return A. Repeatedly apply this construction one cell to the left. Before the final halt every assumed child reply is thereby realized.
* If a requested word has a letters A and b letters B, its prescribed input has `2b + [initial digit = 2] − [last requested letter = B]` letters A and a letters B. Its last letter flips. Pairing two successive lifts gives the exact input length directly from the binary tape. The resulting number of root calls has 259,048 bits. The prescribed first letter is A, while the actual left driver supplies B here.

Thus the altered-input witness establishes a halt on a controlled continuation of the genuine positive tape. The blank machine's decision remains open. Along any trajectory from blank the terminal event has a simple physical signature. A 4 is written only when B on 2 moves right in B. While that request is pending, the next visit to the 4 comes from the right. A call can return B only if it began on B0, because the only write of 0 also exits left immediately. Consequently a scan of B2 with a zero immediately to its right reaches B4 in exactly two defined instructions, and every blank halt must arise this way.

The same construction works at *every* completed positive-group boundary satisfying the startup condition. The last strip ends in `2210111`, giving a mature prefix followed by the same fringe `0111`. It follows that even an arbitrarily long successful run of these startups cannot yield a nonhalting proof that allows unconstrained future inputs to the positive half.

## Reproducing the deeper checkpoint

Starting from the certified 120,000-period configuration, two batch partitions continued independently. One used boundaries at 170,000, 210,000 and 245,000 periods. The other used 195,000, 210,000, 230,000 and 245,000. Both produced byte-identical full checkpoint files at their shared endpoints. The independent physical window simulator then traversed the next period, reproducing both tape halves and the head at raw step **20,331,573,466,142**, 27,442,082 steps after the saved record.

To reproduce with the checked-in executable source, build the worker below, then run from `research/bb2x5`. A single invocation can cross the same interval. These batches also check the required startup letters and allow a restart after each completed boundary.

```sh
python3 frontiers/line15.py --engine /tmp/bb25-line15 --check-prefix \
  --groups 35000 --checkpoint /tmp/line15-35000.json
old=35000
for target in 120000 170000 210000 245000; do
  python3 frontiers/line15.py --engine /tmp/bb25-line15 --check-prefix \
    --groups "$target" --resume "/tmp/line15-$old.json" --checkpoint "/tmp/line15-$target.json"
  old=$target
done
cmp /tmp/line15-245000.json frontiers/runs/line15-next.json
```

## Replay and continuation

Run from `research/bb2x5`. The group target is absolute, including on resume.

```sh
c++ -O3 -std=c++17 frontiers/line15_stream.cpp -o /tmp/bb25-line15
python3 frontiers/line15.py --engine /tmp/bb25-line15 --groups 35000 --checkpoint /tmp/line15.json
cmp /tmp/line15.json frontiers/runs/line15-strips.json
/tmp/bb25-line15 35000 --check-anchor > /dev/null
python3 frontiers/check_line15_fifth.py
python3 frontiers/check_line15_obstruction.py /tmp/line15.json
python3 frontiers/line15.py --engine /tmp/bb25-line15 --resume /tmp/line15.json \
  --groups 35100 --checkpoint /tmp/line15-next.json
```

The window test advances the independent ten-billion-step snapshot to the same tape, coordinate and state as the 5,443-period strip run at **10,365,581,624** steps. The other tests compare strip replies with literal instructions, all tape cells across a small blank run, continuation, exceptional physical outcomes and the fringe witness.

```sh
c++ -O3 -std=c++17 frontiers/window.cpp -o /tmp/bb25-window
python3 frontiers/check_line15_window.py frontiers/runs/line15-next.json \
  --engine /tmp/bb25-line15 --window /tmp/bb25-window
BB25_LINE15=/tmp/bb25-line15 python3 frontiers/test_line15.py
BB25_LINE15=/tmp/bb25-line15 BB25_WINDOW=/tmp/bb25-window python3 frontiers/test_line15_window.py
```

For an incremental prefix audit, first run the blank seed with `--check-prefix` or the stronger `--check-anchor` native check. Supply that certified seed to `line15.py --resume` with `--check-prefix`. The worker verifies each new startup and the remaining letters at the old fringe. At the 120,000-period checkpoint the independent one-period window intersection compares every tape cell again after 13,449,082 more steps.
