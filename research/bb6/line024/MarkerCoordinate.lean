import LandingCoordinate
import MarkerPass

namespace H7846.Line24
open TM Word

/-- A word prefixed by a finite list of digits, and a word interpreted with an
arbitrary exterior beyond its terminal run of ones. -/
def prefixDigits (ds : List Nat) (x : Word) : Word := ds.foldr Word.d x

def openWord : Word → Tape → Tape
  | .tip j, R => rep (7+3*j) [true] R
  | .d a x, R => blkV a (openWord x R)

/-- The four words produced by direct contact with six marked cells. -/
def absorbed : Nat → Nat → Word
  | 0,j => .d (j+2) (.tip 0)
  | 1,j => .d (j+1) (.d 0 (.tip 1))
  | 2,j => .d j (.d 1 (.d 1 (.tip 0)))
  | _,j => .d j (.d 1 (.d 0 (.d 0 (.tip 1))))

def contactCost : Nat → Nat
  | 0 => 82 | 1 => 96 | 2 => 104 | _ => 118

private theorem timedAbsorb {g : Nat} (hg : g<4) (j : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (rep g [false] (rep 6 [true] (rep 4 [false] R))))
      (openWord (absorbed g j) R) (14*j+contactCost g) := by
  match g with
  | 0 =>
    have h := timedTouch j 2 R
    rwa [show 14*(j+2)+54=14*j+82 by omega] at h
  | 1 => exact timedGapOne j R
  | 2 => exact timedGapTwo j 1 R
  | 3 => exact timedContact j R
  | n+4 => omega

private theorem readPrefix (ds : List Nat) (x : Word) (R : Tape) :
    openWord (prefixDigits ds x) R = sq blkV ds (openWord x R) := by
  induction ds with
  | nil => rfl
  | cons d ds ih => exact congrArg (blkV d) ih

/-- If the tail is reached through positive digits and directly meets a
six-one marker, four trailing blanks suffice to complete this pass. -/
theorem absorbPass (es : List Nat) (j g : Nat) (hg : g<4) (L R : Tape) :
    let ds := es.map (·+1)
    steps (((es.map (fun e => 14*(e+1)+4)).sum+(14*j+contactCost g))+15)
      (visitX L ds (rep (7+3*j) [true] (rep g [false] (rep 6 [true] (rep 4 [false] R))))) =
    some (visitX (rep 3 [true] L) [] (openWord (prefixDigits ds (absorbed g j)) R)) := by
  dsimp only
  have h : Timed (sq blkV (es.map (·+1)) (rep (7+3*j) [true] (rep g [false] (rep 6 [true] (rep 4 [false] R)))))
      (sq blkV (es.map (·+1)) (openWord (absorbed g j) R))
      ((es.map (fun e => 14*(e+1)+4)).sum+(14*j+contactCost g)) := by
    induction es with
    | nil => simpa using timedAbsorb hg j R
    | cons e es ih =>
      have next := timedKeep e ih
      simp only [List.map_cons,List.sum_cons]
      rw [show (14*(e+1)+4)+(es.map (fun d => 14*(d+1)+4)).sum+(14*j+contactCost g) =
          ((es.map (fun d => 14*(d+1)+4)).sum+(14*j+contactCost g))+(14*(e+1)+4) by omega]
      exact next
  rw [readPrefix]
  exact steps_seq trans (h (cons false L)) (wall_turn L _)

private theorem weightTwo (n : Nat) : weight (n+2) = 4*weight n+1 := by
  rw [weight,weight]; omega

private theorem intake (g j : Nat) (hg : g<4) :
    (absorbed g j).mass = j+2 ∧ (absorbed g j).clock = absorptionClock g := by
  match g with
  | 0 | 1 | 2 | 3 => simp [absorbed,mass,clock,weight,absorptionClock]
  | n+4 => omega

