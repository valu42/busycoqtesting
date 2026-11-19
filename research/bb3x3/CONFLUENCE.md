# An exact checkpoint for #758

Every A(1,c) with **1,059,491,543,272,883 ≤ c ≤ 1,079,817,520,122,229** reaches **A(1,1,079,817,520,208,950)**. This covers 20,325,976,849,347 seeds. The lower endpoint is the [community's reported forward checkpoint](https://wiki.bbchallenge.org/wiki/1RB2LC1RC_2LC---2RB_2LA0LB0RA). The implication from that checkpoint is independently checked here. The exact lower endpoint is the published checkpoint. The independent [blank crossing](BLANK_CROSSINGS.md) reaches some reset in its first 5,001 seeds, so the common endpoint now follows from blank as well.

After the first move c is odd. Put q = floor((c+1)/4). When a ≥ 4q+3, the two bulk branches have the exact common update L(a,c) = (a−4q−3,6q+5). The other continuing interior branch J(a,c) = (3a+2,c−a+1) applies for odd a ≤ c. Even a ≤ c takes the return R to A(1,a/2+c+2).

For a fixed seed parity, the first move gives a fixed a and increasing c. Along any common L/J word, a stays nonincreasing and c nondecreasing as functions of the original seed, and the parity of a stays the same across seeds. L eligibility is an initial interval, and J eligibility at an odd phase or R eligibility at an even phase is a final interval. Two endpoints with the same L/J word ending in R therefore certify that word for all same-parity seeds between them.

In the stated interval, even seeds have the word J³⁰LR after the first move. Odd seeds have J³⁰LLJJLR. Writing W = a+2c, the first move costs at most 8 in W for even seeds and 4 for odd seeds, L at most 9, J exactly 4, and R exactly 5. Consequently the next return advances c by at most 71 or 82, respectively. This also bounds an earlier visit to a = 1 within the word since W strictly increases. All seeds continue and c increases strictly at returns. Every trajectory therefore leaves the interval, and its first exit comes from the last 82 seeds. Exact evaluation yields 23 distinct exits. Tracing 1,216 distinct return edges sends them all to the stated common checkpoint.

```sh
python3 check_confluence.py
```
