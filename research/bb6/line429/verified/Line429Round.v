(* Composing the left-language parser with the word written by a right sweep.
   The input and output half-tapes are nearest-symbol first. *)
From BusyCoq Require Import Individual62 Line429Engine.
From BusyCoq Require Import Line429RightSweep Line429LeftLanguage.
From Coq Require Import List Arith Lia.
Import ListNotations Bell429 LeftLanguage429.
Open Scope list_scope.
Open Scope sym_scope.

Module Round429.
Definition choose (b : bool) (o : outcome) := if b then o else Turn.
Lemma ML0 y o : accepts MJ y o -> accepts ML (0 >> y) o.
Proof.
  intro H; remember MJ as q eqn:E; induction H; inversion E; subst;
    cbn [Str_app]; first [apply L01; assumption | apply Lrun0; assumption |
      apply Lbad | apply L0000 | apply Lrun1].
Qed.
Definition layer a b s y := (exists z, s = 1 >> z) /\ forall o,
  accepts MJ y o -> accepts ML s (choose a o) /\ accepts MJ s (choose b o).
Lemma initial y : layer true true (1 >> 0 >> y) y.
Proof.
  split; [eexists; reflexivity|]. intros o h; split; [apply L10|apply J1,ML0]; exact h.
Qed.
Lemma write_one a b s y : layer a b s y -> layer false a (1 >> s) y.
Proof.
  intros [[z ->] H]; split; [eexists; reflexivity|]. intros o hy.
  split; [apply L11|apply J1,(H o hy)].
Qed.
Lemma write_10 a b s y : layer a b s y -> layer b b ([1;0] *> s) y.
Proof.
  intros [_ H]; split; [eexists; reflexivity|]. intros o hy.
  split; [apply L10|apply J1,ML0]; apply (H o hy).
Qed.
Lemma write_101 a b s y : layer a b s y -> layer a a ([1;0;1] *> s) y.
Proof.
  intros [_ H]; split; [eexists; reflexivity|]. intros o hy.
  split; [apply L10,J1|apply J1,L01]; apply (H o hy).
Qed.

Lemma written_effect p : Generated p -> forall a b, exists u v, forall s y,
  layer a b s y -> layer u v (p *> s) y.
Proof.
  induction 1 as [|p G IH|p G IH|p G IH]; intros a b.
  - exists a,b; cbn; auto.
  - destruct (IH false a) as [u [v P]]. exists u,v. intros s y H.
    rewrite Str_app_assoc; apply P,(write_one _ _ _ _ H).
  - destruct (IH a a) as [u [v P]]. exists u,v. intros s y H.
    rewrite Str_app_assoc; apply P,(write_101 _ _ _ _ H).
  - destruct (IH b b) as [u [v P]]. exists u,v. intros s y H.
    rewrite Str_app_assoc; apply P,(write_10 _ _ _ _ H).
Qed.

Lemma written_frozen p : Generated p -> forall s y, layer false false s y ->
  layer false false (p *> s) y.
Proof.
  induction 1; intros s y Hs; [exact Hs|..]; rewrite Str_app_assoc; apply IHGenerated;
    first [apply (write_one _ _ _ _ Hs)|apply (write_101 _ _ _ _ Hs)|apply (write_10 _ _ _ _ Hs)].
Qed.

(* For any right half-tape, one Boolean selects between an unconditional turn and
   forwarding the old left suffix's exact MJ classification. The same output
   words, number of moves, and Boolean apply to every left suffix. *)
Theorem round_factor w :
  exists (gate : bool) (p q : list Sym) (t : nat),
    (4 <= t <= 4 * length w + 4)%nat /\
    forall y, let left := p *> (1 >> 0 >> y) in
      AR (0 >> y) (1 >> (w *> 0inf)) -[src_tm]->> t / CfgL left (q *> 0inf) /\
      forall o, accepts MJ y o -> first (choose gate o) (CfgL left (q *> 0inf)).
