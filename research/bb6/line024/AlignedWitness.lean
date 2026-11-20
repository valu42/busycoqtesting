import StackInvariant
import Box
import Locality

namespace H7846.Line24
open TM Word

/-- An ordinary stack return with bottom wall width 44, no older walls and
the left exterior of the two blank-run restarts. -/
abbrev witnessWord := Word.d 1 (.d 0 (.tip 0))
def alignedInput := visitX (stackBase 44 [] exterior) [] witnessWord.tape

theorem witnessPhases : StackPhases witnessWord 44 [] 154 [0,45] :=
  StackPhases.last (Series.nil witnessWord) 44 []

theorem witnessAlignment : ∀ m ∈ [0,45], m % 3 = 0 := by
  apply witnessPhases.aligned (by decide)
  simp

private def finiteWitness : FCfg St := ⟨runs [(true,5),(false,1),(true,2),(false,1),(true,3)],
  runs [(false,49),(true,12),(false,2),(true,4)],.A⟩

private theorem bitCheck {f : FCfg St} {n : Nat}
    (h : (TM.fsteps trans n f).map (fun d => (d.st,d.r.headD false)) = some (.B,true)) :
    ∃ c, steps n f.toCfg = some c ∧ step c = none := by
  cases e : TM.fsteps trans n f with
  | none => simp [e] at h
  | some d =>
    rw [e,Option.map_some] at h
    have st := congrArg Prod.fst (Option.some.inj h)
    have bit := congrArg Prod.snd (Option.some.inj h)
    have rb : d.toCfg.r 0 = true := (app_head _).trans bit
    have run := FCfg.steps_eq trans n f
    rw [e,Option.map_some] at run
    exact ⟨d.toCfg,run,by simp [TM.step,show d.toCfg.st = .B from st,rb,trans]⟩

set_option maxRecDepth 20000 in
set_option maxHeartbeats 1200000 in
theorem alignedRestartHalts : ∃ c, steps 3121 (regenerated [0,45] exterior) = some c ∧ step c = none := by
  have f : (TM.fsteps trans 3121 finiteWitness).map (fun d => (d.st,d.r.headD false)) = some (.B,true) := by
    decide +kernel
  have eq : finiteWitness.toCfg = regenerated [0,45] exterior := rfl
  rw [← eq]
  exact bitCheck f

theorem alignedInputHalts : ∃ c, steps 3275 alignedInput = some c ∧ step c = none := by
  obtain ⟨c,h,halt⟩ := alignedRestartHalts
  have run := steps_seq trans (witnessPhases.execute exterior) h
  exact ⟨c,run,halt⟩

/-- This aligned return also preserves the *actual* first two marker offsets. -/
def pairedGaps : List Nat := [0,8607,8628,1320]

theorem pairedPhases : StackPhases witnessWord 8606 [8628,1320]
    (38+(27+((0::8607::8628::1320::[]).map (fun m => 22+m)).sum)) pairedGaps :=
  StackPhases.last (Series.nil witnessWord) 8606 [8628,1320]

theorem pairedAlignment : ∀ m ∈ pairedGaps, m % 3 = 0 := by
  apply pairedPhases.aligned (by decide)
  simp

private def finitePaired : FCfg St := ⟨finiteWitness.l,
  runs [(false,1324),(true,6),(false,8628),(true,6),
        (false,8607),(true,12),(false,2),(true,4)],.A⟩

private theorem repeatTape (n : Nat) (b : Bool) (R : Tape) :
    app (List.replicate n b) R = rep n [b] R := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [List.replicate_succ,app_cons,rep_succ,app]; rw [ih]

private theorem pairedTape : finitePaired.toCfg = regenerated pairedGaps exterior := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  refine ⟨rfl,?_,rfl⟩
  change app (runs _) blank = _
  simp only [runs,List.flatMap_cons,List.flatMap_nil,List.append_nil,← app_app,repeatTape]
  rw [show 1324=4+1320 by decide,rep_add 4 1320]
  rfl

theorem pairedRestartHalts : ∃ c, steps 2899518 (regenerated pairedGaps exterior) = some c ∧
    c.st = .B ∧ c.r 0 = true := by
  have check : (TM.fsteps trans 2899518 finitePaired).map (fun d => (d.st,d.r.headD false)) =
      some (.B,true) := by decide +native
  cases e : TM.fsteps trans 2899518 finitePaired with
  | none => simp [e] at check
  | some d =>
    rw [e,Option.map_some] at check
    have pair := Option.some.inj check
    have run := FCfg.steps_eq trans 2899518 finitePaired
    rw [e,Option.map_some,pairedTape] at run
    exact ⟨d.toCfg,run,congrArg Prod.fst pair,(app_head _).trans (congrArg Prod.snd pair)⟩

/-- All tape beyond this radius can be arbitrary; the right half after its
last marker may contain the original distant third marker and the old debris. -/
theorem pairedWithExteriorHalts (R : Tape) : ∃ c,
    steps 2899518 ⟨exterior,Box.cut 2899519 (regenerated pairedGaps exterior).r R,.A⟩ =
    some c ∧ step c = none := by
  obtain ⟨d,h,st,bit⟩ := pairedRestartHalts
  have same : Locality.Agree (2899518+1) (regenerated pairedGaps exterior)
      (⟨exterior,Box.cut 2899519 (regenerated pairedGaps exterior).r R,.A⟩ : Config) := by
    refine ⟨rfl,fun _ _ => rfl,?_⟩
    intro i hi
    exact ((Box.read 2899519 _ _ i).trans (ite_eq_left hi)).symm
  obtain ⟨c,t,s,_,r⟩ := Locality.transfer trans 2899518 1 same h
  have st' := s.symm.trans st
  have bit' := (r 0 (by decide)).symm.trans bit
  exact ⟨c,t,by simp [TM.step,st',bit',trans]⟩

#print axioms pairedWithExteriorHalts
#print axioms alignedInputHalts
end H7846.Line24
