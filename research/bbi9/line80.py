"""Check an inductive nonhalting certificate for BBi(9), six states, three symbols, line 80."""

MACHINE = "1RB---2LF_2LC------_---2LD---_0LE---0LD_2RE---2RA_------0RE"
SYMBOLS = "012"

# Each pair is read left to right. The index is the parity of its left cell.
LEFT = (set("00 02 22".split()), set("00 01 02 20 21 22".split()))
RIGHT = (set("00 22".split()), set("00 02 20 22".split()))

# Each row gives head parity, state, and five-cell words in physical tape order.
WINDOWS = """
0 A 00000 02000 02002 02220 02222 22000 22002
0 C 00120 02120 02122 22120 22122
0 D 00000 00002 00200 00202 02000 02002 02200 02202 22000 22002 22200 22202
0 E 00000 00002 00220 00222 02000 02002 22000 22002 22220 22222
0 F 00220 00222 02220 02222 22220 22222
1 A 02200 02222 22200 22222
1 B 01000 21000 21022
1 D 00000 00022 00200 00222 02200 02222 20000 20022 20200 20222 22200 22222
1 E 00000 00200 00222 02000 02022 02200 20000 20200 20222 22000 22022 22200
1 F 00222 20222
"""


def check(machine):
    rows = machine.split("_")
    if len(rows) != 6 or any(len(row) != 9 for row in rows):
        raise ValueError("Expected a six-state, three-symbol table")
    moves = {}
    for state, row in zip("ABCDEF", rows):
        for index, symbol in enumerate(SYMBOLS):
            instruction = row[3 * index:3 * index + 3]
            if instruction == "---":
                continue
            write, direction, target = instruction
            if write not in SYMBOLS or direction not in "LR" or target not in "ABCDEF":
                raise ValueError(f"Invalid instruction {instruction}")
            moves[state, symbol] = (write, direction, target)

    allowed = set()
    for row in WINDOWS.strip().splitlines():
        parity, state, *words = row.split()
        allowed.update((int(parity), state, word) for word in words)
    if (0, "A", "00000") not in allowed or any("00" not in band for band in LEFT + RIGHT):
        raise ValueError("Blank tape fails the invariant")

    edges = 0
    for parity, state, word in sorted(allowed):
        a, b, current, d, e = word
        if (state, current) not in moves:
            raise ValueError(f"Undefined {state}{current} in an admitted window")
        write, direction, target = moves[state, current]
        other = 1 - parity
        if direction == "R":
            # The pair (x-1,x) joins the left half. The exterior (x+2,x+3)
            # supplies the new cell. Every other required pair is inherited.
            if b + write not in LEFT[other]:
                raise ValueError(f"Uncovered left pair after {state} {word}")
            successors = [b + write + d + e + s for s in SYMBOLS if e + s in RIGHT[parity]]
        else:
            # The pair (x,x+1) joins the right half. The exterior (x-3,x-2)
            # supplies the new cell.
            if write + d not in RIGHT[parity]:
                raise ValueError(f"Uncovered right pair after {state} {word}")
            successors = [s + a + b + write + d for s in SYMBOLS if s + a in LEFT[other]]
        if not successors:
            raise ValueError(f"No tape extension for {state} {word}")
        for following in successors:
            if (other, target, following) not in allowed:
                raise ValueError(f"Missing successor {other} {target} {following}")
            edges += 1
    return len(allowed), edges


if __name__ == "__main__":
    contexts, edges = check(MACHINE)
    print(f"NONHALTS from blank: {contexts} head contexts, {edges} one-step extensions checked")
