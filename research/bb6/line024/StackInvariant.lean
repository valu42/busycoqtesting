import StackReturn

namespace H7846.Line24
open TM Word

/-- Any finite sequence of ordinary phases joined by 1,0,1 wall openings,
ending in the 1,0,tip(0) landing. The indices retain time and every output gap. -/
inductive StackPhases : Word → Nat → List Nat → Nat → List Nat → Prop where
  | last {x k t} (h : Series x (.d 1 (.d 0 (.tip 0))) k t) (w : Nat) (ws : List Nat) :
      StackPhases x w ws (((t+15*k)+38)+(27+((0::(1+3*k+w)::ws).map (fun m => 22+m)).sum))
        (0::(1+3*k+w)::ws)
  | next {x y k t w ws u out} (h : Series x (.d 1 (.d 0 (.d 1 y))) k t)
      (rest : StackPhases y 2 ((1+3*k+w)::ws) u out) :
      StackPhases x w ws (((t+15*k)+35)+u) out

theorem StackPhases.execute {x w ws n out} (p : StackPhases x w ws n out) (L : Tape) :
    steps n (visitX (stackBase w ws L) [] x.tape) = some (regenerated out L) := by
  induction p with
  | last h w ws => exact lastStack h w ws L
  | @next x y k t w ws u out h rest ih =>
    exact steps_seq trans (nextStack h w ws L) ih

/-- Every gap contributed by this entire class of stack returns is divisible
by three when the incoming wall width is 2 modulo 3 and the older gaps align. -/
theorem StackPhases.aligned {x w ws n out} (p : StackPhases x w ws n out)
    (hw : w % 3 = 2) (hs : ∀ m ∈ ws, m % 3 = 0) :
    ∀ m ∈ out, m % 3 = 0 := by
  induction p with
  | @last x k t h w ws =>
    intro m hm
    simp only [List.mem_cons] at hm
    rcases hm with rfl | rfl | old
    · decide
    · omega
    · exact hs m old
  | @next x y k t w ws u out h rest ih =>
    apply ih (by decide)
    intro m hm
    simp only [List.mem_cons] at hm
    rcases hm with rfl | old
    · omega
    · exact hs m old
end H7846.Line24
