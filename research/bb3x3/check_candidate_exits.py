"""Trace the narrow incoming windows across three known halting-seed pairs."""
from check_bb33 import first_return

CASES = (
    (1_326_438_094_216_110, (50,), 6_808),
    (2_031_355_966_425_479, (3, 9, 13, 19, 25, 29, 35, 41, 45, 51, 57, 61, 67, 73, 77), 44_461),
    (3_335_436_339_933_243, (140,), 11_454),
)


def trace(candidate):
    cut = candidate - 199_000
    outputs = {}
    exits = set()
    for seed in range(cut, cut + 5_001):
        path = []
        while seed < candidate + 3 and seed not in outputs:
            path.append(seed)
            result = first_return(seed, batch=False)
            assert result is not None and result > seed
            seed = result
        crossing = outputs[seed] if seed in outputs else (path[-1], seed)
        for entry in path:
            outputs[entry] = crossing
        exits.add(crossing[1] - candidate)
    if candidate == CASES[0][0]:
        assert set(outputs.values()) == {(candidate - 17, candidate + 50)}
    if candidate == CASES[2][0]:
        assert set(outputs.values()) == {(candidate - 96, candidate + 140)}
    return tuple(sorted(exits)), len(outputs)


def verify():
    for k, expected, edges in CASES:
        assert trace(k) == (expected, edges)
        print(f"{k:,}: {len(expected)} exits, {edges:,} first-return edges")


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit("Run without -O to enable checks.")
    verify()
