# An exact finite certificate test for the Wily blank

At the 29-bit blank checkpoint the fixed low prefix supplies the repeating edge driver P = 222030111101130321301012. Let G act on a finite upper tape by performing these 24 arrivals in order, stopping immediately if one halts. The actual initial upper tape is empty. Thus any family of finite binary words containing the empty word and closed under successful applications of G proves that both blank Wily machines run forever. This test includes future positive excursions and corrective allocations. [Derivation of the driver](WILY_PHYSICAL_CORRECTIONS.md)

All of G, including physical allocations and intermediate halts, is represented by a transducer with **508 reachable states**. This makes a prospective regular-language proof independently checkable using a finite graph. For the actual driver, an inductive language recognized by a deterministic automaton needs **at least 15 states** reading from the low end, or **at least 10 states** reading from the high end. Tests of the exact finite-survival languages below have yet to produce a blank certificate.

## The return on all upper tapes

A transducer state is the chronological word of carries still reaching the next cell. On an input bit b, send these carries through the bit one by one. Output its final value and retain the live emitted carries, in order, as the successor state. At the end of the input tape, apply the remaining carries literally to an empty word. Its final value is the suffix to append, or a halt. The list of pending carries never lengthens on a bit, so this construction terminates from any finite driver. From P it enumerates 508 lists. An induction on input width gives exactly the physical map: the bits below the next cutoff evolve independently of the bits above it, and their emissions occur in chronological order. Undefined terminal output records a halt at any of the 24 arrivals.

Fix any complete low-first binary deterministic finite automaton (DFA), with start state 0 and transition table D. An accepting set is not needed. Take the synchronous product of the return transducer with two copies of D, reading the input and output bits. Start all three machines at their initial states. At each reachable product state:

* A halting terminal output marks the input DFA state dangerous.
* Otherwise read the terminal suffix from the output DFA state. Record an arc from the input DFA state to that final output state.

Each mark and each arc has a concrete finite-word witness. Conversely every finite word occurs in this construction. Propagate danger backward along the arcs to closure. The complement is the greatest union of DFA classes guaranteed to take a successful G step and remain in the union. The empty word is included exactly when state 0 survives. A failed test is an obstruction for this particular partition. The concrete witnesses on successive abstract arcs can be different tapes.

For high-first reading, start separately at each possible final transducer state with the DFA initialized on its terminal suffix in reverse order (or with a halting marker). Traverse transducer arcs backwards, updating the input and output DFA states on each bit. Reaching the transducer's initial state now gives the class pair for a whole input word. Backward danger propagation is the same.

The checker accepts any proposed JSON array of transition pairs. For example, `[[0,0]]` is the one-state table. A pass prints the accepting states of an explicit inductive certificate. Set `--high-first` for a table that reads from the high end. With `--start-round t`, the checker first verifies the first t rounds on the blank and tests membership from that point.

```sh
python3 wily_driver_invariant.py --dfa proposed_table.json
```

## Testing the finite-horizon languages

Let D_h be the language of words surviving h complete P rounds. D_0 is all words. Obtain D_(h+1) by reading G's output into the DFA for D_h and rejecting inputs with a halting terminal effect. Minimize the resulting DFA, then run the closure test above. This checks *every* union of its states, including stricter sufficient properties. The following tested partitions all reject the blank as a member of their greatest closed safe union.

| Horizon h | States in the minimal DFA for D_h |
|---:|---:|
| 1 | 313 |
| 2 | 994 |
| 5 | 5,471 |
| 10 | 21,920 |
| 20 | 86,084 |
| 30 | 191,001 |

These state counts concern these particular languages. At each of the 30 tested horizons the closed safe union is empty. A different choice of states can distinguish different histories even with far fewer states. For comparison, the same checker certifies an infinite, growing run of the alternate mode-2 driver from an empty upper tape with just three states. Its transition rows are (0,1), (0,2), (1,0) and its accepting states are 0 and 2. That same driver halts from the one-bit tape 1. This control uses the [known four arrival periods](WILY_EDGE_STREAM.md). Run `python3 wily_driver_invariant.py --horizons 30` to reproduce all 30 partitions. The default checks the first two.

## Concrete distinguishable prefixes

The [witness table](wily_driver_distinguishers.tsv) gives a separate lower bound on *every* deterministic inductive language in either indicated reading direction. Each row gives distinct prefixes p and q, a round t and a positive horizon h. Prefixes are encoded by interpreting their bits in reading order as low bits of an integer, with a terminating high one. Starting from the empty word, the actual G-orbit reaches a word p v at round t in the stated reading direction. Replacing just p by q produces a word q v which halts in exactly h rounds. For the high-first test reverse the words before running the physical sweeps.

Any inductive language must accept p v and reject q v. If a DFA ended in the same state after reading p and q, it would give the same answer on the common continuation v. Each pair thus forces distinct states. The table covers all 105 pairs among 15 low-first prefixes and all 45 pairs among 10 high-first prefixes. Its integers, times and halts are checked against the actual orbit and the full return map, as is the transducer itself against literal sweeps on all words of widths 0 through 9. These lower bounds do not limit larger certificates or other proof methods.

Run `python3 wily_driver_invariant.py` from this directory.
