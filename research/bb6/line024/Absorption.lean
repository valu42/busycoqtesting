import CollisionRules
namespace H7846.Line24
open TM Word

def prefixCost (ds : List Nat) : Nat := (ds.map (fun d => 14*(d+1)+4)).sum

private theorem timedPrefix (ds : List Nat) {X Y : Tape} {t : Nat} (h : Timed X Y t) :
    Timed (sq blkV (ds.map (·+1)) X) (sq blkV (ds.map (·+1)) Y) (prefixCost ds+t) := by
  induction ds with
  | nil => simpa [prefixCost] using h
  | cons d ds ih =>
    have a := timedKeep d ih
    change Timed _ _ ((14*(d+1)+4 + prefixCost ds)+t)
    rw [show (14*(d+1)+4 + prefixCost ds)+t = (prefixCost ds+t)+(14*(d+1)+4) by omega]
    exact a

/-- The empty digits introduced at contact disappear one sweep later. An incoming
tail with positive index j+1 becomes one digit j+2 and a tail of index 1. -/
theorem absorbMarker (ds : List Nat) (j : Nat) (L R : Tape) :
    let ks := ds.map (·+1)
    steps ((prefixCost ds + (14*(j+1)+118) + 15) +
           (prefixCost ds + (14*(j+1)+18) + 15))
      (visitX L ks (rep (7+3*(j+1)) [true] (contact R))) =
      some (visitX (rep 6 [true] L) ks (blkV (j+2) (rep 10 [true] R))) := by
  dsimp only
  have first := framedContact ds (j+1) L R
  have core := timedJoin j (cons false (rep 10 [true] R))
  have norm : Timed (blkV (j+1) (contactResult R))
       (blkV (j+2) (rep 10 [true] R)) (14*(j+1)+18) := core
  have second := timedPrefix ds norm (cons false (rep 3 [true] L))
  have turn := wall_turn (rep 3 [true] L) (sq blkV (ds.map (·+1)) (blkV (j+2) (rep 10 [true] R)))
  have both := steps_seq trans first (steps_seq trans second turn)
  exact both

theorem thirdAbsorption (L R : Tape) :
    steps 994 (visitX L [1,2,2,3,3,2,2,3,1] (rep 31 [true] (contact R))) =
      some (visitX (rep 6 [true] L) [1,2,2,3,3,2,2,3,1,9] (rep 10 [true] R)) :=
  absorbMarker [0,1,1,2,2,1,1,2,0] 7 L R
end H7846.Line24
