import WordGrammar
import MarkerGaps

namespace H7846.Line24.Word
open TM

/-- The head of a still-pending marker suffix. -/
def sixMarker (g : Nat) (R : Tape) := rep g [false] (rep 6 [true] (rep 4 [false] R))

/-- Clock contribution from the suffix produced when a marker is absorbed. -/
def absorptionClock : Nat → Int
  | 0 => 1 | 1 => -6 | 2 => 3 | _ => -4

private theorem weightTwo (n : Nat) : weight (n+2) = 4*weight n+1 := by
  rw [weight,weight]; omega

/-- A full core pass can leave the marker intact or absorb it. -/
structure MarkerAdvance (g : Nat) (x y : Word) (used : Bool) : Prop where
  run : ∃ t, ∀ R, Timed (x.above (sixMarker g R)) (y.above (if used then R else sixMarker g R)) t
  grammar : y.noTriple
  mass_eq : y.mass = x.mass + (if used then 2 else 0)
  length_eq : y.digits + 3 = x.digits + (if used then g+4 else 0)
  clock_if : used=false → y.clock=x.clock+1
  clock_used : used=true → y.clock=4*x.clock+(x.digits:Int)+absorptionClock g

private theorem markerTip (g j : Nat) (h : g ≤ 3) :
    ∃ y b, MarkerAdvance g (.tip j) y b := by
  have choices : g=0 ∨ g=1 ∨ g=2 ∨ g=3 := by omega
  rcases choices with rfl | rfl | rfl | rfl
  · refine ⟨.d (j+2) (.tip 0),true,⟨_,fun R => timedTouch j 2 R⟩,?_,?_,by simp [digits],by simp,by simp [clock,digits,mass,weight,absorptionClock]⟩
    · simp [noTriple,notDouble]
    · simp [mass]
  · refine ⟨.d (j+1) (.d 0 (.tip 1)),true,⟨_,fun R => timedGapOne j R⟩,?_,?_,by simp [digits],by simp,by simp [clock,digits,mass,weight,absorptionClock]⟩
    · simp [noTriple,notDouble,headOK]
    · simp [mass]
  · refine ⟨.d j (.d 1 (.d 1 (.tip 0))),true,⟨_,fun R => timedGapTwo j 1 R⟩,?_,?_,by simp [digits],by simp,by simp [clock,digits,mass,weight,absorptionClock]⟩
    · simp [noTriple,notDouble,headOK]
    · simp [mass]
  · refine ⟨.d j (.d 1 (.d 0 (.d 0 (.tip 1)))),true,⟨_,fun R => timedContact j R⟩,?_,?_,by simp [digits],by simp,by simp [clock,digits,mass,weight,absorptionClock]⟩
    · simp [noTriple,notDouble,headOK]
    · simp [mass]

private theorem markerKeep {x y b g} (i : Nat) (h : MarkerAdvance g x y b) :
    MarkerAdvance g (.d (i+1) x) (.d (i+1) y) b := by
  obtain ⟨⟨t,core⟩,hs,hm,hl,hc,used⟩ := h
  refine ⟨⟨_,fun R => timedKeep i (core R)⟩,⟨hs,by omega⟩,by simp [mass,hm,Nat.add_assoc],by simp only [digits]; omega,?_,?_⟩
  · rintro rfl
    have a := hc rfl
    simp only [Bool.false_eq_true,ite_false,Nat.add_zero] at hm
    simp [clock,hm,a,Int.add_assoc]
  · rintro rfl
    have a := used rfl
    simp only [ite_true] at hm
    simp only [clock,digits,hm,weightTwo,a,Int.natCast_add,Int.cast_ofNat_Int]
    omega

private theorem markerSplit {x y b g} (m : Nat) (h : MarkerAdvance g (augment 1 x) y b) :
    MarkerAdvance g (.d (m+2) (.d 0 x)) (.d m (.d 1 y)) b := by
  obtain ⟨⟨t,core⟩,hs,hm,hl,hc,used⟩ := h
  simp only [augmentMass] at hm
  refine ⟨⟨14*m+32+t,?_⟩,?_,?_,?_,?_,?_⟩
  · intro R
    have a := core R
    rw [augmentAbove] at a
    exact timedSplitSuffix m a
  · exact ⟨⟨hs,by omega⟩,fun _ => by simp [notDouble]⟩
  · simp [mass,hm]; omega
  · simp only [digits]; rw [augmentDigits] at hl; omega
  · rintro rfl
    have a := hc rfl
    simp only [Bool.false_eq_true, ite_false,Nat.add_zero] at hm
    simp only [augmentClock] at a
    simp only [clock,mass,hm,a,Nat.zero_add,Nat.one_add,weight]; omega

  · rintro rfl
    have a := used rfl
    simp only [ite_true] at hm
    simp only [augmentClock,augmentDigits] at a
    have t : y.mass=x.mass+3 := by omega
    simp only [clock,mass,digits,Nat.zero_add,Nat.one_add,t,a]
    rw [show x.mass+3 = (x.mass+2)+1 by omega]
    simp only [weight]
    omega

private theorem markerJoin (i g : Nat) (x : Word) (ok : x.noTriple) :
    MarkerAdvance g (.d (i+1) (.d 1 (.d 0 x))) (augment (i+2) x) false := by
  refine ⟨⟨14*(i+1)+18,?_⟩,augmentNoTriple _ _ ok,?_,by simp [digits]; omega,?_,by simp⟩
  · intro R
    simp only [Bool.false_eq_true,ite_false,augmentAbove]
    exact timedJoin i (x.above (sixMarker g R))
  · simp [mass]; omega
  · intro _
    simp only [augmentClock,clock,mass,Nat.zero_add,Nat.one_add,weight]; omega

/-- All four short clearances give a returning physical pass for every ready
word with no three successive empty digits, at arbitrary recursive depth. -/
theorem completeMarkerPass (g : Nat) (gap : g ≤ 3) (x : Word) (ok : x.noTriple) (hr : x.ready) :
    ∃ y b, MarkerAdvance g x y b := by
  apply readyInduction (P := fun z => ∃ y b, MarkerAdvance g z y b) (fun j => markerTip g j gap) _ _ _ x ok hr
  · rintro i _ ⟨y,b,h⟩
    exact ⟨_,b,markerKeep i h⟩
  · rintro m _ ⟨y,b,h⟩
    exact ⟨_,b,markerSplit m h⟩
  · intro i z hz
    exact ⟨_,false,markerJoin i g z hz⟩

#print axioms completeMarkerPass
end H7846.Line24.Word
