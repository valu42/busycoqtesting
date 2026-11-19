import Return

namespace H7846.Line24
open TM
set_option maxRecDepth 40000

private def leftWord := runs [(true,5),(false,1),(true,2),(false,1),(true,3)]
private def frontWord := runs [(false,1324),(true,6),(false,8628),(true,6)]
private theorem frontLength : frontWord.length = 9964 := by decide +native

private def comparison (addMarker : Bool) : FCfg St :=
  ⟨leftWord, frontWord ++ (if addMarker then runs [(false,8626),(true,6)] else []),.A⟩

private theorem observed {a f : FCfg St} {t : Nat} {b : Bool}
    (zf : TM.fsteps trans t a = some f) (st : f.st = .B) (bit : f.r.headD false = b) :
    ∃ d, steps t a.toCfg = some d ∧ d.st = .B ∧ d.r 0 = b := by
  have r := FCfg.steps_eq trans t a
  rw [zf,Option.map_some] at r
  exact ⟨f.toCfg,r,st,(app_head f.r).trans bit⟩

private theorem observation {t : Nat} {a : FCfg St} {b : Bool}
    (check : (TM.fsteps trans t a).map (fun f => (f.st,f.r.headD false)) = some (.B,b)) :
    ∃ d, steps t a.toCfg = some d ∧ d.st = .B ∧ d.r 0 = b := by
  cases h : TM.fsteps trans t a with
  | none => simp [h] at check
  | some f =>
    rw [h,Option.map_some] at check
    have e := Option.some.inj check
    exact observed h (congrArg Prod.fst e) (congrArg Prod.snd e)

private theorem sample (b : Bool) :
    ∃ d, steps 1394298 (comparison b).toCfg = some d ∧ d.st = .B ∧ d.r 0 = b := by
  apply observation
  cases b <;> decide +native

private theorem asRepeat (n : Nat) (b : Bool) (X : Tape) :
    app (List.replicate n b) X = rep n [b] X := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [List.replicate_succ,app_cons,rep_succ,app]; rw [ih]

private theorem frontTape (X : Tape) :
    app frontWord X = rep 1324 [false] (rep 6 [true] (rep 8628 [false] (rep 6 [true] X))) := by
  unfold frontWord runs
  simp only [List.flatMap_cons,List.flatMap_nil,List.append_nil,← app_app,asRepeat]

private theorem nextGap : ∃ X : Tape, (regenerated returnedWidths exterior).r =
    app frontWord (rep 107996733 [false] X) := by
  refine ⟨rep 6 [true] (markers [0,6,30,126,510,2046,8190,32766,131070,524286,2097150,8388606,33554430] clearTail),?_⟩
  rw [frontTape]
  rw [show 1324=4+1320 by decide,rep_add 4 1320]
  rfl

private theorem blankCut (n : Nat) (X : Tape) : Box.cut n (rep n [false] X) blank = blank := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change cons false (Box.cut n (rep n [false] X) blank) = blank
    rw [ih]; exact cons_false_blank

private theorem actualAgreement : Locality.Agree (1394298+1) (comparison false).toCfg secondRestart := by
  refine ⟨rfl,fun _ _ => rfl,?_⟩
  obtain ⟨X,h⟩ := nextGap
  intro i hi
  change app (frontWord ++ []) blank i = Box.cut _ (regenerated returnedWidths exterior).r _ i
  rw [List.append_nil,Box.read,ite_eq_left (by omega : i < 18396801869163),h]
  have same : app frontWord blank =
      Box.cut (frontWord.length+107996733) (app frontWord (rep 107996733 [false] X)) blank := by
    rw [Box.front,blankCut]
  have e := congrFun same i
  have len := frontLength
  rw [Box.read,ite_eq_left (by omega)] at e
  exact e

