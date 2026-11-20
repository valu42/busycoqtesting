import PackedTape
import Wall

namespace H7846.Line24.PackedTape
open TM

/-- Left and right arguments are the two half-tapes beyond the entire matched prefix. -/
def emptyIn (w : Nat) (L R : Runs) : Pack :=
  ⟨prepend [(false,1),(true,w+1),(false,1)] L,prepend [(true,1),(false,2)] R,.D⟩
def emptyOut (w : Nat) (L R : Runs) : Pack := ⟨L,prepend [(false,w+2),(true,4)] R,.A⟩

theorem packedEmpty (w : Nat) (L R : Runs) :
    H7846.steps (7+w) (emptyIn w L R).toCfg = some (emptyOut w L R).toCfg := by
  unfold emptyIn emptyOut Pack.toCfg
  simp only [denotePrepend]
  exact emptyWall w (denote L) (denote R)

def oldIn (m : Nat) (L R : Runs) : Pack :=
  ⟨prepend [(true,2),(false,1),(true,m+2),(false,1)] L,push false 4 R,.A⟩
def oldOut (m : Nat) (L R : Runs) : Pack := ⟨L,prepend [(false,4+m),(true,6)] R,.A⟩

theorem packedOld (m : Nat) (L R : Runs) :
    H7846.steps (20+(m+2)) (oldIn m L R).toCfg = some (oldOut m L R).toCfg := by
  unfold oldIn oldOut Pack.toCfg
  simp only [denotePrepend,denotePush,denoteWith]
  rw [rep_add 4 m]
  exact oldWallStep m (denote L) (denote R)

def eraseIn (n : Nat) (L R : Runs) : Pack :=
  ⟨prepend [(true,n),(false,1)] L,push true 1 R,.A⟩
def eraseOut (n : Nat) (L R : Runs) : Pack := ⟨L,push false (n+2) R,.A⟩

private theorem eraseOnes (n : Nat) (L R : Tape) :
    H7846.steps (n+1) ⟨rep n [true] (cons false L),cons true R,.A⟩ =
      some ⟨L,rep (n+2) [false] R,.A⟩ := by
  induction n generalizing R with
  | zero => rfl
  | succ n ih =>
    have first : H7846.step ⟨rep (n+1) [true] (cons false L),cons true R,.A⟩ =
        some ⟨rep n [true] (cons false L),cons true (cons false R),.A⟩ := rfl
    change TM.steps trans _ _ = _
    rw [steps_succ_of_step trans (n+1) first]
    have z := ih (cons false R)
    rw [show rep (n+2) [false] (cons false R) = rep ((n+2)+1) [false] R from rep_app_comm _ _ _] at z
    exact z

theorem packedErase (n : Nat) (L R : Runs) :
    H7846.steps (n+1) (eraseIn n L R).toCfg = some (eraseOut n L R).toCfg := by
  unfold eraseIn eraseOut Pack.toCfg
  simp only [denotePrepend,denotePush,denoteWith]
  exact eraseOnes n (denote L) (denote R)

def separatorChain : Nat → Runs → Runs
  | 0,L => L
  | n+1,L => prepend [(true,2),(false,1)] (separatorChain n L)

private theorem denoteChain (n : Nat) (L : Runs) :
    denote (separatorChain n L) = rep n [true,true,false] (denote L) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    change denote (prepend _ _) = _
    rw [denotePrepend,ih]; rfl

private theorem threeOnes (n : Nat) (L : Tape) : rep (3*n) [true] L = rep n [true,true,true] L := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [show 3*(n+1)=3+3*n by omega,rep_add,ih]; rfl

def digitIn (k : Nat) (L R : Runs) : Pack :=
  ⟨push false 1 L,prepend [(true,1),(false,1),(true,3),(false,2),(true,3*k),(false,1)] R,.D⟩
def digitOut (k : Nat) (L R : Runs) : Pack :=
  ⟨push false 1 (separatorChain (k+1) (push true 3 L)),prepend [(true,1),(false,1)] R,.D⟩

theorem packedDigit (k : Nat) (L R : Runs) :
    H7846.steps (26+(k+1)*3+3) (digitIn k L R).toCfg = some (digitOut k L R).toCfg := by
  unfold digitIn digitOut Pack.toCfg
  simp only [denotePrepend,denotePush,denoteChain,denoteWith]
  rw [threeOnes k]
  exact wallNextDigit k (denote L) (denote R)

def tailIn (j : Nat) (L R : Runs) : Pack :=
  ⟨push false 1 L,prepend [(true,1),(false,1),(true,3),(false,2),(true,7+3*j)] R,.D⟩
def tailOut (j : Nat) (L R : Runs) : Pack :=
  ⟨separatorChain (j+4) (push true 3 L),R,.D⟩

theorem packedTail (j : Nat) (L R : Runs) :
    H7846.steps (26+(j+4)*3) (tailIn j L R).toCfg = some (tailOut j L R).toCfg := by
  unfold tailIn tailOut Pack.toCfg
  simp only [denotePrepend,denotePush,denoteChain,denoteWith]
  exact wallTail j (denote L) (denote R)

end H7846.Line24.PackedTape
