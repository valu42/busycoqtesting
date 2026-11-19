"""Generate the checked three-marker passage used by FourthWindow.lean.

The final one at coordinate ANCHOR lets FourthWindow replace the tape
beginning there with any continuation. The physical move count and new
anchor position are verified by Lean, independently of the search.
"""
import sys
from pathlib import Path

from epoch_certificate import declarations, large_jump
from explore import advance
from sharp_certificate import SharpCertificate
from stack_certificate import pack


ANCHOR = 123_000_000_000
OUTER = ((1, 5), (0, 1), (1, 2), (0, 1), (1, 3))
FRONT = ((0, 1324), (1, 6), (0, 8628), (1, 6), (0, 137382804), (1, 6))


def generate(path):
    front = FRONT + ((0, ANCHOR - sum(n for _, n in FRONT)), (1, 1))
    state = OUTER, front, 0
    states, legs = [state], []
    cert = SharpCertificate()
    elapsed = last = head = 0

    def close_literals():
        nonlocal last
        if last < elapsed:
            states.append(state)
            legs.append((elapsed-last, None))
            last = elapsed

    while True:
        left, right, q = state
        a, b, s, n, dx, rule = advance(left, right, q)
        following = a, b, s
        if n >= 65536:
            close_literals()
            proof = large_jump(cert, left, right, n, dx, rule)
            legs.append((n, proof))
            states.append(following)
            last = elapsed+n
        state = following
        head += dx
        elapsed += n
        if s == 0 and a == OUTER and b[:2] == FRONT[:2]:
            break
    close_literals()
    assert elapsed == 122546899564 and head == -48
    assert b[-1] == (1, 1) and sum(n for _, n in b[:-1]) == ANCHOR-head
    label = "FourthPassage"
    lines = declarations(path, label, cert.lines)
    lines.extend(f"def p{i} : Pack := {pack(p)}" for i, p in enumerate(states))
    lines.append("attribute [local irreducible] TM.steps Pack.toCfg")
    for i, (n, proof) in enumerate(legs):
        lines.append(f"private theorem leg{i} : H7846.steps {n} p{i}.toCfg = some p{i+1}.toCfg := by")
        lines.append(f"  have h := {proof}\n  exact h" if proof else "  apply runSound\n  decide +native")
    lines.append(f"def finalPack := p{len(legs)}")
    lines.append(f"theorem passage : H7846.steps {elapsed} p0.toCfg = some finalPack.toCfg := by")
    lines.append("  have h0 := leg0")
    for i in range(1, len(legs)):
        lines.append(f"  have h{i} := steps_seq trans h{i-1} leg{i}")
    lines.extend([f"  exact h{len(legs)-1}", f"end H7846.Line24.{label}"])
    (path/(label+".lean")).write_text("\n".join(lines)+"\n")


if __name__ == "__main__":
    generate(Path(sys.argv[1]))
