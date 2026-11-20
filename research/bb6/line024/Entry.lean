import Counter

namespace H7846.Line24
open TM Word

/-- Counter word at the checkpoint, with the last natural as the tail index. -/
def word (ds : List Nat) (j : Nat) : Word := ds.foldr Word.d (.tip j)

def startWord := word [4,2,1,1,1,2,1,1,8,1,1,8,4,4,3,1,0,1,0] 0

def runs (xs : List (Bool × Nat)) : List Bool :=
  xs.flatMap (fun (b,n) => List.replicate n b)

private def outerBits := runs [(true,5),(false,1),(true,2),(false,1),(true,3)]
def exterior : Tape := app outerBits blank

private def entry : FCfg St :=
  ⟨false :: (List.replicate 82430 true ++ [false,true,true,false] ++ List.replicate 1322 true ++ false :: outerBits),
   runs [(true,1),(false,1),(true,12),(false,1),(true,6),(false,1),(true,3),(false,1),
         (true,3),(false,1),(true,3),(false,1),(true,6),(false,1),(true,3),(false,1),
         (true,3),(false,1),(true,24),(false,1),(true,3),(false,1),(true,3),(false,1),
         (true,24),(false,1),(true,12),(false,1),(true,12),(false,1),(true,9),(false,1),
         (true,3),(false,2),(true,3),(false,2),(true,7)], .D⟩

private theorem appRep (n : Nat) (b : Bool) (xs : List Bool) :
    app (List.replicate n b ++ xs) blank = rep n [b] (app xs blank) := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [List.replicate_succ,List.cons_append,app_cons,rep_succ,app]; rw [ih]

def wallBase := cons false (oldWall 1320 exterior)
def entryCfg := visitX (rep 82430 [true] wallBase) [] startWord.tape

private theorem entry_eq : entry.toCfg = entryCfg := by
  apply TM.Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  refine ⟨?_,rfl,rfl⟩
  change app (false :: (List.replicate 82430 true ++ [false,true,true,false] ++ List.replicate 1322 true ++ false :: outerBits)) blank = _
  rw [List.append_assoc, List.append_assoc, app_cons, appRep]
  change cons false (rep 82430 [true] (app [false,true,true,false]
    (app (List.replicate 1322 true ++ false :: outerBits) blank))) = _
  rw [appRep]
  rfl

/-- The bounded physical prefix. -/
theorem blankEntry : steps 20656445 init = some entryCfg := by
  rw [← entry_eq]
  apply blank_reaches
  decide +native

end H7846.Line24
