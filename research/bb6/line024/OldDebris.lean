import PackedStack
import RecoveryPhase
namespace H7846.Line24
open TM Word PackedTape
set_option maxRecDepth 12000

private def leftRuns : Runs :=
  [(true,15353093),(false,1),(true,2),(false,1),(true,137382806),(false,1),
   (true,2),(false,1),(true,8630),(false,1),(true,2),(false,1),(true,1322),
   (false,1),(true,5),(false,1),(true,2),(false,1),(true,3)]

private def retained := push true 4 (wordRuns (word ([1] ++ List.replicate 19 2 ++ [3,0,1,1]) 0) [])

private def bits := [true,false] ++
  [2,2,2,1,3,2,1,4,2,1,5,2,3,4,4,4,4,4,3,1,0,1,0].flatMap
    (fun n => List.replicate (3*n) true ++ [false]) ++ List.replicate 7 true

private theorem repack : postStackPack = packVisit leftRuns postStackWord 18396649123149 retained :=
  by decide +native

private theorem aboveBlank (x : Word) : x.above blank = x.tape := by
  induction x with
  | tip j => rfl
  | d n x ih => exact congrArg (blkV n) ih

private theorem retainedAll (x : Word) : denote (push true 4 (wordRuns x [])) = rep 4 [true] x.tape := by
  rw [denotePush,denoteWord]
  exact congrArg (rep 4 [true]) (aboveBlank x)

private theorem retainedShape : denote retained = rep 4 [true] debris := by
  unfold retained debris
  exact retainedAll _

private theorem stackLeft (w a b c : Nat) :
    denote [(true,w),(false,1),(true,2),(false,1),(true,a+2),(false,1),
      (true,2),(false,1),(true,b+2),(false,1),(true,2),(false,1),(true,c+2),
      (false,1),(true,5),(false,1),(true,2),(false,1),(true,3)] =
    stackBase w [a,b,c] exterior := by rfl

private theorem leftAgrees : denote leftRuns = stackBase 15353093 [137382804,8628,1320] exterior := by
  unfold leftRuns
  exact stackLeft 15353093 137382804 8628 1320

private theorem bitsForm (X : Tape) : app bits X = app [true,false] (postStackWord.above X) := by rfl

private theorem bitsLength : bits.length=197 := by decide +native

private theorem rightCut (X : Tape) : Box.cut 18396649123346 (app [true,false] postStackWord.tape) X =
    app [true,false] (postStackWord.above (rep 18396649123149 [false] X)) := by
  have src := (bitsForm blank).trans (congrArg (app [true,false]) (aboveBlank postStackWord))
  rw [← src,show 18396649123346 = bits.length+18396649123149 by rw [bitsLength],
    Box.front,Box.zeros]
  exact bitsForm _

private theorem exactPostStack : postStackPack.toCfg = postStackState := by
  have first := congrArg Pack.toCfg repack
  have second := visitDenote leftRuns postStackWord 18396649123149 retained
  have good := congrArg (fun R => visitX (denote leftRuns) [] (postStackWord.above (rep 18396649123149 [false] R))) retainedShape
  have second := second.trans good
  apply (first.trans second).trans
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  exact ⟨congrArg (cons false) leftAgrees,(rightCut _).symm,rfl⟩

attribute [local irreducible] TM.steps TM.rep

theorem blankOldDebris : ∃ L, steps 10397282588485330 init = some ⟨L,rep 4 [true] debris,.F⟩ := by
  have h := blankPostStack
  rw [exactPostStack] at h
  obtain ⟨L,z⟩ := debrisContact (stackBase 15353093 [137382804,8628,1320] exterior) (rep 4 [true] debris)
  have both := steps_seq trans h z
  exact ⟨L,both⟩

def recoveredCfg := regenerated debrisWidths
    (debrisExterior (stackBase 15353093 [137382804,8628,1320] exterior))

theorem blankRecovered : steps 21916906635339130 init = some recoveredCfg := by
  have h := blankPostStack
  rw [exactPostStack] at h
  have r := debrisRenewal (stackBase 15353093 [137382804,8628,1320] exterior)
  have both := steps_seq trans h r
  exact both

#print axioms blankOldDebris
#print axioms blankRecovered
end H7846.Line24
