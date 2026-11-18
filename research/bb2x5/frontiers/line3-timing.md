# Line 3 mixed-counter clock

The [mixed-counter construction](../mixed-and-sweeps.md#1-the-mixed-counter-on-line-3)
describes a batch of successful right probes, each followed by one binary
increment to the left of the pivot. The [arithmetic research pass](https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/halting-outlook/arithmetic.md#line-3)
derived the timing formula below and recorded checkpoint 300. This
implementation counts the defined instructions in the existing mixed-counter
simulator and saves a resumable full tape.

| Right token | Incoming probes | Calls to the next token | Raw instructions on this token |
|---|---:|---:|---:|
| Pair with initial digit $d$ in $\{0,1,2\}$ | $c$ | $h=\lfloor(c+2-d)/3\rfloor$ | $3c+h$ |
| Single 4 | $c$ | $2c$ | $3c$ |

For a pair, A2 reads the first cell and B reads the second. A positive digit
then returns in B. For a zero digit, B2 calls the next token and B3 handles
its return. B0 on the leading cell finishes each probe. On a single 4, the
instructions are A4, B2 and B3, with two recursive calls between them.
The capacity test ensures zero calls leave the last token. Adding the table's
last column over all tokens therefore counts every instruction on the right.

On the left, incrementing $z$ flips its trailing ones and walks back over them.
It costs $1+2v_2(z+1)$ instructions, with two extra when a full register
grows. At growth the last carry runs through the marker and the instructions
B1, A0 and B2 recreate it one cell farther left. For $n$ increments the binary
cost is

$$
3n+2\bigl(\operatorname{popcount}(z)-\operatorname{popcount}(z+n)\bigr)+2g,
$$

since $\sum_{i=1}^t v_2(i)=t-\operatorname{popcount}(t)$. Here $g$ is
the increase in bit length of the full register. For a partial register $z$
is its unsigned low-bit value, and the capacity cap prevents overflow, so
$g=0$. Outside these batches the clock counts each defined instruction once.

From blank, checkpoint 9 agrees with the earlier 59,171-step trace. A literal
replay agrees on every nonblank cell, the head and the state at raw step
4,310,726. Continuing independently from the saved 100,000,000-step window
meets the blank replay at checkpoint 14, raw step 386,948,416. At checkpoint
150 the register matches the [earlier transcript](../mixed-verification.txt).
At checkpoint 300 the exact clock (approximately $4.74786\times 10^{287}$),
every nonzero tape cell, the head at −591 in A and the decoded counter tuple
agree with the [arithmetic pass checkpoint](https://github.com/valu42/busycoqtesting/blob/680c69635d58a26ad2d33814ac16df4f72a86975/research/bb2x5/halting-outlook/arithmetic_line3_checkpoint.json).
The [saved run](runs/line3-timed.json) continues to checkpoint 320, raw clock
approximately $3.09717\times 10^{312}$. The head is at −639 in A, with 653
ternary digits, one padding cell and counter value zero. Continuing the arithmetic
pass implementation from its saved checkpoint 300 reproduces the complete tape,
head, state and exact clock at 320. The saved tape starts
at the absolute coordinate `left`. All cells outside `word` are zero.

These commands reproduce, continue and check the run from `research/bb2x5`.

```sh
python3 frontiers/line3_timed.py --checkpoints 320 --output /tmp/line3.json
cmp /tmp/line3.json frontiers/runs/line3-timed.json
python3 frontiers/line3_timed.py --resume /tmp/line3.json --checkpoints 321 --output /tmp/line3-next.json
python3 -m unittest discover -s frontiers -p test_line3_timed.py
```
