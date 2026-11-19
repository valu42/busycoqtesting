"""Identify the consecutive resets across the fourth #758 candidate pair."""
from check_bb33 import first_return
from check_fourth_gateway import K, LOW, verify_gateway
from power_gates_758 import coalesce
from terminal_forest_758 import exhaust, terminal

ENTRY = LOW - 100_000
MERGER = 17_354_320_242_846_420
LAST = K - 35
NEXT = K + 65


def verify_fourth():
    verify_gateway()
    root = terminal(K, 39)
    assert root == terminal(K+2, 39) == (11_620_229_829_445_098, 11_620_229_829_445_097)
    resets, nodes, depth = exhaust(root, 255)
    assert (resets, nodes, depth) == ({K: 38, K+2: 38}, 255, 43)

    seed, edges = coalesce(range(ENTRY, ENTRY+5_001), 7_963)
    assert (seed, edges) == (MERGER, 7_963)
    for _ in range(424):
        assert seed < LOW
        seed = first_return(seed, batch=False)
    assert seed == LOW+109
    seed = first_return(seed, batch=False)
    assert seed == LOW+208 and seed%2

    # The odd corridor's seven bulk moves give period 256 for the exact
    # gain. Jump only full cycles whose ending seed still lies below K+2.
    seen = {}
    calls = 0
    while seed%256 not in seen:
        seen[seed%256] = seed, calls
        seed = first_return(seed, batch=False)
        calls += 1
    base, prefix_calls = seen[seed%256]
    shift, period = seed-base, calls-prefix_calls
    assert (shift, period, prefix_calls) == (768, 8, 1)
    cycles = (K+2-seed)//shift
    assert cycles == 98_990_236_018
    seed += cycles*shift
    calls += cycles*period
    previous = seed
    while seed <= K+2:
        previous = seed
        seed = first_return(seed, batch=False)
        calls += 1
    assert (previous, seed, calls) == (LAST, NEXT, 791_921_888_157)
    return previous, seed


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable verification.")
    previous, seed = verify_fourth()
    print(f"All 5,001 incoming starts cross from {previous:,} to {seed:,}.")
