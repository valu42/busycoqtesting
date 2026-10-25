(* Integer-arithmetic justification of the guarded doubling accelerator.
   This proves an abstract composition theorem, not the C++ implementation,
   its lookup-table construction, or the provenance of a saved checkpoint.
   See research/holdouts-623/CUBIC26.md. AI-assisted by Codex. *)
From Coq Require Import ZArith Lia.
Open Scope Z_scope.

Module Cubic26Jump.
Fixpoint scale (i : nat) : Z :=
  match i with O => 1 | S j => 2 * scale j end.
Lemma scale_positive i : 1 <= scale i.
Proof. induction i; [cbn; lia|change (1 <= 2 * scale i); lia]. Qed.

Definition bounds i c d :=
  3 * Z.of_nat i <= d <= 4 * Z.of_nat i /\
  -3 * scale i + 4 * Z.of_nat i + 3 <= c <= 4 * (scale i - 1).
Definition margin i x n := 3 * scale i <= x /\ 4 * scale i <= n-x.

(* These are the two regular branches of the published recurrence in
   coordinates (a,N=a+b), with slightly stronger sufficient guards. *)
Inductive regular : (Z*Z) -> (Z*Z) -> Prop :=
| reg_left a n : 1 <= a -> 4 <= n-2*a ->
    regular (a,n) (2*a+4-a mod 2,n+3)
| reg_right a n : 1 <= a -> 4 <= n-a -> n <= 2*a ->
    regular (a,n) (2*a-n+1,n+4).

Inductive regular_steps : nat -> (Z*Z) -> (Z*Z) -> Prop :=
| steps_zero p : regular_steps O p p
| steps_next k p q r : regular p q -> regular_steps k q r ->
    regular_steps (S k) p r.

(* The ideal residue doubles modulo the fixed original n. Its correction
   tracks changes to both the real first counter and the real sum. *)
Inductive shadow (n : Z) : nat -> Z -> Z -> Z -> Z -> Z -> Z -> Prop :=
| shadow_zero x c d : shadow n O x c d x c d
| shadow_left k x c d y e f :
    0 <= x < n -> 2*x < n ->
    shadow n k (2*x) (2*c+4-(x+c) mod 2) (d+3) y e f ->
    shadow n (S k) x c d y e f
| shadow_right k x c d y e f :
    0 <= x < n -> n <= 2*x ->
    shadow n k (2*x-n) (2*c-d+1) (d+4) y e f ->
    shadow n (S k) x c d y e f.

Lemma shadow_remainder n k x c d y e f :
  shadow n k x c d y e f -> 0 <= x < n ->
  y = (scale k * x) mod n.
Proof.
  intros H; induction H; intros HX.
  - change (x = (1*x) mod n); rewrite Z.mul_1_l, Z.mod_small; lia.
  - rewrite IHshadow by lia.
    change ((scale k * (2*x)) mod n = (2 * scale k * x) mod n).
    f_equal; ring.
  - rewrite IHshadow by lia.
    change ((scale k * (2*x-n)) mod n = (2 * scale k * x) mod n).
    replace (scale k * (2*x-n)) with (2 * scale k * x + (-scale k)*n) by ring.
    apply Z.mod_add; lia.
Qed.

Lemma small_mod x p q : 0 <= p < 2 -> x = 2*q+p -> x mod 2 = p.
Proof.
  intros; pose proof (Z.mod_pos_bound x 2 ltac:(lia)).
  pose proof (Z.div_mod x 2 ltac:(lia)); lia.
Qed.

(* Four parity states suffice for every precomputed branch word. *)
Lemma parity_rules a n :
  (2*a+4-a mod 2) mod 2 = a mod 2 /\
  (n+3) mod 2 = 1-n mod 2 /\
  (2*a-n+1) mod 2 = 1-n mod 2 /\
  (n+4) mod 2 = n mod 2.
Proof.
  pose proof (Z.mod_pos_bound a 2 ltac:(lia)).
  pose proof (Z.mod_pos_bound n 2 ltac:(lia)).
  pose proof (Z.div_mod n 2 ltac:(lia)).
  repeat split.
  - eapply (small_mod _ _ (a+2-a mod 2)); lia.
  - eapply (small_mod _ _ (n/2+1+n mod 2)); lia.
  - eapply (small_mod _ _ (a-n/2)); lia.
  - eapply (small_mod _ _ (n/2+2)); lia.
