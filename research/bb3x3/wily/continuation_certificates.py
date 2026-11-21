"""Finite certificates for the second automata investigation.

A finite permutation obstruction excludes an infinite family of potential
conjugacies. No nonhalting claim for the actual blank seed is made.
"""
from __future__ import annotations
from collections import Counter
from fibonacci_records import repair_word, value
from return_abstraction import run_return, R, monoid_dfa, BAD
from section_suffix_certificate import table_certificate
from return_sections import return_section, prefix_action, section, reduce_word
from certificates import pass_word, STEP, words

C_TABLE=((0,1),(0,2),(1,0))

def group_recursion_certificate():
    """Exact root recursions supporting the all-depth noncontraction proof.

    These are symbolic section identities, not a test at a finite tree depth.
    Here a temporal (d,c) means the function c composed with d.
    """
    assert section((2,),0)==(0,(2,))  # c|0=c
    assert section((2,),1)==(1,(1,))  # c|1=b
    assert section((1,1),0)==(0,(2,))
    assert section((1,1),1)==(1,(0,3))
    assert reduce_word((3,2))==(0,)
    assert reduce_word((3,2,3))==(0,3)  # ad=dcd, a conjugate of c
    assert section((3,3),0)==(0,())
    assert section((3,3),1)==(1,())
    return {'c_sections':'c,b','b_squared_sections':'c,dcd','d_squared':'identity'}

def raw_return(prefix,period):
    current=prefix;raw=[]
    for _ in range(period):
        current,q=prefix_action(current)
        if q!=4:raw.append(q)
    assert current==prefix
    return tuple(raw)

def level_permutations(depth):
    ws=list(words(depth));ids={w:i for i,w in enumerate(ws)};result=[]
    for mode in range(4):
        perm=[]
        for w in ws:
            q=mode;out=[]
            for b in w:
                emit,q=STEP[q][int(b)];out.append(str(emit))
            perm.append(ids[''.join(out)])
        result.append(tuple(perm))
    return result

def compose_word(gens,temporal):
    p=tuple(range(len(gens[0])))
    for q in temporal:p=tuple(gens[q][i]for i in p)
    return p

def cycle_type(perm):
    unseen=set(range(len(perm)));counts=Counter()
    while unseen:
        x=next(iter(unseen));n=0
        while x in unseen:
            unseen.remove(x);n+=1;x=perm[x]
        counts[n]+=1
    return tuple(sorted(counts.items()))

def all_powers(perm):
    p=tuple(range(len(perm)));result=[]
    while p not in result:
        result.append(p);p=tuple(perm[i]for i in p)
    assert p==tuple(range(len(perm)))
    return result

def checks():
    feature,_=monoid_dfa([C_TABLE,BAD.transitions])
    # The double-suffix strengthening still admits a halting counterexample.
    assert sorted('001100')==sorted('100100')
    assert feature.step_word(feature.initial,'001100')==feature.step_word(feature.initial,'100100')
    trace=['100100','000111','111111','0100100','1011000','0010111','1100111','0111111']
    assert all(w[-2:]in('00','11')for w in trace)
    assert [pass_word(w)for w in trace]==trace[1:]+[None]
    # The actual 32-step return map, including empty-tail behavior.
    assert R==(2,2,1,0,0,3,1,1,2,2,1,0)
    assert ''.join('abcd'[q]for q in raw_return('001100',32))=='ccbadcdbbcdaba'
    bit,first_section=section(R,1)
    second_bit,second_section=section(first_section,0)
    assert (bit,second_bit)==(1,0)
    assert ''.join('abcd'[q]for q in second_section)=='cbacbcba'
    assert run_return('')=='10000010101100'
    first_tail=run_return('');bad_tail='10011010001000'
    assert sorted(first_tail)==sorted(bad_tail)
    assert feature.step_word(feature.initial,first_tail)==feature.step_word(feature.initial,bad_tail)
    assert bad_tail.startswith('10')and bad_tail.endswith('00')
    assert run_return(bad_tail)is None
    w='001100'
    for _ in range(32):w=pass_word(w);assert w is not None
    assert w=='001100'+run_return('')
    # Natural first-repair value and failed uniform Fibonacci family.
    first='10100101010100010010101000100'
    assert value(first)==5**8 and repair_word(5**8)==first
    small=repair_word(25);large=repair_word(3125)
    assert small=='101000100'
    assert pass_word('01011011')==small
    orbit=set();prefix6='001100'
    for _ in range(32):orbit.add(prefix6);prefix6,_=prefix_action(prefix6)
    assert prefix6=='001100'and len(orbit)==32
    assert '010110' in orbit and small[:6]in orbit
    w=small
    for _ in range(6):w=pass_word(w);assert w is not None
    assert w=='111010111'and pass_word(w)is None
    record_period,record_return=return_section(first)
    assert record_period==8192
    assert ''.join('abcd'[q]for q in raw_return(first,8192))=='cccadabbbbabbdadcbdababc'
    assert ''.join('abcd'[q]for q in record_return)=='cccacbbbbabbcabcbabc'
    assert run_return('',record_return)=='00011010001100'
    assert all(run_return(w,record_return)is None for w in('01101','10100','010100'))
    prefix='0101010000'
    assert large==prefix+small
    period,ret=return_section(prefix)
    assert period==128
    assert ''.join('abcd'[q]for q in ret)=='cbadbccdbbaacccbbac'
    gens=level_permutations(7);target=cycle_type(compose_word(gens,ret))
    assert target==((4,4),(8,6),(16,4))
    orders=[]
    for q in range(3):
        powers=all_powers(gens[q]);orders.append(len(powers))
        assert all(cycle_type(p)!=target for p in powers)
    assert orders==[32,16,8]
    return {'suffix_table_checks':table_certificate(),
            'group_recursion':group_recursion_certificate(),
            'natural_prefix_period':period,
            'return_cycle_type_on_seven_bits':target,
            'a_b_c_orders_on_seven_bits':orders}

if __name__=='__main__':
    import json
    print(json.dumps(checks(),sort_keys=True))
