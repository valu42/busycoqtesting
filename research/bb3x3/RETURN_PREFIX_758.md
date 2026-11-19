# Exact prefixes for the #758 crossing checker

The parity-aware checker represents each pending seed inside a direct-trace interval by one bit. Processing the least set bit gives the same ascending seed order and duplicate suppression as the ordered-set version. The checker widens certified parity classes as described in [the crossing proof](BLANK_CROSSINGS.md). On an unresolved class it needs the exact first positive return.

## Sharing exact first-return prefixes

Within a same-parity interval the first reset move and an initial run of jumps produce a fixed first counter $a$ and an increasing second counter $c$. After any further common word of jumps and bulk moves, $a$ remains nonincreasing and $c$ remains nondecreasing as functions of the initial seed. An endpoint comparison therefore proves a common ordinary branch for the whole interval. Each cached prefix stops before taking a move from an interval whose minimum $a$ is at most 1. Thus it cannot skip an earlier visit to $a=1$.

Suppose the prefix has $b$ bulk moves. Translating the seed by $2^{b+1}$ preserves the second-counter residue modulo four at every bulk move. Initially the translation in $(a,c)$ is $(0,2^{b+1})$. A jump sends a translation $(A,C)$ to $(3A,C-A)$. A bulk move sends it to $(A-C,3C/2)$ and consumes one bit of divisibility. A table stores one exact output for each seed residue of the chosen parity. A translated output follows by adding the computed translation. At a return the output seed shifts by precisely the original period, since every translation preserves $A+2C$.

In smaller aligned intervals the checker groups further common runs. For a bulk move put $x=\lfloor(c+1)/4\rfloor+3$. Then $x'=\lfloor3x/2\rfloor$, the decrement of $a$ is $4x-9$, and the new $c$ is $6x-13$. Over $n$ bulk moves the total decrement is

$$
8(x_n-x_0)-9n+4\,\#\{i:0\le i<n,\;x_i\text{ is odd}\}.
$$

Increasing $x_0$ by $2^n$ increases $x_n$ by $3^n$ and preserves all the counted parities. This gives a table for runs of up to seven bulk moves. A jump run uses the original power-of-three formula. Ambiguous or exceptional branches at the end of a cached prefix use the scalar rules. A rare long tail is replayed with the reference checker's original 5,000-call budget.

## Reproduction

Use a C++17 compiler supporting the GCC/Clang trailing-zero builtin. Run these commands in the directory containing the counter sources.

~~~sh
c++ -O3 -std=c++17 cross_758_fast.cpp -o /tmp/cross_758_fast
/tmp/cross_758_fast 2044855966425482 2045355966425482
python3 audit_return_prefix.py
~~~

The benchmark shard prints the following six fields, matching the ordered-set parity checker.

~~~text
2044855966425482 2045355966425482 2045355966425482 2045355966425602 12766 43135720
~~~

The audit compares 65,294 seed/range cases, including 50 halting cases, against unbatched Python counter steps.
