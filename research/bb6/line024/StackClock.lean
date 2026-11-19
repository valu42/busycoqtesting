import Timing

namespace H7846.Line24
open TM Word

/-- A complete stack of ordinary counter phases over a blank right exterior.
Every opening peels the digits 1,0,1. The final phase exposes 1,0,T0. -/
inductive StackWalk : Word → Nat → Nat → Prop where
  | last {x k} (phase : Passes k x (.d 1 (.d 0 (.tip 0)))) : StackWalk x 0 k
  | next {x y k r q} (phase : Passes k x (.d 1 (.d 0 (.d 1 y))))
      (rest : StackWalk y r q) : StackWalk x (r+1) (k+q)

private theorem oddWeight (r : Nat) :
    3*weight (2*r+1) = -8*(4:Int)^r-1 := by
  induction r with
  | zero => decide
  | succ r ih =>
    rw [show 2*(r+1)+1 = (2*r+1)+1+1 by omega]
    rw [weight,weight,Int.pow_succ]
    omega

/-- The number of openings is fixed by the starting mass. The cumulative
ordinary pass count depends only on that mass and the starting clock. -/
theorem StackWalk.count {x r k} (p : StackWalk x r k) :
    x.mass = 2*r+1 ∧ 3*(k:Int)+3*x.clock = 8*(4:Int)^r-2-3*r := by
  induction p with
  | last phase =>
    obtain ⟨m,c,_⟩ := passCount phase
    simp only [mass,clock,weight] at m c
    simp; omega
  | @next x y k r q phase rest ih =>
    obtain ⟨m,c,_⟩ := passCount phase
    obtain ⟨my,cy⟩ := ih
    simp only [mass,clock,Nat.zero_add,Nat.one_add] at m c
    have jump := oddWeight r
    rw [← my] at jump
    rw [weight] at c
    rw [Int.pow_succ]
    simp only [Int.natCast_add,Int.cast_ofNat_Int]
    omega

/-- Ordinary wall visits advance three cells, openings advance nine and the
final T0 exposes D fourteen cells farther right. This closed form gives the
coordinate relative to the initial visiting head. -/
theorem StackWalk.displacement {x r k} (p : StackWalk x r k) :
    (3*k+9*r+14 : Nat) = (8*(4:Int)^r+6*r+12-3*x.clock) := by
  have h := p.count.2
  simp only [Int.natCast_add,Int.natCast_mul,Int.cast_ofNat_Int]
  omega

private theorem repeatOnes (n : Nat) (L : Tape) :
    rep n [true] L = app (List.replicate n true) L := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [rep_succ,List.replicate_succ,app_cons,app]; rw [ih]

private theorem atomOfPass {x y} (p : Pass x y) : ∃ t, Atom x y t := by
  induction p with
  | tipStep j => exact ⟨_,Atom.tip j⟩
  | keep i _ ih =>
    obtain ⟨_,a⟩ := ih
    exact ⟨_,Atom.keep i a⟩
  | split m => exact ⟨_,Atom.split m⟩
  | mergeTail i => exact ⟨_,Atom.mergeTail i⟩
  | mergeDigit i y => exact ⟨_,Atom.mergeDigit i y⟩
  | carry m _ ih =>
    obtain ⟨_,a⟩ := ih
    exact ⟨_,Atom.carry m a⟩

theorem timedOrdinary {x y k} (p : Passes k x y) :
    ∃ n, ∀ L, steps n (visitX L [] x.tape) = some (visitX (rep (3*k) [true] L) [] y.tape) := by
  have hs : ∃ t, Series x y k t := by
    induction p with
    | refl x => exact ⟨_,Series.nil x⟩
    | next _ step ih =>
      obtain ⟨_,s⟩ := ih
      obtain ⟨_,a⟩ := atomOfPass step
      exact ⟨_,Series.snoc s (atomSound a)⟩
  obtain ⟨_,s⟩ := hs
  exact ⟨_,runSeries s⟩

/-- At the landing, the left half consists of an explicit-length finite prefix
followed by the unchanged arbitrary left context. Initially one separator
stood before that same context, hence the head displacement is prefix length minus one. -/
theorem StackWalk.land {x r k} (p : StackWalk x r k) :
    ∃ front : List Bool, front.length = 3*k+9*r+15 ∧
        ∃ n, ∀ L, steps n (visitX L [] x.tape) = some ⟨app front L,blank,.D⟩ := by
  induction p with
  | @last x k phase =>
    let head : List Bool := [true,true,false,true,true,false,true,true,false,true,true,false,true,true,true]
    refine ⟨head ++ List.replicate (3*k) true,?_,?_⟩
    · rw [List.length_append,List.length_replicate]
      change 15+3*k=3*k+9*0+15; omega
    · obtain ⟨t,run⟩ := timedOrdinary phase
      refine ⟨t+38,?_⟩
      intro L
      have a := run L
      have b := wallTail 0 (rep (3*k) [true] L) blank
      have both := steps_seq trans a b
      rw [← app_app,← repeatOnes]
      exact both
  | @next x y k r q phase rest ih =>
    obtain ⟨tail,len,u,run⟩ := ih
    let block : List Bool := [true,true,false,true,true,false,true,true,true]
    refine ⟨tail ++ (block ++ List.replicate (3*k) true),?_,?_⟩
    · rw [List.length_append,List.length_append,List.length_replicate,len]
      change _ + (9 + 3*k) = _; omega
    · obtain ⟨t,first⟩ := timedOrdinary phase
      refine ⟨(t+35)+u,?_⟩
      intro L
      have a := first L
      have b := wallNextDigit 1 (rep (3*k) [true] L) y.tape
      have c := run (app block (rep (3*k) [true] L))
      have both := steps_seq trans (steps_seq trans a b) c
      rw [← app_app,← app_app,← repeatOnes]
      exact both

/-- A single time and left-prefix word work for every initial left context.
The landing's left boundary is located by the initial word's mass and clock. -/
theorem StackWalk.landAt {x r k} (p : StackWalk x r k) :
    ∃ (n : Nat) (front : List Bool),
        (front.length:Int) = 8*(4:Int)^r+6*r+13-3*x.clock ∧
        ∀ L, steps n (visitX L [] x.tape) = some ⟨app front L,blank,.D⟩ := by
  obtain ⟨front,len,n,h⟩ := p.land
  refine ⟨n,front,?_,h⟩
  have d := p.displacement
  simp only [Int.natCast_add,Int.natCast_mul,Int.cast_ofNat_Int] at d
  rw [len]
  simp only [Int.natCast_add,Int.natCast_mul,Int.cast_ofNat_Int]
  omega

#print axioms StackWalk.count
#print axioms StackWalk.landAt
end H7846.Line24
