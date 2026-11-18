"""Audit the B suffix calls made by line 7's fresh and internal A0 guards."""
import argparse
from collections import Counter
from hashlib import sha256
from pathlib import Path

from checkpoints import atomic_json, checksum
from line7 import Calls, MACHINE, RULES, TWOS, load, save, snapshot


def trace_prefix(word, state, limit=512):
    """Run on just the given word. A right exit leaves the exterior unresolved."""
    cells = bytearray(word)
    x = used = 0
    for cost in range(limit+1):
        if x < 0:
            return state, cost, used, bytes(cells[:used])
        if x == len(cells) or cost == limit:
            return 'open', cost, used, bytes(cells[:used])
        used = max(used, x+1)
        rule = RULES.get((state, cells[x]))
        if rule is None:
            return 'halt', cost, used, bytes(cells[:used])
        cells[x], move, state = rule
        x += move


def projected(cells, start):
    """Propagate the requests of B on 3 up to the first nonordinary digit."""
    q, n, pos = 'A', 2, start
    while n and pos < len(cells):
        digit = cells[pos]
        if digit not in (2, 4):
            break
        if q == 'B':
            n = (n + (digit == 4)) // 2
            q = 'A'
        elif digit == 2:
            end = TWOS.match(cells, pos).end()
            n *= 3**(end-pos)
            pos = end
            continue
        else:
            q = 'B'
        pos += 1
    return pos, q, n


def classify(cells, start):
    digit = cells[start] if start < len(cells) else 0
    if digit in (0, 2):
        return 'child_'+str(digit), {}
    if digit == 3:
        if start+2 == len(cells) and cells[start+1] == 2:
            return 'terminal_32', {}
        stop, state, count = projected(cells, start+1)
        if not count:
            return 'ordinary_prefix', {}
        if stop == len(cells):
            if state == 'B' and count <= 2:
                return 'virgin_returns_B', {}
            return 'first_A_on_virgin' if state == 'A' else 'third_B_on_virgin', {
                'distance_to_virgin': stop-start, 'projected_count_bits': count.bit_length()}
    prefix = cells[start:start+64]
    reply, cost, used, _ = trace_prefix(prefix, 'B')
    sample = {'prefix': ''.join(map(str, prefix[:used])), 'local_steps': cost}
    if reply == 'B':
        return 'closed_literal_prefix', sample
    if reply in ('A', 'halt'):
        return 'literal_'+reply, sample
    return 'open_prefix', sample


class Audit:
    def __init__(self, first):
        self.epoch = first
        self.counts = {'outer': Counter(), 'internal': Counter()}
        self.examples = {}
        self.rounds = {'outer': Counter(), 'internal': Counter()}
        self.first_round = {}
        self.internal_prefixes = {}

    def observe(self, group, cells, start):
        kind, detail = classify(cells, start)
        self.counts[group][kind] += 1
        key = group+'_'+kind
        if detail and key not in self.examples:
            # At the start of epoch e, zero-indexed suffix cell 0 is at 2-e.
            self.examples[key] = dict(epoch=self.epoch, guard_coordinate=1-self.epoch+start, **detail)
        if group == 'internal' and kind == 'closed_literal_prefix':
            self.internal_prefixes.setdefault(detail['prefix'], dict(epoch=self.epoch,
                                              guard_coordinate=1-self.epoch+start, **detail))

    def round(self, child, replies):
        group = 'outer' if child == 0 else 'internal'
        self.rounds[group][replies] += 1
        key = group+'_'+replies
        self.first_round.setdefault(key, {'epoch': self.epoch,
                                          'guard_coordinate': 1-self.epoch+child})

    def internal(self, cells, start):
        self.observe('internal', cells, start)


def rank_bits(cells, start):
    """Read the low bits forced on any normal first A return. Pairs are low bit first."""
    width = value = 0
    while start+1 < len(cells) and cells[start] == 4 and cells[start+1] in (2, 4):
        if cells[start+1] == 2:
            value |= 1 << width
        start += 2
        width += 1
    return width, value


