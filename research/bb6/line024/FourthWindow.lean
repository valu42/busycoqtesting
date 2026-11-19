import FourthPassage
import Box

namespace H7846.Line24.FourthWindow
open TM PackedTape
set_option maxRecDepth 1500
attribute [local irreducible] TM.steps

def span : Runs → Nat
  | [] => 0
  | (_,n)::rs => n + span rs

private theorem cutRun (b : Bool) (m n : Nat) (X Y : Tape) :
    Box.cut (m+n) (rep m [b] X) Y = rep m [b] (Box.cut n X Y) := by
  induction m with
  | zero => simp [rep]
  | succ m ih =>
    rw [Nat.succ_add, rep_succ, Box.cut, rep_succ]
    exact congrArg (cons b) ih

theorem cutRuns (rs : Runs) (n : Nat) (X Y : Tape) :
    Box.cut (span rs+n) (denoteWith rs X) Y = denoteWith rs (Box.cut n X Y) := by
  induction rs with
  | nil => simp [span,denoteWith]
  | cons h rs ih =>
    obtain ⟨b,k⟩ := h
    simp only [span, denoteWith, Nat.add_assoc, cutRun, ih]

private theorem atRunEnd (b : Bool) (m i : Nat) (X : Tape) : rep m [b] X (m+i) = X i := by
  induction m with
  | zero => simp [rep]
  | succ m ih => rw [Nat.succ_add,rep_succ]; exact ih

theorem atRunsEnd (rs : Runs) (i : Nat) (X : Tape) :
    denoteWith rs X (span rs+i) = X i := by
  induction rs with
  | nil => simp [span,denoteWith]
  | cons h rs ih =>
    obtain ⟨b,k⟩ := h
    simp only [span, denoteWith, Nat.add_assoc, atRunEnd, ih]

def mark : Tape := cons true blank

/-- A single terminal mark fixes the end of any box whose replacement by that
mark reproduces the original tape. -/
theorem fixedBoundary (rs : Runs) (v : Nat)
    (e : Box.cut v (denoteWith rs mark) mark = denoteWith rs mark) : v = span rs := by
  by_cases h : v < span rs
  · have p := congrFun e (span rs + 0)
    rw [Box.read, ite_eq_right (by omega), atRunsEnd] at p
    obtain ⟨k,hk⟩ := Nat.exists_eq_succ_of_ne_zero (n := span rs + 0 - v) (by omega)
    rw [hk] at p
    contradiction
  · obtain ⟨i,rfl⟩ := Nat.exists_eq_add_of_le (Nat.le_of_not_gt h)
    have p := congrFun e (span rs+i)
    rw [Box.read, ite_eq_right (by omega),Nat.sub_self,atRunsEnd] at p
    cases i with
    | zero => rfl
    | succ i => contradiction



def left := FourthPassage.p0.l
def before := FourthPassage.p0.r.dropLast.dropLast
def afterRuns := FourthPassage.finalPack.r.dropLast.dropLast

def source := before ++ [(false,122862607226)]
def target := afterRuns ++ [(false,122234937563)]

def model (rs : Runs) (R : Tape) : Config := ⟨denote left,denoteWith rs R,.A⟩

theorem denoteJoin (a b : Runs) (R : Tape) :
    denoteWith (a ++ b) R = denoteWith a (denoteWith b R) := by
  induction a with
  | nil => rfl
  | cons p a ih =>
    obtain ⟨bit,n⟩ := p
    exact congrArg (rep n [bit]) ih

private theorem sourceSpan : span source = 123000000000 := by decide
private theorem targetSpan : span target = 123000000048 := by decide

private theorem sentinelRun : steps 122546899564 (model source mark) =
    some (model target mark) := FourthPassage.passage

private theorem leftTrim (n : Nat) : Box.cut (span left+n) (denote left) blank = denote left := by
  unfold denote
  rw [cutRuns,Box.zeros,Box.zeroBlank]

private theorem frameModel (xs : Runs) (n : Nat) (R : Tape) :
    Box.frame (model xs mark) (span left+n) (span xs) blank R = model xs R := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  refine ⟨leftTrim n,?_,rfl⟩
  exact cutRuns xs 0 mark R

/-- All cells from coordinate 123000000000 rightwards can be replaced.
The same exterior begins 48 cells farther from the head on return. -/
theorem passage (R : Tape) : steps 122546899564 (model source R) = some (model target R) := by
  obtain ⟨u,v,size,runBox⟩ := Box.run trans _ sentinelRun
      (span left+123000000000) (span source) (by decide) (by decide)
  have marked := runBox blank mark
  rw [frameModel] at marked
  have marked := sentinelRun.symm.trans marked
  have rightEq := congrArg Cfg.r (Option.some.inj marked)
  have hv : v = span target := fixedBoundary target v rightEq.symm
  have hu : u = span left+122999999952 := by rw [hv, sourceSpan, targetSpan] at size; omega
  have real := runBox blank R
  rw [frameModel,hu,hv,frameModel] at real
  exact real

/-- A replay on precisely the three markers that influence this return. -/
theorem clipped : steps 122546899564 (model before blank) = some (model afterRuns blank) := by
  have h := passage blank
  simpa only [model,source,target,denoteJoin,denoteWith,Box.zeroBlank] using h

theorem extended (n : Nat) (R : Tape) :
    steps 122546899564 (model before (rep (122862607226+n) [false] R)) =
      some (model afterRuns (rep (122234937563+n) [false] R)) := by
  have h := passage (rep n [false] R)
  simpa only [model,source,target,denoteJoin,denoteWith,rep_add] using h

end H7846.Line24.FourthWindow
