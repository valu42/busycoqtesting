"""Verify the spatially reflected table, unbounded left sweeps, and right calls."""

from collections import Counter, defaultdict
from itertools import product

ORIGINAL = "1RB0LF_1RC1RB_0RD0RC_1LE1LF_1LD---_0LB1LA"
MIRROR = "1LC0RF_1RE---_1LD1LC_0LE0LD_1RB1RF_0RC1RA"
ROOT = ("A", "101")
NORMAL = ("D", "011")
EXITS = {
    ROOT: {NORMAL},
    ("A", "111"): {("C", "111"), ("D", "000")},
    ("C", "100"): {("C", "111"), ("D", "000"), NORMAL},
    ("C", "110"): {("D", "001")},
}
DIGITS = (
    (0, "0000", "0110", None), (0, "0110", "0000", 0),
    (0, "0011", "0111", None), (0, "0111", "0011", 1),
    (1, "11", "11", 1), (1, "00", "10", None), (1, "10", "00", 0),
)
HEADERS = (("C", "00", "00"), ("A", "101", "011"))


def table(code):
    return {(q, bit): row[3*bit:3*bit+3]
            for q, row in zip("ABCDEF", code.split("_")) for bit in (0, 1)}


TM = table(MIRROR)


def verify_reflection():
    names = dict(zip("ABCDEF", "ACDEBF"))
    for (q, bit), action in table(ORIGINAL).items():
        derived = "---"
        if action != "---":
            write, move, dest = action
            derived = write + {"L": "R", "R": "L"}[move] + names[dest]
        assert TM[names[q], bit] == derived
    assert names["A"] == "A"


def ones(word, start):
    return {i for i, bit in enumerate(word, start) if bit == "1"}


def literal(q, h, tape):
    action = TM[q, int(h in tape)]
    assert action != "---", (q, h)
    if action[0] == "1":
        tape.add(h)
    else:
        tape.discard(h)
    return action[2], h + (1 if action[1] == "R" else -1)


def initialize():
    q, h, tape = "A", 0, set()
    for _ in range(301):
        q, h = literal(q, h, tape)
    word = "1"*11 + "10"*5 + "01110"
    assert q == "D" and tape == ones(word, h + 1 - 21)


def left_case(rule, a, b):
    if rule == "inc":
        assert b > 0
        inp, out, na, nb, mode, cost = "", "", a+4, b-1, "R", 2*a+12*b+6
    elif rule == "101":
        inp, out, na, nb, mode, cost = "101", "1", a+4, b, "L", 2*a+12*b+16
    elif rule == "11":
        inp, out, na, nb, mode, cost = "11", "", a+4, b, "R", 2*a+12*b+8
    else:
        assert rule == "over" and not b and a % 2
        inp, out, na, nb, mode, cost = "00", "0", 3, 2+a//2, "R", 4*a+23
    edge = 3 + len(inp)
    initial = "1"*a + "10"*b + "011" + inp
    final = "1"*na + "10"*nb + ("101" if mode == "R" else "011") + out
    finish_head = edge - len(out) - (4 if mode == "L" else 0)
    return (ones(initial, edge-len(initial)), ones(final, edge-len(final)),
            ("A" if mode == "R" else "D", finish_head), edge, cost)


def duplicate(cells, cut):
    # Insert a copy of [cut,cut+2) just to its left. Anchor the right end.
    return ({p-2 if p < cut else p for p in cells}
            | {p-2 for p in cells if cut <= p < cut+2})


def check_left(rule, a, b):
    initial, final, finish, edge, cost = left_case(rule, a, b)
    q, h, tape = "D", -1, initial.copy()
    crossings, visits = defaultdict(list), Counter()
    for _ in range(cost):
        assert h < edge  # No inspection of the unknown right suffix.
        visits[h] += 1
        nq, nh = literal(q, h, tape)
        crossings[max(h, nh)].append((nq, nh > h))
        q, h = nq, nh
    assert (q, h) == finish and tape == final
    pumps = []
    if a == 7:
        pumps.append((-5 if rule == "over" else -2*b-a+2, a+2, b))
    if b == 4:
        pumps.append((-2*b+2, a, b+1))
    for cut, aa, bb in pumps:
        assert cut+2 <= min(-1, h)
        assert crossings[cut] == crossings[cut+2]
        ii, ff, hh, ee, cc = left_case(rule, aa, bb)
        assert duplicate(initial, cut) == ii and duplicate(final, cut) == ff
        assert (finish, edge) == (hh, ee)
        assert cost + visits[cut] + visits[cut+1] == cc
    if len(pumps) == 2:
        assert pumps[0][0]+2 <= pumps[1][0]


