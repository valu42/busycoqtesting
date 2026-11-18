"""Line 34 periodic insertion certificate. Run with assertions enabled."""
import argparse
import json
import subprocess
from pathlib import Path

from target34_orbit import analyze, encode, TapeMachine, TERNARY


def subword(config, start, stop):
    width, opens, closes = config
    assert 0 <= start <= stop <= width
    n = stop - start
    shift = width - stop
    # Work on the small extracted integers when checking just one period.
    mask = (1 << n) - 1
    opens = (opens >> shift) & mask
    closes = (closes >> shift) & mask
    return bytes(1 if opens & (1 << i) else 3 if closes & (1 << i) else 2
                 for i in reversed(range(n)))


def mask_word(size, mask):
    return bytes(1 if (mask >> i) & 1 else 2 for i in range(size))


def periodic_successor(word):
    """Stationary matching on a ring with strictly positive total balance."""
    balance = word.count(1) - word.count(3)
    assert balance > 0
    debt = 0
    for cell in reversed(word):
        debt = max(0, debt + (cell == 3) - (cell == 1))
    debt_at_cut = debt
    survivors = []
    debt_sum = 0
    for cell in reversed(word):
        survivors.append(cell == 1 and debt == 0)
        debt = max(0, debt + (cell == 3) - (cell == 1))
        debt_sum += debt
    assert debt == debt_at_cut
    assert sum(survivors) == balance
    bits = survivors[::-1]
    new = bytes(1 if bits[i-1] == bit else 3 if bit else 2
                for i, bit in enumerate(bits))
    cost_per_extra_copy = 2 * (len(word) + debt_sum + balance)
    return new, debt_at_cut, bits[-1], cost_per_extra_copy


def initial_configuration():
    source = (0, 0, 0)
    head = clock = 0
    for _ in range(52):
        (source, h, ticks), _, _, _ = analyze(source, ())
        head -= h
        clock += ticks
    word = subword(source, 0, source[0])
    literal = TapeMachine(TERNARY)
    for _ in range(clock):
        assert literal.step()
    assert literal.head == head and literal.state == 'A'
    assert literal.tape == {head+1+i: x for i, x in enumerate(word)}
    return word, head, clock


def common_prefix(first, second):
    w, a, b = first
    other_w, other_a, other_b = second
    assert other_w >= w
    diff = (a ^ (other_a >> (other_w-w))) | (b ^ (other_b >> (other_w-w)))
    return w - diff.bit_length()


def check_full_literal(engine, actual, cut, period, head, clock, coefficient):
    word = all_digits(actual)
    # Additional periods are inserted at this physical cut. Check the
    # unmodified repeated stretch strictly beyond every terminal-sweep read.
    j = cut
    while j < len(word) and word[j] == period[(j-cut) % len(period)]:
        j += 1
    terminal = None
    for extra in (0, 1):
        run = subprocess.run([str(engine), str(extra)], check=True, capture_output=True)
        header, digits, end = run.stdout.splitlines()
        expected_word = word[:cut] + period * extra + word[cut:]
        assert list(map(int, header.split())) == [clock + extra*coefficient, head, 0, head+1]
        assert digits.translate(bytes.maketrans(b'01234', bytes(range(5)))) == expected_word
        end_ticks, end_head, state, scanned, rightmost = map(int, end.split())
        assert (end_head, state, scanned, rightmost) == (-3043, 1, 4, 143739)
        assert rightmost < head + 1 + j
        if extra == 0:
            terminal = end_ticks
        assert end_ticks == terminal + extra*coefficient
        print(f'Whole literal replay k={extra}: exact full successful checkpoint '
              f'and B4 at {end_ticks}, head {end_head}, maximum terminal-sweep '
              f'coordinate {rightmost}.')
    assert terminal == 2258780781
    print('First unverified physical digit after the periodic cut:', head+1+j)


