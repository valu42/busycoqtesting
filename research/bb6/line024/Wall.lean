import PassRel

/-! Passes of BB(6) line 24 with arbitrary exterior tape.
The imported encodings and sweep theorems are by Fractal Geometry Explorer. -/
namespace H7846.Line24
set_option maxRecDepth 10000

open TM

private abbrev down (L X : Tape) : Config := ⟨L, app [true, false] X, .D⟩
private abbrev up (L X : Tape) : Config := ⟨L, rep 5 [false] X, .A⟩

/-- The inner computation returns to its original cut with any left context. -/
def Core (X Y : Tape) : Prop :=
  ∀ L, ∃ n, steps n (down L X) = some (up L Y)

/-- Put any positive digit before a returning inner computation. -/
theorem keepDigit {X Y : Tape} (h : Core X Y) (j : Nat) :
    Core (blkV (j+1) X) (blkV (j+1) Y) := by
  intro L
  have hr := d_block j L (app [true, false] X)
  obtain ⟨n₁, h₁⟩ := hr
  obtain ⟨n₂, h₂⟩ := h (blkL j L)
  obtain ⟨n₃, h₃⟩ := a_block j L (cons false Y)
  have ein := enc_visit [j] X
  change (cons true (cons false (blkV (j+1) X))) = blkR j (app [true, false] X) at ein
  unfold down
  change ∃ n, steps n ⟨L, cons true (cons false (blkV (j+1) X)), .D⟩ = some _
  rw [ein]
  exact ⟨_, steps_seq trans (steps_seq trans h₁ h₂) h₃⟩

theorem liftVisit {X Y : Tape} (h : Core X Y) (L : Tape) :
    ∃ n, steps n (visitX L [] X) = some (visitX (rep 3 [true] L) [] Y) := by
  obtain ⟨n, hn⟩ := h (cons false L)
  exact ⟨_, steps_seq trans hn (wall_turn L Y)⟩

theorem zeroTail : Core (tailT 0) (blkV 0 (tailT 0)) :=
  fun L => ⟨54, turn_T0 L⟩

theorem tail (i : Nat) : Core (tailT (i+1)) (blkV (i+1) (tailT 0)) := by
  intro L
  have a := d_head L (rep (i+2) [true,true,true] (app [true,true] blank))
  have b := cross_r trans (u := []) d_unit (i+2) (app [true,true,true,false] L) (app [true,true] blank)
  have c := tail_turn (blkL i L)
  obtain ⟨_, d⟩ := a_block 0 (blkL i L) (app [true,true,true,true] blank)
  obtain ⟨_, e⟩ := a_block i L (blkB 0 (app [true,true,true,true] blank))
  unfold down
  change ∃ n, steps n ⟨L, cons true (cons false (tailT (i+1))), .D⟩ = some _
  rw [enc_tail]
  exact ⟨_, steps_seq trans (steps_seq trans (steps_seq trans (steps_seq trans a b) c) d) e⟩

/-- A digit 2, an empty digit, and a digit 1 expose the suffix to a fresh sweep. -/
private theorem enterTwo (L X : Tape) :
    steps 28 (down L (sq blkV [2,0,1] X)) =
      some (down (app [true,true,false,true,true,true,false,true,true,true,true,false] L) X) := rfl

/-- The return crosses the temporary four-one block and restores the empty digit. -/
private theorem leaveTwo (L Y : Tape) :
    steps 36 (up (app [true,true,false,true,true,true,false,true,true,true,true,false] L) Y) =
      some (up L (sq blkV [0,1,2] Y)) := rfl

theorem bounceTwo {X Y : Tape} (h : Core X Y) :
    Core (sq blkV [2,0,1] X) (sq blkV [0,1,2] Y) := by
  intro L
  obtain ⟨n, hn⟩ := h _
  exact ⟨_, steps_seq trans (steps_seq trans (enterTwo L X) hn) (leaveTwo L Y)⟩


private theorem enterDigit (j : Nat) (L X : Tape) :
    ∃ n, steps n (down L (blkV (j+1) X)) = some (down (blkL j L) X) := by
  have e := enc_visit [j] X
  change cons true (cons false (blkV (j+1) X)) = blkR j (app [true,false] X) at e
  change ∃ n, steps n ⟨L, cons true (cons false (blkV (j+1) X)), .D⟩ = _
  rw [e]
  exact d_block j L _

