"""Compare physical block crossing to literal execution through both historical resets."""
import unittest
from line17_pile import EMBEDDED, RESIDUAL, Pile, embedded_tally, exceptional_sweep
from line17 import literal_counts
from prior_frontier import digits, marks_on_word
from prior_frontier import HEAD, T17


def original_sweeps():
    # Physical clocks are counted before fetching the next instruction.
    tape = {}
    x = state = right = 0
    seeds = {252: (-12, 7, 9), 2889: (-37, 20, 400)}
    target = None
    found = []
    for n in range(2_308_941):
        if n in seeds:
            base, width, normal = seeds[n]
            target = (base-2*normal, width, normal)
        if target and target[0]==x and state==0 and x < min(tape, default=0):
            _, width, normal = target
            row = ''.join(str(tape.get(i,0)) for i in range(x+1,max(tape)+1))
            if row.startswith(HEAD+'12'*normal) and len(row)==7+2*(normal+width):
                found.append((n, normal, row[6+2*normal:-1]))
                target = None
        if n==2_308_940: break
        symbol, dx, state = T17[state][tape.get(x,0)]
        if symbol: tape[x]=symbol
        else: tape.pop(x,None)
        x+=dx
    return found


class TestPile(unittest.TestCase):
    def test_deep_repeated_crossing(self):
        pile = Pile()
        original = pile.join(1, 2)
        expected = pile.join(0, 3)
        for _ in range(1500):
            original = pile.join(original, original)
            expected = pile.join(expected, expected)
        # Entering a 12 from the right in A writes 03 and exits left in A
        # in exactly two steps. The depth is above Python's recursion limit.
        self.assertEqual(pile.cross(original, True, 0), (expected, -1, 0, 2**1501, None))

    def test_invalid_inputs(self):
        for size, data in ((-1, '02'), (0, '01'), (1, '3')):
            with self.assertRaises(ValueError):
                exceptional_sweep(size, data)

    def test_three_embedded_header_paths(self):
        signatures = []
        for target in (1, 2, 3):
            tape = {i:int(s) for i,s in enumerate('04'+'0'+EMBEDDED, -2)}
            x = state = count_a = 0
            calls = ''
            for moves in range(100):
                if x == -2 and state == 0:
                    break
                if x == 9:
                    calls += 'AB'[state]
                    count_a += state == 0
                    state = int(state == 0 and count_a == target)
                    x -= 1
                tape[x], direction, state = T17[state][tape.get(x, 0)]
                x += direction
            self.assertEqual(''.join(str(tape.get(i,0)) for i in range(-2,9)),
                             '0'+EMBEDDED+'12')
            signatures.append((calls,moves))
        self.assertEqual(signatures,[('BBBABBB',73),('BBBABBABB',75),('BBBABBABBAB',77)])

    def test_embedded_epoch_clock_and_complete_tape(self):
        for symbol in '102':
            data = symbol+'2'+'02'*20
            for epochs in (1,2,7,24):
                word = bytes((0,1,0,0))*epochs
                counts = []
                for v,_ in digits(data):
                    counts.append(literal_counts((v,0),word))
                    _,word = marks_on_word((v,0),word)
                steps, updated = embedded_tally(epochs,data,counts)
                left = RESIDUAL+'04'*epochs
                physical = left+'0'+EMBEDDED+data+'2'
                cells = {i:int(s) for i,s in enumerate(physical) if s!='0'}
                x,state = len(left),0
                for _ in range(steps):
                    write,dx,state = T17[state][cells.get(x,0)]
                    if write: cells[x] = write
                    else: cells.pop(x,None)
                    x += dx
                expected = RESIDUAL+'0'+EMBEDDED+'12'*epochs+updated+'2'
                self.assertEqual((x,state),(len(RESIDUAL),0))
                self.assertEqual(cells,{i:int(s) for i,s in enumerate(expected) if s!='0'})

    def test_known_blank_resets(self):
        starts = original_sweeps()
        self.assertEqual(len(starts),2)
        # Existing literal blank checkpoints independently give the first new
        # cell and the next fully decoded normalized header.
        for (start,k,data), edge, finish, expected_width in zip(starts,
                (2628,2306191), (2889,2308940), (20,424)):
            outcome, elapsed, edge_delay, _, width = exceptional_sweep(k,data)
            self.assertEqual((outcome,start+edge_delay,start+elapsed,width),
                             ('header',edge,finish,expected_width))

    def test_artificial_small_cases(self):
        for trit,expected in [('1',('header',225)),('0',('halt',1477))]:
            # These cases may include more than one sweep from their initial
            # header. The generic literal solver continues to the first edge.
            outcome, elapsed, _, _, _ = exceptional_sweep(0,trit+'2'+'12'*3)
            self.assertEqual((outcome,elapsed),expected)


if __name__=='__main__':
    unittest.main()
