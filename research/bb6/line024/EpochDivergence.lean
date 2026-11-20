import EpochReturn
import TwoMarkerPrefix

namespace H7846.Line24
open TM PackedTape
set_option maxRecDepth 12000

/-- The third restart has 29,386,071 more clear cells at the position that
held the third six-one marker during the preceding restart. -/
def thirdOldSite : Tape := rep 29386071 [false] (denote (thirdRestartPack.r.drop 5))

theorem thirdRestartSource : thirdRestartPack.toCfg = twoMarkerSource thirdOldSite := by
  rw [twoMarkerSource_eq]
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  refine ⟨rfl,?_,rfl⟩
  let front (X : Tape) := rep 1324 [false] (rep 6 [true] (rep 8628 [false] (rep 6 [true] X)))
  have split := rep_add 107996733 29386071 [false] (denote (thirdRestartPack.r.drop 5))
  exact congrArg front split

theorem epochReadBits : thirdMarkerTail 0 = true ∧ thirdOldSite 0 = false := ⟨rfl,rfl⟩

/-- At the first exterior cell the head and the entire left tape agree between
these two blank-reachable restarts. State F sees a one in the earlier tape and
a zero in the later tape. -/
theorem epochContacts : ∃ P : Tape,
    steps 17588658509 secondRestart = some ⟨P,thirdMarkerTail,.F⟩ ∧
    steps 17588658509 thirdRestartPack.toCfg = some ⟨P,thirdOldSite,.F⟩ := by
  obtain ⟨P,hit⟩ := twoMarkerContact
  rw [secondRestartSource,thirdRestartSource]
  exact ⟨P,hit thirdMarkerTail,hit thirdOldSite⟩

private theorem readOne (P : Tape) : steps 1 ⟨P,thirdMarkerTail,.F⟩ =
    some ⟨TM.tail P,cons (P 0) (cons false (TM.tail thirdMarkerTail)),.A⟩ := by
  rfl

private theorem readZero (P : Tape) : steps 1 ⟨P,thirdOldSite,.F⟩ =
    some ⟨TM.tail P,cons (P 0) (cons true (TM.tail thirdOldSite)),.F⟩ := by
  rfl

attribute [local irreducible] TM.steps

theorem epochDivergence : ∃ P : Tape,
    steps 17588658510 secondRestart = some
      ⟨TM.tail P,cons (P 0) (cons false (TM.tail thirdMarkerTail)),.A⟩ ∧
    steps 17588658510 thirdRestartPack.toCfg = some
      ⟨TM.tail P,cons (P 0) (cons true (TM.tail thirdOldSite)),.F⟩ := by
  obtain ⟨P,a,b⟩ := epochContacts
  have za := steps_seq trans a (readOne P)
  have zb := steps_seq trans b (readZero P)
  exact ⟨P,za,zb⟩

theorem blankThirdDivergence : ∃ P : Tape, steps 555909174447650556709914236947407 init =
    some ⟨TM.tail P,cons (P 0) (cons true (TM.tail thirdOldSite)),.F⟩ := by
  obtain ⟨P,_,b⟩ := epochDivergence
  have z := steps_seq trans blankThirdRestart b
  exact ⟨P,z⟩

#print axioms blankThirdDivergence
end H7846.Line24
