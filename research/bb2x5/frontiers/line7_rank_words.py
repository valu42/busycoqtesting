"""Find suffixes of the first exceptional rank that halt inside a finite known tape window."""
import argparse
import itertools
from collections import Counter
from pathlib import Path

from checkpoints import atomic_json
from line7 import MACHINE, RULES


def local_halt(phases):
    # At the instant of V's A exit the suspended twos contain 3, 4, 0 for
    # ternary phases 0, 1, 2. A leading pair in V guarantees its first cell is 2.
    cells = bytearray((3, 4, 0)[int(d)] for d in phases)
    x = len(cells)-1
    cells.append(2)
    state, steps = 'A', 0
    seen = set()
    while 0 <= x < len(cells):
        config = x, state, bytes(cells)
        if config in seen:
            return None
        seen.add(config)
        rule = RULES.get((state, cells[x]))
        if rule is None:
            return {'ternary_suffix': phases, 'residue': int(phases, 3), 'steps_after_A': steps,
                    'halt_offset_from_V': x-len(phases), 'final_word': ''.join(map(str, cells))}
        cells[x], move, state = rule
        x += move
        steps += 1
    return None


def enumerate_words(width):
    if width < 1:
        raise ValueError('expected positive suffix width')
    # Extend only words without a previously certified shorter suffix.
    free = ['']
    hits = []
    for _ in range(width):
        longer = []
        for digit, suffix in itertools.product('012', free):
            word = digit+suffix
            result = local_halt(word)
            if result is None:
                longer.append(word)
            else:
                hits.append(result)
        free = longer
    modulus = 3**width
    by_length = Counter(len(h['ternary_suffix']) for h in hits)
    covered = modulus-len(free)
    if covered != sum(n*3**(width-size) for size, n in by_length.items()):
        raise ValueError('overlapping halt certificates')
    return {'machine': MACHINE, 'maximum_width': width, 'modulus': modulus,
            'covered_residues': covered, 'counts_by_width': dict(sorted(by_length.items())),
            'certificates': hits}


def rank_certificate(k, rank, width=8):
    """Check only the observed rank's low ternary digits, shortest witness first."""
    suffix = ''
    for _ in range(min(k, width)):
        rank, digit = divmod(rank, 3)
        suffix = str(digit)+suffix
        hit = local_halt(suffix)
        if hit is not None:
            return hit
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--width', type=int, default=8)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result = enumerate_words(args.width)
    atomic_json(args.output, result)
    print(f"{len(result['certificates'])} certificates cover {result['covered_residues']} "
          f"residues modulo {result['modulus']}.")
