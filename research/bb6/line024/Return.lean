import Checkpoint
import ReturnPhases
import Locality
import Box
import Guarded

namespace H7846.Line24
open TM
set_option maxRecDepth 12000

private def clipped : FCfg St :=
  ⟨runs [(true,5),(false,1),(true,2),(false,1),(true,3)],
   runs [(false,1324),(true,6)], .A⟩

private def digits := [2,1,3,1,1,2,2,4,4,3,1,0,1,0]
private def rightBits := [true,false] ++
  digits.flatMap (fun n => List.replicate (3*n) true ++ [false]) ++ List.replicate 7 true

private def outerBits := runs [(true,5),(false,1),(true,2),(false,1),(true,3)]
private def padded : FCfg St :=
  { clipped with l := outerBits ++ List.replicate 64 false }
private def middle := (Guarded.run trans 1864476 padded).getD padded
private def leftBits :=
  false :: (List.replicate 2120 true ++ [false,true,true,false] ++
    List.replicate 8630 true ++ [false,true,true,false] ++
    List.replicate 1322 true ++ false :: outerBits)

private theorem appOnes (n : Nat) (xs : List Bool) (L : Tape) :
    app (List.replicate n true ++ xs) L = rep n [true] (app xs L) := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [List.replicate_succ,List.cons_append,app_cons,rep_succ,app]; rw [ih]

private theorem leftShape (L : Tape) : app leftBits L =
    cons false (stackBase 2120 [8628,1320] (app outerBits L)) := by
  unfold leftBits
  simp only [List.append_assoc,app_cons,appOnes,List.cons_append,List.nil_append]
  rfl

private def carryLeft (n : Nat) (L : Tape) : Tape := app outerBits (rep n [false] L)

private theorem paddedVisit (L : Tape) : steps 1864476 (Guarded.cfg padded L) =
    some (visitX (stackBase 2120 [8628,1320] (carryLeft 16 L)) [] (word digits 0).tape) := by
  have h : Guarded.run trans 1864476 padded = some middle ∧ middle.st = .D ∧
      middle.l = leftBits ++ List.replicate 16 false ∧ middle.r = rightBits := by
    decide +native
  obtain ⟨h,s,l,r⟩ := h
  have eq : Guarded.cfg middle L = visitX (stackBase 2120 [8628,1320] (carryLeft 16 L))
      [] (word digits 0).tape := by
    apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
    refine ⟨?_,?_,s⟩
    · change app middle.l L = _
      rw [l,← app_app,leftShape]; rfl
    · change app middle.r blank = _
      rw [r]; rfl
  exact (Guarded.sound trans h L).trans (congrArg some eq)

private theorem paddedCycle (L : Tape) : steps 22751521280 (Guarded.cfg padded L) =
    some (regenerated returnedWidths (carryLeft 16 L)) := by
  have z := steps_seq trans (paddedVisit L) (regenerate (carryLeft 16 L))
  exact z

private theorem carryBlank (n : Nat) : carryLeft n blank = exterior := by
  unfold carryLeft; rw [Box.zeroBlank]; rfl

private theorem cfgBlank : Guarded.cfg padded blank = clipped.toCfg := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  refine ⟨?_,rfl,rfl⟩
  change app (outerBits ++ List.replicate 64 false) blank = _
  rw [← app_app]
  exact carryBlank 64

private theorem clippedVisit : steps 1864476 clipped.toCfg =
    some (visitX (stackBase 2120 [8628,1320] exterior) [] (word digits 0).tape) := by
  have h := paddedVisit blank
  rwa [cfgBlank,carryBlank] at h

private theorem clippedRun : ∃ P, steps 22598775004 clipped.toCfg =
    some ⟨P,blank,.D⟩ := by
  obtain ⟨P,b⟩ := return0 (stackBase 2120 [8628,1320] exterior)
  have z := steps_seq trans clippedVisit b
  exact ⟨P,z⟩

private theorem prependRun (n : Nat) (b : Bool) (X Y : Tape) {radius : Nat}
    (h : ∀ i < radius, X i = Y i) :
    ∀ i < n+radius, rep n [b] X i = rep n [b] Y i := by
  induction n with
  | zero => simpa using h
  | succ n ih =>
    intro i hi
    cases i with
    | zero => rfl
    | succ i => exact ih i (by omega)

