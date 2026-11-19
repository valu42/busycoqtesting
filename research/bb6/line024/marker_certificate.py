"""Generate a bounded-reach certificate from the next counter entry to the third marker."""
from functools import cache

from certificate import Certificate, term
from explore import phase

START = (1, 3, 1, 1, 4, 2, 2, 4, 4, 3, 1, 0, 1, 0, 0)
STOP = (1, 2, 2, 3, 3, 2, 2, 3, 1, 1, 1, 1, 2, 3, 0, 0)


class GuardedCertificate(Certificate):
    @cache
    def prefix(self, word, count):
        """Prove the first count passes in the unbounded phase decomposition."""
        current = word
        used = cost = reach = 0
        proof = None
        for kind, src, digit in phase(word)[4]:
            available = 1 if kind == "atom" else phase(src)[1]
            n = min(available, count-used)
            if kind == "atom":
                current, elapsed, atom = self.one(src)
                far = elapsed+15
                part = f"(guardAtom {atom})"
            else:
                current, elapsed, far, name = self.prefix(src, n)
                if kind == "frame":
                    current = (digit,) + current
                    overhead = 14*digit+4
                    elapsed += n*overhead
                    far += overhead
                    part = f"(guardFrame {digit-1} {name})"
                else:
                    part = name
            proof = part if proof is None else f"(guardConcat {proof} {part})"
            reach = max(reach, 3*used+far)
            used += n
            cost += elapsed
            if used == count:
                break
        assert count > 0 and used == count
        name = self.lemma(f"GuardSeries {term(word)} {term(current)} {used} {cost} {reach}", proof)
        return current, cost, reach, name


def main():
    cert = GuardedCertificate()
    count = 35995893
    end, cost, reach, proof = cert.prefix(START, count)
    assert end == STOP and cost+15*count == 17585693583 and reach <= 107988195
    print("import GuardedPhase\nimport Entry\nnamespace H7846.Line24\nopen Word")
    print("\n\n".join(cert.lines))
    print(f"theorem nearMarkerPhase : GuardSeries {term(START)} {term(end)} "
          f"{count} {cost} {reach} := {proof}")
    print("end H7846.Line24")


if __name__ == "__main__":
    main()
