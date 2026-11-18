"""Check the six-phase symbolic tilings and their finite blank-orbit prefixes."""

from itertools import product
from pathlib import Path

from prior_sweeps import PARITY, TapeMachine, direct_epoch, word_sweep


PREFIX = "22211111221112111111111212"
PIECES = (
    ("112111211121112121211111112", "1112111211121112121211111112"),
    ("11122121212121212111112111", "111212121212121212111112111"),
    ("11212211111111111111121112121", "112121211111111111111121112121"),
    ("121111121111111111111212121", "1121111121111111111111212121"),
    ("11221211121211111111111211", "112121211121211111111111211"),
    ("11122111112121112111111111212", "111212111112121112111111111212"),
)


def survivors(word):
    """Match closing 2s against preceding opening 1s."""
    bits = [False] * len(word)
    debt = 0
    for i in reversed(range(len(word))):
        if word[i] == "2":
            debt += 1
        elif debt:
            debt -= 1
        else:
            bits[i] = True
    return bits, debt


def derivative(bits, previous):
    digits = []
    for bit in bits:
        digits.append("2" if previous != bit else "1")
        previous = bit
    return "".join(digits)


def advance(prefix, tiles):
    prefix_bits, deficit = survivors(prefix)
    successor, minimum = word_sweep(list(map(int, prefix)), PARITY)
    assert successor is not None and minimum == -deficit
    output = "".join(map(str, successor))
    if prefix_bits[-1]:
        assert output[-1] == "2"
        output = output[:-1]     # finite right-edge carry
    next_prefix = output[:len(prefix)]
    overlap = output[len(prefix):]
    assert overlap

    new_tiles = []
    for tile in tiles:
        bits, debt = survivors(tile)
        assert debt == 0 and bits[-1] == prefix_bits[-1]
        assert 84 <= sum(bits) <= 90
        encoded = derivative(bits, prefix_bits[-1])
        assert encoded.endswith(overlap)
        following = overlap + encoded[:-len(overlap)]
        assert len(following) == len(tile)
        # Check the entire one-tile finite identity against the original sweep.
        exact, low = word_sweep(list(map(int, prefix + tile)), PARITY)
        carry = "2" if bits[-1] else ""
        assert low == minimum
        assert "".join(map(str, exact)) == next_prefix + following + overlap + carry
        new_tiles.append(following)
    return next_prefix, new_tiles, minimum, len(overlap)


def matched_prefix(word, prefix, tiles):
    """Return full tiles and the additional matched part of the next tile."""
    if not word.startswith(prefix):
        return 0, 0
    i = len(prefix)
    count = 0
    while match := next((t for t in tiles if word.startswith(t, i)), None):
        count += 1
        i += len(match)
    partial = 0
    for tile in tiles:
        bound = min(len(tile), len(word) - i)
        n = next((j for j in range(bound) if word[i+j] != tile[j]), bound)
        partial = max(partial, n)
    return count, i + partial


def main():
    data = Path(__file__).with_name("BB2x5_Rocq_holdouts_37.txt").read_text()
    assert data.splitlines()[35] == PARITY
    tiles = ["".join(choice) for choice in product(*PIECES)]
    assert len(set(tiles)) == 64 and {len(t) for t in tiles} == set(range(164, 171))
    assert not any(a.startswith(b) for a in tiles for b in tiles if a != b)
    phase_prefix, phase_tiles = PREFIX, tiles
    guards, overlaps = [], []
    for _ in range(6):
        phase_prefix, phase_tiles, low, overlap = advance(phase_prefix, phase_tiles)
        guards.append(low)
        overlaps.append(overlap)
    assert phase_prefix == PREFIX and phase_tiles == tiles
    assert guards == [-3, -2, 0, -3, -2, 0] and overlaps == [6, 1, 1, 6, 1, 1]
    print("64 tiles of lengths 164 to 170 return in six symbolic sweeps.")

    machine = TapeMachine(PARITY)
    samples = {25: (0, 31, 66), 127: (1, 199, 389),
               1201: (11, 1979, 3790), 2005: (19, 3319, 6336)}
    word = []
    for epoch in range(1, max(samples) + 1):
        word, _ = word_sweep(word, PARITY)
        assert word is not None
        if epoch <= 127:
            assert word == direct_epoch(machine, (1, 2))
        if epoch in samples:
            text = "".join(map(str, word))
            count, matched = matched_prefix(text, PREFIX, tiles)
            assert (count, matched, len(word)) == samples[epoch]
            print(f"Blank epoch {epoch}: {count} full tiles, "
                  f"{matched} matching cells in a word of length {len(word)}.")
        if epoch == 127:
            assert (machine.steps, machine.head) == (89_229, -327)
            print("Literal epoch 127: 89,229 defined transitions, head at -327.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled")
    main()
