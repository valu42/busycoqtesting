(** A two-way traversal of arbitrary 01/011 token lists in line 429's literal table. *)
From BusyCoq Require Import Individual62 Line429Engine Line429Cut.
From Coq Require Import List Arith Lia.
Import ListNotations Bell429 Cut429.
Open Scope sym_scope.
Module Recovery429.
Inductive token := short | long.
Fixpoint incoming (w:list token) : list Sym :=
  match w with []=>[] | short::v=>[0;1]++incoming v | long::v=>[0;1;1]++incoming v end.
Fixpoint outgoing (w:list token) : list Sym :=
  match w with []=>[] | short::v=>[1;0]++outgoing v | long::v=>[1;0;1]++outgoing v end.
Ltac micro := eapply multistep_S; [prove_step|simpl_tape].

Lemma turnaround w : forall l r,
  l {{A}}> incoming w *> [0;1;1;1] *> r -[tm]->> (10+10*length w)%nat /
  l {{A}}> [1;1] *> outgoing w *> [1;0] *> r.
Proof.
  induction w as [|t v IH]; intros l r.
  - cbn [incoming outgoing length]. do 10 micro. constructor.
  - destruct t; cbn [incoming outgoing length].
    + replace (10+10*S (length v))%nat with (2+(10+10*length v)+8)%nat by lia.
      eapply multistep_trans; [eapply multistep_trans; [do 2 micro; apply multistep_0|apply IH]|].
      do 8 micro; apply multistep_0.
    + replace (10+10*S (length v))%nat with (5+(10+10*length v)+5)%nat by lia.
      eapply multistep_trans; [eapply multistep_trans; [do 5 micro; apply multistep_0|apply IH]|].
      do 5 micro; apply multistep_0.
Qed.

Theorem triple w l r :
  l {{B}}> [0;1;1;1;0;1;1] *> incoming w *> [0;1;1;1] *> r
  -[tm]->> (45+10*length w)%nat /
  l <{{E}} [1;1;0;1;1;0;1;1;0] *> outgoing w *> [1;0] *> r.
Proof.
  replace (45+10*length w)%nat with (17+(10+10*length w)+18)%nat by lia.
  eapply multistep_trans; [eapply multistep_trans; [do 17 micro; apply multistep_0|apply turnaround]|].
  do 18 micro; apply multistep_0.
Qed.
Theorem double w l r :
  l {{B}}> [0;1;1;0;1;1] *> incoming w *> [0;1;1;1] *> r
  -[tm]->> (47+10*length w)%nat /
  l <{{A}} [1;1;0;1;0;1;1;0] *> outgoing w *> [1;0] *> r.
Proof.
  replace (47+10*length w)%nat with (16+(10+10*length w)+21)%nat by lia.
  eapply multistep_trans; [eapply multistep_trans; [do 16 micro; apply multistep_0|apply turnaround]|].
  do 21 micro; apply multistep_0.
Qed.
Theorem quadruple w l r :
  l {{B}}> [0;1;1;1;1;0;1;1] *> incoming w *> [0;1;1;1] *> r
  -[tm]->> (47+10*length w)%nat /
  l <{{C}} [0;1;1;0;1;1;0;1;1;0] *> outgoing w *> [1;0] *> r.
Proof.
  replace (47+10*length w)%nat with (18+(10+10*length w)+19)%nat by lia.
  eapply multistep_trans; [eapply multistep_trans; [do 18 micro; apply multistep_0|apply turnaround]|].
  do 19 micro; apply multistep_0.
Qed.
Definition actual_tokens := [long;short;short;short;short].
Definition actual_input := [0;1;1;1;0;1;1] ++ incoming actual_tokens ++ [0;1;1;1].
Definition check_recovery (s : FastState) := match fs_mode s with
  | RAW C L => prefix actual_input (fs_L s) | _ => false end.
Lemma observed :
  match pieces itinerary initFastB with Some s => check_recovery s | None => false end = true.
Proof. vm_check_eq. Qed.
Lemma check_recovery_sound s : check_recovery s = true ->
  exists l r, to_original (fs_denote s) = l {{B}}> actual_input *> r.
Proof.
  destruct s as [l rt m]. destruct m as [| | |q d]; try discriminate.
  destruct q,d; try discriminate. cbn [check_recovery fs_mode fs_L]; intros H.
  apply prefix_sound in H. destruct H as [r P]. exists (rt_denote rt),r.
  unfold to_original,fs_denote; cbn [fs_L fs_R fs_mode]; rewrite P; reflexivity.
Qed.
Theorem blank_recovery : exists l r,
  c0 -[tm]->* l {{B}}> actual_input *> r /\
  l {{B}}> actual_input *> r -[tm]->> 95 /
  l <{{E}} [1;1;0;1;1;0;1;1;0] *> outgoing actual_tokens *> [1;0] *> r.
Proof.
  pose proof observed as H; destruct (pieces itinerary initFastB) as [s|] eqn:P; [|discriminate].
  destruct (check_recovery_sound _ H) as [l [r E]]. exists l,r. split.
  - rewrite <- E. apply from_blank. rewrite <- initFastB_denote. exact (pieces_sound _ _ _ P).
  - exact (triple actual_tokens l r).
Qed.
Lemma realign w r :
  outgoing w *> [1;0] *> r = 1 >> (incoming w *> [0] *> r).
Proof.
  induction w as [|[|] v IH]; [reflexivity| |];
  change (outgoing v *> (1 >> 0 >> r) = 1 >> incoming v *> (0 >> r)) in IH;
  cbn [incoming outgoing]; simpl_tape; rewrite IH; reflexivity.
Qed.
Fixpoint forward_cost (w : list token) : nat :=
  match w with [] => 0%nat | short::v => (2+forward_cost v)%nat | long::v => (5+forward_cost v)%nat end.
Fixpoint forward_left (w : list token) (l : side) : side :=
  match w with [] => l | short::v => forward_left v ([1;1] *> l)
  | long::v => forward_left v ([0;0;1] *> l) end.
Lemma forward w : forall l r,
  l {{A}}> incoming w *> [0] *> r -[tm]->> (forward_cost w+1)%nat /
  (1 >> forward_left w l) {{B}}> r.
Proof.
  induction w as [|[|] v IH]; intros l r; cbn [incoming forward_left forward_cost].
  - do 1 micro; apply multistep_0.
  - replace (2+forward_cost v+1)%nat with (2+(forward_cost v+1))%nat by lia.
    eapply multistep_trans; [do 2 micro; apply multistep_0|apply IH].
  - replace (5+forward_cost v+1)%nat with (5+(forward_cost v+1))%nat by lia.
    eapply multistep_trans; [do 5 micro; apply multistep_0|apply IH].
Qed.
Lemma quintuple_core w l r : exists t,
  (0 >> l) {{F}}> [1;1;1;1;0;1;1] *> incoming w *> [0;1;1;1] *> r
  -[tm]->> (63+10*length w+forward_cost w)%nat / t {{B}}> r.
Proof.
  replace (63+10*length w+forward_cost w)%nat with
    (17+(10+10*length w)+35+(forward_cost w+1))%nat by lia.
  eexists.
  eapply multistep_trans; [eapply multistep_trans; [eapply multistep_trans;
    [do 17 micro; apply multistep_0 | apply turnaround] | rewrite realign; do 35 micro; apply multistep_0]
    | apply forward].
Qed.
Lemma erase_ones n : forall l r, exists l',
  (0 >> l) {{F}}> repeat S1 n *> r -[tm]->> n / (0 >> l') {{F}}> r.
Proof.
  induction n as [|n IH]; intros l r.
  - exists l; constructor.
  - destruct (IH (0 >> l) r) as [t T]. exists t.
    cbn [repeat]; micro; exact T.
Qed.
Theorem five_or_more_right n w l r : exists t,
  l {{B}}> [0;1] *> repeat S1 n *> [1;1;1;1;0;1;1] *> incoming w *> [0;1;1;1] *> r
  -[tm]->> (n+65+10*length w+forward_cost w)%nat / t {{B}}> r.
Proof.
  destruct (erase_ones n (1 >> l) ([1;1;1;1;0;1;1] *> incoming w *> [0;1;1;1] *> r)) as [v T].
  destruct (quintuple_core w v r) as [t P]. exists t.
  replace (n+65+10*length w+forward_cost w)%nat with (2+n+(63+10*length w+forward_cost w))%nat by lia.
  eapply multistep_trans; [eapply multistep_trans; [do 2 micro; apply multistep_0 | exact T] | exact P].
Qed.
Theorem no_ones_halts l r : exists c,
  l {{B}}> [0;0;1] *> r -[tm]->> 2 / c /\ halted tm c.
Proof. eexists. split; [do 2 micro; apply multistep_0|reflexivity]. Qed.
Theorem one l r :
  l {{B}}> [0;1;0;1] *> r -[tm]->> 9 / l <{{C}} [0;1;1;0] *> r.
Proof. do 9 micro; apply multistep_0. Qed.
Theorem five_or_more_halts n w l r : exists c,
  l {{B}}> [0;1] *> repeat S1 n *> [1;1;1;1;0;1;1] *> incoming w *> [0;1;1;1] *> [0;0;1] *> r
  -[tm]->> (n+67+10*length w+forward_cost w)%nat / c /\ halted tm c.
Proof.
  destruct (five_or_more_right n w l ([0;0;1] *> r)) as [t T].
  destruct (no_ones_halts t r) as [c [H D]]. exists c; split; [|exact D].
  replace (n+67+10*length w+forward_cost w)%nat with (n+65+10*length w+forward_cost w+2)%nat by lia.
  exact (multistep_trans _ _ _ _ _ _ T H).
Qed.
Lemma shift_ones n r : repeat S1 n *> (1 >> r) = 1 >> repeat S1 n *> r.
Proof. induction n as [|n IH]; cbn [repeat]; simpl_tape; [reflexivity|now rewrite IH]. Qed.
Lemma sweep_left n : forall l r,
  (repeat S1 n *> (0 >> l)) <{{E}} r -[tm]->> (n+1)%nat /
  l <{{A}} repeat S1 (S n) *> r.
Proof.
  induction n as [|n IH]; intros l r.
  - cbn [repeat]. micro; constructor.
  - cbn [repeat]. micro. specialize (IH l (1 >> r)).
    rewrite shift_ones in IH. exact IH.
Qed.
Definition actual_flank := repeat S1 1227 ++ [0;0].
Definition check_flank (s : FastState) :=
  match takeBitsRTapeAux actual_flank (fs_R s) with Some _ => true | None => false end.
Lemma observed_flank :
  match pieces itinerary initFastB with Some s => andb (check_recovery s) (check_flank s) | None => false end = true.
Proof. vm_check_eq. Qed.
Lemma checks_sound s : check_recovery s = true -> check_flank s = true -> exists l r,
  to_original (fs_denote s) = (actual_flank *> l) {{B}}> actual_input *> r.
Proof.
  destruct s as [u rt m]. destruct m as [| | |q d]; try discriminate.
  destruct q,d; try discriminate. cbn [check_recovery fs_mode fs_L]; intros H.
  apply prefix_sound in H. destruct H as [r P].
  unfold check_flank; cbn [fs_R].
  destruct (takeBitsRTapeAux actual_flank rt) as [v|] eqn:T; [intros _|discriminate].
  exists (rt_denote v),r. unfold to_original,fs_denote; cbn [fs_L fs_R fs_mode].
  rewrite P,(takeBitsRTapeAux_spec _ _ _ T); reflexivity.
Qed.
Theorem blank_left_sweep : exists l r,
  c0 -[tm]->* (actual_flank *> l) {{B}}> actual_input *> r /\
  (actual_flank *> l) {{B}}> actual_input *> r -[tm]->> 1323 /
  (0 >> l) <{{A}} repeat S1 1228 *> [1;1;0;1;1;0;1;1;0] *> outgoing actual_tokens *> [1;0] *> r.
Proof.
  pose proof observed_flank as H; destruct (pieces itinerary initFastB) as [s|] eqn:P; [|discriminate].
  apply Bool.andb_true_iff in H; destruct H as [H G].
  destruct (checks_sound _ H G) as [l [r E]]. exists l,r. split.
  - rewrite <- E. apply from_blank. rewrite <- initFastB_denote. exact (pieces_sound _ _ _ P).
  - change 1323%nat with (95+(1227+1))%nat. eapply multistep_trans.
    + exact (triple actual_tokens (actual_flank *> l) r).
    + unfold actual_flank. rewrite Str_app_assoc. exact (sweep_left 1227 (0 >> l) _).
Qed.
Lemma turn_into_C l r :
  (0 >> l) <{{A}} [1;1;1] *> r -[tm]->> 11 / l <{{C}} [0;1;1;0] *> r.
Proof. do 11 micro; apply multistep_0. Qed.
Lemma move_two_ones n r :
  repeat S1 (S n) *> (1 >> 1 >> r) = [1;1;1] *> repeat S1 n *> r.
Proof. cbn [repeat]; simpl_tape; do 2 rewrite shift_ones; reflexivity. Qed.
Theorem triple_left_flank n w l r :
  (repeat S1 n *> (0 >> 0 >> l)) {{B}}> [0;1;1;1;0;1;1] *> incoming w *> [0;1;1;1] *> r
  -[tm]->> (n+57+10*length w)%nat /
  l <{{C}} [0;1;1;0] *> repeat S1 n *> [0;1;1;0;1;1;0] *> outgoing w *> [1;0] *> r.
Proof.
  replace (n+57+10*length w)%nat with (45+10*length w+(n+1)+11)%nat by lia.
  eapply multistep_trans; [eapply multistep_trans; [apply triple|apply sweep_left]|].
  change ((0 >> l) <{{A}} repeat S1 (S n) *> (1 >> 1 >> ([0;1;1;0;1;1;0] *> outgoing w *> [1;0] *> r)) -[tm]->> 11 /
      l <{{C}} [0;1;1;0] *> repeat S1 n *> [0;1;1;0;1;1;0] *> outgoing w *> [1;0] *> r).
  rewrite move_two_ones. apply turn_into_C.
Qed.
Theorem blank_far_edge : exists l r,
  c0 -[tm]->* (actual_flank *> l) {{B}}> actual_input *> r /\
  (actual_flank *> l) {{B}}> actual_input *> r -[tm]->> 1334 /
  l <{{C}} [0;1;1;0] *> repeat S1 1227 *> [0;1;1;0;1;1;0] *> outgoing actual_tokens *> [1;0] *> r.
Proof.
  destruct blank_left_sweep as [l [r [H T]]]. exists l,r. split; [exact H|].
  unfold actual_flank; rewrite Str_app_assoc. exact (triple_left_flank 1227 actual_tokens l r).
Qed.
End Recovery429.
Print Assumptions Recovery429.triple.

Print Assumptions Recovery429.blank_recovery.

Print Assumptions Recovery429.five_or_more_halts.

Print Assumptions Recovery429.blank_left_sweep.

Print Assumptions Recovery429.blank_far_edge.