def check_digits():
    for mode, before, after, child in DIGITS:
        q, header, expected = HEADERS[mode]
        low, high = -len(header), len(before)
        h, tape, called = 0, ones(header+before, low), False
        for _ in range(100):
            if h < low:
                break
            if h == high:
                assert child is not None and not called
                cq, ch, co = HEADERS[child]
                cut = h-len(ch)
                assert (q, {p for p in tape if p >= cut}) == (cq, ones(ch, cut))
                tape.difference_update(range(cut, high))
                tape.update(ones(co, cut))
                q, h, called = "D", cut-1, True
                continue
            assert low <= h < high
            q, h = literal(q, h, tape)
        assert (q, h, tape) == ("D", low-1, ones(expected+after, low))
        assert called == (child is not None)


def pair_rules():
    # A child begins two cells to the right and borrows the preceding three
    # cells. After the child returns the head is just left of its new header.
    rules = {}
    for interface in EXITS:
        for pair in map("".join, product("01", repeat=2)):
            todo = [(interface[0], 3, ones(interface[1]+pair, 0), None, None)]
            children, outcomes = set(), {}
            while todo:
                q, h, tape, child, answer = todo.pop()
                for _ in range(100):
                    if h < 0:
                        word = "".join("1" if i in tape else "0" for i in range(5))
                        result = ((q, word[:3]), word[3:])
                        assert result[0] in EXITS[interface] and answer not in outcomes
                        outcomes[answer] = result
                        children.add(child)
                        break
                    if h == 5:
                        assert child is None  # At most one call on this pair.
                        header = "".join("1" if i in tape else "0" for i in range(2, 5))
                        child = (q, header)
                        for response in EXITS[child]:
                            newtape = {p for p in tape if p < 2} | ones(response[1], 2)
                            todo.append((response[0], 1, newtape, child, response))
                        break
                    q, h = literal(q, h, tape)
                else:
                    raise AssertionError("Unfinished pair path")
            assert len(children) == 1
            child = children.pop()
            assert set(outcomes) == (EXITS[child] if child else {None})
            rules[interface, pair] = child, outcomes
    # On a blank tail there are at most two further pairs to examine.
    for interface in EXITS:
        child = rules[interface, "00"][0]
        assert child is None or rules[child, "00"][0] is None
    return rules


def check_pair_outputs(rules):
    # The 16 verified pair cases imply the word-level boundary test.
    g, j, k = ("A", "111"), ("C", "100"), ("C", "110")
    c, d, e = ("C", "111"), ("D", "000"), ("D", "001")
    for pair in ("00", "01", "10", "11"):
        assert rules[k, pair] == (None, {None: (e, "1"+pair[1])})
    for x in "01":
        assert rules[j, "1"+x] == (None, {None: (NORMAL, "1"+x)})
    assert rules[j, "00"] == (k, {e: (d, "01")})
    assert rules[j, "01"] == (g, {c: (c, "11"), d: (d, "00")})
    for entry, zero_exit, one_exit in ((ROOT, NORMAL, NORMAL), (g, c, d)):
        for x in "01":
            assert rules[entry, "0"+x] == (None, {None: (zero_exit, "1"+x)})
        assert rules[entry, "11"] == (ROOT, {NORMAL: (one_exit, "11")})
        assert rules[entry, "10"] == (j, {c: (zero_exit, "11"),
                                            d: (one_exit, "00"),
                                            NORMAL: (one_exit, "11")})


def check_uniform_boundary():
    # Both paths inspect only a fixed right prefix. The same two-cell
    # crossing-sequence test as for the left rules pumps the uniform region.
    def path(kind, value):
        if kind == "enter":
            a = value
            init = ones("1"*a + "011", -a)
            end = ones("1"*(a+5), 3-(a+5))
            return init, end, ("D", -1), ("A", 3), 3, 2*a+6
        n = value
        init = ones("1"*(n+1), -n)
        end = ones("111" + "10"*((n-2)//2) + "101", 1-(n+4))
        return init, end, ("C", -4), ("A", 1), 1, 2*n+3

    for kind, values in (("enter", (3, 5, 7)), ("return", (8, 10, 12))):
        for value in values:
            init, end, (q, h), finish, edge, cost = path(kind, value)
            tape, crossings, visits = init.copy(), defaultdict(list), Counter()
            for _ in range(cost):
                assert h < edge
                visits[h] += 1
                nq, nh = literal(q, h, tape)
                crossings[max(nh,h)].append((nq, nh > h))
                q, h = nq, nh
            assert tape == end and (q, h) == finish
            if value == values[-1]:
                cut = -value+2
                ni, ne, ns, nf, eg, nc = path(kind, value+2)
                assert cut+2 <= min(ns[1], finish[1])
                assert crossings[cut] == crossings[cut+2]
                assert duplicate(init, cut) == ni and duplicate(end, cut) == ne
                assert (finish, edge, cost+visits[cut]+visits[cut+1]) == (nf, eg, nc)


def verify():
    assert __debug__, "Run Python without -O"
    verify_reflection()
    initialize()
    for rule in ("inc", "101", "11", "over"):
        for a in (3, 5, 7):
            for b in range(5):
                if (rule == "inc" and not b) or (rule == "over" and b):
                    continue
                check_left(rule, a, b)
    check_digits()
    check_uniform_boundary()
    rules = pair_rules()
    check_pair_outputs(rules)
    return rules
