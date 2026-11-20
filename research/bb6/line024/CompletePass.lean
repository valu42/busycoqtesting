import SharpPhase
namespace H7846.Line24
open TM Word

namespace Word

/-- Add triples to the initial run of ones, including when the word is only a tip. -/
def augment (k : Nat) : Word → Word
  | .tip j => .tip (k+j)
  | .d n z => .d (k+n) z

private theorem triple (n : Nat) (S : Tape) : rep n [true,true,true] S = rep (3*n) [true] S := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [show 3*(n+1) = 3*n+3 by omega]
    change app [true,true,true] (rep n [true,true,true] S) = app [true,true,true] _
    rw [ih]

theorem augmentTape (k : Nat) (x : Word) : (augment k x).tape = rep k [true,true,true] x.tape := by
  cases x with
  | tip j =>
    change rep (7+3*(k+j)) [true] blank = rep k [true,true,true] (rep (7+3*j) [true] blank)
    rw [triple,← rep_add]; congr 1; omega
  | d n z => exact rep_add k n _ _

theorem augmentAbove (k : Nat) (x : Word) (R : Tape) :
    (augment k x).above R = rep k [true,true,true] (x.above R) := by
  cases x with
  | tip j =>
    change rep (7+3*(k+j)) [true] R = rep k [true,true,true] (rep (7+3*j) [true] R)
    rw [triple,← rep_add]; congr 1; omega
  | d n z => exact rep_add k n _ _

private theorem aboveBlank (x : Word) : x.above blank = x.tape := by
  induction x with
  | tip j => rfl
  | d n x ih => exact congrArg (blkV n) ih

@[simp] theorem augmentMass (k : Nat) (x : Word) : (augment k x).mass = k+x.mass := by
  cases x <;> simp [augment,mass,Nat.add_assoc]
@[simp] theorem augmentClock (k : Nat) (x : Word) : (augment k x).clock = x.clock := by cases x <;> rfl
@[simp] theorem augmentDigits (k : Nat) (x : Word) : (augment k x).digits = x.digits := by cases x <;> rfl

theorem augmentSeparated (k : Nat) (x : Word) (ok : x.separated) : (augment k x).separated := by
  cases x with
  | tip j => trivial
  | d n z =>
    obtain ⟨h,hh⟩ := ok
    exact ⟨h,fun e => hh (by change k+n=0 at e; omega)⟩

/-- A ready word is any tip or a nonempty leading digit other than the wall opener 1,0. -/
def ready : Word → Prop
  | .tip _ => True
  | .d k z => 0 < k ∧ (k = 1 → z.headOK)

theorem augmentReady (x : Word) (hx : x.headOK) : (augment 1 x).ready := by
  cases x with
  | tip j => trivial
  | d n z => change 0<n at hx; exact ⟨by change 0<1+n; omega,fun h => by change 1+n=1 at h; omega⟩

/-- A complete core pass on the actual machine and its three accounting identities. -/
structure Advances (x y : Word) : Prop where
  clearance : ∃ t b, (b=0 ∨ b=4) ∧ x.digits+b = 3+y.digits ∧
    ∀ R, Timed (x.above (rep b [false] R)) (y.above R) t
  mass_eq : y.mass = x.mass
  clock_eq : y.clock = x.clock+1
  separated : y.separated

theorem Advances.timed {x y : Word} (h : Advances x y) : ∃ t, Timed x.tape y.tape t := by
  obtain ⟨t,b,small,_,core⟩ := h.clearance
  have z : rep b [false] blank = blank := by
    rcases small with rfl | rfl
    · rfl
    · change cons false (cons false (cons false (cons false blank))) = blank
      repeat rw [cons_false_blank]
  have actual := core blank
  rw [z,aboveBlank,aboveBlank] at actual
  exact ⟨_,actual⟩

private theorem underDigit {x y : Word} (i : Nat) (h : Advances x y) :
    Advances (.d (i+1) x) (.d (i+1) y) := by
  obtain ⟨⟨t,b,small,len,core⟩,hm,hc,hs⟩ := h
  exact ⟨⟨_,b,small,by simp only [digits]; omega,fun R => timedKeep i (core R)⟩,
    by simp [mass,hm],by simp [clock,hm,hc,Int.add_assoc],⟨hs,by omega⟩⟩

