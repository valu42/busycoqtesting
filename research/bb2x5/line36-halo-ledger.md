# Exact ledger for the three-cell line-36 halo

Let $x$ be the old protected cut, $y=x+3$, and $T$ the old suffix starting at $y$. Let $h$ be the number of new header cells, $S$ the known new word through output position $y+h-1$, and $z\le |S|-3$ the next protected cut. No assumption on the colors of old or new closings in the known part is needed. Use the coordinate of the last closing strictly before each cut as its sentinel. The total budget $B$ counts parity changes from that sentinel, through all subsequent closing positions, to the actual last coordinate of the word.

Let $K$ count parity changes from the old cut sentinel through the closings in $[x,y)$, and let $\alpha$ be their final parity, retaining the sentinel if the list is empty. The budget in $T$ is $A=B-K$. For the new known portion, form the list consisting of the new cut sentinel and the closing positions in $S[z:]$. **Normalize each new coordinate $j$ to $j-h+1\bmod 2$**. Write $K'$ for its changes and $\gamma$ for its last label. The normalization preserves changes and applies to the terminal sentinel as well.

Write $s$ for the old survivor bit at $y-1$, $q$ for the bit at $y$, $d$ for the outgoing debt of $T$, and $\epsilon$ for its last survivor bit. In particular $s=[\text{old cell }y-1\text{ is }1][d=0]$. The derivative at $y+h$ is a closing precisely if $s\ne q$. Append its normalized label $m=y+1\bmod 2$ to the known list exactly in that case. Let $k$ count changes **starting from $\gamma$** when doing this, and let $g$ be the resulting last label. This crossing digit is the first output digit beyond $S$.

Let $c$ be the cancellation certified by the cap in $T$. Put $e=[\alpha\ne y-1\bmod 2]$, and form $W=1^eT$ by adding at most one formal opening. Its standard left sentinel has parity $\alpha$, so $M(W)=A$. The cap is unchanged. If $f(W)$ is the number of odd-length runs of surviving openers, optimal dimer charging gives $f(W)+d(W)\le A-c$. This includes a cap whose matched substring extends to the left edge of $T$. The proof only requires that the cap cells lie in $T$.

## First surviving opener preceded by a nonsurvivor

Here $q=0$. The verified cap has a survivor, so the initial zero-run $E$ has positive finite length. Its length is congruent to $d$ modulo two, by matching. All later zero-runs have even length. The first survivor produces a closing at new left-origin coordinate $y+h+|E|$, normalized to $\beta=y+d+1\bmod 2$. It is strictly after the crossing digit already considered.

Starting at that closing, the rest of the output contributes exactly $f(T)+(1-\epsilon)$ changes, including the terminal marker. An intervening even zero-run adds zero. The boundaries of a one-run of length $L$ differ in parity exactly when $L$ is odd. A terminal one-run ends at an appended closing, followed by the same terminal label. A terminal zero-run is even and its last real derivative closing has parity opposite to the terminal coordinate.

If $d>0$, every added opening is matched, so $d(W)=d-e$ and $f(W)=f(T)$. If $d=0$, a formal opening is a separate singleton run immediately before $E$, so $f(W)=f(T)+e$. Thus $f(T)\le A-c-\ell$, where
$$
 \ell=\begin{cases}d-e& d>0,\\ e& d=0.\end{cases}
$$
The code starts with $\max(0,d-e)$ and raises it by one if its parity differs from $[\alpha\ne\beta]$. This gives exactly $\ell$, since $[\alpha\ne\beta]=e\mathbin{\mathrm{xor}}(d\bmod 2)$. The signed edge charge in this case is
$$
 C_0=K'-K+k+[g\ne\beta]-\ell .
$$

## First old cell survives

Here $q=1$ and $d=0$. Let $p$ be the parity of the first surviving run's length. Its right boundary is an output closing whose normalized label is $b=y+p+1\bmod 2$, including an append if the run reaches the end. The suffix after that closing contributes $f(T)-p+(1-\epsilon)$ changes. If $e=0$, the cap inequality gives $f(T)-p\le A-c-p$. If $e=1$, the formal opening extends the first run and flips its parity, so $f(W)=f(T)+1-2p$, and $f(T)-p\le A-c-1+p$.

For $e=0$, maximize $[g\ne b]-p$ over $p$. Its maximum is $[g\ne y+1\bmod 2]$. For $e=1$, maximize $[g\ne b]-1+p$, whose maximum is $[g\ne y\bmod 2]$. In each case the maximum is $[g\ne\alpha]$. The signed edge charge is therefore
$$
 C_1=K'-K+k+[g\ne\alpha].
$$
This case does not occur at positive $d$.

## One-sweep conclusion

For whichever case actually holds,
$$
 B'\le B+C_q+(1-\epsilon)-c.
$$
When $q$ is unknown and $d=0$, use $\max(C_0,C_1)$. The input closing colors in the three known cells are thus subtracted once as $K$. The new derivative at $y+h$ is counted once exactly when it is a closing. Any possible interface retreat or advance is already accounted for by $S[z:]$ in $K'$.

Under $z\le |S|-3=y+h-3$ the uncontrolled suffix **after the next halo** has length at least the old length plus $\epsilon$, since the full word grows by $h+\epsilon$. Once the entire right cap is beyond the three-cell halo, this remains true at later sweeps for these cut choices.

The implementation may generate the known word with an artificial prefix before its retained pieces. A common translation of every label reverses either all parities or none, so the costs above are translation invariant. Correctness of the finite history used to compute $S,z$, and preservation of a safe left header are separate ingredients.
