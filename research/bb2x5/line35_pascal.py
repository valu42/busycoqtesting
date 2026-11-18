"""Transfer the right-boundary Pascal triples from line 37 to line 35."""
from itertools import product
from pathlib import Path

from line37_pascal import digit, next_suffix, outer_triplet
from prior_sweeps import TERNARY_CLOSE, TERNARY_OPEN, TapeMachine, direct_epoch, word_sweep


# Use line 37's names for matching roles: 2 opens, 1 closes, 3 is neutral.
def normalized35(word):
    return tuple(3-x if x in (1,2) else x for x in word)


def centers35(word):
    right = normalized35(reversed(word))
    assert right[:2] == (1,2)
    centers = []
    for j in range(2,len(right)-2,3):
        first,center,third = right[j:j+3]
        if (first,third) != (2,2):
            break
        centers.append(center)
    return tuple(centers)


def next35(centers):
    previous = False
    result = []
    for center in centers:
        current = center == 2
        result.append(digit(current,previous))
        previous = current
    return tuple(result)


def main():
    machines = Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()
    assert machines[34] == TERNARY_CLOSE == '1RB2LA4RA1LA3LA_0LA3RB3LB2RB---'
    assert machines[36] == TERNARY_OPEN == '1RB2LA3LA4RA1LA_0LA3LB3RB1RB---'
    alphabet = (1,2,3)
    successful = [0]*6
    failed = 0
    for n in range(1,9):
        for prefix in product(alphabet,repeat=n-1):
            word = prefix+(2,)
            new,low = word_sweep(word,TERNARY_CLOSE)
            if new is None:
                assert low == -6
                failed += 1
                continue
            right = normalized35(reversed(word))
            extended = (2,)+right
            assert next_suffix(extended)[1:] == normalized35(new[::-1][:n])
            successful[-low] += 1
    print('35/37 suffix correspondence by old debts zero through five:',successful,
          'with',failed,'guard failures')

    clean = {(2,x,2) for x in alphabet}
    for old,previous in product(alphabet,repeat=2):
        assert outer_triplet((2,old,2),previous) == (2,digit(old==2,previous==2),2)
    for exterior in product(alphabet,repeat=3):
        for following in alphabet:
            assert outer_triplet(outer_triplet(exterior,3),following) in clean

    m = TapeMachine(TERNARY_CLOSE)
    word = []
    previous = ()
    for epoch in range(1,1002):
        word,_ = word_sweep(word,TERNARY_CLOSE)
        assert word is not None
        if epoch <= 30:
            assert word == direct_epoch(m,alphabet)
        if epoch == 5:
            assert m.steps == 97 and m.head == -5 and word == list(map(int,'213111112'))
            assert centers35(word)[0] == 2
        if epoch >= 5 and epoch%2:
            current = centers35(word)
            assert current[:len(previous)] == next35(previous)
            previous = current
    print('literal epoch 5 at 97 steps, head -5, word 213111112')
    print('epoch 1001 width',len(word),'with',len(previous),'covered triples after the two-cell cap')
    for k in range(1,65):
        # Augment with the constant bit h[-1]=1.
        bits = 1; mask = (1<<(k+1))-1
        for period in range(1,2*(k+1)+1):
            bits ^= (bits<<1)&mask
            if bits==1:
                break
        assert period == 1<<k.bit_length()
    print('periods of the affine Pascal boundary checked through 64 centers')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
