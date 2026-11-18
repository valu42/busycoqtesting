"""A halting three-digit-count twin of a genuine line-26 blank checkpoint."""
from collections import Counter
from column_tick import raw_tick, tick


def verified_tick(word):
    image = tick(word)
    assert image == raw_tick(word)
    return image


def main():
    ordinary = tuple(map(int, '002311332320312000000000000000'))
    twin = tuple(map(int, '000000000000002323120311332000'))
    word = (2, 1)  # First aligned upper word, derived in column-phases.md.
    for _ in range(1, 144):
        word = verified_tick(word)
    assert word == ordinary
    assert ordinary[:2] == twin[:2] and ordinary[-2:] == twin[-2:]
    assert Counter(zip(ordinary, ordinary[1:], ordinary[2:])) == Counter(
        zip(twin, twin[1:], twin[2:]))
    word = twin
    for _ in range(2134):
        word = verified_tick(word)
        assert word is not None
    assert verified_tick(word) is None
    print("The trigram twin of blank tick 144 reaches B3 on its 2135th tick.")


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    main()
