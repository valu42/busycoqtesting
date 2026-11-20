import FourthWindow
import EpochReturn

namespace H7846.Line24
open TM PackedTape FourthWindow
attribute [local irreducible] TM.steps

private def distantRuns := thirdRestartPack.r.drop 7

/-- Exact tape at the fourth return to A with the original left exterior. -/
def fourthRestartPack : Pack :=
  ⟨left, afterRuns ++ (false,967735738118322616189961224328)::distantRuns, .A⟩

private theorem thirdSource :
    model before (rep 967735738118322616190588893991 [false] (denote distantRuns)) =
      thirdRestartPack.toCfg := rfl

private theorem fourthTarget :
    model afterRuns (rep 967735738118322616189961224328 [false] (denote distantRuns)) =
      fourthRestartPack.toCfg := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  refine ⟨rfl,?_,rfl⟩
  exact (denoteJoin afterRuns ((false,967735738118322616189961224328)::distantRuns) blank).symm

theorem thirdToFourthRestart : steps 122546899564 thirdRestartPack.toCfg =
    some fourthRestartPack.toCfg := by
  have h := extended 967735738118322616067726286765 (denote distantRuns)
  change steps 122546899564
    (model before (rep 967735738118322616190588893991 [false] (denote distantRuns))) =
    some (model afterRuns (rep 967735738118322616189961224328 [false] (denote distantRuns))) at h
  rwa [thirdSource,fourthTarget] at h

theorem blankFourthRestart : steps 555909174447650556710019195188461 init =
    some fourthRestartPack.toCfg := by
  exact steps_seq trans blankThirdRestart thirdToFourthRestart

theorem fourthRestartShape : fourthRestartPack.st = .A ∧
    fourthRestartPack.l = thirdRestartPack.l ∧ fourthRestartPack.r.take 8 =
    [(false,1324),(true,6),(false,8628),(true,6),(false,115343235),(true,6),
      (false,470752242),(true,6)] := by decide

#print axioms blankFourthRestart
end H7846.Line24
