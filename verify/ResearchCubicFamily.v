(* Arithmetic identities for the existing CubicCap certificates.
   The certificate definitions and their proofs belong to BusyCoq's authors.
   These identities justify normalized WF17 events; they do not certify the
   native lookup tables, a checkpoint, or a blank-run classification.
   AI-assisted by Codex. *)
From BusyCoq Require Import CubicCap.
From Coq Require Import Arith Lia.

Module CubicFamily.
Ltac triple_lia := repeat match goal with
| |- (_,_) = (_,_) => f_equal
| |- Some _ = Some _ => f_equal
end; lia.
Definition bounce17 : nat*nat*nat -> nat*nat*nat.
Proof.
  let T := type of WF17 in
  match T with Cert_WF _ (cert1 _ _ ?bounce _ _ _) => exact bounce end.
Defined.
Definition calc17 : nat*nat*nat -> option (nat*nat*nat).
Proof.
  let T := type of WF17 in
  match T with Cert_WF _ (cert1 _ _ _ _ ?calc _) => exact calc end.
Defined.
Definition step17 x := calc17 (bounce17 x).

Lemma bounce_left q b t r : r < 3 ->
  bounce17 (3*q+r,b,q+t) = (r,b+2*q,t).
Proof.
  intro HR; unfold bounce17; cbn beta iota zeta.
  rewrite Nat.div_1_r.
  assert (HD : (3*q+r)/3=q) by (symmetry; apply (Nat.div_unique _ _ _ r); lia).
  rewrite HD, Nat.min_l by lia.
  triple_lia.
Qed.

Lemma bounce_right c b u :
  bounce17 (3*c+3+u,b,c) = (3+u,b+2*c,0).
Proof.
  unfold bounce17; cbn beta iota zeta; rewrite Nat.div_1_r.
  assert (HD : c <= (3*c+3+u)/3) by (apply Nat.div_le_lower_bound; lia).
  rewrite Nat.min_r by lia; triple_lia.
Qed.

Lemma left_zero q b t : 1 <= q -> b <= 1 -> 2 <= t ->
  step17 (3*q,b,q+t) = Some (4*q+2*b+1,0,t-1).
Proof.
  intros HQ HB HT; unfold step17.
  replace (3*q) with (3*q+0) by lia; rewrite bounce_left by lia.
  destruct q as [|q]; [lia|]. destruct b as [|b]; [|destruct b; [|lia]];
  destruct t as [|[|t]]; try lia;
  unfold calc17; cbn; repeat rewrite Nat.add_succ_r; cbn; triple_lia.
Qed.

Lemma left_one q b t : 1 <= q -> b <= 1 -> 2 <= t ->
  step17 (3*q+1,b,q+t) = Some (4*q+2*b+5,0,t-2).
Proof.
  intros HQ HB HT; unfold step17; rewrite bounce_left by lia.
  destruct t as [|[|t]]; try lia;
  unfold calc17; cbn; triple_lia.
Qed.

Definition twice17 x := match step17 x with None => None | Some y => step17 y end.
Lemma left_two q b t : 1 <= q -> b <= 1 -> 2 <= t ->
  twice17 (3*q+2,b,q+t) = Some (4*q+2*b+7,0,t-2).
Proof.
  intros HQ HB HT; unfold twice17, step17; rewrite bounce_left by lia.
  destruct t as [|[|t]]; try lia.
  unfold calc17 at 1; cbn.
  unfold bounce17; cbn.
  unfold calc17; cbn; triple_lia.
Qed.

Lemma right_event c b u :
  step17 (3*c+3+u,b,c) = Some (1+u,1,3+2*b+4*c).
Proof.
  unfold step17; rewrite bounce_right; unfold calc17; cbn.
  triple_lia.
Qed.

Lemma boundary_halt c b : twice17 (3*c+2,b,c) = None.
Proof.
  unfold twice17, step17, bounce17; cbn beta iota zeta.
  rewrite Nat.div_1_r.
  assert (HD : (3*c+2)/3=c) by (symmetry; apply (Nat.div_unique _ _ _ 2); lia).
  rewrite HD, Nat.min_id.
  replace (3*c+2-c*3) with 2 by lia; replace (c-c*1) with 0 by lia.
  unfold calc17; cbn.
  reflexivity.
Qed.

Print Assumptions bounce_left.
Print Assumptions bounce_right.
Print Assumptions left_zero.
Print Assumptions left_one.
Print Assumptions left_two.
Print Assumptions right_event.
Print Assumptions boundary_halt.
End CubicFamily.
