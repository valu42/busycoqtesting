import CompletePass
namespace H7846.Line24.Word
open TM

/-- At most one zero digit at the beginning. -/
def notDouble : Word → Prop
  | .tip _ => True
  | .d k z => k=0 → z.headOK

/-- Allow at most two consecutive empty digits. -/
def noTriple : Word → Prop
  | .tip _ => True
  | .d k z => z.noTriple ∧ (k=0 → z.notDouble)

theorem headNotDouble (x : Word) (h : x.headOK) : x.notDouble := by
  cases x with
  | tip => trivial
  | d k z => intro hk; change 0 < k at h; omega

theorem separatedNoTriple (x : Word) (h : x.separated) : x.noTriple := by
  induction x with
  | tip => trivial
  | d k z ih => exact ⟨ih h.1,fun e => headNotDouble z (h.2 e)⟩

theorem augmentNoTriple (k : Nat) (x : Word) (h : x.noTriple) : (augment k x).noTriple := by
  cases x with
  | tip => trivial
  | d n z => exact ⟨h.1,fun eq => h.2 (by change k+n=0 at eq; omega)⟩

theorem augmentOneReady (x : Word) (h : x.notDouble) : (augment 1 x).ready := by
  cases x with
  | tip => trivial
  | d n z => exact ⟨by change 0<1+n; omega,fun e => h (by change 1+n=1 at e; omega)⟩

/-- Structural induction tailored to a complete ready-word sweep. The split
case recurses on a word with augmented initial run and smaller total mass. -/
theorem readyInduction {P : Word → Prop}
    (tipCase : ∀ j, P (.tip j))
    (keepCase : ∀ i x, P x → P (.d (i+1) x))
    (splitCase : ∀ m z, P (augment 1 z) → P (.d (m+2) (.d 0 z)))
    (joinCase : ∀ i z, z.noTriple → P (.d (i+1) (.d 1 (.d 0 z))))
    (x : Word) (ok : x.noTriple) (hr : x.ready) : P x := by
  suffices allWords : ∀ n : Nat, ∀ x : Word, x.mass+x.digits ≤ n → x.noTriple → x.ready → P x from
    allWords _ x (Nat.le_refl _) ok hr
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
    intro x size ok hr
    match x with
    | .tip j =>
      exact tipCase j
    | .d 0 _ => exact False.elim (by have := hr.1; omega)
    | .d (i+1) x =>
      by_cases hx : x.ready
      · have hlt : x.mass+x.digits < n := by simp [mass,digits] at size; omega
        exact keepCase i x (ih _ hlt x (by omega) ok.1 hx)
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
            exact splitCase m z (ih _ hlt (augment 1 z) (by omega) (augmentNoTriple 1 z ok.1.1) (augmentOneReady z positive))
          | succ k =>
            cases k with
            | zero =>
              cases z with
              | tip j => exact False.elim (hx ⟨by decide,fun _ => trivial⟩)
              | d n w =>
                cases n with
                | zero => exact joinCase i w ok.1.1.1
                | succ n => exact False.elim (hx ⟨by decide,fun _ => Nat.zero_lt_succ _⟩)
            | succ k => exact False.elim (hx ⟨by omega,by omega⟩)


/-- A pass over a word with at most two consecutive zero digits. -/
structure WideAdvance (x y : Word) : Prop where
  clearance : ∃ t b, (b=0 ∨ b=4) ∧ x.digits+b = 3+y.digits ∧
    ∀ R, Timed (x.above (rep b [false] R)) (y.above R) t
  mass_eq : y.mass = x.mass
  clock_eq : y.clock = x.clock+1
  legal : y.noTriple

