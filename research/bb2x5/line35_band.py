"""Run line 35 in pairs of sweeps with a compressed, synchronized right suffix."""
import argparse
import base64
import hashlib
import json
import zlib
from dataclasses import dataclass
from itertools import product
from pathlib import Path

from frontiers.checkpoints import atomic_json, checksum
from prior_sweeps import TERNARY_CLOSE, TapeMachine, direct_epoch, word_sweep

O, C, N = 1, 2, 3
HEADERS = ('2', '1', '3', '1323', '1313', '1331')
EXTRA = (1, 1, 2, 8, 9, 11)


def masks(word):
    o = c = 0
    for digit in word:
        o = (o << 1) | (digit == O)
        c = (c << 1) | (digit == C)
    return len(word), o, c


HEADER_MASKS = tuple(masks(tuple(map(int, h))) for h in HEADERS)
TO_MASK = {symbol: bytes(49 if i == symbol else 48 for i in range(256)) for symbol in (O, C, N)}


def mask_of(word, symbol):
    return int(word.translate(TO_MASK[symbol]), 2) if word else 0


def digits(width, opens, closes):
    size = (width + 7) // 8
    a = opens.to_bytes(size, 'little')
    b = closes.to_bytes(size, 'little')
    return bytes(O if a[i // 8] >> (i % 8) & 1 else C if b[i // 8] >> (i % 8) & 1 else N
                 for i in reversed(range(width)))


def prefix_debt(width, opens, closes):
    debt = 0
    while closes:
        busy = (closes + ~opens) ^ closes ^ ~opens
        debt += (busy >> width) & 1
        closes &= busy
        opens &= ~busy
    return debt


@dataclass
class Band:
    """At odd epochs, bits of centers run from the right cap toward the guard."""
    width: int
    opens: int
    closes: int
    count: int = 0
    nonopen: int = 0
    neutral: int = 0

    @property
    def length(self):
        return self.width + 2 + 3 * self.count

    def absorb(self):
        # In right-to-left order the next three digits must be O,a,O.
        while self.width >= 3 and self.opens & 5 == 5:
            if not self.opens & 2:
                self.nonopen |= 1 << self.count
                if not self.closes & 2:
                    self.neutral |= 1 << self.count
            self.width -= 3
            self.opens >>= 3
            self.closes >>= 3
            self.count += 1

    @classmethod
    def from_word(cls, word):
        if tuple(word[-2:]) != (O, C):
            raise ValueError('the synchronized suffix needs the terminal opening and closing')
        word = bytes(word)
        right = len(word) - 3
        centers = bytearray()
        while right >= 2 and word[right] == O and word[right - 2] == O:
            centers.append(word[right - 1])
            right -= 3
        prefix = word[:right + 1]
        centers.reverse()
        k = len(centers)
        return cls(len(prefix), mask_of(prefix, O), mask_of(prefix, C), k,
                   ((1 << k) - 1) ^ mask_of(centers, O), mask_of(centers, N))

    def unpack(self):
        """Recover the complete physical word at an odd epoch."""
        nb = (self.count + 7) // 8
        h = self.nonopen.to_bytes(nb, 'little')
        z = self.neutral.to_bytes(nb, 'little')
        right = bytearray((C, O))
        for j in range(self.count):
            bit = 1 << (j % 8)
            center = N if z[j // 8] & bit else C if h[j // 8] & bit else O
            right.extend((O, center, O))
        return digits(self.width, self.opens, self.closes) + bytes(reversed(right))

    def test(self, incoming, divisor):
        """Return first-test debt and second-test slack at x=ceil(uncovered/divisor)."""
        x = (self.width + divisor - 1) // divisor
        if x < 20 or self.count == 0:
            return None
        left_o = self.opens >> (self.width - x)
        left_c = self.closes >> (self.width - x)
        debt = prefix_debt(x, left_o, left_c)
        balance = left_o.bit_count() - left_c.bit_count()
        slack = balance + 5 - incoming - (self.width - x + 25) // 8
        return debt, slack, x

    def paired_test(self, divisor):
        """Certify both sweeps from the same odd prefix and right suffix length."""
        m = self.width
        x = (m + divisor - 1) // divisor
        if x < 20 or self.count == 0:
            return None
        o, c = self.opens >> (m - x), self.closes >> (m - x)
        balance = o.bit_count() - c.bit_count()
        surviving = o
        guard = 0
        while c:
            busy = (c + ~surviving) ^ c ^ ~surviving
            surviving &= ~busy
            c &= busy
            guard += (busy >> x) & 1
        if guard >= 6:
            return guard, -1, -1, -1
        # If this margin is nonnegative the first guard/header is fixed.
        reserve = balance + guard - (m - x + 25) // 8
        h, ho, hc = HEADER_MASKS[guard]
        prev = (surviving >> 1) | (int(guard < 2) << (x - 1))
        mask = (1 << x) - 1
        qo = (ho << x) | (~(prev ^ surviving) & mask)
        qc = (hc << x) | (surviving & ~prev)
        next_m = m + h + 1
        y = (next_m + divisor - 1) // divisor
        # For the default divisor 5 this holds at every possible header length.
        if not (20 <= y <= h + x):
            return None
        qo >>= h + x - y
        qc >>= h + x - y
        second_debt = prefix_debt(y, qo, qc)
        second_balance = qo.bit_count() - qc.bit_count()
        # One possible lost opening balance and a maximum of one terminal debt.
        second_reserve = second_balance + 3 - (next_m - y + 25) // 8
        return guard, reserve, second_debt, second_reserve

    def half(self, right_bit, incoming, suffix_charge):
        """Update the uncovered material with the two signals at its fixed right index."""
        m = self.width
        o = self.opens << incoming
        c = (self.closes << incoming) | incoming
        # incoming is zero or one. Synthetic closing and its cut are outside the band.
        band_mask = (1 << m) - 1
        cuts = band_mask << (incoming + 1)
        guard = area = 0
        while c:
            busy = (c + ~o) ^ c ^ ~o
            area += (busy & cuts).bit_count()
            c &= busy
            o &= ~busy
            guard += (busy >> (m + incoming)) & 1
        if guard >= 6:
            return None, guard
        survivors = o >> incoming
        h, ho, hc = HEADER_MASKS[guard]
        leftmost = bool(survivors >> (m - 1)) if m else right_bit
        virtual = guard < 2
        first_o = virtual == leftmost
        first_c = leftmost and not virtual
        right = (survivors << 1) | right_bit
        new_o = ~(survivors ^ right) & band_mask
        new_c = (~survivors & right) & band_mask
        right_moves = 2 * self.length + 1 + area - survivors.bit_count() + suffix_charge + EXTRA[guard]
        self.width += h + 1
        self.opens = new_o | (int(first_o) << m) | (ho << (m + 1))
        self.closes = new_c | (int(first_c) << m) | (hc << (m + 1))
        return 2 * right_moves + h, guard

    def signals(self):
        """Return (outgoing survivor, debt, sum of cut debts minus survivors) by phase."""
        if not self.count:
            return (0, 0, 1), (0, 0, 1)
        h = self.nonopen
        z = self.neutral
        last_h = h >> (self.count - 1)
        last_n = z >> (self.count - 1)
        o = self.count - h.bit_count()
        n = z.bit_count()
        odd = (int(not last_h or last_n), 0, 1 - 3 * o - 2 * n)
        even = (1 - last_h, last_n, 2 + self.count - 4 * o + n - last_h)
        return odd, even

    def advance_centers(self):
        h = self.nonopen
        self.nonopen = h ^ (((h << 1) | 1) & ((1 << self.count) - 1))
        self.neutral = self.nonopen & ~h
        self.absorb()


def epoch_five():
    machine = TapeMachine(TERNARY_CLOSE)
    for _ in range(5):
        word = direct_epoch(machine, (O, C, N))
    assert (machine.steps, machine.head) == (97, -5)
    return Band.from_word(word), machine.steps, machine.head


def pascal_at(bits, pairs, count):
    """Jump a Pascal register with constant bit 0 set (the right-hand boundary)."""
    pairs %= 1 << count.bit_length()
    mask = (1 << (count + 1)) - 1
    while pairs:
        power = pairs & -pairs
        bits = (bits ^ (bits << power)) & mask
        pairs -= power
    return bits


def audit():
    # Compare two complete half-steps including their exact raw clocks to literal execution.
    checked = 0
    for w in range(7):
        for prefix in product((O, C, N), repeat=w):
            word = list(prefix + (O, C))
            model = Band.from_word(word)
            machine = TapeMachine(TERNARY_CLOSE, word, left=1)
            for signal in model.signals():
                start = machine.steps
                cost, guard = model.half(*signal)
                expected, low = word_sweep(word, TERNARY_CLOSE)
                assert guard == -low and (cost is None) == (expected is None)
                assert direct_epoch(machine, (O, C, N)) == expected
                if cost is None:
                    break
                assert cost == machine.steps - start
                word = expected
                checked += 1
            else:
                model.advance_centers()
                assert model.unpack() == bytes(word)
    print('literal half-sweep comparisons:', checked)


def load_checkpoint(path):
    doc = json.loads(Path(path).read_text())
    record = doc['payload']
    if doc['sha256'] != checksum(record) or record['format'] != 'bb2x5-line35-epoch-v1':
        raise ValueError('invalid line 35 checkpoint checksum or format')
    tape = zlib.decompress(base64.b64decode(record['tape_zlib_base64'], validate=True))
    if (record['machine'] != TERNARY_CLOSE or record['state'] != 'A'
            or record['left'] != record['head'] + 1 or record['epoch'] < 5
            or record['epoch'] % 2 != 1 or record['steps'] < 97
            or len(tape) != record['cells'] or not set(tape) <= {O, C, N}):
        raise ValueError('invalid line 35 tape or odd epoch')
    return record, Band.from_word(tape)


def summarize(path, epoch, elapsed, head, tape):
    record = {'format': 'bb2x5-line35-epoch-v1', 'machine': TERNARY_CLOSE, 'epoch': epoch,
              'steps': elapsed, 'head': head, 'state': 'A', 'left': head + 1, 'cells': len(tape),
              'tape_zlib_base64': base64.b64encode(zlib.compress(tape, 9)).decode()}
    if path:
        atomic_json(path, {'payload': record, 'sha256': checksum(record)})
    return hashlib.sha256(tape).hexdigest()


def replay(end, divisor, output):
    band, elapsed, head = epoch_five()
    miss = last_bad = max_debt = 0
    min_slack = None
    pair_miss = None
    pair_minima = None
    epoch = 5
    while True:
        pair = band.paired_test(divisor)
        if pair is None or pair[0] > 5 or pair[1] < 0 or pair[2] > 5 or pair[2] < 0 or pair[3] < 0:
            pair_miss, pair_minima = epoch, None
        else:
            margins = (5 - pair[0], pair[1], 5 - pair[2], pair[3])
            if pair_minima is None:
                pair_minima = [(v, epoch) for v in margins]
            else:
                pair_minima = [min(old, (v, epoch)) for old, v in zip(pair_minima, margins)]
        if epoch == end:
            break
        for signal in band.signals():
            test = band.test(signal[1], divisor)
            if test is None or test[0] > 5 or test[1] < 0:
                miss = epoch
                min_slack = None
                max_debt = 0
            else:
                debt, slack, _ = test
                if min_slack is None or slack < min_slack:
                    min_slack, last_bad = slack, epoch
                max_debt = max(max_debt, debt)
            cost, guard = band.half(*signal)
            if cost is None:
                raise RuntimeError(f'Physical B4 at epoch {epoch} with guard debt {guard}')
            elapsed += cost
            head -= len(HEADERS[guard])
            epoch += 1
        band.advance_centers()
    debt, slack, x = band.test(0, divisor) or (None, None, None)
    if debt is not None:
        if debt > 5 or slack < 0:
            miss, min_slack, max_debt = epoch, None, 0
        else:
            if min_slack is None or slack < min_slack:
                min_slack, last_bad = slack, epoch
            max_debt = max(max_debt, debt)
    print('epoch', epoch, 'width', band.length, 'covered triples', band.count,
          'uncovered', band.width, 'cut', x, 'prefix debt', debt, 'slack', slack)
    print('last miss', miss, 'least subsequent slack', min_slack, 'at', last_bad,
          'maximum subsequent prefix debt', max_debt)
    print('paired test last miss', pair_miss, 'subsequent minimum margins and epochs', pair_minima,
          'final observations', pair)
    print('head', head, 'steps', elapsed, 'tape SHA-256', summarize(output, epoch, elapsed, head, band.unpack()))
    return band


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--epochs', type=int)
    parser.add_argument('--divisor', type=int, default=5)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if not __debug__:
        parser.error('run with assertions enabled')
    if args.epochs is not None and (args.epochs < 5 or args.epochs % 2 == 0):
        parser.error('choose an odd final epoch of at least five')
    if args.divisor < 1:
        parser.error('the divisor must be positive')
    audit()
    if args.epochs is not None:
        replay(args.epochs, args.divisor, args.output)
