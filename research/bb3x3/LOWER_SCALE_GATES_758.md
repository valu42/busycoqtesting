# Four more halting intervals below the large target

Let $H=(3^{307}-8\,282\,708\,212)/13\,959\,275$. Every reset $A(1,H-d)$ in each row halts, including the endpoints. The last column is a sufficient condition on the blank orbit at the first crossing of $a+2c>2(H-d_{\rm near})+1$ for that row. Blank entry remains open. [Original gateway argument](GATEWAYS_758.md) · [Scaled words](SCALED_GATES_758.md)

| Scale | Near distance | Far distance | Consecutive halting resets | Transfer segments | Sufficient recent reset, in counter calls |
|---:|---:|---:|---:|---:|---:|
| 7 | 20,120,357,570,016 | 33,533,929,283,358 | 13,413,571,713,343 | 90 | 2,980,793,714,076 |
| 8 | 60,361,072,710,048 | 100,601,787,850,074 | 40,240,715,140,027 | 135 | 8,942,381,142,228 |
| 9 | 181,083,218,130,136 | 301,805,363,550,222 | 120,722,145,420,087 | 81 | 26,827,143,426,686 |
| 10 | 543,249,654,390,404 | 905,416,090,650,670 | 362,166,436,260,267 | 121 | 80,481,430,280,059 |

For each row, both odd-seed endpoints follow $J^{292} L^8 J L^6 J^{264-n} L R$. Both even-seed endpoints follow the even word of the preceding gateway proof. Intermediate seeds of the same parity have ordered counters along this common word, so their guards hold too. Every first return increases the parameter by at most 1,184. Each reset in the row therefore exits through its near edge within the 5,001-seed strip admitted by the first transfer.

Each of the 427 transfers certifies that every admitted seed halts or enters the outgoing strip of the following transfer. The last strip reaches the preceding row's halting corridor or its certified outgoing strip. Induction from the known scale-6 corridor proves all four rows. These transfers follow the possible entrances to each gap. A proof about every start within a gap requires its own verification. If the orbit avoids a row of width $w$, its mass must rise by at least $2w+1$ from its last reset before the stated upper crossing. Each continuing call adds at most nine to the mass, which gives the bound $\lfloor2w/9\rfloor$ in the table.

The [receipt table](lower_scale_bridges_758.tsv) records scale, far and near cut, visited nodes, directly evaluated returns, terminal branches, surviving exit count, maximum gain bound and the two exit bounds. Each of the four scales was also compared against the independent GMP reference implementation on three shorter intervals. The reference replay recomputes arbitrary rows or the entire grid. It requires a C++17 compiler, a 64-bit LP64 system and GMP.

```sh
c++ -O3 -std=c++17 gateway_758.cpp -lgmpxx -lgmp -o gateway_758
python3 lower_scale_gates_758.py --endpoints
python3 lower_scale_gates_758.py --row 1
python3 lower_scale_gates_758.py --jobs 4
```

## Every reset in the gap at scale 7

The 36 adjacent bands from distance 11,177,976,427,786 through 20,120,357,570,016 were also checked for **every** starting reset. They required 7,768,635,728 bisection nodes and 3,884,317,882 accepted leaves. The even-seed return and the same-parity endpoint tests bound each continuing return so that it decreases the distance and stays at or above 3,403,055. Induction on distance joins the old contiguous basin to the full scale-7 corridor. The [36-row manifest](universal_gap7_758.tsv) records inclusive band limits and exact counts. [Universal proof method and base interval](UNIVERSAL_758.md)

**All 33,533,925,880,304 consecutive reset seeds from $H-33{,}533{,}929{,}283{,}358$ through $H-3{,}403{,}055$ halt.** At the first mass crossing above $2(H-3{,}403{,}055)+1$, a reset within the preceding 7,451,983,528,956 counter updates would suffice. The wider scale-10 interval in the table has its own mass crossing. No blank entry has been proved at either.

The full run used a bounded-integer matcher with exact fallback at ambiguous endpoints. An arbitrary-precision reference rebuilds the same manifest. Row 6 illustrates a single-word band. Omitting the row selection replays all 36 bands.

```sh
python3 lower_scale_gates_758.py --universal --row 6
python3 lower_scale_gates_758.py --universal --jobs 4
```
