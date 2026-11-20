import StackReturn

namespace H7846.Line24
open TM Word

/-- A digit opening can leave a bare wall, or a wall after the separator 110. -/
inductive Layer where
  | bare : Nat → Layer
  | older : Nat → Layer
  deriving DecidableEq, Repr

def Layer.gap : Layer → Nat
  | .bare m | .older m => m

def Layer.left : Layer → Tape → Tape
  | .bare m, L => rep (m+2) [true] (cons false L)
  | .older m, L => oldWall m L

def Layer.mark : Layer → Tape → Tape
  | .bare m, R => rep m [false] (rep 3 [true] R)
  | .older m, R => rep m [false] (rep 6 [true] R)

def Layer.time : Layer → Nat
  | .bare m => 11+m
  | .older m => 22+m

theorem Layer.erase (w : Layer) (L R : Tape) :
    steps w.time ⟨w.left L,rep 4 [false] R,.A⟩ =
    some ⟨L,rep 4 [false] (w.mark R),.A⟩ := by
  cases w with
  | older m =>
    have h := oldWallStep m L R
    rw [show 20+(m+2)=22+m by omega] at h
    exact h
  | bare m =>
    let S := cons false (rep 3 [true] R)
    have enter (P : Tape) : steps 9 ⟨cons true P,rep 4 [false] R,.A⟩ =
        some ⟨P,cons true S,.A⟩ := rfl
    have unit (P Q : Tape) : steps 1 ⟨app [true] P,app [true] Q,.A⟩ =
        some ⟨P,app [true] (app [false] Q),.A⟩ := rfl
    have sweep := cross_l trans unit (m+1) (cons false L) S
    have finish : steps 1 ⟨cons false L,cons true (rep (m+1) [false] S),.A⟩ =
        some ⟨L,rep 2 [false] (rep (m+1) [false] S),.A⟩ := rfl
    have h := steps_seq trans (steps_seq trans (enter _) sweep) finish
    have right : rep 2 [false] (rep (m+1) [false] S) =
        rep 4 [false] (rep m [false] (rep 3 [true] R)) := by
      unfold S
      rw [show cons false (rep 3 [true] R) = app [false] (rep 3 [true] R) by rfl,
          rep_app_comm,← rep_add,← rep_add]
      congr 1 <;> omega
    rw [right,show 9+(m+1)*1+1=11+m by omega] at h
    exact h

/-- Pack pairs of 110s as zero-gap older walls. The final unmatched 110, when
present, changes the last wall from bare to older. -/
def packLayers : Nat → Nat → List Layer → List Layer
  | 0, m, ws => .bare m :: ws
  | 1, m, ws => .older m :: ws
  | n+2, m, ws => .older 0 :: packLayers n m ws

theorem packTape (n m : Nat) (ws : List Layer) (L : Tape) :
    sq Layer.left (packLayers n m ws) L =
    rep n [true,true,false] (rep (m+2) [true] (cons false (sq Layer.left ws L))) := by
  match n with
  | 0 => rfl
  | 1 => rfl
  | n+2 =>
    change app [true,true,false,true,true,false] (sq Layer.left (packLayers n m ws) L) = _
    rw [packTape n m ws L]; rfl

def mixedBase (w : Nat) (ws : List Layer) (L : Tape) :=
  rep w [true] (cons false (sq Layer.left ws L))

/-- This opening rule handles every following digit k, even or odd. -/
theorem openMixed (k w : Nat) (ws : List Layer) (L R : Tape) :
    steps (26+(k+1)*3+3) (visitX (mixedBase w ws L) [1,0] (blkV k R)) =
      some (visitX (mixedBase 2 (packLayers k (w+1) ws) L) [] R) := by
  have h := wallNextDigit k (mixedBase w ws L) R
  have eq : rep (k+1) [true,true,false] (rep 3 [true] (mixedBase w ws L)) =
      mixedBase 2 (packLayers k (w+1) ws) L := by
    unfold mixedBase
    rw [packTape,← rep_add 3 w,show 3+w=w+1+2 by omega]; rfl
  rwa [eq] at h

def laidMarkers (ws : List Layer) (R : Tape) := ws.foldl (fun X w => w.mark X) R

theorem eraseMixed (ws : List Layer) (L R : Tape) :
    steps (ws.map Layer.time).sum ⟨sq Layer.left ws L,rep 4 [false] R,.A⟩ =
      some ⟨L,rep 4 [false] (laidMarkers ws R),.A⟩ := by
  induction ws generalizing R with
  | nil => rfl
  | cons w ws ih => exact steps_seq trans (w.erase _ R) (ih (w.mark R))

