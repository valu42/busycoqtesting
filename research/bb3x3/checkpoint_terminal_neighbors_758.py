"""Check for direct halts at the boundaries of words seen near secondary-cusp mergers."""
from functools import lru_cache

from angular_lift_obstruction_758 import P, REPRESENTATIVE, Y, checkpoints
from check_bb33 import HALTING_TARGET as H, champion_step
from check_confluence import itinerary

GAINS = (5, 9, 7, 7)
SHIFTS = (20, 35, 26, 29)
PACK = 6
MASK = 4**PACK - 1


def pair_table():
    table = []
    for residue in range(MASK+1):
        d, gain = residue, 0
        for _ in range(PACK):
            r = d % 4
            gain += GAINS[r]
            d = (9*d + SHIFTS[r]) // 4
        table.append((d, gain))
    return table


TABLE = pair_table()


@lru_cache(maxsize=200000)
def odd_path(seed):
    """Return the exact postlaunch blocks, last action and next reset if present."""
    u = seed + 584
    d = (u-P) // 2
    assert seed % 2 and P <= u <= 3*P-3
    parts = []
    count = 0
    while count < 1000:
        right, left = 2*d+1, 2*u-4*d-1
        if left == 1:
            return ''.join(parts), 'Z', right
        if left <= right:
            h = u-2*d
            # The size estimate is only a starting index for the two exact tests.
            k = max(1, ((u//h).bit_length()*81)//128)
            while 3**k*h > u+2*k:
                k -= 1
            while 3**(k+1)*h <= u+2*k+2:
                k += 1
            assert k > 0
            u += 2*k
            d = (u-3**k*h)//2
            parts.append('J'*k)
            count += k
            continue

        small, growth = TABLE[d & MASK]
        dest = (d >> (2*PACK))*9**PACK + small
        if 2*dest+1 < u+growth:
            d, u = dest, u+growth
            parts.append('P'*PACK)
            count += PACK
            continue
        r = d % 4
        dest, new_u = (9*d+SHIFTS[r])//4, u+GAINS[r]
        if 2*dest+1 < new_u:
            d, u = dest, new_u
            parts.append('P')
            count += 1
            continue

        first = champion_step(left, right)
        if first is None:
            return ''.join(parts), 'immediate halt', None
        a, c = first
        if c == 1:
            return ''.join(parts), 'E', None
        second = champion_step(a, c)
        if second is None:
            return ''.join(parts), 'H', None
        if second[0] == 1 and a <= c:
            return ''.join(parts), 'R', second[1]
        if second[0] == 1:
            return ''.join(parts)+'P', 'Z', second[1]
        raise AssertionError('failed to classify the final pair')
    raise AssertionError('replay budget exceeded')


def even_next(seed):
    a, c = 4*(P//3)-1, seed-2*(P//3)+587
    assert seed % 2 == 0 and c > 0
    while a != 1:
        a, c = champion_step(a, c)
    return c


def extend(node, levels):
    if levels:
        for letter in 'JP':
            extend(node.setdefault(letter, {}), levels-1)


def sampled_words(starts):
    trie, complete = {}, set()
    odd_count = 0
    for i, start in enumerate(starts):
        seed = start
        for j in range(32):
            if seed % 2 == 0:
                seed = even_next(seed)
                continue
            word, kind, successor = odd_path(seed)
            assert kind in ('H', 'R')
            if j == 0 and i % 31 == 0:
                literal, _ = itinerary(seed)
                assert 'J'+literal == 'J'*292 + word.replace('P', 'LL') + 'L' + kind
            odd_count += 1
            complete.add(word)
            node = trie
            for letter in word:
                node = node.setdefault(letter, {})
            if successor is None:
                break
            seed = successor
    assert (len(starts), odd_count, len(complete)) == (735, 17399, 3918)
    for word in complete:
        assert word.startswith('PPPPJ')
        node = trie
        for letter in word:
            node = node[letter]
        extend(node, 3)
    return trie


def append(matrix, letter):
    # If the downstream strip is (A,D,L,U), its preimage has coefficients
    # (a*A+b*D, den*D, r*L+la*A+ld*D, r*U+ua*A+ud*D).
    a, b, den, r, la, ld, ua, ud = matrix
    if letter == 'J':
        return a, a+3*b, 3*den, r, la+2*r, la+3*ld-r, ua+2*r, ua+3*ud-r
    return 4*a, 9*b, 9*den, 4*r, 4*la+36*r, 9*ld-35*r, 4*ua+20*r, 9*ud-20*r


def search(trie):
    words, multi_run, visits = 0, 0, 0
    distinct, hits = set(), set()
    stack = [(trie, (1,0,1,1,0,0,0,0), '')]
    while stack:
        node, matrix, word = stack.pop()
        for letter, child in node.items():
            stack.append((child, append(matrix, letter), word+letter))
        if not word.startswith('PPPPJ'):
            continue
        words += 1
        multi_run += word.count('PJ') >= 3
        a, b, den, r, la, ld, ua, ud = matrix
        # Apply the inverse composition to the direct-terminal strip
        # -17 <= 9*d - 2*u <= -10, then substitute launch d=(u-P)/2.
        slope, denominator = 2*a+9*b, 9*den
        low, high = -17*r+2*la+9*ld, -10*r+2*ua+9*ud
        q = denominator-2*slope
        lower = max(Y, -((-(P*denominator+2*low))//q)-584)
        upper = min(H, (P*denominator+2*high)//q-584)
        for seed in range(lower+(lower%2 == 0), upper+1, 2):
            visits += 1
            distinct.add(seed)
            actual, kind, _ = odd_path(seed)
            if actual == word and kind == 'H':
                hits.add(seed)
    assert (words, multi_run, visits, len(distinct)) == (121480, 52950, 338709, 313475)
    assert hits == {H-2, H}
    print(f'{words:,} classes, {multi_run:,} with at least three jump runs, '
          f'{len(distinct):,} distinct origins; only H-2 and H halt on the specified words.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    search(sampled_words([REPRESENTATIVE, Y, H, *checkpoints()]))
