import Counter

namespace H7846.Line24
open TM Word

def Timed (X Y : Tape) (n : Nat) := ∀ L, steps n ⟨L, app [true,false] X, .D⟩ =
  some ⟨L, rep 5 [false] Y, .A⟩

private theorem timeEq {n m : Nat} {c d : Config} (h : steps n c = some d) (e : n=m) :
    steps m c = some d := e ▸ h

private theorem rightCost (j : Nat) (L X : Tape) :
    steps (6+j*3) ⟨L,app [true,false] (blkV (j+1) X),.D⟩ =
      some ⟨blkL j L,app [true,false] X,.D⟩ := by
  have e := enc_visit [j] X
  change cons true (cons false (blkV (j+1) X)) = blkR j (app [true,false] X) at e
  change steps _ ⟨L,cons true (cons false (blkV (j+1) X)),.D⟩ = _
  rw [e]
  exact steps_seq trans (d_head L _) (cross_r trans (u := []) d_unit j _ _)

private theorem leftCost (j : Nat) (L R : Tape) :
    steps (j*11+12) ⟨blkL j L,rep 4 [false] R,.A⟩ =
      some ⟨L,rep 4 [false] (blkB j R),.A⟩ :=
  steps_seq trans (cross_l trans a_unit j (app [true,true,true,false] L) R)
    (a_head L (rep j [true,true,true] R))

theorem timedKeep (j : Nat) {X Y t} (h : Timed X Y t) :
    Timed (blkV (j+1) X) (blkV (j+1) Y) (t+(14*(j+1)+4)) := by
  intro L
  have a := steps_seq trans (steps_seq trans (rightCost j L X) (h _)) (leftCost j L (cons false Y))
  rw [show 6+j*3+t+(j*11+12) = t+(14*(j+1)+4) by omega] at a
  exact a

theorem timedTail (j : Nat) : Timed (tailT j) (blkV j (tailT 0)) (14*j+54) := by
  cases j with
  | zero => exact fun L => turn_T0 L
  | succ i =>
    intro L
    have a := d_head L (rep (i+2) [true,true,true] (app [true,true] blank))
    have b := cross_r trans (u := []) d_unit (i+2) (app [true,true,true,false] L) (app [true,true] blank)
    have c := tail_turn (blkL i L)
    have d := leftCost 0 (blkL i L) (app [true,true,true,true] blank)
    have e := leftCost i L (blkB 0 (app [true,true,true,true] blank))
    have h := steps_seq trans (steps_seq trans (steps_seq trans (steps_seq trans a b) c) d) e
    change steps _ ⟨L,cons true (cons false (tailT (i+1))),.D⟩ = _
    rw [enc_tail]
    exact timeEq h (by omega)

theorem timedSplit (m : Nat) :
    Timed (sq blkV [m+2,0] (tailT 0)) (sq blkV [m,1,1] (tailT 0)) (14*(m+2)+72) := by
  intro L
  have a := rightCost (m+1) L (cons false (tailT 0))
  cases m with
  | zero => exact timeEq (steps_seq trans a (turn_split2 L)) (by decide)
  | succ j =>
    have b := turn_split (blkL j L)
    have c := leftCost 0 (blkL 0 (blkL j L)) (cons false (tailT 0))
    have d := leftCost 0 (blkL j L) (blkB 0 (cons false (tailT 0)))
    have e := leftCost j L (blkB 0 (blkB 0 (cons false (tailT 0))))
    have h := steps_seq trans (steps_seq trans (steps_seq trans (steps_seq trans a b) c) d) e
    exact timeEq h (by omega)

theorem timedJoin (i : Nat) (X : Tape) :
    Timed (sq blkV [i+1,1,0] X) (rep (i+2) [true,true,true] X) (14*(i+1)+18) := by
  intro L
  have a := rightCost i L (sq blkV [1,0] X)
  have b := rightCost 0 (blkL i L) (cons false X)
  have c := turn_empty (blkL i L) X
  have d := leftCost i L (app [true,true,true] X)
  have h := steps_seq trans (steps_seq trans (steps_seq trans a b) c) d
  change steps _ _ = some ⟨L, rep 5 [false] (rep (i+1) [true,true,true] (app [true,true,true] X)), .A⟩ at h
  rw [rep_app_comm] at h
  exact timeEq h (by omega)