private theorem rewind (js : List Nat) (L X : Tape) :
    ∃ n, steps n (up (sqr blkL js L) X) =
      some (up L (sq blkV (js.map (·+1)) X)) := by
  obtain ⟨n,h⟩ := lsweep js L (cons false X)
  rw [enc_back0] at h
  exact ⟨n,h⟩

theorem splitEnd (m : Nat) :
    Core (sq blkV [m+2,0] (tailT 0)) (sq blkV [m,1,1] (tailT 0)) := by
  intro L
  obtain ⟨_, a⟩ := enterDigit (m+1) L (cons false (tailT 0))
  cases m with
  | zero => exact ⟨_, steps_seq trans a (turn_split2 L)⟩
  | succ j =>
    have b := turn_split (blkL j L)
    obtain ⟨_,c⟩ := rewind [j,0,0] L (tailT 0)
    exact ⟨_, steps_seq trans (steps_seq trans a b) c⟩

theorem joinRun (i : Nat) (X : Tape) :
    Core (sq blkV [i+1,1,0] X) (rep (i+2) [true,true,true] X) := by
  intro L
  obtain ⟨_,a⟩ := enterDigit i L (sq blkV [1,0] X)
  obtain ⟨_,b⟩ := enterDigit 0 (blkL i L) (cons false X)
  have c := turn_empty (blkL i L) X
  obtain ⟨_,d⟩ := a_block i L (app [true,true,true] X)
  have h := steps_seq trans (steps_seq trans (steps_seq trans a b) c) d
  change steps _ _ = some (up L (rep (i+1) [true,true,true] (app [true,true,true] X))) at h
  rw [rep_app_comm] at h
  exact ⟨_,h⟩

theorem bounce (m : Nat) {X Y : Tape} (h : Core X Y) :
    Core (sq blkV [m+2,0,1] X) (sq blkV [m,1,2] Y) := by
  cases m with
  | zero => exact bounceTwo h
  | succ j =>
    intro L
    obtain ⟨_,a⟩ := enterDigit (j+2) L (sq blkV [0,1] X)
    have b := bounce_turn (blkL j L) X
    obtain ⟨_,c⟩ := h (sqr blkL [j,0,1] L)
    obtain ⟨_,d⟩ := rewind [j,0,1] L Y
    exact ⟨_, steps_seq trans (steps_seq trans (steps_seq trans a b) c) d⟩

/-- The first two digits are 1,0. The next run of ones determines the exit. -/
theorem wallOneZero (L X : Tape) :
    steps 26 (visitX L [1,0] X) =
      some ⟨rep 3 [true] L, rep 5 [true] X, .D⟩ := rfl

private theorem reframe (k : Nat) (R : Tape) :
    rep 5 [true] (blkV k R) = rep (k+1) [true,true,true] (app [true,true,false] R) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    change app [true,true,true] (rep 5 [true] (blkV k R)) = _
    rw [ih]; rfl

