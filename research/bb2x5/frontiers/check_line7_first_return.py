"""Recover the first exceptional clock and the next physical suffix calls from a batch ledger."""
import argparse
import json
from pathlib import Path

from checkpoints import atomic_json, checksum
from line7 import Calls, MACHINE, TWOS, load
from line7_guards import rank_return


def follow(seed, ledger, calls=6, work=10**9):
    if (seed['status'] != 'unknown' or ledger['machine'] != MACHINE
            or checksum(seed) != ledger['start_sha256'] or seed['epochs'] != ledger['start_epochs']):
        raise ValueError('ledger and checkpoint have different origins')
    event = ledger['exceptional_or_literal_epochs'][0]
    if event['reply'] != 'A':
        raise ValueError('the first exceptional event must be a normal A return')
    word = bytes(map(int, seed['word']))
    if word[:2] != b'\x03\x02':
        raise ValueError('expected a header starting in 3 then 2')
    k0 = TWOS.match(word, 1).end()-1
    r = event['epoch']-seed['epochs']-1
    k = event['leading_twos']
    if r < 0 or k != k0+r or calls < 0:
        raise ValueError('the event lies outside the initial geometric stretch')
    prior = 3**k-3**k0
    j = int(event['prior_B_replies_hex'], 16)
    vm = Calls(word[1+k0:], limit=work)
    if vm.run(vm.many(0, 'A', prior+j+1)) != (prior+j, 'A'):
        raise ValueError('single fixed-cut replay did not reproduce the first A')
    digit_sum, n = 0, j
    while n:
        n, digit = divmod(n, 3)
        digit_sum += digit
    raw = int(seed['steps_hex'], 16) + vm.steps + 2*prior+r + 2*j-digit_sum+k+2
    return {'machine': MACHINE, 'start_sha256': checksum(seed), 'epoch': event['epoch'],
            'leading_twos': k, 'prior_B_replies_hex': hex(j), 'first_A_raw_steps_hex': hex(raw),
            'first_A_head': 1-event['epoch']+k+1, 'first_A_state': 'A', 'tail_digit_after_A': vm.tape[0],
            'after_first_A': rank_return(k, j, tail=vm, max_calls=calls)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--resume', required=True, type=Path)
    parser.add_argument('--audit', required=True, type=Path)
    parser.add_argument('--calls', default=6, type=int)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = follow(load(args.resume), json.loads(args.audit.read_text()), args.calls)
    atomic_json(args.output, result)
    print(f"Replayed the first exceptional A at epoch {result['epoch']}.")
