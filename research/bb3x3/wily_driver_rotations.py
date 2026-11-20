"""Rotation and finite-prefix certificates for the Wily pair driver."""
from itertools import product

from check_bb33 import WILY
from wily_physical_corrections import digits, through_bits

P = digits("222030111101130321301012")
SAFE = digits("222303111030")


def alternating(width):
    return sum(1 << i for i in range(0,width,2))


def drive(register, width, events):
    """Process finite inputs and retain their emission order at the cutoff."""
    output = []
    for mode in events:
        for i in range(width):
            bit = (register >> i) & 1
            written,mode = WILY.rules[mode][bit]
            register ^= (bit ^ written) << i
            if mode < 0:
                break
        if mode >= 0:
            output.append(mode)
    return register,tuple(output)


def rotation_check():
    excluded = {}
    opposite = {}
    for width in range(1,16):
        start = alternating(width)
        reached = set()
        word = start
        while word not in reached:
            reached.add(word)
            word,_ = drive(word,width,P)
        assert word == start
        for phase in range(1,len(P)):
            at_boundary,_ = drive(start,width,P[phase:])
            if at_boundary not in reached and phase not in excluded:
                excluded[phase] = width
        for phase in range(len(P)):
            at_boundary,_ = drive(((1 << width)-1)^start,width,P[phase:])
            if at_boundary not in reached and phase not in opposite:
                opposite[phase] = width
    assert len(reached) == 128
    assert sorted(excluded.values()) == [3]*14+[4]*2+[5,8]+[11]*4+[15]
    assert excluded[8] == 15
    assert len(opposite) == 24 and max(opposite.values()) == 15
    for phase, letters in ((13,"331"),(15,"3230")):
        root = P[phase:]+P[:phase]
        for expected in digits(letters):
            assert root[0] == expected
            root = through_bits(root,(1,0))


def local_code(bit, target):
    """A shortest single-emission block, with the original bit restored."""
    options = []
    for source in range(3):
        for start,(written,emitted) in enumerate(WILY.rules[source]):
            if emitted == target:
                options.append((3,)*(bit != start) + (source,) + (3,)*(written != bit))
    return min(options,key=len)


def encode(register, width, output):
    """Lift an emission word, restoring the complete lower register."""
    for i in reversed(range(width)):
        bit = (register >> i) & 1
        output = tuple(q for target in output for q in local_code(bit,target))
    return output


def reset(register, width, destination):
    """Change a register using localized silent flips and no exterior emission."""
    control = []
    for i in range(width):
        if ((register ^ destination) >> i) & 1:
            control.extend(encode(register,i,(3,)))
            register ^= 1 << i
    assert register == destination
    return tuple(control)


def histories(word, width):
    """Literal emitted streams at every even cut, including the input itself."""
    return tuple(drive(alternating(i),i,word)[1] for i in range(0,width+1,2))


def completion_check():
    for b,t in product(range(2),range(4)):
        y,emitted = drive(b,1,local_code(b,t))
        assert y == b and emitted == (t,)
    # Q(SAFE) enters the mixed-sign cycle and returns after six pairs.
    w = SAFE
    for _ in range(6):
        assert w[0] in (2,3)
        w = through_bits(w,(1,0))
    assert w == SAFE

    # P itself as a finite word. Find the first even cutoff it does not touch.
    width = 0
    while drive(alternating(width),width,P)[1]:
        width += 2
    register = alternating(width)
    previous,crossings = drive(register,width,P)
    assert not crossings
    assert all(stream[0] in (2,3) for stream in histories(P,width)[:-1])
    common = P+reset(previous,width,register)
    split = SAFE.index(1)
    a,b = SAFE[:split],SAFE[split:]
    block_a = common+encode(register,width,a)
    block_b = common+encode(register,width,b)
    assert drive(register,width,block_a) == (register,a)
    assert drive(register,width,block_b) == (register,b)
    assert a+b == SAFE and (b+a)[0] == 1
    print(f"One blank period reaches through bit {width-1}; the completion necklace "
          f"has {len(block_a)+len(block_b)} letters.")


if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    rotation_check()
    completion_check()
    print("All 23 other rotations have disjoint synchronized prefix orbits.")
