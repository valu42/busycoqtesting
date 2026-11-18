"""Use line 19's two blank seeds for the exact tables on lines 19 and 23."""
import base64
import zlib

from checkpoints import holdouts
import survey

MACHINES = {19: '1RB2RA3LA---2LB_2LA4RA4RB0RB0LA',
            23: '1RB3LA3LB0RB0LA_2LA4RB1LB1RA---'}
DIGITS = bytes.maketrans(bytes(range(5)), bytes((0, 2, 1, 4, 3)))
STATES = {'A': 'B', 'B': 'A'}


def rule(machine, state, symbol):
    row = machine.split('_')['AB'.index(state)]
    return row[3*symbol:3*symbol+3]


def verify_tables():
    machines = holdouts()
    if any(machines[line-1] != machine for line, machine in MACHINES.items()):
        raise ValueError('wrong line 19 or 23 encoding')
    for state in 'AB':
        for symbol in range(5):
            op = rule(MACHINES[19], state, symbol)
            mapped = op if op == '---' else ''.join((
                str(DIGITS[int(op[0])]), 'L' if op[1] == 'R' else 'R', STATES[op[2]]))
            if mapped != rule(MACHINES[23], STATES[state], DIGITS[symbol]):
                raise ValueError('reflected instructions disagree')


def translate_checkpoint(p, dst_line):
    """Translate between physical coordinates, preserving the defined-step clock.

    Line 23 from blank A corresponds to line 19 from blank B, and vice versa.
    The caller supplies the original orbit; translation does not establish it.
    """
    verify_tables()
    src_line = p['line']
    cells = survey.verify_state(p, MACHINES[src_line])
    if dst_line == src_line:
        return dict(p)
    machine = MACHINES[dst_line]
    reflected = cells[::-1].translate(DIGITS)
    q = dict(p, line=dst_line, machine=machine, state=STATES[p['state']],
             head=-p['head'], left=1-p['left']-len(cells) if cells else 0,
             tape_zlib_base64=base64.b64encode(zlib.compress(reflected, 9)).decode())
    survey.verify_state(q, machine)
    return q


def strip_trace(word, state, position, replies, stop_at_call=False):
    """Trace until left exit or halt, recording all right calls and local steps."""
    tape = list(map(int, word))
    calls = []
    steps = 0
    while position >= 0:
        if position == len(tape):
            if len(calls) >= len(replies):
                if stop_at_call:
                    break
                raise ValueError('trace needs an unaccounted suffix reply')
            calls.append(state)
            state = replies[len(calls)-1]
            position -= 1
        op = rule(MACHINES[19], state, tape[position])
        if op == '---':
            break
        tape[position] = int(op[0])
        position += 1 if op[1] == 'R' else -1
        state = op[2]
        steps += 1
        if steps > 1000:
            raise ValueError('strip work limit')
    return ''.join(map(str, tape)), position, state, ''.join(calls), steps


def verify_parity_guard():
    # Enter one 2 from the left in B. One child B call determines the exit;
    # the cell flips the reply state and charges two local instructions.
    for incoming, word, outgoing in (('A', '2', 'B'), ('B', '0', 'A')):
        if strip_trace('2', 'B', 0, incoming) != (word, -1, outgoing, 'B', 2):
            raise ValueError('wrong B2 strip')
    # At the outermost 2, replay the guard and all steps through halt or exit.
    for incoming, expected in (('A', ('332', -1, 'A', 'B', 8)),
                               ('B', ('233', 1, 'A', 'B', 10))):
        if strip_trace('032', 'A', 0, incoming) != expected:
            raise ValueError('wrong 032 guard trace')

    # The 3022 launch prefix survives the blank-orbit predecessor filters.
    # When the suffix returns A twice, the next scan is the undefined A3.
    for replies, expected in (('B', ('3323020', -1, 'A', 'B', 20)),
                              ('AA', ('2332332', 1, 'A', 'BB', 41))):
        if strip_trace('0330222', 'A', 0, replies) != expected:
            raise ValueError('wrong 0330222 guard trace')


FREQUENT_PREFIX = '033233202332020030'


def verify_long_guard():
    before, position, state, calls, cost = strip_trace(FREQUENT_PREFIX, 'A', 0, '', stop_at_call=True)
    if (before, position, state, calls, cost) != ('121444441444444414', 18, 'B', '', 140):
        raise ValueError('wrong first call on the 3233 control')
    # After B unwinds from a run of twos, the first eleven symbols are
    # alternating. Neither remaining local computation can read past them.
    for reply, alternating, stop, local in (('A', '02', -1, 330), ('B', '20', 1, 64)):
        word = before + (alternating*6)[:11]
        final, p, q, calls, cost = strip_trace(word, reply, len(before)-1, '')
        if (p, q, calls, cost) != (stop, 'A', '', local) or (p == 1 and final[p] != '3'):
            raise ValueError('wrong exit or halt following the long carry')


if __name__ == '__main__':
    verify_tables()
    verify_parity_guard()
    verify_long_guard()
    print('Both reflected tables and the timed guard controls agree.')
