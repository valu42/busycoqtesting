import Machine

namespace H7846.Line24.CellPotential
open TM Lean.Grind AddCommMonoid AddCommGroup

variable {G : Type} [AddCommGroup G]

/-- Site weights are absolute, so residue classes, parity, and arbitrary
nonperiodic weightings are all admitted. Blank cells contribute zero. -/
private def val (w : Int → G) (i : Int) : Bool → G
  | true => w i
  | false => 0
private def move : Dir → Int → Int
  | .L,i => i-1
  | .R,i => i+1

/-- The equalities obtained by cancelling all unchanged cells in a single step. -/
def Balanced (Q : St → Int → G) (w : Int → G) : Prop :=
  ∀ q b i b' dir q', trans q b = some (b',dir,q') →
    Q q i + val w i b = Q q' (move dir i) + val w i b'

structure Shape (Q : St → Int → G) (w : Int → G) : Prop where
  twoPeriod : ∀ i, Q .D (i+2) = Q .D i
  state : ∀ q i, Q q i = match q with
    | .D | .E => Q .D i
    | _ => Q .D (i+1)
  change : ∀ i, Q .D (i+1) = Q .D i + w i
  adjacent : ∀ i, w (i+1) = w i
  torsion : ∀ i, w i + w i = 0

theorem classify {Q : St → Int → G} {w : Int → G} (h : Balanced Q w) : Shape Q w := by
  have c0 (i : Int) : Q .C i = Q .D (i-1) := by
    simpa only [val,move,add_zero] using h .C false i false .L .D rfl
  have c1 (i : Int) : Q .C i = Q .D (i+1) := by
    apply (add_left_inj (w i)).mp
    exact h .C true i true .R .D rfl
  have period (i : Int) : Q .D (i+2) = Q .D i := by
    have z := (c1 (i+1)).symm.trans (c0 (i+1))
    simpa only [show ∀ x : Int, x+1-1=x by omega,show i+1+1=i+2 by omega] using z
  have a (i : Int) : Q .A i = Q .D (i+1) := by
    have z := h .D false (i-1) false .R .A rfl
    simp only [val,move,add_zero,show i-1+1=i by omega] at z
    exact z.symm.trans ((c0 i).symm.trans (c1 i))
  have e (i : Int) : Q .E i = Q .D i := by
    have z : Q .E i = Q .C (i+1) := (add_left_inj (w i)).mp (h .E true i true .R .C rfl)
    rw [z,c1,show i+1+1=i+2 by omega,period]
  have f (i : Int) : Q .F i = Q .D (i+1) := by
    have z := h .E false (i-1) false .R .F rfl
    simp only [val,move,add_zero,show i-1+1=i by omega] at z
    exact z.symm.trans ((e _).trans ((c0 i).symm.trans (c1 i)))
  have change (i : Int) : Q .D (i+1) = Q .D i + w i := by
    have z := h .D true i false .R .E rfl
    simpa only [val,move,add_zero,e] using z.symm
  have b (i : Int) : Q .B i = Q .D (i+1) := by
    have z := h .B false i true .R .C rfl
    simpa only [val,move,add_zero,c1,show i+1+1=i+2 by omega,period,←change] using z
  have opposite (i : Int) : Q .D (i+1) + w i = Q .D i := by
    have z := h .A true i false .L .A rfl
    simpa only [val,move,add_zero,a,show i-1+1=i by omega] using z
  refine ⟨period,?_,change,?_,?_⟩
  · intro q i
    cases q <;> first | exact a i | exact b i | exact c1 i | exact e i | exact f i | rfl
  · intro i
    apply (add_right_inj (Q .D (i+1)) _ _).mp
    exact ((change (i+1)).symm.trans (by rw [show i+1+1=i+2 by omega,period])).trans (opposite i).symm
  · intro i
    apply (add_right_inj (Q .D i) _ _).mp
    rw [← add_assoc,← change,opposite,add_zero]

/-- No additive conserved site count separates blank A from B scanning the
first of two adjacent ones. This is a configuration comparison only. -/
theorem blankEqualsHalt {Q : St → Int → G} {w : Int → G} (h : Balanced Q w) :
    Q .A 0 = Q .B 0 + (w 0 + w 1) := by
  have sh := classify h
  rw [sh.state .A,sh.state .B,show w 1 = w 0 from sh.adjacent 0,sh.torsion,add_zero]

/-- With period three in the state/head correction, every cell weight vanishes. -/
theorem periodThree {Q : St → Int → G} {w : Int → G} (h : Balanced Q w)
    (p : ∀ i, Q .D (i+3) = Q .D i) : ∀ i, w i = 0 := by
  intro i
  have sh := classify h
  have same : Q .D (i+1) = Q .D i := (sh.twoPeriod (i+1)).symm.trans (by rw [show i+1+2=i+3 by omega,p])
  apply (add_right_inj (Q .D i) _ _).mp
  rw [← sh.change,same,add_zero]