theorem completeWide (x : Word) (ok : x.noTriple) (hr : x.ready) :
    ∃ y, WideAdvance x y := by
  apply readyInduction (P := fun x => ∃ y, WideAdvance x y) _ _ _ _ x ok hr
  · intro j
    exact ⟨.d j (.tip 0),⟨_,atomClearance (Atom.tip j)⟩,by simp [mass],by simp [clock,mass,weight],
      ⟨trivial,fun _ => trivial⟩⟩
  · intro i z h
    obtain ⟨y,⟨⟨t,b,small,len,core⟩,hm,hc,legal⟩⟩ := h
    exact ⟨.d (i+1) y,⟨_,b,small,by simp only [digits]; omega,fun R => timedKeep i (core R)⟩,
      by simp [mass,hm],by simp [clock,hm,hc,Int.add_assoc],⟨legal,by omega⟩⟩
  · intro m z h
    obtain ⟨y,⟨⟨t,b,small,len,core⟩,hm,hc,legal⟩⟩ := h
    simp only [augmentMass,augmentClock,augmentDigits] at hm hc len
    refine ⟨.d m (.d 1 y),⟨14*m+32+t,b,small,by simp only [digits]; omega,?_⟩,
      by simp [mass,hm]; omega,?_,⟨⟨legal,by omega⟩,fun _ => by intro e; omega⟩⟩
    · intro R
      have r := core R
      rw [augmentAbove] at r
      exact timedSplitSuffix m r
    · simp only [clock,mass,hm,hc,Nat.zero_add,Nat.one_add,weight]; omega
  · intro i z legal
    refine ⟨augment (i+2) z,⟨14*(i+1)+18,0,Or.inl rfl,by simp [digits]; omega,?_⟩,
      by simp [mass]; omega,?_,augmentNoTriple _ _ legal⟩
    · intro R
      rw [augmentAbove]; exact timedJoin i (z.above R)
    · simp only [augmentClock,clock,mass,Nat.zero_add,Nat.one_add,weight]; omega

theorem wideDigitBounds (x : Word) (ok : x.noTriple) :
    x.digits ≤ 3*x.mass+2 ∧ (x.notDouble → x.digits ≤ 3*x.mass+1) ∧
      (x.headOK → x.digits ≤ 3*x.mass) := by
  induction x with
  | tip j => simp [digits,mass]
  | d k z ih =>
    obtain ⟨top,second,third⟩ := ih ok.1
    cases k with
    | zero =>
      have htop := second (ok.2 rfl)
      simp only [digits,mass,Nat.zero_add,notDouble,headOK]
      exact ⟨by omega,fun h => by have := third (h trivial); omega,by omega⟩
    | succ k =>
      simp only [digits,mass,notDouble,headOK]
      exact ⟨by omega,by omega,by omega⟩

private def wideRemaining (x : Word) : Int :=
  ((3*x.mass+2 : Nat) : Int) * ((2:Int)^(x.mass+1)-1) - x.clock

private theorem wideNonneg (x : Word) (ok : x.noTriple) : 0 ≤ wideRemaining x := by
  have top := x.clockCeiling
  have len := (wideDigitBounds x ok).1
  have nonneg : 0 ≤ (2:Int)^(x.mass+1)-1 := by
    have h : 0 < (2:Int)^(x.mass+1) := Int.pow_pos (by decide)
    omega
  have scale := Int.mul_le_mul_of_nonneg_right (Int.ofNat_le.mpr len) nonneg
  unfold wideRemaining
  omega

/-- Remaining ordinary passes at fixed mass, measured by the signed clock ceiling. -/
def wordRank (x : Word) : Nat := (wideRemaining x).toNat

theorem wordRank_decreases {x y : Word} (legal : y.noTriple)
    (hm : y.mass=x.mass) (hc : y.clock=x.clock+1) : wordRank y < wordRank x := by
  have a := wideNonneg y legal
  have e : wideRemaining y = wideRemaining x-1 := by unfold wideRemaining; rw [hm,hc]; omega
  unfold wordRank
  omega

#print axioms completeWide
#print axioms wordRank_decreases
end H7846.Line24.Word
