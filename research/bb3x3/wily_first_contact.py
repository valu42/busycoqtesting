"""Locate the first selected Wily carry or sign event in an entire finite-prefix orbit."""
import argparse
from functools import cache

from check_bb33 import EventStream, WILY
from wily_integer_map import canonical_bucket, image, inverse


def sweep_rules(backward):
    if not backward:
        return WILY.rules
    rows = []
    for row in WILY.rules:
        reverse = [None, None]
        for bit,(output,child) in enumerate(row):
            reverse[output] = bit,child
        rows.append(tuple(reverse))
    return tuple(rows)


@cache
def numerator_machine(backward):
    """Conjugate the sweep on binary digits of n/3 to one on binary digits of n."""
    sweep = sweep_rules(backward)
    start = (0,0,0)
    identity = (0,-1,0)
    states = [start,identity]
    ids = {state:i for i,state in enumerate(states)}
    rows = []
    for divide,mode,multiply in states:
        row = []
        for bit in (0,1):
            digit = (bit+divide)%2
            written,child = (digit,-1) if mode==-1 else sweep[mode][digit]
            output = (3*written+multiply)%2
            nxt = ((bit+divide-3*digit)//2,child,(3*written+multiply)//2)
            if nxt not in ids:
                ids[nxt] = len(states)
                states.append(nxt)
            row.append((output,ids[nxt]))
        rows.append(row)
    # Minimize equivalent sections, including all copies of the identity.
    groups = [0]*len(rows)
    while True:
        signatures = [tuple((bit,groups[child]) for bit,child in row) for row in rows]
        unique = {s:i for i,s in enumerate(dict.fromkeys(signatures))}
        updated = [unique[s] for s in signatures]
        if updated==groups:
            break
        groups = updated
    idle = groups[ids[identity]]
    active = sorted(set(groups)-{idle})
    labels = {g:i for i,g in enumerate(active)}
    labels[idle] = -1
    rules = tuple(tuple((bit,labels[groups[child]]) for bit,child in rows[groups.index(g)])
                  for g in active)
    return labels[groups[ids[start]]],rules


def summarize(stream,rules):
    @cache
    def count(node,bit):
        if node<=stream.num_modes:
            output,child = rules[node-1][bit]
            return output,int(child!=-1),1
        middle,left,first = count(stream.left[node],bit)
        end,right,second = count(stream.right[node],middle)
        return end,left+right,first+second
    return count


def first_event(word,level,base,rules,predicate):
    """Return (one-based time, low level+1 output bits, arriving mode) or None.

    predicate(mode,input_bit,output_bit) selects events at the indicated digit.
    A missing result excludes the event throughout the full finite-prefix cycle.
    """
    if level<0:
        raise ValueError('negative bit position')
    history = []
    stream = EventStream(len(rules))
    root = base+1
    for position in range(level):
        bit = (word>>position)&1
        count = summarize(stream,rules)
        end,_,_ = count(root,bit)
        if end!=bit:
            root = stream.join(root,root)
        history.append((stream,root,bit,count))
        _,stream,root = stream.through_cell(root,bit,rules)
        if not root:
            return None

    @cache
    def locate(node,bit):
        if node<=stream.num_modes:
            mode = node-1
            output,_ = rules[mode][bit]
            hit = (1,output,mode) if predicate(mode,bit,output) else None
            return output,1,hit
        middle,left,first = locate(stream.left[node],bit)
        end,right,second = locate(stream.right[node],middle)
        if first is None and second is not None:
            j,output,mode = second
            first = left+j,output,mode
        return end,left+right,first

    bit = (word>>level)&1
    end,n,hit = locate(root,bit)
    first_cycle = 0
    if hit is None and end!=bit:
        _,_,hit = locate(root,end)
        first_cycle = n
    if hit is None:
        return None
    rank,top,chosen = hit
    rank += first_cycle
    value = top<<level
    for position in reversed(range(level)):
        previous,node,bit,count = history[position]
        _,emissions,inputs = count(node,bit)
        copies,offset = divmod(rank-1,emissions)
        rank,before = offset+1,copies*inputs
        while node>previous.num_modes:
            left = previous.left[node]
            middle,emitted,length = count(left,bit)
            if rank<=emitted:
                node = left
            else:
                rank -= emitted
                before += length
                bit = middle
                node = previous.right[node]
        output,child = rules[node-1][bit]
        assert rank==1 and child!=-1
        value |= output<<position
        rank = before+1
    return rank,value,chosen


def last_positive(escape):
    if escape>=0 or image(escape)<=0:
        raise ValueError('expected a negative sign-escape source')
    bound = max(2,canonical_bucket(escape))
    # A positive predecessor fits below 5B, and all preceding negative values
    # fit down to -B. Thus the top bit is its true ordinary sign on this range.
    level = (5*bound).bit_length()
    base,rules = numerator_machine(True)
    time,positive,_ = first_event(escape,level,base,rules,lambda _,old,new: old!=new)
    assert 0<positive<5*bound and time<=bound
    return time,positive


def shell_contact(n,level,backward=False,modes=(0,1,2,3)):
    """First selected arrival at digit level of n/3, in either time direction."""
    mask = 1<<(level+1)
    return first_event(n*pow(3,-1,mask)%mask, level, 0, sweep_rules(backward),
                       lambda mode,old,new: mode in modes)


def check():
    for backward,step in ((False,image),(True,inverse)):
        base,rules = numerator_machine(backward)
        for x in range(-25,26):
            if not x%3:
                continue
            for level in range(6):
                mask = (2<<level)-1
                hit = first_event(x,level,base,rules,lambda _,old,new: old!=new)
                y = x
                for t in range(1,mask+2):
                    y = step(y)
                    if (x^y)&(1<<level):
                        assert hit and hit[:2]==(t,y&mask)
                        break
                else:
                    assert hit is None
    for backward in (False,True):
        rules = sweep_rules(backward)
        for n in (-43,-8,7,29):
            for level in range(5):
                modulus = 2<<level
                start = n*pow(3,-1,modulus)%modulus
                for modes in ((0,1,2,3),(1,3),(2,)):
                    found = shell_contact(n,level,backward,modes)
                    z = start
                    for t in range(1,modulus+1):
                        mode = 0
                        arrival = -1
                        for position in range(level+1):
                            if mode==-1:
                                break
                            if position==level:
                                arrival=mode
                            bit=(z>>position)&1
                            output,mode=rules[mode][bit]
                            z ^= (output^bit)<<position
                        if arrival in modes:
                            assert found==(t,z,arrival)
                            break
                    else:
                        assert found is None
    assert last_positive(-5870)==(17,1)
    for seed in (-8,-16):
        e = seed
        for _ in range(8):
            t,p = last_positive(e)
            x=e
            for _ in range(t):
                assert x<0
                x=inverse(x)
            assert x==p and p>0
            e=64*e+270


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--family',type=int,help='compute LLSS^k for k=0 through this value')
    args=parser.parse_args()
    if not __debug__:
        parser.error('enable assertions')
    check()
    if args.family is not None:
        for seed in (-8,-16):
            e=seed
            for k in range(args.family+1):
                t,p=last_positive(e)
                print(seed,k,e,t,p,flush=True)
                e=64*e+270
