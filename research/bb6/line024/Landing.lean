import Timing

namespace H7846.Line24
open TM Word

/-- Runs to the exposed blank exterior for every left context. -/
def Exits (x : Word) (t : Nat) : Prop :=
  ∀ L : Tape, ∃ P : Tape, steps t (visitX L [] x.tape) = some ⟨P,blank,.D⟩

theorem exitSeries {x y k t u} (h : Series x y k t) (next : Exits y u) :
    Exits x ((t+15*k)+u) := by
  intro L
  obtain ⟨P,b⟩ := next (rep (3*k) [true] L)
  exact ⟨P,steps_seq trans (runSeries h L) b⟩

theorem exitDigit (j : Nat) {x t} (next : Exits x t) :
    Exits (.d 1 (.d 0 (.d j x))) ((26+(j+1)*3+3)+t) := by
  intro L
  obtain ⟨P,b⟩ := next (rep (j+1) [true,true,false] (rep 3 [true] L))
  exact ⟨P,steps_seq trans (wallNextDigit j L x.tape) b⟩

theorem exitTip (j : Nat) : Exits (.d 1 (.d 0 (.tip j))) (26+(j+4)*3) :=
  fun L => ⟨_,wallTail j L blank⟩

/-- Seven clear cells at a landing suffice to turn left and erase any finite
stack of older walls. Everything past the seven cells is arbitrary. -/
theorem landingErase (ws : List Nat) (L R : Tape) :
    steps (27 + (ws.map (fun m => 22+m)).sum)
      ⟨app [true,true,false] (sq oldWall ws L),rep 7 [false] R,.D⟩ =
    some ⟨L,rep 4 [false] (markers ws (app [false,false,true,true,true,true] R)),.A⟩ := by
  have turn (X : Tape) : steps 27 ⟨app [true,true,false] X,rep 7 [false] R,.D⟩ =
      some ⟨X,rep 4 [false] (app [false,false,true,true,true,true] R),.A⟩ := by
    set_option maxRecDepth 10000 in rfl
  exact steps_seq trans (turn _) (eraseWalls ws L _)

end H7846.Line24
