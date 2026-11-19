(** Failure of independent half-tape induction at canonical sweep checkpoints.
    All finite words are nearest-first and have implicit infinite zero tails. *)
From BusyCoq Require Import Individual62 Line429Engine Line429RightSweep
  Line429LeftLanguage Line429Gate Line429GateBlank.
From Coq Require Import List.
Import ListNotations Bell429 LeftLanguage429 GateBlank429.
Open Scope sym_scope.
Module GateSplice429.
Definition u : list Sym := [0;1;1;0;1;1;0;1].
Definition w : list Sym := [1;1;1;1;0;0;1;0;0;1].
Definition u39 : list Sym := [0;0;1;1;0;1;1;0;1].
Definition w39 : list Sym := [0;1;1;1;0;0;1;0;1].
Definition u93 : list Sym := [1;0;1;0;0;0;1;1;0;1;1;0;1].
Definition w93 : list Sym := [0;0;1;1;0;0;1;0;0;1].

Tactic Notation "replay" int_or_var(n) :=
  unfold checkpoint, AR, u, w, u39, w39, u93, w93; simpl_tape;
  do n (eapply multistep_S; [prove_step|simpl_tape]);
  repeat rewrite <- (const_unfold _ S0);
  apply multistep_0.

Theorem source_39 : (B;;tape0) -[src_tm]->> 39 / checkpoint [] w.
Proof. replay 39. Qed.
Theorem source_107 : (B;;tape0) -[src_tm]->> 107 / checkpoint u [0;1].
Proof. replay 107. Qed.
Theorem crossed_39 : checkpoint u w -[src_tm]->> 39 / checkpoint u39 w39.
Proof. replay 39. Qed.
Theorem crossed_93 : checkpoint u w -[src_tm]->> 93 / checkpoint u93 w93.
Proof. replay 93. Qed.
Theorem left_stop_gate_closed : accepts MJ (u39 *> 0inf) Stop /\ Gate429.gate Gate429.fresh true true w39=false.
Proof. split; [apply Jbad|reflexivity]. Qed.
Theorem both_open : accepts MJ (u93 *> 0inf) Stop /\ Gate429.gate Gate429.fresh true true w93=true.
Proof. split; [apply J1,L01,Lbad|reflexivity]. Qed.
Theorem crossed_halts : halts_in src_tm (checkpoint u w) 107.
Proof. eexists. split; [eapply multistep_trans with (n:=93%nat) (m:=14%nat);
  [apply crossed_93|unfold checkpoint, AR, u93, w93; do 14 (eapply multistep_S; [prove_step|simpl_tape]); apply multistep_0]|reflexivity]. Qed.

Theorem independent_languages_insufficient (P H : list Sym -> Prop) :
  (forall x z, (B;;tape0) -[src_tm]->* checkpoint x z -> P x /\ H z) ->
  (forall x z, P x -> H z -> ~halts src_tm (checkpoint x z)) -> False.
Proof.
  intros cover safe. pose proof (cover _ _ (without_counter _ _ _ _ source_107)) as [Pu _].
  pose proof (cover _ _ (without_counter _ _ _ _ source_39)) as [_ Hw].
  apply (safe _ _ Pu Hw). exists 107%nat; exact crossed_halts.
Qed.
End GateSplice429.
Print Assumptions GateSplice429.independent_languages_insufficient.
Print Assumptions GateSplice429.both_open.
