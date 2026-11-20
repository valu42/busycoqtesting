import SharpThird
import PhysBridge
import Absorption

namespace H7846.Line24
open TM Word
set_option maxRecDepth 15000

private abbrev bridgeLeft := sharpBridgeLeft
def impactWall := rep 415 [true] bridgeLeft

theorem blankBeforeThird : steps 4679900343384498 init =
    some (preImpact bridgeLeft thirdMarkerTail) := by
  have h := steps_seq trans blankSecondEntry sharpToPreImpact
  exact h

/-- F arrives at the original first one of the third marker. -/
theorem blankThirdContact : ∃ L, steps 4679900343384640 init =
    some ⟨L,thirdMarkerTail,.F⟩ := by
  obtain ⟨L,v⟩ := atFirstContact bridgeLeft thirdMarkerTail
  have h := steps_seq trans blankBeforeThird v
  exact ⟨L,h⟩

private theorem available : thirdMarkerTail =
    rep 6 [true] (rep 4 [false] (rep 33554426 [false] fourthMarkerTail)) := by
  rw [thirdMarkerTail_eq,← rep_add 4 33554426]

/-- In two sweeps the third marker is incorporated into the counter. -/
theorem blankAfterThird : steps 4679900343385492 init = some
    (visitX (rep 6 [true] impactWall) [1,2,2,3,3,2,2,3,1,9]
      (rep 10 [true] (rep 33554426 [false] fourthMarkerTail))) := by
  have a := blankBeforeThird
  rw [available] at a
  have b := thirdAbsorption impactWall (rep 33554426 [false] fourthMarkerTail)
  have h := steps_seq trans a b
  exact h

#print axioms blankThirdContact
#print axioms blankAfterThird
end H7846.Line24
