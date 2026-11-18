"""Check the line-4 scalar executable against literal and two-coordinate returns."""
from pathlib import Path
import subprocess
import sys

from prior_sweeps import TapeMachine


MACHINE = "1RB3LA1LA1RA3RA_2LB2RA---4RB1LB"
MODULUS = 1_000_000_007


def check_tape(machine, left, right):
    start = machine.head - len(left)
    expected = {start + i: digit for i, digit in enumerate(left + right)}
    assert machine.state == "A" and machine.tape == expected


def check_literal():
    machine = TapeMachine(MACHINE)
    checkpoints = [
        (93, [1, 4, 4] + [1] * 7, [1]),
        (6393, [1] + [4] * 6 + [1] * 3, [1] * 71 + [2]),
        (172248, [1] + [4] * 6 + [1] * 3, [1] * 393 + [2]),
    ]
    for step, left, right in checkpoints:
        while machine.steps < step:
            assert machine.step()
        check_tape(machine, left, right)


def a_exit(b):
    """Apply the A rules in their original order. Return B(a,b) and width."""
    a = 6
    width = 0
    while b >= 2 * a + 3:
        a, b = 3 * a + 4, b - 2 * a - 3
        width += 1
    if b == 2 * a + 2:
        return (3 * a + 4, 2), width
    if b == 2 * a + 1:
        return None, width
    if b == 2 * a:
        return (3 * a + 1, 7), width
    if b == 2 * a - 2:
        return (3 * a + 1, 5), width
    pairs, odd = divmod(b, 2)
    if odd:
        return (a - pairs - 1, 3 * pairs + 5), width
    return (a - pairs - 2, 3 * pairs + 7), width


def b_return(a, b):
    while True:
        q, remainder = divmod(a, 3)
        if remainder == 0:
            assert 7 * q + b >= 4
            return 7 * q + b - 4
        if remainder == 1:
            a, b = 7 * q + b + 1, 7
        else:
            a, b = 7 * q + b + 4, 5


def run(program, arguments):
    return subprocess.run(
        [str(program.resolve()), *arguments], capture_output=True, text=True, check=False
    )


def check_program(program):
    samples = {1, 2, 3, 4, 5, 8, 16, 32, 64, 256, 1024}
    b = b_return(2, 7)
    for index in range(1, max(samples) + 1):
        state, width = a_exit(b)
        assert state is not None
        if index in samples:
            expected = (f"return={index} width={width} b_bits={b.bit_length()} "
                        f"b_mod_1000000007={b % MODULUS}\n")
            result = run(program, [str(index)])
            assert (result.returncode, result.stdout) == (0, expected), result
            if index == 1024:
                result = run(program, [])
                assert (result.returncode, result.stdout) == (0, expected), result
        b = b_return(*state)
    for arguments in [["0"], ["-2"], ["9x"], [""], ["1", "2"], [str(2**64)]]:
        result = run(program, arguments)
        assert result.returncode == 2 and result.stderr, result


def check_inverse_residues():
    modulus = 7**4
    surviving = set()
    for initial in range(modulus):
        value = initial
        for _ in range(4):
            q, digit = divmod(value, 7)
            if digit not in (1, 2):
                break
            value = 3 * q + digit - 1
        else:
            surviving.add(initial)
    assert len(surviving) == 16
    for phase in range(6):
        images = {
            (72 * pow(3, n, modulus) - 3*n - 13) % modulus
            for n in range(phase, 6 * modulus, 6)
        }
        assert len(images) == modulus


if __name__ == "__main__":
    if not __debug__ or len(sys.argv) != 2:
        sys.exit("Usage: python3 check_line4_scalar.py PATH_TO_EXECUTABLE (assertions enabled)")
    holdout_list = Path(__file__).with_name("BB2x5_Rocq_holdouts_37.txt")
    assert holdout_list.read_text().splitlines()[3] == MACHINE
    check_literal()
    check_program(Path(sys.argv[1]))
    check_inverse_residues()
    print("Literal tape through step 172248, sampled returns through 1024, CLI, and inverse residues passed.")
