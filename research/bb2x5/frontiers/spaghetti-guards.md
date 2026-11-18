# The BBA guard on lines 19 and 23

Use the line 19 rules and physical coordinates throughout the guard analysis. Line 19 starts in A. Reflection, digit permutation and state exchange turn line 23 from its actual blank A into line 19 from blank B. The `configuration` in each record uses the original machine and coordinates. Its guard records use the common line 19 coordinates and states. [Conjugacy checker](line19_pair.py)

## Which crossing can halt?

A cell strictly to the left of the head was either blank or last written by a rightward step. Its possible symbols are 0, 1, 2 and 4. Strictly to the right the symbols are 0, 2 and 3. The same description applies to the scanned cell on a rightward and leftward arrival, with the corresponding side's alphabet. On the initial blank both conventions agree.

The undefined instruction is A3. A 3 was last written by A2 moving left. Reentering that 3 from its left in A requires A1 or B1. The 1 is impossible on a rightward arrival, so this predecessor has just arrived from the marked 3. Only A2 writes 3 and moves left, sending A. Consequently the last two defined instructions before a halt are A2 then A1. The 1 came from an earlier A0 at coordinate x that sent B into x+1. Its digit stayed 1 until the return from x+1.

On that first B entry at x+1, B0 returns left at once, leaving 2. B2 writes 4 and calls its right neighbor in B. Either reply on 4 exits left without writing 3. The remaining case is B3. Let U be the physical suffix beginning at x+2 at the time of this entry. The following steps apply unless a deeper excursion halts first.

| Replies already received at x+1 | Operation sending the next call to U | Effect of a B reply |
|---|---|---|
| None | B3 writes 0 and sends B | B0 exits left safely |
| A | A0 writes 1 and sends B | B1 writes 4 and calls right. Either subsequent reply exits safely on 4 |
| AA | A1 writes 2 and sends A | B2 writes 4 and calls right. Either subsequent reply exits safely on 4 |

If the last reply is A, A2 writes 3, A1 on the original guard returns A, and the head scans the undefined A3. Thus the ordered calls **BBA** must all return A for this particular guard to cause a halt. A new guard can arise inside an outstanding call.

## No reachable launch begins with 2 in U

Consider an actual A0 at x with 3 at x+1. That 3 was written by A2 moving left. It has not been revisited since its last creation, because the only defined instruction on 3 changes it to 0. Immediately after its creation A scanned x, whose digit lay in the left-side alphabet. While the head remains at x or to its left, each departure left from x may return in either state. The complete possible first exits right from x are as follows. An entry with no successful right exit does not lead to the stated launch.

| Digit originally at x | Possible instruction for the first right exit |
|---|---|
| 0 | A0, immediately |
| 1 | A1 |
| 2 | B3 |
| 4 | B2 or B3 |

An A0 launch must therefore follow the A2 at x+1 immediately. The A2 could not have arrived from x, since both instructions moving right into A write 2 or 4 on the departure cell. Instead it arrived from x+2. For U to start with 2, the preceding instruction at x+2 would have had to be B0, the only rule writing 2 while moving left in A.

At that preceding instant x+1 was strictly left of the head and held 2. Its last rightward departure must have been A1, which entered x+2 in A. Before x+2 next exits left, permit both replies to each local request to the right. For starting symbols 0, 2 and 3 the possible successful left-exit instructions are respectively {A2, A4, B4}, {A2} and the empty set. In particular B0 cannot be that exit. These two one-cell enumerations allow arbitrary intervening returning excursions. The blank initial tape supplies neither the marked 3 nor the 2 at x+1, so both required last writes exist for either initial state. The guard can only launch on U beginning with **0** (left arrival from B4) or **3** (left arrival from A2).

The earlier A1 departure from x+1 consumed a 1, previously written by A0 calling x+2 in B. That call returned A onto the 1. Thus counting from this earlier B call, a fatal suffix sees the consecutive calls **BABBA**, all returning A. The suffix contents evolve during those five calls. `verify_antecedents()` replays the two one-cell exit tables above against every possible reply state. [Checker](spaghetti_guard.py)

## Fresh and previously visited left guards

When A0 scans a previously visited cell x, its 0 was last left by a rightward departure, since the head has just arrived from x+1. The only such zero-write is B3 at x. This launched B into x+1. Its first left exit from x+1 was the A2 that now sends A onto x. By the one-cell B-entry table above, the previous B call could only have exited via A2 by starting on 3 and sending BBA into U with replies AAA. The new A0 guard now sends another BBA to this same evolving suffix. Consequently a halt at a previously visited guard requires **BBABBA with six consecutive A replies**. The synthetic suffix `2202000` can answer all six requests this way. [Literal suffix check](test_spaghetti_guard.py)

## Blank-orbit guard traces

The [line 19](runs/spaghetti-19.json) and [line 23](runs/spaghetti-23.json) runs reach 100,000,000,000 defined instructions each. Each row below counts the normalized B3 entries after the A0 guard, grouped by the first four symbols of U at launch. The reply columns are mutually exclusive completed outcomes. One line 19 guard is still waiting for its first reply at the endpoint.