/-- A leading zero digit clears a wall of width w+3 and every older layer.
The final four ones fuse with whatever word or tape was left at the right. -/
theorem emptyMixed (w : Nat) (ws : List Layer) (L R : Tape) :
    steps ((w+9)+(ws.map Layer.time).sum) (visitX (mixedBase (w+3) ws L) [0] R) =
      some ⟨L,rep 4 [false] (laidMarkers ws (rep w [false] (rep 4 [true] R))),.A⟩ := by
  have a := emptyWall (w+2) (sq Layer.left ws L) R
  have b := eraseMixed ws L (rep w [false] (rep 4 [true] R))
  rw [← rep_add 4 w,show 4+w=w+2+2 by omega] at b
  have h := steps_seq trans a b
  rw [show 7+(w+2)=w+9 by omega] at h
  exact h

theorem alignedPack (k m : Nat) (ws : List Layer) (hm : m%3=0)
    (hs : ∀ z ∈ ws, z.gap%3=0) : ∀ z ∈ packLayers k m ws, z.gap%3=0 := by
  match k with
  | 0 => intro z h; rcases List.mem_cons.mp h with rfl | h; exact hm; exact hs _ h
  | 1 => intro z h; rcases List.mem_cons.mp h with rfl | h; exact hm; exact hs _ h
  | k+2 =>
    intro z h
    rcases List.mem_cons.mp h with rfl | h
    · decide
    · exact alignedPack k m ws hm hs z h


/-- The smallest wall leaves only three initial blanks. The head immediately
scans the four-one debris instead of clearing an older wall. -/
private theorem thinStart (P X : Tape) :
    steps 3 ⟨P,rep 3 [false] (rep 4 [true] X),.A⟩ =
      some ⟨cons true P,app [true,false] (rep 4 [true] X),.D⟩ := rfl

private theorem thinDigitEnc (j : Nat) (X : Tape) :
    rep 4 [true] (blkV j X) =
    app [true,true] (rep j [true,true,true] (app [true,true,false] X)) := by
  induction j with
  | zero => rfl
  | succ j ih =>
    change app [true,true,true] (rep 4 [true] (blkV j X)) = _
    rw [ih]; rfl

theorem thinEmptyDigit (j : Nat) (P X : Tape) :
    steps (20+3*j) (visitX (rep 2 [true] (cons false P)) [0] (blkV j X)) =
    some (visitX (blkL j (cons true P)) [] X) := by
  have a := emptyWall 1 P (blkV j X)
  have b := thinStart P (blkV j X)
  conv at b => rhs; rw [thinDigitEnc]
  have c := d_head (cons true P) (rep j [true,true,true] (app [true,true,false] X))
  have d := cross_r trans (u := []) d_unit j (app [true,true,true,false] (cons true P))
    (app [true,true,false] X)
  have e : steps 3 ⟨blkL j (cons true P),app [true,true,false] X,.D⟩ =
      some (visitX (blkL j (cons true P)) [] X) := rfl
  have h := steps_seq trans (steps_seq trans (steps_seq trans (steps_seq trans a b) c) d) e
  rwa [show 7+1+3+6+j*3+3=20+3*j by omega] at h

private theorem thinTipEnc (j : Nat) (R : Tape) :
    rep 4 [true] (rep (7+3*j) [true] R) =
    app [true,true] (rep (j+3) [true,true,true] R) := by
  induction j with
  | zero => rfl
  | succ j ih =>
    rw [show 7+3*(j+1)=(7+3*j)+3 by omega]
    change app [true,true,true] (rep 4 [true] (rep (7+3*j) [true] R)) = _
    rw [ih]; rfl

theorem thinEmptyTip (j : Nat) (P R : Tape) :
    steps (26+3*j) (visitX (rep 2 [true] (cons false P)) [0] (rep (7+3*j) [true] R)) =
    some ⟨blkL (j+3) (cons true P),R,.D⟩ := by
  have a := emptyWall 1 P (rep (7+3*j) [true] R)
  have b := thinStart P (rep (7+3*j) [true] R)
  conv at b => rhs; rw [thinTipEnc]
  have c := d_head (cons true P) (rep (j+3) [true,true,true] R)
  have d := cross_r trans (u := []) d_unit (j+3) (app [true,true,true,false] (cons true P)) R
  have h := steps_seq trans (steps_seq trans (steps_seq trans a b) c) d
  rwa [show 7+1+3+6+(j+3)*3=26+3*j by omega] at h

#print axioms thinEmptyDigit
#print axioms emptyMixed
#print axioms openMixed
end H7846.Line24
