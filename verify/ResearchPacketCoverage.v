(* Packet laws for supplied entries 405 and 482, found by finite simulation.
   The longitudinal packet/cycle method and boundary are from valu42's
   PacketHalt274 work; upstream PR #39 demonstrated automatic packet learning.
   These are new applications of that method, not new blank-run resolutions.
   The native stream evaluator and saved orbits are not verified here.
   AI-assisted by Codex. *)
From BusyCoq Require Import Individual62 Longitudinal.
From Coq Require Import String List Arith Lia.
Import ListNotations.
Open Scope list.

Module PacketCoverage.
Section Repeated.
Variable tm : TM.
Variable h : list (DH0*DH0).
Variable w : list Sym.
Hypothesis twice : segRLs tm (h^^1) (h^^2) w w.
Lemma repeated_calls n : segRLs tm (h^^n) (h^^(2*n)) w w.
Proof.
  pose proof (segRLs_addmul_v2 1 2 n 0 0 tm h w w ltac:(constructor) twice) as H.
  replace (n*1+0) with n in H by lia.
  replace (n*2+0) with (2*n) in H by lia. exact H.
Qed.
Lemma exponential_calls n m :
  segRLs tm (h^^n) (h^^(n*2^m)) (w^^m) (w^^m).
Proof.
  revert n; induction m; intro n.
  - cbn [Nat.pow lpow]; rewrite Nat.mul_1_r; apply segRLs_nil.
  - cbn [Nat.pow lpow].
    replace (n*(2*2^m)) with ((2*n)*2^m) by nia.
    eapply segRLs_concat; [apply repeated_calls|apply IHm].
Qed.
End Repeated.

Module Entry405.
Definition tm := Eval compute in TM_from_str "1RB0LB_0RC0LF_1LD1RE_0LA0RB_0RD0RF_0LA---".
Definition hR : DH0 := (C,[0]).
Definition hL : DH0 := (A,[0]).
Definition h := [(hR,hL)].
Definition laws : list (list Sym*list Sym*nat) := [
  ([0],[1],0%nat);
  ([0;0;0],[1;0;0],0%nat);
  ([1;0;0],[0;0;0],1%nat);
  ([0;1;0],[1;1;0],0%nat);
  ([1;1;0],[0;0;0],1%nat);
  ([0;0;1;0],[1;0;1;0],0%nat);
  ([1;0;1;0],[1;0;1;0],2%nat);
  ([0;0;1;1;0;0],[1;0;1;1;0;0],0%nat);
  ([1;0;1;1;0;0],[0;0;0;1;0;0],0%nat);
  ([0;0;0;1;0;0],[1;0;0;1;0;0],0%nat);
  ([1;0;0;1;0;0],[0;0;0;0;0;0],1%nat);
  ([0;0;0;0;0;0],[1;0;0;0;0;0],0%nat);
  ([1;0;0;0;0;0],[0;0;0;1;0;0],0%nat)].
