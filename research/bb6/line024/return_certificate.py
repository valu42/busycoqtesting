"""Generate the 13 counter phases ending at the first exposed tail after restart."""
from certificate import Certificate, term

START = (2, 1, 3, 1, 1, 2, 2, 4, 4, 3, 1, 0, 1, 0, 0)


def main():
    cert = Certificate()
    stages = []
    word = START
    while True:
        end, k, core, proof = cert.until_boundary(word)
        assert end[:2] == (1, 0)
        stages.append((word, end, core + 15*k, proof, k))
        if len(end) == 3:
            break
        word = end[3:]
    print("import StackInvariant\nnamespace H7846.Line24\nopen TM Word")
    print("\n\n".join(cert.lines))
    print("attribute [local irreducible] Exits")
    elapsed = 0
    for i in reversed(range(len(stages))):
        x, y, cost, proof, _ = stages[i]
        j = y[2]
        if i == len(stages)-1:
            elapsed = cost + 26 + 3*(j+4)
            after = f"exitTip {j}"
        else:
            elapsed += cost + 32 + 3*j
            after = f"exitDigit {j} return{i+1}"
        print(f"theorem return{i} : Exits {term(x)} {elapsed} := by\n  "
              f"have h := exitSeries {proof} ({after})\n  exact h")
    assert len(stages) == 13 and elapsed == 22596910528
    widths = [8628, 1320]
    width = 2120
    elapsed = 0
    chain = []
    def nums(xs):
        return "[" + ",".join(map(str, xs)) + "]"
    for i, (_, _, cost, proof, k) in enumerate(stages):
        if i+1 == len(stages):
            chain.append(f"StackPhases.last {proof} {width} {nums(widths)}")
            widths = [0, 1+3*k+width] + widths
            elapsed += cost + 38 + 27 + sum(22+m for m in widths)
        else:
            chain.append(f"StackPhases.next (w := {width}) (ws := {nums(widths)}) {proof} p{i+1}")
            widths = [1+3*k+width] + widths
            width = 2
            elapsed += cost + 35
    assert elapsed == 22749656804
    print(f"def returnedWidths : List Nat := {nums(widths)}")
    print(f"theorem returnStack : StackPhases {term(START)} 2120 [8628,1320] {elapsed} returnedWidths := by")
    for i in reversed(range(len(chain))):
        print(f"  have p{i} := {chain[i]}")
    print("  exact p0")
    print(f"theorem regenerate (L : Tape) : steps {elapsed} "
          f"(visitX (stackBase 2120 [8628,1320] L) [] {term(START)}.tape) = "
          f"some (regenerated returnedWidths L) := returnStack.execute L")
    print("theorem returnedWidthsAligned : ∀ m ∈ returnedWidths, m % 3 = 0 := by")
    print("  apply returnStack.aligned (by decide)\n  intro m hm\n"
          "  simp only [List.mem_cons,List.not_mem_nil,or_false] at hm\n"
          "  rcases hm with rfl | rfl <;> decide")
    print("end H7846.Line24")


if __name__ == "__main__":
    main()
