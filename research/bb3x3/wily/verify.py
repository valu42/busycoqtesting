#!/usr/bin/env python3
"""Reproduce the Wily research certificates; this does not decide blank.

Run with Python 3.10+ and assertions enabled. Only the standard library is
used. Finite product certificates prove the stated all-word closure claims;
the separately labeled small-word checks validate implementations.
"""
import json
from pathlib import Path
import sys

if not __debug__:
    raise SystemExit("Run without -O: this verifier requires assertions.")

# Avoid leaving untracked bytecode in this or the pre-existing research tree.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from check_bb33 import WILY
import arithmetic_certificates as arithmetic
import c_safety
import certificates
from dfa import BAD, ENDS_00, SAFE, reduced_invariant_dfa, verify_invariant
from feature_analysis import abstraction, monoid_dfa
from regular_family import PREFIXES, family_dfa
from return_sections import prefix_action, return_section, validate


def check_reference_tables():
    """Exact equality with the repository's existing Lean-derived WILY table."""
    streaming = tuple(
        tuple((bit, 4 if mode == -1 else mode) for bit, mode in row)
        for row in WILY.rules
    ) + (((0, 4), (1, 4)),)
    extensions = tuple(
        None if extension is None else ''.join(map(str, extension))
        for extension in WILY.extension
    ) + ('',)
    assert certificates.STEP == c_safety.RULES == streaming
    assert certificates.END == c_safety.EXTENSION == extensions
    assert arithmetic.BOUNDARY == extensions
    for mode in range(5):
        for bit in (0, 1):
            assert (arithmetic.OUTPUT[mode][bit], arithmetic.NEXT[mode][bit]) == streaming[mode][bit]
    assert WILY.seed == (0, 0)


def check_regular_certificates():
    failures = {}
    for name, candidate in [('next_sweep_safe', SAFE), ('ends_00', ENDS_00)]:
        result = verify_invariant(candidate)
        assert result['contains_start'] and result['unsafe_word'] is None
        assert result['closure_counterexample'] == '000'
        assert result['closure_image'] == '0111'
        assert not result['valid']
        failures[name] = result

    family = family_dfa()
    result = verify_invariant(family, prepend=False, seed='000100')
    assert result['valid'] and len(family.transitions) == 19
    assert not family.accepts('001100')
    tail_modes = (4, 2, 4, 2, 4, 4, 4, 2)
    for index, prefix in enumerate(PREFIXES):
        assert prefix_action(prefix) == (PREFIXES[(index + 1) % 8], tail_modes[index])
    assert return_section('000100') == (8, (2, 2, 2))

    # Regression check of the constructive regular left quotient against its
    # defining predicate. This is not an assertion that SAFE is inductive.
    quotient = reduced_invariant_dfa(SAFE)
    for length in range(9):
        for word in certificates.words(length):
            expected = bool(word) and any(SAFE.accepts('01' * k + '00' + word)
                                          for k in range(1, 2 * len(SAFE.transitions) + 1))
            assert quotient.accepts(word) == expected
    return {'failed_candidates': failures, 'nonblank_regular_family': result}


def check_feature_obstruction():
    joint, signatures = monoid_dfa([c_safety.DFA, BAD.transitions])
    seed, counterexample = '001100', '001010'
    assert joint.step_word(joint.initial, seed) == joint.step_word(joint.initial, counterexample)
    assert len(signatures) == 87
    assert seed.count('0') == counterexample.count('0')
    assert seed.count('1') == counterexample.count('1')
    trajectory = [counterexample]
    for _ in range(3):
        trajectory.append(certificates.pass_word(trajectory[-1]))
    assert trajectory == ['001010', '110010', '011110', None]
    graph = abstraction(joint)
    assert graph['complete'] and not graph['safe']
    return {'joint_signatures': len(signatures), 'halting_counterexample': trajectory,
            'exact_abstract_graph': graph}


def main():
    check_reference_tables()
    print('Source check: all pass tables agree with the pre-existing WILY model.')
    small = certificates.checks()
    print('Small-word implementation checks:', json.dumps(small, sort_keys=True))
    c_safety.check()
    regular = check_regular_certificates()
    features = check_feature_obstruction()
    assert validate(depth=9)
    print('Prefix-section implementation checked independently through depth 9.')
    arithmetic.check_auxiliary_algebra()
    returns = [certificate.verify() for certificate in arithmetic.CERTIFICATES]
    arithmetic.check_failed_conjectures()
    result = {
        'status': 'all stated certificates and regression checks passed',
        'blank_tape_decision': 'UNRESOLVED',
        'regular_certificates': regular,
        'feature_obstruction': features,
        'arbitrary_tail_arithmetic_families': len(returns),
        'arithmetic_return_certificates': returns,
        'failed_mod24_conjecture': {'seed_integer': 146, 'halt_call': 135},
        'proof_scope': 'See README.md; no finite survival horizon is a nonhalting proof.',
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
