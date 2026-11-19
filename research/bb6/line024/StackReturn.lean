import Landing
import Entry

namespace H7846.Line24
open TM Word
def stackBase (w : Nat) (ws : List Nat) (L : Tape) :=
  rep w [true] (cons false (sq oldWall ws L))

private theorem grow (w n : Nat) (ws : List Nat) (L : Tape) :
    rep 3 [true] (rep n [true] (stackBase w ws L)) =
      rep ((1+n+w)+2) [true] (cons false (sq oldWall ws L)) := by
  unfold stackBase
  rw [← rep_add, ← rep_add]
  congr 1 <;> omega

/-- A counter phase followed by opening the next digit creates one older wall. -/
theorem nextStack {x y k t} (h : Series x (.d 1 (.d 0 (.d 1 y))) k t)
    (w : Nat) (ws : List Nat) (L : Tape) :
    steps ((t+15*k)+35) (visitX (stackBase w ws L) [] x.tape) =
      some (visitX (stackBase 2 ((1+3*k+w)::ws) L) [] y.tape) := by
  have a := runSeries h (stackBase w ws L)
  have b := wallNextDigit 1 (rep (3*k) [true] (stackBase w ws L)) y.tape
  rw [grow] at b
  exact steps_seq trans a b

def clearTail := app [false,false,true,true,true,true] blank
def regenerated (ws : List Nat) (L : Tape) : Config :=
  ⟨L,rep 4 [false] (markers ws clearTail),.A⟩

/-- The final tail exposes blank, then the head erases the entire stack. -/
theorem lastStack {x k t} (h : Series x (.d 1 (.d 0 (.tip 0))) k t)
    (w : Nat) (ws : List Nat) (L : Tape) :
    let widths := 0 :: (1+3*k+w) :: ws
    steps (((t+15*k)+38) + (27 + (widths.map (fun m => 22+m)).sum))
      (visitX (stackBase w ws L) [] x.tape) = some (regenerated widths L) := by
  dsimp only
  have a := runSeries h (stackBase w ws L)
  have b := wallTail 0 (rep (3*k) [true] (stackBase w ws L)) blank
  rw [grow] at b
  have c := landingErase (0::(1+3*k+w)::ws) L blank
  have eq : rep 7 [false] blank = blank := by
    have all (n : Nat) : rep n [false] blank = blank := by
      induction n with
      | zero => rfl
      | succ n ih => rw [rep_succ, ih]; exact cons_false_blank
    exact all 7
  rw [eq] at c
  have ab := steps_seq trans a b
  exact steps_seq trans ab c
end H7846.Line24
