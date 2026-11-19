import SecondEntry

namespace H7846.Line24
open TM

private def common := runs [(false,1324),(true,6),(false,8628),(true,6)]
private def insertion := runs [(false,8583),(true,6),(false,3),(true,12),(false,9),(true,6)]

/-- The real third marker and all farther tape remain in place. The next
8,619 cells after the second marker now carry four additional six-one blocks. -/
def withAlignedMarkers : Config :=
  ⟨exterior,app common (app insertion (rep 107988114 [false] thirdMarkerTail)),.A⟩

/-- Exact source and target of the modification, displaying their common far wing. -/
theorem alignedMarkerEdit :
    secondRestart.r = app common (rep 8619 [false] (rep 107988114 [false] thirdMarkerTail)) ∧
    withAlignedMarkers.r = app common (app insertion (rep 107988114 [false] thirdMarkerTail)) := by
  refine ⟨?_,rfl⟩
  rw [← rep_add]
  exact secondRestartFront

private def prefixBits := common ++ insertion
private def finite : FCfg St :=
  ⟨runs [(true,5),(false,1),(true,2),(false,1),(true,3)], prefixBits,.A⟩

private theorem clear (w : List Bool) (n : Nat) (X : Tape) (i : Nat) (hi : i < w.length+n) :
    app w blank i = app w (rep n [false] X) i := by
  induction w generalizing i with
  | nil =>
    have h : i < n := by simpa using hi
    change blank i = rep n [false] X i
    rw [← Box.zeros,Box.read,ite_eq_left h]
  | cons b w ih =>
    cases i with
    | zero => rfl
    | succ i => exact ih i (by simp only [List.length_cons] at hi; omega)

private theorem observed {f : FCfg St} {n : Nat}
    (check : (TM.fsteps trans n f).map (fun d => (d.st,d.r.headD false)) = some (.B,true)) :
    ∃ c, steps n f.toCfg = some c ∧ c.st=.B ∧ c.r 0=true := by
  cases h : TM.fsteps trans n f with
  | none => simp [h] at check
  | some d =>
    rw [h,Option.map_some] at check
    have pair := Option.some.inj check
    have r := FCfg.steps_eq trans n f
    rw [h,Option.map_some] at r
    exact ⟨d.toCfg,r,congrArg Prod.fst pair,(app_head _).trans (congrArg Prod.snd pair)⟩

/-- An exact halting variant with four aligned, six-one insertions and no
change to the original third marker or more distant debris. -/
theorem alignedMarkersHalt : ∃ c, steps 2897169 withAlignedMarkers = some c ∧ step c = none := by
  have sample : (TM.fsteps trans 2897169 finite).map (fun d => (d.st,d.r.headD false)) =
      some (.B,true) := by decide +native
  obtain ⟨d,h,st,bit⟩ := observed sample
  have agree : Locality.Agree (2897169+1) finite.toCfg withAlignedMarkers := by
    refine ⟨rfl,fun _ _ => rfl,?_⟩
    intro i hi
    change app prefixBits blank i = app common (app insertion _) i
    rw [app_app]
    exact clear prefixBits 107988114 _ _ (by omega)
  obtain ⟨c,run,s,_,r⟩ := Locality.transfer trans 2897169 1 agree h
  have sc := s.symm.trans st
  have bc := (r 0 (by decide)).symm.trans bit
  exact ⟨c,run,by simp [TM.step,sc,bc,trans]⟩

#print axioms alignedMarkersHalt
end H7846.Line24
