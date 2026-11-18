"""Finite tile traces and exact local clock for the odd left records on line 18.

At record k >= 1, A scans -2k-1, followed by 134(313)^k. The suffix
starts at k+3. If its A request and its next 2^(k-1) B requests all return
in B, the next record has moved two cells left. Its last 3 comes from the
first cell of that suffix: A2 -> 3LB is the unique leftward B exit.

Write T(r) = ABA (BBA)^r. The guard emits T(2), spending 39 steps. The
six traces in verify() show that each interior tile receiving T(r) emits
T(2r-1) and spends 7+17r steps. The last tile emits A followed by r-1
copies of B and spends 7+12r. All tiles return AAB per input triple.
From the actual B replies of the suffix, these finite traces compose back
to the guard. At tile j (starting at zero) r=2^j+1, so adding the guard,
k-1 interior tiles and one last tile gives 17+24k+29*2^(k-1) local steps.
The guard leaves 13431, and each of the k tiles leaves 331. Appending
the checked suffix digit 3 gives exactly 134(313)^(k+1) at the new cut.
"""
import sys

from checkpoints import ROOT, holdouts

sys.path.insert(0, str(ROOT))
from prior_sweeps import TapeMachine

MACHINE = '1RB2RA3LB4LA---_2LA0RB1LA2RB0RA'


def local_steps(k):
    """Instructions strictly left of the suffix during the two left extensions."""
    if k < 1:
        raise ValueError('the odd record index k must be positive')
    return 17 + 24*k + 29*(1 << (k-1))


def trace(word, incoming, replies, entry=0, limit=100):
    """Simulate a finite strip, counting steps in the strip and recording both cuts."""
    tm = TapeMachine(MACHINE, map(int, word))
    requests = []
    returns = []
    for state in incoming:
        tm.head, tm.state = entry, state
        while tm.head >= 0:
            if tm.head == len(word):
                if len(requests) == len(replies):
                    raise AssertionError('strip demanded an extra reply')
                requests.append(tm.state)
                tm.head, tm.state = len(word)-1, replies[len(requests)-1]
            if tm.steps >= limit or not tm.step():
                raise AssertionError('finite strip failed to return')
        returns.append(tm.state)
    if len(requests) != len(replies):
        raise AssertionError('strip did not consume the supplied replies')
    final = ''.join(str(tm.tape.get(i, 0)) for i in range(len(word)))
    return final, ''.join(requests), ''.join(returns), tm.steps


def verify():
    if holdouts()[17] != MACHINE:
        raise AssertionError('line 18 identity mismatch')

    # Each strip row gives (initial cells, incoming word, supplied replies,
    # entry offset) and (final cells, outgoing word, replies to parent, cost).
    # The guard strip begins one cell left of the old head, so an exit on its
    # left is two cells left of the old head.
    rows = [
        (('00134', 'A', 'AAB'*3, 1), ('13431', 'ABA'+'BBA'*2, 'A', 39)),
        (('313', 'ABA', '', 0), ('334', '', 'AAB', 7)),
        (('334', 'BBA', 'AAB'*2, 0), ('331', 'ABA'+'BBA', 'AAB', 17)),
        (('331', 'BBA', 'AAB'*2, 0), ('331', 'BBA'*2, 'AAB', 17)),
        (('334', 'BBA', 'B', 0), ('331', 'A', 'AAB', 12)),
        (('331', 'BBA', 'B', 0), ('331', 'B', 'AAB', 12)),
    ]
    for args, expected in rows:
        if trace(*args) != expected:
            raise AssertionError(f'incorrect finite strip trace for {args}')

    # For T(r) = ABA (BBA)^r, an interior 313 emits T(2r-1), returns AAB
    # per incoming triple, costs 7+17r and finishes 331. The terminal 313
    # sees B replies, emits A B^(r-1), costs 7+12r and finishes identically.
    # The guard starts with r=2. Hence tile j, counting from zero, receives
    # r=2^j+1. Summing the guard, k-1 interior costs and the terminal cost
    # gives local_steps(k). These longer traces independently check composition.
    for k in range(1, 8):
        count = 1 << (k-1)
        expected = ('13431'+'331'*k, 'A'+'B'*count, 'A', local_steps(k))
        actual = trace('00134'+'313'*k, 'A', 'B'*(count+1), entry=1,
                       limit=local_steps(k)+1)
        if actual != expected:
            raise AssertionError(f'full header trace mismatch at record {k}')


if __name__ == '__main__':
    verify()
    print('Line 18 guard and tile traces and seven composed headers match the TM.')
