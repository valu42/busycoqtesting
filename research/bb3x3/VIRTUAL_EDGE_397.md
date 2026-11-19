# An integer halting guard for #397

For a finite tail \(w\) at the [blank-connected 29-bit cut](TRANSITIVE_SECTION_397.md), let \(k=|w|\), \(B=2^k\), and let \(z\) be its little-endian binary value. Put

$$N=15z-7B.$$

**If \(N>0\), every one of the six input carries survives this application.** Every successful growth restores a strictly positive \(N\). Hence a sufficient condition for #397 to run forever is that the scalar stays positive between successive growths on the exact 33-carry input from blank. The first carry at this cut acts on the empty tail and creates `01`, giving \((N,B)=(2,4)\). A final bit of one implies \(N\ge B/2\). The sign test also protects some words ending in zero.

## Sharp sign bound

Read the word from its most significant bit for the numeric comparison. The empty word has ratio zero, and every nonempty halting word starts in this order with zero. Among those sharing the maximal first four bits `0111`, delete these four bits. Reading the suffix `1110` in the original head-facing order takes exactly the modes `c,e` to `c,e`; every other mode survives the bare edge after those four bits. Consequently the shorter word still halts under the same incoming carry. Repeating shows the binary fraction \(z/B\) is strictly below \(0.\overline{0111}_2=7/15\). A shorter word matching the extremal prefix has an all-zero fractional continuation. The bound is sharp: the head-facing words consisting of `0` followed by `1110` repeated \(j\ge0\) times all halt on `a` and give \(N=-14\), so their ratios tend to \(7/15\).

## Exact scalar update

Complete the word with the infinite tail \(T=(1110)^\omega=-7/15\) in the 2-adic integers. The completed word represents \(N/15\). Apply the chosen carry to that infinite word and call the resulting numerator \(I\). The [checker](virtual_edge_397.py) evaluates this directly from \(N\) and the input mode. Consume the low bit \(b=N\bmod2\), use the table to obtain its replacement and outgoing mode, and recurse on \((N-15b)/2\). The four rotations of \(T\) give the four terminal integer numerators \(-7,-11,-13,-14\). Their images follow by running the table on the periodic digits to the first repeated carry at a block boundary. Absolute values decrease outside \([-15,15]\), and admitted positive values in that interval are the powers of two \(1,2,4,8\), which descend into the terminal set. Silence copies the remaining integer.

If a carry reaches the physical edge, the image has the form \(I=15z'+cB\) for the output bits \(0\le z'<B\) on the existing cells. The table gives \(c\) and the corresponding continuing physical tail value \(N'=15z'+c'B\). For an internal stop use \(c=c'=-7\).

| Edge carry | Virtual coefficient \(c\) | Physical coefficient \(c'\) | Next width factor \(B'/B\) |
|---|---:|---:|---:|
| `a` | −52 | 1 | 2 |
| `b` | −22 | 2 | 4 |
| `c` | −14 | halt | — |
| `d` | 53 | 4 | 8 |
| `e` | 1 | halt | — |
| `f` | −97 | 23 | 16 |

Only `c,e` change the residue of the numerator modulo 15, since \(2^k\) is invertible there. **The physical update halts exactly when \(I\not\equiv N\pmod{15}\).** Otherwise the intervals \([cB,(c+15)B)\) for the four live carries and the internal stop are disjoint, so \((I,B)\) determines the continuing update. All four physical growth coefficients are positive. This gives a two-integer formulation with a one-integer halting test at each call. Infinitely many successful updates on this specific blank input remain to be established.

## Two exact staggered registers still leave ambiguity

The [binary register](FIRST_CONTACT_397.md) can be taken at both pair alignments. At sweep 26,688, after 26 full periods at the 29-bit cut, the real tail is the first word below. The second word would halt on the eighth carry of its 45th period from that point.

```
101101011100010010000010001001100001
100101011100000011010010001001100001
```

Both words have length 36, 22 zero bits and the same final 16 bits. Both registers select nine digits in each word, giving 209 in the first alignment and 70 in the second. The two words even have the same occurrence counts for every contiguous substring of lengths one, two and three. The second word has a scalar numerator **9,707,460 larger** than the actual one. An inductive safety criterion retaining these data and the exact pass number must admit the second word if it accepts the first and imposes only a lower bound on the scalar.

Run `python3 virtual_edge_397.py` to check the periodic coefficients, compare all six scalar updates with the original table on every word through length 11, and reproduce the two matched-register trajectories.