private theorem splitAny {x y : Word} (m : Nat) (h : Advances (augment 1 x) y) :
    Advances (.d (m+2) (.d 0 x)) (.d m (.d 1 y)) := by
  obtain ⟨⟨t,b,small,len,core⟩,hm,hc,hs⟩ := h
  simp only [augmentMass,augmentClock,augmentDigits] at hm hc len
  refine ⟨⟨14*m+32+t,b,small,by simp only [digits]; omega,?_⟩,by simp [mass,hm]; omega,?_,?_⟩
  · intro R
    have r := core R
    rw [augmentAbove] at r
    exact timedSplitSuffix m r
  · simp only [clock,mass,hm,hc,Nat.zero_add,Nat.one_add,weight]; omega
  · exact ⟨⟨hs,by omega⟩,fun _ => Nat.zero_lt_succ _⟩

private theorem joinAny (i : Nat) (x : Word) (ok : x.separated) :
    Advances (.d (i+1) (.d 1 (.d 0 x))) (augment (i+2) x) := by
  refine ⟨⟨14*(i+1)+18,0,Or.inl rfl,by simp [digits]; omega,?_⟩,?_,?_,augmentSeparated _ _ ok⟩
  · intro R
    rw [augmentAbove]; exact timedJoin i (x.above R)
  · simp [mass]; omega
  · simp only [augmentClock,clock,mass,Nat.zero_add,Nat.one_add,weight]; omega

/-- Every separated ready word performs a genuine ordinary pass. -/
theorem completePass (x : Word) (ok : x.separated) (hr : x.ready) : ∃ y, Advances x y := by
  suffices allWords : ∀ n : Nat, ∀ x : Word, x.mass+x.digits ≤ n → x.separated → x.ready → ∃ y, Advances x y from
    allWords _ x (Nat.le_refl _) ok hr
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro x size ok hr
    match x with
    | .tip j =>
      exact ⟨.d j (.tip 0),⟨_,atomClearance (Atom.tip j)⟩,by simp [mass],by simp [clock,mass,weight],
        ⟨trivial,fun _ => trivial⟩⟩
    | .d 0 _ => exact False.elim (by have := hr.1; omega)
    | .d (i+1) x =>
      by_cases hx : x.ready
      · have hlt : x.mass+x.digits < n := by simp [mass,digits] at size; omega
        obtain ⟨y,hy⟩ := ih _ hlt x (by omega) ok.1 hx
        exact ⟨_,underDigit i hy⟩
      · cases x with
        | tip j => exact False.elim (hx trivial)
        | d k z =>
          cases k with
          | zero =>
            have nz : i ≠ 0 := by
              intro e
              have impossible := hr.2 (by omega : i+1=1)
              exact Nat.lt_irrefl 0 impossible
            obtain ⟨m,rfl⟩ := Nat.exists_eq_succ_of_ne_zero nz
            have positive := ok.1.2 rfl
            have hlt : (augment 1 z).mass+(augment 1 z).digits < n := by
              simp [mass,digits] at size; simp; omega
            obtain ⟨y,hy⟩ := ih _ hlt (augment 1 z) (by omega) (augmentSeparated 1 z ok.1.1) (augmentReady z positive)
            exact ⟨_,splitAny m hy⟩
          | succ k =>
            cases k with
            | zero =>
              cases z with
              | tip j => exact False.elim (hx ⟨by decide,fun _ => trivial⟩)
              | d n w =>
                cases n with
                | zero => exact ⟨_,joinAny i w ok.1.1.1⟩
                | succ n => exact False.elim (hx ⟨by decide,fun _ => Nat.zero_lt_succ _⟩)
            | succ k => exact False.elim (hx ⟨by omega,by omega⟩)

/-- The only two shapes that are not ready for another ordinary pass. -/
def boundary (x : Word) := (∃ z, x = .d 0 z) ∨ (∃ z, x = .d 1 (.d 0 z))

