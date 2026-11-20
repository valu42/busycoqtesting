# A further connected blank checkpoint for #758 and #153

Both blank runs reach

\[
A(1,100\,583\,090\,198\,237\,340).
\]

This is a finite extension of the established doubled-power-35 blank proof.
It does **not** establish halting or nonhalting from blank. The connection to
the power-36 gate and the distant halting basin remains open.

## What the new computation adds

The existing regular-window archive, together with the symbolic endpoint
checks, already connects the doubled-power checkpoint to grid cut 28,
`100343090198154948`. Its exact merger reaches reset
`100343090198273147`. The prose in `POWER36_FOLLOWON_758.md` reports an earlier
checkpoint; the existing checker reproduces this farther archived prefix.

The seven new rows in [blank_bridge_receipts_758.tsv](blank_bridge_receipts_758.tsv)
certify windows 28, 30, 31, 32, 33, 34, and 51. All intervening windows have
the common-word endpoint certificates already checked by
`power36_followon_758.py`. The chain therefore reaches every cut through 52,
whose lower endpoint is `100583090198154948`.

Each row guarantees that every incoming reset in its 5,001-seed strip reaches
an even reset in its recorded output strip. Each output strip lies inside the
next window's input strip. Thus the statement follows by composing the
universal crossing statements, starting from the blank checkpoint proved in
[DOUBLED_POWER35_758.md](DOUBLED_POWER35_758.md). No arbitrary choice of one
possible exit is used.

At cut 52, normalize all 5,001 possible incoming seeds using the proved
75-or-77 odd return. Advancing the smallest remaining even seed and merging
equal successors gives one reset, `100583090198237340`, after 3,688 distinct
normalized even-to-even edges. The new checker recomputes this merger using
the original `first_return` counter rules. The narrower output strip of
window 51 merges to the same reset in 1,390 unnormalized first-return edges.

The new rows were computed using the unchanged exponent-35 C++ worker. They
contain 1,510,685 symbolic crossing blocks and 2,221,926,673 normalized return
evaluations in total. The resulting known grid has 4,129 of 4,831 windows
certified, leaving **702** open. Its first open window is 52. These counts
refer to the fixed regular grid; many certified windows above the connected
prefix are still conditional on reaching their entrance.

## Verification

Run in this directory:

```sh
python3 blank_bridge_758.py
c++ -O3 -std=c++17 -DPOWER_EXPONENT=35 cross_even_power_758.cpp -o /tmp/cross36
python3 blank_bridge_758.py --worker /tmp/cross36 --replay
c++ -O3 -std=c++17 -DPOWER_EXPONENT=35 audit_even_power_758.cpp -o /tmp/audit36
/tmp/audit36
```

The default checks every receipt's shape and adjacency, recomputes the
symbolic certificates for the intervening windows, and replays the final
full-strip merger. `--replay` independently regenerates the seven new
crossing rows, retaining the earlier blank proof and archived windows as
dependencies. The unchanged worker's audit completed on 1,179,648 even
inputs, 1,179,648 adjacent odd inputs, and 100,020 complete crossing inputs.

The progression from the previous archived exact checkpoint is
239,999,999,964,193 in the reset parameter. This difference is neither a
first-return count nor a raw Turing-machine running time. No new raw-clock
bound is claimed here.
