import StackInvariant
namespace H7846.Line24
open TM Word

private theorem preZero {x : Word} (h : Pass x (.d 0 (.tip 0))) : x = .tip 0 := by
  cases h <;> rfl

private theorem preTerminal {x : Word} (h : Pass x (.d 1 (.d 0 (.tip 0)))) :
    x = .d 1 (.tip 0) := by
  cases h with
  | keep i s => rw [preZero s]

private theorem preOne {x : Word} (h : Pass x (.d 1 (.tip 0))) : x = .tip 1 := by
  cases h with
  | tipStep => rfl
  | keep i s => cases s

private theorem noPreimage {x : Word} (h : Pass x (.tip 1)) : False := by cases h

/-- Complete list of ordinary histories that can immediately precede the T0
terminal opening. This uses the rewrite relation, not a bound estimated from time. -/
theorem terminalHistories {x : Word} {k : Nat} (h : Passes k x (.d 1 (.d 0 (.tip 0)))) :
    (k=0 ∧ x=.d 1 (.d 0 (.tip 0))) ∨ (k=1 ∧ x=.d 1 (.tip 0)) ∨ (k=2 ∧ x=.tip 1) := by
  cases h with
  | refl => exact Or.inl ⟨rfl,rfl⟩
  | next h s =>
    cases preTerminal s
    cases h with
    | refl => exact Or.inr (Or.inl ⟨rfl,rfl⟩)
    | next h s =>
      cases preOne s
      cases h with
      | refl => exact Or.inr (Or.inr ⟨rfl,rfl⟩)
      | next h s => exact (noPreimage s).elim

/-- A wall opened at width 2 can leave only gap 3, 6 or 9 immediately behind
the zero gap when its next ordinary phase ends in the terminal T0 opening. -/
theorem terminalGap {x : Word} {k : Nat} (h : Passes k x (.d 1 (.d 0 (.tip 0)))) :
    1+3*k+2=3 ∨ 1+3*k+2=6 ∨ 1+3*k+2=9 := by
  rcases terminalHistories h with h | h | h <;> omega

end H7846.Line24
