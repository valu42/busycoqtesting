(* A research DFA generator for the existing, proved FAR procedure.
   It records a polynomial residue of the whole word, together with a
   bounded suffix. This differs from the RWL/LRU/n-gram generators tried
   in the earlier holdout passes. No solved holdout is asserted here.

   The soundness argument is entirely the existing FAR theorem: ANY
   generator is allowed; a positive answer still needs a closed saturation.
   Word orientation is the FAR engine's orientation. No semantic claim
   about an integer represented by the TM's tape is assumed.
   decide_spec inherits FAR's primitive integer/array specifications and
   LibTactics.inj_pair2; its assumptions are not closed. No new axiom is
   introduced. Native positive candidates must be replayed in Coq.
   AI-assisted research by Codex; FAR is the repository authors' work. *)
From BusyCoq Require Import Individual62 CTL HashTable.
From Coq Require Import NArith ZArith.
Require Uint63.

Module AlgebraicFAR.
Module DC := DHTMFromTM BB62.
Module Generator <: CTLCtx Uint63_K DC.TMCtx.
Definition config_t := (Uint63.int * Uint63.int * Uint63.int)%type.
Definition global_state_t := config_t.
Definition global_state_init (x : config_t) := x.
Definition dfa_state_0 := int0.
Definition dfa_trans (x : Uint63.int) (s : BB62.Sym) (_ : dir)
    (cfg : global_state_t) : Uint63.int * global_state_t :=
  let '(modulus,multiplier,suffix_size) := cfg in
  let b := match s with S0 => int0 | S1 => int1 end in
  let residue := Uint63.div x suffix_size in
  let suffix := Uint63.mod x suffix_size in
  let residue' := Uint63.mod (Uint63.add (Uint63.mul residue multiplier) b) modulus in
  let suffix' := Uint63.mod (Uint63.add (Uint63.mul suffix (Uint63.of_Z 2%Z)) b) suffix_size in
  (Uint63.add (Uint63.mul residue' suffix_size) suffix',cfg).
End Generator.
Module Engine := FAR Uint63_K DC.TMCtx Generator.

Definition decide (tm : TM) (modulus multiplier suffix_size maxS maxT : N) :=
  Engine.FAR_decide_nonhalt tm
    (N_to_int modulus,N_to_int multiplier,N_to_int suffix_size)
    maxS maxT maxT.

Theorem decide_spec tm modulus multiplier suffix_size maxS maxT :
  decide tm modulus multiplier suffix_size maxS maxT = true -> ~halts tm c0.
Proof.
  intro H.
  unfold decide in H.
  apply Engine.FAR_decide_nonhalt_spec in H.
  rewrite halts_halts'.
  apply DC.map_nonhalt.
  rewrite <-Engine.TM.halts_halts'.
  exact H.
Qed.
Print Assumptions decide_spec.
End AlgebraicFAR.
