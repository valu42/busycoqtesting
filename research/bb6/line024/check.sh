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
    "$lean" -j 1 "$module.lean" -o "$build/$module.olean"
done
python3 certificate.py > "$build/Phase.lean"
(cd "$build" && "$lean" -j 1 Phase.lean -o Phase.olean)
"$lean" -j 1 Checkpoint.lean -o "$build/Checkpoint.olean"
for module in Locality Box Guarded Landing StackReturn StackInvariant; do
    "$lean" -j 1 "$module.lean" -o "$build/$module.olean"
done
python3 return_certificate.py > "$build/ReturnPhases.lean"
(cd "$build" && "$lean" -j 1 ReturnPhases.lean -o ReturnPhases.olean)
"$lean" -j 1 Return.lean -o "$build/Return.olean"
"$lean" -j 1 MarkerTest.lean -o "$build/MarkerTest.olean"

module() { "$lean" -j 1 "$1.lean" -o "$build/$1.olean"; }
generated() {
    python3 "$1" > "$build/$2.lean"
    (cd "$build" && "$lean" -j 1 "$2.lean" -o "$2.olean")
}
for m in CollisionRules SharpPhase CompletePass WordGrammar MarkerGaps MarkerPass MarkerTrain \
         MixedWalls MergedMarker MarkerLanding StackClock LandingCoordinate MarkerCoordinate TerminalGap PassiveGapPairs CellPotential GuardedPhase \
         Absorption PhysBridge SecondEntry WindowBarrier AlignedWitness AlignedMarkers PackedTape PackedPhase \
         PackedWalls PackedRestart; do
    module "$m"
done
generated sharp_certificate.py SharpThirdPhase
module SharpThird
module TwoMarkerPrefix
module ThirdMarker
generated fourth_certificate.py FourthPhase
module FourthMarker
generated debris_certificate.py DebrisPhase
module DebrisContact
generated recovery_certificate.py RecoveryPhase
generated stack_certificate.py PackedStack
module OldDebris

python3 epoch_certificate.py "$build"
cmp EpochReturn.lean "$build/EpochReturn.lean"
(cd "$build" && {
    shopt -s nullglob
    for source in EpochPart[0-9][0-9][0-9].lean; do
        for support in "${source%.lean}"Support*.lean; do
            "$lean" -j 1 "$support" -o "${support%.lean}.olean"
        done
        "$lean" -j 1 "$source" -o "${source%.lean}.olean"
    done
    "$lean" -j 1 EpochReturn.lean -o EpochReturn.olean
})

module EpochDivergence
