(** The reserve at a protected cut suffices for a positive, physical sweep.
    Potentials and charges are signed integers. Lengths use the actual word. *)
From Coq Require Import List ZArith Bool Lia.
From BusyCoq Require Import Line36Machine Line36Word Line36Tiles Line36Cover Line36TileShield Line36Right
                           Line36Physical Line36Seed.
Import ListNotations.
Import L36Tiles.
Local Open Scope list_scope.

Lemma tail_charge_gap36 w pos prev :
  L36Seed.tail_charge w pos prev = gap_cost w (Bool.eqb prev pos).
Proof.
  revert pos prev. induction w as [|b w IH]; intros [] [];
    try reflexivity; destruct b; cbn [L36Seed.tail_charge gap_cost];
    rewrite IH; reflexivity.
Qed.

Lemma tail_budget_debt36 p u :
  fst (mark36 u 0) <= S (L36Seed.budget p u).
Proof.
  unfold L36Seed.budget. rewrite tail_charge_gap36, <- aligned_gap_cost.
  destruct (Bool.eqb _ _) eqn:E; cbn [app].
  all: pose proof (matching_budget u) as H;
    destruct (mark36 u 0) as [d bits]; cbn [fst] in *.
  - pose proof (monomers_cons_distance u true); lia.
  - lia.
Qed.

(** This statement is about the real tape machine and any exterior word,
    without presupposing that its next sweep succeeds. *)
Theorem reserve_sweep36 ph data u :
  ph < 6 -> covered36 ph data ->
  let p := phase_prefix ph ++ data in
  (52 <= Z.of_nat (length p) - 4 * Z.of_nat (L36Seed.budget p u))%Z ->
  exists v, step36 (p++u) = Some v /\
            progress line36 (checkpoint (p++u)) (checkpoint v).
Proof.
  intros Hph Hcov p Hres.
  pose proof (tail_budget_debt36 p u) as HD.
  pose proof (covered_data36 ph data Hph Hcov) as [D0 Density].
  assert (Len : length p = 26 + length data).
  { unfold p. rewrite length_app, (phase_prefix_length36 ph Hph). reflexivity. }
  rewrite Len, Nat2Z.inj_add in Hres.
  assert (HN : (Z.of_nat (fst (mark36 u 0)) <= bal36 data)%Z) by lia.
  pose proof (mark36_shield data _ HN) as Ds. rewrite D0 in Ds.
  assert (Hd : (fst (mark36 (p++u) 0) < 6)%nat).
  { unfold p. rewrite <- app_assoc, mark36_app.
    assert (Du : fst (mark36 (data++u) 0) = 0).
    { rewrite mark36_app. destruct (mark36 u 0) as [d b]. cbn [fst] in Ds.
      destruct (mark36 data d) as [e bits]. exact Ds. }
    destruct (mark36 (data++u) 0) as [d bs]. cbn [fst] in Du. subst d.
    pose proof (prefix_facts36 ph Hph) as P.
    destruct (mark36 (phase_prefix ph) 0) as [e bits]. apply P. }
  assert (Es : exists v, step36 (p++u) = Some v).
  { unfold step36. destruct (mark36 (p++u) 0) as [d bits]. cbn [fst] in Hd.
    apply Nat.ltb_lt in Hd. rewrite Hd; eauto. }
  destruct Es as [v E]. exists v. split; [exact E|now apply step36_physical].
Qed.

Local Open Scope Z_scope.

(** Combining the three one-step inequalities with the terminal alternation
    gives a conserved lower bound, without dividing integer potentials. *)
Record ledger36 := Ledger36 {
  cut36 : Z; switches36 : Z; left_potential36 : Z;
  cap_potential36 : Z; terminal36 : Z
}.

Definition credit36 s :=
  6 * (cut36 s - 4 * switches36 s) - left_potential36 s
  + 8 * cap_potential36 s + 12 * terminal36 s.

Definition in_range36 s :=
  -110 <= left_potential36 s <= 0 /\ -21 <= cap_potential36 s <= 0 /\
  0 <= terminal36 s <= 1.

Lemma initial_credit36 s :
  in_range36 s -> cut36 s = 530 -> switches36 s = 7 -> 2844 <= credit36 s.
Proof. unfold in_range36, credit36; lia. Qed.

Lemma credit36_step s t C c :
  switches36 t <= switches36 s + C + (1-terminal36 s) - c ->
  left_potential36 t - left_potential36 s <= 6*(cut36 t-cut36 s)-24*C-4 ->
  cap_potential36 s <= 3*c-1+cap_potential36 t ->
  terminal36 t = 1-terminal36 s ->
  credit36 s <= credit36 t.
Proof. unfold credit36; lia. Qed.

Lemma credit36_safe s :
  in_range36 s -> 2844 <= credit36 s -> 454 <= cut36 s - 4*switches36 s.
Proof. unfold in_range36, credit36; lia. Qed.
