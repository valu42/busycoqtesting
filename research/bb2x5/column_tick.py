"""The exact finite transducer for an aligned line-26 tape above its bottom three pairs."""
from collections import deque
from itertools import product
import argparse

from prior_frontier import LIST, M26, parse
from verify import arithmetic26


def column(carry,digit):
    g,q = carry
    u,e = divmod(digit,2)
    passes = (2-e)*((g+1-u)//2)
    u ^= g % 2
    after = bool(q and (u or e))
    if q and not u:
        e ^= 1
    return (passes,after),2*u+e


def finish(carry):
    """Return the new physical suffix, or None for the undefined B3."""
    g,q = carry
    if q and g <= 1:
        return None
    n = (g+1)//2
    suffix = [0]*n
    if g % 2:
        suffix[0] = 2  # u=1,e=0
    if q:
        suffix[g % 2] += 1
    return tuple(suffix)


def tick(word):
    carry = (9,True)
    image = []
    for digit in word:
        carry,new = column(carry,digit)
        image.append(new)
    suffix = finish(carry)
    return None if suffix is None else tuple(image)+suffix


def count_test():
    # On paths that still pass Q, these are exact upper bounds on
    # number of zeros minus number of odd digits in the scanned prefix.
    best = {9:(0,''), 10:(1,'0'), 5:(0,'01'), 6:(1,'010'), 3:(0,'0101'),
            4:(1,'01010'), 2:(0,'010101'), 1:(-1,'01013'), 0:(-2,'010133')}
    def gain(digit):
        return int(digit == 0) - (digit % 2)

    for g,(score,witness) in best.items():
        carry = (9,True)
        for digit in map(int,witness):
            carry,_ = column(carry,digit)
        assert carry == (g,True) and sum(map(gain,map(int,witness))) == score
        for digit in range(4):
            (nxt,passes),_ = column(carry,digit)
            if passes:
                assert score+gain(digit) <= best[nxt][0]
    assert all(best[g][0] < 0 for g in (0,1))
    print('tight upper scores at the two halting carries:',best[0][0],best[1][0])

    # A nondecreasing additive digit score strictly separating 21 from the
    # one-tick halters would have positive dot product with the zero vector.
    def word(s):
        return tuple(map(int,s))
    def counts(w):
        return tuple(w.count(i) for i in range(4))
    def difference(a,b):
        return tuple(x-y for x,y in zip(counts(a),counts(b)))
    pairs = [('111','3331'),('211','1110'),('0312','23310')]
    rows = []
    for source,target in pairs:
        assert tick(word(source)) == raw_tick(word(source)) == word(target)
        rows.append(difference(word(target),word(source)))
    assert tick(word('0133')) is None and raw_tick(word('0133')) is None
    rows.append(difference(word('21'),word('0133')))
    assert all(sum(k*x for k,x in zip((1,2,1,2),col)) == 0 for col in zip(*rows))
    print('additive-score obstruction: three literal safe ticks and one literal B3')


def raw_tick(word):
    """Eight epochs on a nonblank tape in the correct phase, or the first B3."""
    table = parse(M26)
    pair = ('14','11','44','41')  # codes 2u+e, then physical digits (1-u,e)
    data = '4'+'14'*3+''.join(pair[s] for s in word)+'3'
    tape = dict(enumerate(map(int,data)))
    x,state = -1,0
    for _ in range(20000):
        op = table[state][tape.get(x,0)]
        if op is None:
            assert (state,tape[x]) == (1,3)
            return None
        tape[x],direction,state = op
        x += direction
        if x == -9:
            assert state == 0 and tape.get(x,0) == 0
            output = ''.join(str(tape[i]) for i in range(x+1,max(tape)+1))
            assert output.startswith('4'*9+'14'*3) and output.endswith('3')
            high = output[15:-1]
            assert len(high) % 2 == 0
            return tuple(pair.index(high[i:i+2]) for i in range(0,len(high),2))
    raise AssertionError('eight literal epochs exceeded the test budget')


def audit():
    assert LIST[25] == M26 == '1RB2RB4LA2RA1LA_2LA4RA3LA---3RA'
    start = (9,True)
    seen,queue = {start},deque([start])
    while queue:
        carry = queue.popleft()
        for digit in range(4):
            nxt,_ = column(carry,digit)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    assert len(seen) == 18
    assert {c for c in seen if finish(c) is None} == {(0,True),(1,True)}
    print('carry states',len(seen),'with',sum(finish(c) is None for c in seen),'halting terminal states')
    checked = 0
    for length in range(5):
        for word in product(range(4),repeat=length):
            assert tick(word) == raw_tick(word)
            checked += 1
    print('literal eight-epoch checks on',checked,'aligned physical words')

    u = e = width = 0
    word = None
    for t in range(1,4097):
        for token in 'aadd'*4:
            u,e,width = arithmetic26(u,e,width,token)
            assert e < 1<<width
        assert (u|e) % 8 == 0
        actual = tuple(2*(u>>i & 1)+(e>>i & 1) for i in range(3,width))
        if t == 1:
            word = (2,1)
            assert (u,e,width) == (8,16,5)
        else:
            word = tick(word)
        assert actual == word
    print('true first-tick word (2, 1); all checkpoints agree through tick 4096')


def predecessor(transitions,accepting):
    """Minimal complete DFA for words surviving a tick into the given DFA."""
    nodes = [((9,True),0)]
    index = {nodes[0]:0}
    edges,final = [],[]
    for carry,at in nodes:
        row = []
        for digit in range(4):
            after,output = column(carry,digit)
            pair = (after,transitions[at][output])
            if pair not in index:
                index[pair] = len(nodes)
                nodes.append(pair)
            row.append(index[pair])
        edges.append(row)
        suffix = finish(carry)
        if suffix is not None:
            for digit in suffix:
                at = transitions[at][digit]
        final.append(suffix is not None and accepting[at])

    classes = list(map(int,final))
    while True:
        signatures = {}
        refined = []
        for i,row in enumerate(edges):
            key = (final[i],tuple(classes[j] for j in row))
            refined.append(signatures.setdefault(key,len(signatures)))
        if refined == classes:
            break
        classes = refined
    representatives = [0]*len(signatures)
    for i,group in enumerate(classes):
        representatives[group] = i
    assert classes[0] == 0
    return ([tuple(classes[j] for j in edges[i]) for i in representatives],
            [final[i] for i in representatives])


def backward(horizon):
    transitions,accepting = [(0,0,0,0)],[True]
    sizes = []
    # Literal transducer iteration checks all short initial words independently.
    examples = [(w,w) for n in range(5) for w in product(range(4),repeat=n)]
    for _ in range(horizon):
        transitions,accepting = predecessor(transitions,accepting)
        sizes.append(len(transitions))
        updated = []
        for w,image in examples:
            image = None if image is None else tick(image)
            state = 0
            for digit in w:
                state = transitions[state][digit]
            assert accepting[state] == (image is not None)
            updated.append((w,image))
        examples = updated
    print('minimal survival-DFA sizes through horizon',horizon,':',sizes)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--horizon',type=int,default=8,help='number of exact backward preimages')
    args = parser.parse_args()
    if args.horizon < 0:
        parser.error('horizon must be nonnegative')
    audit()
    count_test()
    backward(args.horizon)
