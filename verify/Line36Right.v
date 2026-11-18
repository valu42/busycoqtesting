(** Dimer and closing-parity accounting for the right end of line 36.
    Words and survivor masks are in physical left-to-right order.
    True denotes an opening in a word and a surviving opening in a mask. *)
From Coq Require Import Bool List Lia.
From BusyCoq Require Import Line36Matching.
Import ListNotations.

Definition bit_cost (b : bool) : nat := if b then 1 else 0.

(** Read a mask left-to-right.  The Boolean records the parity of the
    currently open run of surviving positions, whose end has not been seen. *)
Fixpoint run_cost (bits : list bool) (pending : bool) : nat :=
  match bits with
  | [] => bit_cost pending
  | true :: tail => run_cost tail (negb pending)
  | false :: tail => bit_cost pending + run_cost tail false
  end.

Definition odd_runs (bits : list bool) : nat := run_cost bits false.

Lemma run_cost_toggle bits :
  run_cost bits true <= S (run_cost bits false) /\
  run_cost bits false <= S (run_cost bits true).
Proof.
  induction bits as [|a bits IH]; [cbn; lia|].
  destruct a; cbn; lia.
Qed.

(** Each occurrence of a closing ends a compulsory tiling boundary. *)
Inductive input_tiling : list bool -> nat -> Prop :=
| tiling_nil : input_tiling [] 0
| tiling_one : forall x w n, input_tiling w n -> input_tiling (x::w) (S n)
| tiling_two : forall x w n, input_tiling w n -> input_tiling (true::x::w) n.

Fixpoint monomers (w : list bool) : nat :=
  match w with
  | [] => 0
  | false :: tail => S (monomers tail)
  | [true] => 1
  | true :: _ :: tail => monomers tail
  end.

Lemma monomers_attained : forall w, input_tiling w (monomers w).
Proof.
  fix IH 1. intros [|a w]; [constructor|].
  destruct a.
  - destruct w as [|b w]; cbn; [constructor; constructor|constructor; apply IH].
  - cbn. constructor. apply IH.
Qed.

Lemma monomers_cons_distance : forall w a,
  monomers (a::w) <= S (monomers w) /\ monomers w <= S (monomers (a::w)).
Proof.
  induction w as [|b w IH]; intros a; destruct a; try (cbn; lia).
  specialize (IH b). change (monomers w <= S (monomers (b::w)) /\
    monomers (b::w) <= S (monomers w)). lia.
Qed.

Theorem monomers_minimal w n : input_tiling w n -> monomers w <= n.
Proof.
  intros T. induction T as [|a w n T IH|a w n T IH].
  - cbn; lia.
  - pose proof (monomers_cons_distance w a). lia.
  - cbn. exact IH.
Qed.

(** [gap] is the parity of the gap already traversed since the previous
    closing or the virtual left anchor. The terminal gap is also counted. *)
Fixpoint gap_cost (w : list bool) (gap : bool) : nat :=
  match w with
  | [] => bit_cost gap
  | true :: tail => gap_cost tail (negb gap)
  | false :: tail => bit_cost (negb gap) + gap_cost tail false
  end.

Theorem monomers_gap_cost : forall w, monomers w = gap_cost w false.
Proof.
  fix IH 1. intros [|a w]; [reflexivity|].
  destruct a.
  - destruct w as [|b w]; [reflexivity|].
    destruct b; cbn; apply IH.
  - cbn. f_equal. apply IH.
Qed.

Theorem aligned_gap_cost w (e : bool) :
  monomers ((if e then [true] else []) ++ w) = gap_cost w e.
Proof. rewrite monomers_gap_cost. destruct e; reflexivity. Qed.

Lemma monomers_anchor : forall p u,
  monomers (p ++ false :: u) = monomers (p ++ [false]) + monomers u.
