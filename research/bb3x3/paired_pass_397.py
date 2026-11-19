"""Check the two-mode pair rewrite and one-pass halting language for #397."""
from itertools import product

from check_bb33 import H397, sweep


def paired_pass(word, mode=0):
    """Apply ca (0) or cd (3) to a finite bit word, without prepending a bit."""
    assert mode in (0, 3)
    result = list(word)
    stop = len(word) - len(word) % 2
    for i in range(0, stop, 2):
        left, right = word[i:i + 2]
        if mode == 0:
            result[i:i + 2] = 1 - left, 1 - right
            if left == 1:
                return tuple(result)
        mode = 0 if left == right else 3
    if stop == len(word):
        return tuple(result) + ((1,) if mode == 0 else (0, 0, 1))
    if word[-1] == 0:
        return None
    ending = (0, 0, 1) if mode == 0 else (1, 1, 0, 0, 1)
    return tuple(result[:-1]) + ending


def halts_on_pass(word):
    """Recognize the one-pass halting language, without writing any tape bits."""
    if len(word) % 2 == 0 or word[-1] == 1:
        return False
    previous_equal = True
    for i in range(0, len(word) - 1, 2):
        left, right = word[i:i + 2]
        if previous_equal and left == 1:
            return False
        previous_equal = left == right
    return True


def audit():
    for length in range(14):
        count = 0
        for word in product((0, 1), repeat=length):
            a, d = (sweep(H397, word, mode) for mode in (0, 3))
            assert paired_pass(word) == a
            assert paired_pass(word, mode=3) == d
            assert (None if a is None else sweep(H397, a, 0)) == d
            assert halts_on_pass(word) == (a is None)
            count += a is None
        if length % 2 == 0:
            expected = 0
        else:
            pairs = length // 2
            expected = 1 if pairs == 0 else 2 * 3**(pairs - 1)
        assert count == expected
    for length in range(9):
        for word in product((0, 1), repeat=length):
            dangerous = len(word) % 2 == 1 and word[-1] == 0
            for _ in range(2 ** (length // 2)):
                updated = paired_pass(word)
                if updated is None:
                    break
                if not dangerous:
                    assert len(updated) % 2 == 0 or updated[-1] == 1
                word = updated
            assert (updated is None) == dangerous
    word = H397.seed
    for _ in range(256):
        accelerated = paired_pass(word)
        assert accelerated is not None and accelerated == sweep(H397, word, 0)
        word = (0,) + accelerated


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    audit()
    print("Checked the pair rules, cd = ca squared, and one-pass halting counts.")