private theorem framedIntake (ds : List Nat) (g j : Nat) (hg : g<4) :
    let x := prefixDigits ds (.tip j)
    let y := prefixDigits ds (absorbed g j)
    y.mass = x.mass+2 ∧ y.clock = 4*x.clock+ds.length+absorptionClock g := by
  induction ds with
  | nil => simpa [prefixDigits,clock,mass] using intake g j hg
  | cons d ds ih =>
    obtain ⟨m,c⟩ := ih
    dsimp only
    change d+_ = (d+_)+2 ∧ weight _ + _ = 4*(weight _ + _) + (ds.length+1:Nat) + _
    unfold prefixDigits at m c
    rw [m,weightTwo,c]
    push_cast; omega

/-- The marker starts at h+2 plus the encoded word width and g clear cells.
The word width is 3 times its mass, one separator per digit, and 7 for the tip. -/
def markerOffset (x : Word) (g : Nat) : Nat := 9+3*x.mass+x.digits+g

private theorem prefixWidth (ds : List Nat) (j : Nat) :
    (prefixDigits ds (.tip j)).digits = ds.length := by
  induction ds with
  | nil => rfl
  | cons d ds ih =>
    change 1+(prefixDigits ds (.tip j)).digits=ds.length+1
    rw [ih,Nat.add_comm]

private theorem targetFromCounts {x y : Word} (g : Nat) (hg : g<4) (h : Int)
    (hm : y.mass = x.mass+2) (hc : y.clock = 4*x.clock+x.digits+absorptionClock g) :
    h+3+landingCoordinate y =
      4*(h+landingCoordinate x) - 3*(h+markerOffset x g) +
        (if g%2=0 then 6 else 30) := by
  unfold landingCoordinate markerOffset
  rw [hm,hc,weightTwo]
  push_cast
  have key : 3*(g:Int)+9-3*absorptionClock g = (if g%2=0 then 6 else 30) := by
    match g with
    | 0 | 1 | 2 | 3 => decide
    | n+4 => omega
  omega

/-- For any ready word having no three adjacent zero digits, the complete
physical pass either keeps the projected absolute landing or applies the
affine marker update. This includes recursive split/carry behavior. -/
theorem readyTarget (g : Nat) (hg : g<4) (x : Word) (ok : x.noTriple)
    (ready : x.ready) (h : Int) :
    ∃ (y : Word) (used : Bool), MarkerAdvance g x y used ∧
      h+3+landingCoordinate y = if used then
        4*(h+landingCoordinate x)-3*(h+markerOffset x g)+(if g%2=0 then 6 else 30)
        else h+landingCoordinate x := by
  obtain ⟨y,used,run⟩ := completeMarkerPass g (by omega) x ok ready
  refine ⟨y,used,run,?_⟩
  cases used with
  | false =>
    have m : y.mass=x.mass := by simpa using run.mass_eq
    have c := run.clock_if rfl
    simp only [landingCoordinate,m,c,ite_false,Bool.false_eq_true]; omega
  | true =>
    exact targetFromCounts g hg h (by simpa using run.mass_eq) (run.clock_used rfl)

/-- At the pass verified by absorbPass, let Z be the former projected landing,
m the marker start, and Z' the projected landing after the head advances
three cells. Then Z' = 4Z - 3m + 6 (even gap) or +30 (odd gap). This
projects the new encoded word with a blank exterior, even when more actual
markers remain beyond it. -/
theorem targetAfterContact (ds : List Nat) (j g : Nat) (hg : g<4) (h : Int) :
    let x := prefixDigits ds (.tip j)
    let y := prefixDigits ds (absorbed g j)
    h+3+landingCoordinate y =
      4*(h+landingCoordinate x) - 3*(h+markerOffset x g) +
        (if g%2=0 then 6 else 30) := by
  obtain ⟨m,c⟩ := framedIntake ds g j hg
  apply targetFromCounts g hg h m
  rwa [prefixWidth]

#print axioms readyTarget
#print axioms absorbPass
#print axioms targetAfterContact
end H7846.Line24
