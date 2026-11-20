import ThirdMarker
import FourthPhase

namespace H7846.Line24
open TM Word PhysicalWindow
set_option maxRecDepth 12000

private def firstDigits := [1,2,2,3,3,2,2,3,1,9]
private def nextDigits := [2,2,2,2,2,2,2,2,2,2,2]
private def lastDigits := [2,2,2,3,2,2,3,1,3,3,2,0,1,1]
def afterFourthDigits := [2,2,2,3,2,2,3,1,7,1,2,1,1]

private def tapeBits (ds : List Nat) (j : Nat) :=
  [true,false] ++ ds.flatMap (fun d => List.replicate (3*d) true ++ [false]) ++
  List.replicate (7+3*j) true

private theorem cutBits (bits : List Bool) (g : Nat) (R : Tape) :
    Box.cut (bits.length+g) (app bits blank) R = app bits (rep g [false] R) := by
  rw [Box.front,Box.zeros]

private theorem firstStart (L R : Tape) :
    guardedVisit L (word firstDigits 1) 33554532 R =
      visitX L firstDigits (rep 10 [true] (rep 33554426 [false] R)) := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  exact ⟨rfl,cutBits (tapeBits firstDigits 1) 33554426 R,rfl⟩

private def firstWall (L : Tape) := rep 29386116 [true] L
private def nextWall (L : Tape) := rep 2 [true,true,false] (rep 3 [true] (firstWall L))

private def openLeft (L : Tape) := rep 2 [true,true,false] (rep 3 [true] L)
private def sectionWord (x : Word) := Word.d 1 (.d 0 (.d 1 x))

private theorem openSource (x : Word) (L R : Tape) (g : Nat) :
    guardedVisit L (sectionWord x) (11+g) R =
      visitX L [1,0] (blkV 1 (Box.cut g x.tape R)) := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  exact ⟨rfl,Box.front [true,false,true,true,true,false,false,true,true,true,false] g x.tape R,rfl⟩

private theorem openTarget (x : Word) (L R : Tape) (g : Nat) :
    guardedVisit L x (2+g) R = visitX L [] (Box.cut g x.tape R) := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  exact ⟨rfl,Box.front [true,false] g x.tape R,rfl⟩

private theorem openDigit (x : Word) (L R : Tape) (g : Nat) : steps 35
    (guardedVisit L (sectionWord x) (11+g) R) = some (guardedVisit (openLeft L) x (2+g) R) := by
  have a := wallNextDigit 1 L (Box.cut g x.tape R)
  rw [openSource,openTarget]
  exact a

private def nearWall (L : Tape) := rep 4167896 [true] (nextWall L)
private def start : FCfg St := ⟨[false,true],tapeBits lastDigits 0 ++ List.replicate 406 false,.D⟩
private def full : FCfg St := {start with r := start.r ++ List.replicate 6 true ++ List.replicate 4 false}
private def finished : FCfg St := ⟨false::List.replicate 412 true,tapeBits afterFourthDigits 0,.D⟩

private theorem near (L R : Tape) : steps 5775300692
    (visitX L firstDigits (rep 10 [true] (rep 33554426 [false] R))) =
      some (window start (nearWall L) R) := by
  have a := guardRun fourthPhaseA 33554532 (by decide) L R
  change steps _ (guardedVisit L (word firstDigits 1) _ R) = _ at a
  rw [firstStart] at a
  have b := openDigit (word nextDigits 5) (firstWall L) R 4168405
  have c := guardRun fourthPhaseB 4168407 (by decide) (nextWall L) R
  have z := steps_seq trans (steps_seq trans a b) c
  have e : guardedVisit (rep 4167897 [true] (nextWall L)) (word lastDigits 0) 510 R =
      window start (nearWall L) R := by
    apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
    refine ⟨rfl,?_,rfl⟩
    change Box.cut ((tapeBits lastDigits 0).length+406) (app (tapeBits lastDigits 0) blank) R =
      app (tapeBits lastDigits 0 ++ List.replicate 406 false) R
    rw [cutBits,← app_app]
    rfl
  exact z.trans (congrArg some e)

/-- The fourth marker is first reached in C. The whole path up to this read is
independent of the bit on the marker and of all cells beyond it. -/
theorem fourthPassage (L R : Tape) : ∃ P, steps 5775366544
    (visitX L firstDigits (rep 10 [true] (rep 33554426 [false] R))) = some ⟨P,R,.C⟩ := by
  let c := (inside 65852 start).getD start
  have check : inside 65852 start = some c ∧ c.r = [] ∧ c.st = .C := by decide +native
  obtain ⟨run,right,st⟩ := check
  have z := winRun run (nearWall L) R
  unfold window at z
  rw [right,st] at z
  have all := steps_seq trans (near L R) z
  exact ⟨_,all⟩

private theorem afterMarker (L R : Tape) : steps 5775366939
    (visitX L firstDigits (rep 10 [true] (rep 33554426 [false] (rep 6 [true] (rep 4 [false] R))))) =
      some (visitX (rep 412 [true] (nearWall L)) afterFourthDigits (rep 7 [true] R)) := by
  have h : inside 66247 full = some finished := by decide +native
  have run := winRun h (nearWall L) R
  have e : window full (nearWall L) R =
      window start (nearWall L) (rep 6 [true] (rep 4 [false] R)) := by
    apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
    refine ⟨rfl,?_,rfl⟩
    change app ((start.r ++ List.replicate 6 true) ++ List.replicate 4 false) R = _
    rw [← app_app,← app_app]; rfl
  rw [e] at run
  have a := steps_seq trans (near L _) run
  exact a

theorem blankFourthContact : ∃ P, steps 4679906118752036 init = some ⟨P,fourthMarkerTail,.C⟩ := by
  obtain ⟨P,h⟩ := fourthPassage (rep 6 [true] impactWall) fourthMarkerTail
  have z := steps_seq trans blankAfterThird h
  exact ⟨P,z⟩

def fourthWall := rep 412 [true] (nearWall (rep 6 [true] impactWall))
theorem blankAfterFourth : steps 4679906118752431 init = some
    (visitX fourthWall afterFourthDigits
      (rep 7 [true] (rep 8388602 [false] fifthMarkerTail))) := by
  have z := blankAfterThird
  have e : fourthMarkerTail = rep 6 [true] (rep 4 [false] (rep 8388602 [false] fifthMarkerTail)) := by
    rw [fourthMarkerTail_eq,← rep_add 4 8388602]
  rw [e] at z
  have a := steps_seq trans z (afterMarker _ _)
  exact a

#print axioms blankFourthContact
#print axioms blankAfterFourth
end H7846.Line24
