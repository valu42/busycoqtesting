(** Transport the checked properties of a finite right cap to any larger
    physical suffix that contains it. *)
From Coq Require Import List Bool ZArith Lia.
From BusyCoq Require Import Line36Word Line36Right Line36Halo Line36CapModel.
Import ListNotations.

Lemma cap_anchor_decomposition w :
  existsb negb w = true ->
  exists before, w = before ++ false :: cap_after_anchor w.
Proof.
  induction w as [|a w IH]; [discriminate|].
  destruct a.
  - intros E. destruct (IH E) as [before B].
    exists (true::before). cbn [app cap_after_anchor]. now rewrite <- B.
  - intros _. exists []. reflexivity.
Qed.

Lemma mark36_right_member before cap :
  existsb id (snd (mark36 cap 0)) = true ->
  In true (snd (mark36 (before++cap) 0)).
Proof.
  intros H. rewrite mark36_app.
  destruct (mark36 cap 0) as [dc bc]; cbn [snd] in H.
  destruct (mark36 before dc) as [d b]. cbn [snd].
  apply in_or_app; right. apply existsb_exists in H.
  destruct H as [x [Hx E]]. destruct x; [exact Hx|discriminate].
Qed.

Theorem cap_halo_inputs before cap :
  existsb negb cap = true -> existsb id (snd (mark36 cap 0)) = true ->
  exists p, before++cap = p ++ false :: cap_after_anchor cap /\
            In true (snd (mark36 (before++cap) 0)).
Proof.
  intros Anchor Live. destruct (cap_anchor_decomposition cap Anchor) as [pre E].
  exists (before++pre). split.
  - rewrite <- app_assoc. now rewrite <- E.
  - exact (mark36_right_member before cap Live).
Qed.
