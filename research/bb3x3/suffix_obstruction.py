"""Check the far-edge suffix obstruction for #531/#532 and #397."""
from itertools import product

from check_bb33 import H397, WILY


def pass_segment(model, bits, mode):
    """Process a segment, returning its updated bits and outgoing mode."""
    changed = list(bits)
    for i, bit in enumerate(bits):
        if mode == -1:
            break
        changed[i], mode = model.rules[mode][bit]
    return tuple(changed), mode


def lift_event(model, toggle, bits, target):
    """Starting on bits, supply an input stream emitting just target at the edge."""
    predecessors = [{row[bit][1]: (mode, row[bit][0])
                     for mode, row in enumerate(model.rules)} for bit in (0, 1)]
    requests = [target]
    for bit in reversed(bits):
        inputs = []
        for target_mode in requests:
            if target_mode not in predecessors[bit]:
                inputs.append(toggle)
                bit ^= 1
            mode, bit = predecessors[bit][target_mode]
            inputs.append(mode)
        requests = inputs
    return requests


def next_modes(model, possibilities):
    result = set()
    for mode in possibilities:
        if mode == -1:
            result.add(-1)
        else:
            result.update(outgoing for _, outgoing in model.rules[mode])
    return result


def through_cell(model, stream, bit):
    result = []
    for mode in stream:
        bit, outgoing = model.rules[mode][bit]
        if outgoing != -1:
            result.append(outgoing)
    return tuple(result)


def audit(model, toggle, free_bits):
    modes = set(range(len(model.rules)))
    assert model.rules[toggle] == ((1, -1), (0, -1))
    assert modes <= {out for row in model.rules for _, out in row}
    # After the indicated number of free prefix bits, check exact phase sets.
    if model is WILY:
        phase_sets = [modes | {-1}] * 2
    else:
        phase_sets = [{-1, 0, 3}, {-1, 1, 2, 4, 5}] * 2
    witnesses = []
    for p, start in enumerate(model.modes):
        available = {start}
        for _ in range(free_bits):
            available = next_modes(model, available)
        assert available == phase_sets[p]
        # One more free bit rotates the sets, so the bounds hold at every depth.
        assert next_modes(model, available) == phase_sets[(p + 1) % len(phase_sets)]
        assert -1 in available
        assert modes <= available | phase_sets[(p + 1) % len(phase_sets)]
        witnesses.append({pass_segment(model, w, start)[1]: w
                          for w in product(range(2), repeat=free_bits)})
        assert set(witnesses[-1]) == available
        # One actual period of passes, with no middle reselected inside it.
        stream = model.modes[p:] + model.modes[:p]
        streams = {stream}
        for _ in range(3 if model is WILY else 6):
            streams = {through_cell(model, s, bit) for s in streams for bit in (0, 1)}
        assert all((mode,) in streams for mode in modes)
    dangerous = next(i for i, extension in enumerate(model.extension) if extension is None)
    for width in range(8):
        for bits in product(range(2), repeat=width):
            for target in modes:
                word = bits
                stream = lift_event(model, toggle, word, target)
                assert 1 <= len(stream) <= 2**width
                for i, mode in enumerate(stream):
                    word, out = pass_segment(model, word, mode)
                    assert out == (target if i == len(stream) - 1 else -1)
            # Replay an actual phase-correct abstract counterexample, allowing
            # the untracked prefix to vary but fixing its exact length.
            for p in range(len(model.modes)):
                word = bits
                stream = lift_event(model, toggle, bits, dangerous)
                for index, desired in enumerate(stream):
                    if desired not in phase_sets[p]:
                        silent = witnesses[p][-1]
                        changed, out = pass_segment(model, silent + word, model.modes[p])
                        assert changed[free_bits:] == word and out == -1
                        p = (p + 1) % len(phase_sets)
                    prefix = witnesses[p][desired]
                    changed, out = pass_segment(model, prefix + word, model.modes[p])
                    word = changed[free_bits:]
                    p = (p + 1) % len(phase_sets)
                    assert out == (dangerous if index == len(stream) - 1 else -1)


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    audit(WILY, toggle=3, free_bits=3)
    audit(H397, toggle=1, free_bits=4)
    print("Verified the suffix obstruction for #531/#532 and #397.")
