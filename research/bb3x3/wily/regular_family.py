"""An exact regular P0-invariant for the separate seed 000100.

This deliberately is NOT a certificate for the blank reduced seed 001100.
It demonstrates the prefix-cycle / auxiliary-language construction on an
infinite family, with a globally checked finite-automaton certificate.
"""
from dfa import DFA, verify_invariant
from preimages import minimize

C_TABLE = ((0, 1), (0, 2), (1, 0))
PREFIXES = ('000100', '111100', '010000', '101110',
            '001000', '110000', '011100', '100111')

def family_dfa() -> DFA:
    prefixes = sorted({w[:j] for w in PREFIXES for j in range(6)}, key=lambda x:(len(x),x))
    ids = {p:i for i,p in enumerate(prefixes)}
    cbase = len(prefixes)
    dead = cbase + 3
    rows = []
    for p in prefixes:
        row=[]
        for b in '01':
            child=p+b
            if child in PREFIXES:
                row.append(cbase)
            else:
                row.append(ids.get(child, dead))
        rows.append(tuple(row))
    rows += [tuple(cbase + q for q in row) for row in C_TABLE]
    rows.append((dead, dead))
    return minimize(DFA(tuple(rows), frozenset({cbase,cbase+2})))

if __name__ == '__main__':
    import json
    certificate=family_dfa()
    result=verify_invariant(certificate, prepend=False, seed='000100')
    assert result['valid']
    assert not certificate.accepts('001100')
    print(json.dumps({'seed':'000100','states':len(certificate.transitions),
                      'blank_reduced_seed_accepted':certificate.accepts('001100'),
                      'verification':result},sort_keys=True))
    print(json.dumps({'transitions':certificate.transitions,
                      'accepting':sorted(certificate.accepting),
                      'initial':certificate.initial},sort_keys=True))
