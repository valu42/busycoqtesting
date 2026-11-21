#!/usr/bin/env python3
"""Verify continuation certificates; the Wily blank orbit remains unresolved.

Run with Python 3.10+ and assertions enabled. Only the standard library is
used. General proofs and the exact scopes of finite certificates are in
CONTINUATION.md and its linked notes.
"""
import json
from pathlib import Path
import sys

if not __debug__:
    raise SystemExit('Run without -O: this verifier requires assertions.')
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from check_bb33 import WILY
import certificates
import clock_obstruction
import continuation_certificates
from dfa import BAD
import fibonacci_repairs
from feature_analysis import monoid_dfa
import inverse_ca
import padding
import p_adic_obstruction
from return_abstraction import return_classifier


def check_tables():
    reference = tuple(
        tuple((bit, 4 if mode == -1 else mode) for bit, mode in row)
        for row in WILY.rules
    ) + (((0, 4), (1, 4)),)
    extensions = tuple(
        None if value is None else ''.join(map(str, value))
        for value in WILY.extension
    ) + ('',)
    assert certificates.STEP == reference
    assert certificates.END == padding.FINITE == clock_obstruction.BOUNDARY == extensions
    for model in (padding, clock_obstruction):
        for mode in range(5):
            for bit in (0, 1):
                assert (model.OUTPUT[mode][bit], model.NEXT[mode][bit]) == reference[mode][bit]
    assert clock_obstruction.BAD_DFA == BAD.transitions


def checks():
    check_tables()
    padding.verify()
    inverse_ca.verify()
    clocks = clock_obstruction.verify()
    fibonacci = fibonacci_repairs.verify()
    modular = p_adic_obstruction.verify()
    sections = continuation_certificates.checks()
    # This is a complete finite transducer preimage, not a word-length sample.
    feature, _ = monoid_dfa([continuation_certificates.C_TABLE, BAD.transitions])
    classifier = return_classifier(feature)
    assert len(feature.transitions) == 87 and len(classifier.transitions) == 517
    return {
        'status': 'all continuation certificates and regression checks passed',
        'blank_tape_decision': 'UNRESOLVED',
        'source_tables': 'all independent implementations equal the pre-existing WILY table',
        'contextual_clock_obstruction': clocks,
        'fibonacci_reset_certificates': fibonacci,
        'all_depth_polynomial_obstruction': {
            'scope': 'Every k>=1 and length modulus M>=1; constructive proof in P_ADIC_OBSTRUCTION.md',
            'reachable_target_index': modular['target_index'],
            'reachable_target_word': modular['target_word'],
            'example_k1': modular['example_k1'],
            'example_k2': modular['example_k2'],
            'finite_regression_cases': len(modular['finite_regression_checks']),
        },
        'return_section_certificates': sections,
        'exact_return_classifier_states': len(classifier.transitions),
        'proof_scope': 'General proofs are separate from short-word implementation checks. No blank invariant is claimed.',
    }


if __name__ == '__main__':
    print(json.dumps(checks(), indent=2, sort_keys=True))
