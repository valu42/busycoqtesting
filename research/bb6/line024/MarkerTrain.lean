import MarkerPass
import Box

namespace H7846.Line24
open TM Word

/-- A finite train of six-one markers. Each marker has its indicated gap before
it and four reserved zeros after it. The train ends in blank or an opaque wing. -/
inductive MarkerTrain where
  | blank
  | edge (gap : Nat)
  | marker (gap : Nat) (rest : MarkerTrain)

namespace MarkerTrain
def tape : MarkerTrain → Tape → Tape
  | .blank, _ => TM.blank
  | .edge g, R => rep g [false] R
  | .marker g rest, R => sixMarker g (rest.tape R)

def count : MarkerTrain → Nat
  | .blank | .edge _ => 0
  | .marker _ rest => rest.count+1

def hasWing : MarkerTrain → Bool
  | .blank => false
  | .edge _ => true
  | .marker _ rest => rest.hasWing

/-- No six-one marker begins one cell modulo three to the right of the
visit head. The counter length through its tip, including the leading 10,
is 3*mass + digits + 9, so the initial offset is just the digit count. -/
def aligned (f : MarkerTrain) (offset : Nat) : Prop :=
  match f with
  | .blank | .edge _ => True
  | .marker g rest => (offset+g)%3 ≠ 1 ∧ rest.aligned (offset+g+10)

private theorem changeOffset (f : MarkerTrain) {i j : Nat} (h : i%3=j%3)
    (ok : f.aligned i) : f.aligned j := by
  induction f generalizing i j with
  | blank | edge => trivial
  | marker g rest ih =>
    exact ⟨by have a := ok.1; omega,
      ih (by omega) ok.2⟩

/-- A short final gap whose following bits have no specified pattern. -/
def atEdge : MarkerTrain → Prop
  | .edge g => g<4
  | _ => False

private def spend : MarkerTrain → Nat → MarkerTrain
  | .blank, _ => .blank
  | .edge g, b => .edge (g-b)
  | .marker g rest, b => .marker (g-b) rest

private def clear : MarkerTrain → Prop
  | .blank => True
  | .edge g | .marker g _ => 4 ≤ g

private theorem spendTape (f : MarkerTrain) (h : f.clear) (b : Nat) (hb : b≤4) (R : Tape) :
    f.tape R = rep b [false] ((f.spend b).tape R) := by
  cases f with
  | blank => exact (Box.zeroBlank b).symm
  | edge g =>
    change rep g [false] R = rep b [false] (rep (g-b) [false] R)
    rw [← rep_add]; congr 1; change 4≤g at h; omega
  | marker g rest =>
    change rep g [false] _ = rep b [false] (rep (g-b) [false] _)
    rw [← rep_add]; congr 1; change 4≤g at h; omega

private theorem spendAligned (f : MarkerTrain) (h : f.clear) {b i j : Nat} (hb : b≤4)
    (len : i+b = 3+j) (ok : f.aligned i) : (f.spend b).aligned j := by
  cases f with
  | blank | edge => trivial
  | marker g rest =>
    change 4≤g at h
    have a := ok.1
    exact ⟨by omega,changeOffset _ (by omega) ok.2⟩

private structure Progress (x : Word) (f : MarkerTrain) (y : Word) (u : MarkerTrain) : Prop where
  run : ∃ t, ∀ R, Timed (x.above (f.tape R)) (y.above (u.tape R)) t
  legal : y.noTriple
  total : y.mass+2*u.count = x.mass+2*f.count
  wing : u.hasWing=f.hasWing
  align : f.aligned x.digits → u.aligned y.digits
  decrease : u.count < f.count ∨ (u.count = f.count ∧ wordRank y < wordRank x)

private theorem clearStep {x : Word} (ok : x.noTriple) (hr : x.ready)
    (f : MarkerTrain) (h : f.clear) : ∃ y u, Progress x f y u := by
  obtain ⟨y,⟨⟨t,b,small,len,core⟩,mass,clock,legal⟩⟩ := completeWide x ok hr
  have c : (f.spend b).count=f.count := by cases f <;> rfl
  have o : (f.spend b).hasWing=f.hasWing := by cases f <;> rfl
  refine ⟨y,f.spend b,⟨t,?_⟩,legal,by rw [c,mass],o,spendAligned f h (by omega) len,Or.inr ⟨c,wordRank_decreases legal mass clock⟩⟩
  intro R
  rw [spendTape f h b (by omega) R]
  exact core _

