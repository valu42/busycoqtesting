import CollisionRules

namespace H7846.Line24
open TM Word
set_option maxRecDepth 25000

/-- Encode a counter word up to its last one, and append an arbitrary exterior. -/
def Word.above : Word → Tape → Tape
  | .tip j, R => rep (7+3*j) [true] R
  | .d n x, R => blkV n (x.above R)

private theorem openTip (j : Nat) (R : Tape) :
    Timed ((Word.tip j).above (rep 4 [false] R)) ((Word.d j (.tip 0)).above R) (14*j+54) :=
  extendTail (t := 54) (by intro L; rfl) (by intro L; rfl) (by decide) j

private theorem joinOpen (i : Nat) (R : Tape) :
    rep (i+2) [true,true,true] ((Word.tip 0).above R) = (Word.tip (i+2)).above R := by
  induction i with
  | zero => rfl
  | succ i ih =>
    change rep (i+1+2) [true,true,true] _ = rep (7+3*(i+1+2)) [true] _
    rw [show 7+3*(i+1+2) = 7+3*(i+2)+3 by omega]
    exact congrArg (app [true,true,true]) ih

/-- A single ordinary atom uses exactly four or zero blank cells following
the original word. The entire more distant stream is arbitrary. -/
theorem atomClearance {x y t} (h : Atom x y t) :
    ∃ b, (b=0 ∨ b=4) ∧ x.digits+b = 3+y.digits ∧
      ∀ R, Timed (x.above (rep b [false] R)) (y.above R) t := by
  induction h with
  | tip j => exact ⟨4,Or.inr rfl,by simp [digits],openTip j⟩
  | keep j _ ih =>
    obtain ⟨b,small,len,h⟩ := ih
    exact ⟨b,small,by simp only [digits]; omega,fun R => timedKeep j (h R)⟩
  | split m =>
    refine ⟨4,Or.inr rfl,by simp [digits],fun R => ?_⟩
    have h := timedSplitSuffix m (openTip 1 R)
    exact h
  | mergeTail i =>
    refine ⟨0,Or.inl rfl,by simp [digits],fun R => ?_⟩
    have a := timedJoin i ((Word.tip 0).above R)
    rw [joinOpen] at a
    exact a
  | mergeDigit i y =>
    refine ⟨0,Or.inl rfl,by simp [digits]; omega,fun R => ?_⟩
    have a := timedJoin i (blkV 1 (y.above R))
    change Timed _ (rep (i+2) [true,true,true] (app [true,true,true] (cons false (y.above R)))) _ at a
    rw [rep_app_comm] at a
    exact a
  | carry m _ ih =>
    obtain ⟨b,small,len,h⟩ := ih
    exact ⟨b,small,by simp only [digits]; omega,fun R => timedBounce m (h R)⟩

/-- A sequence retaining its ordinary atom witnesses, so its rightward reach
can be inferred from its endpoints. -/
inductive SharpSeries : Word → Word → Nat → Nat → Prop where
  | nil (x : Word) : SharpSeries x x 0 0
  | snoc {x y z k t u} : SharpSeries x y k t → Atom y z u →
      SharpSeries x z (k+1) (t+u)

theorem sharpAtom {x y t} (h : Atom x y t) : SharpSeries x y 1 t := by
  simpa using SharpSeries.snoc (SharpSeries.nil x) h

theorem sharpConcat {x y z k t m u} (a : SharpSeries x y k t) (b : SharpSeries y z m u) :
    SharpSeries x z (k+m) (t+u) := by
  induction b with
  | nil => exact a
  | snoc _ h ih => simpa [Nat.add_assoc] using SharpSeries.snoc ih h

theorem sharpFrame (d : Nat) {x y k t} (a : SharpSeries x y k t) :
    SharpSeries (.d (d+1) x) (.d (d+1) y) k (t+k*(14*(d+1)+4)) := by
  induction a with
  | nil => simp; exact .nil _
  | @snoc y z k t s _ h ih =>
    have u := SharpSeries.snoc ih (Atom.keep d h)
    rw [Nat.succ_mul]
    rw [show t+s+(k*(14*(d+1)+4)+(14*(d+1)+4)) =
        (t+k*(14*(d+1)+4))+(s+(14*(d+1)+4)) by omega]
    exact u

private theorem sharpSound {x y k t} (h : SharpSeries x y k t) :
    ∃ b, b % 4 = 0 ∧ x.digits+b = 3*k+y.digits ∧ ∀ L R,
      steps (t+15*k) (visitX L [] (x.above (rep b [false] R))) =
        some (visitX (rep (3*k) [true] L) [] (y.above R)) := by
  induction h with
  | nil => exact ⟨0,rfl,by omega,fun _ _ => rfl⟩
  | @snoc y z k t s _ atom ih =>
    obtain ⟨a,ha,lenA,first⟩ := ih
    obtain ⟨b,hb,lenB,second⟩ := atomClearance atom
    refine ⟨a+b,by rcases hb with rfl|rfl <;> omega,by omega,?_⟩
    intro L R
    rw [rep_add a b]
    have p := first L (rep b [false] R)
    have q := (second R) (cons false (rep (3*k) [true] L))
    have full := steps_seq trans (steps_seq trans p q) (wall_turn (rep (3*k) [true] L) (z.above R))
    change steps (t+15*k+s+15) (visitX L [] (x.above (rep a [false] (rep b [false] R)))) =
      some (visitX (rep 3 [true] (rep (3*k) [true] L)) [] (z.above R)) at full
    rw [← rep_add 3 (3*k)] at full
    rw [show 3+(3*k) = 3*(k+1) by omega,
        show t+15*k+s+15 = t+s+15*(k+1) by omega] at full
    exact full

/-- Exact cumulative clearance. Additional blanks or any other right suffix
are carried through verbatim and no bound on total running time is needed. -/
theorem sharpRun {x y k t} (h : SharpSeries x y k t) (L R : Tape) :
    let b := 3*k + y.digits - x.digits
    b % 4 = 0 ∧ steps (t+15*k) (visitX L [] (x.above (rep b [false] R))) =
      some (visitX (rep (3*k) [true] L) [] (y.above R)) := by
  obtain ⟨b,res,len,run⟩ := sharpSound h
  have eq : 3*k+y.digits-x.digits=b := by omega
  dsimp only
  rw [eq]
  exact ⟨res,run L R⟩

#print axioms sharpRun
end H7846.Line24