Lemma laws_checked : Forall (fun '(u,v,k) => segRLs tm h (h^^k) u v) laws.
Proof.
  repeat (constructor; [apply BoundedConfig.segRLs_c_spec with (T:=1000); vm_compute; reflexivity|]).
  constructor.
Qed.
Lemma twice : segRLs tm (h^^1) (h^^2) [1;0;1;0] [1;0;1;0].
Proof. apply BoundedConfig.segRLs_c_spec with (T:=1000); vm_compute; reflexivity. Qed.
Theorem expanded_calls n m :
  segRLs tm (h^^n) (h^^(n*2^m)) ([1;0;1;0]^^m) ([1;0;1;0]^^m).
Proof. apply exponential_calls, twice. Qed.
Lemma halt_packet l r : halts tm (l {{{(hR,R)}}} [1;1;1] *> r).
Proof. unfold hR; solve_halt. Qed.
Definition boundary r := (A,(0inf,1,0>>r)).
Lemma boundary_entry r : boundary r -[tm]->* (0inf <*< [1]) {{{(hR,R)}}} [1;0] *> r.
Proof. unfold boundary,hR; esx. Qed.
Lemma blank_seed : c0 -[tm]->* boundary ([1] *> 0inf).
Proof. unfold boundary; esx. Qed.
(* A detector control, not a boundary claimed reachable from blank. *)
Lemma artificial_halt : halts tm (boundary ([1;0;0;1;1] *> 0inf)).
Proof. unfold boundary; solve_halt. Qed.
Print Assumptions laws_checked.
Print Assumptions halt_packet.
Print Assumptions expanded_calls.
Print Assumptions boundary_entry.
Print Assumptions blank_seed.
Print Assumptions artificial_halt.
End Entry405.

Module Entry482.
Definition tm := Eval compute in TM_from_str "1RB0LB_0RC0LD_1LD1RE_0LA0RB_0RD1RF_1LA---".
Definition hR : DH0 := (C,[0]).
Definition hL : DH0 := (A,[0]).
Definition h := [(hR,hL)].
Definition laws : list (list Sym*list Sym*nat) := [
  ([0],[1],0%nat);
  ([0;0;0],[1;0;0],0%nat);
  ([1;0;0],[0;0;0],1%nat);
  ([0;1;0;0],[1;1;0;0],0%nat);
  ([1;1;0;0],[0;0;1;0],0%nat);
  ([0;0;1;0],[1;0;1;0],0%nat);
  ([1;0;1;0],[1;0;1;0],2%nat);
  ([0;0;0;0;0;0],[1;0;0;0;0;0],0%nat);
  ([1;0;0;0;0;0],[0;0;0;1;0;0],0%nat);
  ([0;0;0;1;0;0],[1;0;0;1;0;0],0%nat);
  ([1;0;0;1;0;0],[0;0;0;0;0;0],1%nat);
  ([0;1;0;1;0;0],[1;1;0;1;0;0],0%nat);
  ([1;1;0;1;0;0],[0;0;1;1;0;0],0%nat);
  ([0;0;1;1;0;0],[1;0;1;1;0;0],0%nat);
  ([1;0;1;1;0;0],[0;0;0;1;0;0],0%nat);
  ([0;0;0;1;0;1;0],[1;0;0;1;0;1;0],0%nat);
  ([1;0;0;1;0;1;0],[0;0;0;1;0;1;0],2%nat);
  ([0;1;0;1;0;1;0],[1;1;0;1;0;1;0],0%nat);
  ([1;1;0;1;0;1;0],[0;0;1;1;0;1;0],0%nat);
  ([0;0;1;1;0;1;0],[1;0;1;1;0;1;0],0%nat);
  ([1;0;1;1;0;1;0],[0;0;0;1;0;1;0],0%nat)].
Lemma laws_checked : Forall (fun '(u,v,k) => segRLs tm h (h^^k) u v) laws.
Proof.
  repeat (constructor; [apply BoundedConfig.segRLs_c_spec with (T:=1000); vm_compute; reflexivity|]).
  constructor.
Qed.
Lemma twice : segRLs tm (h^^1) (h^^2) [1;0;1;0] [1;0;1;0].
Proof. apply BoundedConfig.segRLs_c_spec with (T:=1000); vm_compute; reflexivity. Qed.
Theorem expanded_calls n m :
  segRLs tm (h^^n) (h^^(n*2^m)) ([1;0;1;0]^^m) ([1;0;1;0]^^m).
Proof. apply exponential_calls, twice. Qed.
Lemma halt_packet l r : halts tm (l {{{(hR,R)}}} [1;1;1] *> r).
Proof. unfold hR; solve_halt. Qed.
Definition boundary r := (A,(0inf,1,0>>r)).
Lemma boundary_entry r : boundary r -[tm]->* (0inf <*< [1]) {{{(hR,R)}}} [1;0] *> r.
Proof. unfold boundary,hR; esx. Qed.
Lemma blank_seed : c0 -[tm]->* boundary ([1] *> 0inf).
Proof. unfold boundary; esx. Qed.
(* A detector control, not a boundary claimed reachable from blank. *)
Lemma artificial_halt : halts tm (boundary ([1;0;0;1;1] *> 0inf)).
Proof. unfold boundary; solve_halt. Qed.
Print Assumptions laws_checked.
Print Assumptions halt_packet.
Print Assumptions expanded_calls.
Print Assumptions boundary_entry.
Print Assumptions blank_seed.
Print Assumptions artificial_halt.
End Entry482.
End PacketCoverage.
