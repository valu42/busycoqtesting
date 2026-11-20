import CollisionRules

namespace H7846.Line24
open TM Word

set_option maxRecDepth 16000

/-- Four clear cells suffice for the ordinary tail turn. The tape behind them is arbitrary. -/
theorem timedClear (j : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (rep 4 [false] R))
      (blkV j (rep 7 [true] R)) (14*j+54) :=
  extendTail (t := 54) (by intro L; rfl) (by intro L; rfl) (by decide) j

/-- A marker touching the tail extends its index by m, for any length 3m. -/
theorem timedTouch (j m : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (rep (3*m) [true] (rep 4 [false] R)))
      (blkV (j+m) (rep 7 [true] R)) (14*(j+m)+54) := by
  rw [← rep_add,show 7+3*j+3*m=7+3*(j+m) by omega]
  exact timedClear (j+m) R

/-- The one-cell gap at a six-one marker inserts a zero digit and the T1 tail. -/
theorem timedGapOne (j : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (cons false (rep 6 [true] (rep 4 [false] R))))
      (blkV (j+1) (cons false (rep 10 [true] R))) (14*j+96) := by
  have h := extendTail (X := cons false (rep 6 [true] (rep 4 [false] R)))
    (Y := blkV 1 (cons false (rep 10 [true] R))) (t := 96)
    (by intro L; rfl) (by intro L; rfl) (by decide) j
  change Timed _ (rep j [true,true,true] (app [true,true,true] _)) _ at h
  rw [rep_app_comm] at h
  exact h

private theorem subGapTwo (L X : Tape) :
    steps 23 ⟨L,app [true,false] (rep 7 [true]
            (rep 2 [false] (rep 3 [true] X))),.D⟩ =
      some ⟨app [true,true,true,true,false] L,app [true,false] (rep 7 [true] X),.D⟩ := rfl

private theorem subGapTwo' (L X : Tape) :
    steps 20 ⟨L,rep 8 [true] (rep 2 [false] (rep 3 [true] X)),.D⟩ =
      some ⟨app [true,true,true,false] L,app [true,false] (rep 7 [true] X),.D⟩ := rfl

private theorem finishGapTwo (L Y : Tape) :
    steps 13 ⟨app [true,true,true,true,false] L,rep 5 [false] Y,.A⟩ =
      some ⟨L,rep 5 [false] (cons false (blkV 1 Y)),.A⟩ := rfl

private theorem finishGapTwo' (L Y : Tape) :
    steps 12 ⟨app [true,true,true,false] L,rep 5 [false] Y,.A⟩ =
      some ⟨L,rep 4 [false] (cons false (blkV 1 Y)),.A⟩ := rfl

/-- Two blank cells before a positive marker of length 3(m+1) produce
digits j,1,m and a T0 tail, including m=0. -/
theorem timedGapTwo (j m : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (rep 2 [false] (rep (3*(m+1)) [true] (rep 4 [false] R))))
      (blkV j (blkV 1 (blkV m (rep 7 [true] R)))) (14*j+(14*m+90)) := by
  let X := rep (3*m) [true] (rep 4 [false] R)
  let Y := blkV m (rep 7 [true] R)
  have inner := timedClear m R
  rw [show 3*(m+1)=3+3*m by omega,rep_add 3 (3*m)]
  apply extendTail (t := 14*m+90)
  · intro L
    have a := subGapTwo L X
    have b := inner (app [true,true,true,true,false] L)
    rw [rep_add 7 (3*m)] at b
    have z := steps_seq trans (steps_seq trans a b) (finishGapTwo L Y)
    rw [show 23+(14*m+54)+13=14*m+90 by omega] at z
    exact z
  · intro L
    have a := subGapTwo' L X
    have b := inner (app [true,true,true,false] L)
    rw [rep_add 7 (3*m)] at b
    have z := steps_seq trans (steps_seq trans a b) (finishGapTwo' L Y)
    rw [show 20+(14*m+54)+12=14*m+90-4 by omega] at z
    exact z
  · omega

end H7846.Line24
