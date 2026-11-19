import TM.Basic

namespace TM.Locality
variable {Q : Type} (δ : Q → Bool → Option (Bool × Dir × Q))

/-- Both tapes, measured from their respective heads, coincide on their first n cells. -/
def Agree (n : Nat) (a b : Cfg Q) : Prop :=
  a.st = b.st ∧ (∀ i < n, a.l i = b.l i) ∧ (∀ i < n, a.r i = b.r i)

private theorem move {n : Nat} {a b c : Cfg Q} (h : Agree (n+1) a b)
    (s : step δ a = some c) : ∃ d, step δ b = some d ∧ Agree n c d := by
  obtain ⟨hs,hl,hr⟩ := h
  have hr0 := hr 0 (by omega)
  unfold step at s ⊢
  rw [← hs, ← hr0]
  cases v : δ a.st (a.r 0) with
  | none => simp [v] at s
  | some p =>
    obtain ⟨w,dir,q⟩ := p
    cases dir <;> simp [v] at s <;> subst c <;> refine ⟨_,rfl,rfl,?_,?_⟩
    · intro i hi; exact hl (i+1) (by omega)
    · intro i hi; cases i with
      | zero => exact hl 0 (by omega)
      | succ i => cases i with
        | zero => rfl
        | succ i => exact hr (i+1) (by omega)
    · intro i hi; cases i with
      | zero => rfl
      | succ i => exact hl i (by omega)
    · intro i hi; exact hr (i+1) (by omega)

/-- A known run of t moves transfers between two tapes with t+r matching cells
on each side. The endpoints agree for the remaining radius r. -/
theorem transfer (t r : Nat) {a b c : Cfg Q} (h : Agree (t+r) a b)
    (s : steps δ t a = some c) : ∃ d, steps δ t b = some d ∧ Agree r c d := by
  induction t generalizing a b with
  | zero => simp [steps] at s; subst c; exact ⟨b,rfl,by simpa using h⟩
  | succ t ih =>
    cases v : step δ a with
    | none => simp [steps,v] at s
    | some a' =>
      have h' : Agree ((t+r)+1) a b := by simpa [Nat.succ_add] using h
      obtain ⟨b',vb,hab⟩ := move δ h' v
      rw [steps_succ_of_step δ t v] at s
      obtain ⟨d,hd,hh⟩ := ih hab s
      exact ⟨d,by rwa [steps_succ_of_step δ t vb],hh⟩
end TM.Locality
