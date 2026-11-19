#!/bin/sh
# sh replay_line448.sh BUSYCOQ_CHECKOUT H155900.v BUILD_DIRECTORY [witness]
set -eu
test "$#" -eq 3 || { test "$#" -eq 4 && test "$4" = witness; } || {
  echo "usage: sh $0 BUSYCOQ_CHECKOUT H155900.v BUILD_DIRECTORY [witness]" >&2
  exit 2
}
source_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
busycoq=$(CDPATH='' cd -- "$1" && pwd)
proof_file=$2
mkdir -p -- "$3/BusyCoq"
build_dir=$(CDPATH='' cd -- "$3" && pwd)
base=33209bc7dc282b38c8cd6be507bfc551fea56108
for module in LibTactics Helper Eqb HashTable TM Compute Flip Permute Pigeonhole Enumerate Individual BB62 Individual62; do
  git -C "$busycoq" show "$base:verify/$module.v" > "$build_dir/BusyCoq/$module.v"
done

python3 - "$proof_file" "$build_dir/BusyCoq/Line448Engine.v" <<'PY'
import hashlib
from pathlib import Path
import sys

source = Path(sys.argv[1]).read_bytes()
expected = "ccec2379e65fb6c584879b0270da5a2eac3fc091e9bf2d112a6654b498fa37a6"
if hashlib.sha256(source).hexdigest() != expected:
    raise SystemExit("H155900.v differs from the pinned proof")
prefix, marker, _ = source.partition(b"Definition initFastB :")
if not marker or b"Lemma run_pow_spec " not in prefix:
    raise SystemExit("cannot identify the shared engine and its soundness theorem")
Path(sys.argv[2]).write_bytes(prefix + b"End H155900.\n")
PY

cp "$source_dir"/Line448Sweeps.v "$source_dir"/Line448Halt.v "$build_dir/"
cd "$build_dir"
for module in LibTactics Helper Eqb HashTable TM Compute Flip Permute Pigeonhole Enumerate Individual BB62 Individual62 Line448Engine; do
  coqc -q -Q BusyCoq BusyCoq "BusyCoq/$module.v"
done
coqc -q -Q BusyCoq BusyCoq Line448Sweeps.v
if [ "${4:-}" = witness ]; then
  cp "$source_dir"/Line448Witness.v "$source_dir"/line448_witness.ml .
  coqc -q -Q BusyCoq BusyCoq Line448Witness.v
  ocamlfind ocamlopt -O3 -thread -rectypes -package zarith,coq-core.kernel -linkpkg \
    engine448.mli engine448.ml line448_witness.ml -o witness448
  ./witness448
else
  coqc -q -Q BusyCoq BusyCoq Line448Halt.v
  coqchk -silent -bytecode-compiler yes -Q BusyCoq BusyCoq Line448Halt
fi
