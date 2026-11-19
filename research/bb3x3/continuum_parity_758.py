"""Compute the continuum clock integrand and its incoming parity on a regular cell."""
from fractions import Fraction as F


def angular_gap(x):
    """Return the finite word and its open interval; stop at exact boundaries."""
    a,b=F(0),F(1)
    word=''
    for _ in range(1000):
        if x < F(1,3):
            x *= 3
            b /= 3
            word += 'J'
        elif x > F(5,9):
            x = (9*x-5)/4
            a,b = a+5*b/9, 4*b/9
            word += 'P'
        elif F(1,3)<x<F(5,9):
            return word,a+b/3,a+5*b/9
        else:
            raise ValueError('ideal endpoint')
    raise ValueError('angular word unresolved')


def interval(z):
    if not 1 < z < 3 or z==2:
        raise ValueError('requires an interior, nonseam position')
    h=(F(2,3) if z<2 else F(2),F(1))
    cells=[]
    for a in h:
        w,l,r=angular_gap(a/z)
        cells.append((a/r,a/l,w))
    low=max(i[0] for i in cells)
    high=min(i[1] for i in cells)
    return max(low,1 if z<2 else 2),min(high,2 if z<2 else 3),cells


def weights(z):
    lo,hi,cells=interval(z)
    flips=[not(w.count('P')%2) for _,_,w in cells]
    if all(flips):
        return (F(1,2),F(1,2))
    if any(flips):
        return tuple(F(not flip) for flip in flips)
    assert cells[0][0] != cells[1][0]
    assert lo==max(cell[0] for cell in cells)
    return tuple(F(cell[0]<lo) for cell in cells)


def cost(z,h,w):
    price=3*h*h/2
    a,c=2*h,z-h
    for op in w.replace('P','LL')+'LR':
        price+=3*min(a,c)**2
        if op=='J':
            assert a<c
            a,c=3*a,c-a
        elif op=='L':
            assert a>c
            a,c=a-c,3*c/2
        else:
            assert a<c
    return price


def verify():
    seen=set()
    for j in range(1,800):
        z=1+F(j,400)
        if z==2:continue
        try:lo,hi,cells=interval(z)
        except ValueError:continue
        ws=weights(z)
        assert sum(ws)==1 and lo<z<hi
        seen.add((cells[0][2].count('P')%2,cells[1][2].count('P')%2,ws))
        for (_,_,w),h in zip(cells,(F(2,3) if z<2 else F(2),F(1))):
            assert cost(z,h,w)>0
    both=[v for a,b,v in seen if (a,b)==(1,1)]
    assert set(both)=={(1,0),(0,1)}
    return seen


if __name__=='__main__':
    if not __debug__: raise SystemExit('Enable integer assertions.')
    verify()
    for z in (F(18,17),F(13,12),F(4,3),F(5,2)):
        try: lo,hi,cells=interval(z)
        except ValueError:continue
        print(z, (lo,hi), [w for _,_,w in cells], weights(z))
