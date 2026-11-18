"""Exact chronological-column recurrence for BB(2,5) formal line 37."""

from dataclasses import dataclass
from itertools import cycle, islice
from pathlib import Path

from prior_sweeps import TERNARY_OPEN, word_sweep


# An integer letter encodes the (outgoing matching debt, survivor) pair.
# 0 and 1 both have zero debt and survivor bits 0 and 1 respectively.
# For letter n >= 2 the debt is n-1 and the survivor bit is zero.
def run_cell(symbol, letter):
    right_survives = letter == 1
    incoming = max(0, letter - 1)
    survives = symbol == 2 and not incoming
    outgoing = max(0, incoming + (symbol == 1) - (symbol == 2))
    answer = outgoing + 1 if outgoing else int(survives)
    if survives == right_survives:
        return 2, answer
    return (1 if right_survives else 3), answer


@dataclass(frozen=True)
class Stream:
    prefix: tuple
    period: tuple

    def first(self):
        return (self.prefix or self.period)[0]

    def drop_first(self):
        if self.prefix:
            return Stream(self.prefix[1:], self.period)
        return Stream((), self.period[1:] + self.period[:1])

    def take(self, length):
        tail = max(0, length - len(self.prefix))
        return self.prefix[:length] + tuple(islice(cycle(self.period), tail))


def cell_image(stream, symbol):
    prefix = []
    for letter in stream.prefix:
        symbol, answer = run_cell(symbol, letter)
        prefix.append(answer)
    seen = {}
    answers = []
    phase = 0
    while (phase, symbol) not in seen:
        seen[phase, symbol] = len(answers)
        symbol, answer = run_cell(symbol, stream.period[phase])
        answers.append(answer)
        phase = (phase + 1) % len(stream.period)
    split = seen[phase, symbol]
    prefix.extend(answers[:split])
    period = answers[split:]
    # Minimize the period, then move its start left across matching letters.
    for p in range(1, len(period)):
        if len(period) % p == 0 and all(x == period[i % p] for i, x in enumerate(period)):
            period = period[:p]
            break
    start = 0
    while prefix and prefix[-1] == period[(start - 1) % len(period)]:
        prefix.pop()
        start = (start - 1) % len(period)
    return Stream(tuple(prefix), tuple(period[start:] + period[:start]))


def next_epoch(stream):
    """Return (new leftmost stream, width increase), or (None, 0) if B4 follows."""
    first = stream.first()
    debt = max(0, first - 1)
    if debt >= 2:
        return None, 0
    initial = 1 if first == 1 else 2
    stream = cell_image(stream.drop_first(), initial)
    header = (2, 2, 1, 2) if debt else (2,)
    for symbol in header:
        stream = cell_image(stream, symbol)
    return stream, 1 + len(header)


def main():
    assert Path(__file__).with_name('BB2x5_Rocq_holdouts_37.txt').read_text().splitlines()[36] == TERNARY_OPEN
    stream = Stream((), (1,))
    word = [2]
    width = 1
    samples = []
    for epoch in range(1, 513):
        # The stream describes the same right-index even at later epochs.
        # Independently collect the first eight letters of each such stream.
        samples.append([width - 1, stream.take(8), 0])
        base = 0
        expected = {}
        for j, symbol in enumerate(reversed(word)):
            survives = symbol == 2 and base == 0
            base = max(0, base + (symbol == 1) - (symbol == 2))
            expected[j] = base + 1 if base else int(survives)
        for sample in samples:
            j, predicted, index = sample
            assert predicted[index] == expected[j]
            sample[2] += 1
        samples = [s for s in samples if s[2] != 8]
        assert (stream.first() >= 3) == (base >= 2)
        stream, growth = next_epoch(stream)
        word, _ = word_sweep(word, TERNARY_OPEN)
        assert stream is not None and word is not None
        width += growth
        assert width == len(word)
    print('Checked 512 blank epoch updates and overlapping eight-epoch column traces.')
    print(f'Epoch 513: width {width}, chronological prefix {len(stream.prefix)}, period {len(stream.period)}.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run with assertions enabled')
    main()
