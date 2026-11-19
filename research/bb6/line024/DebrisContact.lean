import DebrisPhase
import PhysBridge
import StackReturn
import Checkpoint

namespace H7846.Line24
open TM PhysicalWindow
set_option maxRecDepth 16000

def postStackState : Config := guardedVisit (stackBase 15353093 [137382804,8628,1320] exterior)
  postStackWord 18396649123346 (rep 4 [true] debris)

private def lastDigits := [2,2,2,1,3,5,1,4,2,1,2,1,5,2,2,1,1,2,5,3,1,4,1,2,0]
private def lastBits := [true,false] ++
  lastDigits.flatMap (fun n => List.replicate (3*n) true ++ [false]) ++ List.replicate 7 true
private def start (extra : List Bool) : FCfg St :=
  ⟨[false,true], (lastBits ++ List.replicate 733 false) ++ extra, .D⟩

private theorem blankPrefix (n : Nat) (R : Tape) :
    app (List.replicate n false) R = rep n [false] R := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [List.replicate_succ,app_cons,rep_succ,app]; rw [ih]

private theorem toWindow (L R : Tape) (suffix : List Bool) :
    steps 5717374479265554 (guardedVisit L postStackWord 18396649123346 (app suffix R)) =
      some (window (start suffix) (rep 18396649122413 [true] L) R) := by
  have go := guardRun debrisPhase 18396649123346 (by decide) L (app suffix R)
  change steps 5717374479265554 _ = some
    ⟨cons false (rep 18396649122414 [true] L),Box.cut 932 (app [true,false] lastDebrisWord.tape) (app suffix R),.D⟩ at go
  have right : Box.cut 932 (app [true,false] lastDebrisWord.tape) (app suffix R) =
      app (start suffix).r R := by
    change Box.cut (lastBits.length+733) (app lastBits blank) (app suffix R) =
      app ((lastBits ++ List.replicate 733 false) ++ suffix) R
    rw [Box.front,Box.zeros,← app_app,← app_app,blankPrefix]
  rw [right] at go
  exact go

private def first := (inside 225336 (start [])).getD (start [])
private theorem firstFacts : inside 225336 (start []) = some first ∧ first.st = .F ∧ first.r = [] := by decide +native

private theorem firstConfig (c : FCfg St) (L R : Tape) (st : c.st = .F) (r : c.r=[]) :
    window c L R = ⟨app c.l L,R,.F⟩ := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  exact ⟨rfl,congrArg (fun xs => app xs R) r,st⟩

attribute [local irreducible] first TM.steps TM.rep

/-- From this counter, the first cell of any suffix at the old debris position
is reached in F, without inspecting that suffix beforehand. -/
theorem debrisContact (L R : Tape) : ∃ P : Tape,
    steps 5717374479490890 (guardedVisit L postStackWord 18396649123346 R) =
      some ⟨P,R,.F⟩ := by
  obtain ⟨run,st,r⟩ := firstFacts
  have a := toWindow L R []
  have b := winRun run (rep 18396649122413 [true] L) R
  have eq := firstConfig first (rep 18396649122413 [true] L) R st r
  have z := steps_seq trans a (b.trans (congrArg some eq))
  exact ⟨_,z⟩

private def leading := List.replicate 7 true ++ [false]
private def finish := (inside 225346 (start leading)).getD (start leading)

private theorem finishFacts : inside 225346 (start leading) = some finish ∧ finish.st = .D ∧
    finish.r = [true,false] ∧ finish.l = false :: finish.l.tail := by decide +native

attribute [local irreducible] finish

/-- Exact left half, after absorbing the seven leading ones of the debris and
starting a fresh counter at its surviving suffix. -/
def afterDebrisLeft (L : Tape) : Tape := app finish.l.tail (rep 18396649122413 [true] L)

def debrisExterior (L : Tape) : Tape := app (finish.l.drop 4) (rep 18396649122413 [true] L)

theorem afterDebrisShape (L : Tape) : afterDebrisLeft L = stackBase 2 [] (debrisExterior L) := by
  have h : finish.l.tail = [true,true,false] ++ finish.l.drop 4 := by decide +native
  unfold afterDebrisLeft
  rw [h,← app_app]
  have simple (X : Tape) : app [true,true,false] X = stackBase 2 [] X := by
    unfold stackBase
    rw [rep_succ 1,rep_succ 0,rep_zero]
    rfl
  exact simple _

private theorem returnConfig (c : FCfg St) (L R : Tape) (s : c.st = .D) (r : c.r = [true,false])
    (l : c.l = false :: c.l.tail) : window c L R = visitX (app c.l.tail L) [] R := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  exact ⟨congrArg (fun xs => app xs L) l,congrArg (fun xs => app xs R) r,s⟩

private theorem runLastWindow (A R : Tape) :
    steps 225346 (window (start leading) A R) = some (visitX (app finish.l.tail A) [] R) := by
  obtain ⟨run,st,r,l⟩ := finishFacts
  have b := winRun run A R
  exact b.trans (congrArg some (returnConfig finish A R st r l))

/-- The same transformation holds for any continuation after the initial seven
ones and the following separating zero. -/
theorem absorbDebris (L R : Tape) :
    steps 5717374479490900 (guardedVisit L postStackWord 18396649123346 (app leading R)) =
      some (visitX (afterDebrisLeft L) [] R) := by
  have a := toWindow L R leading
  have b := runLastWindow (rep 18396649122413 [true] L) R
  have z := steps_seq trans a b
  exact z

def survivingWord := word (List.replicate 19 2 ++ [3,0,1,1]) 0

theorem debrisCounter (L : Tape) :
    steps 5717374479490900 (guardedVisit L postStackWord 18396649123346 (rep 4 [true] debris)) =
      some (visitX (afterDebrisLeft L) [] survivingWord.tape) := by
  have h := absorbDebris L survivingWord.tape
  have inp : app leading survivingWord.tape = rep 4 [true] debris := by
    have deq : debris = blkV 1 survivingWord.tape := rfl
    rw [deq]
    have simple (X : Tape) : app leading X = rep 4 [true] (blkV 1 X) := by
      unfold blkV
      rw [rep_succ 3,rep_succ 2,rep_succ 1,rep_succ 0,rep_zero,rep_succ 0,rep_zero]
      rfl
    exact simple _
  rw [inp] at h
  exact h

#print axioms debrisCounter
end H7846.Line24
