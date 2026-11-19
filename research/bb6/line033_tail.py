"""Blank-tape replay and parametric tail lemmas for BB(6) line 33 (ID 9146).

Use bbtools from Fractal Geometry Explorer, revision
c409c4b292369cb404e939753004bd1216fa3333. See line033-tail.md.
All clocks count defined elementary transitions. A stop at F1 costs no move.
"""

import argparse
from functools import lru_cache
from hashlib import sha256

from bbtools import symtm as tm
from bbtools.machine import Machine

TABLE = "1RB0LF_1LC0RB_0LD1LA_0RA1LE_0LA0RA_1LA---"
MACHINE = Machine.parse(TABLE)
ROUND_PREFIX = tuple(map(int, "10101010110"))
P = "10"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def known_prefix(right, length):
    """Return just the cells guaranteed present for every parameter value."""
    result = []
    for term in right:
        if len(result) == length:
            break
        if isinstance(term, int):
            result.append(term)
        elif isinstance(term, tm.Rep):
            need = length - len(result)
            copies = min(term.n.k, (need + len(term.word) - 1) // len(term.word))
            result.extend((term.word * copies)[:need])
            if not term.n.is_const() and len(result) < length:
                break
        else:
            break
    return tuple(result)


def at_edge(config):
    return (not config.steps.is_zero() and config.state == 0
            and config.left == [tm.Blank()] and config.right[0] == 1)


def at_round(config):
    return at_edge(config) and known_prefix(config.right, len(ROUND_PREFIX)) == ROUND_PREFIX


class SplitPower(Exception):
    """A zero repeat and a positive repeat would need different tokenizations."""


def token_word(terms):
    """Encode a bitstring as successive counts of ones before a zero.

    Keep a trailing unterminated run of ones at an arbitrary suffix. Only a
    blank suffix permits dropping terminal zeros or borrowing a final zero.
    """
    out = []
    pending = 0

    def add(symbol, count):
        count = tm.lin(count)
        if count.is_zero():
            return
        require(count.surely_ge(0), "negative token multiplicity")
        if out and out[-1][0] == symbol:
            out[-1] = (symbol, out[-1][1] + count)
        else:
            out.append((symbol, count))

    def bit(b):
        nonlocal pending
        if b:
            pending += 1
        else:
            add(pending, 1)
            pending = 0

    for term in terms[:-1]:
        if isinstance(term, int):
            bit(term)
            continue
        require(isinstance(term, tm.Rep) and term.n.surely_ge(0), "invalid repeat")
        if term.n.is_const() and term.n.k <= 40:
            for b in term.word * term.n.k:
                bit(b)
            continue
        parts = "".join(map(str, term.word)).split("0")
        require(len(parts) >= 2, "a repeated word has no zero")
        before, after = len(parts[0]), len(parts[-1])
        width = before + after
        require(all(len(part) == width for part in parts[1:-1]),
                "repeated word has unequal cyclic gaps")
        count = (len(parts) - 1) * term.n
        if pending != after:
            if not term.n.surely_ge(1):
                raise SplitPower(term)
            add(pending + before, 1)
            count = count - 1
        add(width, count)
        pending = after

    end = terms[-1]
    if isinstance(end, tm.Blank):
        if pending:
            add(pending, 1)
        if out and out[-1][0] == 0:
            out.pop()
        return tuple(out), 0, "blank"
    require(isinstance(end, tm.Ctx), "missing far tape")
    return tuple(out), pending, end.name


def check_rule(name, start, target, cost, stop=at_edge):
    config = tm.Config.parse("0^inf A> " + start)
    try:
        tm.run(MACHINE, config, stop, rotate=True, max_moves=10000)
    except tm.Halted:
        require(target is None and config.state == 5 and config.right[0] == 1,
                f"{name}: unexpected halt")
    else:
        require(target is not None and config.state == 0 and config.left == [tm.Blank()],
                f"{name}: unexpected end of sweep")
        require(token_word(config.right) == token_word(tm.tokens(target)),
                f"{name}: right tape disagrees")
    require(config.steps == tm.parse_lin(cost), f"{name}: clock disagrees")
    print(f"{name}: verified, {config.steps} defined steps")


def check_tail_lemmas():
    # Lower bounds on parameters are encoded by positive constants.
    check_rule("TD conversion",
               "(10)^6*j+7 110 10 10010 (110110)^j 110 1 (10)^m 1 (10)^9 0101101 0^inf",
               "(10)^4 110 (10)^6*j+8 1110 (10)^3*j+m+6 110 (10)^6 0 10 110110 1 0^inf",
               "210*j+14*m+556", at_round)
    check_rule("race sweep",
               "(10)^a+1 110 (10)^b+1 1110 (10)^m+1 110 (10)^c+2 0 10 R",
               "(10)^a+4 110 (10)^b 1110 (10)^m+2 110 (10)^c 0 10 110 R",
               "14*a+8*b+14*m+8*c+131")
    check_rule("left gap exhausted",
               "(10)^a+1 110 1110 (10)^m+1 110 (10)^c+2 0 10 R",
               "(10)^a+4 11110 (10)^m+2 110 (10)^c 0 10 110 R",
               "14*a+14*m+8*c+123")
    check_rule("four ones to F1",
               "(10)^a+1 11110 (10)^m+1 110 (10)^c+3 0 10 R",
               None, "6*a+28*m+16*c+172")
    check_rule("right gap exhausted",
               "(10)^a+1 110 (10)^b+1 1110 (10)^m+1 110 0 10 R",
               "(10)^a+4 110 (10)^b 0 10 110 (10)^m 1110 110 R",
               "14*a+8*b+8*m+103")
    check_rule("two pairs consumed",
               "(10)^a+1 110 (10)^b+2 0 10 (110)^d+1 R",
               "(10)^a+4 110 (10)^b 0 10 (110)^d+2 R",
               "14*a+8*b+75")
    check_rule("odd j conversion",
               "(10)^18*v+31 110 0 10 (110110)^3*v+3 (10)^6*v+m+11 1110 (110)^6 1 0^inf",
               "(10)^4 110 (10)^18*v+29 1110 (10)^9*v+10 110 (10)^6*v+m+10 0 (10)^13 0^inf",
               "426*v+8*m+915")
    check_rule("even j conversion",
               "(10)^18*v+22 110 0 10 (110110)^3*v+1 110 (10)^6*v+m+8 1110 (110)^6 1 0^inf",
               "(10)^4 110 (10)^18*v+20 0 (10)^9*v+7 110 (10)^6*v+m+7 0 (10)^13 0^inf",
               "426*v+8*m+699")


def template_for(tape, periods, padding):
    """An input run has length base + period * v_i, or is a literal."""
    template = []
    values = {}
    for i, (symbol, length) in enumerate(tape):
        period = periods.get(i, 1)
        if length < padding + 2 * period:
            template.append((symbol, length, 0))
        else:
            base = padding + (length - padding) % period
            template.append((symbol, base, period))
            values[f"v{i}"] = (length - base) // period
    return tuple(template), values


@lru_cache(maxsize=32000)
def one_sweep(template):
    right = []
    for i, (symbol, base, period) in enumerate(template):
        tile = (1,) * symbol + (0,)
        if period:
            exponent = tm.Lin(f"v{i}") + base // period
            right.append(tm.Rep(tile * period, exponent))
            right.extend(tile * (base % period))
        else:
            right.extend(tile * base)
    config = tm.Config([tm.Blank()], 0, right + [tm.Blank()])
    try:
        tm.run(MACHINE, config, at_edge, rotate=True, max_moves=10000)
    except tm.Halted:
        require(config.state == 5 and config.right[0] == 1, "unexpected stop")
        return None, config.steps
    result, _, suffix = token_word(config.right)
    require(suffix == "blank" and config.steps.surely_ge(1), "invalid return")
    return result, config.steps


def get_rule(tape, paddings):
    for padding in paddings:
        periods = {}
        for _ in range(len(tape) + 1):
            template, values = template_for(tape, periods, padding)
            try:
                target, cost = one_sweep(template)
                return template, values, target, cost
            except (tm.NeedSplit, SplitPower) as split:
                variables = split.args[0].n.vars()
                if len(variables) != 1:
                    break
                i = int(next(iter(variables))[1:])
                if i in periods:
                    break
                periods[i] = 2
    raise RuntimeError("could not establish a sweep for these run lengths")


def concrete(runs, values):
    result = []
    for symbol, length in runs:
        n = length.subs(values)
        require(n >= 0, "negative run on substitution")
        if not n:
            continue
        if result and result[-1][0] == symbol:
            result[-1] = (symbol, result[-1][1] + n)
        else:
            result.append((symbol, n))
    return tuple(result)


def advance(tape, paddings, remaining=None):
    template, values, target, cost = get_rule(tape, paddings)
    first_cost = cost.subs(values)
    if target is None:
        return None, first_cost, 0
    next_tape = concrete(target, values)
    if tuple(s for s, _, _ in template) != tuple(s for s, _ in target):
        return next_tape, first_cost, 1

    # Repeat only if this exact symbolic rule translates every variable by a
    # constant, preserves residue classes, and fixes all literal run lengths.
    limits = []
    changes = {}
    for i, ((_, base, period), (_, output)) in enumerate(zip(template, target)):
        if period == 0:
            if output != base:
                return next_tape, first_cost, 1
            continue
        var = f"v{i}"
        delta = output.k - base
        if output.c != {var: period} or delta % period:
            return next_tape, first_cost, 1
        changes[var] = delta // period
        if changes[var] < 0:
            limits.append(values[var] // -changes[var] + 1)
    if not limits:
        raise RuntimeError("a reachable rule closes with positive time; inspect for a nonhalting proof")

    times = min(limits)
    if remaining is not None:
        require(remaining > 0, "positive return budget required")
        times = min(times, remaining)
    last = {v: x + (times - 1) * changes[v] for v, x in values.items()}
    require(all(n >= 0 for n in last.values()), "jump left its proved domain")
    cost_delta = sum(cost.c.get(v, 0) * dx for v, dx in changes.items())
    elapsed = times * first_cost + (times * (times - 1) // 2) * cost_delta
    return concrete(target, last), elapsed, times


def literal(word, limit):
    ones = {i for i, bit in enumerate(word) if bit == "1"}
    state = head = 0
    for elapsed in range(limit):
        op = MACHINE.table[state][int(head in ones)]
        if op is None:
            return elapsed, state, head, ones
        write, direction, state = op
        if write:
            ones.add(head)
        else:
            ones.discard(head)
        head += direction
    return limit, state, head, ones


def check_altered_tape():
    prefix = P * 4 + "110"
    controls = (
        ("RS(7, TD(53))", prefix + P * 7 + "10010" + "1" + P * 53 + "1" + P * 9 + "0101101", 55945),
        ("W(4,32,1,4)", prefix + P * 32 + "1110" + P + "110" + P * 4 + "0" + P * 13, 45292),
    )
    for name, word, expected in controls:
        elapsed, state, head, ones = literal(word, expected + 1)
        require((elapsed, state, head in ones) == (expected, 5, True), "altered-tape control failed")
        print(f"{name} reaches F1 after {expected:,} defined steps.")


def blank_seed():
    elapsed, state, head, ones = literal("", 1817)
    word = P * 4 + "110" + P * 13 + "10010" + P * 11 + "1"
    require(elapsed == 1817 and state == 0
            and ones == {head + i for i, bit in enumerate(word) if bit == "1"},
            "initial blank segment disagrees")
    runs, _, _ = token_word(tm.tokens(word + " 0^inf"))
    return concrete(runs, {})


def cross_check(endpoint, expected_clock, expected_tape):
    tape = blank_seed()
    clock = 1817
    returns = batches = 0
    while returns < endpoint:
        tape, elapsed, count = advance(tape, (9, 12, 18), endpoint - returns)
        require(tape is not None and count > 0, "second replay stopped early")
        clock += elapsed
        returns += count
        batches += 1
    require((clock, tape) == (expected_clock, expected_tape), "second replay disagrees")
    print(f"Second grouping: {batches} batches, same complete tape and exact clock.")


def orbit(batches, repeat):
    tape = blank_seed()
    clock = 1817
    returns = 0
    for i in range(1, batches + 1):
        tape, elapsed, count = advance(tape, (4, 8, 16))
        clock += elapsed
        returns += count
        if tape is None:
            print(f"F1 after {clock} defined transitions, batch {i}")
            return
    # Hash the exact clock and the complete right tape, without displaying
    # thousands of digits. Left tape is blank and A scans the first bit.
    encoded = ",".join(f"{s}:{n:x}" for s, n in tape)
    print(f"{batches} batches, elementary clock bit length {clock.bit_length()}, "
          f"left-edge returns bit length {returns.bit_length()}")
    clock_digest = sha256(format(clock, "x").encode()).hexdigest()
    tape_digest = sha256(encoded.encode()).hexdigest()
    print("clock (hex) sha256:", clock_digest)
    print("tape (token:hex-length) sha256:", tape_digest)
    if clock.bit_length() <= 100:
        print("elementary clock:", clock)
    if batches == 60000:
        require(clock > 10**2387, "stated lower bound failed")
        require(clock_digest == "e1c2b2300a277fb618949a0c75a10f158b88afae1f0ee1661e36dc22628942c0"
                and tape_digest == "87ddf3368c1a3d023f0ae0351c175e1eaedfd04711a8018e0ab00f7ad840dbf9",
                "published endpoint differs")
        print("More than 10^2387 defined elementary transitions from blank.")
    if repeat:
        cross_check(returns, clock, tape)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--batches", type=int, default=60000)
    parser.add_argument("--cross-check", action="store_true",
                        help="repeat to the same edge return using different group sizes")
    options = parser.parse_args()
    if options.batches < 0:
        parser.error("negative batch budget")
    # The pinned machine is immutable. Cache literal finite-tile executions
    # used by bbtools to establish repeat crossings.
    tm._one_copy_left = lru_cache(maxsize=32768)(tm._one_copy_left)
    tm._one_copy_right = lru_cache(maxsize=32768)(tm._one_copy_right)
    check_tail_lemmas()
    check_altered_tape()
    orbit(options.batches, options.cross_check)
