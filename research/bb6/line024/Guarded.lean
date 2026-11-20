import TM.Fin

namespace TM.Guarded
variable {Q : Type}
def cfg (c : FCfg Q) (L : Tape) : Cfg Q := ⟨app c.l L,app c.r blank,c.st⟩

/-- The supplied left extension is opaque. Stop if the finite left buffer is empty. -/
def run (δ : Q → Bool → Option (Bool × Dir × Q)) : Nat → FCfg Q → Option (FCfg Q)
  | 0,c => some c
  | n+1,c =>
    if c.l.isEmpty then none else (fstep δ c).bind (run δ n)

private theorem one (δ : Q → Bool → Option (Bool × Dir × Q)) (c : FCfg Q) (L : Tape)
    (h : c.l.isEmpty = false) :
    step δ (cfg c L) = (fstep δ c).map (fun d => cfg d L) := by
  obtain ⟨ls,rs,st⟩ := c
  cases ls with
  | nil => contradiction
  | cons b ls =>
    simp only [step,fstep,cfg,app_head]
    cases δ st (rs.headD false) with
    | none => rfl
    | some p =>
      obtain ⟨w,dir,q⟩ := p
      cases dir <;> simp [app_tail]

theorem sound (δ : Q → Bool → Option (Bool × Dir × Q)) {n : Nat} {c d : FCfg Q}
    (h : run δ n c = some d) (L : Tape) : steps δ n (cfg c L) = some (cfg d L) := by
  induction n generalizing c with
  | zero => simp [run] at h; subst d; rfl
  | succ n ih =>
    cases e : c.l.isEmpty with
    | true => simp [run,e] at h
    | false =>
      cases v : fstep δ c with
      | none => simp [run,e,v] at h
      | some m =>
        simp [run,e,v] at h
        have z := one δ c L e
        rw [v,Option.map_some] at z
        rw [steps_succ_of_step δ n z]
        exact ih h
end TM.Guarded