Proof.
  destruct (right_finite_tokens w) as [p [q [t [G [time path]]]]].
  destruct (written_effect p G true true) as [a [b carry]].
  exists a,p,q,(1+t)%nat. split.
  { destruct time as [lo hi]. split; [apply le_n_S,lo|].
    replace (4 * length w + 4)%nat with (S (4 * length w + 3)) by lia.
    apply le_n_S,hi. }
  intro y; split; [eapply multistep_trans; [apply ar_one|apply path]|].
  intros o Hy. destruct (carry _ _ (initial y)) as [_ classify].
  exact (accepts_first ML _ _ (proj1 (classify o Hy)) _).
Qed.

Definition robust s := layer false false s 0inf.
Lemma robust3 s : robust ([1;1;1] *> s).
Proof. split; [eexists; reflexivity|]. intros o _. split; [apply L11|apply J1,L11]. Qed.
Lemma robust5 s : robust ([1;0;1;1;1] *> s).
Proof. split; [eexists; reflexivity|]. intros o _. split; [apply L10,J1,L11|apply J1,L01,L11]. Qed.
Lemma robust_returns s w : robust s -> exists y v, AR s (w *> 0inf) -[src_tm]->* AR (0 >> y) (1 >> v).
Proof.
  intro safe. destruct (right_finite_tokens w) as [p [q [t [G [_ sweep]]]]].
  destruct (written_frozen p G _ _ safe) as [_ classify].
  assert (H0 : accepts MJ 0inf Turn).
  { replace 0inf with ([0;0;0] *> 0inf) at 1 by (cbn; repeat rewrite <-const_unfold; reflexivity).
    apply J000. }
  destruct (classify _ H0) as [L _]. cbn [choose] in L.
  destruct (accepts_turn_shape _ _ L (q *> 0inf)) as [y [v back]].
  exists y,v. eapply ev_trans; [eapply without_counter,sweep|]. apply before_path,back.
Qed.

(* Two right-hand prefixes force another turn, regardless of the left half. *)
Theorem reset111 l w :
  exists y v, AR l ([1;1;1] *> w *> 0inf) -[src_tm]->+ AR (0 >> y) (1 >> v).
Proof.
  destruct (robust_returns ([1;1;1] *> l) w (robust3 l)) as [y [v H]].
  exists y,v. eapply progress_intro; [unfold AR; prove_step|].
  eapply ev_trans; [eapply without_counter,ar_one|].
  eapply ev_trans; [eapply without_counter,ar_one|exact H].
Qed.
Theorem reset11010 l w :
  exists y v, AR l ([1;1;0;1;0] *> w *> 0inf) -[src_tm]->+ AR (0 >> y) (1 >> v).
Proof.
  destruct (robust_returns ([1;0;1;1;1] *> l) w (robust5 l)) as [y [v H]].
  exists y,v. eapply progress_intro; [unfold AR; prove_step|].
  eapply ev_trans; [eapply without_counter,ar_one|].
  eapply ev_trans; [eapply without_counter,ar_010|exact H].
Qed.
(* The complementary open gate forwards Y unchanged after exactly eight moves. *)
Lemma open100 y r :
  AR (0 >> y) ([1;0;0] *> r) -[src_tm]->> 8 / CfgJ y (1 >> r).
Proof. unfold AR,CfgJ; simpl_tape.
  do 8 (eapply multistep_S; [prove_step|simpl_tape]); constructor. Qed.
Corollary halt100 x r : halts_in src_tm (AR ([0;0;0;1] *> x) ([1;0;0] *> r)) 10.
Proof.
  eexists; split.
  - unfold AR; simpl_tape. do 10 (eapply multistep_S; [prove_step|simpl_tape]); constructor.
  - reflexivity.
Qed.
End Round429.
Print Assumptions Round429.round_factor.
Print Assumptions Round429.reset111.
Print Assumptions Round429.reset11010.
Print Assumptions Round429.open100.
