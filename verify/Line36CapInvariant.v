(** Interface from an actual word sweep to the finite 50-cell potential.
    The graph's all-states fact is an explicit hypothesis, so this file can
    be checked before evaluating the large finite certificate. *)
From Coq Require Import List Bool Arith Lia ZArith String.
From BusyCoq Require Import Line36Cap Line36CapSound Line36CapModel Line36Right
                            Line36Word Line36CapBridge Line36Machine Line36Seed.
Import ListNotations.
Local Open Scope list_scope.

Module L36CapInvariant.

Definition graph_spec :=
  forall w v, List.length w = 50 -> cap_value w = Some v -> cap_condition w v = true.

Definition terminal_bit w : Z := if last w false then 1%Z else 0%Z.
Definition real_loss w := cap_loss (cap_after_anchor (L36Seed.cap50 w)).

Lemma cap50_split w : 50 < List.length w ->
  exists prefix, w = prefix ++ L36Seed.cap50 w /\ prefix <> [] /\
                 List.length (L36Seed.cap50 w) = 50.
Proof.
  intro H. unfold L36Seed.cap50. exists (firstn (List.length w - 50) w).
  split; [symmetry; apply firstn_skipn|]. split.
  - intro E. apply (f_equal (@List.length bool)) in E.
    rewrite firstn_length in E. cbn in E. lia.
  - rewrite skipn_length. lia.
Qed.

Lemma longer_on_success w out : step36 w = Some out -> List.length w < List.length out.
Proof.
  unfold step36. destruct (mark36 w 0) as [g bits] eqn:M.
  destruct (g <? 6); [|discriminate]. intros [= <-].
  unfold output36. rewrite !length_app, L36CapBridge.derivative_length.
  pose proof (mark36_length w 0) as L. rewrite M in L; cbn [snd] in L.
  assert (0 < List.length (guard36 g)) by (destruct g as [|[|[|[|[|g]]]]]; cbn; lia).
  lia.
Qed.

Theorem real_cap_features (G : graph_spec) w h :
  50 < List.length w -> cap_value (L36Seed.cap50 w) = Some h ->
  h <= 21 /\ In false (L36Seed.cap50 w) /\ In true (snd (mark36 (L36Seed.cap50 w) 0)).
Proof.
  intros H Val. destruct (cap50_split w H) as [p [_ [_ W]]].
  destruct (cap_condition_sound _ _ false (G _ _ W Val)) as [K [Cl [Live _]]].
  auto.
Qed.

Lemma closing_anchor w : In false w ->
  exists prefix, w = prefix ++ false :: cap_after_anchor w.
Proof.
  induction w as [|b w IH]; cbn; [contradiction|].
  destruct b.
  - intros [E|H]; [discriminate|]. destruct (IH H) as [prefix F].
    exists (true::prefix). cbn. now rewrite <- F.
  - intros _. exists (@nil bool). reflexivity.
Qed.

(** A long unknown suffix owns the entire cap. Matching there starts from the
    actual right edge, so every opening surviving in the cap still survives in
    the whole unknown suffix. The suffix after its first closing anchor is
    exactly the input to the finite cancellation count. *)
Theorem tail_anchor (G : graph_spec) p t h :
  50 <= List.length t -> 50 < List.length (p ++ t) ->
  cap_value (L36Seed.cap50 (p ++ t)) = Some h ->
  exists before u, t = before ++ false :: u /\
                   real_loss (p ++ t) = cap_loss u /\
                   In true (snd (mark36 t 0)).
