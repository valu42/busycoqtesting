(** A local configuration at which the two machines make different decisions. *)
From BusyCoq Require Import Individual62 Line429Engine Line429Score Line429Sibling.
From Coq Require Import List NArith Lia.
Import ListNotations Bell429 Score429.
Open Scope sym_scope.
Module Cut429.
Fixpoint pieces (xs : list nat) (s : FastState) :=
  match xs with [] => Some s | k::ks =>
    match run_pow k s with Some t => pieces ks t | None => None end end.
Lemma pieces_sound xs : forall s t, pieces xs s = Some t ->
  fs_denote s -[src_tm]->* fs_denote t.
Proof.
  induction xs as [|k ks IH]; intros s t H; cbn [pieces] in H.
  - inversion H; constructor.
  - pose proof (run_pow_spec k s) as P. destruct (run_pow k s) as [u|]; [|discriminate].
    eapply evstep_trans; [exact P|apply IH, H].
Qed.
Definition to_original (c : Q*tape) := let '(q,t) := flip_conf c in (permState q,t).
Lemma from_blank s : (B;;tape0) -[src_tm]->* fs_denote s -> c0 -[tm]->* to_original (fs_denote s).
Proof.
  intro H. destruct (evstep_multistep _ _ _ H) as [n run]. apply flip_multistep in run.
  change (flip_conf (B;;tape0)) with (B;;tape0) in run. unfold to_original.
  destruct (flip_conf (fs_denote s)) as [q t]. apply multistep_evstep_iff.
  exists n; exact (perm_multistep _ _ _ perm_src _ _ _ _ _ run).
Qed.
Fixpoint prefix (w : list Sym) (l : Runs) : bool :=
  match w with [] => true | b::w' =>
    let '(v,t) := runs_pop l in
    match b,v with S0,S0 | S1,S1 => prefix w' t | _,_ => false end end.
Lemma prefix_sound w l : prefix w l = true -> exists t, runs_denote l = w *> t.
Proof.
  revert l. induction w as [|b w IH]; intros l; [intros _; exists (runs_denote l); reflexivity|].
  cbn [prefix]. pose proof (runs_pop_spec l) as P. destruct (runs_pop l) as [v s]; cbn [fst snd] in P.
  destruct b,v; try discriminate; intros H; destruct (IH _ H) as [t E]; exists t; rewrite P,E; reflexivity.
Qed.
Definition check_cut (s : FastState) := match fs_mode s with
  | RAW C L => prefix [0;1;1;1;0] (fs_L s) | _ => false end.
Definition cut (l r : side) := (B;; (l,S0,[1;1;1;0] *> r)).
Lemma cut_sound s : check_cut s = true -> exists l r, to_original (fs_denote s) = cut l r.
Proof.
  destruct s as [l rt m]. destruct m as [| | |q d]; try discriminate.
  destruct q,d; try discriminate. cbn [check_cut fs_mode fs_L]; intros H.
  apply prefix_sound in H. destruct H as [r P]. exists (rt_denote rt), r.
  unfold to_original, fs_denote; cbn [fs_L fs_R fs_mode]. rewrite P. reflexivity.
Qed.
Definition itinerary : list nat := [16;12;11;8;6;3;2;0]%nat.
Definition cut_ones : N := 4324962677667916309987851332511507720838844766284084744820185366141879566%N.
Lemma witnessed :
  match pieces itinerary initFastB with
  | Some s => andb (check_cut s) (N.eqb (config_count s) cut_ones)
  | None => false end = true.
Proof. vm_check_eq. Qed.
Lemma original_score c n : sigma_score c n -> sigma_score (to_original c) n.
Proof.
  intros H; destruct H as [q l b r a nb z Hl Hb Hr].
  replace (a+nb+z)%nat with (z+nb+a)%nat by lia.
  constructor; [exact Hr|exact Hb|exact Hl].
Qed.
Theorem reachable_cut : exists l r,
  c0 -[tm]->* cut l r /\ sigma_score (cut l r) (N.to_nat cut_ones).
Proof.
  pose proof witnessed as H; destruct (pieces itinerary initFastB) as [s|] eqn:P; [|discriminate].
  apply Bool.andb_true_iff in H. destruct H as [H M]. destruct (cut_sound _ H) as [l [r E]].
  exists l,r. rewrite <- E. split.
  - apply from_blank. rewrite <- initFastB_denote. exact (pieces_sound _ _ _ P).
  - apply N.eqb_eq in M. rewrite <- M. apply original_score, config_correct.
Qed.
(** The word is B:01110 in the supplied orientation. *)
Lemma target_crosses l r : cut l r -[tm]->> 5 / ([0;0;0;0;1] *> l) {{A}}> r.
Proof. unfold cut. do 5 (eapply multistep_S; [prove_step|simpl_tape]). apply multistep_0. Qed.
Lemma sibling_stops l r : exists c, cut l r -[Sibling429.machine279]->> 3 / c /\ halted Sibling429.machine279 c.
Proof. eexists. split; [do 3 (eapply multistep_S; [prove_step|simpl_tape]); apply multistep_0|reflexivity]. Qed.
Theorem reachable_sibling_guard : exists x, Sibling429.guard279 x = true /\
  c0 -[tm]->* Sibling429.embed Sibling429.state429 x.
Proof.
  destruct reachable_cut as [l [r [reach score]]].
  exists (Sibling429.go_right,(S0 >> S1 >> l,S1,S1 >> S0 >> r)). split; [reflexivity|].
  eapply evstep_trans; [exact reach|]. unfold cut,Sibling429.embed.
  do 2 step. apply evstep_refl.
Qed.
End Cut429.
Print Assumptions Cut429.reachable_cut.
Print Assumptions Cut429.target_crosses.
Print Assumptions Cut429.reachable_sibling_guard.
