# BB(3,3) holdout rankings

For the latest #758/#153 checkpoint, enlarged halting interval and exact open proof obligation, see the [research handoff](README.md).

**19 November 2026 · Four open blank-tape questions, six machine encodings.** The longest *proven halting* three-state, three-symbol machine takes **119,112,334,170,342,541 steps**. Of the four holdouts, #758/#153 has the strongest positive case for halting. **Every one of the six encodings has already run beyond that record from blank.** If even one of the four cases halts, the lower bound for BB(3,3) rises. [BB(3,3) status and champion](https://wiki.bbchallenge.org/wiki/BB%283%2C3%29)

## Research queue

Rank reflects how concrete the next proof step is and whether it would settle a second machine, following the linked BB(6) ranking. The behavior column gives a conjecture in every row. A **raw step** is one transition of the original machine. A **pass** or **map step** is one update of the indicated accelerated model. [BB(6) ranking at the supplied commit](https://github.com/valu42/busycoqtesting/blob/175f2c272c1d5dfd1ff16f277839f19877cb2364/research/bb6/RANKINGS.md)

| Rank | Holdout | Expected from blank | Published evidence | Result of this investigation | Next proof step |
|---:|---|---|---|---|---|
| 1 | **#758 / #153**, candidate champion | **Likely halts.** A halt would beat the proven record. | More than 10²⁷ raw steps simulated for #758. Many starting values flow to the same known halt. [Analysis](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA) | The blank orbit bypasses the 64 published direct-halting seeds and the fourth candidate pair, then reaches **18,378,934,934,402,308** at a = 1 after more than **1.48 × 10⁴⁶ raw steps** in each encoding. Near the large target, proved halting intervals contain **33,533,925,880,304** and **362,166,436,260,267** consecutive reset seeds at different distances. [Blank proof](POWER_CROSSINGS_758.md) · [Halting intervals](LOWER_SCALE_GATES_758.md) · [Global exclusion of periodic ordinary motion](FINITE_AFFINE_PERIODS_758.md) | Prove that the blank orbit must enter the interval, or halt sooner. |
| 2 | **#531 / #532**, Wily Coyote | **Leans non-halting.** The dangerous event is a particular carry reaching the far end of the word. | A shared four-mode sweep describes both machines. The wiki reports 3.213 × 10³⁸ raw steps for #531. [Wily Coyote](https://wiki.bbchallenge.org/wiki/Wily_Coyote) | Both completed **2⁹⁶ passes** from blank, implying **more than 3.13 × 10⁵⁷ raw steps** each. | Prove that the far edge never receives mode s1. One invariant would cover both encodings. |
| 3 | **#397** | **Leans non-halting.** Legion conjectured that the halting edge is unreachable. | A related six-carry sweep has two dangerous edge modes. The wiki reports $10^{15.314}$ raw steps. [Analysis](https://wiki.bbchallenge.org/wiki/1RB1LB2LC_1LA2RB1RB_---0LA2LA) | Completed **2³⁶ passes** from blank, implying **more than 2.36 × 10²¹ raw steps**. A future halt would beat the proven record. | Find a property of the reachable words that excludes both edge modes, cc and ce. |
| 4 | **#829**, Bigfoot | **Strongly expected to run forever.** A deterministic counter exhibits positive drift. | Ligocki observed counter value 3,999,888 after 24 million map steps. Halting requires a decrement from zero. [Ligocki's analysis](https://www.sligocki.com/2023/10/16/bb-3-3-is-hard.html) | The blank orbit exceeds **7.57 × 10³² raw steps**. Constructed another seed that follows its first 256 branches and then halts. | Bound cumulative losses along the specific blank seed. Arbitrary seeds can imitate any finite safe prefix. |

The public Lean development gives exact reductions for all six encodings. Those theorems justify studying the smaller maps. A proof deciding one of these four blank orbits would be a further result. The computations below use Python integer arithmetic and have not been independently certified in Lean or Rocq. [Formalized reductions and machine specifications](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB33/README.md)

## #758 and #153 — an interval that leads to a halt

Write A(a,c) for the published two-counter configuration of #758. The blank starts of #758 and #153 enter the same map at (0,1) and (1,1), respectively. I traced those seeds to the common point **(1,341)** after 122 and 126 map steps. I also ran the two raw machines to their published join at steps **1,841,608** and **1,790,901**, respectively, and compared every nonblank cell and the head state after reflection and relabeling. Consequently, if they halt, **#758 runs exactly 50,707 raw steps longer than #153**. [Machine analysis and raw join](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA#Equivalence_to_1RB0LB0RC_2LC2LA1RA_1RA1LC---)

The updated blank-tape calculation also establishes more than **1.28 × 10⁴⁴ raw steps** for each encoding. [Checkpoint and clock](BLANK_CROSSINGS.md)

As a separate clock check, I ran 2²¹ map steps from the #758 blank seed. Adding just the known cost 3a² + 5c + 6 on the odd/odd branch with a ≤ c, plus the two entry steps, gives **at least 1,000,010,983,141,407,650 raw steps**. Omitting all other branches makes this a lower bound. Subtracting 50,707 still leaves #153 above 10¹⁸. Summing all ten branch clocks gives the exact #758 time of **3,251,620,479,139,366,879** at the same 2²¹-update checkpoint. [Clock verifier](timing_758.py) [Published branch timings](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA#A(a,_c)_Rules_and_Timings)

LegionMammal and dyuan identified the halting target

$$
H = \frac{3^{307}-8\,282\,708\,212}{13\,959\,275}.
$$

The published analysis reports a continuous interval reaching at least as far back as H − 8,000,000. I started the calculation with H alone, verified that A(1,H) takes the halting branch on map call 307, and checked every integer in the following **inclusive** interval. [Published interval and reachability argument](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA)

$$
H-12\,000\,000 \;\le c \le\; H-3\,403\,055.
$$

All **8,596,946** starts A(1,c) reach A(1,H). This extends the lower endpoint reported on the wiki by **4,000,000**. The upper endpoint is sharp for this interval. The very next starting value, H − 3,403,054, skips H and reaches H + 196 after 3,229 returns to a = 1. Its subsequent behavior is a separate question.

For each starting value, the verifier computes exact returns to a = 1 until it reaches a previously checked value. It requires each return on these paths to increase c without passing H. To accelerate consecutive odd/odd branches with a ≤ c, put u = a + 1. After k such branches the counters are a′ = 3ᵏu − 1 and c′ = c − u(3ᵏ − 1)/2 + 2k. The verifier batches only when u3ᵏ ≤ 2c + u, a sufficient condition for each individual branch. The blank orbit could still jump across the entire checked interval. A bound on the size of a return jump before entry would address that gap.

## Wily Coyote and #397 — finite blank-tape runs

Each published sweep prepends one bit to a word and processes the old word from its head-facing end. Here bit 0 means tape symbol 2, and bit 1 means symbol 1. After t completed passes, the first t bits equal the length-t prefix of a periodic word. The short cycles below follow directly from the transition tables. Reading one prefix bit emits the next bit and advances to the next listed carry. [Wily sweep](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB33/WilyCoyote.lean) · [#397 sweep](https://github.com/google-deepmind/cryptids/blob/3647718b5df22e1a61462dec0376bd204526285a/BusyBeaver/BB33/M_1RB1LB2LC_1LA2RB1RB_HHH0LA2LA.lean)

| Machine | Repeating prefix in bits | Carries presented to the remaining suffix | Completed passes | Remaining suffix length |
|---|---|---|---:|---:|
| Wily #531 and #532 | 01 | s0, s1 | 2⁹⁶ | 291 bits |
| #397 | 0100 | ca, cc, cd, ce | 2³⁶ | 167 bits |

The calculation processes **one tape cell at a time**. For a fixed starting bit, each input carry determines the new bit and the carry, if any, sent to the next cell. A whole stream of carries can therefore be evaluated by splitting it into two ordered pieces, feeding the first piece's final bit into the second, and reusing identical pieces. The first event at a fresh edge either halts or appends the prescribed bits. Every event comes from the finite periodic input above. The computed suffix and the periodic prefix together specify the entire checkpoint word.

**Conversion to raw steps.** On pass t, count the initial transition on blank and the t protected prefix symbols. For #397 the raw head moves left through tape pattern 2122, starting in A and returning to A every four symbols. For Wily the head starts in B immediately after the initial transition and advances across each 21 pair. #532 uses two raw moves per pair. #531 uses four, including a leftward detour. Thus each completed pass costs at least t + 1 raw transitions in either model. Summing from t = 0 to N − 1 gives the common lower bound **N(N + 1)/2**. It omits the positive initial setup cost and the rest of each sweep.

The verifier compares complete raw configurations for the first 96 passes of #397, #531 and #532. It also compares ordinary chronological suffix evolution at 16,384 passes with the calculation organized by cell. The large checkpoints establish finite survival. An invariant must still explain why a halting carry can never reach the edge.

## Bigfoot — why a finite residue test can be misleading

Use Ligocki's unshifted coordinates B(a,x) = A(a,2x+1,2). The blank tape reaches B(2,0) in 69 raw steps. After 256 map steps from blank, the counters are a = 39, b = 378,951,064,202,468,329,774,865,356,477,385 and c = 2. The configuration contains a run of 2b ones. Each raw transition can create at most one nonblank cell, so the machine has already executed more than **7.57 × 10³² raw steps**. [Blank seed and tape encoding](https://www.sligocki.com/2023/10/16/bb-3-3-is-hard.html)

Over four map steps, the length update on each residue class x modulo 81 has the form x = 81q + r → 256q + sᵣ. On r = 5 the four residues of the original length modulo 6 are **5, 3, 2, 2**. The last two each subtract one from a. Substitution in the published rules gives the following update whenever a ≥ 2. [Bigfoot's four-step representation](https://www.sligocki.com/2023/10/16/bb-3-3-is-hard.html#alternative-representation)

$$
B(a,81q+5) \longrightarrow B(a-2,256q+22).
$$

On this branch the new length is F(x) = (256x + 502)/81. It satisfies 175F(x) + 502 = (256/81)(175x + 502). For any m, choose a nonnegative x with 175x + 502 divisible by 81ᵐ. Such an x exists because 175 is coprime to 81. At every one of the next m blocks, the current length is 5 modulo 81, for as long as the counter permits the block. This gives arbitrarily long runs of losses across the family.

One can even prescribe a safe prefix from blank. Replacing x = 0 by x = 81ᵏv preserves the first k four-step branches and changes the resulting length by 256ᵏv. Since 175 · 256ᵏ is invertible modulo 81ᵐ, one can choose v to force the losing branch thereafter, long enough to halt. The verifier constructs one such seed for k = 64. Its counter matches the blank trajectory through the first **256 map steps**, reaching 39, and its **80th subsequent map step** takes the halting branch. A proof of Bigfoot's expected non-halting needs information about the actual seed beyond any fixed finite residue prefix.

## Machine encodings and reproduction

Rows A, B and C each give the instructions on symbols 0, 1 and 2. An entry `---` is the halting instruction. Every run starts in state A on an all-zero, two-way infinite tape. The IDs are the community's 925-list identifiers. [Holdout list and ID provenance](https://wiki.bbchallenge.org/wiki/BB%283%2C3%29#Certified_Progress)

| ID | Standard transition encoding |
|---:|---|
| 758 | `1RB2LC1RC_2LC---2RB_2LA0LB0RA` |
| 153 | `1RB0LB0RC_2LC2LA1RA_1RA1LC---` |
| 531 | `1RB2LA1LA_2LA0RA2RC_---0LC2RA` |
| 532 | `1RB2LA1LA_2LA0RA2RC_---1RB2RA` |
| 397 | `1RB1LB2LC_1LA2RB1RB_---0LA2LA` |
| 829 | `1RB2RA1LC_2LC1RB2RB_---2LA1LA` |

Run the companion script with Python 3.10 or later. The default command checks the small orbits, the paired raw configurations and the Bigfoot construction. The full run also checks the interval and both large suffixes against their SHA-256 digests. It uses only the standard library. Allow several minutes and roughly 1–2 GiB of memory for the full run. [check_bb33.py](check_bb33.py)

```sh
python3 check_bb33.py
python3 check_bb33.py --full
```
