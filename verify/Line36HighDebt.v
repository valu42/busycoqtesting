(** Location and shape of a deep retreat into a tiled reference. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Word Line36Tiles Line36TileShield.
Import ListNotations L36Tiles L36TileShield.
Local Open Scope Z_scope.

Module L36HighDebt.

Lemma openings_le_length bits : (openings36 bits <= length bits)%nat.
Proof. induction bits as [|[] r IH]; cbn; lia. Qed.

Lemma zeros_no_openings n : openings36 (repeat false n) = 0%nat.
Proof. induction n; cbn; auto. Qed.

Lemma halo_erased halo d : (length halo <= d)%nat ->
  snd (mark36 halo d) = repeat false (length halo) /\
  Z.of_nat (fst (mark36 halo d)) = Z.of_nat d - bal36 halo.
Proof.
  intros Hd. assert (Hlen := mark36_length halo 0).
  assert (Hmask : snd (mark36 halo d) = repeat false (length halo)).
  { change (snd (mark36 halo (0+d)) = repeat false (length halo)). rewrite mark36_more.
    destruct (mark36 halo 0) as [e bits] eqn:M. cbn [snd] in Hlen.
    rewrite erase36_all by (pose proof (openings_le_length bits); lia).
    cbn. now rewrite Hlen. }
  split; [exact Hmask|]. pose proof (mark36_balance halo d) as HB.
  rewrite Hmask, zeros_no_openings in HB. lia.
Qed.

Lemma erased_halo_bounds halo d : length halo = 3%nat -> (29 <= d)%nat ->
  let k := fst (mark36 halo d) in
  (11 < k)%nat /\ Z.of_nat k <= Z.of_nat d+3.
Proof.
  intros Hé Hd. pose proof (halo_erased halo d ltac:(lia)) as [_ Hb].
  pose proof (balance_lower_length halo).
  assert (B : bal36 halo <= Z.of_nat (length halo)).
  { clear. induction halo as [|[] r IH]; cbn [length bal36]; rewrite ?Nat2Z.inj_succ; lia. }
  unfold balance in *; cbn zeta. lia.
Qed.

(** Assume [q] units of exterior debt for the reference, and [k] for the
    actual execution. Before the selected opening the masks agree; this
    remains true across any older prefix [old]. *)
Theorem rank_splice ph start choices data old q k :
  (ph<6)%nat -> factor data (tiles_word ph start choices) ->
  (q<k <= openings36 (snd (mark36 data 0)))%nat ->
  exists l r g before after,
    data=l++true::r /\
    Z.of_nat (length (true::r)) <= 2*Z.of_nat k+22 /\
    bal36 (true::r)=Z.of_nat k /\
    mark36 (old++data) q = (g,before++true::after) /\
    mark36 (old++data) k = (g,before++repeat false (S(length r))) /\
    length before = (length old+length l)%nat.
Proof.
  intros Hp F Hq.
  destruct (ranked_tiled_displacement ph start choices data k Hp F ltac:(lia))
    as [l [r [E [Zr [Br [Lr Mk]]]]]].
  assert (Qbal : Z.of_nat q <= bal36 r).
  { change (1 + bal36 r = Z.of_nat k) in Br; lia. }
  pose proof (mark36_shield r q Qbal) as H0. rewrite Zr in H0.
  destruct (mark36 r q) as [rq rb] eqn:R.
  cbn [fst] in H0. subst rq.
  destruct (mark36 (old++l) 0) as [g before] eqn:M.
  exists l,r,g,before,rb. split; [exact E|]. split; [exact Lr|].
  split; [exact Br|]. rewrite E. rewrite app_assoc.
  split.
  - rewrite mark36_app. cbn [mark36]. now rewrite R,M.
  - split.
    + rewrite mark36_app, Mk, M. reflexivity.
    + pose proof (mark36_length (old++l) 0) as L.
      rewrite M in L; cbn [snd] in L. now rewrite length_app in L.
Qed.

Lemma deriv_flat_true n : deriv36 false (repeat false n) = repeat true n.
Proof. induction n; cbn; congruence. Qed.

Theorem deriv_splice previous before after n :
  exists common bit rest,
    deriv36 previous (before++true::after) = common++bit::rest /\
    deriv36 previous (before++repeat false (S n)) =
       common++negb bit::repeat true n /\
    length common = length before.
Proof.
  exists (deriv36 previous before), (last before previous), (deriv36 true after).
  rewrite !deriv36_app. cbn [repeat deriv36]. rewrite deriv_flat_true.
  split; [destruct (last before previous);reflexivity|].
  split; [destruct (last before previous);reflexivity|].
  clear. revert previous. induction before as [|b r IH]; intros previous; cbn; auto.
Qed.

End L36HighDebt.
