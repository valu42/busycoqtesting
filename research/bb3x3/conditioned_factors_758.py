"""Check an exponent-constrained cusp row and its complete modular return graph."""

from math import gcd, isqrt, lcm


def high_flags(word, exponent, domain):
    power = pow(3, exponent, 4 * domain)
    flags, codes = [], {}
    for z in range(domain):
        u = 2 * z + 1 + 2 * exponent
        d = (u - power) // 2
        code = count = 0
        for instruction in word:
            if instruction == 'J':
                d, u = 3*d - u + 1, u + 2
            else:
                residue = d % 4
                gain = (5, 9, 7, 7)[residue]
                correction = (20, 35, 26, 29)[residue]
                d, u = (9*d + correction) // 4, u + gain
                count += (gain - 5) // 2
                code = 4*code + residue
        flags.append(count + d % 2)
        assert codes.setdefault(code, z % (domain // 2)) == z % (domain // 2)
    assert len(codes) == domain // 2
    return flags


def cycles(mapping):
    complete = set()
    for origin in range(len(mapping)):
        if origin in complete:
            continue
        local = {}
        current = origin
        while current not in complete and current not in local:
            local[current] = len(local)
            current = mapping[current]
        if current in local:
            yield list(local)[local[current]:]
        complete.update(local)


def main():
    progression, a, domain = 60, 34, 2 * 4**7
    k, j = 7, 1
    h = (1 - 5*(k+1)//2 - j - a) % gcd(progression, domain)
    C = j + h + 5*(k+1)//2
    m = next(v for v in range(a, lcm(progression, domain), progression)
             if (v + C) % domain == 1)
    step = lcm(progression, 8 * domain)
    word = 'P'*7 + 'J'*(h + j)
    flags = high_flags(word, m, domain)
    assert flags == high_flags(word, m + step, domain)
    gain = [m + C + b for b in flags]
    assert all(1 <= g % domain <= 2*k+2 for g in gain)
    graph = [(z + g) % domain for z, g in enumerate(gain)]
    loops = list(cycles(graph))
    assert all(len(loop)*(2*k+2) >= domain for loop in loops)
    prime = 65537
    assert all(prime % d for d in range(2, isqrt(prime) + 1))
    avoid = set()
    for loop in loops:
        length = len(loop)
        initial = sum(gain[z] for z in loop)
        avoid.add(-initial * pow(length * step, -1, prime) % prime)
    change = next(i for i in range(prime) if i not in avoid)
    for loop in loops:
        winding = sum(gain[z] for z in loop) + change * step * len(loop)
        assert winding % domain == 0 and gcd(winding, prime**2) == 1
    print("Domain", domain, "cycle lengths", [len(x) for x in loops],
          "integer windings invertible modulo", prime**2)


if __name__ == '__main__':
    main()
