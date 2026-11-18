"""Translate a line-26 visit count to a concrete blank checkpoint and audit it."""
from pathlib import Path
import argparse
import subprocess

from column_reserve import danger_delta, reserve
from prior_frontier import LIST, M26, parse

PAIRS = ('14','11','44','41')


def recover(binary, cut, ticks):
    row = subprocess.check_output([str(binary),str(cut),str(ticks)],text=True).split()
    end,width,visits,allocated = map(int,row[:4])
    digits = tuple(map(int,row[4]))
    assert end == ticks and allocated == len(digits) <= width
    ones_u = sum(d//2 for d in digits)
    ones_e = sum(d%2 for d in digits)
    physical_visits = visits-2*allocated*(width-allocated)
    raw = (192*ticks*ticks - 8*ticks + 3*physical_visits + ones_u + 2*ones_e
           + 7*allocated - 3*allocated*allocated + 5)
    s = (ticks.bit_length()-1)//2
    low_pairs = 3+s
    full_cost = sum(133*3**i*(ticks//4**(i+1)) for i in range(s))
    assert raw >= 192*ticks*ticks+207*ticks+5+full_cost-3*low_pairs*(low_pairs-1)
    cover = s if ticks == 4**s else s+1
    assert allocated <= (9*3**cover+1)//2
    return raw,physical_visits,digits


def literal_check(binary):
    table = parse(M26)
    tape = {}
    head = state = raw = 0
    for tick in range(1,65):
        target = -8*tick-1
        while head != target:
            move = table[state][tape.get(head,0)]
            assert move is not None
            symbol,direction,state = move
            if symbol:
                tape[head] = symbol
            else:
                tape.pop(head,None)
            head += direction
            raw += 1
        guess,_,digits = recover(binary,3+(tick%5),tick)
        word = '4'*(-target)+''.join(PAIRS[d] for d in digits)+'3'
        assert (state,raw) == (0,guess)
        assert len(tape) == len(word)
        assert all(tape.get(head+i,0) == int(a) for i,a in enumerate(word,1))
    print('64 consecutive literal blank checkpoints:',raw,'instructions at tick 64')


def physical_trips(binary):
    """Count the physical aligned pair rows separately on each of the two trips."""
    digits = []
    raw = 5
    targets = {91,1000,5000,12345}
    for n in range(1,8*max(targets)+1):
        raw += 3+12*(n//2)
        for _ in range(2):
            token = 'a' if n%2 else 'd'
            for i,old in enumerate(digits):
                u,e = divmod(old,2)
                if token == 'd':
                    raw += 6 if u else 4 if e else 3
                    if not u:
                        digits[i] ^= 1
                        if not e:
                            break
                else:
                    raw += 6 if token == 'a' else 3 if u else 4
                    if token == 'b':
                        digits[i] ^= 2
                        if u:
                            break
                    token = 'b' if e else 'a'
            else:
                assert token != 'd'
                raw += 11 if token == 'a' else 9
                digits.append(0 if token == 'a' else 2)
        if n%8 == 0 and n//8 in targets:
            guess,_,word = recover(binary,8,n//8)
            assert (raw,tuple(digits)) == (guess,word)
    print('individual physical trips through tick',n//8,'agree at',raw,'instructions')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('binary',type=Path)
    parser.add_argument('--extended',action='store_true')
    args = parser.parse_args()
    binary = args.binary.resolve()
    assert LIST[25] == M26 == '1RB2RB4LA2RA1LA_2LA4RA3LA---3RA'
    literal_check(binary)
    physical_trips(binary)
    ticks = 54306954019 if args.extended else 1268654660
    cuts = (17,18) if args.extended else (15,16)
    left = recover(binary,cuts[0],ticks)
    right = recover(binary,cuts[1],ticks)
    assert left == right
    raw,visits,digits = left
    print('independent calendar cuts',*cuts)
    print('tick',ticks,'width',len(digits),'head',-8*ticks-1)
    print('weighted ordinary visits over the final physical width:',visits)
    print('defined instructions from blank:',raw)
    print('paired digits, low first:',''.join(map(str,digits)))
    u = sum((d//2)<<i for i,d in enumerate(digits))
    e = sum((d%2)<<i for i,d in enumerate(digits))
    print('full packed u and e:',hex(u),hex(e))
    # Reverse the last Q. Its stopping bit is the first selected one in new e.
    high_u,high_e = u>>3,e>>3
    selected = high_e&~high_u
    bit = selected&-selected
    stop = bit.bit_length()-1
    old_e = high_e^(~high_u&(2*bit-1))
    assert stop >= 0
    after = 2*len(digits)+reserve(digits[3:])-len(digits[3:])
    before = after-danger_delta(high_u,old_e,stop)
    print('last Q stopped at full pair',3+stop,'pre-Q common clock',before)
    print('leading gap at the stopping cut:',stop+before.numerator//before.denominator)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
