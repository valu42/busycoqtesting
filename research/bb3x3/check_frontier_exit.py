"""Verify the exits of the #758 frontier certified by cover_frontier.cpp."""
from check_bb33 import first_return


def verify():
    upper = 1_080_000_000_000_000
    bound = 801
    checkpoint = 1_080_000_000_055_450
    exits = set()
    for seed in range(upper - bound + 1, upper + 1):
        result = first_return(seed, batch=False)
        assert result is not None and seed < result <= seed + bound
        if result > upper:
            exits.add(result)
    assert len(exits) == 47
    linked = {checkpoint}
    for c in sorted(exits):
        history = []
        while c not in linked:
            history.append(c)
            result = first_return(c, batch=False)
            assert result is not None and c < result <= checkpoint
            c = result
        linked.update(history)
    assert len(linked) - 1 == 2_175
    print(f"{len(exits)} exits, {len(linked) - 1:,} edges, checkpoint {checkpoint:,}")


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    verify()
