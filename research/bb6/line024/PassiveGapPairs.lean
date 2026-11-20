import TerminalGap

namespace H7846.Line24
open TM Word

namespace PassiveGaps

/-- All possible immediate predecessors under the ordinary pass rules. -/
def previous : Word → List Word
  | .tip j => match j with
    | n+2 => [.d (n+1) (.d 1 (.d 0 (.tip 0)))]
    | _ => []
  | .d digit y =>
    (match y with | .tip 0 => [.tip digit] | _ => []) ++
    (if digit = 0 then [] else (previous y).map (.d digit)) ++
    (match y with | .d 1 (.d 1 (.tip 0)) => [.d (digit+2) (.d 0 (.tip 0))] | _ => []) ++
    (match digit with | n+3 => [.d (n+1) (.d 1 (.d 0 (.d 1 y)))] | _ => []) ++
    (match y with
      | .d 1 (.d 2 z) => (previous z).map (fun x => .d (digit+2) (.d 0 (.d 1 x)))
      | _ => [])

theorem previousCovers {x y : Word} (h : Pass x y) : x ∈ previous y := by
  induction h with
  | tipStep j => rw [previous.eq_def]; simp
  | keep i _ ih => rw [previous.eq_def]; simp [ih]
  | split m => rw [previous.eq_def]; simp
  | mergeTail i => rw [previous.eq_def]; simp
  | mergeDigit i y => rw [previous.eq_def]; simp
  | carry m _ ih => rw [previous.eq_def]; simp [ih]

/-- Words reached by reading exactly n ordinary passes backwards. -/
def previousAt : Nat → Word → List Word
  | 0,y => [y]
  | n+1,y => (previous y).flatMap (previousAt n)

theorem previousAtCovers {x y k} (h : Passes k x y) : x ∈ previousAt k y := by
  induction h with
  | refl => simp [previousAt]
  | next _ last ih => exact List.mem_flatMap.mpr ⟨_,previousCovers last,ih⟩

private theorem noLonger {x y k n} (h : Passes k x y) (big : n ≤ k) :
    ∃ z, z ∈ previousAt n y := by
  induction n generalizing x y k with
  | zero => exact ⟨y,by simp [previousAt]⟩
  | succ n ih =>
    cases h with
    | refl => omega
    | next initial last =>
      obtain ⟨z,hz⟩ := ih initial (by omega)
      exact ⟨z,List.mem_flatMap.mpr ⟨_,previousCovers last,hz⟩⟩

/-- The two last phases of a stack with ordinary passes and a middle 1,0,1
wall opening. Both walls start at width two. The ordered gap pair is far
more restricted than divisibility of both spacings by three. -/
theorem adjacent {x y : Word} {a b : Nat}
    (earlier : Passes a x (.d 1 (.d 0 (.d 1 y))))
    (last : Passes b y (.d 1 (.d 0 (.tip 0)))) :
    (b=1 ∧ a≤11) ∨ ((b=0 ∨ b=2) ∧ a=0) := by
  rcases terminalHistories last with ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩ | ⟨rfl,rfl⟩
  · right; refine ⟨Or.inl rfl,?_⟩
    apply Classical.byContradiction
    intro he
    obtain ⟨_,bad⟩ := noLonger earlier (show 1 ≤ a by omega)
    change _ ∈ ([] : List Word) at bad; contradiction
  · left; refine ⟨rfl,?_⟩
    apply Classical.byContradiction
    intro he
    obtain ⟨_,bad⟩ := noLonger earlier (show 12 ≤ a by omega)
    change _ ∈ ([] : List Word) at bad; contradiction
  · right; refine ⟨Or.inr rfl,?_⟩
    apply Classical.byContradiction
    intro he
    obtain ⟨_,bad⟩ := noLonger earlier (show 1 ≤ a by omega)
    change _ ∈ ([] : List Word) at bad; contradiction


private theorem suffixRun {x y : Word} {k : Nat} (h : Passes k x y) (n : Nat) (le : n ≤ k) :
    ∃ u, Passes n u y := by
  induction n generalizing x y k with
  | zero => exact ⟨y,.refl y⟩
  | succ n ih =>
    cases h with
    | refl => omega
    | next initial last =>
      obtain ⟨z,hz⟩ := ih initial (by omega)
      exact ⟨z,.next hz last⟩

private theorem eleven : Passes 11 (.d 2 (.tip 1)) (.d 1 (.d 0 (.d 1 (.d 1 (.tip 0))))) := by
  have p0 := Passes.refl (.d 2 (.tip 1))
  have p1 := Passes.next p0 (Pass.keep 1 (Pass.tipStep 1))
  have p2 := Passes.next p1 (Pass.keep 1 (Pass.keep 0 (Pass.tipStep 0)))
  have p3 := Passes.next p2 (Pass.mergeTail 1)
  have p4 := Passes.next p3 (Pass.tipStep 3)
  have p5 := Passes.next p4 (Pass.keep 2 (Pass.tipStep 0))
  have p6 := Passes.next p5 (Pass.split 1)
  have p7 := Passes.next p6 (Pass.keep 0 (Pass.keep 0 (Pass.keep 0 (Pass.tipStep 0))))
  have p8 := Passes.next p7 (Pass.keep 0 (Pass.mergeTail 0))
  have p9 := Passes.next p8 (Pass.keep 0 (Pass.tipStep 2))
  have p10 := Passes.next p9 (Pass.keep 0 (Pass.keep 1 (Pass.tipStep 0)))
  have p11 := Passes.next p10 (Pass.keep 0 (Pass.split 0))
  exact p11

/-- All fourteen possible pairs occur in the ordinary-pass model with some
initial word. Physical gap parameters are 3(a+1) and 3(b+1) when each wall
starts at width two. Blank-tape reachability is a separate condition. -/
theorem adjacentIff (a b : Nat) :
    (∃ x y : Word, Passes a x (.d 1 (.d 0 (.d 1 y))) ∧
      Passes b y (.d 1 (.d 0 (.tip 0)))) ↔
      (b=1 ∧ a≤11) ∨ ((b=0 ∨ b=2) ∧ a=0) := by
  constructor
  · rintro ⟨_,_,earlier,last⟩; exact adjacent earlier last
  · rintro (⟨rfl,le⟩ | ⟨hb,rfl⟩)
    · obtain ⟨x,h⟩ := suffixRun eleven a le
      exact ⟨x,_,h,.next (.refl _) (.keep 0 (.tipStep 0))⟩
    · rcases hb with rfl | rfl
      · exact ⟨_,_,.refl _,.refl _⟩
      · exact ⟨_,_,.refl _,.next (.next (.refl _) (.tipStep 1)) (.keep 0 (.tipStep 0))⟩

#print axioms adjacentIff
end PassiveGaps
end H7846.Line24
