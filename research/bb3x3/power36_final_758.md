# The blank runs reach the power-36 checkpoint

Both #758 and #153 on blank tape reach the exact reset

$$
\boxed{A(1,3^{36}+112\,032)
       =A(1,150\,094\,635\,297\,111\,153)}.
$$

This completes the previously open bridge from the doubled-power-35
checkpoint to power 36. The proof connects **every one of the 4,831 regular
windows**, then applies the power-36 gate merger. The eventual blank-tape
halting question remains open. In particular, this finite bridge does not
establish entry to the distant halting basin or assert the same bridge at
later exponents.

## Starting on the actual blank orbit

The [doubled-power-35 proof](DOUBLED_POWER35_758.md) establishes the common
blank reset

$$
S=2\cdot3^{35}+155\,534
 =100\,063\,090\,198\,154\,948.
$$

The regular cuts in `power36_followon_758.py` start at S, increase by
$10^{13}$, and finish with a shortened last window at

$$
G=148\,364\,731\,025\,779\,389.
$$

Each window has a 5,001-seed incoming strip. Its crossing statement is
universal: every reset in that strip reaches a later even reset inside
the next cut's 5,001-seed strip. The entire outgoing set is retained.
Composing these statements therefore tracks the actual blank orbit
without choosing an arbitrary possible exit.

The first regular window is the chain of six archived initial crossings.
For 4,095 regular windows, matching guarded words at the two even endpoints
give the symbolic crossing directly. The remaining crossings use the
archived integer worker. The new [complete-chain checker](power36_final_758.py)
checks that the resulting index set is exactly `{0,...,4830}`. No gap is
left between an earlier exact checkpoint and a later conditional corridor.

## Completing the final 584 windows

The earlier archives are retained unchanged:

- `power36_initial_758.tsv` and `power36_regular_758.tsv` supply the original
  prefix and window calculations.
- `blank_bridge_receipts_758.tsv` supplies the seven-window extension to
  the [cut-52 checkpoint](blank_bridge_758.md).
- `power36_complete_receipts_758.tsv` supplies the 118-window extension to
  the [cut-623 checkpoint](power36_complete_prefix_758.md).

The [final receipt archive](power36_final_receipts_758.tsv) supplies all
**584** remaining windows. Its rows were generated from scratch by the
unchanged exponent-35 `cross_even_power_758.cpp` worker. They contain
**161,976,233 symbolic blocks** and
**243,595,031,059 normalized first-return evaluations**.

These evaluation counts describe verification work. They are neither the
number of first returns taken by the particular blank trajectory nor its
raw Turing-machine running time. The corresponding raw clock bounds are
computed separately in [the clock note](power36_clock_758.md).

The worker combines monotone same-word interval proofs with exact
propagation of the remaining possible resets. Its paired transition
formulas, binary residue tables, integer-size bounds and frontier
enclosures are those established in [EVEN_POWER_758.md](EVEN_POWER_758.md)
and [POWER36_FOLLOWON_758.md](POWER36_FOLLOWON_758.md). This extension adds
no new simulator rule or numerical approximation.

## From the final cut to the exact power-36 reset

Write $Q=3^{36}$ and $O=Q-76$. Across the gate corridor the complete odd and
even first-return words are, respectively,

$$
J^{35}LR,\qquad IJ^{35}LLJLLLR.
$$

The endpoint checks give positive odd reset gains bounded by 77 and 101.
The odd word holds through $O$; the even word holds through $O+79$. The
incoming strip at G lies far below the end of the deep corridor:

$$
G+5000<O-34(4\cdot36+40).
$$

Consequently every possible incoming reset reaches the gate exit set
enumerated by `gate_exits(36,1)`. This uses the established finite residue
cycle argument, not a prediction about which residue the blank machine
will choose. All **32** exits merge through **1,455 distinct first-return
edges** to the single reset $Q+112{,}032$. The gate verifier rechecks both
parity words, the deep-entry margin, the complete exit set, and this merger.

The result thus follows from the connected blank window chain and a
universal exact gate calculation. It applies to both encodings because
both blank orbits already reach S and then follow the same two-counter
dynamics.

## Reproduction and dependencies

Run in this directory:

```sh
python3 power36_final_758.py
c++ -O3 -std=c++17 -DPOWER_EXPONENT=35 cross_even_power_758.cpp -o /tmp/cross36
python3 power36_final_758.py --worker /tmp/cross36 --jobs 8
```

The default validates the four regular receipt archives, checks the six
initial crossings' endpoints and adjacency, recomputes all symbolic
endpoint certificates, proves complete coverage of the regular grid, and
replays the power-36 gate merger. Its `verify()` function returns the exact
target only after all these checks pass.

The command with `--worker` additionally regenerates **the 584 new final
receipts**, comparing every output field. The earlier blank proof and
receipt archives remain inherited proof dependencies; this command does
not regenerate them. Their respective notes give their independent replay
commands. The 118-row intermediate milestone remains separately replayable.

The unchanged worker's literal-counter audit can also be rerun:

```sh
c++ -O3 -std=c++17 -DPOWER_EXPONENT=35 audit_even_power_758.cpp -o /tmp/audit36
/tmp/audit36
```

This is an extension checked by the repository's integer verifiers. It
does not claim a new Coq formalization or settle eventual halting.
