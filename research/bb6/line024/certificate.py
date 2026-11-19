"""Print the finite Lean proof for the counter phase starting at move 20,656,445."""
from functools import cache

# All but the last entry are digits. The last entry is the tail index.
START = (4, 2, 1, 1, 1, 2, 1, 1, 8, 1, 1, 8, 4, 4, 3, 1, 0, 1, 0, 0)


def term(x):
    return "(word [" + ",".join(map(str, x[:-1])) + f"] {x[-1]})"


class Certificate:
    def __init__(self):
        self.lines = []
        self.sequence = 0

    def lemma(self, statement, proof):
        self.sequence += 1
        name = f"segment{self.sequence}"
        self.lines.append(f"private theorem {name} : {statement} := by\n  have h := {proof}\n  exact h")
        return name

    @cache
    def one(self, x):
        """Construct one timed core pass, or leave the boundary to its caller."""
        n = x[0]
        rest = x[1:]
        if not rest:
            y, cost, proof = (n, 0), 14*n+54, f"Atom.tip {n}"
        elif n == 0:
            return None
        elif (suffix := self.one(rest)) is not None:
            end, t, name = suffix
            y, cost, proof = (n,)+end, t+14*n+4, f"Atom.keep {n-1} {name}"
        elif len(x) >= 4 and x[1:3] == (1, 0):
            if x[3:] == (0,):
                y = (n+1,)
                proof = f"Atom.mergeTail {n-1}"
            elif len(x) >= 5 and x[3] == 1:
                y = (n+2,)+x[4:]
                proof = f"Atom.mergeDigit {n-1} {term(x[4:])}"
            else:
                return None
            cost = 14*n+18
        elif n >= 2 and rest == (0, 0):
            y, cost, proof = (n-2, 1, 1, 0), 14*n+72, f"Atom.split {n-2}"
        elif n >= 2 and len(x) >= 4 and x[1:3] == (0, 1):
            suffix = self.one(x[3:])
            if suffix is None:
                return None
            end, t, name = suffix
            y, cost, proof = (n-2, 1, 2)+end, t+14*n+36, f"Atom.carry {n-2} {name}"
        else:
            return None
        name = self.lemma(f"Atom {term(x)} {term(y)} {cost}", proof)
        return y, cost, name

    @cache
    def until_boundary(self, x):
        """Reuse a whole suffix proof under a positive digit, then handle its boundary."""
        w = x
        parts = []
        passes = cost = 0
        if len(x) > 1 and x[0] > 0:
            end, k, t, name = self.until_boundary(x[1:])
            if k:
                w = (x[0],)+end
                parts.append(f"(frame {x[0]-1} {name})")
                passes, cost = k, t+k*(14*x[0]+4)
        atom = self.one(w)
        if atom is not None:
            y, t, name = atom
            parts.append(f"(atomSeries {name})")
            w, k, rest_cost, rest = self.until_boundary(y)
            if k:
                parts.append(rest)
            passes += 1+k
            cost += t+rest_cost
        if not parts:
            return x, 0, 0, None
        proof = parts[0]
        for part in parts[1:]:
            proof = f"(concat {proof} {part})"
        name = self.lemma(f"Series {term(x)} {term(w)} {passes} {cost}", proof)
        return w, passes, cost, name


def main():
    cert = Certificate()
    endpoint, passes, cost, proof = cert.until_boundary(START)
    assert endpoint == (0, 1)+(2,)*19+(3, 0, 1, 1, 0)
    assert passes == 6132267261786
    print("import Timing\nimport Entry\n\nnamespace H7846.Line24\nopen Word\n")
    print("\n\n".join(cert.lines))
    print(f"\ndef endWord := {term(endpoint)}")
    print(f"theorem phase : Series startWord endWord {passes} {cost} := {proof}")
    print("\nend H7846.Line24")


if __name__ == "__main__":
    main()
