"""Replay the exact local counts near the large halting pair using the original map."""
from argparse import ArgumentParser
from check_bb33 import HALTING_TARGET, first_return

KNOWN = {100: 2, 1_000: 6, 10_000: 284, 100_000: 16_102,
         1_000_000: 434_304, 5_000_000: 3_837_489}


def counts(radius):
    lower = HALTING_TARGET-2
    hit = bytearray(radius+3)
    population = 0
    for index in range(len(hit)):
        d = index-2
        seed = lower-d
        successor = first_return(seed)
        if successor is None:
            assert d in (-2,0)
            hit[index] = 1
        else:
            assert successor > seed
            previous_index = HALTING_TARGET-successor
            if previous_index >= 0:
                hit[index] = hit[previous_index]
        population += hit[index]
        if d in KNOWN:
            assert population == KNOWN[d]
            print(f'{population:,} of {index+1:,} reset starts halt before passing H.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--radius', type=int, choices=KNOWN, default=10_000)
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with assertions enabled')
    counts(args.radius)
