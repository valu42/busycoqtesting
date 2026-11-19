"""Independent exact check for eventual ordinary periods; Python 3.10+."""
from argparse import ArgumentParser
from fractions import Fraction
from math import gcd

LIMIT = 14_984_528
PAIR = ((5,20), (9,35), (7,26), (7,29))


def directions(limit):
    """Append older blocks to a suffix. Every mixed cycle has a J followed by P."""
    modulus = 1
    while modulus <= limit**2:
        modulus *= 3
    inv4 = pow(4, -1, modulus)
    found = {}
    tested = set()

    def reconstruct(residue):
        # r q - M h = k, 0 < k < q/2.  Hence h/q is strictly closer
        # to r/M than any other rational with denominator at most limit.
        closest = Fraction(residue, modulus).limit_denominator(limit)
        q = closest.denominator
        k = residue*q - modulus*closest.numerator
        if not 0 < 2*k < q or gcd(q,6) != 1 or gcd(k,q) != 1 or (q,k) in tested:
            return
        start = k
        path = []
        while (q,k) not in tested:
            tested.add((q,k))
            path.append(k)
            if 3*k > q and 2*k < q:
                k = 3*k-q
            elif 9*k < 2*q and k%4 == 0:
                k = 9*k//4
            else:
                return
        # Both branches are injective and their output residues mod 3 differ.
        if k == start:
            i = path.index(min(path))
            found[q,path[i]] = path[i:]+path[:i]

    def suffix(scale, offset):
        if scale == 0:
            reconstruct(offset)
            return
        suffix(3*scale % modulus, (offset-scale) % modulus)
        suffix(9*scale*inv4 % modulus, offset)

    suffix(27*inv4 % modulus, -9*inv4 % modulus)
    return found


def exclude(q, cycle):
    """Bound e from the past, then obtain the exact invariant subset by deletion."""
    choices = []
    for i in range(len(cycle)):
        parent = i
        past = []
        modulus = 1
        pairs = 0
        while modulus <= 7*q:
            previous = (parent-1) % len(cycle)
            jump = 3*cycle[previous] > q
            modulus *= 3 if jump else 9
            pairs += not jump
            past.append((cycle[parent],jump))
            parent = previous
        choices.append((pairs, len(past), i, past))
    _, _, ref, reverse_past = min(choices)
    residues = {0}
    modulus = 1
    for k, jump in reversed(reverse_past):
        if jump:
            modulus *= 3
            residues = {(3*r+q-2*k) % modulus for r in residues}
        else:
            modulus *= 9
            inverse = pow(4,-1,modulus)
            residues = {((9*r+q*b)*inverse-k*v) % modulus
                        for r in residues for v,b in PAIR}
    possible = {-((-r) % modulus) for r in residues}
    possible = {e for e in possible if e >= -7*q}
    successor = {}
    order = cycle[ref:]+cycle[:ref]
    for initial in possible:
        e = initial
        for k, after in zip(order, order[1:]+order[:1]):
            if 3*k > q:
                e = 3*e+q-2*after
            else:
                v,b = PAIR[(q*e) % 4]
                num = 9*e+q*b
                assert num % 4 == 0
                e = num//4 - after*v
            if not -7*q <= e <= 0:
                break
        else:
            if e in possible:
                successor[initial] = e
    while possible:
        image = {successor[e] for e in possible if e in successor}
        if image == possible:
            raise AssertionError((q, order[0], min(image)))
        possible = image


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--limit',type=int,default=LIMIT)
    args = parser.parse_args()
    if not __debug__ or not 1 <= args.limit <= LIMIT:
        parser.error('enable assertions and select a supported positive limit')
    cycles = directions(args.limit)
    for (q,k),cycle in cycles.items():
        exclude(q,cycle)
    if args.limit == LIMIT:
        assert len(cycles) == 400
    print(f'{len(cycles)} coarse cycles through denominator {args.limit:,}; '
          'every bounded deviation set emptied.')
