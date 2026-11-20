import Landing

namespace H7846.Line24
open TM

/-- Right tape seen after a wall tail has opened onto exactly g blanks and a
six-one marker. Seven more blanks protect the arbitrary continuation. -/
def landingTape (g : Nat) (R : Tape) : Tape :=
  rep g [false] (rep 6 [true] (rep 7 [false] R))

/-- Time to turn left, excluding the subsequent erasure of older walls.
Index two is unused because that input instead reaches B1. -/
def landingTime : Nat → Nat
  | 0 => 55 | 1 => 47 | 2 => 0 | 3 => 63 | 4 => 89 | 5 => 77 | 6 => 91 | _ => 27

/-- Right half beyond the four leading zero cells after the turn, in each
nonhalting branch of this particular encounter. -/
def landingOutput (g : Nat) (R : Tape) : Tape :=
  match g with
  | 0 => rep 6 [true] (rep 2 [false] (rep 4 [true] R))
  | 1 => rep 4 [false] (rep 6 [true] (rep 3 [false] R))
  | 2 => R
  | 3 => rep 3 [true] (rep 2 [false] (rep 7 [true] (rep 3 [false] R)))
  | 4 => rep 1 [false] (rep 12 [true] (rep 3 [false] R))
  | 5 => rep 3 [false] (rep 3 [true] (rep 1 [false] (rep 7 [true] (rep 3 [false] R))))
  | 6 => rep 5 [false] (rep 10 [true] (rep 3 [false] R))
  | n+7 => app [false,false,true,true,true,true] (landingTape n R)

set_option maxRecDepth 30000 in
theorem landingTurn (g : Nat) (h : g ≠ 2) (L R : Tape) :
    steps (landingTime g) ⟨app [true,true,false] L,landingTape g R,.D⟩ =
      some ⟨L,rep 4 [false] (landingOutput g R),.A⟩ := by
  match g with
  | 0 | 1 | 3 | 4 | 5 | 6 => rfl
  | 2 => contradiction
  | n+7 =>
    have e : rep (n+7) [false] (rep 6 [true] (rep 7 [false] R)) = rep 7 [false] (landingTape n R) := by
      rw [Nat.add_comm n 7,rep_add]; rfl
    change steps 27 ⟨app [true,true,false] L,rep (n+7) [false] _,.D⟩ = _
    rw [e]; rfl

/-- Every gap except two executes a full erasure of every older wall, with
the exact number of moves and the complete resulting configuration. -/
theorem safeLandingErase (g : Nat) (h : g ≠ 2) (ws : List Nat) (L R : Tape) :
    steps (landingTime g + (ws.map (fun m => 22+m)).sum)
      ⟨app [true,true,false] (sq oldWall ws L),landingTape g R,.D⟩ =
      some ⟨L,rep 4 [false] (markers ws (landingOutput g R)),.A⟩ :=
  steps_seq trans (landingTurn g h _ R) (eraseWalls ws L _)

/-- With the two-cell gap, the third read would be the undefined instruction. -/
theorem twoGapLanding (L R : Tape) : ∃ c, steps 2 ⟨L,landingTape 2 R,.D⟩ =
    some c ∧ step c = none := ⟨_,rfl,rfl⟩

#print axioms safeLandingErase
end H7846.Line24
