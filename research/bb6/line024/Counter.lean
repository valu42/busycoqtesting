import Wall

namespace H7846.Line24
open TM

/-- A list of counter digits with a final tail index. -/
inductive Word where
  | tip : Nat → Word
  | d : Nat → Word → Word
  deriving Repr, DecidableEq

namespace Word
def tape : Word → Tape
  | tip j => tailT j
  | d k x => blkV k x.tape

def mass : Word → Nat
  | tip j => j
  | d k x => k + x.mass

/-- Weight of a digit separator with s units to its right. -/
def weight : Nat → Int
  | 0 => 1
  | s+1 => -1-2*weight s

def clock : Word → Int
  | tip _ => 0
  | d _ x => weight x.mass + x.clock

def headOK : Word → Prop
  | tip _ => True
  | d k _ => 0 < k

def separated : Word → Prop
  | tip _ => True
  | d k x => x.separated ∧ (k = 0 → x.headOK)

def digits : Word → Nat
  | tip _ => 0
  | d _ x => 1+x.digits

/-- One ordinary pass. Boundary collisions are handled separately in Wall.lean. -/
inductive Pass : Word → Word → Prop
  | tipStep (j) : Pass (tip j) (d j (tip 0))
  | keep (i) {x y} : Pass x y → Pass (d (i+1) x) (d (i+1) y)
  | split (m) : Pass (d (m+2) (d 0 (tip 0))) (d m (d 1 (d 1 (tip 0))))
  | mergeTail (i) : Pass (d (i+1) (d 1 (d 0 (tip 0)))) (tip (i+2))
  | mergeDigit (i) (y) : Pass (d (i+1) (d 1 (d 0 (d 1 y)))) (d (i+3) y)
  | carry (m) {x y} : Pass x y → Pass (d (m+2) (d 0 (d 1 x))) (d m (d 1 (d 2 y)))

theorem joinTailTape (i : Nat) : rep (i+2) [true,true,true] (tailT 0) = tailT (i+2) := by
  induction i with
  | zero => rfl
  | succ i ih =>
    unfold tailT at *
    rw [show 7 + 3*(i+1+2) = (7+3*(i+2))+3 by omega]
    change app [true,true,true] _ = app [true,true,true] _
    rw [ih]

theorem passCore {x y} (h : Pass x y) : Core x.tape y.tape := by
  induction h with
  | tipStep j => cases j with
    | zero => exact zeroTail
    | succ i => exact Line24.tail i
  | keep i _ ih => exact keepDigit ih i
  | split m => exact splitEnd m
  | mergeTail i =>
    change Core _ (tailT (i+2))
    rw [← joinTailTape]
    exact joinRun i (tailT 0)
  | mergeDigit i y =>
    have h := joinRun i (blkV 1 y.tape)
    change Core _ (rep (i+2) [true,true,true] (app [true,true,true] (cons false y.tape))) at h
    rw [rep_app_comm] at h
    exact h
  | carry m _ ih => exact bounce m ih

theorem passVisit {x y} (h : Pass x y) (L : Tape) :
    ∃ n, steps n (visitX L [] x.tape) = some (visitX (rep 3 [true] L) [] y.tape) :=
  liftVisit (passCore h) L

theorem accounting {x y} (h : Pass x y) :
    y.mass = x.mass ∧ y.clock = x.clock+1 ∧ (x.separated → y.separated) := by
  induction h with
  | tipStep j => simp [mass, clock, weight, separated, headOK]
  | keep i _ ih =>
    obtain ⟨hm,hc,hs⟩ := ih
    simp [mass, clock, separated, hm, hc, Int.add_assoc]
    exact hs
  | split m => simp [mass,clock,weight,separated,headOK]
  | mergeTail i => simp [mass,clock,weight,separated,headOK]
  | mergeDigit i y =>
    simp [mass, clock, separated, headOK]
    simp only [Nat.one_add, Nat.succ_eq_add_one, weight]
    omega
  | carry m _ ih =>
    obtain ⟨hm,hc,hs⟩ := ih
    simp [mass, clock, separated, headOK, hm, hc]
    simp only [Nat.one_add, Nat.succ_eq_add_one, show ∀ n : Nat, 2+n=n+1+1 by omega, weight]
    exact ⟨by omega, by omega, hs⟩

