# Line 31 can halt only two cells beyond a particular six- or seven-letter prefix

**Machine** `1RB3RB---4RA2RA_2LA2RA3LB4LB1LB`. On blank tape a halt occurs exactly when the rightward entries at some even coordinate start with **ABABAA** or **ABABABB**. The undefined instruction A2 is then reached two cells farther right. Every odd coordinate is safe. If the run lasts forever it visits every nonnegative coordinate. These are reductions of the decision problem. The blank-tape verdict remains **Unknown**.

The [inherited negative-half certificate](../mixed-and-sweeps.md#5-other-candidates-and-verification) gives the input A followed by repetitions of ABAAA at coordinate 0. The [earlier one-cell test](remaining.md#line-31) identifies BA at a fresh coordinate. The pair criterion, positive-half timing inequality and cut-history comparisons below are new in this pass. The [raw transition list](../SIMULATION_TABLE.md) identifies the full string. The arguments here have not been formally verified.

## Exact pair criterion

An entry is a rightward crossing from the preceding cell, or the initial A at zero. A completed excursion ends at the first leftward exit from the entry cell. A first B on a virgin cell exits left in A. A first A on a virgin suffix sends BB to its neighbor and exits left in B after five defined steps. All subsequent completed excursions return left in B. Indeed B0 is the only rule that exits left in A, and every instruction writes a nonzero symbol. These facts supply the return states for computing the following one-cell table from the literal rules. Each entry is the output word sent right and the new symbol. A star indicates that the cell has yet to call its right neighbor.

| Initial | On A | On B |
| --- | --- | --- |
| 0* | BB → 4 | ε → 2* |
| 2* | halt | ε → 3* |
| 3* | A → 1 | ε → 4* |
| 4* | A → 3 | ε → 1* |
| 1* | BA → 1 if calls return | A → 3 |
| 1 | B → 4 | A → 3 |
| 4 | A → 3 | ε → 1 |
| 3 | A → 1 | ε → 4 |

Start at an even coordinate with first entry A. The first two entries at its odd child are BB. They return immediately and leave 3* there. Before that child's first emission, each further B moves it from 3* to 4*, then to 1*. A in either of the former states sends A to the fresh even grandchild. B in 1* sends A. A in 1* sends B, the grandchild's B0 returns immediately in A, and the parent's A3 sends A to the just-written 2. These three defined instructions end on A2. This exception requires precisely BBBBA as the odd child's initial word.

After the initial A, the even parent is in ordinary state 4. For its odd child to receive a third B, the parent's next letters must be BA. The B is silent and the A emits B, restoring 4. A second BA produces the fourth B. The next emission is A exactly if the parent next receives A or BB, while another BA would emit an extra B. Including the original A gives the two target prefixes. In every other case, the first letter entering the even grandchild, when it is opened, is A. Starting with even cell 0 proves the criterion by induction along the frontier. A locally completed parent cannot conceal a deeper halt here: the only exceptional BA goes to a virgin grandchild, its first B immediately returns, and its second entry is itself undefined.

No positive excursion can be trapped in an infinite rightward call. Every mature cell emits at most one child request per entry, with finite local work. At the first unexplored even pair, a fresh A returns after initializing its odd neighbor with BB. A waiting odd edge has at most one outgoing request, apart from its exceptional BA which halts almost immediately. Thus a single root request on a finite visited prefix either returns or encounters the stated halt.

## An upper clock conditional on the coordinate

Assign weights 4 and 3 to A and B and add weights to obtain W(word). Assign the cell symbols 0, 1, 2, 3, 4 the potentials 36, 0, 27, 18, 9 respectively. Every successful edge of the displayed table satisfies

```text
7 W(output) − 3 W(input) ≥ potential(after) − potential(before).
```

For example, the silent B moves 3 → 4 and 4 → 1 each decrease the potential by nine. This finite certificate includes the preparation of a virgin cell. Summing over a completed input, using its initial potential 36 and nonnegative terminal potential, gives W(out) ≥ (3/7)W(in) − 36/7. Let W_x be the weight of the entire entry history at coordinate x through N completed root requests. Iterating the inequality gives

```text
W_x ≥ (3/7)^x (W_0 + 9) − 9,     W_0 ≥ 3N.
```

Consequently by N_x = ceil(11 (7/3)^x) requests the run has either halted or delivered at least seven entries at x: its weight is then strictly above 24 and six entries weigh at most 24. This excludes any infinite run restricted to finite positive width. For a proposed halt at x+2, checking the first seven entries of the even x settles that location permanently.

The negative driver uses 4j+1 local steps in its nearest block for j requests and passes j−1 requests down. Its total cost through N negative replies is 2N²+3N, as follows by summation of the [driver table](../frontiers/longitudinal.py). Until a halt at h=x+2 no positive coordinate beyond h has been visited. At most two entries cross each positive cut per root request: there is one per mature cell, plus the extra bounce at one virgin pair described above. The positive time per request is therefore at most 4(h+1) instructions, counting both directions. A coarse **upper bound conditional on h** is

```text
2 N_x² + 3 N_x + 4(h+1) N_x.
```

This bound is uniform over how the actual prefix is generated. It neither places an upper bound on the possible halting coordinate nor supplies a percentile of blank halting times. Individual gaps may be computed exactly from two completed group checkpoints by subtracting their clocks.

## Observations from blank

At the inherited 10¹³-group checkpoint the replay agrees on the complete tape, head, state and exactly 5,000,000,000,000,629,129,529,402,408 defined steps. Among the even coordinates 0–136, only 82 has initial ABAB, and its actual prefix is ABABBAAB. At 136 the observed prefix ABA is still undecided at that clock. The two target words do occur at other positions in the sampled even streams: ten occurrences in the first 32 entries of even cells 0–66 and twelve in the samples at 68–136 (truncated at the frontier). The first such interior match is at coordinate 12, offset 10 counting from zero. A blanket prohibition of either target as an interior factor cannot prove the needed restriction at the distinguished entry. [Saved lifetime cut histories](edge31_prefixes.json)

Eight further batches of 10¹² source groups reach 18 × 10¹² groups at exactly **16,200,000,000,001,132,433,153,618,030 raw steps**. The observed even prefixes at 136 and 138 now begin ABAAB and AAB. These prefixes permanently clear the A2 tests at coordinates 138 and 140. At 140 the prefix is still ABA and at 141 it is BBB. The earliest remaining candidate location for A2 is therefore 142. [Complete endpoint](edge31_checkpoint.json) · [Batch records](edge31_batches.jsonl)

The first A entries at 138 and 140 occurred at steps 7,388,458,752,799,867,023,940,439,264 and 8,613,875,231,497,429,561,833,864,156. The gap between opening these two opportunities was **1,225,416,478,697,562,537,893,424,892 defined instructions**. These clocks come from bisection on completed driver groups, followed by literal positive execution of at most one five-request group in physical order. The negative tape is reconstructible from the completed request count. The same locator matches the unaccelerated full configurations and clocks at 2, 4 and 6. [First visits](edge31_visits.jsonl) · [Locator](edge31_visits.py)

The same density of inputs can give an immediate failure. The artificial root input A followed by repetitions of BABAAAAAAA has eight As and two Bs per repeating word, exactly as two true periods do. Its initial ABABAA already halts at coordinate 2. Actual phase, correlations and changes with depth matter. There is no calibrated per-pair halting probability here.

## Replay and next proof step

From `research/bb2x5`, use Python 3 and a C++17 compiler with GMP. The tests exhaust all 4,095 supplied A-initial words of length at most 12, including 199 physical halts, and verify the local potential certificate. Four small blank traces compare the full configuration, raw count and cut histories against the literal interpreter. The longer run reuses the repository's guarded boundary worker, including its handling of candidates in physical order. [Verifier](edge31.py) · [Test output](edge31_verification.txt)

```sh
c++ -O3 -std=c++17 frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-stream
python3 frontiers/replay_streams.py --line 31 --engine /tmp/bb25-stream --trace-prefix 32 > /tmp/edge31-prefixes.json
cmp /tmp/edge31-prefixes.json halting-outlook/edge31_prefixes.json
python3 frontiers/longitudinal.py --engine /tmp/bb25-stream --line 31 --groups 1000000000000 --batches 8 --trace-prefix 8 --resume frontiers/runs/stream-31.json --checkpoint /tmp/edge31-endpoint.json > /tmp/edge31-batches.jsonl
cmp /tmp/edge31-endpoint.json halting-outlook/edge31_checkpoint.json
cmp /tmp/edge31-batches.jsonl halting-outlook/edge31_batches.jsonl
python3 halting-outlook/edge31.py --engine /tmp/bb25-stream
python3 halting-outlook/edge31_visits.py --engine /tmp/bb25-stream > /tmp/edge31-visits.jsonl
cmp /tmp/edge31-visits.jsonl halting-outlook/edge31_visits.jsonl
```

A proof target is the distinguished prefix of the paired transformation on the specific periodic driver. In the ordinary cell states ordered 1,4,3, A advances a cyclic phase and B retreats it. When the input period has nonzero displacement modulo three, three repetitions visit every initial phase at each position. They emit (2a+b) As and a Bs in total for a period with a As and b Bs. This identity follows by reading the three ordinary rows of the table; it controls aggregate counts only. Track the **position of the first emissions** as well as this phase when passing to the next pair. A certificate excluding the two anchored words at all even cuts would settle nonhalting. Alternatively a physically replayed occurrence at any one even cut would settle halting.
