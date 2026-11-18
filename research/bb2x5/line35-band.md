# Testing two line 35 sweeps from one prefix

**Line 35 remains open.** On the actual blank tape, a sufficient test for two consecutive sweeps holds at every odd epoch from **26,351 through 300,001**. The test reads a short left prefix at the odd epoch and uses the length of the synchronized right suffix. At epoch 300,001 the prefix occupies 51,578 of the 610,114 cells (8.45%). An induction preserving the test on the blank orbit would establish non-halting. A concrete altered tape passes it and fails it two sweeps later, which identifies a missing reachability condition. [Executable checker](line35_band.py) · [Full checkpoint](frontiers/runs/line35-band.json)

## A certificate for two sweeps

Use physical digits $O=1$, $C=2$, $N=3$. Write $b(P)=\#O-\#C$ and let $d(P)$ be the greatest excess of closings over openings in any prefix, including the empty prefix. At an odd epoch let $k\ge1$ triples at the right end have the shape $OaO$, immediately to the left of the terminal $OC$. Their $c=2+3k$ cells send zero debt leftward now and at most one on the next sweep. They remain covered after a pair of successful sweeps. Let $m=n-c$ be the uncovered width. [Right-suffix theorem](line35-pascal.md)

For the recorded test take $x=\lceil m/5\rceil\ge20$ and $P=W[0,x)$. The [five-sweep interval bound](https://github.com/valu42/busycoqtesting/blob/1a47b45f468aa296f57255a7a127ce137464c69d/research/bb2x5/line35-middle.md) bounds the debt from the rest of the tape by $B=\lfloor(m-x+25)/8\rfloor$. Its hypotheses hold at epochs at least five. At most four header cells per sweep can lack ordinary ancestry on the left, and the synchronized suffix has at least five cells on the right.

The first two requirements are
$$
 H=d(P)\le5,\qquad b(P)+H\ge B.
$$
For every actual exterior debt $e\le B$, the resulting guard debt is $\max(H,e-b(P))=H$. Thus the sweep succeeds, and its header of length $h$ and virtual left survivor bit are known. Match $P$ with **zero** exterior debt and compute its next header and $x$ ordinary output cells. Call those $h+x$ digits $V$. Set $m'=m+h+1$, $y=\lceil m'/5\rceil$, and $Q=V[0,y)$. Here $20\le y\le h+x$.

The second pair of requirements is
$$
 d(Q)\le5,\qquad b(Q)+3\ \ge\ \left\lfloor(m'-y+25)/8\right\rfloor .
$$

To prove sufficiency, a nonzero exterior debt erases the rightmost $e$ surviving openings of $P$. The source bits before the first erased survivor agree with the zero-debt calculation. From that survivor onward they are zero. Writing the ordinary digit $D(l,r)$ for adjacent bits, the erased part therefore emits at most one neutral followed by openings. The true successor prefix has no larger deficit than $Q$. Its balance is at least $b(Q)-1$. Indeed, if $r$ counts rises, $v$ is the virtual starting bit and $s$ the last bit, the balance of $i$ ordinary outputs is $i-3r-v+s$. Erasure cannot create a rise and can lower the final bit by at most one. The five-sweep bound applied past $y$ gives at most $\lfloor(m'-y+25)/8\rfloor$ debt before including the right suffix, which contributes at most one. The second pair of inequalities leaves the full guard debt at most five. Both positive finite sweeps therefore succeed. This proof uses no observed periodicity of the guard. [Exact guard and sweep rules](line35-guard-stream.md)

## Exact blank replay

The independent implementation stores the uncovered cells explicitly and advances the covered centers with the Pascal rule. It detects new triples at every odd boundary. The first 26,350 epochs are covered by direct sweep replay. From odd epoch 26,351 onward the smallest margins in the two balance inequalities were both **20**, first at epochs 28,739 and 34,063 respectively. The two tested prefix deficits were at most three. At epoch 300,001 the observations were $H=1$, first margin 2,173, $d(Q)=0$, second margin 2,343. There were 117,408 covered triples and 257,888 uncovered cells. The machine was in A at head $-310114$ after **293,713,845,976 defined instructions**. A separate full-word replay agreed on the complete checkpoint, including tape, state, head and clock. [Earlier full-word implementation](https://github.com/valu42/busycoqtesting/blob/1a47b45f468aa296f57255a7a127ce137464c69d/research/bb2x5/line35_timed.py)

For the clock, each cell contributes its outgoing matching debt minus its survivor bit to the full-word quantity $A-s$ in the [timed sweep formula](https://github.com/valu42/busycoqtesting/blob/1a47b45f468aa296f57255a7a127ce137464c69d/research/bb2x5/line35-timed.md#counting-the-literal-moves). The cap $OC$ contributes one on both sweeps. If $o$ centers are openings and $z$ neutral, the full synchronized suffix contributes $1-3o-2z$ on the odd sweep. On the intermediate sweep it contributes $2+k-4o+z-[a_{k-1}\ne O]$. For each intermediate triple the contribution for center $C,O,N$ is respectively $0,-3,1$, with one extra when the previous center differs from $O$. The virtual previous center is $C$. The checker compares both phases with literal TM execution, including failing inputs.

## Why the numerical test needs a reachability argument

Consider the [altered tape that eventually reaches B4](https://github.com/valu42/busycoqtesting/blob/1a47b45f468aa296f57255a7a127ce137464c69d/research/bb2x5/line35-timed.md#an-altered-tape-shadows-almost-ten-guard-periods). At its epoch 655, after 255 successful sweeps from the planted state, the first and second balance margins are **2,982 and 2,175**. The two prefix deficits are zero and one. At epoch 657 the first margin is **−15**. The altered machine later reaches B4 at epoch 1288. This is a failure of the proposed induction step on a tape with genuine sweep ancestry. [Independent paired replay](line35_band_control.py)

The same example can have an arbitrarily large synchronized fraction of the tape. At odd epoch 401 insert $K$ clean triples immediately before the original cap $OC$. Give the outermost inserted triple center $C$ and all its inner neighbors center $O$. For the first $K$ paired samples the outermost center remains $C$. In the augmented Pascal register with initial polynomial $1+X^K$, the top bit at paired time $t<K$ is $1+\binom{t}{K}=1$. After the initial $C$, each subsequent $1\to1$ step also gives $C$. This center presents zero debt and survivor zero on both sweeps, exactly as the original cap does. In fixed right-index coordinates every cell of the old strip above the insertion follows its original recurrence for those pairs. Its uncovered width, prefix tests and guards agree. Taking $K$ arbitrarily large retains the failure and the subsequent halt. The checker also replays $K=1024$. This leaves the way the *blank* machine generates its uncovered material as the essential open question.

From this directory, run

```sh
python3 line35_band.py --epochs 300001 --output /tmp/line35-band.json
cmp /tmp/line35-band.json frontiers/runs/line35-band.json
python3 line35_band_control.py
python3 line35_pressure.py frontiers/runs/line35-band.json
```

[All-future pressure at a fixed synchronized cut](line35-pressure.md)
