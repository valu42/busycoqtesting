"""Construct a simultaneous odd/even first-return interval using exact rationals."""

from fractions import Fraction


def launch_threshold(b, k):
    return b * 3**k - 4 * (b - 1) - 2 * k


def launch_groups(lower, upper):
    cuts = {lower, upper}
    for b in (1, 2):
        k = 0
        while launch_threshold(b, k) < upper:
            threshold = launch_threshold(b, k)
            if lower < threshold:
                cuts.add(threshold)
            k += 1
    ordered = sorted(cuts)
    return max(zip(ordered, ordered[1:]), key=lambda interval: interval[1] - interval[0])


def find_gap(lower, upper):
    """Return a central part of a complementary Cantor gap and its address."""
    width = upper - lower
    center = (lower + upper) / 2
    origin, size = Fraction(0), Fraction(1)
    word = []
    while True:
        gap_lower = origin + size / 3
        gap_upper = origin + 5 * size / 9
        if size <= width / 4 or gap_lower < center < gap_upper:
            left, right = max(lower, gap_lower), min(upper, gap_upper)
            margin = (right - left) / 4
            result = (left + margin, right - margin)
            assert result[1] - result[0] >= width / 108
            assert min(result[0] - gap_lower, gap_upper - result[1]) >= width / 216
            return result, ''.join(word), (gap_lower, gap_upper)
        if center <= gap_lower:
            size /= 3
            word.append('J')
        else:
            origin = gap_upper
            size *= Fraction(4, 9)
            word.append('P')


def parity_window(lower, upper, b):
    k = 0
    while launch_threshold(b, k + 1) < upper:
        k += 1
    assert launch_threshold(b, k) <= lower
    h, shift = b * 3**k, 4 * (b - 1) + 2 * k
    lo, hi = Fraction(h, upper + shift), Fraction(h, lower + shift)
    (zlo, zhi), word, (glo, ghi) = find_gap(lo, hi)
    assert (lower + shift) * min(zlo - glo, ghi - zhi) > 18
    narrowed = h / zhi - shift, h / zlo - shift
    assert lower < narrowed[0] < narrowed[1] < upper
    assert narrowed[1] - narrowed[0] >= (upper - lower) / 972
    return narrowed, 'I' * (b - 1) + 'J' * k + word.replace('P', 'LL') + 'LR'


def common_window(start, width):
    if start < 1 or width < 10**9:
        raise ValueError('start must be positive and width must be at least one billion')
    interval = launch_groups(Fraction(2 * start + width, 2), Fraction(start + width))
    interval, odd = parity_window(*interval, 1)
    interval, even = parity_window(*interval, 2)
    lo, hi = interval
    assert hi - lo >= Fraction(width, 10**7)
    return -(-lo.numerator // lo.denominator), hi.numerator // hi.denominator, odd, even


if __name__ == '__main__':
    from scale_clauses_758 import H, check_word

    examples = [(1, 10**9), (3**80, 10**9), (H - 10**120, 10**112),
                (H - 10**42, 10**42), (H - 10**20, 10**20)]
    for start, width in examples:
        lo, hi, odd, even = common_window(start, width)
        for parity, word in ((1, odd), (0, even)):
            for point in (lo, (lo + hi) // 2, hi - 1):
                seed = point + (parity - point) % 2
                if lo <= seed <= hi:
                    check_word(seed, word)
        print(f'input width {width}, certified {hi-lo+1} seeds, '
              f'odd/even calls {len(odd)}/{len(even)}')
