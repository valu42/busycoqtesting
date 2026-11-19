"""Emit independently checkable Lean chunks for the next return to the same left exterior.

Usage: python3 epoch_certificate.py BUILD_DIRECTORY. Compile EpochPart*.lean
in numeric order, then EpochReturn.lean. All intermediate tapes are exact.
"""
import sys
from pathlib import Path

from explore import advance, decode, drop, encode, phase, rules
from sharp_certificate import SharpCertificate
from stack_certificate import second, tape, pack, START_TIME, END_OFFSET


def large_jump(cert, left, right, n, dx, rule):
    if rule == "passes":
        x = decode(drop(right, 2))
        k = dx//3
        end, cost, proof = cert.prefix(x, k)
        assert cost+15*k == n
        ext = drop(right, 2+sum(w for _,w in encode(x)))
        g, rest = (ext[0][1],ext[1:]) if ext else (3*k+len(end)-len(x),())
        return f"packedSharp {proof} {tape(left[1:])} {g} {tape(rest)} (by decide)"
    if rule == "older wall":
        width = left[2][1]
        return f"packedOld {width-2} {tape(drop(left,width+4))} {tape(drop(right,4))}"
    if rule == "empty wall":
        width = left[1][1]
        return f"packedEmpty {width-1} {tape(drop(left,width+2))} {tape(drop(right,3))}"
    if rule == "erase ones":
        return f"packedErase {n-1} {tape(drop(left,n))} {tape(drop(right,1))}"
    raise ValueError(rule)


def declarations(path, label, lemmas):
    """Keep a single unexpectedly large pass DAG out of the elaborator's working set."""
    imports = "import PackedPhase\nimport PackedWalls\nimport Entry"
    header = f"namespace H7846.Line24.{label}\nopen TM Word PackedTape\nset_option maxRecDepth 20000"
    if len(lemmas) <= 4000:
        return [imports, header, *lemmas]
    # Private names belong to the defining module. Export the intermediate
    # theorems inside this chunk's namespace for later supports to reuse.
    for start in range(0, len(lemmas), 1000):
        name = f"{label}Support{start//1000:03d}"
        block = [text.removeprefix("private ") for text in lemmas[start:start+1000]]
        source = [imports, header, *block, f"end H7846.Line24.{label}"]
        (path / (name+".lean")).write_text("\n".join(source)+"\n")
        imports = f"import {name}"
    return [imports, header]


def write_chunk(path, index, cert, states, legs):
    label = f"EpochPart{index:03d}"
    parts = declarations(path, label, cert.lines)
    parts += [f"def p{i} : Pack := {pack(s)}" for i,s in enumerate(states)]
    parts.append("attribute [local irreducible] TM.steps Pack.toCfg")
    for i,(steps,proof) in enumerate(legs):
        claim = f"private theorem leg{i} : H7846.steps {steps} p{i}.toCfg = some p{i+1}.toCfg := by"
        body = f"  have h := {proof}\n  exact h" if proof else "  apply runSound\n  decide +native"
        parts.append(claim+"\n"+body)
    parts.append(f"def finalPack := p{len(legs)}")
    parts.append(f"theorem passage : H7846.steps {sum(t for t,_ in legs)} p0.toCfg = some finalPack.toCfg := by")
    parts.append("  have h0 := leg0")
    for i in range(1,len(legs)):
        parts.append(f"  have h{i} := steps_seq trans h{i-1} leg{i}")
    parts.extend([f"  exact h{len(legs)-1}",f"end H7846.Line24.{label}"])
    (path / (label+".lean")).write_text("\n".join(parts)+"\n")
    return label


def main(path):
    state = second()
    exterior = state[0]
    offset = head = operations = chunk = last = 0
    names, legs, states = [], [], []
    cert = SharpCertificate()
    while True:
        if offset == END_OFFSET:
            states = [state]
            last = offset
        returning = (states and head == -48 and state[2] == 0 and state[0] == exterior
                     and state[1][:2] == ((0,1324),(1,6)))
        if states and (len(cert.lines) >= 2200 or len(legs) >= 56 or returning):
            if last < offset:
                states.append(state)
                legs.append((offset-last,None))
                last = offset
            names.append(write_chunk(path, chunk, cert, states, legs))
            shard_size = len(cert.lines)
            print(f"{names[-1]}: {len(legs)} checked legs, {shard_size} rewrite lemmas, move {START_TIME+offset}",flush=True)
            chunk += 1
            states, legs = [state], []
            cert.one.cache_clear()
            cert.prefix.cache_clear()
            cert = SharpCertificate()
            if returning:
                break
        left, right, state_id = state
        a,b,q,n,dx,rule = advance(left,right,state_id)
        if states and n >= 65536:
            if last < offset:
                states.append(state)
                legs.append((offset-last,None))
            cmd = large_jump(cert,left,right,n,dx,rule)
            states.append((a,b,q))
            legs.append((n,cmd))
            last = offset+n
        head += dx
        offset += n
        state = a,b,q
        operations += 1
        if operations % 100000 == 0:
            phase.cache_clear()
            rules.one.cache_clear()
    pieces = ["import PackedStack"]+["import "+name for name in names]
    pieces.append("namespace H7846.Line24\nopen TM PackedTape\nattribute [local irreducible] TM.steps Pack.toCfg")
    pieces.append(f"def thirdRestartPack : Pack := {pack(state)}")
    pieces.append(f"private theorem exactTape : {names[-1]}.finalPack = thirdRestartPack := by decide")
    pieces.append(f"theorem blankThirdRestart : steps {START_TIME+offset} init = some thirdRestartPack.toCfg := by")
    pieces.append("  have h := blankPostStack")
    for i,name in enumerate(names):
        prev = "h" if not i else f"z{i-1}"
        pieces.append(f"  have z{i} := steps_seq trans {prev} {name}.passage")
    pieces.append(f"  exact z{len(names)-1}.trans (congrArg (fun p : Pack => some p.toCfg) exactTape)")
    pieces.append("theorem thirdRestartShape : thirdRestartPack.st = .A ∧ "
                  "thirdRestartPack.l = restartPack.l ∧ thirdRestartPack.r.take 7 = "
                  "[(false,1324),(true,6),(false,8628),(true,6),(false,137382804),(true,6),"
                  "(false,967735738118322616190588893991)] := by decide")
    pieces.extend(["#print axioms blankThirdRestart","end H7846.Line24"])
    (path/"EpochReturn.lean").write_text("\n".join(pieces)+"\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
