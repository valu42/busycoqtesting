From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Left Line36LeftStep Line36LeftPotential.
Import ListNotations L36Left L36LeftStep L36LeftPotential.
Module L36LeftCheck.

Definition test_case (s : state) ctx (d : nat) : bool :=
  match evaluate s ctx d with
  | Some e => edge_ok value s e
  | None => false
  end.

Definition check_one s :=
  forallb (fun h => let ctx := prepare s h in
                    forallb (test_case s ctx) (seq 0 29)) (seq 0 16).

Lemma check_one_sound s hist d : check_one s = true ->
  (hist < 16)%nat -> (d < 29)%nat ->
  exists e, step s hist d = Some e /\
    (value (target e) - value s <= weight e)%Z.
Proof.
 apply checked_step.
Qed.

Definition check_partial_range (ph k : nat) (b v : bool) (start count : nat) :=
  forallb (fun n => forallb (fun h => check_one (State ph k b v n h)) (seq 0 8))
          (seq start count).

Lemma check_partial_range_sound ph k b v start count n h :
  check_partial_range ph k b v start count = true ->
  (start <= n < start+count)%nat -> (h < 8)%nat ->
  check_one (State ph k b v n h) = true.
Proof.
  intros H Hn Hh. unfold check_partial_range in H.
  apply forallb_forall with (x := n) in H; [|apply in_seq; lia].
  apply forallb_forall with (x := h) in H; auto. apply in_seq; lia.
Qed.
End L36LeftCheck.

Module L36LeftGroups.
Import L36LeftCheck.
Definition check_group ph k b v :=
  check_partial_range ph k b v 0 (length (piece ph k v)).
Definition check_kind ph k :=
  forallb (fun b => forallb (fun v => check_group ph k b v) [false;true]) [false;true].
Definition check_phase ph := forallb (check_kind ph) (seq 0 6).
Definition well_formed s : Prop :=
  (phase s < 6 /\ kind s < 6 /\
   partial_len s < length (piece (phase s) (kind s) (partial_choice s)) /\ halo s < 8)%nat.

Lemma checked_phase s :
  check_phase (phase s) = true -> well_formed s -> check_one s = true.
Proof.
  destruct s as [ph k b v len h]. cbn [phase kind last_choice partial_choice partial_len halo].
  intros H W. unfold well_formed in W; cbn in W.
  unfold check_phase in H.
  apply forallb_forall with (x:=k) in H; [|apply in_seq; lia].
  unfold check_kind in H.
  apply forallb_forall with (x:=b) in H; [|destruct b; simpl; auto].
  apply forallb_forall with (x:=v) in H; [|destruct v; simpl; auto].
  eapply check_partial_range_sound; [exact H|lia|lia].
Qed.
End L36LeftGroups.
