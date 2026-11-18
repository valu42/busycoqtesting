"""Reproduce the line 6 local-factor obstruction and the conditional unary-test floor."""
import base64
from collections import Counter
import json
from pathlib import Path
import sys
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from frontiers.checkpoints import checksum, holdouts
from line6 import HEADER, MACHINE
from prior_sweeps import TapeMachine


# Euler-trail rearrangement of the interior of the extension-80 word.
# The fixed word makes the witness independent of any search or RNG.
ALTERED = (
    "32232330032232323200320032003232000000320032003200320032003203200323"
    "20032003200320032003200323200323232323032003200000032003200320032003"
    "20032003200320000320000320322303203223232323232333332333233323332333"
    "23333333323332333233323333323333323332333233333332333332333233323333"
    "33332333233032003200323200320032032"
)


def checkpoint_word(tm):
    return "".join(str(tm.tape.get(x, 0)) for x in range(tm.head + 1, max(tm.tape) + 1))


def left_extension(tm, position, limit):
    while tm.head > position and tm.steps < limit:
        assert tm.step(), "unexpected halt"
    assert tm.head == position and tm.state == "A" and min(tm.tape) == position + 1


def main():
    assert holdouts()[5] == MACHINE
    tm = TapeMachine(MACHINE)
    left_extension(tm, -80, 183_133)
    word = checkpoint_word(tm)
    assert tm.steps == 183_132 and len(word) == len(ALTERED) == 307
    assert word != ALTERED and word.startswith(HEADER) and ALTERED.startswith(HEADER)
    assert word[:15] == ALTERED[:15] and word[-18:] == ALTERED[-18:]
    for k in range(1, 8):
        def factors(w):
            padded = "0" * (k - 1) + w + "0" * (k - 1)
            return Counter(padded[i:i+k] for i in range(len(padded) - k + 1))
        assert factors(word) == factors(ALTERED)
    control = TapeMachine(MACHINE, map(int, word), left=1)
    left_extension(control, -2, 10_279)
    left_extension(tm, -82, 193_411)
    assert (control.steps, tm.steps) == (10_278, 193_410)
    assert {x - 80: v for x, v in control.tape.items()} == tm.tape
    assert (control.head - 80, control.state) == (tm.head, tm.state)
    changed = TapeMachine(MACHINE, map(int, ALTERED), left=1)
    for _ in range(1085):
        assert changed.step()
    assert not changed.step() and (changed.head, changed.state, changed.tape[97]) == (97, "A", 1)
    print("Extension 80 at 183132. Padded factor counts 1..7 agree. "
          "Altered halt at 1085. Control completes two extensions in 10278 steps.")

    snapshot = json.loads((ROOT / "frontiers/runs/window-06.json").read_text())
    p = snapshot["payload"]
    assert checksum(p) == snapshot["sha256"]
    tape = zlib.decompress(base64.b64decode(p["tape_zlib_base64"]))
    assert (p["machine"], p["left"], p["steps"], tape[0]) == (MACHINE, -16299, 10**10, 1)
    print("Inherited checkpoint contains a written 1 at -16299. Unary tests n=0..16298 succeed.")

    saved = json.loads(Path(__file__).with_name("probe6-checkpoint.json").read_text())
    end = saved["payload"]
    data = zlib.decompress(base64.b64decode(end["tape_zlib_base64"]))
    assert checksum(end) == saved["sha256"]
    assert (end["machine"], end["state"], end["head"], end["steps"], end["left"]) == (
        MACHINE, "A", -16_310, 10_087_506_894, -16_309)
    assert set(data) <= {0, 2, 3} and data.count(2) == 16_310
    if "--replay" in sys.argv[1:]:
        literal = TapeMachine(MACHINE, tape, head=p["head"], left=p["left"])
        literal.state, literal.steps = p["state"], p["steps"]
        left_extension(literal, -16_310, end["steps"] + 1)
        assert (literal.steps, literal.state, literal.head) == (end["steps"], end["state"], end["head"])
        assert literal.tape == {end["left"] + i: x for i, x in enumerate(data) if x}
        print("Fully replayed 87506894 defined steps. Complete tape and clock match the saved extension 16310.")



if __name__ == "__main__":
    if not __debug__:
        raise SystemExit("Run with assertions enabled.")
    main()
