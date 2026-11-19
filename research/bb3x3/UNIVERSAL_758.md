# A contiguous halting basin for #758 and #153

**All 11,177,973,024,732 reset seeds from H−11,177,976,427,786 through H−3,403,055 halt.** The check below directly covers offsets through 10,000,000,000,000. It overlaps the previously proved interval at offsets 6,706,785,856,672 through 11,177,976,427,786. Both endpoints are included. [Independent outer interval](GATEWAYS_758.md)

At the blank orbit's first crossing of mass $W>2(H-3{,}403{,}055)+1$, a reset in the preceding **2,483,994,005,496** ordinary counter updates would suffice for halting. If the orbit avoids the basin, its last preceding reset must have second counter below the lower endpoint. Crossing the upper mass would then take a gain of at least $2w+1$, where $w=11{,}177{,}973{,}024{,}732$. Each continuing update gains at most nine, giving the stated bound $\lfloor2w/9\rfloor$. Whether the blank orbit satisfies this condition is open.

A subsequent check covers every remaining distance through 33,533,929,283,358 and proves that **33,533,925,880,304 consecutive reset seeds halt**. The same upper crossing now has a sufficient recent-reset bound of 7,451,983,528,956 calls. [Additional bands and proof](LOWER_SCALE_GATES_758.md)

## Original certificate

| First offset | Last offset | Bands | Bisection nodes | Accepted leaves |
|---:|---:|---:|---:|---:|
| 64,000,000 | 5,000,000,000 | 2 | 21,659,016 | 10,829,509 |
| 5,000,000,000 | 1,000,000,000,000 | 100 | 1,251,114,470 | 625,557,285 |
| 1,000,000,000,000 | 10,000,000,000,000 | 90 | 5,256,291,790 | 2,628,145,940 |

Write H for the known halting reset and let d = H−c at A(1,c). The existing exact [halting basin](COVER_758.md) covers every d from 3,403,055 through 64,000,000. The universal checker extends this interval by examining every seed parity. A certificate for a band [l,h] establishes that **each** reset from the band either halts along the checked path or reaches another reset with strictly smaller d and d ≥ 3,403,055. Descending induction on c, equivalently strong induction on increasing d, therefore proves halting at every intermediate seed. The conclusion applies to #153 through its published join with #758. Entry from blank into the basin remains open.

The [near-H counter reduction](GATEWAYS_758.md) supplies two exact computations. When d is odd, the reset seed H−d is even and the checked first-return increment lies between 605 and 615. Our bands start beyond 64 million, so each such return respects the inner endpoint. When d is even, the reset seed is odd. A fixed prefix, a batch of k odd/odd jumps and a finite word of bulk, jump and exceptional moves precede the final reset or halt. The checker compares both ends of each even-d interval. Equal k and equal words suffice for every intermediate even d, as proved by the opposite coordinate order and the exceptional-branch equality in the gateway calculation. An even-first-counter terminal at the end of this word may halt or reset. On reset the actual increment is at most the common word's mass bound, which uses the larger permitted contribution for each bulk.

The verifier accepts a leaf when its two endpoint words agree and that common increment bound is at most l−3,403,055. If the words differ, it bisects the even distances into disjoint progressions. A shared word whose bound exceeds the allowed gain fails verification. Each nonhalting return decreases d because every live update increases a+2c. All bands include their endpoints, so one endpoint shared by neighboring bands is checked twice. The certificate gives a conclusion about all seeds in the interval without tracking a single entrance strip.

The [four-column manifest](universal_758.tsv) gives the near and far offsets and the exact bisection node and leaf counts. The 192-band calculation used a bounded-integer endpoint matcher that falls back to exact arbitrary-precision arithmetic at an ambiguous comparison. Selected bands were also checked independently with the GMP reference implementation. The reference executable provided here reconstructs every band using GMP integer arithmetic. Compile the gateway checker as described in [GATEWAYS_758.md](GATEWAYS_758.md), then use the manifest shipped with this note:

```sh
python3 check_universal_758.py universal_758.tsv --row 1
python3 check_universal_758.py universal_758.tsv --jobs 4
```

The first command replays one band. The second replays every band and compares the resulting counts to the manifest.
