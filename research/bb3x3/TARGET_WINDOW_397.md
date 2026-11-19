# A regular halting target at a recurring blank phase of #397

Let U be the following 40-bit suffix prefix, measured after removing the protected periodic bits.

```
1100010001000000000110000001100000011010
```

The blank trajectory has prefix U just before sweep index 1,161,058. At the same phase, **every complete word U (10)ⁿ 01, for n ≥ 0, halts on the fifth carry leaving U**, 1,124 sweeps later. Here (10)ⁿ denotes concatenation of n copies of `10`. The actual word at the witnessed index is 93 bits long and is outside this family.

For as long as the run survives, U and its sweep phase recur at indices 1,161,058 + 2,097,152j for every integer j ≥ 0. The [transitive-section theorem](TRANSITIVE_SECTION_397.md) gives the 1,024-sweep return for the first 29 bits and a period of 2¹¹ returns for the next eleven. At the offset within this period used here the map on occupied bits is conjugate to that at the start, since every carry permutes fixed-length bit words.

| Sweep index at the witnessed occurrence | Carry leaving U |
|---:|:---:|
| 1,161,058 | d |
| 1,161,153 | e |
| 1,161,642 | d |
| 1,161,985 | e |
| 1,162,182 | d |

These are the only arrivals across the cut in the indicated interval. They depend solely on U and the phase.

## Characterizing the tails

1. Among all finite tails starting with an arbitrary word and **ending in `001`**, the tails that halt during this five-arrival window are exactly (10)ⁿ 01 with n ≥ 1.
2. Among **all** finite tails, the tails that first grow by `d` at the very first arrival and halt during the window are exactly (10)ⁿ 01 with n ≥ 0.

In either case the first growth appends `001`, and the fifth arrival produces the halting `e` at the moving edge. A fresh growth on a word ending `01` leaves the `001` suffix used in the first statement. [First-contact tests](FIRST_CONTACT_397.md)

For the forward direction the pair `10` transmits both `d` and `e` unchanged and remains `10`. Thus any number of leading `10` pairs can be removed. Passing `deded` through `01` gives `dbacd`. The first `d` at an empty edge creates `001`. The next three arrivals turn it into `101`, then `011`, then `100`. The final `d` emits the halting `e`.

For the converse, label the five arrivals with their chronological indices. To process a prefix of an unknown tail, carry forward the ordered stream surviving that prefix. On reading an occupied bit, propagate the stream through that bit, retaining its intermediate updates and omitting early stops. At the end of the word apply the resulting stream to the actual empty edge, with growth and halting handled in order. There are 399 reachable labelled streams for the initial `deded`. Each update either retains or drops an input timestamp, so this is a finite calculation.

For the `001`-capped test, reserve the final three bits and mark a state accepting when passing its stream through `001` subsequently halts at the empty edge. Backward reachability leaves exactly the following states and transitions from which acceptance is still possible.

| Current stream | Bit | Next stream |
|---|:---:|---|
| `deded` | 1 | `fdfdf` |
| `fdfdf` | 0 | `deded` |

Only `fdfdf` accepts the reserved cap. The prefix before `001` must therefore be (10)ʳ 1. For the unrestricted first-growth test, use the same two transitions and add `deded` on 0 to `eaeae`, then `eaeae` on 1 to `dbacd`. Only `dbacd` accepts an empty continuation with the required growth and halt. The [verifier](target_window_397.py) constructs all states and checks both pruned tables against the six-carry rules.

If the blank run is infinite, every fixed word U (10)ⁿ 01 eventually appears as a **prefix** at the specified phase. This follows from transitivity on the first 11 + 2n + 2 cells beyond the 29-bit cut, after enough cells exist. Entry into the halting target requires the word to **end** there. Whether this ever happens from blank remains open.
