"""Classify 36-return halts from an empty suffix and any nonnegative counter."""
from collections import deque
from return596 import next_boundary


def shortest():
    distance, queue, predecessors = {'': 0}, deque(['']), {}
    terminal = []
    checked = 0
    while queue:
        word = queue.popleft()
        depth = distance[word]
        if depth >= 36:
            continue
        for r in range(3):
            kind, n, tail, _ = next_boundary(300 + r, word, clock=False, affine=True)
            checked += 1
            if kind == 'halt':
                terminal.append((depth + 1, word, r))
                continue
            assert n >= 400
            if tail not in distance:
                distance[tail] = depth + 1
                queue.append(tail)
            if distance[tail] == depth + 1:
                predecessors.setdefault(tail, []).append((word, r, n - 400))

    def paths(word):
        if not word:
            yield ()
        else:
            for prev, r, add in predecessors[word]:
                for path in paths(prev):
                    yield path + ((r, add),)

    # On the first j selected residues the current integer is
    # b + 4^j * t when the initial integer is a + 3^j * t.
    classes = []
    for depth, word, r in terminal:
        assert depth == 36
        for path in paths(word):
            a = b = 0
            p3 = p4 = 1
            for digit, add in path + ((r, 0),):
                d = (digit - b) % 3  # 4^j is 1 modulo 3
                a += p3 * d
                b = 4 * ((b + p4 * d) // 3) + add
                p3 *= 3
                p4 *= 4
            classes.append(a)
    assert len(classes) == len(set(classes))
    # The affine rows use n >= 300. Check the remaining finite starts directly.
    for n in range(300):
        counter, tail = n, ''
        for j in range(1, 37):
            kind, counter, tail, _ = next_boundary(counter, tail, clock=False)
            if kind == 'halt':
                assert j == 36 and n in classes
                break
        else:
            assert n not in classes
    return checked, len(distance), terminal, sorted(classes)


if __name__ == '__main__':
    import sys
    rows, tails, stops, classes = shortest()
    print('Verified affine rows:', rows, '| tail words:', tails)
    print('First possible halting return:', min(d for d, _, _ in stops))
    print('Number of classes:', len(classes), '| modulus:', 3**36, '| least representative:', classes[0])
    if '--list' in sys.argv:
        for n in classes:
            print(n)
