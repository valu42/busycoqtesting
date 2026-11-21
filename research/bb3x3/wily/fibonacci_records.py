"""Independent Fibonacci encoding check; no blank-orbit decision claim."""
from __future__ import annotations
from certificates import STEP, END, pass_word

def fibonacci(n):
    f=[1,2]
    while len(f)<n:f.append(f[-1]+f[-2])
    return f[:n]

def value(w):return sum(int(b)*f for b,f in zip(w,fibonacci(len(w))))

def repair_word(n):
    assert n>0
    f=[1,2]
    while f[-1]<=n:f.append(f[-1]+f[-2])
    bits=['0']*(len(f)-1)
    for j in range(len(bits)-1,-1,-1):
        if f[j]<=n:bits[j]='1';n-=f[j]
    assert n==0
    w=''.join(bits)+'00'
    assert '11'not in w and w.endswith('100')
    return w

def pass_info(w):
    q=0;out=[]
    for b in w:
        bit,q=STEP[q][int(b)];out.append(str(bit))
    return q,None if END[q]is None else ''.join(out)+END[q]

if __name__ == '__main__':
    first = '10100101010100010010101000100'
    assert value(first) == 5 ** 8 and repair_word(5 ** 8) == first
    print('First repair Fibonacci coordinate verified:', value(first))
