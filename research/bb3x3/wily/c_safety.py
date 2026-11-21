#!/usr/bin/env python3
"""Complete finite-word decision and exact halt clock for repeated Wily mode s2.

This is a theorem about c = wilyPass(s2), NOT a decision of the blank Wily
orbit, which iterates F(w)=0+wilyPass(s0,w).  No external packages are used.

Run: python c_safety.py
The seven-state product closure check is an exhaustive finite certificate
of an unbounded regular-language invariant.  Enumerating short words is
only an independent implementation cross-check of the clock formulas.
"""
from collections import deque
from itertools import product

# a,b,c,d,e are s0,s1,s2,s3 and the identity after an early sweep exit.
# Pairs contain (output bit,next mode).
RULES = (
    ((1, 1), (0, 2)),
    ((1, 3), (0, 0)),
    ((0, 2), (1, 1)),
    ((1, 4), (0, 4)),
    ((0, 4), (1, 4)),
)
EXTENSION = ("0", None, "1100", "00", "")

# C,D,E in the mathematical note; D alone is the halting basin.
DFA = ((0, 1), (0, 2), (1, 0))


def sweep(word, mode=2):
    """The literal pass, without F's prepended zero; None means undefined."""
    output = []
    for char in word:
        bit, mode = RULES[mode][int(char)]
        output.append(str(bit))
    suffix = EXTENSION[mode]
    return None if suffix is None else "".join(output) + suffix


def d(word):
    return "00" if not word else str(1 - int(word[0])) + word[1:]


def dfa_state(word):
    state = 0
    for char in word:
        state = DFA[state][int(char)]
    return state


def dfa_state_from(word, state):
    for char in word:
        state = DFA[state][int(char)]
    return state


def c_nonhalting(word):
    """Exact decision, proved by the shortening recurrences in the note."""
    return dfa_state(word) != 1


def c_halt_clock(word):
    """Successful c-calls before its first undefined call; None means infinity.

    Maintain the equality H(original)=scale*H(word)+offset.  Every branch
    below shortens word, so this algorithm always terminates.
    """
    scale, offset = 1, 0
    while word not in ("", "1", "11"):
        if word.startswith("0"):
            word = word[1:]
        elif word.startswith("10"):
            word = word[2:]
            offset += scale
            scale *= 2
        elif word.startswith("110"):
            word = "1" + word[3:]
            scale *= 2
        elif word.startswith("111"):
            word = word[3:]
            scale *= 2
        else:
            raise AssertionError("Nonbinary input")
    return offset if word == "1" else None


def b_halt_clock(word):
    """Successful s1 calls before halt; None means an infinite s1 orbit."""
    if not word:
        return 0
    if word[0] == "0":
        clock = c_halt_clock(word[1:])
        return None if clock is None else 2 * clock + 1
    clock = c_halt_clock(d(word[1:]))
    return None if clock is None else 2 * clock


def epsilon_orbit(n):
    """Exact c^n(epsilon), recursively defined on the binary digits of n."""
    if n == 0:
        return ""
    if n % 2 == 0:
        return "10" + epsilon_orbit(n // 2)
    return "11" + d(epsilon_orbit(n // 2))


def product_closure_certificate():
    """All reachable states of pass x input-DFA x output-DFA.

    Closure of these seven triples under both bits is a finite induction
    certificate valid for binary words of every length.  For each accepted
    input end state, the pass must be defined and its completed output
    must again be accepted.  The proof is not a length-bounded test.
    """
    start = (2, 0, 0)
    todo = deque([start])
    reachable = {start}
    while todo:
        mode, input_state, output_state = todo.popleft()
        if input_state != 1:
            extension = EXTENSION[mode]
            assert extension is not None
            final_state = output_state
            for bit in extension:
                final_state = DFA[final_state][int(bit)]
            assert final_state != 1
        for bit in (0, 1):
            output, next_mode = RULES[mode][bit]
            following = (
                next_mode,
                DFA[input_state][bit],
                DFA[output_state][output],
            )
            if following not in reachable:
                reachable.add(following)
                todo.append(following)
    expected = {
        (2, 0, 0), (1, 1, 1), (3, 0, 2), (0, 2, 0),
        (4, 0, 0), (4, 1, 1), (4, 2, 2),
    }
    assert reachable == expected
    return sorted(reachable)


def check():
    print("Unbounded c-invariant certificate:", product_closure_certificate())
    for n in range(1024):
        assert sweep(epsilon_orbit(n)) == epsilon_orbit(n + 1)
    safe_counts = []
    for length in range(15):
        count = 0
        largest_clock = 0
        for bits in product("01", repeat=length):
            word = "".join(bits)
            # Exact finite-boundary identity a(d(w))=c(w).
            assert sweep(d(word), 0) == sweep(word, 2)
            if word:
                assert sweep(d(word), 2) == sweep(word, 0)
            b_clock = b_halt_clock(word)
            assert (dfa_state_from(word, 1) != 1) == (b_clock is None)
            if b_clock is not None:
                current = word
                for _ in range(b_clock):
                    current = sweep(current, 1)
                    assert current is not None
                assert sweep(current, 1) is None
            clock = c_halt_clock(word)
            assert c_nonhalting(word) == (clock is None)
            if clock is None:
                count += 1
                following = sweep(word)
                assert following is not None and c_nonhalting(following)
            else:
                largest_clock = max(largest_clock, clock)
                current = word
                for _ in range(clock):
                    current = sweep(current)
                    assert current is not None
                assert sweep(current) is None
                assert clock <= (1 << ((length - 1) // 2)) - 1
        safe_counts.append(count)
        assert count == (2 ** (length + 1) + (-1) ** length) // 3
        if length:
            assert largest_clock == (1 << ((length - 1) // 2)) - 1
    print("Independent b/c clock and identity checks: all 32,767 words of length <=14")
    print("Nonhalting counts by length:", safe_counts)
    print("The blank F-orbit remains undecided by this theorem.")


if __name__ == "__main__":
    check()
