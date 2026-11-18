# Line 17 · timing the first visit to +12

Line 17 first reaches the blank at coordinate +12 within **81,526,541 inputs at cut 403**, the entrance to its last 21 data pairs. This bound is sharp if the continuation after the 26 known inputs there can be any valid marked stream. On the actual blank orbit, inversion through the first 95 pairs places the visit before sweep **4.763 × 10¹⁷¹** and raw step **3.176 × 10³⁴⁴**. The [simulation table](SIMULATION_TABLE.md) gives the observed lower endpoint. The return branch taken by the blank orbit and the machine's eventual halting status remain open. [Elementary-machine reduction](frontier-background.md#why-the-424-digits-reach-the-edge)

## Bounding the time at a single cut

Suppose a digit starts with trit v. After n input slots, let O count its output slots, C its compound pulses (including pending pulses), and w its final trit. The two rows of the [pulse table](frontier-background.md) give the identity

```
3O + w = n + v + 4C.
```

An ordinary pulse increments the left side by one. A compound pulse increments it by five at each of the three trits. Thus O = ⌊(n + v + 4C)/3⌋. Starting from any trit and pending bit, the all-zero continuation minimizes O at every input length. An initial pending burst must complete or consume the entire available prefix. Any later externally marked slot can only add compound pulses. This comparison applies separately at each digit, even when additional marks change its downstream stream.

The true stream at cut 53 has period 147,740 and starts with the 26-slot word `00001000001000001000001000`. A digit starting at trit 1 with clear pending bit preserves this whole prefix. In particular, the fifth mark at cut 403 can be no earlier than slot 27. To check the preservation, emit the known input, then enumerate the next five output bits over legal continuations. A legal mark has at least two preceding unmarked slots after the previous mark and cannot overlap a pending pulse. Retain the common prefix. All 350 digits at indices 53 through 402 start in the required state. Applying the same finite check to the 21 remaining digits supplies a guaranteed prefix at each of their inputs.

Start at the singleton with required output rank one. At each preceding digit, append zeros to its guaranteed input prefix and find the input slot that emits the required rank. The identity above proves that the true digit emits at least that many slots by then. Repeating the calculation right to left gives required slot **81,526,541 at cut 403**. Independently, supplying its guaranteed prefix and then only zeros, propagating those specified streams, and running the triggering pulse on the physical suffix gives the first visit on precisely that slot. The word on cells −1 through 11 in this example is `4444040444444`.

## Translating cut slots into raw time from blank

In each of the 350 homogeneous digits the four known marks contribute twelve compound pulses. For a required rank R beyond that prefix, its latest parent is 3R − 49. This follows from the single-digit identity with v = 1 and C = 12. We apply this bound back to cut 95. Through digits 0 to 94 we use the true periodic input from blank and find the exact root slot emitting that cut-95 rank. The worker skips repeated periods in reverse and independently checks the selected slot by counting complete sweeps forward and replaying the last one to four root slots.

Write E for the resulting sweep, rounding the root slot up after division by four. We get E < 4.763 × 10¹⁷¹. To bound elementary steps, charge each partially executed pulse up to the singleton its complete local cost under the ordinary replies. Every completed sweep with pile length k costs 58 + 28k plus the raw probes issued into the fixed register, before counting work within that register. There are at most 16 such probes per sweep. Every fixed pair takes at most four incoming probes, eight outgoing probes and six internal moves per input slot. Pair i receives at most 4E·2ⁱ slots. Adding the blank initialization and the single B2 instruction from the singleton into +12 gives

```
time of first +12 ≤ 2,308,941 + 14E(E−1) + [74 + 72(2^424−1)]E.
```

The comparison only charges instructions up to the first arrival. It yields the raw bound above without assuming ordinary replies continue after +12.

## The return depends on two bits

At cut 418 the first eight inputs are `01000000`. The first visit to +12 occurs by slot 12 at this cut. The three-slot mark separation allows only six sets of new marks in slots 9–12. Running the last six pairs and singleton literally gives this complete decision rule.

| Slot 9 | Slot 10 | Symbol at −1 with B at +12 | First cut-418 slot reaching +12 |
|---|---|---:|---|
| Marked | Unmarked | 1 | 9 |
| Unmarked | Marked | 0 | 10 |
| Unmarked | Unmarked | 4 | 11 if marked there, otherwise 12 |

Applying the same backward bound to **slot 10 at cut 418** gives **52,828,727 slots at cut 403**, or **1,956,632 at cut 406**. A finite prefix through this deadline suffices to select the actual return if its marks are known. The `decide` command accepts sparse mark positions. It also works on shorter prefixes and reports which branches the observed slots still permit.

There is a simpler sufficient condition for symbol 4. Suppose the marks seen at cut 403 through the decision deadline form an initial segment of 5, 11, 17, 23, 29, 35, … . At a single digit, each child marked position depends only on the input marks up to its parent. Deleting all input marks after a given one therefore retains an initial segment of the child marks. This property composes across digits, including any initial pending pulse. Both extreme streams at cut 403 (stop marking after 23, or continue every six slots forever) give **exactly one mark at cut 406, on slot 4**, followed by unmarked slots forever. Every intermediate truncation has that same cut-406 stream, hence the same symbol 4. A different return on the blank orbit requires a first mark departing from this progression before the decision has been made.

## Three continuations of a true upstream prefix

All three possible symbols at −1 survive even if an input at cut 53 must begin with **one entire true period**, and its continuation then passes through all 350 homogeneous digits. The three cut-403 streams below share the first five marks at 5, 11, 17, 23 and 28. Each subsequently places marks at the stated constant gap until its first extension.

| Gap at cut 403 | Cut-403 slot entering +12 | Cells −1 through 11 with B at +12 |
|---:|---:|---|
| 5 | 165 | `0444040444444` |
| 7 | 3,641 | `4444040444444` |
| 8 | 461 | `1444040444444` |

To construct each continuation, propagate the 18,468 marks of the true first period through the [integer register](marked-register.md#times-of-marked-slots). Exactly four marks survive. Let C be its coefficient after this prefix, P = 3³⁵⁰ and A = (P−1)/2. For a desired child mark y, supply the next mark at cut-53 slot t = Py − 5A − C. This selects residue one at each digit and increases C by 8A. The first new t is beyond the true period. Subsequent gaps in the constructed input are P(gap−4) + 4, so all marks are sufficiently separated. The checker verifies each emission with the forward integer recurrence. It then reconstructs the suffix immediately before the triggering input and executes that pulse with the physical transition table. An independent test runs every input literally on all 21 pairs through the extension.

These three continuations agree with the first true period. To determine the actual return one must also use the fact that the true period repeats. A different explicit case, continuing with a mark every sixth slot forever at cut 403, enters +12 on slot 9,058,530 with symbol 4 at −1.

## Reproduction

Run these commands from `research/bb2x5`. The Python-only bound uses the first 53 exact pairs and gives the same sharp cut-403 bound. The packed calculation uses 95 exact pairs for the stronger blank-orbit clock.

```sh
python3 frontiers/line17_edge.py bound
c++ -O3 -std=c++17 frontiers/line17_packed.cpp -lgmpxx -lgmp -o /tmp/bb25-packed17
python3 frontiers/line17_edge.py bound --cut 95 --packed-engine /tmp/bb25-packed17
python3 frontiers/line17_edge.py suffix --prefix 00001000001000001000001000 --period 0
python3 frontiers/line17_edge.py decide --through 52828727 --marks 5 11 17 23
python3 frontiers/line17_edge.py branches
BB25_PACK17=/tmp/bb25-packed17 python3 frontiers/test_line17_edge.py
```