private theorem one {x : Word} (ok : x.noTriple) (hr : x.ready)
    (f : MarkerTrain) (away : ¬f.atEdge) : ∃ y u, Progress x f y u := by
  by_cases h : f.clear
  · exact clearStep ok hr f h
  cases f with
  | blank => exact (h trivial).elim
  | edge g => exact False.elim (by change ¬4≤g at h; change ¬g<4 at away; omega)
  | marker g rest =>
    change ¬4≤g at h
    obtain ⟨y,b,⟨⟨t,core⟩,legal,mass,len,clock,_⟩⟩ := completeMarkerPass g (by omega) x ok hr
    cases b with
    | true =>
      refine ⟨y,rest,⟨t,fun R => core (rest.tape R)⟩,legal,?_,rfl,?_,Or.inl (by simp [count])⟩
      · simp [count,mass]; omega
      · intro aligned
        simp only [ite_true] at len
        exact changeOffset _ (by omega) aligned.2
    | false =>
      simp only [Bool.false_eq_true,ite_false,Nat.add_zero] at mass
      exact ⟨y,.marker g rest,⟨t,fun R => core (rest.tape R)⟩,legal,by rw [mass],rfl,fun ok => changeOffset _ (by simp at len; omega) ok,
        Or.inr ⟨rfl,wordRank_decreases legal mass (clock rfl)⟩⟩

/-- Every train is traversed in finitely many passes up to a wall boundary or
the last opaque gap. The mass plus two per surviving marker is conserved. -/
theorem traverse (x : Word) (f : MarkerTrain) (ok : x.noTriple) :
    ∃ (y : Word) (u : MarkerTrain) (k t : Nat), (¬y.ready ∨ u.atEdge) ∧ y.noTriple ∧
      y.mass+2*u.count = x.mass+2*f.count ∧ u.hasWing=f.hasWing ∧ (f.aligned x.digits → u.aligned y.digits) ∧ ∀ L R,
      steps t (visitX L [] (x.above (f.tape R))) =
        some (visitX (rep (3*k) [true] L) [] (y.above (u.tape R))) := by
  by_cases done : ¬x.ready ∨ f.atEdge
  · exact ⟨x,f,0,0,done,ok,rfl,rfl,id,fun _ _ => rfl⟩
  have ready : x.ready := Classical.byContradiction (fun hn => done (Or.inl hn))
  obtain ⟨y,u,⟨⟨t,step⟩,legal,mass,wing,align,smaller⟩⟩ := one ok ready f (fun h => done (Or.inr h))
  obtain ⟨z,v,k,n,last,good,total,finalWing,finalAlign,run⟩ := traverse y u legal
  refine ⟨z,v,1+k,(t+15)+n,last,good,total.trans mass,finalWing.trans wing,fun h => finalAlign (align h),?_⟩
  intro L R
  have a := steps_seq trans (step R (cons false L)) (wall_turn L (y.above (u.tape R)))
  have path := steps_seq trans a (run (rep 3 [true] L) R)
  rw [show 3*(1+k)=3*k+3 by omega,rep_add (3*k) 3]
  exact path
termination_by (f.count,wordRank x)
decreasing_by
  rcases smaller with less | ⟨eq,rank⟩
  · exact Prod.Lex.left _ _ less
  · rw [eq]; exact Prod.Lex.right _ rank

/-- The three possible exits from the train traversal with nested wall openings. -/
inductive Exit (hasFarWing : Bool) (initialAlignment : Prop) (R : Tape) : Config → Prop where
  | empty (P : Tape) (x : Word) (f : MarkerTrain) (wing : f.hasWing=hasFarWing) :
      Exit hasFarWing initialAlignment R (visitX P [0] (x.above (f.tape R)))
  | landing (P : Tape) (f : MarkerTrain) (wing : f.hasWing=hasFarWing)
      (safe : initialAlignment → f.aligned 2) :
      Exit hasFarWing initialAlignment R ⟨P,f.tape R,.D⟩
  | edge (P : Tape) (x : Word) (g : Nat) (short : g < 4) (wing : hasFarWing=true) :
      Exit hasFarWing initialAlignment R (visitX P [] (x.above (rep g [false] R)))

