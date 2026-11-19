import Phase

namespace H7846.Line24
open TM Word

set_option maxRecDepth 12000

def wallWidth : Nat := 18396801867788

/-- The tail at the leading-empty-digit collision, with the empty digit removed. -/
def debris := (word ([1] ++ List.replicate 19 2 ++ [3,0,1,1]) 0).tape

private theorem atWall {x y k t} (h : Series x y k t) (w : Nat) (L : Tape) :
    steps (t+15*k) (visitX (rep w [true] L) [] x.tape) =
      some (visitX (rep (3*k+w) [true] L) [] y.tape) := by
  rw [rep_add (3*k) w]
  exact runSeries h _

private theorem endpoint : endWord.tape = cons false debris := rfl

theorem collisionFromEntry : steps 4661463180679270 entryCfg =
    some (visitX (rep wallWidth [true] wallBase) [0] debris) := by
  have h := atWall phase 82430 wallBase
  rw [endpoint] at h
  exact h

theorem blankCollision : steps 4661463201335715 init =
    some (visitX (rep wallWidth [true] wallBase) [0] debris) := by
  have joined := steps_seq trans blankEntry collisionFromEntry
  exact joined

/-- The exact tape after erasing the new wall and its 1322-cell predecessor. -/
def restart : Config :=
  ⟨exterior, rep 1324 [false] (rep 6 [true]
    (rep (wallWidth-3) [false] (rep 4 [true] debris))), .A⟩

private theorem twoWalls (w m : Nat) (L R : Tape) :
    steps ((7+(w+2)) + (20+(m+2)))
      (visitX (rep (w+3) [true] (cons false (oldWall m L))) [0] R) =
      some ⟨L, rep (4+m) [false] (rep 6 [true]
        (rep w [false] (rep 4 [true] R))), .A⟩ := by
  rw [rep_add 4 m]
  have a := emptyWall (w+2) (oldWall m L) R
  have b := oldWallStep m L (rep w [false] (rep 4 [true] R))
  exact steps_seq trans a b

attribute [local irreducible] TM.steps TM.rep

theorem eraseBoth : steps 18396801869136
    (visitX (rep wallWidth [true] wallBase) [0] debris) = some restart := by
  have h := twoWalls (wallWidth-3) 1320 exterior debris
  exact h

theorem blankRestart : steps 4679860003204851 init = some restart := by
  have joined := steps_seq trans blankCollision eraseBoth
  exact joined

#print axioms phase
#print axioms collisionFromEntry
#print axioms eraseBoth
#print axioms blankRestart
end H7846.Line24
