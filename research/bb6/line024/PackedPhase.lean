import PackedTape
import SharpPhase

namespace H7846.Line24.PackedTape
open TM Word

/-- Prepend the finite word up to its last one, merging with adjacent runs. -/
def wordRuns : Word → Runs → Runs
  | .tip j, tail => push true (7+3*j) tail
  | .d a x, tail => push true (3*a) (push false 1 (wordRuns x tail))

private theorem tripleRep (n : Nat) (R : Tape) : rep (3*n) [true] R = rep n [true,true,true] R := by
  induction n with
  | zero => rfl
  | succ n ih => rw [show 3*(n+1)=3+3*n by omega,rep_add,ih]; rfl

theorem denoteWord (x : Word) (tail : Runs) : denote (wordRuns x tail) = x.above (denote tail) := by
  induction x with
  | tip j => exact denotePush true _ _
  | d a x ih =>
    change denote (push true (3*a) (push false 1 (wordRuns x tail))) = _
    rw [denotePush,denotePush,ih,tripleRep]; rfl

/-- Pack a D visit with g blank cells between the counter and the right exterior. -/
def packVisit (L : Runs) (x : Word) (g : Nat) (R : Runs) : Pack :=
  ⟨push false 1 L,push true 1 (push false 1 (wordRuns x (push false g R))),.D⟩

theorem visitDenote (L : Runs) (x : Word) (g : Nat) (R : Runs) :
    (packVisit L x g R).toCfg = visitX (denote L) [] (x.above (rep g [false] (denote R))) := by
  unfold packVisit Pack.toCfg
  rw [denotePush,denotePush,denotePush,denoteWord,denotePush]
  rfl

/-- Carry an arbitrary full right suffix across a certified sequence of passes.
Only the exact blank clearance consumed by the word is charged to the gap. -/
theorem packedSharp {x y k t} (h : SharpSeries x y k t) (L : Runs) (g : Nat) (R : Runs)
    (hg : 3*k+y.digits-x.digits ≤ g) :
    H7846.steps (t+15*k) (packVisit L x g R).toCfg =
      some (packVisit (push true (3*k) L) y (g-(3*k+y.digits-x.digits)) R).toCfg := by
  let b := 3*k+y.digits-x.digits
  have z := (sharpRun h (denote L) (rep (g-b) [false] (denote R))).2
  change H7846.steps _ (visitX (denote L) [] (x.above (rep b [false] (rep (g-b) [false] (denote R))))) = _ at z
  rw [← rep_add,show b+(g-b)=g by dsimp only [b]; omega] at z
  rw [visitDenote,visitDenote,denotePush]
  exact z
end H7846.Line24.PackedTape
