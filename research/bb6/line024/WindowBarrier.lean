import SecondEntry
import MarkerTest

namespace H7846.Line24
open TM
set_option maxRecDepth 40000

private theorem prependBits (n : Nat) (b : Bool) (T : Tape) :
    app (List.replicate n b) T = rep n [b] T := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [List.replicate_succ,app_cons,rep_succ,app]; rw [ih]

private theorem bitAt (n : Nat) (b : Bool) (T : Tape) (i : Nat) :
    rep n [b] T i = if i<n then b else T (i-n) := by
  induction n generalizing i with
  | zero => simp
  | succ n ih => cases i with
    | zero => simp
    | succ i => simp [ih]

/-- Around the original second marker and the six-cell edit, the only
genuinely reachable ones are those in the second marker. -/
private theorem localBits (i : Nat) (lo : 1330≤i) (hi : i<108006697) :
    secondRestart.r i = decide (9958≤i ∧ i<9964) := by
  rw [secondRestartFront]
  have prefixEq (T : Tape) :
      app (runs [(false,1324),(true,6),(false,8628),(true,6)]) T =
        rep 1324 [false] (rep 6 [true] (rep 8628 [false] (rep 6 [true] T))) := by
    unfold runs
    simp only [List.flatMap_cons,List.flatMap_nil,List.append_nil,← app_app,prependBits]
  rw [prefixEq,bitAt,ite_eq_right (by omega),bitAt,ite_eq_right (by omega),bitAt]
  split
  · rw [decide_eq_false (by omega)]
  · rw [bitAt]; split
    · rw [decide_eq_true (by omega)]
    · rw [bitAt,ite_eq_left (by omega),decide_eq_false (by omega)]

/-- All right-hand length-n windows of a have witnesses among those of b,
at locations congruent modulo q. Positions are measured from the current
head. The unaugmented case takes q=1. -/
def rightCovered (n q : Nat) (a b : Config) : Prop :=
  ∀ i : Nat, ∃ j : Nat, i%q=j%q ∧ ∀ k < n, a.r (i+k) = b.r (j+k)

/-- With any left window, this altered halting tape has the genuine local
configuration and only genuine right n-grams up to width 8627. Eight,
for example, is an admissible modulus for matching positions. -/
theorem twinCovered (n q : Nat) (hn : n≤8627) (hq : q ∣ 8632) :
    rightCovered n q (withThirdMarker secondRestart) secondRestart ∧
      ∀ k ≤ n, (withThirdMarker secondRestart).r k = secondRestart.r k := by
  constructor
  · intro i
    by_cases hit : i<18596 ∧ 18590<i+n
    · refine ⟨i-8632,?_,?_⟩
      · have e : i = i-8632+8632 := by omega
        calc i%q = (i-8632+8632)%q := congrArg (·%q) e
             _ = (i-8632)%q := by simp [Nat.add_mod,Nat.mod_eq_zero_of_dvd hq]
      · intro k hk
        change (if 18590 ≤ i+k ∧ i+k < 18596 then true else _) = _
        rw [localBits (i+k) (by omega) (by omega),
            localBits (i-8632+k) (by omega) (by omega)]
        split
        · rw [decide_eq_true (by omega)]
        · rw [decide_eq_false (by omega),decide_eq_false (by omega)]
    · refine ⟨i,rfl,?_⟩
      intro k hk
      change (if _ then true else _) = _
      rw [ite_eq_right (by omega)]
  · intro k hk
    change (if _ then true else _) = _
    rw [ite_eq_right (by omega)]

/-- Any inductive abstraction that admits every configuration with the same
left tape, state, read window, and covered right windows as an accepted
one must admit a reachable undefined instruction in its abstract set. -/
theorem noRightWindowCertificate (n q : Nat) (hn : n ≤ 8627) (hq : q ∣ 8632)
    (I : Config → Prop) (initial : I init)
    (closed : ∀ {c d}, I c → step c = some d → I d)
    (covered : ∀ a b : Config, I b → a.l=b.l → a.st=b.st →
       (∀ k ≤ n, a.r k = b.r k) → rightCovered n q a b → I a) :
    ∃ c, I c ∧ step c = none := by
  have follow (m : Nat) {a b : Config} (ha : I a) (run : steps m a = some b) : I b := by
    induction m generalizing a with
    | zero => simp [steps,TM.steps] at run; exact run ▸ ha
    | succ m ih =>
      cases e : step a with
      | none =>
        change TM.step trans a = none at e
        simp [steps,TM.steps,e] at run
      | some z =>
        rw [show steps (m+1) a = steps m z from steps_succ_of_step trans m e] at run
        exact ih (closed ha e) run
  have actual := follow _ initial blankSecondRestart
  obtain ⟨grams,localMatch⟩ := twinCovered n q hn hq
  have altered := covered (withThirdMarker secondRestart) secondRestart actual rfl rfl localMatch grams
  obtain ⟨c,run,halt⟩ := sixCellWitness
  exact ⟨c,follow _ altered run,halt⟩

#print axioms noRightWindowCertificate
end H7846.Line24
