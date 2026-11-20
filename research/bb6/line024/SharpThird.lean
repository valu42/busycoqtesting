import SharpThirdPhase
import SecondEntry
import PhysBridge

namespace H7846.Line24
open TM Word
set_option maxRecDepth 15000

def sharpBridgeLeft : Tape := rep 107987678 [true] (stackBase 8588 [8628,1320] exterior)

private def buffer := [true,false] ++ [1,3,1,1,4,2,2,4,4,3,1,0,1,0].flatMap
  (fun d : Nat => List.replicate (3*d) true ++ [false]) ++ List.replicate 7 true

private theorem bufferOn (X : Tape) : app buffer X = app [true,false] (secondEntryWord.above X) := rfl

theorem sharpEntryTape (R : Tape) :
    Box.cut 107988195 secondEntryModel.r R =
      app [true,false] (secondEntryWord.above (rep 107988091 [false] R)) := by
  have len : buffer.length = 104 := by decide
  have e : app buffer blank = secondEntryModel.r := rfl
  have z := Box.front buffer 107988091 blank R
  rw [len,e,Box.zeros] at z
  exact z.trans (bufferOn _)

private theorem aboveWord (ds : List Nat) (j : Nat) (R : Tape) :
    (word ds j).above R = sq blkV ds (rep (7+3*j) [true] R) := by
  induction ds with
  | nil => rfl
  | cons d ds ih => exact congrArg (blkV d) ih

private theorem endForm (L R : Tape) :
    visitX (rep 415 [true] L) [] ((word impactDigits 8).above (rep 3 [false] R)) = preImpact L R := by
  exact congrArg (fun Z : Tape => (⟨cons false (rep 415 [true] L),app [true,false] Z,.D⟩ : Config))
    (aboveWord impactDigits 8 (rep 3 [false] R))

private theorem sharpEntryCfgEq : secondEntryCfg =
    visitX (stackBase 8588 [8628,1320] exterior) []
      (secondEntryWord.above (rep 107988091 [false] thirdMarkerTail)) := by
  exact congrArg (fun Y : Tape => (⟨secondEntryModel.l,Y,.D⟩ : Config)) (sharpEntryTape thirdMarkerTail)

attribute [local irreducible] TM.steps TM.rep

theorem sharpOpenToPreImpact (w R : Tape) :
    steps 17585760683 (visitX w [] (secondEntryWord.above (rep 107988091 [false] R))) =
    some (preImpact (rep 107987678 [true] w) R) := by
  have h := (sharpRun sharpThirdPhase w (rep 3 [false] R)).2
  change steps 17585760683 (visitX w [] (secondEntryWord.above
    (rep 107988088 [false] (rep 3 [false] R)))) =
      some (visitX (rep 107988093 [true] w) [] ((word impactDigits 8).above
        (rep 3 [false] R))) at h
  have el : rep 107988093 [true] w = rep 415 [true] (rep 107987678 [true] w) :=
    rep_add 415 107987678 _ _
  have er : rep 107988088 [false] (rep 3 [false] R) = rep 107988091 [false] R :=
    (rep_add 107988088 3 _ _).symm
  rw [er,el,endForm] at h
  exact h

/-- Exact ordinary-pass certificate from second entry to the three-cell clearance. -/
theorem sharpToPreImpact : steps 17585760683 secondEntryCfg =
    some (preImpact sharpBridgeLeft thirdMarkerTail) := by
  rw [sharpEntryCfgEq]
  exact sharpOpenToPreImpact _ _

#print axioms sharpToPreImpact
end H7846.Line24
