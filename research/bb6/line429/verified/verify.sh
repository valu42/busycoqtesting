#!/bin/sh
# Use dedicated BusyCoq checkouts at the revisions listed in README.md.
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
repo93=$(CDPATH= cd -- "${1:?supply the BusyCoq PR 93 checkout}" && pwd)
repo82=$(CDPATH= cd -- "${2:?supply the BusyCoq PR 82 checkout}" && pwd)
cd "$repo93/verify"
make Makefile.coq
make -j4 -f Makefile.coq Individual62.vo
python3 "$here/make_engine.py" M_1RB1RD_1LC0RE_1LD1LC_1RA0LB_0RD0RF_0RDHHH.v Line429Engine.v
coqc -Q . BusyCoq Line429Engine.v
for unit in Line429Score Line429Sibling Line429Cut Line429Frontier Line429Progress Bound20; do
  cp "$here/$unit.v" .
  coqc -Q . BusyCoq "$unit.v"
done
cd "$repo82/verify"
make Makefile.coq
make -j4 -f Makefile.coq Individual62.vo ES_v2.vo Longitudinal.vo
coqc -Q . BusyCoq M_1RB0LC_1RC1RA_1LD0RE_1LA1LD_0RA1RF_0LCHHH.v
for unit in Line429Sibling Line429Milestone; do
  cp "$here/$unit.v" .
  coqc -Q . BusyCoq "$unit.v"
done
