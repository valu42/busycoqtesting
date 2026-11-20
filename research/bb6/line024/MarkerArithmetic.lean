import MarkerCoordinate

namespace H7846.Line24
open Word

private theorem weightModFour (n : Nat) : weight n % 4 = 1 := by
  induction n with
  | zero => decide
  | succ n ih => simp only [weight]; omega

private theorem clockModFour (x : Word) : x.clock % 4 = (x.digits : Int) % 4 := by
  induction x with
  | tip j => rfl
  | d j x ih =>
    have w := weightModFour x.mass
    simp only [clock,digits,Int.natCast_add,Int.cast_ofNat_Int]
    omega

/-- The projected landing and the first cell beyond the encoded word
occupy the same residue class modulo four at every counter visit. -/
theorem contactResidue (h : Int) (x : Word) (g : Nat) :
    ((h+markerOffset x g)-(h+landingCoordinate x))%4 = (g:Int)%4 := by
  have a := clockModFour x
  have b := weightModFour x.mass
  unfold landingCoordinate markerOffset
  push_cast
  omega

/-- Projected landing immediately after absorbing the six ones at m. -/
def markerTarget (z m : Int) : Int :=
  4*z-3*m+(if (m-z)%2=0 then 6 else 30)

/-- A complete ready pass updates the projected landing using just the
old landing and the absolute start of the pending marker. -/
theorem readyCoordinate (g : Nat) (hg : g<4) (x : Word) (ok : x.noTriple)
    (ready : x.ready) (h : Int) :
    let z := h+landingCoordinate x
    let m := h+markerOffset x g
    ∃ (y : Word) (used : Bool), MarkerAdvance g x y used ∧
      h+3+landingCoordinate y = if used then markerTarget z m else z := by
  dsimp only
  obtain ⟨y,used,run,coord⟩ := readyTarget g hg x ok ready h
  refine ⟨y,used,run,?_⟩
  have res := contactResidue h x g
  have key : ((h+markerOffset x g)-(h+landingCoordinate x))%2=0 ↔ g%2=0 := by omega
  simpa only [markerTarget,key] using coord

/-- After one absorption the residue is independent of the old target. -/
theorem markerTargetResidue (z m : Int) : markerTarget z m % 4 = (m+2)%4 := by
  unfold markerTarget
  split <;> omega

/-- The parity correction after the first marker depends only on the
spacing between the two consecutive consumed markers. -/
theorem markerTargetNext (z m n : Int) :
    markerTarget (markerTarget z m) n =
      4*markerTarget z m-3*n+(if (n-m)%2=0 then 6 else 30) := by
  have r := markerTargetResidue z m
  change 4*markerTarget z m-3*n+(if (n-markerTarget z m)%2=0 then 6 else 30) = _
  have parity : (n-markerTarget z m)%2=0 ↔ (n-m)%2=0 := by omega
  simp only [parity]

#print axioms contactResidue
#print axioms readyCoordinate
#print axioms markerTargetNext
end H7846.Line24
