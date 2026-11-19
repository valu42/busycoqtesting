"""Emit ordinary-atom proofs with exact right-tape consumption."""
from functools import cache

from certificate import Certificate, term
from explore import phase


class SharpCertificate(Certificate):
    @cache
    def prefix(self, word, count):
        """Compress the first count passes, retaining their ordinary atom derivations."""
        assert 0 < count <= phase(word)[1]
        current, used, cost, proof = word, 0, 0, None
        for kind, source, digit in phase(word)[4]:
            n = min(count-used, 1 if kind == "atom" else phase(source)[1])
            if kind == "atom":
                current, elapsed, atom = self.one(source)
                part = f"(sharpAtom {atom})"
            else:
                current, elapsed, part = self.prefix(source, n)
                if kind == "frame":
                    current = (digit,) + current
                    elapsed += n*(14*digit+4)
                    part = f"(sharpFrame {digit-1} {part})"
            proof = part if proof is None else f"(sharpConcat {proof} {part})"
            used += n
            cost += elapsed
            if used == count:
                break
        assert used == count
        name = self.lemma(f"SharpSeries {term(word)} {term(current)} {count} {cost}", proof)
        return current, cost, name


def main():
    start = (1,3,1,1,4,2,2,4,4,3,1,0,1,0,0)
    count = 35996031
    cert = SharpCertificate()
    end, cost, proof = cert.prefix(start, count)
    assert end == (1,2,2,3,3,2,2,3,1,8) and cost == 17045820218
    print("import SharpPhase\nimport Entry\nnamespace H7846.Line24\nopen Word")
    print("\n\n".join(cert.lines))
    print(f"theorem sharpThirdPhase : SharpSeries {term(start)} {term(end)} {count} {cost} := {proof}")
    print("end H7846.Line24")


if __name__ == "__main__":
    main()
