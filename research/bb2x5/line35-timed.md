# The line 35 guard through 150,000 blank-tape epochs

For line 35 (`1RB2LA4RA1LA3LA_0LA3RB3LB2RB---`), epoch 150,000 begins after **73,421,002,000 defined instructions**, with A on the blank at −155,058 and a contiguous word of length 305,057 immediately to its right. The full word, encoded as one byte per symbol, has SHA-256 `eede34c04e3481911a0cbdc6c8f9f046a635db7b8fe469e558618bc97c4f59dc`. The blank-tape halting status is open.

From epoch 5 through 149,999, the numbers of sweeps with guard debt 0, 1, 2, and 3 are 74,154, 64,039, 10,116, and 1,686 respectively. The pair of guard debt and debt after the first eight cells agrees with its value 89 epochs earlier at every epoch from 144 through 149,999. It differs at epoch 143. Every observed complete 89-epoch block in this range adds 181 tape cells. Proving the observed repetition persists would settle the machine. The existing [eight-cell criterion](line35-pascal.md) already suffices if cut-8 debt is always at most four.

A global bound of five on the debt at *all* cuts fails on the genuine blank tape. After epoch 5 the successive first occurrences of maximum interior debt 2, 3, 4, 5 and 6 are epochs 6, 34, 189, 1406 and 30354. This distinguishes interior debt from debt at the guard, whose sixth unit would cause a halt.

## Counting the literal moves

Use the [known sweep law](line35-pascal.md). At the start of an epoch let the word have width $n$ and end in a closing. This holds at epoch 5 and is preserved by every successful sweep. Let $d$ be total guard debt, $s$ the number of surviving openings, and $A$ the sum of the suffix debts over all cuts, including the cut before the first digit. The blank cut after the last contributes zero. Denote the header width by $h$. For $d<6$, the number of defined instructions to the next epoch is

$$h+2(2n+1+A-s+e_d),\qquad (e_0,\dots,e_5)=(1,1,2,8,9,11).$$

The net motion of the head is $-h$, so it suffices to count right moves. On the outward pass, the head has net displacement $n+1$ to the first blank beyond the word. Each matched closing walks left to its partner. Each unmatched closing walks left to its guard. The sum of the matching distances, measured to the original guard for unmatched closings, is $A$: count each crossing of each cut by its pending closing. On the third and later guard uses there is one extra left step per use to the guard reset position. In addition the single local reset makes a closed excursion of ten steps there (five left and five right), with the A0 departure then resuming the outward path. Thus the outward right moves total $n+1+A+\max(0,d-2)+5[d\ge3]$.

On return the physical row contains 3 at each of the $s$ surviving source cells and 2 at all other source cells. Label ternary digits by the cycle (3,1,2). At each non-wall site the return adds one plus the incoming carry to the original digit; each outgoing carry costs one right move from this site. The total addition is at most four and each site emits at most one carry. Every source 2 emits one and every source 3 emits zero. The rightmost 2 also causes one right move from the adjacent blank, via A0 then B0 and A1. The raw headers at debts 0 through 5 are respectively `1`, `3`, `2`, `3412`, `3432`, `3422`. Following the same return over these headers gives respectively 0, 0, 1, 1, 1, and 2 right moves. The wall 4 writes 3 and emits no carry. Combining the two passes yields the displayed constants.

The implementation uses the [line 37 carry-mask method](line37_orbit.py) with opening and closing symbols exchanged. At matching level $k$, the bit at a cut is set if a pending closing occupies that level at the cut. Popcounts across all levels therefore compute $A$. The number of levels encountered gives the maximum debt over all cuts, and sampling cut zero and cut eight gives their respective debts.

## Reproduction

From this directory, with Python 3.10 or later:

```sh
python3 line35_timed.py --epochs 150000 --check-window frontiers/runs/window-35.json --output frontiers/runs/line35-epochs.json
```

Before running the long calculation the checker compares the tape, clock and head against the literal interpreter for every word ending in a closing of length 1 through 8, including failures on B4. It obtains the blank seed by literal execution to epoch 5 at step 97. At epoch 55,363, the clock is 9,999,897,285. From this epoch 102,715 literal transitions reproduce the full tape, head and state in the existing ten-billion-step checkpoint. The [saved checkpoint](frontiers/runs/line35-epochs.json) contains the entire word, head and clock. To continue to an absolute epoch, pass this checkpoint with `--resume`, set `--epochs` and select a new output path.

## An altered tape shadows almost ten guard periods

Let $W$ be the actual epoch-400 word. On a blank exterior, start A immediately left of the finite word formed by appending 1,358 copies of `12323112321132311123213121323112111311211311213` and one final `2` to $W$. For all 888 successive sweeps corresponding to epochs 400 through 1287, both its guard debt and its cut-8 debt equal the blank run's. At epoch 1288 the altered word has guard debt 6. Its literal execution reaches B4 at head −920 after 282,627,758 defined steps, with positions measured from the altered initial head at zero. These calculations concern an altered suffix and leave the genuine blank orbit open.

The block was found by testing circular words. For a circular matching with positive balance, every closing has a partner and there is a surviving opener. Thus a cut with zero matching debt exists. Processing a whole period from incoming debt zero locates the initial cut's cyclic debt, and a second pass from that debt marks all periodic survivors. Applying the ordinary output rule gives the next circular word. The selected ring has negative balance after 888 updates. The finite planted tape was separately replayed, so its delayed halt follows from the finite checks below.

```sh
python3 line35-shadow.py --literal
```
