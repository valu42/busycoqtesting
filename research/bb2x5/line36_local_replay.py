"""Replay the one-cell left certificate on full words with earlier piece histories."""
import argparse
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory

from line36_left import check_seed, phases
from line36_physical import HEADER
from line36_tiles import survivors


HERE = Path(__file__).resolve().parent
PACKED = HERE / 'line36-left-potential.json'


def pack(blocks,table):
    values = []
    for phase,(_,pieces,_) in enumerate(blocks):
        for kind in range(6):
            for choice in (0,1):
                piece = pieces[kind,choice]
                for halo in '12':
                    value = sum((-table[phase,kind,piece[:n],halo])<<(6*n)
                                for n in range(len(piece)))
                    values.append(str(value))
    return values


def unpack(blocks,packed):
    assert len(packed) == 144
    words = iter(map(int,packed))
    table = {}
    for phase,(_,pieces,_) in enumerate(blocks):
        for kind in range(6):
            for choice in (0,1):
                piece = pieces[kind,choice]
                for halo in '12':
                    value = next(words)
                    for n in range(len(piece)):
                        v = -(value&63)
                        assert -56 <= v <= 0
                        assert table.setdefault((phase,kind,piece[:n],halo),v) == v
                        value >>= 6
                    assert value == 0
    assert len(table) == 3588
    return table


def generate(binary,blocks):
    tokens = []
    for prefix,pieces,header in blocks:
        tokens.extend((prefix,str(header)))
        for k in range(6):
            tokens.extend((pieces[k,0],pieces[k,1]))
    with TemporaryDirectory() as temp:
        path = Path(temp)/'potential.tsv'
        subprocess.run([str(Path(binary).resolve()),str(path)],input='\n'.join(tokens)+'\n',
                       text=True,check=True)
        table = {}
        for line in path.read_text().splitlines():
            ph,k,part,halo,v = line.split('\t')
            table[int(ph),int(k),part,halo] = int(v)
    return pack(blocks,table)


def parse_global(word,limit,prefix,pieces):
    assert word.startswith(prefix)
    pos,kind = len(prefix),0
    while True:
        for choice in (0,1):
            p = pieces[kind,choice]
            if pos+len(p) <= limit and word.startswith(p,pos):
                pos += len(p)
                kind = (kind+1)%6
                break
        else:
            n = 0
            for choice in (0,1):
                p = pieces[kind,choice]
                j = 0
                while pos+j < limit and j < len(p) and word[pos+j] == p[j]:
                    j += 1
                n = max(n,j)
            return kind,word[pos:pos+n],pos+n


def labels(word,start,end,offset):
    # The last closing before the cut and every closing in its known continuation.
    before = word.rindex('2',0,start)
    positions = [before]+[i for i in range(start,end) if word[i]=='2']
    return [(i+offset)%2 for i in positions]


def changes(seq):
    return sum(a!=b for a,b in zip(seq,seq[1:]))


def charge(old,new,x,z,h,d):
    y = x+1
    a = labels(old,x,y,0)
    b = labels(new,z,len(new),1-h)
    align = a[-1] != (y-1)%2
    survives = old[x]=='1' and d==0
    possibilities = []
    for q in ((0,1) if not d else (0,)):
        tagged = b + ([(y+1)%2] if bool(q)!=survives else [])
        if q:
            adjustment = tagged[-1] != a[-1]
        else:
            fee = d-align if d else int(align)
            adjustment = int(tagged[-1] != (y+d+1)%2)-fee
        possibilities.append(changes(tagged)-changes(a)+adjustment)
    return max(possibilities)


def replay(blocks,table):
    checked = 0
    minimum = 1000
    for state,v in table.items():
        phase,kind,part,halo = state
        pref,ps,h = blocks[phase]
        target_phase = (phase+1)%6
        npref,nps,_ = blocks[target_phase]
        start = (kind+4)%6
        for a in (0,1):
            for b in (0,1):
                # Replay from the actual phase prefix, choosing a concrete older history.
                earlier = [(j+phase+a+b)%2 for j in range(6+start)]
                prior = pref+''.join(ps[j%6,choice] for j,choice in enumerate(earlier))
                expected = npref+''.join(nps[j%6,choice] for j,choice in enumerate(earlier))
                local = ps[start,a]+ps[(start+1)%6,b]+part
                minimum = min(minimum,local.count('1')-local.count('2'))
                old = prior+local+halo
                x = len(old)-1
                bits,guard = survivors(old)
                assert guard < 6 and len(HEADER[guard]) == h
                positions = [i for i in reversed(range(len(bits))) if bits[i]]
                out = bytearray(HEADER[guard],'ascii')
                previous = guard==1
                for bit in bits:
                    out.append(49+(previous!=bit))
                    previous = bit
                for d in range(13):
                    if d:
                        pos = positions[d-1]+h
                        out[pos] = 99-out[pos]
                        if pos+1 < len(out):
                            out[pos+1] = 99-out[pos+1]
                    new = out.decode('ascii')
                    assert new.startswith(expected+nps[start,a][:h+1])
                    nk,npart,z = parse_global(new,x+h,npref,nps)
                    assert new.rfind('2',len(expected),z) >= len(expected)
                    dest = target_phase,nk,npart,new[z]
                    c = charge(old,new,x,z,h,d)
                    assert table[dest]-v <= 3*(z-x)-24*c-4
                    checked += 1
    assert checked == 186576 and minimum == 20
    print('Full-history replay:',checked,'cases, minimum two-piece balance',minimum,
          'and seed potential',table[0,0,'','1'])


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--rebuild',metavar='EXECUTABLE',help='compare the C++ generator with the supplied table')
    args = parser.parse_args()
    blocks = phases()
    packed = json.loads(PACKED.read_text())
    if args.rebuild:
        assert generate(args.rebuild,blocks) == packed
    check_seed()
    replay(blocks,unpack(blocks,packed))
