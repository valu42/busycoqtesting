"""Compare the complete angular join to direct integer iteration on small grids."""

import csv
from pathlib import Path
import subprocess
import sys


def exact_length(numerator, denominator):
    a, q, length = numerator, denominator, 0
    while True:
        if 3*a < q:
            a, length = 3*a, length+1
        elif 9*a > 5*q:
            a, q, length = 9*a-5*q, 4*q, length+2
        else:
            return length


def direct_tails(power, threshold):
    result = {}
    denominator = 4**power
    for numerator in range(5, denominator, 10):
        length = exact_length(numerator,denominator)
        if length >= threshold:
            result[numerator] = length
    return result


def check_ledger():
    path = Path(__file__).with_name('dyadic_long_tails_758.tsv')
    with path.open() as stream:
        reader = csv.DictReader(stream,delimiter='\t')
        rows = [(int(row['p']),int(row['numerator']),int(row['length'])) for row in reader]
    assert rows and rows == sorted(set(rows))
    for p,n,length in rows:
        assert 0 < n < 4**p and n%10 == 5
        assert length >= 189 and exact_length(n,4**p) == length
    print(f'All {len(rows)} recorded long tails agree with direct integer iteration.')


def main():
    check_ledger()
    executable = Path(sys.argv[1] if len(sys.argv)>1 else './dyadic_tail_join').resolve()
    for p, half_length, threshold in ((6,4,24), (8,5,39), (9,6,47)):
        expected = direct_tails(p,threshold)
        assert expected
        for bits in (12,32):
            rows = subprocess.check_output(
                [executable, str(p), str(half_length), str(threshold), str(bits)],
                text=True
            ).splitlines()
            got = {}
            for row in rows[1:]:
                tag, reported_p, numerator, length = row.split()
                assert tag == 'long_tail' and int(reported_p) == p
                assert int(numerator) not in got
                got[int(numerator)] = int(length)
            assert got == expected
            assert int(rows[0].split()[-1]) == len(expected)
        print(f'p={p}: both grids match all {len(expected)} tails of length at least {threshold}')


if __name__ == '__main__':
    main()
