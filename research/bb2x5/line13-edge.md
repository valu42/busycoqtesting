# Line 13 can halt only at a fresh right edge

On the blank orbit, line 13 halts exactly when some odd coordinate receives a first A after a positive even number of B entries from its left. The head then reaches the undefined instruction B3 at that odd coordinate in two more defined steps. Here an entry is the state of the head as it crosses into the coordinate from the left. The initial A at coordinate zero also counts as an entry.

## What happens at the first A

The machine is `1RB3RA3RB4LA1LA_1LB2LA1LA---1RB`. Until a fresh cell's first A, its first B writes 1 and moves left in B. Further B entries alternate its symbol between 2 and 1 and move left in A. None of these entries touches its right neighbor.

| Leading B entries | Symbol at first A | First call to the right | Return to the parent |
|---|---:|---|---|
| Zero | 0 | A0 writes 1 and sends B | The fresh child returns B. B1 writes 2 and exits left in A. |
| Odd | 1 | A1 writes 3 and sends A | A on a fresh suffix returns A in three steps. A3 writes 4 and exits left in A. |
| Positive even | 2 | A2 writes 3 and sends B | B0 on the fresh child writes 1 and moves left in B. The parent now scans 3. |

Every defined instruction writes a nonzero symbol. B0 is the only instruction that moves left in B, so after the first visit a child can only return left in A. Also, every instruction that exits a cell to the left leaves 1, 2 or 4 behind. No subsequent entry from the left can itself find 3. The only way to reach B3 is therefore the last row of the table. At coordinate zero the initial A always exits left in A, as do all subsequent completed excursions. These are precisely the inputs for which the [negative-half driver](mixed-and-sweeps.md#5-other-candidates-and-verification) gives a finite return on every call.

Coordinate zero first receives A, so the first entry at coordinate one is B. A cell whose first entry was B can only open the following coordinate through the odd or positive-even row. The odd row sends A. The positive-even row halts at the parent as soon as its child returns. Induction gives an A first at every even parent that opens a new cell before a halt and a B first at every odd parent. The exceptional even child entered in B at the halting event immediately returns to its odd parent.

## Reading an edge trace

From `research/bb2x5`, the following run reports the first 48 rightward entry letters seen at each coordinate during one batch. The array index is the physical coordinate. Short words contain every entry through the end of the batch.

```sh
c++ -O3 -std=c++17 frontiers/longitudinal.cpp -lgmpxx -lgmp -o /tmp/bb25-stream
python3 frontiers/longitudinal.py --line 13 --engine /tmp/bb25-stream \
  --groups 100000000000000 --trace-prefix 48 --checkpoint /tmp/line13.json
```

This blank run visits coordinates 0 through 127. Of the odd coordinates, 61 start with `BA`. Coordinates 91 and 97 start with `BBBA`. Coordinate 127 has received just `B` at this endpoint. If resuming from a checkpoint, each trace begins at that batch's first entry. Complete the prefix at a previously visited coordinate by concatenating its entries across batches in order, truncating only after enough letters have been collected.

An externally supplied input `ABBAAA` at coordinate zero sends `BBA` to coordinate one and halts there. This gives a short control case for the positive-even branch. The blank input at coordinate zero is A followed by repeated `BABAB`. Deciding whether this particular source produces an exceptional odd coordinate remains open.
