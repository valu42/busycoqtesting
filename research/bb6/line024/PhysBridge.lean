import Entry

namespace H7846.Line24
open TM
set_option maxRecDepth 15000

namespace PhysicalWindow

/-- A bounded window with independently replaceable tapes on both sides. -/
def window (c : FCfg St) (L R : Tape) : Config :=
  ⟨app c.l L,app c.r R,c.st⟩

/-- Both buffers must be nonempty before executing an instruction. In
particular, no instruction ever reads the right exterior, even if the very
last move puts the head on its first cell. -/
def inside : Nat → FCfg St → Option (FCfg St)
  | 0,c => some c
  | n+1,c => if c.l.isEmpty || c.r.isEmpty then none else (fstep c).bind (inside n)

private theorem winOne (c : FCfg St) (L R : Tape)
    (h : (c.l.isEmpty || c.r.isEmpty) = false) :
    step (window c L R) = (fstep c).map (fun d => window d L R) := by
  obtain ⟨ls,rs,st⟩ := c
  cases ls with
  | nil => contradiction
  | cons b ls =>
    cases rs with
    | nil => contradiction
    | cons a rs =>
      unfold step TM.step fstep TM.fstep window
      simp only [app_cons,cons_zero,List.headD_cons]
      cases trans st a with
      | none => rfl
      | some p =>
        obtain ⟨w,d,q⟩ := p
        cases d <;> rfl

theorem winRun {n : Nat} {a b : FCfg St} (h : inside n a = some b)
    (L R : Tape) : steps n (window a L R) = some (window b L R) := by
  induction n generalizing a with
  | zero => simp [inside] at h; subst b; rfl
  | succ n ih =>
    cases g : a.l.isEmpty || a.r.isEmpty with
    | true => simp [inside,g] at h
    | false =>
      cases v : fstep a with
      | none => simp [inside,g,v] at h
      | some d =>
        simp [inside,g,v] at h
        have z := winOne a L R g
        rw [v,Option.map_some] at z
        exact (steps_succ_of_step trans n z).trans (ih h)

end PhysicalWindow
open PhysicalWindow

def bridgeDigits : List Nat := [1,2,2,3,3,2,2,3,1,1,1,1,2,3,0]
def impactDigits : List Nat := [1,2,2,3,3,2,2,3,1]

private def rightBuffer (ds : List Nat) (ones zeros : Nat) : List Bool :=
  [true,false] ++ ds.flatMap (fun d => List.replicate (3*d) true ++ [false]) ++
  List.replicate ones true ++ List.replicate zeros false

private def start : FCfg St := ⟨[false,true],rightBuffer bridgeDigits 7 411,.D⟩
private def before : FCfg St :=
  ⟨false :: List.replicate 415 true,rightBuffer impactDigits 31 3,.D⟩

def bridgeStart (L R : Tape) : Config :=
  ⟨cons false (cons true L),app [true,false] (sq blkV bridgeDigits
    (rep 7 [true] (rep 411 [false] R))),.D⟩

def preImpact (L R : Tape) : Config :=
  ⟨cons false (rep 415 [true] L),app [true,false] (sq blkV impactDigits
    (rep 31 [true] (rep 3 [false] R))),.D⟩

/-- From the last guarded jump, 138 more ordinary passes lead to the
three-cell clearance. The unseen right suffix may start with either bit. -/
theorem toPreImpact (L R : Tape) : steps 67100 (bridgeStart L R) =
    some (preImpact L R) := by
  have h : inside 67100 start = some before := by decide +native
  exact winRun h L R

/-- The 142nd move of the next sweep places the head on the first exterior
cell in F. Even if this cell is changed, the entire preceding path still works. -/
theorem contactWithFixedLeft (L : Tape) : ∃ P, ∀ R : Tape,
    steps 142 (preImpact L R) = some ⟨P,R,.F⟩ := by
  let c := (inside 142 before).getD before
  have h : inside 142 before = some c ∧ c.r = [] ∧ c.st = .F := by decide +native
  obtain ⟨run,r,s⟩ := h
  refine ⟨app c.l L,fun R => ?_⟩
  have z := winRun run L R
  unfold window at z
  rw [r,s] at z
  exact z

theorem atFirstContact (L R : Tape) : ∃ P, steps 142 (preImpact L R) =
    some ⟨P,R,.F⟩ := by
  obtain ⟨P,h⟩ := contactWithFixedLeft L
  exact ⟨P,h R⟩
#print axioms toPreImpact
#print axioms atFirstContact
end H7846.Line24
