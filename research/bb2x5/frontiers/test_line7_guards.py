"""Compare the guard, rank and geometric epoch rules to literal machine instructions."""
import itertools
import unittest

from check_line7_first_return import follow
from line7 import Calls, MACHINE, snapshot
from line7_guards import audit_blocks, rank_bits, rank_return, trace_prefix
from prior_sweeps import TapeMachine


def register(n, width):
    pairs = ([4, 2 if (n >> i) & 1 else 4] for i in range(width))
    return list(itertools.chain.from_iterable(pairs)) + [3]


def literal_call(vm, state):
    vm.head, vm.state = 0, state
    for _ in range(1_000_000):
        if vm.head < 0:
            return vm.state
        if not vm.step():
            return 'halt'
    raise AssertionError('literal call exceeded the test budget')


class GuardTests(unittest.TestCase):
    def test_residual_prefixes(self):
        for word, cost, result in [('3434222424242244424424242', 129, '2444222444242242424224444'),
                                   ('3434242', 21, '2444244')]:
            self.assertEqual(trace_prefix(bytes(map(int, word)), 'B'),
                             ('B', cost, len(word), bytes(map(int, result))))

    def test_register_bits_and_raw_cost(self):
        for n in range(64):
            for width in (n.bit_length(), n.bit_length()+1):
                cells = register(n, width)
                self.assertEqual(rank_bits(cells, 0), (width, n))
                vm = TapeMachine(MACHINE, cells+[1, 0, 4])
                for _ in range(n):
                    self.assertEqual(literal_call(vm, 'A'), 'B')
                self.assertEqual(literal_call(vm, 'A'), 'A')
                self.assertEqual(literal_call(vm, 'B'), 'B')
                self.assertEqual(vm.steps, 2+7*n-4*n.bit_count()+8*width)

    def test_partial_register_on_unrestricted_tails(self):
        normal = 0
        for width in (1, 2, 3):
            for low in range(1 << width):
                prefix = register(low, width)[:-1]
                for tail in itertools.product(range(5), repeat=2):
                    vm = TapeMachine(MACHINE, prefix+list(tail))
                    for j in range(20):
                        reply = literal_call(vm, 'A')
                        if reply == 'A':
                            self.assertEqual(j % (1 << width), low)
                            self.assertEqual((vm.tape[0], vm.tape[1]), (2, 2))
                            normal += 1
                        if reply != 'B':
                            break
        self.assertGreater(normal, 40)

    def test_one_cell_switch_at_the_outer_guard(self):
        for k in range(1, 9):
            d = 3**k
            width = d.bit_length()+1
            halting = [0, 3]+[2]*k+register(d, width)
            safe = [0, 3]+[2]*k+register(d+(1 << (width-1)), width)
            self.assertEqual(sum(a != b for a, b in zip(halting, safe)), 1)
            for exterior in ([], [1, 0, 4]):
                vm = TapeMachine(MACHINE, halting+exterior)
                self.assertEqual(literal_call(vm, 'A'), 'halt')
                self.assertEqual((vm.head, vm.tape[0], vm.steps),
                                 (0, 1, 9*d+2*k+5-4*d.bit_count()+8*width))
                vm = TapeMachine(MACHINE, safe+exterior)
                self.assertEqual(literal_call(vm, 'A'), 'A')
                self.assertEqual((vm.head, vm.tape[0]), (-1, 3))

    def test_two_halting_routes_after_a_real_prior_B_exit(self):
        for word, clock, entries, replies in [('0004', 65, 'ABA', 'AAA'),
                                              ('0022', 31, 'AAB', 'BAB')]:
            vm = TapeMachine(MACHINE, map(int, word), head=1)
            for _ in range(3):
                self.assertTrue(vm.step())
            self.assertEqual((vm.head, vm.state, vm.tape[1]), (0, 'A', 3))
            sent, received = [], []
            while vm.steps <= clock:
                x = vm.head
                if not vm.step():
                    break
                if (x, vm.head) == (1, 2):
                    sent.append(vm.state)
                if (x, vm.head) == (2, 1):
                    received.append(vm.state)
            self.assertEqual((vm.head, vm.state, vm.tape[0], vm.steps), (0, 'A', 1, clock))
            self.assertEqual((''.join(sent), ''.join(received)), (entries, replies))

    def test_suspended_header_for_every_small_rank(self):
        for k in range(1, 5):
            cut = k+2
            for j in range(2*3**k):
                trial = TapeMachine(MACHINE, [0, 3]+[2]*k+register(j, j.bit_length()))
                cost_outside = 0
                while True:
                    x = trial.head
                    self.assertTrue(trial.step())
                    cost_outside += x < cut
                    if x == cut and trial.head == cut-1 and trial.state == 'A':
                        break
                digits, q = [], j
                while q:
                    q, digit = divmod(q, 3)
                    digits.append(digit)
                self.assertEqual(cost_outside, 2*j-sum(digits)+k+2)
                before = trial.steps
                while 0 <= trial.head < cut and trial.step():
                    pass
                outcome = 'safe' if trial.head < 0 else 'needs_tail' if trial.head == cut else 'halt'
                local = rank_return(k, j)
                self.assertEqual((local['outcome'], local['steps_after_reply'],
                                  local['head_from_guard'], local['state']),
                                 (outcome, trial.steps-before, trial.head, trial.state))

    def test_fibonacci_family_of_forced_halts(self):
        fib, successor = 1, 1
        for k in range(1, 9):
            found = 0
            for digits in itertools.product('02', repeat=k):
                word = ''.join(digits)
                if word[0] != '0' or word[-1] != '0' or '22' in word:
                    continue
                found += 1
                offset = int(word, 3)
                self.assertEqual(rank_return(k, offset)['outcome'], 'safe')
                j = 3**k+offset
                width = j.bit_length()
                local = rank_return(k, j)
                self.assertTrue(local['ternary_propagation'])
                self.assertEqual((local['outcome'], local['head_from_guard']), ('halt', 0))
                vm = TapeMachine(MACHINE, [0, 3]+[2]*k+register(j, width))
                self.assertEqual(literal_call(vm, 'A'), 'halt')
                self.assertEqual((vm.head, vm.steps), (0, 9*j+2*k+5-4*j.bit_count()+8*width))
            self.assertEqual(found, fib)
            fib, successor = successor, fib+successor

    def test_fixed_cut_absolute_clock_and_followup_calls(self):
        good, k0 = 2, 2
        cut = 2+k0
        d = 3**(k0+good)
        for j in (d-1, d, d+1):
            at_fixed_cut = d-3**k0+j
            word = [3]+[2]*k0+register(at_fixed_cut, at_fixed_cut.bit_length())
            seed = snapshot(1, Calls(word, raw=3))
            _, ledger = audit_blocks(seed, 1+good+1, 10**7, 5)
            got = follow(seed, ledger, calls=6)
            literal = TapeMachine(MACHINE, [0]+word)
            while True:
                x = literal.head
                self.assertTrue(literal.step())
                if x == cut and literal.head == cut-1 and literal.state == 'A':
                    break
            self.assertEqual((int(got['first_A_raw_steps_hex'], 16), got['first_A_head']),
                             (literal.steps+3, literal.head-1))
            events, local_steps = [], 0
            while literal.head >= -good:
                x, entry, clock = literal.head, literal.state, literal.steps
                if x == cut:
                    if len(events) == 6:
                        break
                    while literal.head >= cut and literal.step():
                        pass
                    reply = literal.state if literal.head < cut else 'halt'
                    events.append({'entry': entry, 'reply': reply, 'prefix_steps_before': local_steps,
                                   'inside_steps_hex': hex(literal.steps-clock)})
                    if reply == 'halt':
                        break
                elif literal.step():
                    local_steps += 1
                else:
                    break
            self.assertEqual(got['after_first_A']['tail_calls'], events)
            self.assertEqual(got['after_first_A']['steps_after_reply'], local_steps)

    def test_geometric_batches_and_first_exception(self):
        ordinary, batched = Calls(), Calls()
        epoch = 0
        while epoch < 128:
            n, halted = batched.epoch_block(min(19, 128-epoch))
            self.assertFalse(halted)
            for _ in range(n):
                self.assertTrue(ordinary.epoch())
            epoch += n
            self.assertEqual(snapshot(epoch, ordinary), snapshot(epoch, batched))

        for good in range(5):
            k = 2
            n = 3**k*(3**good-1) + 3**(k+good)
            tail = [3]+[2]*k+register(n, n.bit_length())
            ordinary, batched = Calls(tail), Calls(tail)
            if good:
                self.assertEqual(batched.epoch_block(good+2), (good, False))
                for _ in range(good):
                    self.assertTrue(ordinary.epoch())
                self.assertEqual(snapshot(good, ordinary), snapshot(good, batched))
            self.assertEqual(batched.epoch_block(5), (0, True))
            self.assertFalse(ordinary.epoch())
            self.assertEqual(snapshot(good, batched, halted=True), snapshot(good, ordinary, halted=True))

        end, log = audit_blocks(snapshot(0, Calls()), 128, 10**7, 17)
        self.assertEqual(end['epochs'], 128)
        covered = {e['epoch'] for e in log['exceptional_or_literal_epochs']}
        for first, last in log['all_B_epoch_ranges_inclusive']:
            self.assertTrue(covered.isdisjoint(range(first, last+1)))
            covered.update(range(first, last+1))
        self.assertEqual(covered, set(range(1, 129)))


if __name__ == '__main__':
    unittest.main()
