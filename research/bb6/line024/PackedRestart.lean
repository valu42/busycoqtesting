import Return
import PackedTape

namespace H7846.Line24.PackedTape
open TM
set_option maxRecDepth 16000

/-- The marker train in the certified second state-A restart. The denotation
preserves separate adjacent runs, and prepend merges them for execution. -/
private def train : Runs := (false,4) :: returnedWidths.foldl
  (fun xs w => (false,w) :: (true,6) :: xs) [(false,2),(true,4)]

private def debrisRuns : Runs :=
  ([1] ++ List.replicate 19 2 ++ [3,0,1,1]).flatMap
    (fun k : Nat => [(true,3*k),(false,1)]) ++ [(true,7)]

private def size (xs : Runs) : Nat := (xs.map Prod.snd).sum
private abbrev cutAt := 18396801869163

/-- Both half-tapes including the distance to the older counter suffix. -/
def restartPack : Pack :=
  ⟨[(true,5),(false,1),(true,2),(false,1),(true,3)],
   prepend train (push false (cutAt-size train) (push true 4 (prepend debrisRuns []))), .A⟩

private theorem cutRep (k n : Nat) (b : Bool) (X Y : Tape) :
    Box.cut (k+n) (rep k [b] X) Y = rep k [b] (Box.cut n X Y) := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [show k+1+n = (k+n)+1 by omega]
    exact congrArg (cons b) ih

private theorem cutRuns (xs : Runs) (n : Nat) (X Y : Tape) :
    Box.cut (size xs+n) (denoteWith xs X) Y = denoteWith xs (Box.cut n X Y) := by
  induction xs with
  | nil => simp [size,denoteWith]
  | cons h xs ih =>
    obtain ⟨b,k⟩ := h
    change Box.cut ((k+size xs)+n) (rep k [b] (denoteWith xs X)) Y = rep k [b] _
    rw [Nat.add_assoc,cutRep,ih]

private theorem foldedMarkers (ws : List Nat) (rs : Runs) (tail : Tape) :
    denoteWith (ws.foldl (fun xs w => (false,w)::(true,6)::xs) rs) tail =
      markers ws (denoteWith rs tail) := by
  induction ws generalizing rs with
  | nil => rfl
  | cons w ws ih => exact ih ((false,w)::(true,6)::rs)

private theorem trainEq : denoteWith train blank = (regenerated returnedWidths exterior).r := by
  exact congrArg (rep 4 [false]) (foldedMarkers returnedWidths [(false,2),(true,4)] blank)
private theorem digitTape (n : Nat) (X : Tape) : rep (3*n) [true] (cons false X) = blkV n X := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [show 3*(n+1)=3+(3*n) by omega,rep_add]
    exact congrArg (app [true,true,true]) ih

private theorem wordTape (ds : List Nat) :
    denoteWith (ds.flatMap (fun k : Nat => [(true,3*k),(false,1)]) ++ [(true,7)]) blank =
      (word ds 0).tape := by
  induction ds with
  | nil => rfl
  | cons d ds ih =>
    change rep (3*d) [true] (cons false _) = blkV d _
    exact (digitTape d _).trans (congrArg (blkV d) ih)

private theorem debrisEq : denoteWith debrisRuns blank = debris := wordTape _

theorem restartPack_eq : restartPack.toCfg = secondRestart := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  refine ⟨rfl,?_,rfl⟩
  change denote (prepend train (push false (cutAt-size train) (push true 4 (prepend debrisRuns [])))) = Box.cut cutAt (regenerated returnedWidths exterior).r (rep 4 [true] debris)
  rw [denotePrepend,denotePush,denotePush,denotePrepend]
  have sz : cutAt = size train + (cutAt-size train) := by decide
  rw [← trainEq]
  conv => rhs; arg 1; rw [sz]
  rw [cutRuns,Box.zeros]
  exact congrArg (fun X => denoteWith train (rep (cutAt-size train) [false] (rep 4 [true] X))) debrisEq

#print axioms restartPack_eq
end H7846.Line24.PackedTape
