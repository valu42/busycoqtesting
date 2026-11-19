"""Emit a finite SAT obstruction to a seven-state right-to-left #397 invariant."""
from argparse import ArgumentParser
from itertools import combinations
from pathlib import Path

from check_bb33 import H397, sweep

RETURN = tuple(ord(c) - ord('a') for c in 'bcbcbebcbcbcecbcbcbcffdfffffaffbc')


def one_return(word):
    for mode in RETURN:
        word = sweep(H397, word, mode)
        if word is None:
            break
    return word


def necessary_examples():
    positive = set()
    word = ()
    for index in range(8193):
        if index < 16 or index & (index - 1) == 0:
            positive.add(word)
        if index != 8192:
            word = one_return(word)
            assert word is not None
    negative = set()
    implications = []
    sample_path = Path(__file__).with_name('regular_guard_397.tsv')
    for line in sample_path.read_text().splitlines():
        kind, digits = line.split()
        word = tuple(map(int, digits))
        if kind == 'neg':
            value = word
            for _ in range(8):
                value = one_return(value)
                if value is None:
                    break
            assert value is None
            negative.add(word)
        else:
            assert kind == 'edge'
            target = one_return(word)
            if target is None:
                negative.add(word)
            else:
                implications.append((word, target))
    return positive, negative, implications


def make_cnf(positive, negative, implications, size=7):
    ids = {}
    clauses = []
    def variable(*key):
        return ids.setdefault(key, len(ids) + 1)

    states = range(size)
    def transition(i, bit, j):
        return variable('transition', i, bit, j)

    for i in states:
        for b in (0, 1):
            row = [transition(i, b, j) for j in states]
            clauses.append(row)
            clauses.extend([-x, -y] for x, y in combinations(row, 2))
            # Name reachable states by first discovery from state zero.
            position = 2 * i + b
            for j in range(1, size):
                if j > position + 1:
                    clauses.append([-row[j]])
                elif j > 1:
                    earlier = [transition(pos // 2, pos % 2, j - 1) for pos in range(position)]
                    clauses.append([-row[j], *earlier])

    all_words = positive | negative | {w for implication in implications for w in implication}
    suffixes = {word[i:] for word in all_words for i in range(len(word) + 1)}
    def reaches(word, i):
        return variable('reaches', word, i)

    clauses.append([reaches((), 0)])
    for word in sorted(suffixes):
        if not word:
            continue
        bit, suffix = word[0], word[1:]
        for i in states:
            for j in states:
                clauses.append([-reaches(suffix, i), -transition(i, bit, j), reaches(word, j)])
    def accepted(word):
        return variable('accepted', word)

    for w in sorted(all_words):
        for i in states:
            final = variable('final', i)
            clauses.append([-reaches(w, i), -final, accepted(w)])
            clauses.append([-reaches(w, i), final, -accepted(w)])
    clauses.extend([accepted(w)] for w in sorted(positive))
    clauses.extend([-accepted(w)] for w in sorted(negative))
    clauses.extend([-accepted(w), accepted(v)] for w, v in implications)
    return len(ids), clauses


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='destination for the DIMACS CNF')
    args = parser.parse_args()
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    positive, negative, implications = necessary_examples()
    variables, clauses = make_cnf(positive, negative, implications)
    with args.output.open('w') as output:
        print(f'p cnf {variables} {len(clauses)}', file=output)
        for clause in clauses:
            print(*clause, 0, file=output)
    print(f'{len(positive)} accepted, {len(negative)} rejected, {len(implications)} implications.')
    print(f'{variables} variables, {len(clauses)} clauses.')


if __name__ == '__main__':
    main()
