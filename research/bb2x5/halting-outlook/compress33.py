"""Check and replay the bulk line-33 ordinary-request transducer."""
import argparse
import base64
from collections import Counter
from contextlib import contextmanager
from itertools import product
import json
from pathlib import Path
import random
import subprocess
import sys
import zlib

from neglected33 import MACHINE, SOURCE, ExceptionalReturn, batch, checkpoint, literal_step, split_reserve

HERE = Path(__file__).resolve().parent


@contextmanager
def worker(binary, shifted=False):
    process = subprocess.Popen([str(binary.resolve())], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    try:
        def request(word, n):
            if shifted:
                assert n == 1
            process.stdin.write(word + "\n" if shifted else f"{n} {word}\n")
            process.stdin.flush()
            line = process.stdout.readline().rstrip("\n")
            if line == "exceptional solitary 2":
                raise ExceptionalReturn
            cost, output = line.split(" ", 1)
            return output, int(cost, 16)
        yield request
    finally:
        process.stdin.close()
        assert process.wait() == 0


def verify(request):
    counts = Counter()
    rng = random.Random(33)
    cases = [(w, n) for width in range(6) for w in map(''.join, product('124', repeat=width))
             for n in (0, 1, 2, 3, 6, 9)]
    cases += [(''.join(rng.choices('124', k=rng.randrange(60))), rng.randrange(2**80)) for _ in range(300)]
    cases += [('', 3**k + d) for k in (1, 21, 99, 543) for d in (-1, 0, 1)]
    for word, n in cases:
        try:
            v, elapsed = batch(word,n)
        except ExceptionalReturn:
            try:
                request(word,n)
            except ExceptionalReturn:
                counts['exception'] += 1
                continue
            raise AssertionError((word,n))
        assert request(word,n) == (v,elapsed)
        counts['ordinary'] += 1
        if len(word) <= 5 and n <= 9:
            tape = {i:int(c) for i,c in enumerate(word)}
            clock = 0
            for _ in range(n):
                head, state = 0,'A'
                while head >= 0:
                    head, state = literal_step(tape,head,state)
                    clock += 1
                    assert clock <= elapsed
                assert state == 'A' and head == -1
            assert clock == elapsed and tape == {i:int(c) for i,c in enumerate(v)}
            counts['literal'] += 1
    for word,limit,position,kind in [('2421',234,-2,'escape'), ('22222421',39142,34,'halt')]:
        tape = {i+1:int(c) for i,c in enumerate('2'+word)}
        head,state = 0,'A'
        for _ in range(limit):
            head,state = literal_step(tape,head,state)
        assert (head,state) == (position,'B')
        if kind == 'escape':
            assert tape == {i-1:int(c) for i,c in enumerate('421'*8)}
        else:
            assert tape[head] == 3
    print(dict(counts), 'two exact-schedule artificial controls',flush=True)


def extend(request,target,save,resume):
    p = json.loads(resume.read_text())
    assert p['machine'] == MACHINE and 33 <= p['left_extension'] <= target
    word = zlib.decompress(base64.b64decode(p['word_zlib_base64'])).decode()
    assert word.startswith('2') and len(word) == p['word_length']
    y, clock = word[1:], int(p['steps'])
    for epoch in range(p['left_extension']+1,target+1):
        result,cost = request(y,1)
        y = '2'+result
        clock += cost+4
        print(epoch,len(y)+1,clock.bit_length(),split_reserve(y)[1],flush=True)
    if save:
        save.write_text(json.dumps(checkpoint(target,y,clock),indent=2)+'\n')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Enable Python assertions.')
    assert SOURCE.read_text().splitlines()[32] == MACHINE
    if hasattr(sys,'set_int_max_str_digits'):
        sys.set_int_max_str_digits(0)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine',type=Path,required=True)
    parser.add_argument('--verify',action='store_true')
    parser.add_argument('--shifted',action='store_true',help='use the independent shifted-epoch checker (one blank epoch only)')
    parser.add_argument('--epoch',type=int)
    parser.add_argument('--save',type=Path)
    parser.add_argument('--resume',type=Path,default=HERE/'neglected33-checkpoint.json')
    a = parser.parse_args()
    with worker(a.engine,a.shifted) as run:
        if a.verify:
            verify(run)
        if a.epoch is not None:
            if a.epoch < 33: parser.error('start at extension 33')
            extend(run,a.epoch,a.save,a.resume)
