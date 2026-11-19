"""Emit a bounded integer reachability query for the #758/#153 halting target."""
import argparse

from check_bb33 import HALTING_TARGET as H, champion_step
from halting_collar_758 import EXTENDED_FAR, NEAR

# A blank-connected reset. Later checkpoints can replace it in this query.
BLANK_RESET = 3**36 + 112_032
TERMINAL_MASS = 2*H + 1258
MIDDLE = 2*(H-(EXTENDED_FAR+NEAR)//2)+1


def numeral(x, width):
    if not 0 <= x < 2**width:
        raise ValueError('bit-vector constant out of range')
    return f'(_ bv{x} {width})'


def query(mode, depth, cap, start, start_mass=None, fixed_end=None, two_sided=False):
    """The endpoints and all witnesses are nonnegative integer counter pairs."""
    if depth < 0 or cap < 2 or (start is None) == (start_mass is None):
        raise ValueError('supply one starting state or one starting mass window')
    # Even arbitrary quantified coordinates have a correctly evaluated mass in
    # the twice-widened sort. For admitted inputs all branch arithmetic fits.
    width = (3*cap+16).bit_length()
    n = lambda x: numeral(x, width)
    typ = f'(_ BitVec {width})'
    decl = ' '.join(f'({name} N)' for name in ('a','c','b','d'))
    pieces = ['(set-logic BV)', f'(define-sort N () {typ})',
              f'(define-fun odd ((x N)) Bool (= (bvand x {n(1)}) {n(1)}))',
              '(define-fun mass ((a N) (c N)) (_ BitVec %d) '
              '(bvadd ((_ zero_extend 2) a) ((_ zero_extend 2) c) ((_ zero_extend 2) c)))' % (width+2),
              f'(define-fun legal ((a N) (c N)) Bool (bvule (mass a c) {numeral(cap,width+2)}))',
              f'(define-fun triple ((x N)) N (bvadd x x x))',
              f'(define-fun step ({decl}) Bool']
    same = lambda x,y: f'(and (= b {x}) (= d {y}))'
    if mode == 'ordinary':
        # q is floor((c+1)/4). Only continuing jumps and strong bulks survive.
        jump = same(f'(bvadd (triple a) {n(2)})', f'(bvadd (bvsub c a) {n(1)})')
        bulk = same('(bvsub a cost)', f'(bvadd (triple q) (triple q) {n(5)})')
        pieces.append(f''' (let ((q (bvlshr (bvadd c {n(1)}) {n(2)})))
 (let ((cost (bvadd (bvshl q {n(2)}) {n(3)})))
 (and (legal a c) (odd c) (bvugt a {n(1)}) (bvugt b {n(1)})
      (or (and (odd a) (bvule a c) {jump}) (and (bvuge a cost) {bulk}))))))''')
    elif mode == 'terminal':
        sink = same(n(0),n(0))
        small = f'''(ite (odd a)
             (ite (odd c) {same(f'(bvadd (triple a) {n(2)})',f'(bvadd gap {n(1)})')}
                          {same('(triple a)',f'(bvadd gap {n(4)})')})
             (ite (odd c) {same(n(1),f'(bvadd (bvlshr a {n(1)}) c {n(2)})')} {sink}))'''
        large = f'''(ite (not (odd c)) {same(f'(bvsub delta {n(1)})',f'(bvadd thrice_half {n(2)})')}
            (ite (= delta {n(1)}) {sink}
            (ite (= (bvand c {n(3)}) {n(1)}) {same(f'(bvsub delta {n(2)})',f'(bvadd thrice_half {n(5)})')}
            (ite (= delta {n(2)}) {same(f'(bvadd (triple c) {n(8)})',n(1))}
            (ite (= delta {n(3)}) {sink} {same(f'(bvsub delta {n(4)})',f'(bvadd thrice_half {n(8)})')})))))'''
        pieces.append(f''' (let ((gap (bvsub c a)) (delta (bvsub a c))
        (thrice_half (triple (bvlshr c {n(1)}))))
 (and (legal a c) (ite (and (= a {n(0)}) (= c {n(0)})) {sink}
 (and (bvugt c {n(0)}) (ite (bvule a c) {small} {large}))))))''')
    else:
        raise ValueError(mode)
    previous = 'step'
    for level in range(1,depth+1):
        name = f'path{level}'
        pieces.append(f'''(define-fun {name} ({decl}) Bool
 (exists ((h N) (j N)) (forall ((right Bool))
  ({previous} (ite right h a) (ite right j c) (ite right b h) (ite right d j)))))''')
        previous = name
    pieces += [f'(declare-const {x} N)' for x in ('a','c','b','d')]
    if start is None:
        lo, hi = start_mass
        pieces.append(f'(assert (and (bvuge (mass a c) {numeral(lo,width+2)}) '
                      f'(bvule (mass a c) {numeral(hi,width+2)})))')
    else:
        pieces.append(f'(assert (and (= a {n(start[0])}) (= c {n(start[1])})))')
    if fixed_end is not None:
        pieces.append(f'(assert {same(n(fixed_end[0]),n(fixed_end[1]))})')
    pieces.append(f'(assert ({previous} a c b d))')
    if two_sided:
        if start is not None or fixed_end is not None or mode != 'ordinary':
            raise ValueError('two-sided queries require an ordinary mass window')
        pieces += ['(declare-const x N)', '(declare-const y N)',
                   f'(assert ({previous} x y a c))']
    pieces += ['(check-sat)']
    return '\n'.join(pieces)+'\n'


def bulk_witness():
    # Choose the initial mass so the 392nd bulk lands exactly on the cut.
    c, gain = 1, 0
    for _ in range(392):
        q = (c+1)//4
        next_c = 6*q+5
        gain += 2*(next_c-c)-4*q-3
        c = next_c
    a, c = MIDDLE-gain-2, 1
    for i in range(784):
        q = (c+1)//4
        assert a >= 4*q+3 and a>1
        assert champion_step(a,c) == (a-4*q-3,6*q+5)
        a,c = a-4*q-3,6*q+5
        if i==391:
            assert a+2*c==MIDDLE
    assert a>1


def checks():
    # Each SMT block asserts that some endpoint differs from literal execution.
    # An independent solver should answer unsat to all six checks.
    cap = 160
    width = (3*cap+16).bit_length()
    for mode in ('ordinary','terminal'):
        for depth in (0,1,2):
            formula = query(mode,depth,cap,(1,1))
            print(formula[:formula.index('(declare-const a N)')],end='')
            print('(declare-const b N)\n(declare-const d N)\n(assert (or')
            for a in range(1,11):
                for c in range(1,11):
                    if depth == 2 and (a,c)!=(2,2):
                        continue
                    if depth and (a,c) not in ((3,7),(6,7),(2,2)):
                        continue
                    state = (a,c)
                    for _ in range(2**depth):
                        x,y = state
                        if x+2*y>cap:
                            state=None
                            break
                        if mode == 'terminal':
                            state = (0,0) if state==(0,0) else champion_step(x,y) or (0,0)
                        else:
                            q = (y+1)//4
                            if x<=1 or not y%2 or not ((x%2 and x<=y) or x>=4*q+3):
                                state=None
                                break
                            state=champion_step(x,y)
                            if state[0]<=1:
                                state=None
                                break
                    expected = ('false' if state is None else
                                f'(and (= b {numeral(state[0],width)}) (= d {numeral(state[1],width)}))')
                    path = f'path{depth}' if depth else 'step'
                    print(f' (xor ({path} {numeral(a,width)} {numeral(c,width)} b d) {expected})')
            print('))\n(check-sat)\n(reset)')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=('ordinary','terminal','checks'))
    p.add_argument('--depth',type=int,help='ordinary path length is 2 to this power (default 12)')
    args=p.parse_args()
    if args.mode=='checks':
        bulk_witness()
        checks()
        return
    if args.mode=='ordinary':
        depth=12 if args.depth is None else args.depth
        # Allow room for the 787-call exceptional return inside the basin.
        limit=2*(H-NEAR)+1-5458
        if not 0<=depth<=62 or MIDDLE+8+9*(2**depth)>limit:
            p.error('the ordinary proof requires depth 0 through 62')
        if MIDDLE-9*(2**depth)<2*(H-EXTENDED_FAR)+1:
            p.error('insufficient room below the central crossing')
        print(query('ordinary',depth,MIDDLE+8+9*(2**depth),None,(MIDDLE,MIDDLE+8),two_sided=True),end='')
    else:
        if args.depth is not None:
            p.error('terminal mode determines its complete depth from the mass horizon')
        steps=(TERMINAL_MASS-(1+2*BLANK_RESET))//4+1
        print(query('terminal',(steps-1).bit_length(),TERMINAL_MASS,(1,BLANK_RESET),fixed_end=(0,0)),end='')


if __name__=='__main__':
    main()
