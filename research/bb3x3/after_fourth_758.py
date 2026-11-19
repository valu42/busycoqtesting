"""Verify the common checkpoint of all six fourth-candidate crossing phases."""
from check_bb33 import champion_step, first_return
from check_confluence import itinerary
from check_fourth_gateway import K, EXPECTED

ODD_END = 17_713_937_045_736_097
EVEN_END = 18_378_934_934_326_344
CHECKPOINT = 18_378_934_934_402_308


def increments(first, last, word):
    """Certify a single ordinary first-return word and its periodic gains."""
    assert first % 2 == last % 2 and 'E' not in word
    assert itinerary(first)[0] == itinerary(last)[0] == word
    assert itinerary(last+2)[0] != word
    a, c = champion_step(1, last)
    for _ in word[:-1]:
        assert a > 1
        a, c = champion_step(a, c)
    assert a > 1 and champion_step(a, c)[0] == 1
    # Each bulk L loses one bit. Seed shifts divisible by 2^(1+#L)
    # preserve c modulo 4 at each L and hence every exact mass charge.
    modulus = 2**(1+word.count('L'))
    gains = {}
    for r in range(first % 2, modulus, 2):
        seed = first+(r-first)%modulus
        assert seed <= last
        gain = first_return(seed, batch=False)-seed
        assert gain > 0 and gain % 2 == 0
        gains[r] = gain
    return modulus, gains


def cross(seed, end, modulus, gains):
    """First lift above end, using a repeated residue's exact period."""
    seen = {}
    count = 0
    while seed <= end:
        r = seed % modulus
        if r in seen:
            old, old_count = seen[r]
            period = seed-old
            assert period > 0 and period % modulus == 0
            times = (end-seed)//period
            seed += times*period
            count += times*(count-old_count)
            seen.clear()
        seen[r] = seed, count
        seed += gains[r]
        count += 1
    return seed, count


def verify():
    firsts = [K+above for _, above in EXPECTED]
    odd = increments(min(firsts), ODD_END, 'J'*33+'L'*7+'R')
    outputs = []
    for seed in firsts:
        top, odd_steps = cross(seed, ODD_END, *odd)
        even = top
        transitions = 0
        while even % 2:
            even = first_return(even, batch=False)
            transitions += 1
            assert even and transitions <= 3
        outputs.append((top, odd_steps, even, transitions))
    even_word = increments(min(row[2] for row in outputs), EVEN_END, 'J'*33+'LLJLR')
    for seed, (top, odd_steps, even, transitions) in zip(firsts, outputs):
        exit_seed, even_steps = cross(even, EVEN_END, *even_word)
        current = exit_seed
        last_steps = 0
        while current < CHECKPOINT:
            current = first_return(current, batch=False)
            last_steps += 1
            assert current and last_steps <= 328
        assert current == CHECKPOINT
        print(seed-K, top, even, exit_seed, odd_steps+transitions+even_steps+last_steps)
    assert first_return(CHECKPOINT, batch=False) == 18_378_934_934_402_601
    print(f"All six crossings reach reset {CHECKPOINT:,}.")


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit("Run without -O to enable the checks.")
    verify()
