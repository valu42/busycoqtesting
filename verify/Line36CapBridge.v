(** Exact projection of successful line-36 word sweeps to the width-50 graph. *)
From Coq Require Import List Bool Arith Lia.
From BusyCoq Require Import Line36Word Line36CapModel.
Import ListNotations.

Module L36CapBridge.

Lemma final_mask w d default :
  w <> [] -> last (snd (mark36 w d)) default =
             andb (last w false) (Nat.eqb d 0).
Proof.
  induction w as [|b w IH] using rev_ind; [contradiction|].
  intro H. rewrite mark36_app, last36_app.
  destruct b, d as [|d]; cbn [mark36];
    repeat match goal with
    | |- context [mark36 w ?q] => destruct (mark36 w q)
    end;
    cbn [snd]; rewrite last36_app; reflexivity.
Qed.

Lemma cap_derivative_is a w : cap_deriv a w = deriv36 a w.
Proof. induction w as [|b w IH] in a |- *; cbn; [reflexivity|now rewrite IH]. Qed.

Lemma derivative_length a w : length (deriv36 a w) = length w.
Proof. induction w as [|b w IH] in a |- *; cbn; auto. Qed.

Lemma next_width w a : w <> [] -> length (cap_next w a) = length w.
Proof.
  unfold cap_next. destruct (mark36 w 0) as [d m] eqn:M; intro H.
  rewrite cap_derivative_is.
  pose proof (mark36_length w 0) as L; rewrite M in L; cbn in L.
  destruct (last w false); [| now rewrite derivative_length].
  remember (deriv36 (a && (d =? 0)) m) as D eqn:E.
  assert (LD : length D = length w) by (rewrite E, derivative_length; exact L).
  destruct D; destruct w; cbn in *; try contradiction; try lia.
  rewrite app_length. cbn. lia.
Qed.

(** The actual left neighbor of a cap cell can survive exactly when its digit
    is an opening and the cap sends it zero debt. The same fact gives the true
    right carry at the end of a nonempty cap. *)
Theorem actual_cap_image p w out :
  p <> [] -> w <> [] -> step36 (p ++ w) = Some out ->
  exists front, out = front ++ cap_next w (last p false).
Proof.
  intros P W. unfold step36. rewrite mark36_app.
  destruct (mark36 w 0) as [d m] eqn:M.
  destruct (mark36 p d) as [g bits] eqn:G; cbn [fst snd].
  destruct (g <? 6) eqn:ok; [|discriminate]. intros [= <-].
  pose proof (final_mask p d (g =? 1) P) as L.
  rewrite G in L. cbn [snd] in L.
  pose proof (final_mask w 0 (last bits (g =? 1)) W) as T.
  rewrite M in T. cbn [snd Nat.eqb] in T. rewrite andb_true_r in T.
  unfold cap_next, output36, carry36. rewrite M. change cap_deriv with deriv36.
  rewrite deriv36_app, last36_app, T, L.
  remember (deriv36 (last p false && (d =? 0)) m) as D eqn:E.
  destruct (last w false) eqn:F.
  - assert (D <> []).
    { pose proof (mark36_length w 0) as Len. rewrite M in Len; cbn in Len.
      intro Empty. apply (f_equal (@length bool)) in Empty.
      rewrite E, derivative_length, Len in Empty; destruct w; cbn in *; congruence. }
    destruct D as [|b D]; [contradiction|].
    exists (guard36 g ++ deriv36 (g =? 1) bits ++ [b]).
    cbn [tl app]. now rewrite <- !app_assoc.
  - exists (guard36 g ++ deriv36 (g =? 1) bits).
    now rewrite !app_nil_r, <- app_assoc.
Qed.

Definition window (k : nat) (w : list bool) := skipn (length w - k) w.

Lemma window_suffix n front w : length w = n -> window n (front ++ w) = w.
Proof.
  intro E. unfold window. rewrite app_length, E.
  replace (length front + n - n) with (length front) by lia.
  rewrite skipn_app, skipn_all, Nat.sub_diag. reflexivity.
Qed.

Corollary actual_window n p w out :
  p <> [] -> w <> [] -> length w = n -> step36 (p ++ w) = Some out ->
  window n out = cap_next w (last p false).
Proof.
  intros P W N S. destruct (actual_cap_image p w out P W S) as [front ->].
  apply window_suffix. rewrite next_width by assumption. exact N.
Qed.

(** A successful sweep adds the header and, on an open ending, one cell.
    A next cut no farther than the old cut plus that header therefore keeps
    the full old uncontrolled width in the next suffix. *)
Lemma exact_width w out : w <> [] -> step36 w = Some out ->
  length out = length w + length (guard36 (fst (mark36 w 0))) +
               (if last w false then 1 else 0).
Proof.
  intro W. unfold step36. destruct (mark36 w 0) as [d bits] eqn:M.
  destruct (d <? 6); [|discriminate]. intros [= <-].
  unfold output36, carry36. rewrite !length_app, derivative_length.
  pose proof (final_mask w 0 (d =? 1) W) as T.
  pose proof (mark36_length w 0) as L. rewrite M in L,T.
  cbn [snd] in T,L. rewrite andb_true_r in T. rewrite T.
  destruct (last w false); cbn [length fst]; lia.
Qed.

Lemma tail_margin p t np nt :
  p ++ t <> [] -> step36 (p ++ t) = Some (np ++ nt) ->
  length np <= length p + length (guard36 (fst (mark36 (p++t) 0))) ->
  length t <= length nt.
Proof.
  intros W Step Cut. pose proof (exact_width _ _ W Step) as E.
  rewrite !length_app in E. lia.
Qed.

(** At a final closing, both it and its left neighbor have zero survivor bits.
    At a final opening the return appends one closing. *)
Theorem terminal_alternates w out : 2 <= length w ->
  step36 w = Some out -> last out false = negb (last w false).
Proof.
  induction w as [|b w IH] using rev_ind; [cbn; lia|].
  induction w as [|a p IH2] using rev_ind; [cbn; lia|].
  intros Len. rewrite <- app_assoc. cbn [app]. unfold step36. rewrite mark36_app. destruct a,b; cbn [mark36];
    repeat match goal with
    | |- context [mark36 p ?q] => destruct (mark36 p q) as [d bits] eqn:M
    end;
    cbn [app]; destruct (d <? 6); try discriminate;
    intros [= <-]; unfold output36, carry36;
    rewrite !deriv36_app, !last36_app; cbn [deriv36 last app Bool.eqb];
    destruct (last bits (d =? 1)); reflexivity.
Qed.

End L36CapBridge.
