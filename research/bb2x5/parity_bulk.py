"""Line 36. Exact finite-tape sweeps and eventual parity uniformity for finite bulk seeds."""
from itertools import product

from prior_frontier import LIST
from prior_sweeps import PARITY, TapeMachine, direct_epoch, word_sweep


def ordinary_sweep(closers):
    """Finite defect set on an infinite background of opening symbols."""
    covered = set(closers)
    for c in sorted(closers):
        x = c-1
        while x in covered:
            x -= 1
        covered.add(x)
    return covered ^ {x+1 for x in covered}


def comoving(closers):
    """Measure positions to the left of the leading (rightmost) closer."""
    return {max(closers)-x for x in closers} if closers else set()


def intervals(row):
    """Disjoint matched intervals in right-to-left coordinates, with exclusive ends."""
    positions = sorted(row)
    i = 0
    while i < len(positions):
        start = positions[i]
        end = start+2
        i += 1
        while i < len(positions) and positions[i] <= end:
            i += 1
            end += 2
        yield start,end


def clusters(row):
    """One boundary-free sweep with the spatial origin following the leading particle."""
    return {x for pair in intervals(row) for x in pair}


def finite_sweep(length, row):
    """Exact finite TM epoch. Distances are counted leftward from the last data cell."""
    blocks = list(intervals(row))
    end = blocks[-1][1] if blocks else 0
    deficit = max(0,end-length)
    if deficit >= 6:
        return None
    guard = (1,3,2)[deficit%3]
    header = (guard,) if deficit<3 else (1,3,3,4,guard,2)
    append = int(0 not in row) if length else int(header[-1]==3)
    new_length = len(header)+length+append
    out = {0} if append else set()
    for a,b in blocks:
        for edge in (a-1,b-1):
            if 0 <= edge < length-1:
                out.add(edge+append)
    # The first data cell reads its left neighbor's carry from the raw header.
    if length and ((end < length) != (header[-1]==3)):
        out.add(length-1+append)
    carry = False
    for i,digit in enumerate(header):
        if (digit!=2) != carry:
            out.add(new_length-1-i)
        carry = digit==3
    return new_length,out


def changes(xs):
    xs = sorted(xs)
    return sum((x-y)%2 for x,y in zip(xs,xs[1:]))


def domains(row):
    """First and last distances of the successive parity runs, read from the leader."""
    runs = []
    for x in sorted(row):
        if runs and (x-runs[-1][1])%2 == 0:
            runs[-1] = (runs[-1][0],x)
        else:
            runs.append((x,x))
    return runs


def audit_settling():
    slowest = []
    for width in range(1,14):
        worst = 0
        for mask in range(1<<max(0,width-2)):
            row = {0,width-1}|{j+1 for j in range(width-2) if (mask>>j)&1}
            count = 0
            old = domains(row)
            initial_b = (old[-1][1]+len(old)-1-old[0][1])//2
            while len(old)>1:
                row = clusters(row)
                new = domains(row)
                assert len(new) <= len(old)
                assert new[-1][1]+len(new) <= old[-1][1]+len(old)+2
                assert new[0][1] >= old[0][1]+2
                if len(new)==len(old):
                    x,y,z = old[-2][1],old[-1][0],old[-1][1]
                    assert new[-1][1] == z+2
                    if y==x+1:
                        assert new[-2][1] >= x+4
                    else:
                        assert new[-2][1] == x+2 and new[-1][0] == y
                old = new
                count += 1
            assert count <= initial_b*(initial_b+1)//2
            assert all(j%2==0 for j in row)
            worst = max(worst,count)
        slowest.append(worst)
    print('Largest bulk settling times exhaustively through width 13:',slowest)
    for r in range(30):
        row={0,2*r+1}
        for _ in range(r):
            row=clusters(row)
            assert 2*r+1 in row
        assert 2*r+1 not in clusters(row)


def audit():
    assert LIST[35] == PARITY == '1RB2LA1LA4RA2LA_0LA3RB3LB2RB---'
    for n in range(10):
        for bits in product((False,True),repeat=n):
            c = {j for j,b in enumerate(bits) if b}
            raw, _ = word_sweep([1+int(b) for b in bits],PARITY)
            sparse = finite_sweep(n,{n-1-i for i in c})
            expected = None if raw is None else (len(raw),{j for j,a in enumerate(reversed(raw)) if a==2})
            assert sparse == expected
            bulk = ordinary_sweep(c)
            assert comoving(bulk) == clusters(comoving(c))
            assert changes(bulk) <= changes(c)
            if all(j-1 not in c for j in c):
                assert bulk == ({j-1 for j in c}^{j+1 for j in c})
            # Padding isolates all these matched intervals from the TM header and terminal.
            pad = 2*n+4
            word = [1]*pad + [1+int(b) for b in bits] + [1]*pad
            out,low = word_sweep(word,PARITY)
            assert low == 0
            if n <= 4:
                machine = TapeMachine(PARITY,word,left=1)
                assert direct_epoch(machine,(1,2)) == out
            body = out[1:1+len(word)]
            observed = {x-pad for x in range(1,len(word)-1) if body[x]==2}
            assert observed == bulk
    row = (0,set())
    for epoch in range(181):
        if epoch>=2:
            assert (0 in row[1]) == (epoch%2==0)
        row = finite_sweep(*row)
        assert row is not None
    print('Exact finite boundary formulas agree through length 9; alternating terminal phase checked on blank.')
    print('Cluster and padded data sweeps agree for lengths 1..9; literal TM replays agree for lengths 1..4.')
    for n in range(1,10):
        for mask in range(1<<(n-1)):
            row = {0}|{j+1 for j in range(n-1) if (mask>>j)&1}
            for r in range(7):
                window = 2*r+1
                stop = r+1
                z = row.copy()
                for _ in range(stop):
                    z = clusters(z)
                assert all(j%2==0 for j in z if j<=window)
                low = {j for j in z if j<=window}
                for _ in range(3):
                    z = clusters(z)
                    low ^= {j+2 for j in low if j+2<=window}
                    assert {j for j in z if j<=window} == low
    print('Sharp linear clearing times and subsequent Rule 90 evolution agree on finite windows.')
    for z in range(1,100):
        c = {2*i for i in range(z.bit_length()) if (z>>i)&1}
        row = c.copy()
        for steps in range(1,33):
            row = ordinary_sweep(row)
            if steps&(steps-1)==0:
                assert row == ({j-steps for j in c}^{j+steps for j in c})
    print('Power-of-two Rule 90 jumps agree through 32 bulk sweeps.')
    # The machine header and right edge can create new parity changes.
    seed = [1,1,2,1]
    out,low = word_sweep(seed,PARITY)
    assert low == 0
    before = changes(j for j,a in enumerate(seed) if a==2)
    after = changes(j for j,a in enumerate(out) if a==2)
    assert (before,after)==(0,3)
    print('Finite tape witness 1121 -> '+''.join(map(str,out))+' increases parity changes from 0 to 3.')


if __name__ == '__main__':
    audit()
    audit_settling()