private theorem boundary (x : Word) (nx : ¬x.ready) : x.boundary := by
  cases x with
  | tip => exact False.elim (nx trivial)
  | d n z =>
    cases n with
    | zero => exact Or.inl ⟨z,rfl⟩
    | succ n =>
      cases n with
      | succ k => exact False.elim (nx ⟨by omega,by omega⟩)
      | zero =>
        cases z with
        | tip j => exact False.elim (nx ⟨by decide,fun _ => trivial⟩)
        | d j w => cases j with
          | zero => exact Or.inr ⟨w,rfl⟩
          | succ j => exact False.elim (nx ⟨by decide,fun _ => Nat.zero_lt_succ _⟩)

/-- Even arbitrarily many intervening 1,0,digit wall openings cannot postpone
the next empty-wall event, terminal D landing, or uncharacterized far wing forever. -/
private theorem openings (H : Prop) (x : Word) (f : MarkerTrain) (ok : x.noTriple) (ha : H → f.aligned x.digits) (L R : Tape) :
    ∃ n c, steps n (visitX L [] (x.above (f.tape R))) = some c ∧ Exit f.hasWing H R c := by
  obtain ⟨y,u,k,t,stop,legal,total,wing,align,h⟩ := traverse x f ok
  have path := h L R
  let P := rep (3*k) [true] L
  rcases stop with stop | edge
  · rcases boundary y stop with ⟨z,rfl⟩ | ⟨z,rfl⟩
    · exact ⟨t,_,path,Exit.empty P z u wing⟩
    · cases z with
      | tip j =>
        have run := wallTail j P (u.tape R)
        have endRun := steps_seq trans path run
        exact ⟨_,_,endRun,Exit.landing _ _ wing (fun h => align (ha h))⟩
      | d j z =>
        have run := wallNextDigit j P (z.above (u.tape R))
        let P' := rep (j+1) [true,true,false] (rep 3 [true] P)
        have less : z.mass+2*u.count < x.mass+2*f.count := by
          simp only [mass] at total; omega
        obtain ⟨n,c,next,finish⟩ := openings H z u legal.1.1.1 (fun h =>
          changeOffset _ (by simp [digits]; omega) (align (ha h))) P' R
        rw [wing] at finish
        exact ⟨_,c,steps_seq trans (steps_seq trans path run) next,finish⟩
  · cases u with
    | blank => contradiction
    | marker => contradiction
    | edge g => exact ⟨t,_,path,Exit.edge P y g edge wing.symm⟩
termination_by x.mass+2*f.count

theorem throughOpenings (x : Word) (f : MarkerTrain) (ok : x.noTriple) (L R : Tape) :
    ∃ n c, steps n (visitX L [] (x.above (f.tape R))) = some c ∧ Exit f.hasWing (f.aligned x.digits) R c :=
  openings _ x f ok id L R

/-- At an aligned landing whose first exterior is known, the three scanned
cells cannot be the fatal 001. This also applies to an isolated train before
a still-opaque distant wing, whenever a marker remains. -/
theorem safeLanding (f : MarkerTrain) (a : f.aligned 2)
    (known : ∀ g, f ≠ .edge g) (R : Tape) :
    ¬(f.tape R 0 = false ∧ f.tape R 1 = false ∧ f.tape R 2 = true) := by
  cases f with
  | blank => simp [tape,TM.blank]
  | edge g => exact (known g rfl).elim
  | marker g rest =>
    have h := a.1
    have ne : g≠2 := by omega
    cases g with
    | zero => intro z; exact Bool.false_ne_true z.1.symm
    | succ g =>
      cases g with
      | zero => intro z; exact Bool.false_ne_true z.2.1.symm
      | succ g =>
        cases g with
        | zero => exact (ne rfl).elim
        | succ g => intro z; exact Bool.false_ne_true z.2.2

end MarkerTrain
#print axioms MarkerTrain.traverse
#print axioms MarkerTrain.throughOpenings
end H7846.Line24
