#!/bin/sh
# Run after verify.sh in a checkout containing the compiled engine and score.
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
verify=$(CDPATH= cd -- "${1:?supply the PR 93 checkout}/verify" && pwd)
build=${2:?supply a new output directory}
mkdir -p "$build"
build=$(CDPATH= cd -- "$build" && pwd)
cd "$verify"
cp "$here/ExtractSearch.v" .
coqc -Q . BusyCoq ExtractSearch.v
cp bell429z.ml bell429z.mli "$here/search429.ml" "$build/"
cd "$build"
# BusyCoq's context includes 63-bit constants for hash tables. The search uses Zarith for tape counts.
sed -i '1i module Uint63 = struct let of_int (x:int) = x end' bell429z.ml
sed -i '1i module Uint63 : sig val of_int : int -> int end' bell429z.mli
sed -i 's/^type int (\* AXIOM TO BE REALIZED \*)/type int = Stdlib.Int.t/' bell429z.ml bell429z.mli
ocamlfind ocamlopt -O3 -package zarith -linkpkg bell429z.mli bell429z.ml search429.ml -o search429
cp "$here/frontier429.ml" .
ocamlfind ocamlopt -O3 -package zarith -linkpkg bell429z.cmx frontier429.ml -o frontier429
