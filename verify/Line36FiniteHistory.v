(** Complete physical interpretation of an accepted finite-history edge. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36History Line36HistoryParse Line36Word Line36HistoryEncoding
  Line36Tiles Line36Left Line36LeftStep Line36Charge Line36Front.
Import ListNotations L36History L36HistoryParse L36Tiles L36Left L36LeftStep.
Local Open Scope nat_scope.

Module L36FiniteHistory.
Lemma observed_image w d g out : observed w d = (g,out) ->
  known_image w d = out /\ fst (mark36 w d) = g.
Proof. unfold observed,known_image; destruct (mark36 w d); congruence || intros [= <- <-]; auto. Qed.
Lemma prepare_word36 s hist :
  x (prepare s hist) = length (representative s hist) /\
  full (prepare s hist) = representative s hist ++ halo_word (halo s).
Proof. unfold prepare; destruct (scan _ _ _ _); reflexivity || auto. Qed.
Lemma firstn_prefix36 {T} (xs ys:list T) :
  firstn (length xs) (xs++ys) = xs.
Proof. rewrite firstn_app, firstn_all, Nat.sub_diag, firstn_O, app_nil_r. reflexivity. Qed.

Theorem finite_history_semantics f d (Valid:fvalid f)
  (Pieces:5<=length (fchoices f)) (Small:d<=28) :
  exists hist, hist<16 /\ forall e, L36LeftStep.step (fstate f) hist d = Some e ->
    exists cs exposed,
    let dest := target e in
    let p := parsed_front (phase dest) cs (partial_choice dest) (partial_len dest) in
    let old := fprefix f in let h := firstn 3 (ftail f) in
      observed (old++h) d = (phase_guard (fphase f),p++exposed) /\
      phase dest = next (fphase f) /\
      kind dest = boundary 0 cs /\ last_choice dest = last cs false /\
      halo dest = encode_halo exposed /\ encode_halo exposed <> 8 /\
      In false p /\
      dx e = (Z.of_nat (length p)-Z.of_nat (length old))%Z /\
      charge e = checked_charge old h p exposed (length (guard36 (phase_guard (fphase f)))) d.
Proof.
  destruct (concrete_history36 f Valid Pieces)
    as [actual [padded [a [b [c [ee [ff [hist [Fac [Hi [Bk [Cnt [Rep Hal]]]]]]]]]]]]].
  exists hist. split; [exact Hi|]. intros edge Step. cbn zeta.
  destruct Valid as [Hp [Hpart Htail]].
  set (ph:=fphase f) in *.
  set (k:=boundary 0 actual) in *.
  set (h:=firstn 3 (ftail f)) in *.
  set (common:=segments ph k [a;b;c;ee;ff] ++ fpart f) in *.
  set (pn:=next ph).
  assert (Hal3 : length h<=3) by (unfold h; rewrite length_firstn; lia).
  assert (Kf : fkind f = four_kind (next k)).
  { unfold fkind. rewrite Fac, <- fkind_start, boundary_app. reflexivity. }
  assert (Part : prefix (fpart f) (phase_pieces ph (four_kind (next k)) (foption f))).
  { unfold fpart. fold ph. rewrite Kf. unfold prefix. eexists. symmetry. apply firstn_skipn. }
  assert (Real : fprefix f = front ph actual ++ common).
  { unfold fprefix,fdata,front,common. fold ph. rewrite Fac,segments_app.
    unfold k. now repeat rewrite <- app_assoc. }
  assert (Rep2 : representative (fstate f) hist = front ph padded ++ common).
  { exact Rep. }
  pose proof (five_history_replacement ph actual padded k a b c ee ff (foption f)
                 (fpart f) h d Hp eq_refl (eq_sym Bk) Part Hal3 Small)
     as [local [A B]].
  change (five_tail ph k a b c ee ff (fpart f) h) with
    ((segments ph k [a;b;c;ee;ff]) ++ fpart f ++ h) in A,B.
  rewrite (app_assoc (segments ph k [a;b;c;ee;ff]) (fpart f) h) in A,B.
  fold common in A,B. fold pn in A,B.
  destruct (prepare_word36 (fstate f) hist) as [PX PF].
  set (ctx:=prepare (fstate f) hist) in *.
  assert (Sphase:phase (fstate f)=ph) by reflexivity.
  assert (O:observed (full ctx) d=(phase_guard ph,front pn padded++local)).
  { rewrite PF,Rep2,Hal. now rewrite <- app_assoc. }
  replace (piece_count (fkind f)) with (piece_count (kind (fstate f))) in Cnt by reflexivity.
  assert (X : x ctx = length (front ph padded ++ common)) by now rewrite PX,Rep2.
  destruct (transfer_edge (fstate f) ctx d edge actual padded local common
                Hp Bk Cnt X O Step)
     as [t [More [NewCl [Loc [Tp [Tq [Dst [Kt [La [Ht [Ne DX]]]]]]]]]]].
  change (next (phase (fstate f))) with pn in Tp,Tq,Dst,DX.
  change (phase (fstate f)) with ph in DX.
  exists (actual++further t), (unused t).
  rewrite Dst,Tp,Real.
  assert (OldCl: In false common).
  { unfold common. apply in_or_app;left. cbn [segments]. apply in_or_app;left.
    apply phase_piece_closing; [exact Hp|unfold k;apply boundary_bounded;lia]. }
  assert (Ap : observed ((front ph actual ++ common)++h) d =
      (phase_guard ph,(front pn actual ++ common_out t)++ unused t)).
  { rewrite <- app_assoc,A,Loc. f_equal. rewrite app_assoc; reflexivity. }
  repeat split; try assumption; try reflexivity.
  - apply in_or_app; right; exact NewCl.
  - pose proof (evaluator_charge_projection (fstate f) hist d edge Step) as Proj.
    cbn zeta in Proj. destruct Proj as [z [Dz Ch]].
    rewrite Hal,Rep2 in Ch. rewrite Rep2 in Dz.
    assert (Bpad:observed ((front ph padded++common)++h) d =
                  (phase_guard ph,(front pn padded++common_out t)++unused t)).
    { rewrite <- app_assoc,B,Loc. f_equal. now rewrite app_assoc. }
    destruct (observed_image _ _ _ _ Bpad) as [Image Guard].
    rewrite Image,Guard in Ch.
    assert (LA:length (front pn actual) = length (front ph actual))
       by exact (front_next_length ph actual Hp).
    assert (LP:length (front pn padded) = length (front ph padded))
       by exact (front_next_length ph padded Hp).
    assert (Z:z=length (front pn padded++common_out t)).
    { rewrite !length_app in Dz,DX |- *. rewrite (length_app (front ph actual) common) in DX. lia. }
    rewrite Z,firstn_prefix36,skipn_word_suffix in Ch.
    rewrite (checked_charge_splice (front ph actual) (front ph padded)
     (front pn actual) (front pn padded) common (common_out t) h (unused t)
      (length (guard36 (phase_guard ph))) d LA LP OldCl NewCl).
    exact Ch.
Qed.
End L36FiniteHistory.
