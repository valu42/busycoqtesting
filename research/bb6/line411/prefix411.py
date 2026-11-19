"""Certify line 411 boundaries while treating everything beyond a finite prefix as unknown."""
import argparse
from functools import lru_cache
import hashlib
import json
import struct
import zlib
from pathlib import Path
from sweeps import CHECKPOINTS


def put(runs, bit, length):
    if length:
        if runs and runs[-1][0] == bit:
            runs[-1] = (bit, runs[-1][1] + length)
        else:
            runs.append((bit, length))


def join(left, right):
    if not left or not right:
        return left + right
    if left[-1][0] == right[0][0]:
        return left[:-1] + [(right[0][0], left[-1][1] + right[0][1])] + right[1:]
    return left + right


def drop(runs, count):
    i = 0
    while count and count >= runs[i][1]:
        count -= runs[i][1]
        i += 1
    if count:
        bit, n = runs[i]
        return [(bit, n - count)] + runs[i + 1:]
    return runs[i:]


def peek(runs, size):
    out = ''
    for bit, n in runs:
        out += str(bit) * min(n, size - len(out))
        if len(out) == size:
            break
    return out


@lru_cache(40000)
def one_call(packet):
    """If returned, F(packet x) = output F^carry(x) for every x."""
    pos, out = 0, ''
    while pos < len(packet):
        start = pos
        while packet.startswith('1001', pos):
            pos += 4
        skipped = pos - start
        if packet.startswith('0', pos):
            return out + '1' * (skipped + 1) + packet[pos + 1:], 0
        if packet.startswith('11', pos):
            out += '0' * skipped + '11'
            pos += 2
            continue
        if packet.startswith('101', pos):
            return out + '0' * skipped + '111' + packet[pos + 3:], 0
        if packet.startswith('1000', pos) and pos + 4 < len(packet):
            return out + '0' * skipped + '00011' + packet[pos + 5:], 0
        return None
    return out, 1


@lru_cache(20000)
def packet_orbit(packet):
    words, total, seen = [], [0], {}
    while packet not in seen and len(words) < 2048:
        seen[packet] = len(words)
        words.append(packet)
        result = one_call(packet)
        if result is None:
            return words, total, None
        packet, forwarded = result
        total.append(total[-1] + forwarded)
    return words, total, seen.get(packet)


