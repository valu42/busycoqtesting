#!/usr/bin/env python3
"""Audit the complete second-cusp reduction to halt or the first hard J/E input.

All quantified bounds are proved in REINJECTION_758.md. An emitted J/E is
unresolved; this code does not follow it or claim a blank-tape decision.
"""
from fractions import Fraction
from check_bb33 import champion_step
def jump(state):
    a,c=state
    assert a>1 and a%2==c%2==1 and a<=c
    out=champion_step(a,c)
    assert out==(3*a+2,c-a+1)
    return out


def bulk(state):
    a,c=state
    bit=((c+7)//2)%2
    assert c%2==1 and a>=4*((c+1)//4)+3
    out=champion_step(a,c)
    assert out==(a-c-2-2*bit,(3*c+7+6*bit)//2)
    return out,bit


def header(m,s):
    assert s%2==0
    p=3**m; z=s+2*m
    state=champion_step(1,s)
    assert state==(3,s+3)
    for _ in range(m-1): state=jump(state)
    assert state==(4*(p//3)-1,z-2*(p//3)+3)
    state,e0=bulk(state); state,e1=bulk(state)
    state=jump(state); state=jump(state)
    a,c=state; w=a+2*c; h=(a+1)//2; u=(w-1)//2
    assert w==2*z+23+4*(e0+e1)
    assert 4*c==49*z-54*p+318+98*e0+44*e1
    assert 49*w-8*c==108*p+491+108*e1
    assert 45*u+4*h==54*p+225+54*e1
    if e0:
        sibling,_,sibling_e1=header(m,s+2)
        assert sibling==state and sibling_e1==e1
    else:
        assert z%4==0 and e1==(z//4+m+1)%2
    return state,e0,e1


def bridge(m,s):
    """From the certified even exit strip to the second cusp section."""
    p=3**m
    cutoff=54*p//49-2*m-504
    assert m>=20 and cutoff<=s<=cutoff+2*m+40 and s%2==0
    start=s; returns=0; calls=0
    while True:
        z=s+2*m
        state=champion_step(1,s);calls+=1
        for _ in range(m-1):state=jump(state);calls+=1
        state,e0=bulk(state);state,e1=bulk(state);calls+=2
        state=jump(state);calls+=1
        a,c=state;t=c-a+1
        assert 4*t==49*z-54*p+318+98*e0+44*e1
        assert a%4==1 and t%2==1
        if t<=-3:
            state,e2=bulk(state);calls+=1
            assert state[0]%4==2 and 2<=state[0]<=state[1]
            state=champion_step(*state);calls+=1
            assert state==(1,s+2*m+14+2*(e0+e1+e2))
            s=state[1];returns+=1
            assert returns<=10 and s%2==0
            continue
        exceptional=t==-1
        if exceptional:
            assert c%4==3 and a==c+2 and e1==1
            state=champion_step(a,c)
            assert state==(3*a+2,1)
        else:
            state=jump(state)
        calls+=1
        a,c=state;w=a+2*c;u=(w-1)//2;h=(a+1)//2
        lane=225+54*e1+90*exceptional
        assert lane in (225,279,369)
        assert 45*u+4*h==54*p+lane
        assert 1<=c and 2*c<=49*m+555
        assert 49*w<=108*p+49*(4*m+63)
        assert calls<=11*m+54
        assert h%18==9
        return dict(m=m,start=start,departure=s,returns=returns,calls=calls,
                    state=state,lane=lane,exceptional=exceptional,
                    header_carries=e0+e1)


def odd_short_return(m,s):
    assert s%2==1
    state=(1,s)
    # First J permits the starting reset.
    state=champion_step(*state)
    for _ in range(m-1): state=jump(state)
    bits=[]
    for _ in range(5):
        state,bit=bulk(state);bits.append(bit)
        assert state[0]!=1
    a,c=state
    assert a%2==0 and a<=c
    out=champion_step(a,c)
    assert out==(1,s+2*m+15+2*sum(bits)) and out[1]%2==0
    return out[1],sum(bits)


def v2(n):
    assert n>0
    return (n&-n).bit_length()-1


def audit_metric_changes():
    assert pow(3,42,49)==1
    assert all(pow(3,d,49)!=1 for d in (6,14,21))
    assert v2(3**42-1)==3
    examples=[]
    for precision in (3,4,8,10):
        k=0
        for bits in range(4,precision+1):
            modulus=2**bits
            if (pow(3,19+42*k,modulus)+109)%modulus:
                k+=2**(bits-4)
            assert (pow(3,19+42*k,modulus)+109)%modulus==0
        m=20+42*k
        period=42*2**max(0,precision-3)
        if m<263:m+=period*(-((m-263)//period))
        p=3**m
        assert (54*p+1978)%49==0
        z=(54*p+1978)//49
        (a,c),e0,e1=header(m,z-2*m)
        before=(18*p+5788)//49;after=(c+7)//2
        assert (c,e0,e1,after)==(585,0,1,296)
        pre_a=(a-2)//3;pre_c=c+pre_a-1
        assert before==(pre_c+7)//2
        assert before%2==after%2==0
        assert v2(before//2+1)>=precision and v2(after//2+1)==0
        entered=bridge(m,z-2*m)
        assert entered['returns']==0 and entered['state']==(a,c)
        examples.append((m,v2(before//2+1),0))
    for precision in (7,8,12,16):
        c_expected=2**(precision+2)-11
        residue=(43+9*c_expected)%49
        m0=next(m for m in range(42) if pow(3,m,49)==residue)
        minimum=max(20,-((-2**(precision+4)-23359)//98))
        m=m0+42*max(0,-((m0-minimum)//42))
        p=3**m
        assert (54*p+4*c_expected-362)%49==0
        z=(54*p+4*c_expected-362)//49
        assert 20*49<=49*z-54*p<=1000*m*49
        (a,c),e0,e1=header(m,z-2*m)
        before=(36*p+19*c+461)//98;after=(c+7)//2
        assert (c,e0,e1)==(c_expected,0,1)
        pre_a=(a-2)//3;pre_c=c+pre_a-1
        assert before==(pre_c+7)//2
        assert before%2==after%2==0
        assert v2(before//2+1)==0 and v2(after//2+1)==precision
        entered=bridge(m,z-2*m)
        assert entered['returns']==0 and entered['state']==(a,c)
        examples.append((m,0,precision))
    return examples




K = Fraction(54, 49)


def verify_constants():
    r = Fraction(9, 4)
    assert (176+36*2)/r < 1038
    assert 8*K/(147-8/r) < Fraction(1,16)
    assert (108+10*2)/r < 512
    assert 4*K/(49-4/r) < Fraction(1,10)
    assert 4*K/49 > Fraction(89,1000)
    assert Fraction(-512,49) > -11
    m = 20
    assert 3**m >= 1000*m*r
    assert (8000*K*m-1038)/147 > 20*m+60
    assert Fraction(53*m,2)-11 > Fraction(35*m+85,2)
    assert (Fraction(1125,8)*m-(2*m+6))/(2*m+16) < 70
    assert Fraction(1265,8)*m+Fraction(85,2) < 200*m
    assert 71*(5*m+10)+15*m+60 == 370*m+770


def band(m):
    p,b,n,d = 3**m,2,9,4
    while p*d*4 >= 1000*m*n*9:
        b,n,d = b+2,n*9,d*4
    q = Fraction(p*d,n)
    assert 1000*m <= q < 2250*m and b < 3*m
    lo = Fraction(162*n*p-1038*n+(176+36*b)*d,147*n-8*d)
    hi = Fraction(54*n*p-512*n+(108+10*b)*d,49*n-4*d)
    assert 20*m+60 < lo-K*p < q/16
    assert Fraction(89,1000)*q-11 < hi-K*p < q/10
    assert hi-lo > Fraction(53,2000)*q-11 >= Fraction(53*m,2)-11
    assert hi-lo > Fraction(35*m+85,2)
    return b,lo,hi


def audit_band(m):
    b,lo,hi = band(m)
    low = -((-lo.numerator)//lo.denominator)
    high = hi.numerator//hi.denominator
    # z=s+2m is even at every even reset. Check both boundaries and all
    # four two-carry residue representatives nearest the lower boundary.
    low += low % 2
    high -= high % 2
    seeds = {low-2*m, high-2*m}
    seeds.update(low+2*j-2*m for j in range(4))
    seen = set()
    for seed in sorted(seeds):
        assert lo <= seed+2*m <= hi
        state,e0,e1 = header(m,seed)
        seen.add((e0,e1))
        for _ in range(b):
            state,_ = bulk(state)
            assert state[0] >= 3
        a,c = state
        assert a % 2 == c % 2 == 1 and 3 <= a <= c
    assert seen == {(0,0),(0,1),(1,0),(1,1)}
    return m,b,len(seeds)


def advance_header(m, seed, state, header_carries, exceptional=False):
    """Follow the finite bulk prefix, stopping before an unresolved J/E.

    A completed odd reset takes the separately proved short return. The
    asserted bulk bound is a proved consequence of the source collar, not
    an execution cutoff whose exhaustion is called a success.
    """
    b = carries = 0
    while state[0] > 1 and state[0] >= 4*((state[1]+1)//4)+3:
        state, bit = bulk(state)
        b += 1
        carries += bit
        assert b < 3*m
    a, c = state
    calls = b
    chi = int(exceptional)
    if a == 1:
        assert b >= 4 and b % 4 == 0
        first = c
        expected = seed+2*m+11+5*b//2+2*(header_carries+carries+chi)
        assert first == expected and first % 2 == 1
    elif b % 2:
        assert a % 2 == 0
        successor = champion_step(a, c)
        calls += 1
        if successor is None:
            return dict(kind="halt", value=None, calls=calls, bulks=b)
        assert successor[0] == 1
        first = successor[1]
        expected = seed+2*m+(27+5*b)//2+2*(header_carries+carries+chi)
        assert first == expected and first % 2 == int(b % 4 == 3)
    else:
        assert a > 1 and a % 2 == c % 2 == 1
        if a <= c:
            return dict(kind="J", value=state, calls=calls, bulks=b)
        assert a == c+2 and c % 4 == 3
        return dict(kind="E", value=state, calls=calls, bulks=b)
    if first % 2:
        final, _ = odd_short_return(m, first)
        calls += m+6
    else:
        final = first
    assert final % 2 == 0 and calls <= 4*m+6
    return dict(kind="reset", value=final, first=first, calls=calls, bulks=b)


def collar_attempt(m, seed):
    p = 3**m
    z = seed+2*m
    assert seed % 2 == 0 and 20*49 <= 49*z-54*p <= 1000*m*49
    state, e0, e1 = header(m, seed)
    result = advance_header(m, seed, state, e0+e1)
    result["calls"] += m+4
    assert result["calls"] <= 5*m+10
    if result["kind"] == "reset":
        gain = result["value"]-seed
        assert 2*m+16 <= gain <= Fraction(35*m+85, 2)
    return result


def reduce_exit_strip(m, seed):
    """Complete finite reduction from an inherited even exit-strip member."""
    p = 3**m
    receipt = bridge(m, seed)
    result = advance_header(
        m, receipt["departure"], receipt["state"],
        receipt["header_carries"], receipt["exceptional"],
    )
    calls = receipt["calls"]+result["calls"]
    if result["kind"] != "reset":
        assert calls <= 370*m+770
        return dict(kind=result["kind"], value=result["value"],
                    calls=calls, attempts=0, lane=receipt["lane"])
    seed = result["value"]
    assert 49*(2*m+6) <= 49*(seed+2*m)-54*p <= 49*(20*m+60)
    expected_b, lo, hi = band(m)
    for attempt in range(1, 72):
        z = seed+2*m
        assert 20*49 <= 49*z-54*p < 200*m*49
        in_band = lo <= z <= hi
        assert z < lo or in_band
        result = collar_attempt(m, seed)
        calls += result["calls"]
        if in_band:
            assert result["kind"] == "J" and result["bulks"] == expected_b
        if result["kind"] != "reset":
            assert calls <= 370*m+770
            return dict(kind=result["kind"], value=result["value"],
                        calls=calls, attempts=attempt, lane=receipt["lane"])
        seed = result["value"]
    raise AssertionError("The proved outer rank did not terminate.")


def audit_reductions():
    lanes = set()
    stops = set()
    checked = 0
    for m in (20, 35, 36, 51, 292):
        p = 3**m
        start = 54*p//49-2*m-504
        for offset in (0, 1, m, 2*m+19, 2*m+40):
            seed = start+offset
            seed += seed % 2
            if seed > start+2*m+40:
                continue
            result = reduce_exit_strip(m, seed)
            lanes.add(result["lane"])
            stops.add(result["kind"])
            checked += 1
    m = 51
    start = 54*3**m//49-2*m-504
    receipt = bridge(m, start+15)
    assert receipt["exceptional"] and receipt["returns"] == 4
    assert receipt["lane"] == 369 and receipt["state"][1] == 1
    result = reduce_exit_strip(m, start+15)
    lanes.add(result["lane"])
    stops.add(result["kind"])
    checked += 1
    assert lanes == {225, 279, 369}
    return checked, sorted(stops)


def audit():
    verify_constants()
    reductions, stops = audit_reductions()
    band_sources = 0
    for m in (20, 35, 36, 292, 4500):
        _, _, count = audit_band(m)
        band_sources += count
    metric_cases = audit_metric_changes()
    print("Verified second-cusp bridge, exceptional section, and complete finite reduction.")
    print("Focused exit-strip reductions:", reductions, "outcomes:", stops)
    print("Forced-band sources, covering both endpoints and all four carries:", band_sources)
    print("Actual exit-strip carry-valuation changes:", len(metric_cases))


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O for verification.")
    audit()
