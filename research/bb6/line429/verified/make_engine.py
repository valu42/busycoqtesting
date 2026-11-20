"""Retarget the pinned BusyCoq PR 93 proof and fast interpreter to line 429."""
import argparse
import hashlib
import re
from pathlib import Path

SOURCE_DIGEST = '63964df1e1da61d8d3497a0faa03ad1ffe0bf0a331dcd9da7f3957fea4930c78'
ORIGINAL = '1RB0LC_1RC1RA_1RD0RF_0LE---_1LA1LE_0RA0RF'
REFLECTED = '1RB1RA_1LC0RD_1LD1LB_1LF0LE_0LB0LE_0RA---'


def derive(source):
    if hashlib.sha256(source).hexdigest() != SOURCE_DIGEST:
        raise ValueError('Expected the #598 proof from BusyCoq PR 93 at aaa730e0f2653bd02b80f94aa9d450557e810c85')
    src = source.decode().split('Lemma run_ok :')[0]
    src = src.replace('M598', 'Bell429')
    src = src.replace('1RB1RD_1LC0RE_1LD1LC_1RA0LB_0RD0RF_0RD---', ORIGINAL)
    src = src.replace('1RB1RA_1LC0RD_1LD1LB_1RA0LE_0LB0LF_0LB---', REFLECTED)
    src = src.replace('| A => C | B => D | C => A | D => B | E => E | F => F',
                      '| A => E | B => A | C => B | D => C | E => F | F => D')
    src = src.replace('initFastC', 'initFastB').replace('(C;; tape0)', '(B;; tape0)')
    src = src.replace('(RAW C R).\nDefinition is_none', '(RAW B R).\nDefinition is_none')
    # The source's counted proof scripts treat D0 as one step. In line 429 it is
    # D0, F0, A1. The three literal steps also prove the extra cell is zero.
    src = re.sub(r'\bdo (k|[0-9]+) step\b', r'do \1 bell_step', src)
    tactic = '''Ltac bell_step :=
  lazymatch goal with
  | |- (D, (_, S0, _)) -[ _ ]->* _ => do 3 step
  | _ => step
  end.

'''
    src = src.replace('Ltac norm_cb :=', tactic + 'Ltac norm_cb :=')
    return src + '''Theorem blank_engine k :
  match run_pow k initFastB with
  | Some s => (B;; tape0) -->* fs_denote s
  | None => halts tm c0
  end.
Proof.
  pose proof (run_pow_spec k initFastB) as H.
  rewrite initFastB_denote in H.
  destruct (run_pow k initFastB); [exact H | apply halts_iso; exact H].
Qed.
End Bell429.
Print Assumptions Bell429.blank_engine.
'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.write_text(derive(args.source.read_bytes()))
