#!/usr/bin/env python3
"""Check an earlier #758 terminal and two short intervals that lead to it.

Set K = 12,966,580,636,926,693,791,014,052. Each of the 53 resets in
[K-26,353, K-26,301] and each of the 53 in [K-25,997, K-25,945] reaches
the same terminal. Every reset in [K-72,881, K-52,882] passes K+2 alive.

The reverse search shows that the terminal's only possible last resets are
K and K+2. Hence a blank orbit reaching it must skip the 20,000-seed miss
interval between consecutive resets, a jump of at least 20,001 in c.
Mass a+2c increases by at most 9 per map call, so this requires at least
4,445 calls in that excursion. The calculation leaves this possibility open.

Run beside check_bb33.py and terminal_forest_758.py with Python 3.10+.
"""
from itertools import groupby

from check_bb33 import first_return
from terminal_forest_758 import exhaust, terminal


K = 12_966_580_636_926_693_791_014_052
LOW, HIGH = K - 72_881, K + 2


def main():
    if not __debug__:
        raise SystemExit("run without -O to enable the verification checks")

    target = terminal(K, 67)
    assert target == (8_644_387_091_284_462_527_342_804,
                      8_644_387_091_284_462_527_342_803)
    assert terminal(K + 2, 67) == target
    assert exhaust(target, 603) == ({K: 66, K + 2: 66}, 603, 69)

    # Descending induction. A first return within the window already has a
    # verdict. A return above it has passed both possible last resets forever.
    hits = bytearray(HIGH - LOW + 1)
    for seed in range(HIGH, LOW - 1, -1):
        index = seed - LOW
        if seed in (K, K + 2):
            hits[index] = 1
            continue
        successor = first_return(seed, batch=False)
        assert successor is not None and successor > seed
        if successor <= HIGH:
            hits[index] = hits[successor - LOW]

    assert sum(hits) == 17_340
    assert hits.index(1) == 20_000
    longest_gapless_runs = []
    for reaches, indices in groupby(range(len(hits)), key=hits.__getitem__):
        if reaches:
            left = next(indices)
            right = max(indices, default=left)
            if right - left + 1 >= 53:
                longest_gapless_runs.append((LOW + left, LOW + right))
    assert longest_gapless_runs == [(K - 26_353, K - 26_301),
                                    (K - 25_997, K - 25_945)]
    print("Exactly 17,340 of 72,884 reset seeds reach this terminal. "
          "The two longest runs contain 53 seeds each.")
    print("All 20,000 resets from K-72,881 through K-52,882 pass K+2 alive.")


if __name__ == "__main__":
    main()
