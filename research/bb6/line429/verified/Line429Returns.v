From BusyCoq Require Import Individual62 Line429Engine.
From Coq Require Import List.
Import ListNotations Bell429.
Open Scope list_scope.
Open Scope sym_scope.

Module Returns429.
Definition finite (s : side) := exists w : list Sym, s = w *> 0inf.
Lemma finite_rest b s : finite (b >> s) -> finite s.
Proof.
  intros [[|c w] H].
  - exists (@nil Sym). change (b >> s = 0inf) in H.
    exact (f_equal (@Streams.tl _) H).
  - exists w. exact (f_equal (@Streams.tl _) H).
Qed.

Inductive destination : Q*tape -> Prop :=
| at_ML l r : destination (CfgL l r)
| at_MJ l r : destination (CfgJ l r)
| at_AR l r : destination (l {{A}}> r).
Definition escape c := exists d, c -[src_tm]->+ d /\ destination d.
Lemma hit c d : c -[src_tm]-> d -> destination d -> escape c.
Proof. intros S H. exists d; split; [apply progress_base; exact S|exact H]. Qed.
Lemma earlier c d : c -[src_tm]-> d -> escape d -> escape c.
Proof. intros S [z [H P]]; exists z; split; [exact (progress_step S H)|exact P]. Qed.
Ltac more := eapply earlier; [prove_step|simpl_tape].
Ltac arrive := eapply hit; [prove_step|simpl_tape].
Ltac done_AR := match goal with |- destination (A,(?l,?b,?r)) => exact (at_AR l (b >> r)) end.

(* B moving left with two zeros immediately to its right is always safe. *)
Lemma BL00 l r : escape (l <{{B}} (0 >> 0 >> r)).
Proof.
  destruct l as [[|] l].
  - arrive. apply at_MJ.
  - more. more. arrive. done_AR.
Qed.

Ltac use_BL00 := match goal with |- escape (B,(?l,?b, S0 >> S0 >> ?r)) => exact (BL00 (b >> l) r) end.

(* While E moves left, each erased one pushes another zero to the right.
   The first zero under E produces a left-moving B with a double-zero suffix. *)
Lemma EL0 l r : finite l -> escape (l <{{E}} (0 >> r)).
Proof.
  intros [w ->]; revert r. induction w as [|[|] w IH]; intro r; cbn.
  - more. use_BL00.
  - more. use_BL00.
  - more. apply IH.
Qed.

(* This is the only dangerous front in a fallback entering D from the right. *)
Definition badD (l : side) :=
  exists x, l = 0 >> 1 >> x.
Lemma DL_safe l r : finite l -> ~badD l -> escape (l <{{D}} r).
Proof.
  destruct l as [[|] l]; intro H; apply finite_rest in H; intro safe.
  - destruct l as [[|] l].
    + more. arrive. done_AR.
    + exfalso; apply safe; exists l; reflexivity.
  - more. apply EL0,H.
Qed.
Lemma DL_hit x r : exists c, (0 >> 1 >> x) <{{D}} r -[src_tm]->> 1 / c /\ halted src_tm c.
Proof. eexists; split; [eapply multistep_S; [prove_step|apply multistep_0]|reflexivity]. Qed.

Definition badML l := exists x, l = 0 >> 0 >> 0 >> 1 >> x.
Definition badMJ l := exists x, l = 0 >> 0 >> 1 >> x.

Theorem ML_escape l r : finite l -> ~badML l -> escape (CfgL l r).
Proof.
  unfold CfgL. destruct l as [[|] l]; intro H; apply finite_rest in H; intro safe.
  - destruct l as [[|] l]; apply finite_rest in H.
    + more. more. apply DL_safe; [exact H|].
      intros [x ->]; apply safe; now exists x.
    + more. arrive. apply at_ML.
  - more. more. more. use_BL00.
Qed.

Theorem MJ_escape l r : finite l -> ~badMJ l -> escape (CfgJ l r).
Proof.
  unfold CfgJ. destruct l as [[|] l]; intro H; apply finite_rest in H; intro safe.
  - more. apply DL_safe; [exact H|].
    intros [x ->]; apply safe; now exists x.
  - arrive. apply at_ML.
Qed.
Theorem ML_halts x r : exists c,
   CfgL (0 >> 0 >> 0 >> 1 >> x) r -[src_tm]->> 3 / c /\ halted src_tm c.
Proof. unfold CfgL. eexists; split; [do 3 (eapply multistep_S; [prove_step|simpl_tape]); apply multistep_0|reflexivity]. Qed.
Theorem MJ_halts x r : exists c,
   CfgJ (0 >> 0 >> 1 >> x) r -[src_tm]->> 2 / c /\ halted src_tm c.
Proof. unfold CfgJ. eexists; split; [do 2 (eapply multistep_S; [prove_step|simpl_tape]); apply multistep_0|reflexivity]. Qed.
End Returns429.
Print Assumptions Returns429.ML_escape.
Print Assumptions Returns429.MJ_escape.
