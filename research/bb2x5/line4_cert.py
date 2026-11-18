"""Universal replay of the line-4 local rules, including their exact durations.

An affine expression is (slope, intercept) for slope*n + intercept, n >= 0.
The interpreter rejects a branch when it cannot prove the same move for every n.
9 is an opaque boundary. Reaching it at the very end of a rule is permitted.
"""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Lin:
    s: int
    c: int

    def __add__(self, other):
        if isinstance(other, int):
            return Lin(self.s, self.c + other)
        return Lin(self.s + other.s, self.c + other.c)

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, int):
            return self + -other
        return Lin(self.s - other.s, self.c - other.c)

    def __mul__(self, value):
        return Lin(self.s * value, self.c * value)

    __rmul__ = __mul__

    def nonnegative(self):
        return self.s >= 0 and self.c >= 0

    def positive(self):
        return self.s >= 0 and self.c > 0


ZERO = Lin(0, 0)
ONE = Lin(0, 1)
MACHINE = "1RB3LA1LA1RA3RA_2LB2RA---4RB1LB"
RULES = {(state,int(i)): word[3*i:3*i+3]
         for state,word in zip("AB", MACHINE.split("_")) for i in range(5)}


def add_run(stack, digit, count):
    if count == ZERO:
        return
    assert count.positive(), count
    if stack and stack[-1][0] == digit:
        count += stack.pop()[1]
    stack.append((digit,count))


def runs(word):
    stack = []
    for item in word:
        digit, count = item if isinstance(item,tuple) else (item,ONE)
        add_run(stack, digit, count)
    return stack


def pop_span(stack, digit, count):
    if not stack:
        assert digit == 0
        return
    got, old = stack.pop()
    assert got == digit
    add_run(stack,digit,old-count)


def right_to_left(left,right):
    """Shift the split left by one cell, without changing the tape."""
    old = left[-1][0] if left else 0
    pop_span(left,old,ONE)
    add_run(right,old,ONE)


def verify_rule(start,target,duration,rules=RULES):
    left, right = runs(start[0]), runs(reversed(start[1]))
    state = 'A'
    remaining = duration
    while remaining != ZERO:
        assert remaining.positive(), remaining
        digit = right[-1][0] if right else 0
        assert digit != 9, "read through an opaque context"
        write, direction, state2 = rules[state,digit]
        assert direction in "LR", "early halt"
        write = int(write)
        # On a left-moving instruction, the contiguous input starts at the head
        # and extends into the left stack. On a right-moving instruction it is
        # already entirely on the right stack.
        if state2 != state:
            available = ONE
        elif direction == 'L':
            available = ONE + (left[-1][1] if left and left[-1][0] == digit else ZERO)
        else:
            available = right[-1][1] if right else ONE
        n = remaining if (available-remaining).nonnegative() else available
        assert (remaining-n).nonnegative()
        assert n.positive()
        if direction == 'R':
            pop_span(right,digit,n)
            add_run(left,write,n)
        else:
            pop_span(right,digit,ONE)
            if n != ONE:
                pop_span(left,digit,n-1)
            add_run(right,write,n)
            right_to_left(left,right)
        state = state2
        remaining -= n
    def normalize(stack):
        return stack[1:] if stack and stack[0][0] == 0 else stack
    if target is None:
        assert state == 'B' and right[-1][0] == 2
    else:
        assert state=='A'
        assert normalize(left) == runs(target[0]), (left,runs(target[0]))
        assert normalize(right) == runs(reversed(target[1])), (right,runs(reversed(target[1])))


def local_rules(t):
    """All rows with parameters cover t=0,1,2,... ."""
    k = t+3
    def ones(x):
        return (1,x)
    def fours(x):
        return (4,x)
    yield (([9,4,ones(k)], [1,1,9]), ([9,ones(k+3)], [9]), 4*k+8)
    yield (([1,ones(k)], [1,1,1,9]), ([1,fours(k+1),1,1,1],[9]), 2*k+13)
    yield (([1,ones(k)], [1,1,2]), ([1,fours(k+1),1,1],[1]), 2*k+12)
    yield (([1,ones(k)], [1,2]), None, 2*k+5)
    yield (([1,ones(k)], [2]), ([1,fours(k-2),ones(ZERO+7)],[1]), 2*k+60)
    yield (([1,4,ones(k)], [2]), ([1,fours(k+1),ones(ZERO+5)],[1]), 6*k+46)
    yield (([9,4,4,ones(k)], [2]), ([9,ones(k+4)],[1]), 8*k+22)
    yield (([9,4,ones(k)], [1,2]), ([9,ones(k+2)],[1]), 4*k+7)
    yield (([9,4,4,4,ones(t)], [1]), ([9,ones(t+7)],[1]),12*t+56)
    yield (([1,ones(t+4)],[1]),([1,fours(ZERO+6),1,1,1],[ones(t),2]),3*t+69)
    yield (([1,4,ones(t)],[1]),([1,fours(t+1),ones(ZERO+7)],[1]),6*t+76)
    yield (([1,4,4,ones(t)],[1]),([1,fours(t+4),ones(ZERO+5)],[1]),10*t+74)


def verify():
    if not __debug__:
        raise RuntimeError("Run with Python assertions enabled")
    assert Path(__file__).with_name("BB2x5_Rocq_holdouts_37.txt").read_text().splitlines()[3] == MACHINE
    # Split off the small counts, so that all run lengths encountered by the
    # remaining symbolic case have fixed sign throughout n >= 0.
    for t in [Lin(0,i) for i in range(12)]+[Lin(1,12)]:
        for row,(start,target,time) in enumerate(local_rules(t)):
            try:
                verify_rule(start,target,time)
            except Exception as e:
                raise AssertionError(f"rule {row}, parameter {t}") from e
    for b,target,cost in [(0,([1,1,1,1,1],[1]),33),(1,([1,4,4,4]+[1]*7,[1]),107),
                          (2,None,55),(3,([1]+[4]*6+[1]*2,[1]),65)]:
        verify_rule(([1]*(b+1),[1]), target, ZERO+cost)
    verify_rule(([],[]),([1,4,4]+[1]*7,[1]), ZERO+93)
    print("12 universal local rules, four short B exceptions, and blank initialization verified")


if __name__ == "__main__":
    verify()
