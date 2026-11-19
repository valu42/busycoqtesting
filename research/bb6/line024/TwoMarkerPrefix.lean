import SharpThird

namespace H7846.Line24
open TM
set_option maxRecDepth 12000

/-- The entire 108,006,697-cell prefix up to the old third marker, followed
by an arbitrary stream. This equality spells out the input to the contact rule. -/
theorem twoMarkerSource_eq (R : Tape) : twoMarkerSource R =
    ⟨exterior,rep 1324 [false] (rep 6 [true] (rep 8628 [false]
      (rep 6 [true] (rep 107996733 [false] R)))),.A⟩ := by
  have same (n : Nat) (b : Bool) (S : Tape) :
      app (List.replicate n b) S = rep n [b] S := by
    induction n with
    | zero => rfl
    | succ n ih => simp only [List.replicate_succ,app_cons,rep_succ,app]; rw [ih]
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  refine ⟨rfl,?_,rfl⟩
  change app (runs [(false,1324),(true,6),(false,8628),(true,6)]) _ = _
  unfold runs
  simp only [List.flatMap_cons,List.flatMap_nil,List.append_nil,← app_app,same]

/-- All suffixes produce the same entire left tape in F exactly when the head
reaches their first cell. The two-marker prefix itself is overwritten en route. -/
theorem twoMarkerContact : ∃ P : Tape, ∀ R : Tape,
    steps 17588658509 (twoMarkerSource R) = some ⟨P,R,.F⟩ := by
  let w := stackBase 8588 [8628,1320] exterior
  obtain ⟨P,c⟩ := contactWithFixedLeft (rep 107987678 [true] w)
  refine ⟨P,fun R => ?_⟩
  have e : secondEntryWith R = visitX w [] (secondEntryWord.above (rep 107988091 [false] R)) :=
    congrArg (fun Y : Tape => (⟨secondEntryModel.l,Y,.D⟩ : Config)) (sharpEntryTape R)
  have a := (twoMarkerEntry R).trans (congrArg some e)
  have h := steps_seq trans (steps_seq trans a (sharpOpenToPreImpact w R)) (c R)
  exact h

#print axioms twoMarkerContact
end H7846.Line24
