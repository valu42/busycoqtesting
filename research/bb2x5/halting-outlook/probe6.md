# Line 6 — how far a local safety test can go

`1RB---3LB4RB0LA_2LB3LA3RB4RA0RA` · **Unknown** · 2026-11-18

## Blank execution and the unary test

The [inherited reduction](../line6.md) identifies the opportunity. At each new leftmost blank, A writes a waiting 1 and sends B into the remaining word. A return in A hits A1. A halt inside a subordinate probe can also propagate from a `30` prefix. A successful return in B moves the head one cell further left. Every probe terminates on a finite input. The blank machine runs forever exactly if the probe on each unary word $2^n$ returns B, for every $n\ge0$. Each success through $n$ gives the blank checkpoint at coordinate $-(n+1)$.

The [inherited ten-billion-step tape](../frontiers/runs/window-06.json) contains a written 1 at coordinate −16,299. Reaching that position for the first time completes the corresponding left extension, so unary inputs **0 through 16,298** (indexed by their length) already pass. Continuing with one literal instruction at a time, extension 16,300 occurs at 10,087,438,408 and extension **16,310 at 10,087,506,894**. Thus unary lengths through **16,309** succeed. The last ten opportunities span 68,486 raw instructions. [Complete new checkpoint](probe6-checkpoint.json)

## A seven-cell statistic loses decisive information

The 80th left extension occurs at 183,132 defined instructions. Its word has 307 cells. We kept its first 15 and last 18 cells and rearranged the interior. The resulting word preserves the multiplicities of **every** contiguous pattern of lengths 1 through 7, including those that straddle the blank exterior. It retains the protected nine-cell header, the counts of each symbol, and the original head and state. The search treated length-six factors as vertices and successive length-seven factors as edges, then reordered an Euler trail between the same endpoints. The full altered word is a fixture in the verifier.

From this altered checkpoint the machine reaches A1 after **1,085** defined instructions at coordinate +97 relative to the initial head. From the actual checkpoint the next two extensions take **10,278** instructions, and the resulting complete translated tape agrees with an uninterrupted literal run from blank. Thus this collection of local statistics cannot by itself certify a forward-closed safe set containing the real checkpoint. This comparison supplies no likelihood that the altered tape is reached. All runs for this witness are literal.

## A deterministic ceiling conditional on the first failure

Write $C_n$ for the exact defined-step cost of the single probe on $2^n$. If $n$ is the first failing length, the **blank halting time equals $C_n+n+1$**. To verify the offset, take $n\ge1$, since $n=0$ succeeds. The successful first subprobe on $2^{n-1}$ leaves residual $v$. At that point the corresponding blank checkpoint has word `32v` and time $C_{n-1}+n+1$. Both computations next call $F(v)$. If that call halts internally, the unary test adds five local steps before it. The blank machine takes one outer A0 and four steps to enter it. If it returns A, the unary rule adds nine local steps and the blank machine takes one A0 and the eight-step `32` rule. Its next instruction is undefined. In both failing cases the earlier time offset persists. On a success the blank machine additionally executes B1, giving the inherited offset $n+2$.

There is also a coarse ceiling computable before running the test. Put $L=2^n$. The inherited probe tables give

$$C_n\le 9 L(n+2L+1).$$

* A call with $m$ twos has at most $2^m$ base-case leaves. Its single-child pair rules never increase the number of twos in that child. At a `2u` split, the first call has $m-1$ twos. After a B return the second call also has $m-1$. After an A return the second word is $(32)^j0s$ and uses exactly one base-case leaf. A first-child halt needs no second call. Apply induction on the finite call tree.
* On the initial unary input at most $2L$ previously untouched cells beyond its right end are scanned. In the local traces a first visit there on B0 is a base case. A first visit there on A0 can only be the leading pass of `30` and immediately starts a base case one further to the right. Other accesses in the rules revisit cells already used by the same local trace or by a subordinate probe.
* Each nested call begins at least one cell to the right of its parent. The tree thus has at most $n+2L+1$ levels, at most $L$ nodes per level, and at most nine local defined instructions per node. The same argument includes incomplete local traces when a subordinate halt propagates.

This conditional ceiling and the exact offsets do not predict the first failing $n$. Neither the counting argument nor the finite runs above determine whether such an $n$ exists. These derivations have no formal proof-assistant verification.

## Reproduction and next step

Run `python3 research/bb2x5/halting-outlook/probe6.py` from the repository root. It regenerates the true 80th checkpoint, checks the factor multisets, replays the altered tape to its undefined instruction, compares complete control configurations and clocks, and checks the integrity and machine identity of the inherited snapshot. Add `--replay` to repeat all 87,506,894 literal steps from that snapshot and compare the complete tape, clock, head and state with the saved extension 16,310. [Verifier and altered checkpoint](probe6.py) · [Prior probe proof and tables](../line6.md)

The next proof target on this line is an invariant on the **ordered** zero-separated parts of the residual at each `30` call. Such an invariant must accept the actual extension-80 word and exclude the altered witness or track enough history to distinguish their descendants. The frequency of local patterns supplies no calibrated stopping-time estimate.
