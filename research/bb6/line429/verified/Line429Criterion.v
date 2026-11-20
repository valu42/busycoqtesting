From BusyCoq Require Import Individual62 Line429Engine Line429Progress.
From BusyCoq Require Import Line429Returns.
From BusyCoq Require Import Line429RightSweep.
From Coq Require Import List Lia Wf_nat.
Import ListNotations Bell429 Returns429.
Open Scope list_scope.
Open Scope sym_scope.

Module Criterion429.
Definition supported (c : Q * tape) :=
  let '(_, (l, _, r)) := c in finite l /\ finite r.
Lemma finite_push b r : finite r -> finite (b >> r).
Proof. intros [w ->]. exists (b :: w); reflexivity. Qed.
Lemma finite_tl r : finite r -> finite (Streams.tl r).
Proof. destruct r as [b r]. apply finite_rest. Qed.
Lemma finite_full r : finite (Streams.tl r) -> finite r.
Proof. destruct r as [b r]. apply finite_push. Qed.
Lemma step_support tm c d : c -[tm]-> d -> supported c -> supported d.
Proof. destruct 1; cbn; intros [Hl Hr]; split; auto using finite_push, finite_tl. Qed.
Lemma path_support tm c d : c -[tm]->* d -> supported c -> supported d.
Proof. induction 1; eauto using step_support. Qed.

Inductive hazard : Q*tape -> Prop :=
| hazard_ML x r : hazard (CfgL (0 >> 0 >> 0 >> 1 >> x) r)
| hazard_MJ x r : hazard (CfgJ (0 >> 0 >> 1 >> x) r).

Lemma read_badML l : badML l \/ ~badML l.
Proof.
  destruct l as [[|] [[|] [[|] [[|] x]]]];
    first [left; exists x; reflexivity | right; intros [z E]; discriminate E].
Qed.
Lemma read_badMJ l : badMJ l \/ ~badMJ l.
Proof.
  destruct l as [[|] [[|] [[|] x]]];
    first [left; exists x; reflexivity | right; intros [z E]; discriminate E].
Qed.

Lemma landmark_alternative c : destination c -> supported c -> hazard c \/ escape c.
Proof.
  destruct 1 as [l r|l r|l r]; intros [Hl Hr].
  - destruct (read_badML l) as [[x ->]|safe].
    + left; constructor.
    + right; apply ML_escape; auto using finite_full.
  - destruct (read_badMJ l) as [[x ->]|safe].
    + left; constructor.
    + right; apply MJ_escape; auto using finite_full.
  - right. apply finite_full in Hr. destruct Hr as [w ->].
    destruct (right_finite w) as [p [q [[|k] [size path]]]]; [lia|].
    exists (CfgL (p *> l) (q *> 0inf)); split; [eapply multistep_progress; apply path|constructor].
Qed.

Definition reaches_hazard c := exists d, c -[src_tm]->* d /\ hazard d.

Theorem halt_from_landmark c : destination c -> supported c ->
  (halts src_tm c <-> reaches_hazard c).
Proof.
  intros landmark support. split.
  - intros [k H]. revert c H landmark support.
    induction k using lt_wf_ind; intros c stop landmark support.
    destruct (landmark_alternative _ landmark support) as [bad | [d [run landmarkD]]].
    + exists c; split; [constructor|exact bad].
    + pose proof (progress_evstep _ _ _ run) as path.
      pose proof (path_support _ _ _ path support) as supportD.
      destruct (progress_multistep _ _ _ run) as [n count].
      pose proof (within_halt _ _ _ _ _ stop count) as le.
      pose proof (preceeds_halt _ _ _ _ _ stop count le) as stopD.
      destruct (H (k - S n)%nat ltac:(lia) d stopD landmarkD supportD) as [e [rest bad]].
      exists e; split; [eapply evstep_trans; eauto|exact bad].
  - intros [d [path bad]]. eapply evstep_halts; [exact path|].
    destruct bad as [x r|x r]; [exists 3%nat; apply ML_halts|exists 2%nat; apply MJ_halts].
Qed.

Lemma startup : (B;;tape0) -[src_tm]-> CfgJ 0inf 0inf.
Proof.
  replace (CfgJ 0inf 0inf) with (C;;move_left (0inf {{S1}} 0inf)).
  - apply step_left; reflexivity.
  - unfold CfgJ; cbn [Str_app move_left Streams.hd Streams.tl]; solve_const0_eq.
Qed.
Lemma start_support : supported (CfgJ 0inf 0inf).
Proof. split; [exists (@nil Sym)|exists [S1;S0;S0]]; reflexivity. Qed.

Theorem blank_halt_iff :
  halts tm c0 <-> reaches_hazard (B;;tape0).
Proof.
  split.
  - intro H. apply flip_halts in H. change (flip_conf c0) with (A;;tape0) in H.
    pose proof (perm_halts _ _ _ A tape0 Progress429.perm_back H) as h.
    apply (proj1 (halts_step_iff _ _ _ startup)) in h.
    apply (proj1 (halt_from_landmark _ (at_MJ _ _) start_support)) in h.
    destruct h as [d [run bad]]. exists d; split; [eapply evstep_step; eauto using startup|exact bad].
  - intros [d [path bad]]. apply halts_iso. eapply evstep_halts; [exact path|].
    destruct bad as [x r|x r]; [exists 3%nat; apply ML_halts|exists 2%nat; apply MJ_halts].
Qed.
End Criterion429.
Print Assumptions Criterion429.blank_halt_iff.
