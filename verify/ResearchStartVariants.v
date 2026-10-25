(* Two pairs with the same transition program but different blank starts.
   These reductions do NOT equate the two blank runs of either pair.
   AI-assisted research by Codex; uses the repository's Permute/Flip lemmas. *)
From BusyCoq Require Import Individual62 ES_v2 ES_v3
  ResearchFractalSweep ResearchMonotoneFrontier.
From Coq Require Import List String.
Import ListNotations.
Open Scope sym_scope.

Module FractalTwin.
Definition tm := Eval compute in
  (TM_from_str "1RB0RA_1LC1RA_0LD1LD_0LE0LC_1LA0LF_---1LC").
Definition ren (q : Q) : Q :=
  match q with A => B | B => C | C => D | D => E | E => A | F => F end.

Lemma ren_perm : Perm (flip FractalSweep.tm) tm ren.
Proof.
  split.
  - intros [] [] H; unfold flip in H; cbn in H; try discriminate; reflexivity.
  - intros [] [] s' d q' H; unfold flip in H; cbn in H; inversion H; reflexivity.
Qed.

Definition unren (q : Q) : Q :=
  match q with A => E | B => A | C => B | D => C | E => D | F => F end.
Lemma unren_perm : Perm (flip tm) FractalSweep.tm unren.
Proof.
  split.
  - intros [] [] H; unfold flip in H; cbn in H; try discriminate; reflexivity.
  - intros [] [] s' d q' H; unfold flip in H; cbn in H; inversion H; reflexivity.
Qed.

Lemma blank_halts_iff_E :
  halts tm c0 <-> halts FractalSweep.tm (E;; tape0).
Proof.
  split; intro H.
  - exact (perm_halts _ _ unren A tape0 unren_perm (flip_halts tm c0 H)).
  - exact (perm_halts _ _ ren E tape0 ren_perm
      (flip_halts FractalSweep.tm (E;; tape0) H)).
Qed.

Definition initial : FractalSweep.pair := ([S1], [S1]).
Lemma E_to_initial :
  (E;; tape0) -[FractalSweep.tm]->+ FractalSweep.config B initial.
Proof.
  unfold initial, FractalSweep.config, FractalSweep.side_of; cbn.
  eapply progress_intro; [prove_step | simpl_tape]; es.
Qed.

Theorem blank_halts_iff_turns :
  halts tm c0 <-> iter_halts FractalSweep.turn initial.
Proof.
  rewrite blank_halts_iff_E, <- FractalSweep.halts_iff_turns.
  apply halts_evstep_iff, progress_evstep, E_to_initial.
Qed.

Print Assumptions ren_perm.
Print Assumptions unren_perm.
Print Assumptions blank_halts_iff_E.
Print Assumptions E_to_initial.
Print Assumptions blank_halts_iff_turns.
End FractalTwin.

Module MonotoneTwin.
Definition tm := Eval compute in
  (TM_from_str "1RB0RF_1LC0RD_1LA0LD_1LE0RA_0LB---_0LB1RB").
Definition ren (q : Q) : Q :=
  match q with A => D | B => E | C => B | D => C | E => A | F => F end.

Lemma ren_perm : Perm (flip MonotoneFrontier.tm) tm ren.
Proof.
  split.
  - intros [] [] H; unfold flip in H; cbn in H; try discriminate; reflexivity.
  - intros [] [] s' d q' H; unfold flip in H; cbn in H; inversion H; reflexivity.
Qed.

Definition unren (q : Q) : Q :=
  match q with A => E | B => C | C => D | D => A | E => B | F => F end.
Lemma unren_perm : Perm (flip tm) MonotoneFrontier.tm unren.
Proof.
  split.
  - intros [] [] H; unfold flip in H; cbn in H; try discriminate; reflexivity.
  - intros [] [] s' d q' H; unfold flip in H; cbn in H; inversion H; reflexivity.
Qed.

Lemma blank_halts_iff_E :
  halts tm c0 <-> halts MonotoneFrontier.tm (E;; tape0).
Proof.
  split; intro H.
  - exact (perm_halts _ _ unren A tape0 unren_perm (flip_halts tm c0 H)).
  - exact (perm_halts _ _ ren E tape0 ren_perm
      (flip_halts MonotoneFrontier.tm (E;; tape0) H)).
Qed.

Theorem blank_halts_iff_root :
  halts tm c0 <->
  halts MonotoneFrontier.tm (0inf <* [1;0;1] {{B}}> 0inf).
Proof.
  rewrite blank_halts_iff_E.
  apply halts_evstep_iff, progress_evstep, MonotoneFrontier.blank_E.
Qed.

Print Assumptions ren_perm.
Print Assumptions unren_perm.
Print Assumptions blank_halts_iff_E.
Print Assumptions blank_halts_iff_root.
End MonotoneTwin.
