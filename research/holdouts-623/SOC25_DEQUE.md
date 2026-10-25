# Sliding-word acceleration for SOC25 reset rounds

**Result: one billion reset rounds from each of three initial states, with no halt.** At 100,000 rounds, the new deque implementation is 415–457 times faster than an independently written, compiled big-integer implementation of the same map. This is a measured representation improvement, not an exponential-time shortcut or a classification.

This additional direction arose while auditing [upstream PR #40](https://github.com/ccz181078/busycoq/pull/40). It is separate from [the Cubic Mess search](CUBIC26.md). The three representative tables below do not occur in the supplied 623-machine file, including under reflected state renaming; this work is not counted as progress on three additional members of that ordering.

## Source and exact scope

The return map is **`SOC25Iter.F` from upstream PR #40**, pinned at commit `069dc1eb72df69dfa595f491b5c315c3ce424ac6`. The source is [SOC25_Iter.v](https://github.com/ccz181078/busycoq/blob/069dc1eb72df69dfa595f491b5c315c3ce424ac6/verify/SOC25_Iter.v), written by Claude under Andrew McKnight's direction, building on BusyCoq's existing `SOC25Model`. Its integer map and halting reductions are their work, not new theorems claimed by this branch. The PR reports one million rounds from each of the three starts, with counter widths around 8.5 million bits.

The source file's Git blob hash was checked against the PR (`bfe85f62b2f0fdbdb89ec3b8aa080989404a1b36`). It compiled against this branch's dependencies with Coq 8.20.1 and passed independent `coqchk`. The eight `eqv_F` statements in that main file and `F_G` all reported closed assumptions. The separate `SOC25_Iter_v3.v` wrappers were not included in that audit. The upstream source was not copied into this PR.

`F` samples at complete left-overflow/reset boundaries. Its domain is

```text
L >= 1, 2 <= X < 2^(L+1).
```

For example, `(1,2)` maps to `(5,20)` and then to `(16,52144)`; `(3,6)` halts. These are reset rounds, not individual counter ticks or raw TM transitions.

| CLI start | Initial (L,X) | One representative machine |
| --- | --- | --- |
| 1 | (1,2) | `1RB1LA_1LC1RD_1LA0LC_1RE0RB_1RF1LA_1RA---` |
| 2 | (2,4) | `1RB1LA_1LC1RD_1LA0LC_1RE0RB_1RF1LC_1RA---` |
| 3 | (1,3) | `1RB1LA_1LC1RD_1LA0LC_1RE0RB_1RF0RB_1RA---` |

The upstream proof relates additional tables to the same three starts. No equivalence or classification is inferred merely from a transition-table resemblance.

## Representation change

The direct map repeatedly removes blocks from the **low** end of the integer, adds or subtracts powers of two, and creates bits at the **high** end. An ordinary contiguous big integer copies or shifts its remaining limbs when dropping a low block. As the counter grows, that mandatory work dominates the simulation.

[soc25_deque.cpp](soc25_deque.cpp) keeps 64-bit words in a deque with an absolute bit origin:

- Removing low bits advances the origin, discards fully consumed words, and masks one boundary word. The untouched middle is not copied.
- Adding or subtracting a power of two edits its word and propagates a carry or borrow only as far as needed.
- The auxiliary counter in `F_loop` is represented temporarily as a sum of signed powers of two with a shared shift. This avoids constructing a second huge integer.
- A read-only planning pass computes the next round and its size before changing the counter. A space limit therefore leaves the last complete round intact.
- Positive powers are applied before negative powers. On a valid nonnegative result, every intermediate subtraction is then nonnegative. The source map's truncated-subtraction behavior is retained in both independent reference implementations and compared against the native algebraic rewrite.

The new representation removes a full-counter copy from the common path. It does **not** prove constant cost for every round: a long low-block scan or carry can still touch many words, and space still grows with the counter. The measured billion-round runs scale well, but no worst-case exponential speedup is claimed.

## Independent validation and benchmark

[soc25_validate.py](soc25_validate.py) implements the source map directly with unbounded Python integers and truncated subtraction. [soc25_bigint.cpp](soc25_bigint.cpp) is a separate direct translation using Boost.Multiprecision `cpp_int`; it is both a comparison implementation and a benchmark. Neither reference uses the sliding-word arithmetic or signed-power planner.

Checks completed:

- 18,056 round cases: all valid inputs through `L=12`, plus sampled multi-round continuations through `L=19`. These include 6,033 halting cases.
- 100,000 random arithmetic operations against native unsigned 128-bit arithmetic, covering unaligned low ends, carries, borrows, and word boundaries.
- Three 10,000-round blank-orbit comparisons against Python, comparing the entire integer.
- Three 100,000-round comparisons against the compiled big-integer reference, again comparing the entire integer rather than just a hash.
- A separate complete 100,000-round comparison against Python for start 1.
- Checks that space exhaustion preserves the last completed round, and that time limits and malformed arguments are handled.
- The full native/Python validation suite passed under the undefined-behavior sanitizer.

Both C++ implementations were compiled with GCC using `-O3 -march=native -std=c++17`; the comparison used Boost 1.74 headers. Simulation times on this host:

| Start | Rounds | Direct C++ big integer | C++ deque | Ratio |
| --- | ---: | ---: | ---: | ---: |
| 1 | 100,000 | 6.799079 s | 0.014887 s | 456.70x |
| 2 | 100,000 | 6.668231 s | 0.015204 s | 438.59x |
| 3 | 100,000 | 6.292706 s | 0.015158 s | 415.14x |

These ratios compare the two implementations included here, not the unpublished implementation used by the upstream author. They are not extrapolated into a claimed billion-round reference runtime.

## Long runs

Each run below completed **1,000,000,000 reset rounds**, a thousand times the round count reported in the pinned PR, without a halt:

| Start | Final L | Final counter bits | Simulation seconds | FNV-1a-64 |
| --- | ---: | ---: | ---: | --- |
| 1 | 8,559,339,705 | 8,559,339,706 | 153.811378 | `4bfb7caece8d623f` |
| 2 | 8,558,855,765 | 8,558,855,766 | 156.501918 | `c63e0c7fa0aa2034` |
| 3 | 8,558,814,606 | 8,558,814,607 | 153.762578 | `97d15be482fbeb1f` |

Each final counter uses about one GiB of word payload. [soc25_results.json](soc25_results.json) records the exact summaries and validation measurements. The hash is computed over little-endian bytes of the logical 64-bit words, including zero padding in the last word; it is a reproducibility aid, not a cryptographic certificate. Validation above compares full integers.

The large counter states are not checked into Git. This tool currently replays from one of the three starts; it does not offer checkpoint resume. The billion-round experiments take about 2.6 minutes each on this host and are reproducible with the commands below.

## Reproduction and limitations

From the repository root:

```sh
g++ -O3 -march=native -std=c++17 -Wall -Wextra -Wconversion research/holdouts-623/soc25_deque.cpp -o /path/to/soc25_deque
# Optional independent reference; requires Boost.Multiprecision headers.
g++ -O3 -march=native -std=c++17 research/holdouts-623/soc25_bigint.cpp -o /path/to/soc25_bigint
python3 research/holdouts-623/soc25_validate.py /path/to/soc25_deque --bigint /path/to/soc25_bigint
/path/to/soc25_deque --start 1 --rounds 1000000000 --seconds 240 --max-bits 9000000000
/path/to/soc25_deque --start 2 --rounds 1000000000 --seconds 240 --max-bits 9000000000
/path/to/soc25_deque --start 3 --rounds 1000000000 --seconds 240 --max-bits 9000000000
```

The default space limit is 256 million bits, much smaller than the billion-round commands above. `--max-bits` limits the next completed counter width, not all auxiliary allocation. Time is checked between rounds at periodic intervals; a single round can overshoot the budget. `--hex` emits the complete counter and is intended for small comparison runs. The reference executable caps requests at one million rounds.

**The native executable and its signed-power rewrite are unverified.** Checking the upstream recurrence proof does not certify this implementation or its billion-round orbit. Outputs always state `"verified": false`; a native halt would require proof replay. Bounded runs without a halt do not establish nonhalting, and no raw-TM-step count is claimed.

AI-assisted implementation and testing by Codex. The return map and its halting reductions remain credited to upstream PR #40 and BusyCoq's existing model authors.
