(** A batch of accelerations followed by one literal transition. The raw-tape
    calculations strengthen the corresponding PR 93 lemmas to a single step. *)
From BusyCoq Require Import Individual62 Line429Engine.
From Coq Require Import List NArith.
Import ListNotations Bell429.
Open Scope sym_scope.
Module Progress429.
Lemma raw_tick l rt q d :
  match rawStep l rt q d with
  | Some s' => fs_denote (MkFastState l rt (RAW q d)) -[src_tm]-> fs_denote s'
  | None => halted src_tm (fs_denote (MkFastState l rt (RAW q d)))
  end.
Proof.
  destruct d; unfold rawStep; cbn [fs_denote fs_L fs_R fs_mode].
  - pose proof (runs_pop_spec l) as Hp.
    destruct (runs_pop l) as [b l']; cbn [fst snd] in Hp.
    rewrite Hp; cbn [hd tl].
    destruct (src_tm (q, b)) as [[[b' [|]] q']|] eqn:E.
    + cbn [fs_denote fs_L fs_R fs_mode].
      unfold rt_denote; cbn [r_raw d_front d_back r_tail].
      rewrite push_plug. change (N.to_nat 1) with 1%nat.
      cbn [sw_toList lpow app Str_app].
      exact (step_left E).
    + cbn [fs_denote fs_L fs_R fs_mode].
      rewrite runs_push_spec. change (N.to_nat 1) with 1%nat.
      cbn [sw_toList lpow app Str_app].
      exact (step_right E).
    + exact E.
  - pose proof (popBitRTape_spec rt) as Hp.
    destruct (popBitRTape rt) as [b rt']; cbn [fst snd] in Hp.
    rewrite Hp; cbn [hd tl].
    destruct (src_tm (q, b)) as [[[b' [|]] q']|] eqn:E.
    + cbn [fs_denote fs_L fs_R fs_mode].
      unfold rt_denote; cbn [r_raw d_front d_back r_tail].
      rewrite push_plug. change (N.to_nat 1) with 1%nat.
      cbn [sw_toList lpow app Str_app].
      exact (step_left E).
    + cbn [fs_denote fs_L fs_R fs_mode].
      rewrite runs_push_spec. change (N.to_nat 1) with 1%nat.
      cbn [sw_toList lpow app Str_app].
      exact (step_right E).
    + exact E.
Qed.

Lemma literal_tick l rt m :
  match toRawAndStep l rt m with
  | Some s' => fs_denote (MkFastState l rt m) -[src_tm]-> fs_denote s'
  | None => halted src_tm (fs_denote (MkFastState l rt m))
  end.
Proof.
  destruct m as [| | | q d]; unfold toRawAndStep.
  - pose proof (raw_tick l (MkRTape (runs_push (SW_raw [0; 1; 0; 0]) 1 (r_raw rt)) (d_front rt) (d_back rt) (r_tail rt)) A R) as H.
    replace (fs_denote (MkFastState l (MkRTape (runs_push (SW_raw [0; 1; 0; 0]) 1 (r_raw rt)) (d_front rt) (d_back rt) (r_tail rt)) (RAW A R)))
      with (fs_denote (MkFastState l rt MR)) in H.
    + exact H.
    + cbn [fs_denote fs_L fs_R fs_mode]. unfold CfgR, rt_denote; cbn [r_raw d_front d_back r_tail].
      rewrite push_plug. change (N.to_nat 1) with 1%nat. cbn [sw_toList lpow app Str_app]. reflexivity.
  - pose proof (raw_tick l (MkRTape (runs_push (SW_raw [1]) 1 (r_raw rt)) (d_front rt) (d_back rt) (r_tail rt)) B L) as H.
    replace (fs_denote (MkFastState l (MkRTape (runs_push (SW_raw [1]) 1 (r_raw rt)) (d_front rt) (d_back rt) (r_tail rt)) (RAW B L)))
      with (fs_denote (MkFastState l rt ML)) in H.
    + exact H.
    + cbn [fs_denote fs_L fs_R fs_mode]. unfold CfgL, rt_denote; cbn [r_raw d_front d_back r_tail].
      rewrite push_plug. change (N.to_nat 1) with 1%nat. cbn [sw_toList lpow app Str_app]. reflexivity.
  - pose proof (raw_tick l (MkRTape (runs_push (SW_raw [1; 0; 0]) 1 (r_raw rt)) (d_front rt) (d_back rt) (r_tail rt)) C L) as H.
    replace (fs_denote (MkFastState l (MkRTape (runs_push (SW_raw [1; 0; 0]) 1 (r_raw rt)) (d_front rt) (d_back rt) (r_tail rt)) (RAW C L)))
      with (fs_denote (MkFastState l rt MJ)) in H.
    + exact H.
    + cbn [fs_denote fs_L fs_R fs_mode]. unfold CfgJ, rt_denote; cbn [r_raw d_front d_back r_tail].
      rewrite push_plug. change (N.to_nat 1) with 1%nat. cbn [sw_toList lpow app Str_app]. reflexivity.
  - apply raw_tick.
Qed.

Definition batch (k:nat) (s:FastState) : option FastState :=
  match run_pow k s with
  | None => None
  | Some (MkFastState l rt m) => toRawAndStep l rt m end.
Lemma batch_spec k s : match batch k s with
  | Some t => fs_denote s -[src_tm]->+ fs_denote t
  | None => halts src_tm (fs_denote s) end.
Proof.
  pose proof (run_pow_spec k s) as H. unfold batch.
  destruct (run_pow k s) as [[l rt m]|]; [|exact H].
  pose proof (literal_tick l rt m) as T. destruct (toRawAndStep l rt m) as [t|].
  - eapply evstep_progress_trans; [exact H|apply progress_base; exact T].
  - eapply evstep_halts; [exact H|apply halted_halts; exact T].
Qed.
Definition to_reflected q := match q with
 | A=>B | B=>C | C=>D | D=>F | E=>A | F=>E end.
Lemma perm_back : Perm (flip tm) src_tm to_reflected.
Proof.
  split.
  - intros q b H; destruct q,b; cbv in H |- *; try discriminate; reflexivity.
  - intros q b w d t H; destruct q,b; cbv in H |- *; inversion H; subst; reflexivity.
Qed.
Theorem complete k : halts tm c0 <-> iter_halts (batch k) initFastB.
Proof.
  assert (I : halts tm c0 <-> halts src_tm (fs_denote initFastB)).
  { rewrite initFastB_denote. split; [|exact halts_iso]. intro H.
    apply flip_halts in H. change (flip_conf c0) with (A;;tape0) in H.
    exact (perm_halts _ _ _ A tape0 perm_back H). }
  rewrite I. eapply (halts_iff src_tm FastState initFastB (batch k) fs_denote (fun _ => True)).
  - intros s _. pose proof (batch_spec k s) as H. destruct (batch k s); auto.
  - exact Logic.I.
Qed.
Theorem closed_family k (safe : FastState -> Prop) : safe initFastB ->
  (forall s, safe s -> exists t, batch k s = Some t /\ safe t) -> ~halts tm c0.
Proof.
  intros initial closed H. apply (proj1 (complete k)) in H.
  revert initial. induction H as [s stop|s t move later IH]; intro good;
    destruct (closed s good) as [u [Hu Hgood]].
  - congruence.
  - rewrite move in Hu. inversion Hu; subst. exact (IH Hgood).
Qed.
End Progress429.
Print Assumptions Progress429.closed_family.
