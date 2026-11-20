#!/usr/bin/env python3
"""Generate and audit a sufficient global halting obligation for #758/#153.

The mathematical proof and the unresolved full-target status are in
GLOBAL_SAFETY_758.md. This standard-library script emits exact integer Horn
rules; it does not invoke a solver or claim a decision.

Default: focused arithmetic and scalar-transition audits.
--emit target: the full known blank-checkpoint to basin obligation.
--emit toy-safe / toy-cross: positive and negative controls with an empty basin.
--strengthened: add proved provenance and sufficient carry-to-basin stops.
"""
from fractions import Fraction
import re

from check_bb33 import HALTING_TARGET, champion_step
from excursion_power_758 import PAIRS


BLANK_SEED = 150124733170248900
BASIN_LOWER = HALTING_TARGET-160391744210493965542
BASIN_UPPER = HALTING_TARGET-3403055
CASES = {
    "target": (BLANK_SEED, BASIN_LOWER, BASIN_UPPER),
    "toy-safe": (12, 32, 31),
    "toy-cross": (12, 30, 29),
}


def integer_literal(value):
    """SMT-LIB negative integers use unary minus, not a signed numeral."""
    return str(value) if value >= 0 else f"(- {-value})"


def classify(u, d):
    """Return (label, predicate, arguments, raw_calls) for an ordinary state.

    Ord(u,d) means a=2u-4d-1 >= 3 and c=2d+1 >= 1.  Its next macro is
    one J/E or a two-bulk pair or bulk/reset.  The unrepresented complement
    halts on its second raw call.  Pair endpoints at a=1 go to Reset.
    """
    if not (isinstance(u, int) and isinstance(d, int) and d >= 0
            and u-2*d >= 2):
        raise ValueError("require integer d>=0 and u-2d>=2")
    candidates = []
    if u <= 3*d+1:
        candidates.append(("J", "Ord", (u+2, 3*d-u+1), 1))
    v, b = PAIRS[d % 4]
    next_d = (9*d+b)//4
    next_u = u+v
    next_h = next_u-2*next_d
    if next_h >= 1:
        if next_h == 1:
            candidates.append(("P"+str(d % 4), "Reset", (next_u,), 2))
        else:
            candidates.append(("P"+str(d % 4), "Ord", (next_u, next_d), 2))
    if d % 2 == 0 and 3*d+2 <= u and 2*u <= 9*d+9:
        candidates.append(("LR0", "Reset", (u+5,), 2))
    if d % 2 == 1 and 3*d+3 <= u and 2*u <= 9*d+14:
        candidates.append(("LR1", "Reset", (u+7,), 2))
    if d % 2 == 1 and u == 3*d+2:
        candidates.append(("E", "Ord", (u+4, 0), 1))
    if len(candidates) > 1:
        raise AssertionError((u, d, candidates))
    return candidates[0] if candidates else ("Halt", None, (), 2)


def literal_macro(u, d):
    """Check the proposed macro directly against the published scalar map."""
    label, predicate, args, calls = classify(u, d)
    state = (2*u-4*d-1, 2*d+1)
    for index in range(calls):
        assert state is not None
        state = champion_step(*state)
        if state is None:
            assert predicate is None and index == calls-1
            return label, predicate, args, calls
        if index < calls-1:
            assert state[0] != 1
    assert predicate is not None
    expected = ((1, args[0]) if predicate == "Reset" else
                (2*args[0]-4*args[1]-1, 2*args[1]+1))
    assert state == expected, (u, d, label, state, expected)
    return label, predicate, args, calls


