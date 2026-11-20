From BusyCoq Require Import Individual62 Line429Engine.
From Coq Require Import List Lia.
Import ListNotations.
Open Scope sym_scope.
Module SpliceFamily429.
Fixpoint pairs (m:nat) (l:side) := match m with O => l | S n => S1 >> S1 >> pairs n l end.
Fixpoint alt (m:nat) (r:side) := match m with O => r | S n => S1 >> S0 >> alt n r end.
Lemma pairs_one m l : pairs m (S1 >> l) = S1 >> pairs m l.
Proof. induction m; cbn; congruence. Qed.
Lemma alt_pair m r : alt m (S1 >> S0 >> r) = S1 >> S0 >> alt m r.
Proof. induction m; cbn; congruence. Qed.
Ltac walk := eapply multistep_S; [prove_step|simpl_tape].
Lemma down m l r :
  (S0 >> pairs m l) {{C}}> (S0 >> S0 >> r) -[tm]->> (8*m)%nat /
  (S0 >> l) {{C}}> (S0 >> S0 >> alt m r).
Proof.
  revert r. induction m as [|m IH]; intros r.
  - apply multistep_0.
  - replace (8*S m)%nat with (8+8*m)%nat by lia. cbn [pairs alt].
    do 8 walk. rewrite <- alt_pair. apply IH.
Qed.
Lemma up m l r :
  l {{B}}> (alt m r) -[tm]->> (2*m)%nat / (pairs m l) {{B}}> r.
Proof.
  revert l. induction m as [|m IH]; intros l.
  - apply multistep_0.
  - replace (2*S m)%nat with (2+2*m)%nat by lia. cbn [pairs alt].
    do 2 walk. rewrite <- !pairs_one. apply IH.
Qed.
Definition entry m l r := ([0;0] *> pairs m ([0;0] *> l)) {{A}}> (S1 >> r).
Definition exit_left m l := pairs m ([1;0;0;1;0] *> l).
Lemma bridge m l r : entry m l r -[tm]->> (10*m+11)%nat / (exit_left m l) {{B}}> r.
Proof.
  unfold entry,exit_left. replace (10*m+11)%nat with (1+(8*m+(10+2*m)))%nat by lia.
  walk. eapply multistep_trans; [apply down|]. do 10 walk. apply up.
Qed.
Theorem block m l r : entry m l (S0 >> S1 >> S0 >> S1 >> r) -[tm]->> (10*m+14)%nat /
   entry (S m) (S1 >> S0 >> l) r.
Proof.
  replace (10*m+14)%nat with ((10*m+11)+3)%nat by lia.
  eapply multistep_trans; [apply bridge|]. do 3 walk.
  unfold exit_left,entry. cbn [pairs Str_app]. rewrite pairs_one. apply multistep_0.
Qed.
Theorem terminal m l r : halts_in tm (entry m l (S0 >> S0 >> S1 >> r)) (10*m+13)%nat.
Proof.
  eexists. split.
  - replace (10*m+13)%nat with ((10*m+11)+2)%nat by lia.
    eapply multistep_trans; [apply bridge|]. do 2 walk. apply multistep_0.
  - reflexivity.
Qed.
Fixpoint remaining (k:nat) (r:side) := match k with
  | O => S0 >> S0 >> S1 >> r | S j => S0 >> S1 >> S0 >> S1 >> remaining j r end.
Fixpoint cost (m k:nat) : nat := match k with
  | O => 10*m+13 | S j => (10*m+14) + cost (S m) j end.
Theorem family k m l r : halts_in tm (entry m l (remaining k r)) (cost m k).
Proof.
  revert m l. induction k as [|k IH]; intros m l.
  - apply terminal.
  - destruct (IH (S m) (S1 >> S0 >> l)) as [d [R H]]. exists d; split; [|exact H].
    cbn [cost remaining]. eapply multistep_trans; [apply block|exact R].
Qed.

Lemma cost_closed k m : cost m k = (5*k*k + 10*m*k + 19*k + 10*m + 13)%nat.
Proof. revert m. induction k as [|k IH]; intro m; cbn [cost]; [lia|rewrite IH; nia]. Qed.

Definition cstart k l r :=
  ([0;1;0;1;0;0;1;0] *> l) {{C}}>
  ([0;0;1;0;1;1;0;1;0;1;0;1] *> remaining k r).
Definition start_left l := [1;1;1;0;0;1;1;1;1;1;0;0;1] *> l.
Lemma start_reaches k l r : cstart k l r -[tm]->> 69 /
   entry 1 (start_left l) (remaining k r).
Proof. unfold cstart,entry,start_left. do 69 walk. apply multistep_0. Qed.
Theorem cstart_halts k l r :
  halts_in tm (cstart k l r) (5*(k+2)*(k+2)+9*(k+2)+54)%nat.
Proof.
  destruct (family k 1 (start_left l) r) as [d [R H]].
  exists d; split; [|exact H].
  replace (5*(k+2)*(k+2)+9*(k+2)+54)%nat with (69+cost 1 k)%nat by (rewrite cost_closed; nia).
  eapply multistep_trans; [apply start_reaches|exact R].
Qed.
(** The missing case n=1 of C:00101(1010)^n01. *)
Theorem cstart_one l r : halts_in tm
  (([0;1;0;1;0;0;1;0] *> l) {{C}}> ([0;0;1;0;1;1;0;1;0;0;1] *> r)) 68.
Proof. eexists; split; [do 68 walk;apply multistep_0|reflexivity]. Qed.
End SpliceFamily429.
Print Assumptions SpliceFamily429.family.
Print Assumptions SpliceFamily429.cstart_halts.
