#!/usr/bin/env bash
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
explorer=$(cd "${1:?Pass the pinned busy-beaver-explorer checkout}" && pwd)
machine=1RB0LA_1RC---_0LD1RD_0RA0RE_0RF1RC_1LF0LA
upstream="$explorer/holdouts/$machine/lean"
lean=$(command -v "${LEAN:-lean}")
export LEAN="$lean"
export LEANLIB=${LEANLIB:-$("$lean" --print-prefix)/lib/lean}

"$explorer/tools/lean/check.sh" "$upstream" Machine.lean Sweeps.lean PassTail.lean PassRules.lean PassRel.lean
build=$(mktemp -d "$here/line024-check.XXXXXXXX")
trap 'rm -rf "$build"' EXIT
export LEAN_PATH="$build:$upstream/out:$explorer/tools/lean/out:$LEANLIB"
cd "$here"
for module in Wall Counter Timing Entry; do
    "$lean" "$module.lean" -o "$build/$module.olean"
done
python3 certificate.py > "$build/Phase.lean"
(cd "$build" && "$lean" Phase.lean -o Phase.olean)
"$lean" Checkpoint.lean -o "$build/Checkpoint.olean"
for module in Locality Box Guarded Landing StackReturn StackInvariant; do
    "$lean" "$module.lean" -o "$build/$module.olean"
done
python3 return_certificate.py > "$build/ReturnPhases.lean"
(cd "$build" && "$lean" ReturnPhases.lean -o ReturnPhases.olean)
"$lean" Return.lean -o "$build/Return.olean"
"$lean" MarkerTest.lean -o "$build/MarkerTest.olean"
