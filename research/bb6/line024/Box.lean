import TM.Basic

namespace TM.Box
variable {Q : Type}
def cut : Nat → Tape → Tape → Tape
  | 0, _, Y => Y
  | n+1, X, Y => cons (X 0) (cut n (tail X) Y)

def frame (c : Cfg Q) (a b : Nat) (L R : Tape) : Cfg Q :=
  ⟨cut a c.l L, cut b c.r R,c.st⟩

theorem front (w : List Bool) (n : Nat) (X Y : Tape) :
    cut (w.length+n) (app w X) Y = app w (cut n X Y) := by
  induction w with
  | nil => simp
  | cons b w ih =>
    change cut ((w.length+1)+n) (cons b (app w X)) Y = _
    rw [show w.length+1+n=(w.length+n)+1 by omega]
    exact congrArg (cons b) ih

theorem zeros (n : Nat) (Y : Tape) : cut n blank Y = rep n [false] Y := by
  induction n with
  | zero => rfl
  | succ n ih => exact congrArg (cons false) ih

theorem zeroBlank (n : Nat) : rep n [false] blank = blank := by
  induction n with
  | zero => rfl
  | succ n ih => rw [rep_succ, ih]; exact cons_false_blank

theorem read (n : Nat) (X Y : Tape) (i : Nat) :
    cut n X Y i = if i < n then X i else Y (i-n) := by
  induction n generalizing X i with
  | zero => simp [cut]
  | succ n ih =>
    cases i with
    | zero => simp [cut]
    | succ i => simp only [cut,cons_succ,ih,Nat.succ_lt_succ_iff,Nat.succ_sub_succ,tail]

/-- Independent replacements at opposite ends of a box. Its width is conserved
when viewed from the new head, even if the actual displacement is unknown. -/
theorem run (δ : Q → Bool → Option (Bool × Dir × Q)) (t : Nat) {c d : Cfg Q}
    (h : steps δ t c = some d) (a b : Nat) (ha : t ≤ a) (hb : t ≤ b) :
    ∃ u v, u+v = a+b ∧ ∀ L R,
      steps δ t (frame c a b L R) = some (frame d u v L R) := by
  induction t generalizing c a b with
  | zero =>
    simp [steps] at h; subst d; exact ⟨a,b,rfl,fun _ _ => rfl⟩
  | succ t ih =>
    obtain ⟨a,rfl⟩ := Nat.exists_eq_succ_of_ne_zero (n := a) (by omega)
    obtain ⟨b,rfl⟩ := Nat.exists_eq_succ_of_ne_zero (n := b) (by omega)
    cases act : δ c.st (c.r 0) with
    | none => simp [steps,step,act] at h
    | some p =>
      obtain ⟨w,dir,q⟩ := p
      cases dir with
      | L =>
        let c' : Cfg Q := ⟨tail c.l,cons (c.l 0) (cons w (tail c.r)),q⟩
        have one : step δ c = some c' := by simp [step,act,c']
        rw [steps_succ_of_step δ t one] at h
        obtain ⟨u,v,sz,hv⟩ := ih h a (b+2) (by omega) (by omega)
        refine ⟨u,v,by omega,fun L R => ?_⟩
        have framed : step δ (frame c (a+1) (b+1) L R) = some (frame c' a (b+2) L R) := by
          simp [frame,cut,c',step,act]
        rw [steps_succ_of_step δ t framed]; exact hv L R
      | R =>
        let c' : Cfg Q := ⟨cons w c.l,tail c.r,q⟩
        have one : step δ c = some c' := by simp [step,act,c']
        rw [steps_succ_of_step δ t one] at h
        obtain ⟨u,v,sz,hv⟩ := ih h (a+2) b (by omega) (by omega)
        refine ⟨u,v,by omega,fun L R => ?_⟩
        have framed : step δ (frame c (a+1) (b+1) L R) = some (frame c' (a+2) b L R) := by
          simp [frame,cut,c',step,act]
        rw [steps_succ_of_step δ t framed]; exact hv L R
end TM.Box
