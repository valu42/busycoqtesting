(** Finite prefixes of the six-phase reference language. *)
From Coq Require Import List ZArith Arith Lia.
From BusyCoq Require Export Line36Word Line36Reference Line36TileShield Line36Tiles.
Import ListNotations L36Tiles.

Fixpoint after36 (choices : list bool) (k : nat) :=
  match choices with [] => k | _::r => after36 r (next k) end.

Lemma segments_app36 ph a b k :
  segments ph k (a++b) = segments ph k a ++ segments ph (after36 a k) b.
Proof.
  revert k. induction a as [|c a IH]; intros k; [reflexivity|].
  cbn [segments after36 app]; rewrite IH, app_assoc; reflexivity.
Qed.

Lemma six_reset36 t : length t = 6 -> after36 t 0 = 0.
Proof.
  do 6 (destruct t as [|? t]; [discriminate|]).
  destruct t; [reflexivity|discriminate].
Qed.

Lemma region_segments36 ph tiles :
  Forall (fun t => length t = 6) tiles ->
  region36 ph tiles = segments ph 0 (concat tiles).
Proof.
  intro H; induction H as [|t ts Ht Hts IH]; [reflexivity|].
  change (tile36 ph t ++ region36 ph ts = segments ph 0 (t ++ concat ts)).
  now rewrite segments_app36, (six_reset36 t Ht), IH.
Qed.

Definition covered36 ph (data : list bool) : Prop :=
  exists tiles ext, Forall (fun t => length t = 6) tiles /\
                      data ++ ext = region36 ph tiles.

Lemma mark36_debt_mono w n : fst (mark36 w 0) <= fst (mark36 w n).
Proof.
  change (fst (mark36 w 0) <= fst (mark36 w (0+n))). rewrite (mark36_more w 0 n).
  destruct (mark36 w 0) as [d bs], (erase36 bs n); cbn; lia.
Qed.

Lemma covered_data36 ph data :
  ph < 6 -> covered36 ph data ->
  fst (mark36 data 0) = 0 /\
  (Z.of_nat (length data) - 2 * bal36 data <= 22)%Z.
Proof.
  intros Hp [tiles [ext [Htiles He]]].
  pose proof (region_facts36 ph tiles Hp Htiles) as R.
  rewrite <- He, mark36_app in R.
  destruct (mark36 ext 0) as [de be].
  pose proof (mark36_debt_mono data de) as M.
  destruct (mark36 data de) as [d b]. cbn [fst] in M. destruct R as [-> _].
  split; [lia|].
  eapply (factor_density ph 0 (concat tiles) data Hp).
  exists (@nil bool),ext. cbn [app]. change (segments ph 0 (concat tiles) = data++ext).
  now rewrite <- region_segments36 by assumption.
Qed.

Lemma phase_prefix_length36 ph : ph < 6 -> length (phase_prefix ph) = 26.
Proof. do 6 (destruct ph as [|ph]; [reflexivity|]); lia. Qed.