private theorem zeroGap (n : Nat) (X : Tape) : ∀ i < n, blank i = rep n [false] X i := by
  induction n with
  | zero => simp
  | succ n ih =>
    intro i hi
    cases i with
    | zero => rfl
    | succ i => exact ih i (by omega)

private theorem initialAgreement (n : Nat) (hn : n ≤ 18396801869115) :
    Locality.Agree n clipped.toCfg restart := by
  refine ⟨rfl,fun _ _ => rfl,?_⟩
  let X := rep 4 [true] debris
  have z := zeroGap (wallWidth-3) X
  have h := prependRun 1324 false _ _ (prependRun 6 true _ _ z)
  intro i hi
  exact h i (by change i < 1324+(6+18396801867785); omega)

/-- From blank, the 13 returning phases expose 000 in D at the first landing
after the six-one marker regenerates a counter. -/
theorem blankReturn : ∃ c, steps 4679882601979855 init = some c ∧
    c.st = .D ∧ c.r 0 = false ∧ c.r 1 = false ∧ c.r 2 = false := by
  obtain ⟨P,h⟩ := clippedRun
  obtain ⟨c,hc,hs,_,hr⟩ := Locality.transfer trans 22598775004 3 (initialAgreement _ (by decide)) h
  have finalRun := steps_seq trans blankRestart hc
  exact ⟨c,finalRun,hs.symm,
    (hr 0 (by decide)).symm,(hr 1 (by decide)).symm,(hr 2 (by decide)).symm⟩

/-- The first trillion cells on each side of the regenerated head are explicit. -/
theorem blankRegenerated : ∃ c, steps 4679882754726131 init = some c ∧
    Locality.Agree 1000000000000 (regenerated returnedWidths exterior) c := by
  have h := steps_seq trans clippedVisit (regenerate exterior)
  obtain ⟨c,hc,hs⟩ := Locality.transfer trans 22751521280 1000000000000
    (initialAgreement _ (by decide)) h
  have z := steps_seq trans blankRestart hc
  exact ⟨c,z,hs⟩

private def nearBits := runs [(false,1324),(true,6)]
private abbrev gap := 18396801867785
private abbrev cutAt := 18396801869115

/-- Restore an arbitrary exterior after the original cleared gap. -/
def restored (g : Nat) (R : Tape) : Config := ⟨exterior,app nearBits (rep g [false] R),.A⟩

private theorem rightCut (g : Nat) (R : Tape) : Box.cut (1330+g) clipped.toCfg.r R =
    app nearBits (rep g [false] R) := by
  change Box.cut (nearBits.length+g) (app nearBits blank) R = _
  rw [Box.front,Box.zeros]

private theorem leftCut (n : Nat) (L : Tape) : Box.cut (12+n) exterior L =
    carryLeft n L := by
  change Box.cut (outerBits.length+n) (app outerBits blank) L = _
  rw [Box.front,Box.zeros]; rfl

private theorem past (xs : List Bool) (S : Tape) (n : Nat) : app xs S (xs.length+n) = S n := by
  induction xs with
  | nil => simp
  | cons b bs ih =>
    change cons b (app bs S) (bs.length+1+n) = _
    rw [show bs.length+1+n=(bs.length+n)+1 by omega]; exact ih

private def mark := cons true blank

private theorem position {u : Nat}
    (eq : Box.cut u exterior mark = carryLeft 16 (rep 23000000000 [false] mark)) :
    u = 23000000028 := by
  let i : Nat := 23000000028
  have sample : carryLeft 16 (rep 23000000000 [false] mark) i = true := by
    unfold carryLeft
    change app outerBits _ (outerBits.length+23000000016) = true
    rw [past, ← rep_add, ← Box.zeros, Box.read]
    rfl
  have background : exterior i = false := by
    change app outerBits blank (outerBits.length+23000000016) = false
    rw [past]; rfl
  rw [← eq,Box.read] at sample
  split at sample
  · rw [background] at sample; contradiction
  · have m : ∀ j, mark j = true → j = 0 := by
      intro j; cases j <;> simp [mark,blank]
    have z := m _ sample
    change 23000000028 - u = 0 at z
    have hu : ¬ 23000000028 < u := by assumption
    omega

