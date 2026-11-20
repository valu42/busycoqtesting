# Mixed ordinary ancestors and the limits of forward closure

A state has the same future as any of its physical predecessors after
their paths merge. Consequently, an accepted state from the
[extended entry test](entry_transport_758.md) can certify a much larger
primitive left coordinate among its descendants. The predecessor need
not be the one actually followed from blank.

The [checker](inverse_entry_758.py) implements the restricted but exact
test `find_entry_ancestor(h, u)`: it searches for an accepted source whose
forward word is $J^j$, or $J^jLLJ^i$. A successful result includes the
source and the physical word. An unsuccessful result is inconclusive.
This is a certificate for a supplied state, not a proof that blank
reaches such a state.

## Exact mixed inverse

At odd/odd boundaries write $h=(a+1)/2$ and $u=(a+2c-1)/2$.
A jump predecessor is $(h/3,u-2)$ when $3\mid h$ and the result is
physical. Its forward guard is automatic from $h\le u$.

For a pair $P=LL$, put $z=4h+5u$. Its possible predecessors are

| Condition | Earlier $h$ | Earlier $u$ |
|---|---|---|
| $z\equiv5\pmod9$ | $(z-5)/9$ | $u-5$ or $u-7$ |
| $z\equiv2\pmod9$ | $(z-11)/9$ | $u-7$ or $u-9$ |

Keep only positive odd/odd states executing both ordinary bulk guards.
The formulas follow from the four paired updates
$4h'=9h-5u-e$, with $(v,e)=(5,20),(9,34),(7,24),(7,30)$ and
$u'=u+v$. The two alternatives within a row are the
[coalescing siblings](COARSE_RECONSTRUCTION_758.md); this does not make
the entire inverse forest unique when different past words are allowed.

For example, start with $h=2$ and let $u$ be the first even integer at
least $H-F$, plus 1000. After 291 jumps and one pair, the resulting $h$
is an odd, three-free **139-digit integer**, beyond both existing
primitive-coordinate cutoffs. The mixed inverse recovers an accepted
source and certifies halting. Direct replay confirms its subsequent
return into the basin. This is an arbitrary-state example, not a blank
crossing witness.

## A bound on what forward closure alone can cover

Let $E$ be the accepted scale-20 extended entry set and let $B$ be all basin reset
states $A(1,s)$ with $H-F\le s\le H-L$. Consider the union of all
**forward descendants** of $E\cup B$, at a fixed odd/odd mass coordinate
$u\ge H-F$.

Every source in $E$ first returns to $B$ within 553 calls, with mass
coordinate gain at most 2488. Before that first reset, a descendant at
the chosen slice must come from an even source mass in $[u-2488,u]$.
There are at most 1245 such masses, and at most $h_{\max}/2$ source
left coordinates at each. Mass strictly increases, so each source
visits the chosen slice at most once. After its first reset, its path is
already among the descendants of $B$. Those add at most $F-L+1$ states
at the slice, again by strict mass increase.

Thus the entire forward closure has at most

$$
1245\frac{h_{\max}}2+(F-L+1)
=43,246,096,003,749,008,708,341,883,613,946,558,761
$$

states there. An odd/odd slice has $\lfloor(u+1)/2\rfloor$ physical
states. The displayed cap is less than $5\times10^{-102}$ of that
number throughout the indicated range.

This rules out complete slice coverage by this particular forward
closure, at any search depth. It says nothing about a distribution for
the blank trajectory. It also does **not** bound backward preimages of
the entry set, or the much larger set already certified by short
physical returns in [the cut analysis](CUT_DENSITY_758.md).

There is a second limitation for ordinary inverse searches: if a known
entry reaches its first reset within 553 calls, a descendant before
that reset has its own first reset within 553 minus the intervening
calls. Therefore these witnesses cannot settle a target already known
to survive its next 553 calls without a reset. A useful further
saturation argument would need a stronger future certificate or a
connection through already settled basin resets.

## Reproduction

```sh
python3 inverse_entry_758.py
```

The checker compares the simplified pair inverse with the existing
elementary-word inverse at every odd/odd state of mass coordinate below
100, replays the mixed-ancestor example and its return, and checks the
exact slice cap. It reuses the verified entry theorem as a dependency;
it does not repeat its guard or lattice exhaustions.
