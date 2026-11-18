"""Read the exact two-entry halt test one cell upstream (lines 21 and 22)."""
from collections import Counter
from itertools import product
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from mixed_and_sweeps import LEFT_RB, LEFT_RA, cell
from prior_sweeps import TapeMachine


WORDS = {21: ('BAAAAA', 'BAAAABB', 'BAABBA', 'BAABBBB'), 22: ('BAAAAA',)}


def literal(machine, prefix):
    """Drive a fresh physical suffix. Stop at each left exit or actual halt."""
    m = TapeMachine(machine)
    for entry in prefix:
        m.state = entry
        m.head = 0
        while m.head >= 0:
            assert m.head <= 1, 'a bad control should never require a grandchild return'
            if not m.step():
                assert m.head == 1 and (m.state, m.tape[1]) == ('B', 2)
                return m.steps
    raise AssertionError('witness did not halt')


def check(line, machine):
    words = WORDS[line]
    controls = {word: literal(machine, word) for word in words}
    for n in range(9):
        for chars in product('AB', repeat=n):
            prefix = ''.join(chars)
            state = (0,)
            output = ''
            for a in prefix:
                state, stream = cell(machine, state, a)
                output += stream
                if state == 'halt' or len(output) >= 2:
                    break
            assert output.startswith('BB') == any(prefix.startswith(w) for w in words)
    data = json.loads((HERE / f'streams-{line}.json').read_text())
    assert machine == data['machine'] == (HERE.parent / 'BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()[line-1]
    traces = data['cuts']
    summary = []
    for part in (traces[:100], traces[100:]):
        counts = Counter()
        for row in part:
            s = row['prefix']
            if any(w.startswith(s) and len(w)>len(s) for w in words):
                counts['undecided'] += 1
            elif s.startswith(words):
                counts['dangerous'] += 1
            else:
                counts['excluded'] += 1
            counts['body occurrences'] += sum(s.startswith(words, j) for j in range(1,len(s)))
        summary.append(dict(counts))
    print(line, 'exact controlled local ticks', controls, 'cuts 0..99 then remaining cuts', summary)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled')
    check(21, LEFT_RB)
    check(22, LEFT_RA)
