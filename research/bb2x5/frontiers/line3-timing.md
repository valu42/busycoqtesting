# Line 3 mixed-counter clock

The [mixed-counter construction](../mixed-and-sweeps.md#1-the-mixed-counter-on-line-3)
describes a batch of successful right probes, each followed by one binary
increment to the left of the pivot. The tape at the end of a batch is already
determined by that construction. The clock below counts the defined instructions
executed inside the tokens and inside the binary register.

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
The [saved run](runs/line3-timed.json) continues to checkpoint 250, raw clock
approximately $7.15678\times 10^{242}$, with 507 ternary digits, one padding
cell and counter value zero. It is a finite blank run. The saved tape starts
at the absolute coordinate `left`. All cells outside `word` are zero.

These commands reproduce, continue and check the run from `research/bb2x5`.

```sh
python3 frontiers/line3_timed.py --checkpoints 250 --output /tmp/line3.json
cmp /tmp/line3.json frontiers/runs/line3-timed.json
python3 frontiers/line3_timed.py --resume /tmp/line3.json --checkpoints 251 --output /tmp/line3-next.json
python3 -m unittest discover -s frontiers -p test_line3_timed.py
```
