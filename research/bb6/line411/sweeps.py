"""Replay complete line 411 sweeps and write an exact compressed checkpoint."""
import argparse
import ctypes
import hashlib
import json
import random
import sys
import zlib
from pathlib import Path
from line411 import add_calls, right_call, verify

HERE = Path(__file__).resolve().parent
CHECKPOINTS = {
    100: "8138d6a9990f450a8b24bbda3cf580d3d4d7d0012788a6451febb08a8edbdc1b",
    3338: "295ebd9de7ad57a451d95db7e3412c0ae62923825805a6399d504c283a943a9b",
    14500: "5b6a39734c074497e07a9f8186db9d11e4a0b9e4f0d592a29078b8ada59c9c0a",
    50000: "4483796bf9b931bcecef1c7fb97a357766f871d0646df915c00a142b36211c39",
    100000: "c109d1e574336f606ea1cbcd69f1f276d9ee18c0cde6f7d10626789be40e7d96",
    150000: "464631aba678b44b44b72ac0d19a4f497caad32813363c8f954a850472e099ea",
    500000: "191096ad5842098c978379eb43975731ee269bf7d0a605dda9347417a190b230",
}


def open_engine():
    lib = ctypes.CDLL(str(HERE / "sweep_power.so"))
    data_args = [ctypes.c_char_p, ctypes.c_size_t]
    lib.exponentiate.argtypes = data_args
    lib.take_boundary.argtypes = data_args + [ctypes.POINTER(ctypes.c_uint64)]
    lib.take_boundary.restype = ctypes.c_int
    lib.set_word.argtypes = [ctypes.c_char_p]
    lib.word_prefix.argtypes = [ctypes.c_uint64]
    lib.word_prefix.restype = ctypes.c_char_p
    lib.runs.restype = lib.width.restype = ctypes.c_uint64
    lib.run_data.restype = ctypes.POINTER(ctypes.c_uint64)
    return lib


def encode(n):
    return n.to_bytes((n.bit_length() + 7) // 8, "little")


def check_powers(lib):
    rules = verify()
    rng = random.Random(116372)
    for _ in range(1600):
        word = ''.join(rng.choices('01', k=rng.randrange(100))).rstrip('0')
        count = rng.getrandbits(rng.randrange(1, 90))
        lib.set_word(word.encode())
        data = encode(count)
        lib.exponentiate(data, len(data))
        while count:
            batch, new = add_calls(count, word)
            if batch:
                word = new
                count -= batch
            else:
                word = right_call(word, rules)
                count -= 1
        assert lib.word_prefix(lib.width()).decode() == word
    print("Matched 1,600 powers against the four-interface verifier.")


def snapshot(lib, epoch, visits, n):
    head = json.dumps([epoch, visits, hex(n), lib.leading()], separators=(',', ':')).encode()
    if sys.byteorder == "little":
        data = ctypes.string_at(lib.run_data(), 8 * lib.runs())
    else:
        data = b"".join(int(lib.run_data()[i]).to_bytes(8, "little") for i in range(lib.runs()))
    return head + b'\n' + data


def replay(limit, output):
    lib = open_engine()
    check_powers(lib)
    lib.set_word(b"000110011")
    n, epoch, visits = 36, 0, 0
    skipped = ctypes.c_uint64()
    while epoch < limit:
        data = encode(n // 2)
        tag = lib.take_boundary(data, len(data), ctypes.byref(skipped))
        visits += 1
        if tag == 3:
            raise RuntimeError(f"Halt at boundary {visits}, after {epoch} sweeps")
        if tag in (1, 2):
            n += 4 + skipped.value
            continue
        assert tag == 0
        n = 2 * n + 4
        epoch += 1
        if epoch in CHECKPOINTS or epoch == limit:
            raw = snapshot(lib, epoch, visits, n)
            digest = hashlib.sha256(raw).hexdigest()
            if epoch in CHECKPOINTS:
                assert digest == CHECKPOINTS[epoch], (epoch, digest)
            print(epoch, visits, n.bit_length(), lib.width(), lib.runs(), digest, flush=True)
    if output is not None:
        output.write_bytes(zlib.compress(snapshot(lib, epoch, visits, n), 4))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epochs', type=int, default=3338)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.epochs < 0:
        parser.error('epochs must be nonnegative')
    replay(args.epochs, args.output)
