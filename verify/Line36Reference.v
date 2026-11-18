(** Reference sweeps with any finite number of independently chosen tiles. *)
From Coq Require Import List Bool Lia Arith.
From BusyCoq Require Import Line36Word Line36Tiles.
Import ListNotations.
Import L36Tiles.

Definition tile36 ph := segments ph 0.

Fixpoint patterns36 n : list (list bool) :=
  match n with
  | 0 => [[]]
  | S k => map (cons false) (patterns36 k) ++ map (cons true) (patterns36 k)
  end.

Lemma patterns36_complete v : In v (patterns36 (length v)).
Proof.
  induction v as [|b v IH]; cbn; [auto|].
  apply in_or_app; destruct b; [right|left]; now apply in_map.
Qed.

Definition bits_eq36 a b :=
  if list_eq_dec Bool.bool_dec a b then true else false.
Lemma bits_eq36_sound a b : bits_eq36 a b = true -> a=b.
Proof. unfold bits_eq36; destruct (list_eq_dec _ _ _); congruence. Qed.

Definition tile_test36 ph choices :=
  let '(d,bits) := mark36 (tile36 ph choices) 0 in
  (d =? 0) && Bool.eqb (last bits (phase_last ph)) (phase_last ph) &&
  bits_eq36 (phase_overlap ph ++ deriv36 (phase_last ph) bits)
            (tile36 (next ph) choices ++ phase_overlap ph).

Lemma all_tile_tests36 :
  forallb (fun ph => forallb (tile_test36 ph) (patterns36 6)) (seq 0 6) = true.
Proof. vm_compute. reflexivity. Qed.

Lemma tile_facts36 ph choices (Hp : ph < 6) (Hn : length choices = 6) :
  let '(d,bits) := mark36 (tile36 ph choices) 0 in
  d = 0 /\ last bits (phase_last ph) = phase_last ph /\
  phase_overlap ph ++ deriv36 (phase_last ph) bits =
  tile36 (next ph) choices ++ phase_overlap ph.
Proof.
  pose proof all_tile_tests36 as H.
  apply forallb_forall with (x:=ph) in H; [|apply in_seq; lia].
  apply forallb_forall with (x:=choices) in H.
  2: rewrite <- Hn; apply patterns36_complete.
  unfold tile_test36 in H. destruct (mark36 _ _) as [d bits].
  repeat rewrite andb_true_iff in H.
  destruct H as [[Hd Hb] He]. apply Nat.eqb_eq in Hd.
  apply Bool.eqb_prop in Hb. now apply bits_eq36_sound in He.
Qed.

Definition region36 ph (tiles : list (list bool)) :=
  concat (map (tile36 ph) tiles).

Lemma region_facts36 ph tiles (Hp : ph < 6)
  (Htiles : Forall (fun v => length v = 6) tiles) :
  let '(d,bits) := mark36 (region36 ph tiles) 0 in
  d = 0 /\ last bits (phase_last ph) = phase_last ph /\
  phase_overlap ph ++ deriv36 (phase_last ph) bits =
  region36 (next ph) tiles ++ phase_overlap ph.
Proof.
  induction Htiles as [|t ts Ht Hall IH].
  - cbn [region36 mark36 deriv36 last map concat]. rewrite app_nil_r; auto.
  - change (region36 ph (t::ts)) with (tile36 ph t ++ region36 ph ts).
    change (region36 (next ph) (t::ts)) with (tile36 (next ph) t ++ region36 (next ph) ts).
    rewrite mark36_app.
    destruct (mark36 (region36 ph ts) 0) as [dt bts].
    destruct IH as [-> [Et Hts]].
    pose proof (tile_facts36 ph t Hp Ht) as H.
    destruct (mark36 (tile36 ph t) 0) as [d bt]. destruct H as [-> [E Ht']].
    split; [reflexivity|]. rewrite last36_app, E. split; [exact Et|].
    rewrite deriv36_app, E, app_assoc, Ht'.
    rewrite <- app_assoc, Hts, app_assoc. reflexivity.
Qed.

Lemma prefix_facts36 ph (Hp : ph < 6) :
  let '(d,bits) := mark36 (phase_prefix ph) 0 in
  d = phase_guard ph /\ d < 6 /\
  last bits (d =? 1) = phase_last ph /\
  guard36 d ++ deriv36 (d =? 1) bits = phase_prefix (next ph) ++ phase_overlap ph.
Proof. do 6 (destruct ph as [|ph]; [vm_compute; repeat split; lia|]); lia. Qed.

Theorem reference_sweep36 ph tiles (Hp : ph < 6)
  (Htiles : Forall (fun v => length v = 6) tiles) :
  step36 (phase_prefix ph ++ region36 ph tiles) =
  Some (phase_prefix (next ph) ++ region36 (next ph) tiles ++ phase_overlap ph ++
        (if phase_last ph then [false] else [])).
Proof.
  unfold step36. rewrite mark36_app.
  pose proof (region_facts36 ph tiles Hp Htiles) as R.
  destruct (mark36 (region36 ph tiles) 0) as [dt bt]. destruct R as [-> [Rt R]].
  pose proof (prefix_facts36 ph Hp) as P.
  destruct (mark36 (phase_prefix ph) 0) as [d bp]. destruct P as [_ [Hd [Ep P]]].
  apply Nat.ltb_lt in Hd; rewrite Hd. unfold output36, carry36.
  rewrite deriv36_app, last36_app, Ep, Rt. f_equal.
  repeat rewrite app_assoc. rewrite P.
  rewrite <- (app_assoc (phase_prefix (next ph)) (phase_overlap ph)), R.
  now repeat rewrite app_assoc.
Qed.
