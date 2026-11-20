import CollisionRules
namespace H7846.Line24
open TM Word
set_option maxRecDepth 100000
set_option maxHeartbeats 1500000

/-- A merged six-one pair followed by enough blanks for the local return. -/
def clearDouble (R : Tape) := rep 12 [true] (rep 12 [false] R)
def doubleAfter (R : Tape) := rep 7 [true] (cons false (rep 3 [true] (cons false (rep 6 [true] R))))

/-- The innermost packet of the observed marker train. -/
def innerPacket (R : Tape) := rep 12 [true] (rep 2 [false] (rep 4 [true] R))
def packetAfter (R : Tape) := rep 6 [true] (rep 6 [false] (innerPacket R))

theorem doubleGapOne (j : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (cons false (clearDouble R)))
      (blkV (j+1) (rep 7 [false] (doubleAfter R))) (14*j+330) := by
  have h := extendTail (X := cons false (clearDouble R))
      (Y := blkV 1 (rep 7 [false] (doubleAfter R))) (t := 330)
      (by intro L; rfl) (by intro L; rfl) (by decide) j
  change Timed _ (rep j [true,true,true] (app [true,true,true] _)) _ at h
  rw [rep_app_comm] at h
  exact h

theorem doubleGapThree (j : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (rep 3 [false] (clearDouble R)))
      (blkV j (blkV 1 (rep 8 [false] (doubleAfter R)))) (14*j+352) :=
  extendTail (t := 352) (by intro L; rfl) (by intro L; rfl) (by decide) j

theorem packetGapOne (j : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (cons false (innerPacket (rep 43 [false] R))))
      (blkV (j+1) (rep 32 [false] (packetAfter R))) (14*j+1416) := by
  have h := extendTail (X := cons false (innerPacket (rep 43 [false] R)))
      (Y := blkV 1 (rep 32 [false] (packetAfter R))) (t := 1416)
      (by intro L; rfl) (by intro L; rfl) (by decide) j
  change Timed _ (rep j [true,true,true] (app [true,true,true] _)) _ at h
  rw [rep_app_comm] at h
  exact h

theorem packetGapThree (j : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (rep 3 [false] (innerPacket (rep 43 [false] R))))
      (blkV j (blkV 1 (rep 33 [false] (packetAfter R)))) (14*j+1438) :=
  extendTail (t := 1438) (by intro L; rfl) (by intro L; rfl) (by decide) j

/-- For even clearances the four-one terminator remains the rightmost run
and the sweep advances seven places past its end. -/
def packetEvenAfter (R : Tape) := blkV 1 (blkV 2 (cons false (rep 4 [true] R)))

theorem packetGapZero (j : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (innerPacket (rep 7 [false] R)))
      (blkV (j+4) (packetEvenAfter R)) (14*j+154) := by
  have h := extendTail (X := innerPacket (rep 7 [false] R))
    (Y := blkV 4 (packetEvenAfter R)) (t := 154)
    (by intro L; rfl) (by intro L; rfl) (by decide) j
  unfold blkV at h ⊢
  rw [← rep_add j 4] at h
  exact h

theorem packetGapTwo (j : Nat) (R : Tape) :
    Timed (rep (7+3*j) [true] (rep 2 [false] (innerPacket (rep 7 [false] R))))
      (blkV j (blkV 1 (blkV 3 (packetEvenAfter R)))) (14*j+176) :=
  extendTail (t := 176) (by intro L; rfl) (by intro L; rfl) (by decide) j

#print axioms packetGapThree
end H7846.Line24
