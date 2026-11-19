import Machine

namespace H7846.Line24.PackedTape

open TM
abbrev Runs := List (Bool × Nat)

structure Pack where
  l : Runs
  r : Runs
  st : St
  deriving Repr, DecidableEq

/-- Attach a list of nearest-first runs to an arbitrary continuation. -/
def denoteWith : Runs → Tape → Tape
  | [], tail => tail
  | (b,n)::xs, tail => rep n [b] (denoteWith xs tail)

def denote (xs : Runs) : Tape := denoteWith xs blank

def Pack.toCfg (c : Pack) : Config := ⟨denote c.l,denote c.r,c.st⟩

/-- On canonical tapes this keeps runs maximal, suppresses zero lengths, and
leaves the infinite blank suffix implicit. -/
def push (b : Bool) (n : Nat) (xs : Runs) : Runs :=
  if n = 0 then xs else
  match xs with
  | [] => if b then [(true,n)] else []
  | (h,k)::tail => if b = h then (b,n+k)::tail else (b,n)::xs

private theorem blankZeros (n : Nat) : rep n [false] blank = blank := by
  induction n with
  | zero => rfl
  | succ n ih => rw [rep_succ,ih]; exact cons_false_blank

theorem denotePush (b : Bool) (n : Nat) (xs : Runs) :
    denote (push b n xs) = rep n [b] (denote xs) := by
  by_cases z : n = 0
  · subst n; rfl
  · cases xs with
    | nil =>
      cases b with
      | false => simpa [push,z,denote,denoteWith] using (blankZeros n).symm
      | true => simp [push,z,denote,denoteWith]
    | cons h xs =>
      obtain ⟨d,k⟩ := h
      by_cases e : b = d
      · subst d; simp [push,z,denote,denoteWith,rep_add]
      · simp [push,z,e,denote,denoteWith]

def prepend (rs xs : Runs) : Runs := rs.foldr (fun p t => push p.1 p.2 t) xs

theorem denotePrepend (rs xs : Runs) : denote (prepend rs xs) = denoteWith rs (denote xs) := by
  induction rs with
  | nil => rfl
  | cons h rs ih =>
    obtain ⟨b,n⟩ := h
    change denote (push b n (prepend rs xs)) = rep n [b] (denoteWith rs (denote xs))
    rw [denotePush,ih]

/-- Drop the nearest cell. Empty represents blank in both directions. -/
def pop : Runs → Bool × Runs
  | [] => (false,[])
  | (_,0)::xs => pop xs
  | (b,1)::xs => (b,xs)
  | (b,n+2)::xs => (b,(b,n+1)::xs)

theorem denotePop (xs : Runs) : cons (pop xs).1 (denote (pop xs).2) = denote xs := by
  induction xs with
  | nil => exact cons_false_blank
  | cons h xs ih =>
    obtain ⟨b,n⟩ := h
    cases n with
    | zero => exact ih
    | succ n => cases n <;> rfl

theorem popHead (xs : Runs) : (denote xs) 0 = (pop xs).1 := by
  rw [← denotePop xs]; rfl

theorem popTail (xs : Runs) : TM.tail (denote xs) = denote (pop xs).2 := by
  rw [← denotePop xs]; rfl

def step (c : Pack) : Option Pack :=
  let (b,rest) := pop c.r
  match trans c.st b with
  | none => none
  | some (w,.R,q) => some ⟨push w 1 c.l,rest,q⟩
  | some (w,.L,q) =>
    let (a,left) := pop c.l
    some ⟨left,push a 1 (push w 1 rest),q⟩

theorem stepEq (c : Pack) : H7846.step c.toCfg = (step c).map Pack.toCfg := by
  unfold H7846.step TM.step step Pack.toCfg
  simp only [popHead,popTail]
  cases h : trans c.st (pop c.r).1 with
  | none => rfl
  | some p =>
    obtain ⟨w,dir,q⟩ := p
    cases dir <;> simp only [Option.map_some,denotePush] <;> rfl

def run : Nat → Pack → Option Pack
  | 0,c => some c
  | n+1,c => match step c with
    | some d => run n d
    | none => none

theorem runEq (n : Nat) (c : Pack) : H7846.steps n c.toCfg = (run n c).map Pack.toCfg := by
  induction n generalizing c with
  | zero => rfl
  | succ n ih =>
    unfold H7846.steps
    have one : TM.step trans c.toCfg = (step c).map Pack.toCfg := stepEq c
    rw [TM.steps,one,run]
    cases step c with
    | none => rfl
    | some d => exact ih d

theorem runSound {n : Nat} {c d : Pack} (h : run n c = some d) :
    H7846.steps n c.toCfg = some d.toCfg := by
  rw [runEq,h]; rfl

end H7846.Line24.PackedTape