Qed.

Lemma left_bounds i x c d : bounds i c d ->
  bounds (S i) (2*c+4-(x+c) mod 2) (d+3).
Proof.
  unfold bounds; rewrite Nat2Z.inj_succ; cbn [scale].
  pose proof (Z.mod_pos_bound (x+c) 2 ltac:(lia)).
  pose proof (scale_positive i). intros; lia.
Qed.
Lemma right_bounds i c d : bounds i c d ->
  bounds (S i) (2*c-d+1) (d+4).
Proof.
  unfold bounds; rewrite Nat2Z.inj_succ; cbn [scale].
  pose proof (scale_positive i). intros; lia.
Qed.

Lemma left_margin i x n : 0 <= x < n ->
  margin (S i) (2*x) n -> margin i x n.
Proof. unfold margin; cbn [scale]; intros; lia. Qed.
Lemma right_margin i x n : 0 <= x < n ->
  margin (S i) (2*x-n) n -> margin i x n.
Proof. unfold margin; cbn [scale]; intros; lia. Qed.

Lemma left_regular i x c d n :
  bounds i c d -> margin i x n -> margin (S i) (2*x) n ->
  regular (x+c,n+d) (2*x+(2*c+4-(x+c) mod 2),n+(d+3)).
Proof.
  unfold bounds,margin; cbn [scale]; intros.
  replace (2*x+(2*c+4-(x+c) mod 2)) with (2*(x+c)+4-(x+c) mod 2) by ring.
  replace (n+(d+3)) with ((n+d)+3) by ring.
  apply reg_left; lia.
Qed.
Lemma right_regular i x c d n :
  bounds i c d -> margin i x n -> margin (S i) (2*x-n) n ->
  regular (x+c,n+d) (2*x-n+(2*c-d+1),n+(d+4)).
Proof.
  unfold bounds,margin; cbn [scale]; intros.
  replace (2*x-n+(2*c-d+1)) with (2*(x+c)-(n+d)+1) by ring.
  replace (n+(d+4)) with ((n+d)+4) by ring.
  apply reg_right; lia.
Qed.

Theorem guarded_shadow n k x c d y e f :
  shadow n k x c d y e f -> forall i,
  bounds i c d -> margin (i+k)%nat y n ->
  margin i x n /\
  regular_steps k (x+c,n+d) (y+e,n+f) /\ bounds (i+k)%nat e f.
Proof.
  intros H; induction H; intros i HB HM.
  - rewrite Nat.add_0_r in *; split; [exact HM|].
    split; [constructor|exact HB].
  - assert (HB' := left_bounds i x c d HB).
    replace (i+S k)%nat with (S i+k)%nat in HM by lia.
    destruct (IHshadow (S i) HB' HM) as [HM' [HS HE]].
    assert (HM0 : margin i x n) by (eapply left_margin; eauto).
    split; [exact HM0|]. split.
    + eapply steps_next; [eapply left_regular; eauto|exact HS].
    + replace (i+S k)%nat with (S i+k)%nat by lia; exact HE.
  - assert (HB' := right_bounds i c d HB).
    replace (i+S k)%nat with (S i+k)%nat in HM by lia.
    destruct (IHshadow (S i) HB' HM) as [HM' [HS HE]].
    assert (HM0 : margin i x n) by (eapply right_margin; eauto).
    split; [exact HM0|]. split.
    + eapply steps_next; [eapply right_regular; eauto|exact HS].
    + replace (i+S k)%nat with (S i+k)%nat by lia; exact HE.
Qed.

Corollary guarded_jump n k a r c d :
  shadow n k a 0 0 r c d ->
  3 * scale k <= r -> 4 * scale k <= n-r ->
  regular_steps k (a,n) (r+c,n+d).
Proof.
  intros H HL HR.
  assert (HB : bounds O 0 0) by (unfold bounds; cbn; lia).
  assert (HM : margin (O+k)%nat r n) by (unfold margin; cbn; auto).
  destruct (guarded_shadow n k a 0 0 r c d H O HB HM) as [_ [HS _]].
  now rewrite !Z.add_0_r in HS.
Qed.

Print Assumptions guarded_shadow.
Print Assumptions guarded_jump.
Print Assumptions shadow_remainder.
Print Assumptions parity_rules.
End Cubic26Jump.