def periodic_family(word, period, copies, successful, head, literal=False, engine=None):
    left, right = word[:-15], word[-15:]
    source = encode(word)
    artificial_word = left + period * copies + right
    actual = encode(artificial_word)
    cut = len(left) + len(period) * (copies // 2)
    if literal:
        machine = TapeMachine(TERNARY, artificial_word, head=head, left=head+1)
    ticks_total = coefficient = 0
    shortest_common = len(word)
    minimum_balance = len(period)
    for epoch in range(successful + 1):
        assert subword(actual, cut, cut+len(period)) == period
        shortest_common = min(shortest_common, common_prefix(source, actual))
        src_step, src_guard, src_debts, _ = analyze(source, (9, 12))
        assert src_step is not None
        step, guard, debts, _ = analyze(actual, (9, 12, cut, cut+len(period)))
        balance = period.count(1) - period.count(3)
        if epoch == successful:
            assert step is None and balance < 0
            if literal:
                while machine.step():
                    assert machine.steps < ticks_total + 10**7
                assert machine.state == 'B' and machine.tape[machine.head] == 4
            print(f'{len(period)} cells, {copies} copies, {epoch} successful sweeps; '
                  f'final guard debts {guard} (altered), {src_guard} (blank); '
                  f'minimum earlier periodic balance {minimum_balance}; '
                  f'final periodic balance {balance}.')
            print(f'Common left digits >= {shortest_common}; surviving raw clock '
                  f'{ticks_total} + {coefficient} per extra copy.')
            print('Final period:', ''.join(map(str, period)))
            if literal:
                print(f'Literal B4 at step {machine.steps} from the altered checkpoint, '
                      f'head {machine.head}.')
            if engine is not None:
                check_full_literal(engine, actual, cut, period, head, ticks_total, coefficient)
            return
        assert step is not None and (src_guard, src_debts) == (guard, debts[:2])
        new_period, ring_debt, last_survivor, extra_cost = periodic_successor(period)
        minimum_balance = min(minimum_balance, balance)
        for pos, debt in zip((cut, cut+len(period)), debts[2:]):
            last_open = bool(actual[1] & (1 << (actual[0]-pos)))
            assert debt == ring_debt and (last_open and debt == 0) == last_survivor
        actual, h, ticks = step
        source = src_step[0]
        head -= h
        cut += h
        period = new_period
        ticks_total += ticks
        coefficient += extra_cost
        if literal:
            for _ in range(ticks):
                assert machine.step()
            assert (machine.head, machine.state) == (head, 'A')
            assert actual[0] == len(machine.tape)
            occupied = bytes(machine.tape[i] for i in range(head+1, head+1+actual[0]))
            assert encode(occupied) == actual


def all_digits(config):
    width, opens, closes = config
    if not width:
        return b''
    return bytes(1 if o == '1' else 3 if c == '1' else 2
                 for o, c in zip(format(opens, f'0{width}b'), format(closes, f'0{width}b')))


def screen_blank(source_word, period):
    # Evaluate each phase independently of its location or rotation on the tape.
    phases = {}
    n = len(period)
    for phase in range(2990):
        for r in range(n):
            rotated = period[r:] + period[:r]
            phases.setdefault(rotated, (phase, r))
        if phase < 2989:
            period = periodic_successor(period)[0]

    def matches(config, epoch):
        hits = 0
        best = (0, ())
        words = all_digits(config)
        for j in range(len(words)-n+1):
            candidate = words[j:j+n]
            if candidate in phases:
                hits += 1
                k = n
                while j+k < len(words) and words[j+k] == candidate[k % n]:
                    k += 1
                if k > best[0]:
                    best = (k, (epoch, j, *phases[candidate]))
        return hits, best

    config = encode(source_word)
    count = 0
    longest = (0, ())
    for epoch in range(52, 3042):
        hits, best = matches(config, epoch)
        count += hits
        if best[0] > longest[0]:
            longest = best
        if epoch < 3041:
            config = analyze(config, ())[0][0]
    assert (count, longest) == (71, (52, (977, 296, 2974, 28)))
    print('Blank epochs 52..3041:', count, 'single-period matches; longest',
          longest, '(length, (epoch, offset, phase, rotation)).')

    record = json.loads(Path(__file__).with_name('target34_checkpoint.json').read_text())
    assert record['machine'] == TERNARY and record['completed_sweeps'] == 125000
    sample = (record['width'], int(record['opens_hex'], 16), int(record['closes_hex'], 16))
    count, longest = matches(sample, 125000)
    assert (count, longest) == (3, (48, (125000, 134501, 2500, 38)))
    print('Epoch 125000:', count, 'single-period matches; longest', longest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--literal', type=Path, help='compiled back34_literal.cpp')
    args = parser.parse_args()
    engine = args.literal.resolve() if args.literal else None
    roster = Path(__file__).resolve().parents[1] / 'BB2x5_Rocq_holdouts_37.txt'
    assert roster.read_text().splitlines()[33] == TERNARY == '1RB2LA4RA1LA3LA_0LA2RB3RB2LB---'
    word, head, clock = initial_configuration()
    print(f'Blank seed epoch 52: head {head}, raw clock {clock}, width {len(word)}.')
    for copies in (50, 51):
        periodic_family(word, mask_word(11, 0xd), copies, 10, head, literal=True)
    period = mask_word(47, 0x3eee39d5e64e)
    periodic_family(word, period, 3600, 2989, head, engine=engine)
    screen_blank(word, period)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled.')
    main()