theorem digitBound (x : Word) (h : x.separated) :
    x.digits ≤ 2*x.mass+1 ∧ (x.headOK → x.digits ≤ 2*x.mass) := by
  induction x with
  | tip j => simp [digits,mass]
  | d n x ih =>
    obtain ⟨hx,hh⟩ := h
    obtain ⟨b,b'⟩ := ih hx
    cases n with
    | zero =>
      have b₀ := b' (hh rfl)
      simp [digits,mass,headOK]; omega
    | succ n => simp [digits,mass,headOK]; omega


private def cap (m : Nat) : Int := (2:Int)^(m+1)-1

private theorem weightBounds (j : Nat) : -cap j ≤ weight j ∧ weight j ≤ cap j := by
  induction j with
  | zero => decide
  | succ j ih =>
    simp only [cap] at *
    rw [weight, Int.pow_succ (2:Int) (j+1)]
    omega

private theorem capMono {j m : Nat} (h : j ≤ m) : cap j ≤ cap m := by
  obtain ⟨n,rfl⟩ := Nat.exists_eq_add_of_le h
  induction n with
  | zero => exact Int.le_refl _
  | succ n ih =>
    unfold cap at *
    rw [show j+(n+1)+1 = (j+n+1)+1 by omega, Int.pow_succ (2:Int) (j+n+1)]
    have hp : 0 ≤ (2:Int)^(j+n+1) := Int.pow_nonneg (by decide)
    omega

private theorem clockBounds (x : Word) (m : Nat) (hm : x.mass ≤ m) :
    -(x.digits : Int) * cap m ≤ x.clock ∧ x.clock ≤ (x.digits : Int) * cap m := by
  induction x with
  | tip j => simp [digits,clock]
  | d k x ih =>
    change k+x.mass ≤ m at hm
    have hx : x.mass ≤ m := by omega
    obtain ⟨lo,hi⟩ := ih hx
    obtain ⟨wlo,whi⟩ := weightBounds x.mass
    have hcap := capMono hx
    simp only [digits,clock,Int.natCast_add,Int.cast_ofNat_Int,
      Int.neg_add,Int.add_mul,Int.one_mul,Int.neg_one_mul]
    omega

/-- Exactly k ordinary passes. -/
inductive Passes : Nat → Word → Word → Prop
  | refl (x) : Passes 0 x x
  | next {k x y z} : Passes k x y → Pass y z → Passes (k+1) x z

theorem passCount {k x y} (h : Passes k x y) :
    y.mass=x.mass ∧ y.clock=x.clock+k ∧ (x.separated → y.separated) := by
  induction h with
  | refl x => simp
  | next _ step ih =>
    obtain ⟨a,b,c⟩ := accounting step
    obtain ⟨d,e,f⟩ := ih
    exact ⟨a.trans d, by rw [b,e]; omega, fun h => c (f h)⟩

/-- A separated counter of fixed mass must leave the ordinary-pass relation in finite time. -/
theorem phaseBound {k x y} (h : Passes k x y) (ok : x.separated) :
    (k:Int) ≤ ((2*x.mass+1:Nat):Int) * ((2:Int)^(x.mass+1)-1) - x.clock := by
  obtain ⟨hm,hc,hs⟩ := passCount h
  have digit := (digitBound y (hs ok)).1
  rw [hm] at digit
  have top := (clockBounds y x.mass (Nat.le_of_eq hm)).2
  have nneg : 0 ≤ cap x.mass := by
    have h := capMono (Nat.zero_le x.mass)
    change (1:Int) ≤ cap x.mass at h
    omega
  have hmul := Int.mul_le_mul_of_nonneg_right (Int.ofNat_le.mpr digit) nneg
  unfold cap at top hmul
  omega

end Word
end H7846.Line24
