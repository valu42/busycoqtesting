import Timing
import Box

namespace H7846.Line24
open TM Word

private theorem uncut (n : Nat) (X : Tape) : Box.cut n X (fun i => X (n+i)) = X := by
  funext i
  rw [Box.read]
  split
  · rfl
  · congr 1; omega

private theorem cutUnique (a b : Nat) (X : Tape)
    (h : ∀ U, Box.cut a X U = Box.cut b X U) : a=b := by
  have impossible (i : Nat) (e : (!X i) = X i) : False := by
    cases v : X i <;> simp [v] at e
  by_cases lt : a < b
  · have z := congrFun (h (fun _ => !X a)) a
    rw [Box.read,Box.read,ite_eq_right (by omega),ite_eq_left lt] at z
    exact (impossible a z).elim
  · by_cases ne : a=b
    · exact ne
    have lt' : b<a := by omega
    have z := congrFun (h (fun _ => !X b)) b
    rw [Box.read,Box.read,ite_eq_left lt',ite_eq_right (by omega)] at z
    exact (impossible b z.symm).elim

/-- A timed core returns to the original cut, even with arbitrary data at distance g.
Parametricity in the left tape fixes both endpoints of the moving box. -/
theorem guardedTimed {X Y t} (h : Timed X Y t) (g : Nat) (hg : t ≤ g) (L R : Tape) :
    steps t ⟨L, Box.cut g (app [true,false] X) R,.D⟩ =
      some ⟨L,Box.cut g (rep 5 [false] Y) R,.A⟩ := by
  let A := app [true,false] X
  obtain ⟨u,v,sum,all⟩ := Box.run trans t (h L) t g (by omega) hg
  have same (U : Tape) : Box.cut t L U = Box.cut u L U := by
    have z := all U (fun i => A (g+i))
    change steps t ⟨Box.cut t L U,Box.cut g A (fun i => A (g+i)),.D⟩ = _ at z
    rw [uncut] at z
    have c := (h (Box.cut t L U)).symm.trans z
    exact congrArg Cfg.l (Option.some.inj c)
  have hu := cutUnique t u L same
  have hv : v=g := by omega
  subst u; subst v
  have z := all (fun i => L (t+i)) R
  change steps t ⟨Box.cut t L (fun i => L (t+i)),_,.D⟩ =
    some ⟨Box.cut t L (fun i => L (t+i)),_,.A⟩ at z
  rwa [uncut] at z

/-- A counter visit viewed up to the chosen cut, with an arbitrary exterior R. -/
def guardedVisit (L : Tape) (x : Word) (g : Nat) (R : Tape) : Config :=
  ⟨cons false L,Box.cut g (app [true,false] x.tape) R,.D⟩

private theorem guardedSingle {x y : Word} {t : Nat} (h : Timed x.tape y.tape t) (g : Nat)
    (hg : t+15 ≤ g) (L R : Tape) :
    steps (t+15) (guardedVisit L x g R) =
      some (guardedVisit (rep 3 [true] L) y (g-3) R) := by
  have hcore := guardedTimed h g (by omega) (cons false L) R
  let tail := Box.cut (g-5) y.tape R
  have c : Box.cut g (rep 5 [false] y.tape) R = rep 5 [false] tail := by
    have z := Box.front [false,false,false,false,false] (g-5) y.tape R
    change Box.cut (5+(g-5)) _ _ = _ at z
    rwa [show 5+(g-5)=g by omega] at z
  rw [c] at hcore
  have z := steps_seq trans hcore (wall_turn L tail)
  have e : Box.cut (g-3) (app [true,false] y.tape) R = app [true,false] tail := by
    have a := Box.front [true,false] (g-5) y.tape R
    change Box.cut (2+(g-5)) _ _ = _ at a
    rwa [show 2+(g-5)=g-3 by omega] at a
  unfold guardedVisit
  rw [e]
  exact z

/-- Every member pass has cost plus its head offset bounded by r. -/
inductive GuardSeries : Word → Word → Nat → Nat → Nat → Prop where
  | nil (x : Word) (r : Nat) : GuardSeries x x 0 0 r
  | snoc {x y z k t s r} : GuardSeries x y k t r → Timed y.tape z.tape s →
      3*k+s+15 ≤ r → GuardSeries x z (k+1) (t+s) r

theorem guardAtom {x y t} (h : Atom x y t) : GuardSeries x y 1 t (t+15) := by
  simpa using GuardSeries.snoc (GuardSeries.nil x (t+15)) (atomSound h) (by omega)

private theorem weaken {x y k t r} (h : GuardSeries x y k t r) {u : Nat} (hu : r ≤ u) :
    GuardSeries x y k t u := by
  induction h with
  | nil => exact .nil _ _
  | snoc _ s b ih => exact .snoc (ih hu) s (by omega)

theorem guardFrame (j : Nat) {x y k t r} (h : GuardSeries x y k t r) :
    GuardSeries (.d (j+1) x) (.d (j+1) y) k (t+k*(14*(j+1)+4)) (r+(14*(j+1)+4)) := by
  induction h with
  | nil => simp; exact .nil _ _
  | @snoc y z k t s r _ step bound ih =>
    have z := GuardSeries.snoc (z := .d (j+1) z) ih (timedKeep j step) (by omega)
    rw [Nat.succ_mul]
    rw [show t+s+(k*(14*(j+1)+4)+(14*(j+1)+4)) = t+k*(14*(j+1)+4)+(s+(14*(j+1)+4)) by omega]
    exact z

private theorem appendBound {x y z k t p s r u v}
    (a : GuardSeries x y k t r) (b : GuardSeries y z p s u) (ha : r ≤ v) (hb : 3*k+u ≤ v) :
    GuardSeries x z (k+p) (t+s) v := by
  induction b with
  | nil => exact weaken a ha
  | snoc _ step bound ih =>
    have z := GuardSeries.snoc (ih hb) step (by omega)
    simpa [Nat.add_assoc] using z

theorem guardConcat {x y z k t p s r u} (a : GuardSeries x y k t r) (b : GuardSeries y z p s u) :
    GuardSeries x z (k+p) (t+s) (max r (3*k+u)) := appendBound a b (by omega) (by omega)

theorem guardRun {x y k t r} (h : GuardSeries x y k t r) (g : Nat) (hg : r ≤ g) (L R : Tape) :
    steps (t+15*k) (guardedVisit L x g R) =
      some (guardedVisit (rep (3*k) [true] L) y (g-3*k) R) := by
  induction h with
  | nil => rfl
  | @snoc y z k t s r _ step bound ih =>
    have a := ih hg
    have b := guardedSingle step (g-3*k) (by omega) (rep (3*k) [true] L) R
    have both := steps_seq trans a b
    rw [show t+15*k+(s+15) = t+s+15*(k+1) by omega,
      show g-3*k-3=g-3*(k+1) by omega,← rep_add,show 3+3*k=3*(k+1) by omega] at both
    exact both

end H7846.Line24