def rank_return(k, j, limit=100_000, tail=None, max_calls=0):
    """Replay the suspended guard, optionally following a bounded number of actual V calls."""
    if k < 1 or j < 0:
        raise ValueError('invalid leading width or rank')
    block_index, offset = divmod(j, 3**k)
    if block_index > 1:
        raise ValueError('rank lies beyond both A calls on the leading twos')
    phases = bytearray(k)
    i = k
    while offset:
        i -= 1
        offset, phases[i] = divmod(offset, 3)
    propagates = phases[0] == phases[-1] == 0 and 1 not in phases and b'\x02\x02' not in phases
    cells = bytearray([1, 0 if block_index else 4])
    cells.extend((3, 4, 0)[phase] for phase in phases)
    x, state = len(cells)-1, 'A'
    budget = max(limit, 4*k+16)
    calls = []
    cost = 0
    while True:
        if x < 0:
            kind = 'safe'
            break
        if x == len(cells):
            if tail is None or len(calls) == max_calls:
                kind = 'needs_tail'
                break
            before = tail.steps
            _, reply = tail.run(tail.many(0, state, 1))
            calls.append({'entry': state, 'reply': reply, 'prefix_steps_before': cost,
                          'inside_steps_hex': hex(tail.steps-before)})
            if reply == 'halt':
                kind, x, state = 'halt_in_tail', x+tail.halt_cell, 'A'
                break
            x, state = x-1, reply
            continue
        rule = RULES.get((state, cells[x]))
        if rule is None:
            kind = 'halt'
            break
        if cost == budget:
            kind = 'budget'
            break
        cells[x], move, state = rule
        x += move
        cost += 1
    if propagates and kind != ('halt' if block_index else 'safe'):
        raise ValueError('literal suspended path violates the ternary propagation rule')
    result = {'outcome': kind, 'steps_after_reply': cost, 'head_from_guard': x, 'state': state,
              'ternary_propagation': propagates}
    if tail is not None:
        result['tail_calls'] = calls
    return result


class RootRanks:
    """Probe the first exceptional A input to the tail after the leading twos."""
    def __init__(self):
        self.histogram = Counter()
        self.digest = sha256()
        self.closest = None
        self.distance = None
        self.residues = Counter()
        self.family_parity = Counter()
        self.residue_examples = {}
        self.events = []

    def probe(self, cells, epoch, work):
        if cells[:2] != b'\x03\x02':
            self.histogram['different_header'] += 1
            return None
        end = TWOS.match(cells, 1).end()
        k = end-1
        block = 3**k
        width, low = rank_bits(cells, end)
        mask = (1 << width)-1
        residue = block & mask
        match = 'no_pairs' if not width else ('compatible' if residue == low else 'excluded')
        self.residues[match] += 1
        parity = 'no_pairs' if not width else ('odd' if low & 1 else 'excluded_even')
        self.family_parity[parity] += 1
        if match not in self.residue_examples:
            self.residue_examples[match] = {'epoch': epoch, 'leading_twos': k, 'pairs': width,
                                            'low_bits_hex': hex(low), 'target_residue_hex': hex(residue)}
        trial = Calls(cells[end:], limit=work)
        j, reply = trial.run(trial.many(0, 'A', 2*block))
        self.digest.update(f'{epoch} {k} {j:x} {reply}\n'.encode())
        if reply == 'halt':
            kind, prediction = 'halt_inside_tail', 'halt'
        elif reply == 'B':
            if j != 2*block:
                raise ValueError('incomplete rank probe')
            kind, prediction = 'two_complete_blocks', 'safe'
        elif j == 0:
            kind, prediction = 'first_call', 'safe'
        elif j == block:
            kind, prediction = 'first_call_second_block', 'halt'
        elif j < block:
            kind, prediction = 'inside_first_block', None
        else:
            kind, prediction = 'inside_second_block', None
        self.histogram[kind] += 1
        if reply == 'A':
            if (j & mask) != low:
                raise ValueError('normal A return violates the visible register bits')
            local = rank_return(k, j)
            self.events.append({'epoch': epoch, 'leading_twos': k, 'prior_B_replies_hex': hex(j),
                                'tail_digit_after_A': trial.tape[0], 'after_first_A': local})
            if local['outcome'] in ('safe', 'halt'):
                prediction = local['outcome']
            distance = abs(j-block)
            if self.distance is None or distance*self.distance[1] < self.distance[0]*block:
                self.distance = distance, block
                self.closest = {'epoch': epoch, 'leading_twos': k, 'prior_B_replies_hex': hex(j)}
        return prediction

    def report(self):
        return {'counts': self.histogram, 'rank_transcript_sha256': self.digest.hexdigest(),
                'closest_relative_to_block': self.closest, 'rank_residues': self.residues,
                'first_residue_examples': self.residue_examples, 'exceptional_returns': self.events,
                'family_parity': self.family_parity}


