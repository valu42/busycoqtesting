(** Spatial consequences of the six-piece grammar at an arbitrary finite cut. *)
From Coq Require Import List Bool ZArith Lia.
From BusyCoq Require Import Line36Matching Line36Tiles.
Import ListNotations L36Tiles.
Local Open Scope Z_scope.

Module L36TileShield.

Lemma prefix_is_factor_of_factor (p r whole : list bool) :
  factor (p++r) whole -> factor p whole.
Proof.
  intros [a [b ->]]. exists a, (r++b). repeat rewrite <- app_assoc; reflexivity.
Qed.

Lemma suffix_is_factor_of_factor (p r whole : list bool) :
  factor (p++r) whole -> factor r whole.
Proof.
  intros [a [b ->]]. exists (a++p), b. repeat rewrite <- app_assoc; reflexivity.
Qed.

(** A prefix attains the extreme deficit. This lets the density theorem
    bound the debt of any finite reference continuation, regardless of its
    length or the number of complete pieces crossed. *)
Lemma prefix_attains_debt (w : list bool) : exists p r, w = p ++ r /\
  balance p = - Z.of_nat (fst (mark36 w 0)).
Proof.
  induction w as [|x w IH].
  - exists [], []; auto.
  - destruct IH as [p [r [E Hb]]].
    cbn [mark36]. destruct (mark36 w 0) as [d bits] eqn:Mm.
    cbn [fst] in Hb |- *. destruct x.
    + destruct d as [|d].
      * exists [], (true::w). split; reflexivity.
      * exists (true::p),r. split; [now rewrite E|].
        change (1 + balance p = - Z.of_nat d). rewrite Hb, Nat2Z.inj_succ. lia.
    + exists (false::p),r. split; [now rewrite E|].
      change (-1 + balance p = - Z.of_nat (S d)). rewrite Hb, Nat2Z.inj_succ. lia.
Qed.

Theorem continuation_debt_le_eleven ph start choices w :
  (ph < 6)%nat -> factor w (tiles_word ph start choices) ->
  (fst (mark36 w 0) <= 11)%nat.
Proof.
  intros Hph HF. destruct (prefix_attains_debt w) as [p [r [E Hb]]].
  assert (F : factor p (tiles_word ph start choices)).
  { rewrite E in HF. destruct HF as [a [b ->]]. exists a,(r++b). repeat rewrite <- app_assoc; reflexivity. }
  pose proof (factor_balance_floor ph start choices p Hph F).
  lia.
Qed.

Theorem ranked_tiled_displacement ph start choices w d :
  (ph < 6)%nat -> factor w (tiles_word ph start choices) ->
  (0 < d <= openings36 (snd (mark36 w 0)))%nat ->
  exists l r, w = l ++ true :: r /\ fst (mark36 r 0) = 0%nat /\
    balance (true::r) = Z.of_nat d /\
    Z.of_nat (length (true::r)) <= 2 * Z.of_nat d + 22 /\
    mark36 (true::r) d = (0%nat, repeat false (length (true::r))).
Proof.
  intros Hph HF Hd.
  destruct (mark36_rank w d Hd) as [l [r [E [Dz [B Eq]]]]].
  assert (F : factor (true::r) (tiles_word ph start choices)).
  { rewrite E in HF. exact (suffix_is_factor_of_factor l _ _ HF). }
  pose proof (factor_density ph start choices _ Hph F).
  change (balance (true::r) = Z.of_nat d) in B.
  exists l,r; repeat split; auto; lia.
Qed.

(** The occupied header has 26 symbols. Under this margin the perturbed
    suffix begins in the actual tiled data, even when exterior debt is high. *)
Theorem protected_has_survivors ph start choices protected charge d :
  (ph < 6)%nat -> factor protected (tiles_word ph start choices) ->
  0 <= charge -> 52 <= 26 + Z.of_nat (length protected) - 4 * charge ->
  Z.of_nat d <= charge + 1 ->
  (d <= openings36 (snd (mark36 protected 0)))%nat.
Proof.
  intros Hph HF HA Hmargin Hd. pose proof (factor_density ph start choices _ Hph HF).
  pose proof (mark36_balance protected 0).
  unfold balance in *; lia.
Qed.

End L36TileShield.
