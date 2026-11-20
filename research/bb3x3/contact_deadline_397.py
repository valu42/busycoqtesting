"""Verify two finite potential certificates for CONTACT_DEADLINE_397.md."""
from check_bb33 import H397
from regular_guard_397 import one_return

WIDTH = 10
CASES = (
    ((21, 1, 1, 21, 1, 1), (1, -7, -15, 2, -8, -8), 25),
    ((3, 21, 21, 3, 21, 21), (-29, -1, 3, -12, 2, 2), 3),
)


def transitions():
    for word in range(1 << WIDTH):
        for mode in range(len(H397.rules)):
            updated, outgoing = word, mode
            for index in range(WIDTH):
                bit = (word >> index) & 1
                new_bit, outgoing = H397.rules[outgoing][bit]
                updated ^= (bit ^ new_bit) << index
                if outgoing == -1:
                    break
            yield word, updated, mode, outgoing


def certificate(edges, weights):
    potential = [0] * (1 << WIDTH)
    silent = [(u, v, weights[m]) for u, v, m, out in edges if out == -1]
    for _ in range(len(potential)):
        changed = False
        for u, v, gain in silent:
            if potential[u] + gain > potential[v]:
                potential[v] = potential[u] + gain
                changed = True
        if not changed:
            break
    assert min(potential) == 0 and max(potential) == 31
    assert all(potential[v] >= potential[u] + gain for u, v, gain in silent)
    defect = max(weights[m] + potential[u] - potential[v]
                 for u, v, m, out in edges if out != -1)
    return defect


def main():
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    edges = list(transitions())
    for profile, weights, gain in CASES:
        assert sum(a * b for a, b in zip(profile, weights)) == gain
        defect = certificate(edges, weights)
        print(f"Base gain {gain}, potential range 31, maximum contact defect {defect}")
    initial = one_return(one_return(()))
    assert initial is not None and len(initial) == 18
    print("After two copies of S, exactly 18 new suffix bits are occupied.")


if __name__ == "__main__":
    main()
