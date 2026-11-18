From Coq Require Import List Bool Lia Arith.
From BusyCoq Require Import Line36Matching Line36Right Line36CapModel Line36Cap.
Import ListNotations.

Lemma cap_deriv_tl p q bits : tl (cap_deriv p bits) = tl (cap_deriv q bits).
Proof. destruct bits; reflexivity. Qed.

Lemma cap_condition_sound : forall w v previous,
  cap_condition w v = true ->
   v <= 21 /\ In false w /\ In true (snd (mark36 w 0)) /\
   exists next, cap_value (cap_next w previous) = Some next /\
   S next <= v + 3 * cap_loss (cap_after_anchor w).
Proof.
  intros w v previous C. unfold cap_condition in C. unfold cap_next.
  destruct (mark36 w 0) as [d bits] eqn:Match. simpl snd.
  repeat rewrite andb_true_iff in C.
  destruct C as [[[[V Surv] Close] Left] Right].
  apply Nat.leb_le in V. apply existsb_exists in Surv, Close.
  destruct Surv as [[|] [Surv Sval]]; [|discriminate].
  destruct Close as [[|] [Close Cval]]; [discriminate|].
  repeat split; try assumption.
  assert (Test : bounded_successor v (cap_loss (cap_after_anchor w))
    (if last w false then tl (cap_deriv (previous && (d =? 0)) bits) ++ [false]
     else cap_deriv (previous && (d =? 0)) bits) = true).
  { destruct previous; [|exact Left].
    destruct d as [|d], (last w false) eqn:Last.
    - cbn in *. rewrite (cap_deriv_tl true false). exact Left.
    - exact Right.
    - exact Left.
    - exact Left. }
  unfold bounded_successor in Test.
  destruct (cap_value _) as [next|] eqn:N in Test; try discriminate.
  exists next. split; [exact N|apply Nat.leb_le; exact Test].
Qed.
