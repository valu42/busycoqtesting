"""Reconstruct and certify the entire second restart through all sixteen markers.

The accelerator proposes checkpoints. Dense portions are replayed by the
verified literal interpreter on complete run-length encoded tapes. Large
counter jumps are proved by SharpSeries and the packed-tape transfer theorem.
"""
from certificate import term
from explore import advance, decode, drop, encode, runs
from sharp_certificate import SharpCertificate

START_TIME = 4679882754726131
END_OFFSET = 25354268309

def second():
    outer = ((1, 5), (0, 1), (1, 2), (0, 1), (1, 3))
    widths = (1320,8628,107996733,33554430,8388606,2097150,524286,131070,32766,8190,2046,510,126,30,6,0)
    front = [(0,4)] + [z for w in widths for z in ((0,w),(1,6))] + [(0,2),(1,4)]
    front += [(0,18396801869163-sum(n for _,n in front)),(1,4)]
    return outer, runs(tuple(front)+encode((1,)+(2,)*19+(3,0,1,1,0))), 0

def tape(rs):
    return "[" + ",".join(f"({'true' if b else 'false'},{n})" for b,n in rs) + "]"

def pack(state):
    left, right, q = state
    return f"⟨{tape(left)},{tape(right)},.{chr(65+q)}⟩"

def generate():
    state = second()
    cert = SharpCertificate()
    segments = []
    configs = [state]
    t = last = 0

    def literals():
        nonlocal last
        if last < t:
            segments.append((t-last, None))
            configs.append(state)
            last = t

    while t < END_OFFSET:
        l, r, q = state
        a,b,s,n,d,rule = advance(l,r,q)
        if n > 250000 and rule == "passes":
            literals()
            x = decode(drop(r,2))
            count = d//3
            end, core, proof = cert.prefix(x,count)
            assert core+15*count == n
            ext = drop(r,2+sum(w for _,w in encode(x)))
            # An infinite blank tail admits any finite amount of clearance.
            gap, rest = (ext[0][1],ext[1:]) if ext else (3*count+len(end)-len(x),())
            args = (proof,l[1:],gap,rest)
            segments.append((n,args))
            configs.append((a,b,s))
            last = t+n
        t += n
        state = (a,b,s)
    assert t == END_OFFSET
    literals()
    print("import PackedPhase\nimport PackedRestart\nimport Entry\nnamespace H7846.Line24\nopen TM Word PackedTape")
    print("set_option maxRecDepth 10000\n")
    print("\n\n".join(cert.lines))
    for i, cfg in enumerate(configs):
        print(f"def stackPoint{i} : Pack := {pack(cfg)}")
    print("attribute [local irreducible] TM.steps Pack.toCfg")
    for i,(cost,args) in enumerate(segments):
        print(f"private theorem leg{i} : steps {cost} stackPoint{i}.toCfg = some stackPoint{i+1}.toCfg := by")
        if args is None:
            print("  apply runSound\n  decide +native")
        else:
            proof, left, gap, rest = args
            print(f"  have h := packedSharp {proof} {tape(left)} {gap} {tape(rest)} (by decide)")
            print("  exact h")
    print(f"def postStackPack := stackPoint{len(segments)}")
    print(f"theorem blankPostStack : steps {START_TIME+END_OFFSET} init = some postStackPack.toCfg := by")
    print("  have a : steps 4679882754726131 init = some stackPoint0.toCfg := by")
    print("    have e : stackPoint0 = restartPack := by decide\n    rw [e,restartPack_eq]\n    exact blankSecondRestart")
    for i in range(len(segments)):
        prev = "a" if i == 0 else f"z{i-1}"
        print(f"  have z{i} := steps_seq trans {prev} leg{i}")
    print(f"  exact z{len(segments)-1}")
    print("#print axioms blankPostStack\nend H7846.Line24")

if __name__ == "__main__":
    generate()
