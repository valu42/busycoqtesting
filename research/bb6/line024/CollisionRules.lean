import Timing

namespace H7846.Line24
open TM Word
set_option maxRecDepth 30000

/-- The unprocessed six-one marker, with three blanks before and four after it. -/
def contact (R : Tape) := rep 3 [false] (rep 6 [true] (rep 4 [false] R))

/-- The six-one marker becomes the new T1 tail, with two empty digits before it. -/
def contactResult (R : Tape) := sq blkV [1,0,0] (rep 10 [true] R)

private theorem tailUnfold (j : Nat) (X : Tape) :
    rep (7+3*(j+1)) [true] X =
    app [true,true] (rep j [true,true,true] (rep 8 [true] X)) := by
  induction j with
  | zero => rfl
  | succ j ih =>
    rw [show 7+3*(j+1+1) = (7+3*(j+1))+3 by omega]
    change app [true,true,true] (rep (7+3*(j+1)) [true] X) = _
    rw [ih]; rfl

private theorem contactTurn (L R : Tape) :
    steps 114 ⟨L,rep 8 [true] (contact R),.D⟩ =
      some ⟨L,rep 4 [false] (cons false (contactResult R)),.A⟩ := by rfl

/-- Lift a finite turn at the right tip to all tail indices. Only the two
fixed-size contexts (seven and eight ones) depend on the exterior pattern. -/
theorem extendTail {X Y : Tape} {t : Nat}
    (base : Timed (rep 7 [true] X) Y t)
    (turn : ∀ L, steps (t-4) ⟨L,rep 8 [true] X,.D⟩ = some ⟨L,rep 4 [false] Y,.A⟩)
    (ht : 4 ≤ t) (j : Nat) :
    Timed (rep (7+3*j) [true] X) (rep j [true,true,true] Y) (14*j+t) := by
  cases j with
  | zero => simpa using base
  | succ j =>
    intro L
    have enter := d_head L (rep j [true,true,true] (rep 8 [true] X))
    have right := cross_r trans (u := []) d_unit j (app [true,true,true,false] L)
        (rep 8 [true] X)
    have left := steps_seq trans (cross_l trans a_unit j (app [true,true,true,false] L) Y)
        (a_head L (rep j [true,true,true] Y))
    have run := steps_seq trans (steps_seq trans (steps_seq trans enter right) (turn (blkL j L))) left
    change steps _ ⟨L,app [true,false] (rep _ [true] X),.D⟩ = _
    rw [tailUnfold,show 14*(j+1)+t = 6+j*3+(t-4)+(j*11+12) by omega]
    exact run

/-- For every tail index, including zero, contact with a six-one marker across
three zeros returns a counter. Both exterior tapes are arbitrary. -/
theorem timedContact (j : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (contact R))
      (blkV j (contactResult R)) (14*j+118) :=
  extendTail (t := 118) (by intro L; rfl) (fun L => contactTurn L R) (by decide) j

/-- Positive digits before the contact persist. The head moves three cells
right after turning at the wall. -/
theorem framedContact (ds : List Nat) (j : Nat) (L R : Tape) :
    let ks := ds.map (·+1)
    steps (((ds.map (fun d => 14*(d+1)+4)).sum+(14*j+118))+15)
      (visitX L ks (rep (7+3*j) [true] (contact R))) =
    some (visitX (rep 3 [true] L) ks (blkV j (contactResult R))) := by
  dsimp only
  have framed : Timed (sq blkV (ds.map (·+1)) (rep (7+3*j) [true] (contact R)))
      (sq blkV (ds.map (·+1)) (blkV j (contactResult R)))
      ((ds.map (fun d => 14*(d+1)+4)).sum+(14*j+118)) := by
    induction ds with
    | nil => simpa using timedContact j R
    | cons x xs ih =>
      have a := timedKeep x ih
      simp only [List.map_cons,List.sum_cons] 
      rw [show (14*(x+1)+4)+(xs.map (fun d => 14*(d+1)+4)).sum+(14*j+118) =
          ((xs.map (fun d => 14*(d+1)+4)).sum+(14*j+118))+(14*(x+1)+4) by omega]
      exact a
  exact steps_seq trans (framed (cons false L)) (wall_turn L _)