/-- Crossing the following digit k makes a new wall visit, even for k = 0. -/
theorem wallNextDigit (k : Nat) (L R : Tape) :
    steps (26 + (k+1)*3 + 3) (visitX L [1,0] (blkV k R)) =
      some (visitX (rep (k+1) [true,true,false] (rep 3 [true] L)) [] R) := by
  have h := wallOneZero L (blkV k R)
  rw [reframe] at h
  have h' := cross_r trans (u := []) d_unit (k+1) (rep 3 [true] L) (app [true,true,false] R)
  have finish (P : Tape) : steps 3 ⟨P, app [true,true,false] R, .D⟩ =
      some (visitX P [] R) := rfl
  exact steps_seq trans (steps_seq trans h h') (finish _)

private theorem reframeTail (j : Nat) (R : Tape) :
    rep 5 [true] (rep (7+3*j) [true] R) = rep (j+4) [true,true,true] R := by
  induction j with
  | zero => rfl
  | succ j ih =>
    rw [show 7+3*(j+1) = (7+3*j)+3 by omega]
    change app [true,true,true] (rep 5 [true] (rep (7+3*j) [true] R)) = _
    rw [ih]; rfl

/-- At a tail, D scans the very first cell of the exterior tape. -/
theorem wallTail (j : Nat) (L R : Tape) :
    steps (26 + (j+4)*3) (visitX L [1,0] (rep (7+3*j) [true] R)) =
      some ⟨rep (j+4) [true,true,false] (rep 3 [true] L), R, .D⟩ := by
  have h := wallOneZero L (rep (7+3*j) [true] R)
  rw [reframeTail] at h
  exact steps_seq trans h (cross_r trans (u := []) d_unit (j+4) _ R)

/-- A tail followed by 001 reaches B1, for every left and right exterior. -/
theorem wallTailHalt (j : Nat) (L R : Tape) :
    ∃ c, steps (26 + (j+4)*3 + 2)
      (visitX L [1,0] (rep (7+3*j) [true] (app [false,false,true] R))) =
        some c ∧ step c = none := by
  have h := wallTail j L (app [false,false,true] R)
  have finish (P : Tape) : steps 2 ⟨P, app [false,false,true] R, .D⟩ =
      some ⟨app [true,false] P, cons true R, .B⟩ := rfl
  exact ⟨_, steps_seq trans h (finish _), rfl⟩

private def faceLeft (L R : Tape) : Config := ⟨TM.tail L, cons (L 0) R, .A⟩

private theorem erase (w : Nat) (L R : Tape) :
    steps w (faceLeft (rep w [true] L) R) = some (faceLeft L (rep w [false] R)) := by
  induction w generalizing R with
  | zero => rfl
  | succ w ih =>
    have first : steps 1 (faceLeft (rep (w+1) [true] L) R) =
        some (faceLeft (rep w [true] L) (cons false R)) := rfl
    have h := steps_seq trans first (ih (cons false R))
    rw [Nat.add_comm 1 w] at h
    rw [← rep_app_comm w [false] R]
    exact h

/-- A leading empty digit erases a wall of w+1 ones. -/
theorem emptyWall (w : Nat) (L R : Tape) :
    steps (7+w) (visitX (rep (w+1) [true] (cons false L)) [0] R) =
      some ⟨L, rep (w+2) [false] (rep 4 [true] R), .A⟩ := by
  have h : steps 7 (visitX (rep (w+1) [true] (cons false L)) [0] R) =
      some (faceLeft (rep w [true] (cons false L)) (cons false (rep 4 [true] R))) := rfl
  have h' := steps_seq trans h (erase w (cons false L) (cons false (rep 4 [true] R)))
  rw [show rep w [false] (cons false (rep 4 [true] R)) =
        rep (w+1) [false] (rep 4 [true] R) from rep_app_comm w [false] _] at h'
  exact h'

/-- A separator and a previous wall, nearest cell first. Actual wall width is m+2. -/
def oldWall (m : Nat) (L : Tape) := app [true,true,false] (rep (m+2) [true] (cons false L))

/-- Crossing a previous wall leaves six ones behind it. -/
theorem oldWallStep (m : Nat) (L R : Tape) :
    steps (20+(m+2)) ⟨oldWall m L, rep 4 [false] R, .A⟩ =
      some ⟨L, rep 4 [false] (rep m [false] (rep 6 [true] R)), .A⟩ := by
  have enter (P : Tape) : steps 20 ⟨app [true,true,false] P, rep 4 [false] R, .A⟩ =
      some (faceLeft P (cons false (rep 6 [true] R))) := rfl
  have h := steps_seq trans (enter (rep (m+2) [true] (cons false L)))
    (erase (m+2) (cons false L) (cons false (rep 6 [true] R)))
  rw [show rep (m+2) [false] (cons false (rep 6 [true] R)) =
        rep (m+3) [false] (rep 6 [true] R) from rep_app_comm (m+2) [false] _] at h
  exact h

def markers (widths : List Nat) (R : Tape) : Tape :=
  widths.foldl (fun X m => rep m [false] (rep 6 [true] X)) R

/-- Arbitrarily many older walls, in order from the head outwards. -/
theorem eraseWalls (widths : List Nat) (L R : Tape) :
    steps ((widths.map (fun m => 22+m)).sum)
      ⟨sq oldWall widths L, rep 4 [false] R, .A⟩ =
      some ⟨L, rep 4 [false] (markers widths R), .A⟩ := by
  induction widths generalizing R with
  | nil => rfl
  | cons w ws ih =>
    have h := steps_seq trans (oldWallStep w (sq oldWall ws L) R)
      (ih (rep w [false] (rep 6 [true] R)))
    rw [show 20+(w+2) = 22+w by omega] at h
    exact h

end H7846.Line24