theorem timedBounce (m : Nat) {X Y t} (inner : Timed X Y t) :
    Timed (sq blkV [m+2,0,1] X) (sq blkV [m,1,2] Y) (t+14*(m+2)+36) := by
  intro L
  cases m with
  | zero =>
    have a : steps 28 ⟨L,app [true,false] (sq blkV [2,0,1] X),.D⟩ =
        some ⟨app [true,true,false,true,true,true,false,true,true,true,true,false] L,app [true,false] X,.D⟩ := rfl
    have b : steps 36 ⟨app [true,true,false,true,true,true,false,true,true,true,true,false] L,rep 5 [false] Y,.A⟩ =
        some ⟨L,rep 5 [false] (sq blkV [0,1,2] Y),.A⟩ := by set_option maxRecDepth 10000 in rfl
    have h := steps_seq trans (steps_seq trans a (inner _)) b
    exact timeEq h (by omega)
  | succ j =>
    have a := rightCost (j+2) L (sq blkV [0,1] X)
    have b := bounce_turn (blkL j L) X
    have z := inner (blkL 1 (blkL 0 (blkL j L)))
    have c := leftCost 1 (blkL 0 (blkL j L)) (cons false Y)
    have d := leftCost 0 (blkL j L) (blkB 1 (cons false Y))
    have e := leftCost j L (blkB 0 (blkB 1 (cons false Y)))
    have h := steps_seq trans (steps_seq trans (steps_seq trans (steps_seq trans (steps_seq trans a b) z) c) d) e
    exact timeEq h (by omega)

/-- A sequence of core sweeps, with the number of passes and the sum of their core costs. -/
inductive Series : Word → Word → Nat → Nat → Prop where
  | nil (x) : Series x x 0 0
  | snoc {x y z k t s} : Series x y k t → Timed y.tape z.tape s → Series x z (k+1) (t+s)

theorem single {x y : Word} {t} (h : Timed x.tape y.tape t) : Series x y 1 t := by
  simpa using Series.snoc (Series.nil x) h

/-- Word-level certificates keep concrete tape reductions out of proof search. -/
inductive Atom : Word → Word → Nat → Prop
  | tip (j) : Atom (.tip j) (.d j (.tip 0)) (14*j+54)
  | keep (j) {x y t} : Atom x y t → Atom (.d (j+1) x) (.d (j+1) y) (t+(14*(j+1)+4))
  | split (m) : Atom (.d (m+2) (.d 0 (.tip 0))) (.d m (.d 1 (.d 1 (.tip 0)))) (14*(m+2)+72)
  | mergeTail (i) : Atom (.d (i+1) (.d 1 (.d 0 (.tip 0)))) (.tip (i+2)) (14*(i+1)+18)
  | mergeDigit (i) (y) : Atom (.d (i+1) (.d 1 (.d 0 (.d 1 y)))) (.d (i+3) y) (14*(i+1)+18)
  | carry (m) {x y t} : Atom x y t → Atom (.d (m+2) (.d 0 (.d 1 x)))
      (.d m (.d 1 (.d 2 y))) (t+14*(m+2)+36)

theorem atomSound {x y t} (h : Atom x y t) : Timed x.tape y.tape t := by
  induction h with
  | tip j => exact timedTail j
  | keep j _ ih => exact timedKeep j ih
  | split m => exact timedSplit m
  | mergeTail i =>
    change Timed _ (tailT (i+2)) _
    rw [← Word.joinTailTape]
    exact timedJoin i (tailT 0)
  | mergeDigit i y =>
    have a := timedJoin i (blkV 1 y.tape)
    change Timed _ (rep (i+2) [true,true,true] (app [true,true,true] (cons false y.tape))) _ at a
    rw [rep_app_comm] at a
    exact a
  | carry m _ ih => exact timedBounce m ih

theorem atomSeries {x y t} (h : Atom x y t) : Series x y 1 t :=
  single (atomSound h)

theorem concat {x y z k₁ t₁ k₂ t₂} (a : Series x y k₁ t₁) (b : Series y z k₂ t₂) :
    Series x z (k₁+k₂) (t₁+t₂) := by
  induction b with
  | nil => exact a
  | snoc _ h ih => simpa [Nat.add_assoc] using Series.snoc ih h

theorem frame (j : Nat) {x y k t} (h : Series x y k t) :
    Series (.d (j+1) x) (.d (j+1) y) k (t+k*(14*(j+1)+4)) := by
  induction h with
  | nil => simp; exact Series.nil _
  | @snoc y z k t s _ step ih =>
    have joined := Series.snoc (z := .d (j+1) z) ih (timedKeep j step)
    rw [Nat.succ_mul]
    rw [show t+s+(k*(14*(j+1)+4)+(14*(j+1)+4)) = t+k*(14*(j+1)+4)+(s+(14*(j+1)+4)) by omega]
    exact joined

theorem runSeries {x y k t} (h : Series x y k t) (L : Tape) :
    steps (t+15*k) (visitX L [] x.tape) = some (visitX (rep (3*k) [true] L) [] y.tape) := by
  induction h with
  | nil => rfl
  | @snoc y z k t s _ step ih =>
    have a := step (cons false (rep (3*k) [true] L))
    have b := wall_turn (rep (3*k) [true] L) z.tape
    have f := steps_seq trans (steps_seq trans ih a) b
    rw [show t+15*k+s+15 = t+s+15*(k+1) by omega] at f
    rw [show 3*(k+1)=3*k+3 by omega]
    exact f

end H7846.Line24