Proof.
  intros Wide Whole Val.
  pose proof (real_cap_features G (p++t) h Whole Val) as [_ [Close Live]].
  set (cut := List.length t - 50).
  set (a := firstn cut t). set (b := skipn cut t).
  assert (T : t = a ++ b) by (unfold a,b; symmetry; apply firstn_skipn).
  assert (W : List.length b = 50) by (unfold b,cut; rewrite length_skipn; lia).
  assert (E : L36Seed.cap50 (p ++ t) = b).
  { rewrite T, app_assoc. apply L36CapBridge.window_suffix. exact W. }
  rewrite E in Close, Live.
  destruct (closing_anchor b Close) as [q Anchor].
  exists (a ++ q),(cap_after_anchor b). split.
  - rewrite T. rewrite Anchor at 1. now rewrite <- app_assoc.
  - split.
    + unfold real_loss. now rewrite E.
    + rewrite T, mark36_app.
      destruct (mark36 b 0) as [d m] eqn:M; cbn in Live.
      destruct (mark36 a d) as [g marks]. cbn. apply in_or_app. now right.
Qed.

(** The signed potential used by the global ledger is [- Z.of_nat h].
    Expressing the unsigned successor displacement here also gives its
    signed predecessor inequality directly. *)
Theorem real_cap_step (G : graph_spec) w out h :
  50 < List.length w -> cap_value (L36Seed.cap50 w) = Some h ->
  step36 w = Some out ->
  exists h', cap_value (L36Seed.cap50 out) = Some h' /\
             h <= 21 /\ h' <= 21 /\ 50 < List.length out /\
             (Z.of_nat h' - Z.of_nat h <= 3 * Z.of_nat (real_loss w) - 1)%Z /\
             terminal_bit out = (1 - terminal_bit w)%Z.
Proof.
  intros Wide Val Sweep.
  destruct (cap50_split w Wide) as [p [Cut [P W]]].
  assert (C : L36Seed.cap50 w <> []) by (intro E; rewrite E in W; discriminate).
  assert (E : L36Seed.cap50 out = cap_next (L36Seed.cap50 w) (last p false)).
  { change (L36CapBridge.window 50 out = cap_next (L36Seed.cap50 w) (last p false)).
    apply L36CapBridge.actual_window; try assumption.
    rewrite <- Cut. exact Sweep. }
  destruct (cap_condition_sound _ _ (last p false) (G _ _ W Val)) as [B [_ [_ [v [N I]]]]].
  rewrite <- E in N.
  assert (Out : 50 < List.length out) by (pose proof (longer_on_success w out Sweep); lia).
  destruct (real_cap_features G out v Out N) as [B' _].
  pose proof (L36CapBridge.terminal_alternates w out ltac:(lia) Sweep) as T.
  exists v. repeat split; try assumption.
  - unfold real_loss. lia.
  - unfold terminal_bit. rewrite T. destruct (last w false); reflexivity.
Qed.

Corollary after_protected_cut (G : graph_spec) p t out h :
  53 <= List.length t -> cap_value (L36Seed.cap50 (p ++ t)) = Some h ->
  step36 (p ++ t) = Some out ->
  exists h', cap_value (L36Seed.cap50 out) = Some h' /\
             h <= 21 /\ h' <= 21 /\ 50 < List.length out /\
             (Z.of_nat h' - Z.of_nat h <= 3 * Z.of_nat (real_loss (p++t)) - 1)%Z /\
             terminal_bit out = (1 - terminal_bit (p++t))%Z.
Proof. intros W. apply real_cap_step; [assumption|rewrite length_app; lia]. Qed.

(** The graph's two physical initialization points are members independently
    of the all-states dynamic-programming certificate. *)
Theorem seed_values :
  cap_value (L36Seed.cap50 L36Seed.epoch32_word) = Some 0 /\
  cap_value (L36Seed.cap50 line36_blank_seed) = Some 5.
Proof. vm_compute. split; reflexivity. Qed.

Definition cap335 := read_digits "21211111111111112121112121121211112111211211122111"%string.
Fixpoint take_sweeps (n : nat) (w : list bool) : option (list bool) :=
  match n with
  | 0 => Some w
  | S k => match step36 w with Some v => take_sweeps k v | None => None end
  end.

Theorem cap_four_sweeps_later :
  option_map L36Seed.cap50 (take_sweeps 4 line36_blank_seed) = Some cap335 /\
  cap_value cap335 = Some 1.
Proof. vm_compute. split; reflexivity. Qed.

End L36CapInvariant.
