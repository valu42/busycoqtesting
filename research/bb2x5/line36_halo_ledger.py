"""Audit the three-cell-halo switch charge in both physical and word coordinates."""

from itertools import groupby, product

from line36_tiles import PIECES, PREFIX, advance, survivors
from prior_sweeps import PARITY, word_sweep


def changes(labels):
    return sum(a != b for a, b in zip(labels, labels[1:]))


def anchored(word, start, dummy):
    labels = [dummy] + [(start + i) % 2 for i, digit in enumerate(word) if digit == "2"]
    return changes(labels + [(start + len(word) - 1) % 2])


def cancellation(cap):
    tail = cap.split("2", 1)[1]
    bits, debt = survivors(tail)
    odd = sum(len(list(g)) % 2 for bit, g in groupby(bits) if bit)
    return anchored(tail, 0, 1) - debt - odd


def charge(y, old, final, debt, before_survives, first_survives):
    # Output labels here have already been normalized by subtracting h and adding one.
    middle = (y + 1) % 2
    if first_survives:
        assert debt == 0
        known = [final] if before_survives else [final, middle]
        return changes(known + [old])
    last = (y + debt - 1) % 2
    e = int(old != (y - 1) % 2)
    low = max(0, debt - e)
    if low % 2 != (old != last):
        low += 1
    assert low == (debt - e if debt else e)
    known = [final, middle] if before_survives else [final]
    return changes(known + [last]) - low


def audit_tails(max_length=13):
    counts = [0, 0, 0]
    for length in range(2, max_length + 1):
        for digits in product("12", repeat=length):
            tail = "".join(digits)
            bits, debt = survivors(tail)
            # At each old cap cut, the leftmost 2 determines its cancellation.
            valid_caps = [tail[j:] for j in range(length)
                          if "2" in tail[j:] and any(bits[j:])]
            if not valid_caps:
                continue
            c = max(map(cancellation, valid_caps))
            case = 0 if bits[0] else (1 if debt == 0 else 2)
            for y, old, final in product(range(2), repeat=3):
                budget = anchored(tail, y, old)
                for before in ([False] if debt else [False, True]):
                    fee = charge(y, old, final, debt, before, bits[0])
                    labels = [final]
                    prev = before
                    for j, bit in enumerate(bits):
                        if prev != bit:
                            labels.append((y + j + 1) % 2)
                        prev = bit
                    if bits[-1]:
                        labels.append((y + length + 1) % 2)
                    # The new word has h additional header cells plus the append.
                    # Undo h and add one, including when the terminal cell is an append.
                    labels.append((y + length + bits[-1]) % 2)
                    assert changes(labels) <= budget + fee + (not bits[-1]) - c
                    counts[case] += len(valid_caps)
    return counts


def audit_full_sweeps():
    prefix = PREFIX
    tile = "".join(p[1] for p in PIECES)
    checked = 0
    for _ in range(6):
        next_prefix, images, _, header = advance(prefix, [tile])
        for offset in (0, 3, 14, 27):
            common = prefix + tile[:offset]
            x = len(common)
            for digits in product("12", repeat=3):
                halo = "".join(digits)
                y = x + len(halo)
                for suffix in product("12", repeat=5):
                    tail = "".join(suffix)
                    bits, debt = survivors(tail)
                    if "2" not in tail or not any(bits):
                        continue
                    text = common + halo + tail
                    actual, _ = word_sweep(list(map(int, text)), PARITY)
                    if actual is None:
                        continue
                    image = "".join(map(str, actual))
                    # Some short test prefixes can change the incoming debt at the
                    # header. Use the actual header length for every successful case.
                    h = len(image) - len(text) - int(bits[-1])
                    known = image[:h + y]
                    old_left = text.rindex("2", 0, x) % 2
                    old_labels = [old_left] + [i % 2 for i in range(x, y) if text[i] == "2"]
                    before = text[y-1] == "1" and debt == 0
                    for pos in (max(4, x - 6), x + h - 2, x + h):
                        if pos <= 0 or pos > len(known) - 3 or "2" not in known[:pos]:
                            continue
                        new_left = known.rindex("2", 0, pos) % 2
                        known_labels = [(new_left - h + 1) % 2]
                        known_labels += [(i - h + 1) % 2 for i in range(pos, len(known))
                                         if known[i] == "2"]
                        fee = changes(known_labels) - changes(old_labels)
                        fee += charge(y, old_labels[-1], known_labels[-1], debt, before, bits[0])
                        old_budget = anchored(text[x:], x, old_left)
                        new_budget = anchored(image[pos:], pos, new_left)
                        assert new_budget <= old_budget + fee + (not bits[-1]) - cancellation(tail)
                        checked += 1
        prefix, tile = next_prefix, images[0]
    return checked


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled")
    counts = audit_tails()
    print(f"Local tail/cap/parity checks, E empty or nonempty at zero or positive debt: {counts}")
    print(f"Full sweep and variable-cut checks: {audit_full_sweeps()}")
