import StackClock

namespace H7846.Line24
open TM Word

/-- Relative coordinate of the exposed D whenever the current word finishes
by ordinary passes, openings and a terminal tail. -/
def landingCoordinate (x : Word) : Int :=
  3*(x.mass:Int)+8-3*x.clock-3*weight x.mass

theorem coordinatePasses {x y k} (p : Passes k x y) :
    landingCoordinate x = 3*(k:Int) + landingCoordinate y := by
  obtain ⟨m,c,_⟩ := passCount p
  simp only [landingCoordinate,m,c]; omega

theorem coordinateDigit (a : Nat) (y : Word) :
    landingCoordinate (.d 1 (.d 0 (.d a y))) = (6+3*(a:Int)) + landingCoordinate y := by
  simp only [landingCoordinate,mass,clock,Nat.zero_add,Nat.one_add,weight,Int.natCast_succ,Int.natCast_add]
  omega

theorem coordinateTail (j : Nat) :
    landingCoordinate (.d 1 (.d 0 (.tip j))) = 14+3*(j:Int) := by
  simp only [landingCoordinate,mass,clock,Nat.zero_add,Nat.one_add,weight,Int.natCast_succ]
  omega

private theorem weightPower (n : Nat) : 3*weight n = 4*(-2:Int)^n-1 := by
  induction n with
  | zero => decide
  | succ n ih => rw [weight,Int.pow_succ]; omega

theorem coordinateClosed (x : Word) :
    landingCoordinate x = 3*(x.mass:Int)+9-3*x.clock-4*(-2:Int)^x.mass := by
  have h := weightPower x.mass
  unfold landingCoordinate; omega

/-- All complete stacks whose passes are ordinary until an opening of [1,0,a]
or the terminal [1,0,Tj]. The right exterior is blank throughout the model. -/
inductive LandingPath : Word → Nat → Prop where
  | tail {x k} (j : Nat) (p : Passes k x (.d 1 (.d 0 (.tip j)))) :
      LandingPath x (3*k+(14+3*j))
  | digit {x y k d} (a : Nat) (p : Passes k x (.d 1 (.d 0 (.d a y))))
      (rest : LandingPath y d) : LandingPath x (3*k+(6+3*a)+d)

theorem LandingPath.coordinate {x d} (p : LandingPath x d) : (d:Int) = landingCoordinate x := by
  induction p with
  | tail j run =>
    rw [coordinatePasses run,coordinateTail]
    simp
  | digit a run _ ih =>
    rw [coordinatePasses run,coordinateDigit,← ih]
    simp; omega

private theorem prependRepeat (n : Nat) (w : List Bool) (L : Tape) :
    rep n w L = app ((List.replicate n w).flatten) L := by
  induction n with
  | zero => rfl
  | succ n ih => rw [rep_succ,ih,List.replicate_succ,List.flatten_cons,app_app]

private theorem repeatLen (n : Nat) (w : List Bool) :
    (List.replicate n w).flatten.length = n*w.length := by
  induction n with
  | zero => simp
  | succ n ih => simp [List.replicate_succ,ih,Nat.succ_mul,Nat.add_comm]

/-- The computed position is realized by the machine. The left prefix under
the landing has length d+1, and the left prefix at the initial visit has one
cell. The time and the resulting finite prefix are uniform in the context. -/
theorem LandingPath.physical {x d} (p : LandingPath x d) :
    ∃ (n : Nat) (front : List Bool), front.length = d+1 ∧
      ∀ L, steps n (visitX L [] x.tape) = some ⟨app front L,blank,.D⟩ := by
  induction p with
  | @tail x k j run =>
    obtain ⟨t,first⟩ := timedOrdinary run
    let blocks := (List.replicate (j+4) [true,true,false]).flatten
    let ones := (List.replicate (3*k) [true]).flatten
    refine ⟨t+(26+(j+4)*3),blocks++([true,true,true]++ones),?_,?_⟩
    · simp only [List.length_append,blocks,ones,repeatLen]
      change (j+4)*3+(3+(3*k)*1)=_; omega
    · intro L
      have b := wallTail j (rep (3*k) [true] L) blank
      have z := steps_seq trans (first L) b
      rw [← app_app,← app_app,← prependRepeat,← prependRepeat]
      exact z
  | @digit x y k d a run _ ih =>
    obtain ⟨t,first⟩ := timedOrdinary run
    obtain ⟨u,tail,len,last⟩ := ih
    let blocks := (List.replicate (a+1) [true,true,false]).flatten
    let ones := (List.replicate (3*k) [true]).flatten
    refine ⟨(t+(26+(a+1)*3+3))+u,tail++(blocks++([true,true,true]++ones)),?_,?_⟩
    · simp only [List.length_append,blocks,ones,repeatLen,len]
      change d+1+((a+1)*3+(3+(3*k)*1))=_; omega
    · intro L
      have b := wallNextDigit a (rep (3*k) [true] L) y.tape
      have c := last (rep (a+1) [true,true,false] (rep 3 [true] (rep (3*k) [true] L)))
      have z := steps_seq trans (steps_seq trans (first L) b) c
      rw [← app_app,← app_app,← app_app,← prependRepeat,← prependRepeat]
      exact z

#print axioms LandingPath.coordinate
#print axioms LandingPath.physical
end H7846.Line24