| Original line | Start of U | B3 entries | First visit at A0 | Previously visited | B | AB | AAB | AAA | Open |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 19 | `0222` | 2,216 | 0 | 2,216 | 0 | 0 | 2,216 | 0 | 0 |
| 19 | `3000` | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 |
| 19 | `3202` | 24,799 | 0 | 24,799 | 0 | 2,215 | 22,584 | 0 | 0 |
| 19 | `3232` | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| 19 | `3233` | 31,531 | 31,531 | 0 | 0 | 0 | 31,530 | 0 | 1 |
| 23 | `0222` | 2,230 | 2 | 2,228 | 0 | 0 | 2,230 | 0 | 0 |
| 23 | `3202` | 56,258 | 31,480 | 24,778 | 0 | 2,228 | 54,030 | 0 | 0 |

Every one of line 23's 58,488 launches belongs to the `0222` or `3202` classes. Both guarantee an ordinary exit from this guard whenever all its suffix calls return normally. In this finite run, all 27,015 line 19 launches at previously visited A0 sites likewise have one of those two safe prefixes. Every `3233` launch on line 19, including the one still outstanding, arose on a first visit to a new leftmost coordinate. A proof that this restriction persists would separate the unresolved `3233` case from previously visited guards. Neither run has launched on `3022`. [Checked four-cell guard filter](line19-guard-filter.md)

The first completed third call on line 19 arose from a B3 at normalized coordinate 0 at clock 96. Its three replies arrived at 98, 108 and 116. On line 23 the first B3 leading to a third reply was at normalized coordinate −3 at clock 53, with arrivals at 55, 65 and 73. In both cases the entry suffix started with 0. Each call begins one instruction after the recorded B3 or previous reply.

Line 19's longest observed third call lasted 354,371,331 instructions. At coordinate −61,339 the first two replies arrived at 94,484,237,403 and 94,484,237,409. The third call entered the suffix in A at 94,484,237,410 and returned B at 94,838,608,741. On line 23 the longest third call lasted only seven instructions. Among right-oriented inputs an A call returns in B within seven steps exactly when its word begins `020`. It then takes seven steps and rewrites those three cells to `232`. Enumerating seven digits suffices, since none of the first seven steps can scan an eighth cell. Thus **all 56,260 completed third calls on line 23 started on 020**. Proving that future line 23 guards reaching AA must present this prefix would settle that orbit. The line 23 splice calculation traces how the short return is produced and exhibits a halting splice of two blank-orbit tapes. [Seven-step exhaustive check](spaghetti_guard.py) · [Short returns and splices](line23-splice.md)

## Reproducing and continuing

The worker packs 16 two-bit cells per tile. Code 3 denotes physical 4 for a cell on the left and physical 3 for a cell on the right. At the head the direction of arrival selects the interpretation. It composes literal eight-cell traces to advance a tile. Every cache key includes the entire word, the entering side and the state. A first-exit trace also records whether a candidate event can occur inside its tile, or at its left boundary conditioned on the exterior digit being 1. An eventful tile replays chronologically. The event counters recognize the outgoing B3 and the leftward returns on 0, 1 and 2 next to the suspended 1. A per-coordinate record matches each return to its original guard. Each tile summary retains the smallest physical coordinate reached and the relative clock when it was first reached, counting the starting head and the arrival on an exit. The global minimum starts at the origin at clock zero. For a B3 entry at cell y at clock t, the previous A0 is fresh-left exactly if y−1 became the global minimum for the first time at t−1. Its arrival came from y, and nearest-neighbor steps make the visited set a contiguous interval. Literal tests keep the full set of visited coordinates and compare the classifications. Bounded subtraces preserve their exact intermediate configurations.

From `research/bb2x5`, build and run the worker and cross-check against the independent physical moving-window checkpoints.

```sh
c++ -O3 -std=c++17 frontiers/spaghetti_guard.cpp -o /tmp/bb25-spaghetti
python3 frontiers/spaghetti_guard.py --engine /tmp/bb25-spaghetti --line 19 \
  --target 100000000000 --profile --checkpoint /tmp/spaghetti-19.json
BB25_SPAGHETTI=/tmp/bb25-spaghetti python3 frontiers/test_spaghetti_guard.py
```

A second implementation continued the existing moving-window checkpoint on each physical machine from 10 billion to 100 billion steps. At width 10 it took 1,880,311,590 window operations on line 19 and 1,880,304,949 on line 23. On both it matched the entire stored tape, head, state and raw clock of the guard-aware simulator. To reproduce either comparison, set `n` to its original line number.

```sh
n=19
python3 frontiers/survey.py --engine /tmp/bb25-window --line "$n" --width 10 \
  --resume "frontiers/runs/window-$n.json" --target 100000000000 --work 11000000000 \
  --checkpoint /tmp/spaghetti-window-check.json
PYTHONPATH=frontiers python3 -c 'import sys, survey, spaghetti_guard as g
n = int(sys.argv[1])
p = survey.load("/tmp/spaghetti-window-check.json", n, g.MACHINES[n])
assert p == g.load(f"frontiers/runs/spaghetti-{n}.json", n)["configuration"]' "$n"
```

Use `--line 23` for the other blank orbit. Request a larger absolute target to extend the guard chronology from blank. For a continuation that needs only the physical tape, extract the enclosed window payload and use the ordinary window engine.

```sh
c++ -O3 -std=c++17 frontiers/window.cpp -o /tmp/bb25-window
PYTHONPATH=frontiers python3 -c "import spaghetti_guard as g, survey; p = g.load('frontiers/runs/spaghetti-19.json',19); survey.save('/tmp/spaghetti-window.json',p['configuration'])"
python3 frontiers/survey.py --engine /tmp/bb25-window --line 19 \
  --resume /tmp/spaghetti-window.json --target 100001000000 --checkpoint /tmp/next-window.json
```