def pass_packet(packet, least, bits):
    """The incoming count is least + t*2^bits, t >= 0. None for bits means exact."""
    words, total, start = packet_orbit(packet)
    if bits is None and least < len(words):
        return words[least], total[least], None
    if start is None or least < start:
        return None
    period = len(words) - start
    if bits is not None and (1 << bits) % period:
        return None
    repeats, phase = divmod(least - start, period)
    per_cycle = total[-1] - total[start]
    sent = total[start + phase] + repeats * per_cycle
    next_bits = None
    if bits is not None and per_cycle:
        increment = ((1 << bits) // period) * per_cycle
        next_bits = (increment & -increment).bit_length() - 1
    return words[start + phase], sent, next_bits


def apply_power(runs, least, bits=None):
    """Every possible resulting tape begins with the returned finite prefix."""
    i, used, out = 0, 0, []
    while i < len(runs):
        bit, length = runs[i]
        if bits is None and least == 0:
            put(out, bit, length - used)
            return join(out, runs[i + 1:])
        if bit and length - used >= 2:
            take = (length - used) // 2 * 2
            put(out, 1, take)
            used += take
            if used == length:
                i, used = i + 1, 0
            continue
        packet, j, scanned = '', i, used
        # Unresolved cuts only shorten the certificate. Each accepted cut
        # carries its own universal one-call identities and finite cycle.
        result = None
        for size in range(2, 68, 2):
            while len(packet) < size and j < len(runs):
                bit, length = runs[j]
                take = min(size - len(packet), length - scanned)
                packet += str(bit) * take
                scanned += take
                if scanned == length:
                    j, scanned = j + 1, 0
            if len(packet) < size:
                break
            result = pass_packet(packet, least, bits)
            if result is not None:
                break
        if result is None:
            return out
        word, least, bits = result
        for char in word:
            put(out, int(char), 1)
        i, used = j, scanned
    return out


DIGITS = {
    'r': {'11': 'r', '00': 'd', '10': 'd'},
    'd': {'0000': 'd', '0110': 'd', '0011': 'r', '0111': 'r'},
}


@lru_cache(None)
def read_digit(state, bit):
    mode, token = state[0], state[1:] + bit
    if token in DIGITS[mode]:
        return DIGITS[mode][token], int(token != '11')
    if any(word.startswith(token) for word in DIGITS[mode]):
        return mode + token, 0
    return None, 0


def period_bits(runs):
    """Both an unshifted and a one-cell-shifted call preserve this prefix
    when the raw call count is a multiple of the indicated power of two."""
    worst = 0
    for state in ('r', 'r1'):
        capacity = 0
        for bit, count in runs:
            while count:
                if bit and state in ('r', 'r1'):
                    if count % 2:
                        state = 'r1' if state == 'r' else 'r'
                    break
                if not bit and state in ('d', 'd0', 'd00', 'd000'):
                    groups, count = divmod(count, 4)
                    capacity += groups
                    if not count:
                        break
                state, cost = read_digit(state, str(bit))
                if state is None:
                    return None
                capacity += cost
                count -= 1
        if state not in ('r', 'r1'):
            return None
        worst = max(worst, capacity + (state == 'r1'))
    return worst


def stable_part(runs, bits):
    """A simple common period for a sequence of ones and 0^(4h+3)111 blocks."""
    out, cost, i = [], 0, 0
    while i < len(runs):
        bit, n = runs[i]
        if bit:
            put(out, 1, n)
            i += 1
            continue
        if n % 4 != 3 or i + 1 >= len(runs) or runs[i + 1][1] < 3:
            break
        cost += n // 4 + 2
        if cost > bits:
            break
        out.extend(runs[i:i + 2])
        i += 2
    return out


def large_power(runs, residue, bits, shifted=False):
    # At entry the actual count is at least 2^(bits+1), by the checkpoint bound.
    if shifted:
        runs = join([(1, 1)], runs)
    modulus = 1 << bits
    out = apply_power(runs, modulus + residue % modulus, bits)
    if shifted and out:
        assert out[0][0] == 1
        return drop(out, 1)
    return out


def consume_ones(runs, count, s, bits):
    """Suffix after count consecutive regular sweeps. The true s is even."""
    assert s % 2 == 0 and count > 0
    modulus = 1 << bits
    for j in range(min(count, bits + 2)):
        exponent = (s << j) % modulus
        valuation = (exponent & -exponent).bit_length() - 1 if exponent else bits
        if stable_part(runs, valuation - 1) == runs:
            return runs
        if j % 8 == 0:
            needed = period_bits(runs)
            if needed is not None and needed <= valuation:
                return runs
        runs = large_power(runs, exponent, bits, shifted=(count - 1 - j) % 2 == 1)
    if count > bits + 2:
        return stable_part(runs, bits - 1)
    return runs


def one_boundary(n, runs, bits):
    skipped = 0
    while peek(runs, 4) == '1001':
        skipped += 4
        runs = drop(runs, 4)
    word = peek(runs, 4)
    modulus = 2 << bits
    if word.startswith('0'):
        ones = [(1, skipped)] if skipped else []
        out = large_power(join(ones, drop(runs, 1)), n // 2, bits)
        return 'sweep', (2 * n + 4) % modulus, out
    if word.startswith('11'):
        return 'return', (n + skipped + 4) % modulus, apply_power(drop(runs, 2), 1)
    if word.startswith('101'):
        return 'return', (n + skipped + 4) % modulus, drop(runs, 2)
    return ('halt' if word == '1000' else 'unknown'), n, runs


def certify(path, limit, pairs, bits):
    raw = zlib.decompress(path.read_bytes())
    meta, data = raw.split(b'\n', 1)
    epoch, visits, n, first = json.loads(meta)
    assert CHECKPOINTS[epoch] == hashlib.sha256(raw).hexdigest()
    n = int(n, 16)
    assert n.bit_length() > bits + 10
    assert bits >= 4 and pairs > 0 and limit >= epoch
    modulus = 2 << bits
    n %= modulus
    runs = [(first ^ (i % 2), length) for i, (length,) in
            enumerate(struct.iter_unpack('<Q', data[:16 * pairs]))]
    while epoch < limit:
        s = (n + 4) // 8
        if n % 8 == 4 and peek(runs, 7) == '0000111' and s % 2 == 0:
            count = min(runs[1][1] - 2, limit - epoch)
            after = consume_ones(drop(runs, 6 + count), count, s, bits - 2)
            runs = join([(0, 4), (1, 2)], after)
            n = (((n + 4) << min(count, bits + 1)) - 4) % modulus
            epoch += count
            visits += count
            continue
        tag, n, runs = one_boundary(n, runs, bits)
        if tag == 'unknown':
            raise RuntimeError(f"Prefix exhausted after {epoch} sweeps and {visits} checks")
        visits += 1
        if tag == 'halt':
            raise RuntimeError(f"Halting pattern at check {visits}, after {epoch} sweeps")
        epoch += tag == 'sweep'
    return epoch, visits, runs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkpoint', type=Path)
    parser.add_argument('--through', type=int, default=180000000)
    parser.add_argument('--pairs', type=int, default=2400)
    parser.add_argument('--bits', type=int, default=5120)
    args = parser.parse_args()
    epoch, visits, prefix = certify(args.checkpoint, args.through, args.pairs, args.bits)
    print(f"{epoch:,} completed sweeps, {visits:,} boundary checks.")
    print("First certified (bit, run length) pairs:", prefix[:8])
