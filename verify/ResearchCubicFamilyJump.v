(* Abstract guards for the two native cubic-family accelerators.
   This file does not verify C++, lookup-table construction, or checkpoints.
   AI-assisted by Codex; extends the ResearchCubic26Jump proof pattern. *)
From Coq Require Import ZArith Lia.
Open Scope Z_scope.

Module CubicFamilyDoubling.
Fixpoint scale (i : nat) : Z :=
  match i with O => 1 | S j => 2 * scale j end.
Lemma scale_positive i : 1 <= scale i.
Proof. induction i; [cbn; lia|change (1 <= 2 * scale i); lia]. Qed.
Definition bounds i c d :=
  Z.of_nat i <= d <= 2 * Z.of_nat i /\
  -6 * scale i + 2 * Z.of_nat i + 6 <= c <= 8 * (scale i - 1).
Definition margin i x n := 6 * scale i <= x /\ 8 * scale i <= n-x.

Section Model.
Variables ell bl : Z.
Hypothesis ell_bounds : 2 <= ell <= 4.
Hypothesis bl_bounds : 0 <= bl <= 2.
Inductive regular : (Z*Z*Z) -> (Z*Z*Z) -> Prop :=
| reg_left a n b : 0 <= b <= 2 -> 1 <= a -> 16 <= n-2*a ->
    regular (a,n,b) (2*a+2*b+ell,n+2-a mod 2,bl)
| reg_right a n b : 0 <= b <= 2 -> 1 <= a -> 4 <= n-a -> 4 <= 2*a-n ->
    regular (a,n,b) (2*a-n+2*b-4,n+2,2).
Inductive regular_steps : nat -> (Z*Z*Z) -> (Z*Z*Z) -> Prop :=
| steps_zero p : regular_steps O p p
| steps_next k p q r : regular p q -> regular_steps k q r ->
    regular_steps (S k) p r.
Inductive shadow (n : Z) : nat -> Z -> Z -> Z -> Z -> Z -> Z -> Z -> Z -> Prop :=
| shadow_zero x c d b : shadow n O x c d b x c d b
| shadow_left k x c d b y e f z :
    0 <= x < n -> 2*x < n -> 0 <= b <= 2 ->
    shadow n k (2*x) (2*c+2*b+ell) (d+2-(x+c) mod 2) bl y e f z ->
    shadow n (S k) x c d b y e f z
| shadow_right k x c d b y e f z :
    0 <= x < n -> n <= 2*x -> 0 <= b <= 2 ->
    shadow n k (2*x-n) (2*c-d+2*b-4) (d+2) 2 y e f z ->
    shadow n (S k) x c d b y e f z.

Lemma left_bounds i x c d b : bounds i c d -> 0 <= b <= 2 ->
  bounds (S i) (2*c+2*b+ell) (d+2-(x+c) mod 2).
Proof.
  unfold bounds; rewrite Nat2Z.inj_succ; cbn [scale].
  pose proof (Z.mod_pos_bound (x+c) 2 ltac:(lia)); intros; lia.
Qed.
Lemma right_bounds i c d b : bounds i c d -> 0 <= b <= 2 ->
  bounds (S i) (2*c-d+2*b-4) (d+2).
Proof. unfold bounds; rewrite Nat2Z.inj_succ; cbn [scale]; intros; lia. Qed.
Lemma left_margin i x n : 0 <= x < n ->
  margin (S i) (2*x) n -> margin i x n.
Proof. unfold margin; cbn [scale]; intros; lia. Qed.
Lemma right_margin i x n : 0 <= x < n ->
  margin (S i) (2*x-n) n -> margin i x n.
Proof. unfold margin; cbn [scale]; intros; lia. Qed.

Lemma left_regular i x c d n b :
  0 <= b <= 2 -> bounds i c d -> margin i x n -> margin (S i) (2*x) n ->
  regular (x+c,n+d,b) (2*x+(2*c+2*b+ell),n+(d+2-(x+c) mod 2),bl).
Proof.
  unfold bounds,margin; cbn [scale]; intros.
  replace (2*x+(2*c+2*b+ell)) with (2*(x+c)+2*b+ell) by ring.
  replace (n+(d+2-(x+c) mod 2)) with ((n+d)+2-(x+c) mod 2) by ring.
  apply reg_left; lia.
Qed.
Lemma right_regular i x c d n b :
  0 <= b <= 2 -> bounds i c d -> margin i x n -> margin (S i) (2*x-n) n ->
  regular (x+c,n+d,b) (2*x-n+(2*c-d+2*b-4),n+(d+2),2).