private theorem boundaryOfNotReady (x : Word) (h : ¬x.ready) : x.boundary := by
  cases x with
  | tip j => exact False.elim (h trivial)
  | d k z =>
    cases k with
    | zero => exact Or.inl ⟨z,rfl⟩
    | succ k =>
      cases k with
      | succ k => exact False.elim (h ⟨by omega,by omega⟩)
      | zero =>
        cases z with
        | tip j => exact False.elim (h ⟨by decide,fun _ => trivial⟩)
        | d n w =>
          cases n with
          | zero => exact Or.inr ⟨w,rfl⟩
          | succ n => exact False.elim (h ⟨by decide,fun _ => Nat.zero_lt_succ _⟩)

private def remaining (x : Word) : Int :=
  ((2*x.mass+1:Nat):Int) * ((2:Int)^(x.mass+1)-1) - x.clock

private theorem remainingNonneg (x : Word) (ok : x.separated) : 0 ≤ remaining x :=
  phaseBound (.refl x) ok

/-- From every separated word over a blank right exterior there is a *finite
actual run* to one of the two wall events. The left exterior is unrestricted.
No assumption that a pass oracle returns or that a phase terminates is needed. -/
theorem reachesBoundary (x : Word) (ok : x.separated) :
    ∃ y k t, Series x y k t ∧ y.boundary ∧ y.separated ∧ y.mass=x.mass ∧ y.clock=x.clock+k := by
  by_cases hx : x.ready
  · obtain ⟨y,hy⟩ := completePass x ok hx
    obtain ⟨s,step⟩ := hy.timed
    obtain ⟨_,hm,hc,hs⟩ := hy
    have smaller : (remaining y).toNat < (remaining x).toNat := by
      have a := remainingNonneg y hs
      have e : remaining y = remaining x - 1 := by unfold remaining; rw [hm,hc]; omega
      omega
    obtain ⟨z,k,t,hz,b,sep,massEq,clockEq⟩ := reachesBoundary y hs
    have one := single (x := x) (y := y) step
    exact ⟨z,1+k,s+t,concat one hz,b,sep,massEq.trans hm,by rw [clockEq,hc]; omega⟩
  · exact ⟨x,0,0,Series.nil x,boundaryOfNotReady x hx,ok,rfl,by simp⟩
termination_by (remaining x).toNat

theorem physicalBoundary (x : Word) (ok : x.separated) (L : Tape) :
    ∃ (y : Word) (k n : Nat), steps n (visitX L [] x.tape) =
      some (visitX (rep (3*k) [true] L) [] y.tape) ∧ y.boundary ∧ y.separated ∧ y.mass=x.mass := by
  obtain ⟨y,k,t,h,b,sep,hm,_⟩ := reachesBoundary x ok
  exact ⟨y,k,t+15*k,runSeries h L,b,sep,hm⟩


/-- A terminal counter event is either an exposed empty digit or a D landing
on the blank exterior. The tape outside the counter on the left is unrestricted. -/
def terminalCounter (c : Config) : Prop :=
  (∃ (P : Tape) (z : Word), c = visitX P [0] z.tape ∧ z.separated ∧ z.headOK) ∨
  (∃ P : Tape, c = ⟨P,blank,.D⟩)

/-- On a blank right exterior the procedure of continuing through every digit
opening also terminates. Each opening removes the leading 1 and the opened
digit from the counter mass. -/
theorem terminalEvent (x : Word) (ok : x.separated) (L : Tape) :
    ∃ n c, steps n (visitX L [] x.tape) = some c ∧ terminalCounter c := by
  obtain ⟨y,k,n,h,bound,sep,hm⟩ := physicalBoundary x ok L
  let P := rep (3*k) [true] L
  rcases bound with ⟨z,rfl⟩ | ⟨z,rfl⟩
  · exact ⟨n,_,h,Or.inl ⟨P,z,rfl,sep.1,sep.2 rfl⟩⟩
  · cases z with
    | tip j =>
      have t := wallTail j P blank
      have joined := steps_seq trans h t
      exact ⟨_,_,joined,Or.inr ⟨_,rfl⟩⟩
    | d j z =>
      have smaller : z.mass < x.mass := by simp [mass] at hm; omega
      have split := wallNextDigit j P z.tape
      let P' := rep (j+1) [true,true,false] (rep 3 [true] P)
      obtain ⟨u,c,finish,event⟩ := terminalEvent z sep.1.1.1 P'
      exact ⟨_,c,steps_seq trans (steps_seq trans h split) finish,event⟩