/-- The observed pass at the third marker has this particular positive prefix and tail. -/
theorem thirdContact (L R : Tape) :
    steps 547 (visitX L [1,2,2,3,3,2,2,3,1] (rep 31 [true] (contact R))) =
      some (visitX (rep 3 [true] L) [1,2,2,3,3,2,2,3,1] (blkV 8 (contactResult R))) :=
  framedContact [0,1,1,2,2,1,1,2,0] 8 L R


/-- Across a positive digit followed by an empty digit, the head enters the
remaining tape with three new ones before it. Any returning suffix computation
can therefore be used here, including a collision with an existing marker. -/
theorem timedSplitSuffix (m : Nat) {X Y : Tape} {t : Nat}
    (core : Timed (rep 3 [true] X) Y t) :
    Timed (sq blkV [m+2,0] X) (sq blkV [m,1] Y) (14*m+32+t) := by
  cases m with
  | zero =>
    intro L
    let P := app [true,true,true,true,false] L
    have a : steps 19 ⟨L,app [true,false] (sq blkV [2,0] X),.D⟩ =
        some ⟨P,app [true,false] (rep 3 [true] X),.D⟩ := rfl
    have b : steps 13 ⟨P,rep 5 [false] Y,.A⟩ =
        some ⟨L,rep 5 [false] (sq blkV [0,1] Y),.A⟩ := rfl
    have r := steps_seq trans (steps_seq trans a (core P)) b
    rw [show 14*0+32+t = 19+t+13 by omega]
    exact r
  | succ m =>
    intro L
    let Z := rep 7 [true] (rep 2 [false] X)
    have enc : app [true,false] (sq blkV [m+1+2,0] X) =
        app [true,false,true,true] (rep m [true,true,true] Z) := by
      have e (k : Nat) : rep (k+1+2) [true,true,true] (rep 2 [false] X) =
          app [true,true] (rep k [true,true,true] Z) := by
        induction k with
        | zero => rfl
        | succ k ih =>
          change app [true,true,true] (rep (k+1+2) [true,true,true] (rep 2 [false] X)) = _
          rw [ih]; rfl
      exact congrArg (app [true,false]) (e m)
    have a := d_head L (rep m [true,true,true] Z)
    have b := cross_r trans (u := []) d_unit m (app [true,true,true,false] L) Z
    have c (P : Tape) : steps 16 ⟨P,Z,.D⟩ =
        some ⟨app [true,true,true,false] P,app [true,false] (rep 3 [true] X),.D⟩ := rfl
    have inner := core (app [true,true,true,false] (blkL m L))
    have d := a_head (blkL m L) (cons false Y)
    let U := cons false (app [true,true,true] (cons false Y))
    have f := cross_l trans a_unit m (app [true,true,true,false] L) U
    have g := a_head L (rep m [true,true,true] U)
    have r := steps_seq trans (steps_seq trans (steps_seq trans (steps_seq trans
        (steps_seq trans (steps_seq trans a b) (c (blkL m L))) inner) d) f) g
    change steps _ ⟨L,app [true,false] _,.D⟩ = _
    rw [enc,show 14*(m+1)+32+t = 6+m*3+16+t+12+m*11+12 by omega]
    exact r

/-- The split case with the same three-blank clearance as the actual collision. -/
theorem timedSplitContact (m : Nat) (R : Tape) :
    Timed (sq blkV [m+2,0] (rep 7 [true] (contact R)))
      (sq blkV [m,1,1] (contactResult R)) (14*m+32+132) :=
  timedSplitSuffix m (timedContact 1 R)

#print axioms timedSplitSuffix
#print axioms framedContact
end H7846.Line24