Proof.
  unfold bounds,margin; cbn [scale]; intros.
  replace (2*x-n+(2*c-d+2*b-4)) with (2*(x+c)-(n+d)+2*b-4) by ring.
  replace (n+(d+2)) with ((n+d)+2) by ring.
  apply reg_right; lia.
Qed.

Theorem guarded_shadow n k x c d b y e f z :
  shadow n k x c d b y e f z -> forall i,
  bounds i c d -> margin (i+k)%nat y n ->
  margin i x n /\ regular_steps k (x+c,n+d,b) (y+e,n+f,z) /\ bounds (i+k)%nat e f.
Proof.
  intros H; induction H; intros i HB HM.
  - rewrite Nat.add_0_r in *; split; [exact HM|]. split; [constructor|exact HB].
  - assert (HB' := left_bounds i x c d b HB H1).
    replace (i+S k)%nat with (S i+k)%nat in HM by lia.
    destruct (IHshadow (S i) HB' HM) as [HM' [HS HE]].
    assert (HM0 : margin i x n) by (eapply left_margin; eauto).
    split; [exact HM0|]. split.
    + eapply steps_next; [eapply left_regular; eauto|exact HS].
    + replace (i+S k)%nat with (S i+k)%nat by lia; exact HE.
  - assert (HB' := right_bounds i c d b HB H1).
    replace (i+S k)%nat with (S i+k)%nat in HM by lia.
    destruct (IHshadow (S i) HB' HM) as [HM' [HS HE]].
    assert (HM0 : margin i x n) by (eapply right_margin; eauto).
    split; [exact HM0|]. split.
    + eapply steps_next; [eapply right_regular; eauto|exact HS].
    + replace (i+S k)%nat with (S i+k)%nat by lia; exact HE.
Qed.
Corollary guarded_jump n k a b r c d z :
  shadow n k a 0 0 b r c d z ->
  6 * scale k <= r -> 8 * scale k <= n-r ->
  regular_steps k (a,n,b) (r+c,n+d,z).
Proof.
  intros H HL HR.
  assert (HB : bounds O 0 0) by (unfold bounds; cbn; lia).
  assert (HM : margin (O+k)%nat r n) by (unfold margin; cbn; auto).
  destruct (guarded_shadow n k a 0 0 b r c d z H O HB HM) as [_ [HS _]].
  now rewrite !Z.add_0_r in HS.
Qed.
End Model.
Print Assumptions guarded_shadow.
Print Assumptions guarded_jump.
End CubicFamilyDoubling.

From Coq Require Import QArith Psatz.
Open Scope Q_scope.
Module CubicFamilyAsymmetric.
Ltac qlra := unfold Qdiv in *; change (/3) with (1#3) in *; lra.
Fixpoint scale (i : nat) : Q :=
  match i with O => 1 | S j => 4 * scale j end.
Fixpoint ticks (i : nat) : Q :=
  match i with O => 0 | S j => ticks j + 1 end.
Lemma scale_positive i : 1 <= scale i.
Proof. induction i; [cbn; qlra|change (1 <= 4 * scale i); qlra]. Qed.
Lemma ticks_nonnegative i : 0 <= ticks i.
Proof. induction i; [cbn; qlra|change (0 <= ticks i + 1); qlra]. Qed.
Definition bounds i c d :=
  0 <= d <= 3 * ticks i /\
  -3 * scale i + 3 * ticks i + 3 <= c <= 3 * (scale i - 1).
Definition margin i x n := 3 * scale i <= x /\ scale i <= n-x.

(* alpha is delta[a mod 3]+6*b, hence between 3 and 19.
   beta is 6*b-2, hence between -2 and 4. A left event increments
   N by 0, 2, or 3. Bounds suffice for this abstract argument. *)
Inductive regular : (Q*Q) -> (Q*Q) -> Prop :=
| reg_left a n aa nn alpha inc :
    3 <= a -> 12 <= 3*n-4*a -> 3 <= alpha <= 19 -> 0 <= inc <= 3 ->
    aa == (4*a+alpha)/3 -> nn == n+inc -> regular (a,n) (aa,nn)
| reg_right a n aa nn beta :
    3 <= 4*a-3*n -> -2 <= beta <= 4 ->
    aa == 4*a-3*n+beta -> nn == n+3 -> regular (a,n) (aa,nn).
Inductive regular_steps : nat -> (Q*Q) -> (Q*Q) -> Prop :=
| steps_zero p : regular_steps O p p
| steps_next k p q r : regular p q -> regular_steps k q r ->
    regular_steps (S k) p r.
Inductive shadow (n : Q) : nat -> Q -> Q -> Q -> Q -> Q -> Q -> Prop :=
| shadow_zero x c d : shadow n O x c d x c d
| shadow_left k x c d y e f alpha inc :
    0 <= x < n -> 4*x < 3*n -> 3 <= alpha <= 19 -> 0 <= inc <= 3 ->
    shadow n k (4*x/3) ((4*c+alpha)/3) (d+inc) y e f ->
    shadow n (S k) x c d y e f
| shadow_right k x c d y e f beta :
    0 <= x < n -> 3*n <= 4*x -> -2 <= beta <= 4 ->
    shadow n k (4*x-3*n) (4*c-3*d+beta) (d+3) y e f ->
    shadow n (S k) x c d y e f.

Lemma left_bounds i c d alpha inc : bounds i c d ->
  3 <= alpha <= 19 -> 0 <= inc <= 3 ->
  bounds (S i) ((4*c+alpha)/3) (d+inc).
Proof.
  unfold bounds; cbn [scale ticks]; pose proof (scale_positive i).
  pose proof (ticks_nonnegative i); intros; qlra.
Qed.
Lemma right_bounds i c d beta : bounds i c d -> -2 <= beta <= 4 ->
  bounds (S i) (4*c-3*d+beta) (d+3).
Proof. unfold bounds; cbn [scale ticks]; intros; qlra. Qed.
Lemma left_margin i x n : 0 <= x < n ->
  margin (S i) (4*x/3) n -> margin i x n.
Proof. unfold margin; cbn [scale]; pose proof (scale_positive i); intros; qlra. Qed.
Lemma right_margin i x n : 0 <= x < n ->
  margin (S i) (4*x-3*n) n -> margin i x n.
Proof. unfold margin; cbn [scale]; pose proof (scale_positive i); intros; qlra. Qed.

Lemma left_regular i x c d n alpha inc :
  bounds i c d -> margin i x n -> margin (S i) (4*x/3) n ->
  3 <= alpha <= 19 -> 0 <= inc <= 3 ->
  regular (x+c,n+d) (4*x/3+(4*c+alpha)/3,n+(d+inc)).
Proof.
  unfold bounds,margin; cbn [scale]; pose proof (ticks_nonnegative i); intros.
  eapply reg_left with (alpha:=alpha) (inc:=inc); qlra.
Qed.
Lemma right_regular i x c d n beta :
  bounds i c d -> margin (S i) (4*x-3*n) n -> -2 <= beta <= 4 ->
  regular (x+c,n+d) (4*x-3*n+(4*c-3*d+beta),n+(d+3)).
Proof.
  unfold bounds,margin; cbn [scale]; pose proof (ticks_nonnegative i); intros.
  eapply reg_right with (beta:=beta); qlra.
Qed.

Theorem guarded_shadow n k x c d y e f :
  shadow n k x c d y e f -> forall i,
  bounds i c d -> margin (i+k)%nat y n ->
  margin i x n /\ regular_steps k (x+c,n+d) (y+e,n+f) /\ bounds (i+k)%nat e f.
Proof.
  intros H; induction H; intros i HB HM.
  - rewrite Nat.add_0_r in *; split; [exact HM|]. split; [constructor|exact HB].
  - assert (HB' := left_bounds i c d alpha inc HB H1 H2).
    replace (i+S k)%nat with (S i+k)%nat in HM by lia.
    destruct (IHshadow (S i) HB' HM) as [HM' [HS HE]].
    assert (HM0 : margin i x n) by (eapply left_margin; eauto).
    split; [exact HM0|]. split.
    + eapply steps_next; [eapply left_regular; eauto|exact HS].
    + replace (i+S k)%nat with (S i+k)%nat by lia; exact HE.
  - assert (HB' := right_bounds i c d beta HB H1).
    replace (i+S k)%nat with (S i+k)%nat in HM by lia.
    destruct (IHshadow (S i) HB' HM) as [HM' [HS HE]].
    assert (HM0 : margin i x n) by (eapply right_margin; eauto).
    split; [exact HM0|]. split.
    + eapply steps_next; [eapply right_regular; eauto|exact HS].
    + replace (i+S k)%nat with (S i+k)%nat by lia; exact HE.
Qed.

(* The +0 forms deliberately avoid identifying Qeq with Leibniz equality. *)
Corollary guarded_jump n k a r c d :
  shadow n k a 0 0 r c d ->
  3 * scale k <= r -> scale k <= n-r ->
  regular_steps k (a+0,n+0) (r+c,n+d).
Proof.
  intros H HL HR.
  assert (HB : bounds O 0 0) by (unfold bounds; cbn; lra).
  assert (HM : margin (O+k)%nat r n) by (unfold margin; cbn; auto).
  destruct (guarded_shadow n k a 0 0 r c d H O HB HM) as [_ [HS _]]. exact HS.
Qed.
Print Assumptions guarded_shadow.
Print Assumptions guarded_jump.
End CubicFamilyAsymmetric.