termination_by x.mass


/-- At a short gap the next ordinary pass would return if it had four blanks.
The actual exterior can instead interrupt that pass. -/
def stopped (x : Word) (g : Nat) : Prop :=
  x.boundary ∨ (x.ready ∧ g < 4 ∧ ∃ (y : Word) (t : Nat), Advances x y ∧
    x.digits+4=3+y.digits ∧ ∀ R, Timed (x.above (rep 4 [false] R)) (y.above R) t)

/-- Progress all the way to a wall event or a possible marker contact, with an
arbitrary pending right exterior. The total retired clearance is a multiple of
four. Every move before this stopping point is certified on both full tapes. -/
theorem finiteFrontier (x : Word) (ok : x.separated) (g : Nat) :
    ∃ (y : Word) (k n r : Nat), stopped y r ∧ y.separated ∧ y.mass=x.mass ∧
      y.clock=x.clock+k ∧ r ≤ g ∧ (g-r)%4=0 ∧ x.digits+g=3*k+y.digits+r ∧
      ∀ L R, steps n (visitX L [] (x.above (rep g [false] R))) =
      some (visitX (rep (3*k) [true] L) [] (y.above (rep r [false] R))) := by
  have done (h : stopped x g) : ∃ (y : Word) (k n r : Nat), stopped y r ∧ y.separated ∧
      y.mass=x.mass ∧ y.clock=x.clock+k ∧ r ≤ g ∧ (g-r)%4=0 ∧ x.digits+g=3*k+y.digits+r ∧
      ∀ L R, steps n (visitX L [] (x.above (rep g [false] R))) =
      some (visitX (rep (3*k) [true] L) [] (y.above (rep r [false] R))) := by
    exact ⟨x,0,0,g,h,ok,rfl,by simp,by omega,by simp,by omega,fun _ _ => rfl⟩
  by_cases hr : x.ready
  · obtain ⟨y,hy⟩ := completePass x ok hr
    obtain ⟨t,b,small,len,core⟩ := hy.clearance
    by_cases avail : b ≤ g
    · have smaller : (remaining y).toNat < (remaining x).toNat := by
        have a := remainingNonneg y hy.separated
        have e : remaining y = remaining x - 1 := by unfold remaining; rw [hy.mass_eq,hy.clock_eq]; omega
        omega
      obtain ⟨z,k,n,r,stop,sep,massEq,clockEq,le,mod,delta,tailRun⟩ :=
        finiteFrontier y hy.separated (g-b)
      refine ⟨z,1+k,t+15+n,r,stop,sep,massEq.trans hy.mass_eq,by rw [clockEq,hy.clock_eq]; omega,
        by omega,by rcases small with rfl|rfl <;> omega,by omega,?_⟩
      intro L R
      let S := rep (g-b) [false] R
      have p := core S (cons false L)
      have q := wall_turn L (y.above S)
      have a := tailRun (rep 3 [true] L) R
      have h := steps_seq trans (steps_seq trans p q) a
      have eq : rep g [false] R = rep b [false] S := by
        unfold S; rw [← rep_add]; congr 1; omega
      rw [eq,show 3*(1+k)=3*k+3 by omega,rep_add (3*k) 3]
      exact h
    · have hb : b=4 := by rcases small with rfl|rfl <;> omega
      subst b
      exact done (Or.inr ⟨hr,by omega,y,t,hy,len,core⟩)
  · exact done (Or.inl (boundaryOfNotReady x hr))
termination_by (remaining x).toNat

end Word
#print axioms Word.finiteFrontier
#print axioms Word.terminalEvent
#print axioms Word.physicalBoundary
#print axioms Word.completePass
end H7846.Line24
