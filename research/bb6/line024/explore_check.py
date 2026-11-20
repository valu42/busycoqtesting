"""Cross-check each accelerated operation against literal moves on short tapes."""
from collections import Counter
from random import Random

from explore import advance, encode, literal, runs


def check_restarts():
    exterior = ((1, 5), (0, 1), (1, 2), (0, 1), (1, 3))
    debris = ((1, 4),) + encode((1,) + (2,)*19 + (3, 0, 1, 1, 0))
    first = runs(((0, 1324), (1, 6), (0, 18396801867785)) + debris)
    widths = (1320, 8628, 107996733, 33554430, 8388606, 2097150, 524286,
              131070, 32766, 8190, 2046, 510, 126, 30, 6, 0)
    prefix = [(0, 4)] + [part for w in widths for part in ((0, w), (1, 6))]
    prefix += [(0, 2), (1, 4)]
    gap = 18396801869163 - sum(n for _, n in prefix)
    second = runs(tuple(prefix) + ((0, gap),) + debris)
    left = right = ()
    time = head = state = 0
    for target, target_head, target_right in ((4679860003204851, -69, first),
                                              (4679882754726131, -117, second)):
        while time < target:
            left, right, state, dt, dh, _ = advance(left, right, state)
            time += dt
            head += dh
        assert (time, head, left, right, state) == (target, target_head, exterior, target_right, 0)
    print("Both exact restart tapes match from blank, including the distant suffix.")


def main():
    rng = Random(7846)
    cases = Counter()
    words = [(0,), (1, 0, 0), (1, 0, 1, 0), (2, 0, 1, 1, 0),
             (0, 1, 0), (2, 0, 0), (2, 1, 0, 0)]

    def context():
        return runs((rng.randrange(2), rng.randrange(1, 8)) for _ in range(5))

    for i in range(20000):
        left = runs(((0, 1), (1, rng.randrange(1, 12)), (0, 1)) + context())
        word = rng.choice(words + [(rng.randrange(4), 0, 1, 0)])
        right = runs(((1, 1), (0, 1)) + encode(word) + ((0, rng.randrange(1, 80)),) + context())
        state = 3
        if i % 8 == 0:
            state = 0
            left = runs(((1, 2), (0, 1), (1, rng.randrange(2, 12)), (0, 1)) + context())
            right = runs(((0, 6),) + context())
        elif i % 8 == 1:
            state = 0
            left = runs(((1, 11), (0, 1)) + context())
            right = runs(((1, 1), (0, 3)) + context())
        end_left, end_right, end_state, elapsed, displacement, rule = advance(left, right, state)
        head = 0
        for _ in range(elapsed):
            left, right, state, _, move, _ = literal(left, right, state)
            head += move
        assert (left, right, state, head) == (end_left, end_right, end_state, displacement)
        cases[rule] += 1
    assert len(cases) == 7, cases
    print("20,000 full-tape comparisons passed.", dict(cases))
    check_restarts()


if __name__ == "__main__":
    main()
