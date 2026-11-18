(** Input to the finite certificate on a real protected cut. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Front Line36Cut Line36Safety Line36Physical
  Line36Tiles Line36Left Line36LeftStep Line36History Line36LeftCheck Line36Word Line36Machine Line36Seed.
Import ListNotations L36Tiles L36Left L36LeftStep L36LeftGroups.

Lemma halo_code36 tail : 3 <= length tail -> encode_halo tail < 8.
Proof.
  destruct tail as [|a [|b [|c t]]]; cbn [length]; try lia.
  destruct a,b,c; reflexivity || (cbn; lia).
Qed.

Theorem front_context36 f :
  fvalid f ->
  (454 <= Z.of_nat (length (fprefix f)) - 4 * Z.of_nat (L36Seed.budget (fprefix f) (ftail f)))%Z ->
  well_formed (fstate f) /\ 5 <= length (fchoices f) /\
  exists out, step36 (fword f) = Some out.
Proof.
  intros [Hp [Pl T]] Reserve.
  assert (K : fkind f < 6) by (apply Nat.mod_upper_bound; lia).
  split.
  - unfold well_formed, fstate; cbn [phase kind partial_len partial_choice halo].
    rewrite L36History.piece_exact by assumption.
    repeat split; try assumption; apply halo_code36; lia.
  - split.
    + pose proof (L36Cut.canonical_width _ _ _ _ Hp Pl) as W.
      change (length (fprefix f) < 26 + 30*S (length (fchoices f))) in W. lia.
    + destruct (reserve_sweep36 _ (fdata f) (ftail f) Hp
          (L36Cut.canonical_covered _ _ _ _) ltac:(change (52 <= Z.of_nat (length (fprefix f)) -
             4 * Z.of_nat (L36Seed.budget (fprefix f) (ftail f)))%Z; lia)) as [v [S _]].
      exists v; exact S.
Qed.

Lemma front_tail36 f : fvalid f ->
  ftail f = firstn 3 (ftail f) ++ skipn 3 (ftail f) /\
  length (firstn 3 (ftail f)) = 3 /\ 50 <= length (skipn 3 (ftail f)).
Proof.
  intros [_ [_ T]]. split; [symmetry; apply firstn_skipn|].
  rewrite length_firstn, length_skipn. lia.
Qed.