Proof.
  fix IH 1. intros [|a p] u; [reflexivity|].
  destruct a.
  - destruct p as [|b p]; [reflexivity|]. cbn. apply IH.
  - cbn. rewrite IH. reflexivity.
Qed.

(** A tail may already have supplied pending closings and a suffix of
    survivor bits.  This stronger form charges joined survivor runs once. *)
Theorem tiling_matching_charge w n : input_tiling w n ->
  forall (incoming : nat) (following : list bool),
    let '(outgoing, bits) := mark36 w incoming in
    outgoing + odd_runs (bits ++ following) <= incoming + odd_runs following + n.
Proof.
  intros T. induction T as [|a w n T IH|a w n T IH]; intros incoming following; unfold odd_runs in *.
  - cbn. lia.
  - specialize (IH incoming following). cbn [mark36].
    destruct (mark36 w incoming) as [d bits] eqn:M. cbn in IH.
    destruct a.
    + destruct d as [|d].
      * cbn [app odd_runs run_cost negb] in *.
        pose proof (run_cost_toggle (bits ++ following)). lia.
      * cbn [app odd_runs run_cost bit_cost negb] in *. lia.
    + cbn [app odd_runs run_cost bit_cost negb] in *. lia.
  - specialize (IH incoming following). cbn [mark36].
    destruct (mark36 w incoming) as [d bits] eqn:M. cbn in IH.
    destruct a.
    + destruct d as [|[|d]]; cbn [app odd_runs run_cost bit_cost negb] in *; lia.
    + cbn [app odd_runs run_cost bit_cost negb] in *. lia.
Qed.

Corollary matching_charge w incoming following :
  let '(d,bits) := mark36 w incoming in
  d + odd_runs (bits ++ following) <= incoming + odd_runs following + monomers w.
Proof. apply (tiling_matching_charge _ _ (monomers_attained w)). Qed.

Corollary matching_budget w :
  let '(d,bits) := mark36 w 0 in d + odd_runs bits <= monomers w.
Proof.
  pose proof (matching_charge w 0 []) as H.
  destruct (mark36 w 0) as [d bits]. rewrite app_nil_r in H. exact H.
Qed.

(** The local witness [u] starts just after the first closing in the cap. *)
Definition cap_loss (u : list bool) : nat :=
  let '(d,bits) := mark36 u 0 in monomers u - (d + odd_runs bits).

Lemma cap_loss_exact u :
  let '(d,bits) := mark36 u 0 in d + odd_runs bits + cap_loss u = monomers u.
Proof.
  pose proof (matching_budget u). unfold cap_loss. destruct (mark36 u 0); lia.
Qed.

Theorem anchored_cancellation p u :
  let '(d,bits) := mark36 (p ++ false :: u) 0 in
  d + odd_runs bits + cap_loss u <= monomers (p ++ false :: u).
Proof.
  rewrite monomers_anchor.
  replace (p ++ false :: u) with ((p ++ [false]) ++ u) by
    (rewrite <- app_assoc; reflexivity).
  rewrite mark36_app.
  pose proof (cap_loss_exact u) as E.
  destruct (mark36 u 0) as [du bu] eqn:M.
  pose proof (matching_charge (p ++ [false]) du bu) as H.
  destruct (mark36 (p ++ [false]) du) as [dp bp]. lia.
Qed.

(** The old aligned suffix pays all but at most one of the closings entering
    the tiled prefix.  This estimate is available before the next sweep. *)
Theorem debt_le_aligned_budget w e :
  fst (mark36 w 0) <= gap_cost w e + bit_cost e.
Proof.
  pose proof (matching_budget w) as H.
  destruct (mark36 w 0) as [d bits]. cbn [fst].
  destruct e.
  - pose proof (monomers_cons_distance w true) as D.
    rewrite (monomers_gap_cost (true::w)) in D. cbn [gap_cost negb] in D.
    cbn [bit_cost]. lia.
  - rewrite <- monomers_gap_cost. cbn [bit_cost]. lia.
Qed.
