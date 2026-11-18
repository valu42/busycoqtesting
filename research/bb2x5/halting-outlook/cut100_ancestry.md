# Line 34 · Five consecutive increases are impossible

**On every blank sweep from epoch 1,300 onward, the word after cell 100 cannot contain `1211312113121131211312113`, five consecutive copies of `12113`.** This excludes five consecutive positive groups in the [signed count of unmatched closings](cut100_charge.md). The proof uses three earlier sweeps. It makes no assumption about the future guard or the eight-cell bound. It does leave open whether *separated* positive groups can build enough debt to halt.

The machine is `1RB2LA4RA1LA3LA_0LA2RB3RB2LB---`. The start commit, blank checkpoint, physical timing proof and two sufficient conditions for nonhalting are in the [line 34 report](cut100.md).

## Looking three sweeps back

Take an ordinary interior factor of the current word. It comes from adjacent survivor bits of the previous matching sweep. Equal bits emit `1`, a fall emits `2` and a rise emits `3`. A factor containing a fall or rise determines every one of those bits, including the bit before its first digit. Each one marks an older opening that survived. Between two such openings, all old Os must pair with Cs inside the gap. A C pairing to the left of the gap would have consumed its bounding opening first. An O pairing to the right of the gap would be shielded by the next surviving opening.

Suppose a gap has length $L$, contains $q$ Cs and starts and ends in generating bits $p,p'$. It contains $q$ Os and $q+p-p'$ neutral digits, hence $L=3q+p-p'$. A length congruent to one modulo three forces a fall from one to zero. A length congruent to two forces a rise from zero to one. The nonzero residues of successive gaps must therefore alternate, even when some intervening lengths are divisible by three.

To recover candidate older factors, keep just the interval from the first forced survivor through the last. Each end is an O. Fill each gap with ordinary digits that have equal O and C counts and whose every prefix has at least as many Os as Cs. Carry the generating bit across all gaps. This includes every possible older interior, even if no exterior realizes a candidate. Ignoring the two loose ends can only add candidates.

| Target | One sweep back | Two sweeps back | Three sweeps back |
| --- | ---: | ---: | ---: |
| Five consecutive copies of `12113` | 33 candidates | 2 candidates | 0 candidates |

The first inverse has five gaps of length three. With starting bit zero, each gap must be `132`. With starting bit one, each is `123` or `213`, giving $1+2^5=33$ choices. Applying the same gap rule leaves only `111121111311112111131111211` and `111131111211113111121111311`. Decoding either gives two successive complete zero gaps of length five. Both demand a rise with no intervening fall. Neither can have an ordinary parent. The [enumerator](cut100_ancestry.py) also checks its inverse against 12,237 forward matching controls. [Transcript](cut100-ancestry-verification.txt)

At a successful sweep the header has length one or five. The oldest forced interval can start at most six normalized positions farther left per generation, so a factor after cell 100 stays clear of all three older headers. A final carry appends a neutral `2`. The target ends in `3` and all retained older intervals end in `1`, so no calculation uses an appended cell as an old survivor. Words from the blank run have sufficient ancestry long before epoch 1,300. The written finite exclusion has no proof-assistant formalization.

Each positive group is `12113` or `121132` with specified surviving openings. A group starts in generating bit one. The longer variant ends in bit zero, so another positive group cannot follow it immediately. Five consecutive positive groups would therefore contain the excluded 25-digit factor, even if their last group had the optional neutral. The proof bounds the length of a consecutive run of increases. It does not bound their total across neutral or negative groups.

## What eight earlier sweeps still permit

The ordinary periodic word with repeating block `21111323111` has more openings than closings on each of its first eight input generations. Start a period at a minimum of its cumulative opening surplus. Every closing then matches within that rotated period, independently of its neighbors. Applying the survivor-bit rule eight times gives the repeating block **`13232131232`**, with one excess closing per eleven digits. Repetition gives arbitrarily large interior deficits in this periodic example. The verifier records all nine words. This is a calculation on periodic data, distinct from blank execution. [Derivation and checks](cut100_ancestry.py)

For a finite physical control, keep the entire **1,585-cell** blank-run word, head and state at epoch 1,300. Append copies of the initial period immediately to its right. The genuine tape has zero copies. All three tapes below have identical guard and cut-100 debts for their first eight sweeps. The ninth sweep separates them.

| Appended copies | Ninth guard debt | Ninth cut-100 debt | Literal result from the checkpoint |
| ---: | ---: | ---: | --- |
| 0 | 1 | 0 | Completes nine sweeps in 51,255 instructions |
| 881 | 5 | 61 | Completes nine sweeps in 10,293,619 instructions |
| 882 | 6 | 62 | Reaches B4 after 10,293,928 defined instructions |

The literal interpreter checked every executed instruction and the entire tape, head, state and count at every completed boundary. It stopped on B reading 4 at coordinate −1,310 in the last case. These are three exact finite computations. They give no halt date or probability for the genuine tape. [Output](cut100-ancestry-verification.txt)

The next proof target is to follow positive groups **through their separators**. For example, determine which sequences of a positive group, zero-charge groups and another positive group survive the inverse gap test and can occur on the genuine blank orbit. The periodic control shows why a proof must use further structure to bound the cumulative deficit.

Run `python3 cut100_ancestry.py` from `research/bb2x5/halting-outlook` to reproduce both the ancestry exclusion and all three full-machine controls.
