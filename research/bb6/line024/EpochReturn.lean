import PackedStack
import EpochPart000
import EpochPart001
import EpochPart002
import EpochPart003
import EpochPart004
import EpochPart005
import EpochPart006
import EpochPart007
import EpochPart008
namespace H7846.Line24
open TM PackedTape
attribute [local irreducible] TM.steps Pack.toCfg
def thirdRestartPack : Pack := ⟨[(true,5),(false,1),(true,2),(false,1),(true,3)],[(false,1324),(true,6),(false,8628),(true,6),(false,137382804),(true,6),(false,967735738118322616190588893991),(true,7),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,6),(false,1),(true,12),(false,1),(true,3),(false,1),(true,6),(false,1),(true,7)],.A⟩
private theorem exactTape : EpochPart008.finalPack = thirdRestartPack := by decide
theorem blankThirdRestart : steps 555909174447650556709896648288897 init = some thirdRestartPack.toCfg := by
  have h := blankPostStack
  have z0 := steps_seq trans h EpochPart000.passage
  have z1 := steps_seq trans z0 EpochPart001.passage
  have z2 := steps_seq trans z1 EpochPart002.passage
  have z3 := steps_seq trans z2 EpochPart003.passage
  have z4 := steps_seq trans z3 EpochPart004.passage
  have z5 := steps_seq trans z4 EpochPart005.passage
  have z6 := steps_seq trans z5 EpochPart006.passage
  have z7 := steps_seq trans z6 EpochPart007.passage
  have z8 := steps_seq trans z7 EpochPart008.passage
  exact z8.trans (congrArg (fun p : Pack => some p.toCfg) exactTape)
theorem thirdRestartShape : thirdRestartPack.st = .A ∧ thirdRestartPack.l = restartPack.l ∧ thirdRestartPack.r.take 7 = [(false,1324),(true,6),(false,8628),(true,6),(false,137382804),(true,6),(false,967735738118322616190588893991)] := by decide
#print axioms blankThirdRestart
end H7846.Line24
