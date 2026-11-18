"""Generate the six-phase grammar and replay the integer left-front certificate."""

from itertools import product
from pathlib import Path
import subprocess
import sys

from line36_tiles import PIECES, PREFIX, advance
from prior_sweeps import PARITY, TapeMachine, direct_epoch, word_sweep


def phases():
    choices = list(product((0, 1), repeat=6))
    prefix = PREFIX
    tiles = [''.join(PIECES[k][b] for k, b in enumerate(bits)) for bits in choices]
    original = tiles.copy()
    rows = []
    for _ in range(6):
        pieces = {}
        for bits, tile in zip(choices, tiles):
            position = 0
            for k, b in enumerate(bits):
                length = len(PIECES[k][b])
                piece = tile[position:position + length]
                assert pieces.setdefault((k, b), piece) == piece
                position += length
            assert position == len(tile)
        for k in range(6):
            left, right = pieces[k, 0], pieces[k, 1]
            assert "2" in left and "2" in right
            assert not left.startswith(right) and not right.startswith(left)
        following, tiles, minimum, header = advance(prefix, tiles)
        rows.append((prefix, pieces, header))
        prefix = following
    assert tiles == original and prefix == PREFIX
    assert [r[2] for r in rows] == [6, 1, 1, 6, 1, 1]
    return rows


def check_density(rows):
    # The score of an interval is length minus twice its signed balance.
    maximum = 0
    min_shield = None
    for _, pieces, _ in rows:
        for start in range(6):
            for bits in product((0, 1), repeat=7):
                parts = [pieces[(start+j) % 6, b] for j, b in enumerate(bits)]
                period = ''.join(parts[:6])
                assert period.count('2') * 3 - period.count('1') <= -4
                # Four complete pieces shield older inputs from the finite
                # debt range even after any next-piece prefix and three twos.
                shield = ''.join(parts[:4])
                balance = shield.count('1') - shield.count('2')
                min_shield = balance if min_shield is None else min(min_shield, balance)
                for digit in parts[4]:
                    balance += 1 if digit == '1' else -1
                    min_shield = min(min_shield, balance)
                assert sum(map(len, parts[:5])) <= 143
                score = 0
                for digit in ''.join(parts):
                    score = max(0, score + (3 if digit == '2' else -1))
                    maximum = max(maximum, score)
    assert min_shield == 49
    assert maximum == 22
    print('Every tiled interval has length minus twice its balance at most 22.', flush=True)


def check_seed():
    data = Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt').read_text()
    assert data.splitlines()[35] == PARITY
    machine = TapeMachine(PARITY)
    word = []
    for _ in range(331):
        word, _ = word_sweep(word, PARITY)
        assert word is not None and direct_epoch(machine, (1, 2)) == word
    assert (machine.steps, machine.head) == (612_729, -871)
    text = ''.join(map(str, word))
    tiles = [''.join(parts) for parts in product(*PIECES)]
    cursor = len(PREFIX)
    assert text.startswith(PREFIX)
    count = 0
    while cursor < 530:
        tile = next(t for t in tiles if text.startswith(t, cursor))
        cursor += len(tile)
        count += 1
    assert count == 3
    assert cursor == 530 and len(text) == 1035 and text[cursor:cursor+3] == '111'
    assert text.rindex('2', 0, cursor) == 529 and text.rindex('2') == 1031
    labels = [text.rindex('2', 0, cursor) % 2]
    labels += [i % 2 for i in range(cursor, len(text)) if text[i] == '2']
    labels.append((len(text) - 1) % 2)
    assert sum(a != b for a, b in zip(labels, labels[1:])) == 7
    print('Blank epoch 331: 612729 literal steps, head -871, width 1035, cut 530, switch count 7.', flush=True)


def main():
    if len(sys.argv) not in (2, 3) or (len(sys.argv) == 3 and sys.argv[2] != '--projected'):
        raise SystemExit('Pass the path to the compiled line36_left executable, optionally followed by --projected.')
    rows = phases()
    check_density(rows)
    check_seed()
    tokens = []
    for prefix, pieces, header in rows:
        tokens.extend([prefix, str(header)])
        for k in range(6):
            tokens.extend([pieces[k, 0], pieces[k, 1]])
    subprocess.run(sys.argv[1:], input='\n'.join(tokens) + '\n', text=True, check=True)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled')
    main()
