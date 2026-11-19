# Recognizing a genuine scale-74 reset at the midpoint

Put $G=10^{10}3^{74}$, $T=H-5G/4$ and $M=2T+1$. An infinite blank trajectory would have a first state with mass $W\ge M$. **There is an explicit set of 701 possible states whose membership at that crossing is equivalent to having visited a scale-74 reset with parameter between $H-3G/2$ and $T+4$ by that time.** Every such visit leads to the known singleton exit $A(1,H-G+698)$. Which state the blank trajectory reaches, and whether this singleton eventually halts, remain open. [Scale corridors and exit cycles](SCALED_GATES_758.md)

## All local crossing states and their reset ancestors

Every reset from $H-3G/2$ up to $T$ has a positive first return that advances the seed by at most 1,184. Hence any orbit with such a reset strictly before the midpoint's mass crossing has its last preceding reset among $T-1184,\ldots,T-1$. Tracing these seeds using the original map gives 815 that reach $M$ before an earlier reset, producing exactly 700 distinct first crossing states. Two of these are $A(1,T)$ and $A(1,T+2)$.

For each of the 698 nonreset states the [complete predecessor search](TERMINALS_758.md) exhausts. Across these searches it examines 750,444 states, counted with multiplicity, and none extends beyond 507 reverse calls. Every possible last reset has its parameter between $T-1018$ and $T-1$. Thus on an actual blank crossing at one of these states, a recent scale-74 reset is compulsory even if its path before the crossing was unknown.

It remains possible for the first visit to the gate to be a reset at the crossing itself. A crossing has $M\le W\le M+8$, leaving five nominal reset parameters from $T$ through $T+4$. Since $T=1\bmod6$, the target $T+3$ is even and could only come from the usual reset rule. That rule raises mass by five and could not first cross from below $M$ to $M+6$. For $T+4$ only the nine-unit bulk rule can first cross. Its only possible parent has mass $M-1$ and its entire inverse search exhausts after three states without a reset. Blank visited $A(1,3)$ long before this mass, ruling out that parent. Adding $A(1,T+1)$ to the 700 states therefore gives the claimed criterion. The criterion does not assert that each listed state is reachable from blank.

## Crossing after a deep entry

If a prior reset has distance $D$ from $H$ satisfying $5G/4+39{,}004{,}000\le D\le3G/2$, the scale's residue cycle has already captured the trajectory before distance $5G/4+4{,}000$. Its unique exit there is seed $T-3{,}142$. Following exact returns to the midpoint gives a unique first crossing state of mass **exactly** $M$,

$$
A(2\cdot3^{36}-1,\ T-3^{36}+1).
$$

Its complete inverse search has the single possible last reset $A(1,T-72)$, exactly 36 odd/odd jumps earlier. These results characterize the cut under genuine reset conditioning, leaving open an excursion that traverses the gate without any reset.

Run the [checker](scale74_ancestry.py) alongside the existing counter, scale and inverse modules.

~~~sh
python3 scale74_ancestry.py
~~~