def audit(p, target, work, ranks=False):
    if p['status'] != 'unknown' or target <= p['epochs']:
        raise ValueError('expected a later absolute epoch on an open run')
    probes = RootRanks() if ranks else None
    first = p['epochs']+1
    log = Audit(first)
    vm = Calls(map(int, p['word']), int(p['steps_hex'], 16), work, on_guard=log.internal, on_round=log.round)
    for epoch in range(first, target+1):
        log.epoch = epoch
        log.observe('outer', vm.tape, 0)
        prediction = probes.probe(vm.tape, epoch, work) if probes else None
        completed = vm.epoch()
        if prediction and completed != (prediction == 'safe'):
            raise ValueError('rank prediction disagrees with the full physical guard')
        if not completed:
            end = snapshot(epoch-1, vm, halted=True)
            break
    else:
        end = snapshot(target, vm)
    ledger = {'machine': MACHINE, 'start_epochs': first-1, 'end_epochs': end['epochs'],
              'start_sha256': checksum(p), 'end_sha256': checksum(end),
              'status': end['status'], 'counts': log.counts, 'first_examples': log.examples,
              'guard3_reply_rounds': log.rounds, 'first_round': log.first_round,
              'internal_literal_prefixes': list(log.internal_prefixes.values())}
    if probes:
        ledger['root_ranks'] = probes.report()
    return end, ledger


def audit_blocks(p, target, work, batch):
    """Search for the first non-B tail reply in each stretch of growing outer headers."""
    if p['status'] != 'unknown' or target <= p['epochs'] or batch < 1:
        raise ValueError('expected a later target and a positive batch size')
    vm = Calls(map(int, p['word']), int(p['steps_hex'], 16), work)
    epoch = p['epochs']
    stretches, exceptions = [], []

    def record(k, count, reply, j):
        if reply == 'B':
            if stretches and stretches[-1][1] == epoch:
                stretches[-1][1] += count
            else:
                stretches.append([epoch+1, epoch+count])
        else:
            event = {'epoch': epoch+1, 'leading_twos': k, 'reply': reply}
            if j is not None:
                event['prior_B_replies_hex'] = hex(j)
            if reply == 'A':
                event['after_first_A'] = rank_return(k, j)
            exceptions.append(event)

    while epoch < target:
        count, halted = vm.epoch_block(min(batch, target-epoch), record)
        epoch += count
        if halted:
            break
    end = snapshot(epoch, vm, halted)
    return end, {'machine': MACHINE, 'start_epochs': p['epochs'], 'end_epochs': epoch,
                 'start_sha256': checksum(p), 'end_sha256': checksum(end), 'status': end['status'],
                 'all_B_epoch_ranges_inclusive': stretches, 'exceptional_or_literal_epochs': exceptions}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resume', type=Path)
    parser.add_argument('--epochs', type=int, required=True)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--ranks', action='store_true', help='also test the exact power-of-three halt condition')
    mode.add_argument('--batch', type=int, help='search for exceptional outer ranks in batches of this many epochs')
    parser.add_argument('--work', type=int, default=10**9)
    parser.add_argument('--checkpoint', type=Path, required=True)
    parser.add_argument('--audit', type=Path, required=True)
    args = parser.parse_args()
    p = load(args.resume) if args.resume else snapshot(0, Calls())
    if args.batch is None:
        end, log = audit(p, args.epochs, args.work, args.ranks)
    else:
        end, log = audit_blocks(p, args.epochs, args.work, args.batch)
    save(args.checkpoint, end)
    atomic_json(args.audit, log)
    print(f"{end['epochs']} completed epochs, {end['status']}")
