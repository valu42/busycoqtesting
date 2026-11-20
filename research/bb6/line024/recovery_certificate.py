"""Construct the wall-stack return after the old debris becomes a counter."""
from certificate import Certificate


def main():
    word = (2,)*19 + (3,0,1,1,0)
    cert = Certificate()
    width = 2
    older = []
    stages = []
    elapsed = 0
    while True:
        end, count, cost, proof = cert.until_boundary(word)
        elapsed += cost+15*count
        stages.append((proof,width,older))
        if end == (1,0,0):
            widths = [0,1+3*count+width] + older
            landing = elapsed+38
            elapsed = landing+27+sum(22+k for k in widths)
            break
        assert end[:3] == (1,0,1)
        older = [1+3*count+width] + older
        width = 2
        elapsed += 35
        word = end[3:]
    assert len(stages) == 22 and landing == 11472711550734861
    def nums(xs):
        return "[" + ",".join(map(str,xs)) + "]"
    print("import StackInvariant\nimport DebrisContact\nnamespace H7846.Line24\nopen TM Word")
    print("\n\n".join(cert.lines))
    print(f"def debrisWidths : List Nat := {nums(widths)}")
    print(f"theorem recoveryStack : StackPhases survivingWord 2 [] {elapsed} debrisWidths := by")
    for i in reversed(range(len(stages))):
        proof,w,ws = stages[i]
        if i+1 == len(stages):
            print(f"  have p{i} := StackPhases.last {proof} {w} {nums(ws)}")
        else:
            print(f"  have p{i} := StackPhases.next (w := {w}) (ws := {nums(ws)}) {proof} p{i+1}")
    print("  exact p0")
    print(f"theorem debrisRenewal (L : Tape) : steps {5717374479490900+elapsed} "
          "(guardedVisit L postStackWord 18396649123346 (rep 4 [true] debris)) = "
          "some (regenerated debrisWidths (debrisExterior L)) := by")
    print("  have a := debrisCounter L\n  rw [afterDebrisShape] at a\n"
          "  have h := steps_seq trans a (recoveryStack.execute (debrisExterior L))\n  exact h")
    print("#print axioms debrisRenewal\nend H7846.Line24")


if __name__ == "__main__":
    main()