def baseline_smt(seed, lower, upper):
    """Return a linear-integer Horn problem for a supplied certified basin.

    Reset seeds in [lower,upper] are successful stops.  Other successful
    stops are the exact halting complement of the live grouped rules.
    Bad records either predicate at mass coordinate >upper.  Source caps
    do not cap a destination: every crossing endpoint remains reachable.
    """
    if not (all(isinstance(x, int) for x in (seed, lower, upper))
            and seed >= 1 and 1 <= lower <= upper+1):
        raise ValueError("require positive integer seed and 1<=lower<=upper+1")
    lines = [
        "; Exact grouped #758 rules. Basin membership is an external theorem.",
        "(set-logic HORN)",
        "(set-option :fp.engine spacer)",
        "(declare-rel Reset (Int))",
        "(declare-rel Ord (Int Int))",
        "(declare-rel Bad ())",
        "(declare-var u Int)",
        "(declare-var d Int)",
        "(declare-var s Int)",
        "(declare-var q Int)",
        f"(rule (Reset {seed}))",
        f"(rule (=> (and (Reset s) (> s {upper})) Bad))",
        f"(rule (=> (and (Ord u d) (> u {upper})) Bad))",
        "; Reset sources below the certified basin; first real call included.",
        f"(rule (=> (and (Reset (+ (* 2 q) 1)) (>= q 0) "
        f"(< (+ (* 2 q) 1) {lower})) (Ord (+ (* 2 q) 3) q)))",
        f"(rule (=> (and (Reset (* 2 q)) (>= q 1) (< (* 2 q) {lower})) "
        "(Ord (+ (* 2 q) 4) (+ q 1))))",
        "; J: the odd/odd jump.  Its result has h>=6.",
        f"(rule (=> (and (Ord u d) (>= d 0) (>= u (+ (* 2 d) 2)) "
        f"(<= u {upper}) (<= u (+ (* 3 d) 1))) "
        "(Ord (+ u 2) (- (+ (* 3 d) 1) u))))",
    ]
    for residue, (gain, offset) in enumerate(PAIRS):
        constant = (9*residue+offset)//4
        assert 4*constant == 9*residue+offset
        d_expr = f"(+ (* 4 q) {residue})"
        next_d = f"(+ (* 9 q) {constant})"
        next_u = f"(+ u {gain})"
        next_h = f"(- {next_u} (* 2 {next_d}))"
        body = (f"(Ord u {d_expr}) (>= q 0) "
                f"(>= u (+ (* 8 q) {2*residue+2})) (<= u {upper})")
        lines += [
            f"; P residue {residue}: endpoint h>=1 proves both bulk guards.",
            f"(rule (=> (and {body} (= {next_h} 1)) (Reset {next_u})))",
            f"(rule (=> (and {body} (>= {next_h} 2)) "
            f"(Ord {next_u} {next_d})))",
        ]
    lines += [
        "; Low-carry bulk followed by reset, including an even left zero.",
        f"(rule (=> (and (Ord u (* 2 q)) (>= q 0) (<= u {upper}) "
        "(>= u (+ (* 6 q) 2)) (<= (* 2 u) (+ (* 18 q) 9))) "
        "(Reset (+ u 5))))",
        "; High-carry bulk followed by reset.",
        f"(rule (=> (and (Ord u (+ (* 2 q) 1)) (>= q 0) (<= u {upper}) "
        "(>= u (+ (* 6 q) 6)) (<= (* 2 u) (+ (* 18 q) 23))) "
        "(Reset (+ u 7))))",
        "; The exceptional restart remains an exact live transition.",
        f"(rule (=> (and (Ord u (+ (* 2 q) 1)) (>= q 0) (<= u {upper}) "
        "(= u (+ (* 6 q) 5))) (Ord (+ u 4) 0)))",
        "(query Bad)",
    ]
    return "\n".join(lines)+"\n"


