(** The original halting problem as iteration on a pair of finite words.
    A round consumes a right sweep and the entire following left sweep. *)
From BusyCoq Require Import Individual62 Line429Engine Line429Progress Line429RightSweep
  Line429LeftLanguage Line429LeftOutput Line429RightExec Line429LeftExec Line429GateBlank.
From Coq Require Import List.
Import ListNotations Bell429 LeftLanguage429.
Open Scope list_scope.
Open Scope sym_scope.
Module WordOrbit429.
Definition words := (list Sym * list Sym)%type.
Definition initial : words := ([],[1;1]).
Definition config (s:words) := GateBlank429.checkpoint (fst s) (snd s).
(** Strip only the far-end zeros. The infinite half-tape is unchanged. *)
Fixpoint trim w : list Sym :=
  match w with [] => [] | x::xs =>
    match trim xs with [] => match x with S0=>[] | S1=>[S1] end | vs => x::vs end end.
Lemma trim_ok w : trim w *> 0inf = w *> 0inf.
Proof. induction w as [|x w IH]; [reflexivity|]. cbn [trim]. destruct (trim w) eqn:E.
  - cbn in IH. destruct x; cbn [Str_app]; rewrite <- IH; [apply const_unfold|reflexivity].
  - cbn [Str_app]; now rewrite <-IH.
Qed.
Definition round (s:words) : option words :=
  let '(u,w) := s in
  let '(p,q) := RightExec429.right_words (1::w) in
  match LeftExec429.left_words ML (p ++ (0::u)) with
  | None => None
  | Some (y,v) => Some (trim y,trim (v ++ q))
  end.

Theorem round_spec s : match round s with
  | None => halts src_tm (config s)
  | Some t => config s -[src_tm]->+ config t
  end.
Proof.
  destruct s as [u w]. unfold round.
  pose proof (RightExec429.right_words_spec (1::w) (0 >> (u *> 0inf))) as right.
  destruct (RightExec429.right_words (1::w)) as [p q] eqn:R.
  pose proof (LeftExec429.left_words_spec ML (p ++ (0::u))) as left.
  destruct (LeftExec429.left_words ML (p ++ (0::u))) as [[y v]|].
  - pose proof (LeftOutput429.emit_correct _ _ _ left (q *> 0inf)) as L.
    cbn [LeftOutput429.denotation at_left] in L. rewrite Str_app_assoc in L.
    change (config (u,w) -[src_tm]->+ config (trim y,trim (v++q))).
    eapply progress_evstep_trans; [exact right|].
    unfold config, GateBlank429.checkpoint; cbn [fst snd].
    rewrite !trim_ok, Str_app_assoc. exact (before_path _ _ L).
  - pose proof (LeftOutput429.emit_correct _ _ _ left (q *> 0inf)) as L.
    destruct L as [z [B H]]. rewrite Str_app_assoc in B.
    eapply evstep_halts; [apply progress_evstep; exact right|].
    eapply evstep_halts; [exact (before_path _ _ B)|apply halted_halts,H].
Qed.

Theorem original_iff_word_orbit : halts tm c0 <-> iter_halts round initial.
Proof.
  assert (H : halts tm c0 <-> halts src_tm (B;;tape0)).
  { split; [|exact halts_iso]. intro stop; apply flip_halts in stop.
    change (flip_conf c0) with (A;;tape0) in stop.
    exact (perm_halts _ _ _ A tape0 Progress429.perm_back stop). }
  rewrite H, (halts_evstep_iff _ _ _ (without_counter _ _ _ _ GateBlank429.startup)).
  change (halts src_tm (config initial) <-> iter_halts round initial).
  eapply (halts_iff src_tm words initial round config (fun _ => True)).
  - intros s _. pose proof (round_spec s) as P. destruct (round s); auto.
  - exact I.
Qed.

Fixpoint iterate n s := match n with
  | O => Some s
  | S k => match round s with None => None | Some t => iterate k t end
  end.
Lemma finite_stop s : iter_halts round s <-> exists n, iterate n s=None.
Proof.
  split.
  - induction 1 as [s N|s t R _ [k K]].
    + exists 1%nat. cbn [iterate]; now rewrite N.
    + exists (S k). cbn [iterate]; now rewrite R.
  - intros [n N]. revert s N. induction n; intros s N; cbn [iterate] in N; [discriminate|].
    destruct (round s) as [v|] eqn:E; [eapply iter_halts_S; [apply E|apply IHn,N]|constructor; exact E].
Qed.
Corollary blank_iff_finite_words : halts tm c0 <-> exists n, iterate n initial = None.
Proof. rewrite original_iff_word_orbit; apply finite_stop. Qed.

Example first_turn : iterate 1 initial = Some ([1],[0;1]).
Proof. reflexivity. Qed.
Example fifth_turn : iterate 5 initial = Some ([0;1;1;0;1;1;0;1],[0;1]).
Proof. reflexivity. Qed.

Theorem closed_word_family (P:words->Prop) : P initial ->
  (forall s, P s -> exists t, round s = Some t /\ P t) -> ~halts tm c0.
Proof.
  intros P0 closed H. apply original_iff_word_orbit in H.
  revert P0. induction H as [s S|s t S _ IH]; intro good;
    destruct (closed s good) as [v [E V]].
  - congruence.
  - rewrite E in S. inversion S; subst. exact (IH V).
Qed.
End WordOrbit429.
Print Assumptions WordOrbit429.original_iff_word_orbit.