/-- At this particular test the actual third marker is far enough away for B to see 0. -/
theorem actualMarkerTest : ∃ c, steps 4679882756120429 init = some c ∧ c.st = .B ∧ c.r 0 = false := by
  obtain ⟨c,h,s,r⟩ := sample false
  obtain ⟨d,f,st,_,right⟩ := Locality.transfer trans 1394298 1 actualAgreement h
  have z := steps_seq trans blankSecondRestart f
  exact ⟨d,z,st.symm.trans s,(right 0 (by decide)).symm.trans r⟩

/-- The same left exterior, first two markers and a third six-one block after a
gap of 8626 give a halting tape. -/
theorem nearbyMarkerHalts : ∃ c, steps 1394298 (comparison true).toCfg = some c ∧ step c = none := by
  obtain ⟨c,h,s,r⟩ := sample true
  exact ⟨c,h,by simp [TM.step,s,r,trans]⟩

private theorem lookup (w : List Bool) (R : Tape) (i : Nat) : app w R i =
    if i < w.length then app w blank i else R (i-w.length) := by
  induction w generalizing i with
  | nil => simp
  | cons b w ih =>
    cases i with
    | zero => simp
    | succ i => simp [ih]

private theorem runBit (n : Nat) (b : Bool) (R : Tape) (i : Nat) : rep n [b] R i =
    if i < n then b else R (i-n) := by
  induction n generalizing i with
  | zero => simp
  | succ n ih =>
    cases i with
    | zero => simp
    | succ i => simp [ih]

def withThirdMarker (c : Config) : Config :=
  { c with r := fun i => if 18590 ≤ i ∧ i < 18596 then true else c.r i }

private theorem twoInputs (i : Nat) :
    (comparison true).toCfg.r i = (withThirdMarker (comparison false).toCfg).r i := by
  change app (frontWord ++ runs [(false,8626),(true,6)]) blank i =
    if _ then true else app (frontWord ++ []) blank i
  rw [← app_app,List.append_nil,lookup]
  have len := frontLength
  rw [len]
  by_cases before : i < 9964
  · rw [ite_eq_left before, ite_eq_right (by omega)]
  · rw [ite_eq_right before,lookup frontWord blank i,len,ite_eq_right before]
    have e : app (runs [(false,8626),(true,6)]) blank =
        rep 8626 [false] (rep 6 [true] blank) := by
      unfold runs
      simp only [List.flatMap_cons,List.flatMap_nil,List.append_nil,← app_app,asRepeat]
    rw [e,runBit]
    by_cases lo : i-9964 < 8626
    · rw [ite_eq_left lo,ite_eq_right (by omega)]; rfl
    · rw [ite_eq_right lo,runBit]
      by_cases hi : i-9964-8626 < 6
      · rw [ite_eq_left hi,ite_eq_left (by omega)]
      · rw [ite_eq_right hi,ite_eq_right (by omega)]; exact (rfl : false = false)

/-- Alter only six initially blank cells of the *exact* second restart. Every
other bit, including the distant debris, stays at the same position. -/
theorem sixCellWitness : ∃ c, steps 1394298 (withThirdMarker secondRestart) = some c ∧ step c = none := by
  have h : Locality.Agree (1394298+1) (comparison true).toCfg (withThirdMarker secondRestart) := by
    refine ⟨rfl,fun _ _ => rfl,?_⟩
    intro i hi
    rw [twoInputs]
    change (if _ then true else _) = (if _ then true else _)
    split
    · rfl
    · exact actualAgreement.2.2 i hi
  obtain ⟨c,s,st,bit⟩ := sample true
  obtain ⟨d,run,hs,_,hr⟩ := Locality.transfer trans 1394298 1 h s
  have sd := hs.symm.trans st
  have rd := (hr 0 (by decide)).symm.trans bit
  exact ⟨d,run,by simp [TM.step,sd,rd,trans]⟩

#print axioms sixCellWitness
#print axioms actualMarkerTest
#print axioms nearbyMarkerHalts
end H7846.Line24
