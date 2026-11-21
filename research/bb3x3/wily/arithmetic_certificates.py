"""Exact certificates for arithmetic sections of the Wily Coyote pass.

Run with Python 3.10+; standard library only.  Words are read left-to-right,
which is least-significant-bit first for the *counter* encoded by rho.
This does NOT claim that the blank orbit has been decided.
"""
from dataclasses import dataclass
from itertools import product

# Modes a,b,c,d,e correspond to s0,s1,s2,s3,identity.
NEXT = ((1, 2), (3, 0), (2, 1), (4, 4), (4, 4))
OUTPUT = ((1, 0), (1, 0), (0, 1), (1, 0), (0, 1))
BOUNDARY = ('0', None, '1100', '00', '')


def pass_word(word, mode=0):
    output = []
    for char in word:
        bit = int(char)
        output.append(str(OUTPUT[mode][bit]))
        mode = NEXT[mode][bit]
    tail = BOUNDARY[mode]
    return None if tail is None else ''.join(output) + tail


def iterate(word, count, mode=0):
    for _ in range(count):
        word = pass_word(word, mode)
        if word is None:
            return None
    return word


def rho(bits):
    return ''.join('01' if b == '0' else '10' for b in bits)


def bits(n):
    assert n >= 0
    return bin(n)[:1:-1] if n else ''


def counter(n):
    """The canonical word R(n)=rho(binary_lsb(n))0, including R(0)=0."""
    return rho(bits(n)) + '0'


def E(n):
    return '0' + counter(n)


def prefix_action(prefix):
    """Exact section identity a(prefix+x)=output+P_mode(x)."""
    mode = 0
    output = []
    for char in prefix:
        bit = int(char)
        output.append(str(OUTPUT[mode][bit]))
        mode = NEXT[mode][bit]
    return ''.join(output), mode


def append_section(reduced, mode):
    """Chronological composition on a NONEMPTY tail.

    Replace a by d followed by c, using a=c o d on nonempty words.
    Cancel consecutive d's, since d^2=id on nonempty words.
    Other letters are retained; no unproved group relation is used.
    """
    for letter in ('dc', 'b', 'c', 'd', '')[mode]:
        if letter == 'd' and reduced and reduced[-1] == 'd':
            reduced.pop()
        else:
            reduced.append(letter)


def fixed_bits(value, width):
    assert 0 <= value < 1 << width
    return ''.join(str((value >> i) & 1) for i in range(width))


@dataclass(frozen=True)
class ReturnCertificate:
    width: int
    residue: int
    steps: int
    increment: int

    def verify(self, short_base=True):
        """Proves the universal prefix/section obligation by finite calculation.

        Also checks the one short canonical representative separately.  It is
        essential: padding high binary zeros changes the finite word.
        """
        k, r, t, delta = self.width, self.residue, self.steps, self.increment
        assert 0 <= r < (1 << k)
        prefix = '0' + rho(fixed_bits(r, k))
        reduced = []
        for _ in range(t):
            prefix, mode = prefix_action(prefix)
            append_section(reduced, mode)
        r_new = (r + delta) % (1 << k)
        j = (r + delta) // (1 << k)
        assert prefix == '0' + rho(fixed_bits(r_new, k))
        assert reduced == ['b'] * j
        if short_base:
            assert iterate(E(r), t) == E(r + delta)
        return {
            'width': k, 'residue': r, 'steps': t, 'increment': delta,
            'output_residue': r_new, 'tail_b_power': j,
            'short_base_checked': short_base,
        }


# Each row has a general arbitrary-tail certificate and its short canonical
# representative has been checked.  Thus every n>=0 in its residue class
# satisfies a^steps(E(n))=E(n+increment), with no intermediate halt.
CERTIFICATES = (
    ReturnCertificate(1, 1, 2, 3),
    ReturnCertificate(4, 4, 6, 21),
    ReturnCertificate(5, 8, 14, 69),
    ReturnCertificate(6, 2, 62, 429),
    ReturnCertificate(6, 16, 14, 69),
    ReturnCertificate(6, 24, 14, 69),
    ReturnCertificate(7, 14, 126, 1053),
    ReturnCertificate(7, 34, 62, 429),
    ReturnCertificate(7, 44, 22, 165),
    ReturnCertificate(7, 48, 30, 141),
    ReturnCertificate(7, 118, 94, 1221),
    ReturnCertificate(8, 64, 78, 741),
    ReturnCertificate(8, 76, 54, 549),
    ReturnCertificate(8, 78, 126, 1053),
    ReturnCertificate(8, 120, 126, 573),
    ReturnCertificate(8, 174, 126, 1245),
)


def check_auxiliary_algebra(max_length=10):
    """Finite regression checks, supplementary to the algebraic proofs."""
    for length in range(max_length + 1):
        for chars in product('01', repeat=length):
            w = ''.join(chars)
            # a o d = c holds even at the empty word.
            assert pass_word(pass_word(w, 3), 0) == pass_word(w, 2)
            if w:
                # c o d = a and d^2=id require a nonempty word.
                assert pass_word(pass_word(w, 3), 2) == pass_word(w, 0)
                assert pass_word(pass_word(w, 3), 3) == w
            left = pass_word(pass_word('10' + w, 2), 2)
            cw = pass_word(w, 2)
            right = None if cw is None else '10' + cw
            assert left == right
    for n in range(1024):
        assert pass_word(counter(n), 1) == counter(n + 1)
        assert pass_word('1' + counter(n), 2) == '1' + counter(n + 1)


def check_failed_conjectures():
    # A superficially plausible mod24 invariant fails during an excursion.
    w = E(146)
    assert 146 % 24 == 2
    assert iterate(w, 134) == '010111101010110110111111'
    assert iterate(w, 135) is None
    assert all(not (v and v[0] == '0' and len(v) % 2 == 0
                    and v[-1] == '0'
                    and all(v[i:i+2] in ('01', '10')
                            for i in range(1, len(v)-1, 2)))
               for v in (iterate(w, t) for t in range(1, 135)))
    # Padding cannot be erased. The symbolic rule below is valid for all
    # nonempty counter tails after the nineteen fixed digits, but not E434.
    padded_rule = ReturnCertificate(19, 434, 13694, 1994205)
    padded_rule.verify(short_base=False)
    assert iterate(E(434), 13694) != E(434 + 1994205)
    # A yet shorter boundary counterexample: canonical E10 halts in254 steps.
    assert iterate(E(10), 253) is not None
    assert iterate(E(10), 254) is None


def main():
    import json
    check_auxiliary_algebra()
    rows = [cert.verify() for cert in CERTIFICATES]
    check_failed_conjectures()
    print(json.dumps({'status': 'all checks passed',
                      'meaning': 'parameterized partial results, not a decision',
                      'return_certificates': rows,
                      'mod24_counterexample': {'n': 146, 'halt_step': 135}},
                     indent=2))


if __name__ == '__main__':
    main()