private theorem sameLeft (n : Nat) (U : Tape) :
    Box.cut (12+(64+n)) exterior U = app padded.l (rep n [false] U) := by
  rw [leftCut]
  unfold carryLeft
  rw [rep_add]
  change app outerBits (rep 64 [false] (rep n [false] U)) =
    app (outerBits ++ List.replicate 64 false) (rep n [false] U)
  rw [← app_app]; rfl

private theorem sameRight (g : Nat) : Box.cut (1330+g) clipped.toCfg.r blank = clipped.toCfg.r := by
  rw [rightCut,Box.zeroBlank]; rfl

private theorem sourceMarked (g n : Nat) (U : Tape) :
    Box.frame clipped.toCfg (12+(64+n)) (1330+g) U blank = Guarded.cfg padded (rep n [false] U) := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  exact ⟨sameLeft n U,sameRight g,rfl⟩

private theorem sourceActual (g : Nat) (R : Tape) : Box.frame clipped.toCfg 23000000076 (1330+g) blank R = restored g R := by
    apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
    exact ⟨(leftCut 23000000064 blank).trans (carryBlank _),rightCut g _,rfl⟩

private theorem clipCycle : steps 22751521280 clipped.toCfg =
    some (regenerated returnedWidths exterior) := by
  have h := paddedCycle blank
  rwa [cfgBlank,carryBlank] at h

private theorem displacement (g u v : Nat)
    (z : TM.steps trans 22751521280 (Box.frame clipped.toCfg 23000000076 (1330+g) mark blank) =
      some (Box.frame (regenerated returnedWidths exterior) u v mark blank)) : u=23000000028 := by
  have e := sourceMarked g 23000000000 mark
  have z := (congrArg (steps 22751521280) e.symm).trans z
  have pc := paddedCycle (rep 23000000000 [false] mark)
  have rel := congrArg Cfg.l (Option.some.inj (pc.symm.trans z))
  exact position rel.symm

/-- The entire regenerated configuration, including its remote suffix. -/
theorem restoredCycle (g : Nat) (hg : 22751521280 ≤ 1330+g) (R : Tape) : steps 22751521280 (restored g R) =
    some (Box.frame (regenerated returnedWidths exterior)
              23000000028 ((1330+g)+48) blank R) := by
  obtain ⟨u,v,sum,runsBox⟩ := Box.run trans _ clipCycle 23000000076 (1330+g) (by decide) hg
  have hu := displacement g u v (runsBox mark blank)
  have hv : v = (1330+g)+48 := by omega
  have actual := runsBox blank R
  rw [hu,hv,sourceActual] at actual
  exact actual

/-- Second exact return tape. The old distant word starts 48 cells farther from
the head than at the preceding restart. -/
def secondRestart : Config :=
  ⟨exterior, Box.cut (cutAt+48) (regenerated returnedWidths exterior).r
      (rep 4 [true] debris), .A⟩

theorem blankSecondRestart : steps 4679882754726131 init = some secondRestart := by
  have h := restoredCycle gap (by decide) (rep 4 [true] debris)
  have hleft := (leftCut 23000000016 blank).trans (carryBlank _)
  have eq : Box.frame (regenerated returnedWidths exterior) 23000000028 ((1330+gap)+48)
          blank (rep 4 [true] debris) = secondRestart := by
    apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
    exact ⟨hleft,rfl,rfl⟩
  rw [eq] at h
  have src : restored gap (rep 4 [true] debris) = restart := by
    apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
    refine ⟨rfl,?_,rfl⟩
    change app (List.replicate 1324 false ++ List.replicate 6 true) _ = _
    rw [← app_app]
    have repBits (n : Nat) (b : Bool) (X : Tape) : app (List.replicate n b) X = rep n [b] X := by
      induction n with
      | zero => rfl
      | succ n ih => simp only [List.replicate_succ,app_cons,rep_succ,app]; rw [ih]
    rw [repBits,repBits]; rfl
  rw [src] at h
  have z := steps_seq trans blankRestart h
  exact z

#print axioms blankSecondRestart
#print axioms blankRegenerated
#print axioms blankReturn
end H7846.Line24
