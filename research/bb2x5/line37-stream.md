# Line 37 as a recurrence on ultimately periodic words

For `1RB2LA3LA4RA1LA_0LA3LB3RB1RB---`, the blank computation halts exactly when the following recurrence produces a stream starting with an integer at least 3. The starting stream is the constant word 111… . Each iterate is represented exactly by a finite prefix and a repeating period. The recurrence makes no assumption about the guard schedule or the maximum matching debt. I have not decided whether a forbidden leading letter ever occurs.

Use the sweep epochs and digit map D in [the right-boundary proof](line37-pascal.md). A tape symbol 2 is an opening, 1 a closing, and 3 is neutral. Reading a word from its right end, a closing adds one unit of matching debt; an opening consumes a unit if possible, and survives otherwise. For a cell record the debt **after** processing it, together with its survivor bit. Encode the possible pairs as stream letters.

| Letter | Debt | Survivor bit |
|---|---:|---:|
| 0 | 0 | 0 |
| 1 | 0 | 1 |
| n ≥ 2 | n−1 | 0 |

For a cell at fixed distance j from the right edge, list these letters in chronological order, starting with its birth epoch. The word grows after each successful sweep, so j continues to exist. A stream may be extended through hypothetical future epochs using the triangular suffix rule. Its letters agree with the physical tape throughout the actual computation up to a halt.

## The one-cell transducer

Let M_q act on a stream with initial cell digit q. For each input letter unpack the incoming debt d and right neighbor's survivor bit r. The new survivor bit s equals one precisely when q=2 and d=0. The outgoing debt is e=max(0,d+[q=1]−[q=2]). Emit the letter for (e,s), then replace q with D(s,r) before reading the next input. This three-state transducer sends any ultimately periodic stream to an ultimately periodic stream: after its finite prefix, the input phase and q range over finitely many pairs. During a finite period the integer output alphabet is finite as well.

## Epoch update

Start at epoch 1 with the one-digit word 2. Its rightmost column always stays a surviving 2, hence its chronological stream is Z = 111… . At any epoch, Z denotes the stream of the current **leftmost** column, starting at that epoch. If its first letter encodes (H,s), then H is the number of unmatched closings in the entire current tape word. If H≥2 the machine reaches B4 during this sweep.

For H≤1, let V be Z with its first letter removed. Initially replace V by M_q(V), where q=1 if s=1 and q=2 otherwise. Next perform one of the following lists of replacements in the given order. The final V is Z for the next epoch.

| Current H | Replacements after M_q | Change in word length |
|---:|---|---:|
| 0 | M₂ | +2 |
| 1 | M₂, M₂, M₁, M₂ | +5 |

To see this, let n be the old width. For old right-indices 0 through n−1, the streams simply advance by one epoch. New right-index n starts with D(0,s). This digit belongs to the converted old leftmost cell. Its predecessor at fixed right-index n−1 supplies the chronological stream V starting on the next epoch, so M_q gives the correct stream for the new column n. The remaining new columns have the initial digits of the guard header taken right-to-left, namely (2) or (2,2,1,2). Each consumes its immediate right neighbor's stream through its own M. The last is the new leftmost column. This proves the recurrence by induction, including the halt test.

If one assumes the observed single reset per eleven sweeps, eleven such updates use 25 new columns and discard eleven chronological samples. The recurrence itself checks the debt at each update and can handle a different successful guard pattern. This distinction matters when searching for an invariant of the stream iterates.

Run `python3 line37_stream.py` alongside `prior_sweeps.py`. It compares 512 consecutive blank updates and overlapping eight-epoch predictions for each fresh leftmost column with the independent word sweep. At epoch 513 the word has 1,163 cells; the reduced chronological stream of its leftmost column has a prefix of length 523 and period 1,024.