def verify_partition(limit=200):
    count = 0
    for u in range(2, limit):
        for d in range((u-2)//2+1):
            literal_macro(u, d)
            count += 1
    for seed in range(1, limit):
        state = champion_step(1, seed)
        if seed % 2:
            u, d = seed+2, (seed-1)//2
        else:
            u, d = seed+4, (seed+2)//2
        assert state == (2*u-4*d-1, 2*d+1)
    return count


def parse_smt(source):
    """Parse this generated SMT subset; strings and quoted symbols are unused."""
    source = re.sub(r";[^\n]*", "", source)
    tokens = re.findall(r"\(|\)|[^\s()]+", source)
    stack, roots = [], []
    for token in tokens:
        if token == "(":
            value = []
            (stack[-1] if stack else roots).append(value)
            stack.append(value)
        elif token == ")":
            if not stack:
                raise ValueError("unmatched close parenthesis")
            stack.pop()
        else:
            if not stack:
                raise ValueError("top-level atom")
            stack[-1].append(token)
    if stack:
        raise ValueError("unclosed parenthesis")
    return roots


def render(value):
    if isinstance(value, list):
        return "("+" ".join(render(item) for item in value)+")"
    return str(value)


def first_forbidden_bulk_length(upper):
    """Smallest b with 8*3^b > (upper+7)*2^b, using exact integers."""
    b, numerator, denominator = 0, 1, 1
    while 8*numerator <= (upper+7)*denominator:
        b += 1
        numerator *= 3
        denominator *= 2
    return b


def bulk_lengths(upper):
    return tuple(range(1, first_forbidden_bulk_length(upper), 2))


def provenance(u, d):
    h = u-2*d
    return (h in (2, 3, 6) or d % 9 in (2, 5) or h % 9 == 0
            or (u+d) % 27 in (9, 18) or (d == 0 and h % 6 == 3))


def terminal_cone(u, d, bulks, lower, upper):
    if not (d >= 0 and u-2*d >= 2 and bulks >= 1 and bulks % 2 == 1):
        return False
    n, q = 3**bulks, 2**bulks
    return (3*n*(2*d+8) >= q*(2*u+9*bulks+22)
            and 2*n*(2*d+14) <= q*(2*u+5*bulks+27)
            and lower <= u+(5*bulks+5)//2
            and u+(9*bulks+5)//2 <= upper)


def definitions(lower, upper):
    h = "(- u (* 2 d))"
    provenance_source = f"""
      (define-fun P2_758 ((u Int) (d Int)) Bool
        (or (= {h} 2) (= {h} 3) (= {h} 6)
            (= (mod d 9) 2) (= (mod d 9) 5)
            (= (mod {h} 9) 0)
            (= (mod (+ u d) 27) 9) (= (mod (+ u d) 27) 18)
            (and (= d 0) (= (mod {h} 6) 3))))
    """
    terms = parse_smt(provenance_source)
    calls = []
    for b in bulk_lengths(upper):
        n, q = 3**b, 2**b
        source = f"""
          (define-fun BulkTerminal_{b} ((u Int) (d Int)) Bool
            (and (>= (* {3*n} (+ (* 2 d) 8))
                     (* {q} (+ (* 2 u) {9*b+22})))
                 (<= (* {2*n} (+ (* 2 d) 14))
                     (* {q} (+ (* 2 u) {5*b+27})))
                 (>= u {integer_literal(lower-(5*b+5)//2)})
                 (<= u {integer_literal(upper-(9*b+5)//2)})))
        """
        terms.extend(parse_smt(source))
        calls.append([f"BulkTerminal_{b}", "u", "d"])
    union = ["or", *calls] if calls else "false"
    terms.append(["define-fun", "CarrySafe_758", [["u", "Int"], ["d", "Int"]],
                  "Bool", ["and", [">=", "d", "0"],
                           [">=", ["-", "u", ["*", "2", "d"]], "2"], union]])
    return terms


def strengthened_terms(seed, lower, upper):
    original = parse_smt(baseline_smt(seed, lower, upper))
    definitions_ = definitions(lower, upper)
    output, changed = [], 0
    for term in original:
        if term[:1] == ["set-logic"]:
            output.append(term)
            output.extend(definitions_)
            continue
        if term[:1] != ["rule"] or not isinstance(term[1], list):
            output.append(term)
            continue
        implication = term[1]
        if implication[:1] != ["=>"] or implication[2] == "Bad":
            output.append(term)
            continue
        body, head = implication[1], implication[2]
        assert body[0] == "and"
        ordinary = [item for item in body[1:]
                    if isinstance(item, list) and item[:1] == ["Ord"]]
        if not ordinary:
            output.append(term)
            continue
        assert len(ordinary) == 1 and head[0] in ("Ord", "Reset")
        u, d = ordinary[0][1:]
        # These are additional predicates on the actual source.  The head
        # (in particular every possible crossing endpoint) is unchanged.
        output.append(["rule", ["=>", [*body, ["P2_758", u, d],
                                        ["not", ["CarrySafe_758", u, d]]], head]])
        changed += 1
    assert changed == 12
    return original, output


def strengthened_smt(seed, lower, upper):
    original, output = strengthened_terms(seed, lower, upper)
    return ("; Proved P2 provenance and sufficient carry-to-basin stops.\n"
            "; All live destinations and Bad predicates remain uncapped.\n"
            + "\n".join(render(term) for term in output)+"\n")


def verify_strengthening():
    checked = 0
    for u in range(2, 200):
        for d in range((u-2)//2+1):
            if not provenance(u, d):
                continue
            label, predicate, args, calls = literal_macro(u, d)
            if predicate == "Ord":
                assert provenance(*args), (u, d, label, args)
            checked += 1
    for seed in range(1, 200):
        u, d = ((seed+2, (seed-1)//2) if seed % 2
                else (seed+4, (seed+2)//2))
        assert provenance(u, d)

    for b in (1, 3, 9, 51, 201, 785):
        c, r = 101, Fraction(3, 2)**b
        low = 2*r*(c+13)-5*b-26
        high = 3*r*(c+7)-9*b-21
        mass = (low+high)//2
        mass += 1-mass % 2
        assert low <= mass <= high and mass-2*c >= 3
        u, d = (mass-1)//2, (c-1)//2
        lower, upper = u+(5*b+5)//2, u+(9*b+5)//2
        assert terminal_cone(u, d, b, lower, upper)
        assert b in bulk_lengths(upper)
        state = (mass-2*c, c)
        for _ in range(b):
            assert state[0] >= 4*((state[1]+1)//4)+3
            state = champion_step(*state)
            assert state is not None and state[0] != 1
        assert state[0] % 2 == 0 and state[0] <= state[1]
        state = champion_step(*state)
        assert state[0] == 1 and lower <= state[1] <= upper
        assert not terminal_cone(u, d, b, lower+1, upper)
        assert not terminal_cone(u, d, b, lower, upper-1)

    upper = HALTING_TARGET-3403055
    lower = HALTING_TARGET-160391744210493965542
    lengths = bulk_lengths(upper)
    assert first_forbidden_bulk_length(upper) == 787
    assert len(lengths) == 393 and lengths[-1] == 785
    original, strengthened = strengthened_terms(150124733170248900, lower, upper)
    original_rules = [term for term in original if term[:1] == ["rule"]]
    new_rules = [term for term in strengthened if term[:1] == ["rule"]]
    assert len(original_rules) == len(new_rules)
    changed = 0
    for old, new in zip(original_rules, new_rules):
        if old == new:
            continue
        assert old[1][0] == new[1][0] == "=>"
        assert old[1][2] == new[1][2] and old[1][2] != "Bad"
        assert old[1][1] == new[1][1][:-2]
        assert new[1][1][-2][0] == "P2_758"
        assert new[1][1][-1][0] == "not"
        changed += 1
    assert changed == 12
    return checked, len(lengths)


def smt(seed, lower, upper, *, strengthened=False):
    """Emit one exact sufficient safety problem, without invoking a solver."""
    generator = strengthened_smt if strengthened else baseline_smt
    return generator(seed, lower, upper)


def verify_controls():
    # These are complete paths, so the safe control also has an explicit
    # finite inductive invariant independently of any solver result.
    trace = [("Reset", (12,)), ("Ord", (16, 7)), ("Ord", (18, 6)),
             ("Ord", (20, 1)), ("Ord", (29, 11)), ("Ord", (31, 5))]
    assert champion_step(1, 12) == (3, 15)
    for (_, current), (predicate, following) in zip(trace[1:], trace[2:]):
        _, actual_predicate, actual_arguments, _ = literal_macro(*current)
        assert (actual_predicate, actual_arguments) == (predicate, following)
    assert literal_macro(31, 5) == ("Halt", None, (), 2)
    assert max(arguments[0] for _, arguments in trace) == 31
    for name in ("toy-safe", "toy-cross"):
        seed, lower, upper = CASES[name]
        assert lower == upper+1  # no supplied halting-basin assumption
        for strengthened in (False, True):
            text = smt(seed, lower, upper, strengthened=strengthened)
            assert parse_smt(text)[-1] == ["query", "Bad"]
    # The strengthened toy-safe problem's terminal cones cannot stop a
    # source, because a nonempty output interval cannot fit in an empty basin.
    for _, state in trace[1:]:
        for b in bulk_lengths(31):
            assert not terminal_cone(*state, b, 32, 31)


def verify():
    ordinary = verify_partition()
    provenance_cases, cones = verify_strengthening()
    verify_controls()
    assert len(parse_smt(baseline_smt(*CASES["target"]))) > 0
    print("Exact grouped scalar comparisons:", ordinary)
    print("Provenance preservation comparisons:", provenance_cases)
    print("Target carry-terminal conditions:", cones)
    print("Complete safe/crossing controls and unchanged-destination audit passed.")
    print("No full-target invariant or halting decision is supplied by these checks.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", choices=tuple(CASES),
                        help="emit the selected SMT-LIB Horn problem to stdout")
    parser.add_argument("--strengthened", action="store_true",
                        help="add proved provenance and carry-terminal conditions")
    args = parser.parse_args()
    if not __debug__:
        parser.error("enable assertions")
    if args.emit:
        print(smt(*CASES[args.emit], strengthened=args.strengthened), end="")
    else:
        verify()