theorem uniformWeight {Q : St → Int → G} {w : Int → G} (h : Balanced Q w) (i : Int) :
    w i = w 0 := by
  have adj := (classify h).adjacent
  cases i with
  | ofNat n =>
    induction n with
    | zero => rfl
    | succ n ih => exact (adj (Int.ofNat n)).trans ih
  | negSucc n =>
    induction n with
    | zero => exact (adj (-1)).symm
    | succ n ih =>
      have shift : Int.negSucc (n+1) + 1 = Int.negSucc n := by omega
      exact ((adj (Int.negSucc (n+1))).symm.trans (congrArg w shift)).trans ih

theorem witnessStopped : H7846.step ⟨blank,app [true,true] blank,.B⟩ = none := rfl

/-- The surviving parity bit really is conserved. -/
def parityState (q : St) (i : Int) : BitVec 1 :=
  match q with
  | .D | .E => BitVec.ofInt 1 i + 1
  | _ => BitVec.ofInt 1 i

theorem parityBalanced : Balanced parityState (fun _ => (1 : BitVec 1)) := by
  intro q b i x dir t h
  cases q <;> cases b <;> simp only [trans,Option.some.injEq,Prod.mk.injEq] at h
  all_goals first | contradiction | rcases h with ⟨rfl,rfl,rfl⟩
  all_goals simp only [parityState,val,move,Int.sub_eq_add_neg,BitVec.ofInt_add]
  all_goals generalize BitVec.ofInt 1 i = v; revert v; decide

/-- For the general form, cells on opposite sides may receive different
weights. The head carries an arbitrary charge depending on both state and bit. -/
def Centered (P : St → Int → Bool → G) (L R : Int → G) : Prop :=
  ∀ q b i b' dir q', trans q b = some (b',dir,q') → ∀ neighbor,
    match dir with
    | .R => P q i b + val R (i+1) neighbor = val L i b' + P q' (i+1) neighbor
    | .L => P q i b + val L (i-1) neighbor = val R i b' + P q' (i-1) neighbor

private theorem entersRight (q : St) : ∃ p b c, trans p b = some (c,.R,q) := by
  cases q with
  | A => exact ⟨.D,false,false,rfl⟩
  | B => exact ⟨.A,false,true,rfl⟩
  | C => exact ⟨.B,false,true,rfl⟩
  | D => exact ⟨.C,true,true,rfl⟩
  | E => exact ⟨.D,true,false,rfl⟩
  | F => exact ⟨.E,false,false,rfl⟩

theorem reduceCentered {P : St → Int → Bool → G} {L R : Int → G}
    (h : Centered P L R) :
    L = R ∧ (∀ q i b, P q i b = P q i false + val R i b) ∧
    Balanced (fun q i => P q i false) R := by
  have bit (q : St) (i : Int) : P q i true = P q i false + R i := by
    obtain ⟨p,b,c,eq⟩ := entersRight q
    have z := h p b (i-1) c .R q eq false
    have o := h p b (i-1) c .R q eq true
    simp only [val,add_zero,show i-1+1=i by omega] at z o
    apply (add_right_inj (val L (i-1) c) _ _).mp
    unfold val
    rw [←o,←add_assoc,←z]
  have lr : L=R := by
    funext i
    have z := h .A true (i+1) false .L .A rfl false
    have o := h .A true (i+1) false .L .A rfl true
    simp only [val,add_zero,zero_add,show i+1-1=i by omega] at z o
    rw [z,bit] at o
    exact (add_right_inj _ _ _).mp o
  have localForm (q : St) (i : Int) (b : Bool) : P q i b = P q i false + val R i b := by
    cases b with
    | false => exact (add_zero _).symm
    | true => exact bit _ _
  refine ⟨lr,localForm,?_⟩
  intro q b i x dir t eq
  have z := h q b i x dir t eq false
  cases dir <;> simp only [val,add_zero,lr] at z <;>
    exact (localForm q i b).symm.trans (z.trans (add_comm _ _))

theorem centeredBlankEqualsHalt {P : St → Int → Bool → G} {L R : Int → G}
    (h : Centered P L R) : P .A 0 false = P .B 0 true + R 1 := by
  obtain ⟨_,localForm,balanced⟩ := reduceCentered h
  rw [localForm .B 0 true,add_assoc]
  exact blankEqualsHalt balanced

#print axioms classify
#print axioms blankEqualsHalt
end H7846.Line24.CellPotential
