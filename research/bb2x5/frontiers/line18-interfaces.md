# Line 18 · excluding an A return at the moving cut

**Root-return theorem.** Suppose the odd-record suffix starts with `13`. Feed it one A request and any finite number of B requests, in order. Every completed request returns B across the outer cut, for every choice of the remaining tape. A suffix can still halt or run forever inside a request. In particular the theorem applies to any later record as soon as its first two digits are known. A literal control is the artificial suffix `134` followed by blanks. Its A request returns B and its first B request reaches A4.

At the checked-in record 9,333, just **1,866** suffix cells already suffice to exclude an A return in **366 consecutive record attempts**, 9,333 through 9,698. If some attempt fails to complete, the guarantee applies up to that point. During attempt 9,333 a first halt would have to be at or to the right of physical coordinate **+11,202**. The argument permits arbitrary initial cells and arbitrary returning behavior beyond the indicated prefix. These counts describe a protected region and a conditional horizon. The raw clock for the entire tape is recorded separately. [Blank checkpoint](runs/line18-returns.json) · [Verifier](line18_interfaces.py)

## A four-cell check proves the two-cell criterion

Consider `13xy` for each of the 25 possibilities for x and y. A graph node consists of the four current symbols, head position, and control state. Start at the left end in A. Inside the four cells, follow the original TM instruction. At the right exit, allow either A or B to resume on the last cell, independently on every visit. At the left exit, record the reply. A B reply begins another request in B on the first cell. A missing instruction is a terminal halt. Each actual finite excursion follows one of these paths because a returning exterior excursion leaves the four cells intact.

Exhaustive closure over the 25 starts visits 1,709 nodes, counting each start separately. No path exits in A. On every B exit the first digit is 3, since A2 → 3LB is the only instruction moving left in B. Among the 25 initial words, the graph can reach a local halt only from `1314`, `1334`, or `134x`. In particular all nine `13xy` with x and y in {1,2,3} are safe throughout their four cells, independently of every exterior reply. The three-cell graphs for `131`, `132`, and `133` all allow an A exit under the same arbitrary-reply model.

## Propagating a verified prefix through later records

Write a request stream as A followed by n copies of B. Where every child returns B, the following two tiles send the same type of stream to the next tile for n ≥ 1.

| Initial tile | Final tile | Number of B requests after the one child A |
|---|---|---:|
| `13` | `31` for even n, `32` for odd n | ⌊(n−1)/2⌋ |
| `133` | `313` | 2(n−1) |

For `13`, the A request leaves `34` without a child. The first B leaves `32` after one A child. The pair then alternates between `31` and `32`, issuing B on `31`. For `133`, the A request leaves `343`, and the first B leaves `313` after one A child. Each later B on `313` restores it and issues BB. Every conditional parent reply in these paths is B, and no local path reads A4. With n = 0 the A request on a leading `13` leaves `34` in three instructions and leaves everything farther right intact.

A clean positive halt criterion follows from the same transfers. The six cells `133313` on an incoming ABB prefix give two B replies. On the third request the head reaches A4 at offset 5 after 31 total instructions in those six cells. The trace never visits the exterior on the right. Thus a record whose tiles project at least two B requests after A onto an actual `133313` strip must halt, irrespective of the farther suffix. This is a synthetic control and a sufficient local target for the blank-orbit search.

Starting with $n=2^{k-1}$ at record k, the verifier follows whole tiles up to a closing four-cell guard `13xy` with x and y in {1,2,3}. The guard supplies every completed B reply required by the earlier conditional tiles. Induction back to the cut excludes any root A and excludes a halt in those tiles or the guard. Even if the exterior never replies, the machine cannot subsequently execute a local halt while waiting. On completion the concatenation of the tile outputs and the guard's leading 3 is known. Drop its first 3 into the growing left header and apply the same argument to the remaining known prefix at the next record. The [left-header traces](line18_header.py) justify the two left extensions and contain no undefined instruction while the suffix calls return B.

At record 9,333 this calculation guarantees 1,862 prefix cells at the next cut. At the last protected attempt, record 9,698, seven known cells exclude a halt strictly left of +9,708 and guarantee three cells at the following cut. The criterion can be reapplied after simulating the unresolved part of the tape.

## The binary tail under repeated B inputs

For any m ≥ 1 consider a right suffix consisting of m pairs, each `31` or `32`, followed by either a single 3 or no symbol, then blank tape. **Any number of B requests returns B, preserves this class of suffixes and avoids A4.** A `31` carries into its child and becomes `32` upon a B reply in four local steps. A `32` becomes `31` in three steps and stops the carry. Thus an ordinary carry through j low `31` pairs followed by one `32` takes 4j+3 steps.

If all m pairs are `31` and the terminal 3 is present, B on that 3 and the next blank returns B and leaves `32` in three steps. Unwinding gives `(32)^(m+1)` in 4m+3 steps. If the terminal 3 is absent, the innermost `31` together with its blank exterior physically returns B and leaves `31313` in 15 steps. This trace consumes the exceptional A from the virgin blank. The other m−1 pairs each take four local steps, yielding `(32)^(m−1)31313` in 4m+11 steps. Both outputs again consist of pairs and the permitted terminal symbol. This proves the claim by induction over requests. A leading A changes the reply for an entire stream. **On any such nonempty register, one A followed by any number of B inputs always terminates and returns A on every call.** Thus a halt inside an initially pristine binary register requires an A input *after* its first request. Two successive A inputs already halt on its first cell, since the first writes 4 and exits in A.

To prove the second assertion, first consider a virgin suffix in pairs of blank cells. A on the first `00` leaves `13` and returns A without calling deeper. On B inputs the virgin pair successively becomes `20`, `10`, then `13`. The third B sends one A right; the first two send nothing. Provided children return A, further B probes toggle `13` and `23`, sending one B on each `13`. The child input under either a B-only stream or an initial A with trailing Bs is therefore a shorter prefix of one of those same two types. Strong induction on the total number of requests proves both streams on blank return all A. On a terminal singleton 3 an initial A alone exits immediately. An initial AB leaves `13 32` and returns AA by literal execution. Every subsequent B on the leading `13` now issues BB to a nonempty binary register, restores `13` and returns A.

Induct on the number of pairs for a leading A on a nonempty register. It changes `31` or `32` into `41` or `42` and returns A. The first B on `41` sends A to the remaining register. When it returns A, the local pair is `23`; later B inputs alternate `23` and `13`, sending B on `13`. The child receives exactly a prefix of A followed by Bs, covered by induction. On `42` the first B produces `23` locally, and the next B gives `13`. Subsequent calls send only Bs into the remaining register. If it is nonempty or has a terminal singleton 3, its B replies keep the pair at `13`, sending BB and returning A each time. If it is virgin, its A replies instead give the alternation of `13` and `23`. These cases all give finite local paths and A replies at the original cut.

From `research/bb2x5`, verify the four-cell closures, the finite tile paths, both overflow bases, and the protected horizon with:

```sh
python3 frontiers/line18_interfaces.py
python3 frontiers/test_line18_interfaces.py
```

The tests compare every binary word of one through six pairs, with both terminal choices, against literal execution. They check the leading-A result through four pairs and 100 subsequent calls. They also compare projected prefixes with the next 100 blank-orbit records and with artificial suffixes that can actually halt.
