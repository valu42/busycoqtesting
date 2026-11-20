import Return

namespace H7846.Line24
open TM Word

/-- A finite window with both exterior streams kept opaque. -/
private def window (c : FCfg St) (L R : Tape) : Config := ⟨app c.l L,app c.r R,c.st⟩

private def clippedSteps : Nat → FCfg St → Option (FCfg St)
  | 0,c => some c
  | n+1,c => if c.l.isEmpty || c.r.isEmpty then none else (fstep c).bind (clippedSteps n)

private theorem oneWindow (c : FCfg St) (L R : Tape) (hl : c.l.isEmpty=false) (hr : c.r.isEmpty=false) :
    step (window c L R) = (fstep c).map (fun d => window d L R) := by
  obtain ⟨l,r,s⟩ := c
  cases l with
  | nil => contradiction
  | cons b l =>
    cases r with
    | nil => contradiction
    | cons z r =>
      simp only [step,TM.step,fstep,TM.fstep,window,app_cons,cons_zero,List.headD_cons]
      cases trans s z with
      | none => rfl
      | some p => obtain ⟨w,d,s'⟩ := p; cases d <;> rfl

private theorem windowRun {n : Nat} {c d : FCfg St} (h : clippedSteps n c=some d) (L R : Tape) :
    steps n (window c L R) = some (window d L R) := by
  induction n generalizing c with
  | zero => simp [clippedSteps] at h; subst d; rfl
  | succ n ih =>
    cases hl : c.l.isEmpty <;> cases hr : c.r.isEmpty <;> simp [clippedSteps,hl,hr] at h
    cases hs : fstep c with
    | none => simp [hs] at h
    | some c' =>
      simp [hs] at h
      have v := oneWindow c L R hl hr
      rw [hs, Option.map_some] at v
      rw [show steps (n+1) (window c L R) = steps n (window c' L R) from steps_succ_of_step trans n v]
      exact ih h

private def outerBits := runs [(true,5),(false,1),(true,2),(false,1),(true,3)]
private def markerBits := runs [(false,1324),(true,6),(false,8628),(true,6)]
private def initial : FCfg St :=
  ⟨outerBits ++ List.replicate 64 false,markerBits ++ List.replicate 10036 false,.A⟩

def secondEntryWord := word [1,3,1,1,4,2,2,4,4,3,1,0,1,0] 0
private def wordBits := runs [(true,1),(false,1),(true,3),(false,1),(true,9),(false,1),
  (true,3),(false,1),(true,3),(false,1),(true,12),(false,1),(true,6),(false,1),
  (true,6),(false,1),(true,12),(false,1),(true,12),(false,1),(true,9),(false,1),
  (true,3),(false,2),(true,3),(false,2),(true,7)]
private def leftBits := false :: (List.replicate 8588 true ++ [false,true,true,false] ++
    List.replicate 8630 true ++ [false,true,true,false] ++ List.replicate 1322 true ++ false :: outerBits)
private def reached : FCfg St :=
  ⟨leftBits ++ List.replicate 16 false,wordBits ++ List.replicate 1394 false, .D⟩

private theorem replay : clippedSteps 2897684 initial = some reached := by decide +native

private theorem asRep (n : Nat) (b : Bool) (S : Tape) :
    app (List.replicate n b) S = rep n [b] S := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [List.replicate_succ,app_cons,rep_succ,app]; rw [ih]

private theorem markerForm (S : Tape) : app markerBits S =
    rep 1324 [false] (rep 6 [true] (rep 8628 [false] (rep 6 [true] S))) := by
  unfold markerBits runs
  simp only [List.flatMap_cons,List.flatMap_nil,List.append_nil,← app_app,asRep]

private def markersAfterThird := markers [0,6,30,126,510,2046,8190,32766,131070,524286,2097150,8388606,33554430] clearTail
/-- Stream after the third six-one marker, including the remote original debris. -/
def thirdAfter : Tape := Box.cut 18396693862460 markersAfterThird (rep 4 [true] debris)
def thirdMarkerTail : Tape := rep 6 [true] thirdAfter

private theorem baseShape : (regenerated returnedWidths exterior).r =
    app markerBits (rep 107996733 [false] (rep 6 [true] markersAfterThird)) := by
  rw [markerForm,show 1324=4+1320 by decide,rep_add 4 1320]
  rfl

private theorem cutRun (b : Bool) (n k : Nat) (X Y : Tape) :
    Box.cut (n+k) (rep n [b] X) Y = rep n [b] (Box.cut k X Y) := by
  induction n with
  | zero => simp
  | succ n ih =>
    rw [show (n+1)+k=(n+k)+1 by omega]
    exact congrArg (cons b) ih

/-- A six-one marker and the remaining stack, clipped where the old debris begins.
The list order is the same as in `markers`, with the nearest gap last. -/
def pendingMarker (clearance : Nat) (ws : List Nat) : Tape :=
  Box.cut clearance (rep 6 [true] (markers ws clearTail)) (rep 4 [true] debris)

theorem pendingMarker_next (n g : Nat) (ws : List Nat) :
    pendingMarker (6+(g+n)) (ws ++ [g]) = rep 6 [true] (rep g [false] (pendingMarker n ws)) := by
  unfold pendingMarker markers
  rw [List.foldl_append]
  change Box.cut (6+(g+n)) (rep 6 [true] (rep g [false] _)) _ = _
  rw [cutRun,cutRun]

theorem pendingMarker_last (n : Nat) :
    pendingMarker (6+(2+(4+n))) [] = rep 6 [true] (rep 2 [false] (rep 4 [true]
      (rep n [false] (rep 4 [true] debris)))) := by
  change Box.cut (6+(2+(4+n))) (rep 6 [true] (rep 2 [false] (rep 4 [true] blank))) _ = _
  rw [cutRun,cutRun,cutRun,Box.zeros]

def fourthMarkerTail : Tape := pendingMarker 18396660308030
    [0,6,30,126,510,2046,8190,32766,131070,524286,2097150,8388606]

def fifthMarkerTail : Tape := pendingMarker 18396651919418
    [0,6,30,126,510,2046,8190,32766,131070,524286,2097150]

theorem fourthMarkerTail_eq :
    fourthMarkerTail = rep 6 [true] (rep 8388606 [false] fifthMarkerTail) :=
  by
    have h := pendingMarker_next 18396651919418 8388606 [0,6,30,126,510,2046,8190,32766,131070,524286,2097150]
    exact h

theorem thirdMarkerTail_eq :
    thirdMarkerTail = rep 6 [true] (rep 33554430 [false] fourthMarkerTail) := by
  apply congrArg (rep 6 [true])
  change Box.cut (33554430+18396660308030) (rep 33554430 [false] _) _ = _
  rw [cutRun]
  rfl

private theorem secondSource : secondRestart.r = app markerBits (rep 107996733 [false] thirdMarkerTail) := by
  change Box.cut 18396801869163 (regenerated returnedWidths exterior).r _ = _
  rw [baseShape]
  have len : markerBits.length = 9964 := by decide +native
  rw [show 18396801869163 = markerBits.length+(107996733+(6+18396693862460)) by omega,
    Box.front,cutRun,cutRun]
  rfl

theorem secondRestartFront : secondRestart.r =
    app (runs [(false,1324),(true,6),(false,8628),(true,6)])
      (rep 107996733 [false] thirdMarkerTail) := secondSource

/-- Exact two-marker prefix, with the tape beginning at the old third-marker
position freely replaceable. -/
def twoMarkerSource (R : Tape) : Config :=
  ⟨exterior,app markerBits (rep 107996733 [false] R),.A⟩

theorem secondRestartSource : secondRestart = twoMarkerSource thirdMarkerTail := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  exact ⟨rfl,secondSource,rfl⟩

private def rightWing (R : Tape) := rep 107986697 [false] R

private theorem sourceWindow (R : Tape) : window initial blank (rightWing R) = twoMarkerSource R := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  refine ⟨?_,?_,rfl⟩
  · change app (outerBits ++ List.replicate 64 false) blank = exterior
    rw [← app_app,asRep,Box.zeroBlank]; rfl
  · change app (markerBits ++ List.replicate 10036 false) (rightWing R) =
      app markerBits (rep 107996733 [false] R)
    rw [← app_app,asRep]
    unfold rightWing
    rw [← rep_add]

def secondEntryModel : Config := visitX (stackBase 8588 [8628,1320] exterior) [] secondEntryWord.tape

private theorem appOnes (n : Nat) (xs : List Bool) (L : Tape) :
    app (List.replicate n true ++ xs) L = rep n [true] (app xs L) := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [List.replicate_succ,List.cons_append,app_cons,rep_succ,app]; rw [ih]

private theorem leftShape : app leftBits blank = secondEntryModel.l := by
  unfold leftBits
  simp only [List.append_assoc,app_cons,appOnes,List.cons_append,List.nil_append]
  rfl

private theorem wordShape : app wordBits blank = secondEntryModel.r := by rfl

def secondEntryWith (R : Tape) : Config :=
  ⟨secondEntryModel.l, Box.cut 107988195 secondEntryModel.r R,.D⟩

private theorem reachedWindow (R : Tape) : window reached blank (rightWing R) = secondEntryWith R := by
  apply Cfg.mk.injEq _ _ _ _ _ _ |>.mpr
  refine ⟨?_,?_,rfl⟩
  · change app (leftBits ++ List.replicate 16 false) blank = _
    rw [← app_app,asRep,Box.zeroBlank]; exact leftShape
  · change app (wordBits ++ List.replicate 1394 false) (rightWing R) =
      Box.cut 107988195 secondEntryModel.r R
    have len : wordBits.length = 104 := by decide +native
    rw [← wordShape,show 107988195 = wordBits.length+107988091 by omega,Box.front,Box.zeros,
      ← app_app,asRep]
    unfold rightWing
    rw [← rep_add]

theorem twoMarkerEntry (R : Tape) : steps 2897684 (twoMarkerSource R) = some (secondEntryWith R) := by
  have h := windowRun replay blank (rightWing R)
  rwa [sourceWindow,reachedWindow] at h

def secondEntryCfg : Config := secondEntryWith thirdMarkerTail

theorem secondEntry : steps 2897684 secondRestart = some secondEntryCfg := by
  rw [secondRestartSource]
  exact twoMarkerEntry _

theorem blankSecondEntry : steps 4679882757623815 init = some secondEntryCfg := by
  have h := steps_seq trans blankSecondRestart secondEntry
  exact h

#print axioms secondEntry
end H7846.Line24
