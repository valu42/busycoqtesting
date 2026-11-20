# A reusable power crossing through a change of active parity

**Uniform family extension.** The [new algebraic passage theorem](UNIFORM_PARITY_PASSAGE_758.md) proves explicit nonempty phase bands through this change for every $m\ge20$, including an unbounded family of mixed words and the full subsequent even corridor. Its separate incoming-phase corollary applies for every $m\ge2200$, and complementary phases remain open. The theorem below still supplies the stronger all-phase coverage on its finite exponent range; the new lemma does not replace that finite handoff.

Put $P=3^m$ and $A=\lfloor24P/23\rfloor$. For every $20\le m\le292$, every reset $A(1,s)$ with $A\le s\le A+100,000$ travels to the upper boundary near $54P/49$, a distance of approximately $5.856\%$ of $P$. The incoming phase uses an odd preserving word, and the outgoing phase uses an even preserving word. The transfer includes the cusp where the odd word loses its guard. Across all 273 exponents, the finite checks at that change of phase require **86,975 distinct first-return evaluations**, at most 556 per exponent. The two macroscopic intervals on either side are proved with endpoint checks.

From the particular input $s=\lfloor24P/23\rfloor$, adding the exact quadratic clocks on the two preserving words and evaluating the finite transitions at their boundaries gives $32,409,772,864,627$ first returns and $325,476,182,146,575,128,087,429,192,156,433,319,319,602,524,249$ raw transitions at $m=35$. At $m=292$ the corresponding flight spans $2.02531997\times10^{135}$ first returns and $3.53381008\times10^{414}$ transitions, rounded. The [residue-cycle method](TARGET_CLOCK_758.md) evaluates both long sections without iterating over the return count.

At $m=35$ the blank trajectory reaches this entrance because the [published forward crossing](POWER35_PARITY_BRIDGES_758.md) traverses this part of the annulus with individual seed gains below 100,000. All possible even exits at the second boundary merge at the exact blank reset **55,136,804,803,035,090**. At $m=292$ the entry is conditional, and this particular corridor lies above the proposed halting target $H$. The [continuum parity criterion](CONTINUUM_PARITY_758.md) predicts the parity handoff from the two normalized angular gap endpoints.

## Exact finite passage

Let
$$
 C=\lfloor2187P/2059\rfloor-2m-500,\qquad
 E=\lfloor54P/49\rfloor-2m-504.
$$
Across the entire entrance window an even seed executes $I J^{m-1} L^2 J L^2 J^3 L R$ and returns odd. Every odd seed from $A$ through $C-1$ takes $J^m L^7 R$ and remains odd. Thus any incoming seed reaches an odd reset in $[C,C+2m+40]$. The first return crossing $C$ gains at most $2m+40$, by the individual mass charges of the fixed word.

On the entire span from $C$ through $E-1$ the even word is $I J^{m-1}L^2 J L R$ and its output stays even. For each possible odd exit just above $C$, the checker follows ordinary first returns up to the first even seed, merging coincident paths. Every one of these first even seeds is at most $C+25,222$ across the 273 tested powers, and is below $E$. That even seed follows the preserving word until the first reset at or above $E$, which is even and at most $E+2m+40$. The checker verifies all word guards at the two endpoints of each parity interval, including the absence of any intermediate reset. The [ordered endpoint theorem](CONFLUENCE.md) interpolates between them. Positive seed gains carry every input across each finite interval.

The [receipt table](power_parity_transport_758.tsv) has one line per exponent, with the number of distinct calls at the parity switch, the largest examined switch offset above $C$, the common final reset as an offset above $E$, and the number of edges in the final merger. The final merger starts with *all* even seeds in the output enclosure. Some may exceed the exact set of attainable exits.

Run the [checker](power_parity_transport_758.py) with Python 3.10 or later.

```sh
python3 power_parity_transport_758.py 35 292 --clock
python3 power_parity_transport_758.py --all --merge > /tmp/power_parity_transport_758.tsv
cmp /tmp/power_parity_transport_758.tsv power_parity_transport_758.tsv
```
