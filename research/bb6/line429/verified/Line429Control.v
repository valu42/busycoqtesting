From BusyCoq Require Import Individual62 Line429Engine.
From BusyCoq Require Import Line429RightSweep Line429LeftLanguage.
From Coq Require Import List.
Import ListNotations Bell429 LeftLanguage429.
Open Scope list_scope.
Open Scope sym_scope.

Module Control429.
Definition one_mark := B;; ([0;0;0;0;0;1] *> 0inf) {{S0}} 0inf.
Lemma closed_mark :
  one_mark -[src_tm]->> 4 / AR ([0;0;0;1] *> 0inf) ([1;1;1] *> 0inf).
Proof. unfold one_mark,AR; simpl_tape; do 4 (eapply multistep_S; [prove_step|simpl_tape]); constructor. Qed.
Lemma open_mark :
  one_mark -[src_tm]->> 16 / AR ([0;1;0;0;0;1] *> 0inf) ([1;0;1] *> 0inf).
Proof.
  unfold one_mark,AR; simpl_tape; do 16 (eapply multistep_S; [prove_step|simpl_tape]).
  repeat rewrite <- (const_unfold _ S0). constructor.
Qed.
Theorem mark_halts : halts_in src_tm one_mark 38.
Proof.
  eexists; split.
  - unfold one_mark; simpl_tape; do 38 (eapply multistep_S; [prove_step|simpl_tape]); constructor.
  - reflexivity.
Qed.
End Control429.
Print Assumptions Control429.mark_halts.
