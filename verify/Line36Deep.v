(** Truncating a legal finite reference at the first deep mismatch gives a
    legal next cut, even if the exterior demands arbitrarily many openings. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Cover Line36Reference Line36Word Line36Tiles Line36TileShield
                           Line36HighDebt Line36Splice.
Import ListNotations L36Tiles L36TileShield L36Splice.
Local Open Scope Z_scope.

Module L36Deep.

Lemma protected_prefix_step p t v : step36 (p++t) = Some v ->
  exists tail, v = protected_output p (fst (mark36 t 0)) ++ tail.
Proof.
  unfold step36, protected_output. rewrite mark36_app.
  destruct (mark36 t 0) as [d b]; cbn [fst].
  destruct (mark36 p d) as [g a].
  destruct (Nat.ltb g 6); [|discriminate]. intros [= <-].
  unfold output36. rewrite deriv36_app.
  exists (deriv36 (last a (Nat.eqb g 1)) b ++ carry36 (Nat.eqb g 1) (a++b)).
  now repeat rewrite <- app_assoc.
Qed.

Lemma derivative_length p bits : length (deriv36 p bits) = length bits.
Proof. revert p; induction bits as [|b bits IH]; intros p; simpl; auto. Qed.

Lemma next_region_length ph ts :
  (ph<6)%nat -> Forall (fun t => length t = 6%nat) ts ->
  length (region36 (next ph) ts) = length (region36 ph ts).
Proof.
  intros Hph Hts. pose proof (region_facts36 ph ts Hph Hts) as F.
  pose proof (mark36_length (region36 ph ts) 0) as E.
  destruct (mark36 (region36 ph ts) 0) as [k bs].
  destruct F as [_ [_ Eq]]. apply (f_equal (@length bool)) in Eq.
  rewrite !length_app, derivative_length in Eq. cbn [snd] in E. lia.
Qed.

Lemma region_app ph a b : region36 ph (a++b) = region36 ph a ++ region36 ph b.
Proof. unfold region36. now rewrite map_app, concat_app. Qed.

Lemma pad_size ph : (ph < 6)%nat -> (6 <= length (tile36 ph (repeat false 6)))%nat.
Proof. intros Hp; cases_six ph; vm_compute; lia. Qed.

Lemma maximal_header g : (length (guard36 g) <= 6)%nat.
Proof. destruct g as [|[|[|[|[|g]]]]]; cbn; lia. Qed.

Lemma common_covered (head region post common extra : list bool) :
  (* The reference begins with the next header/region and the chosen cut
     falls between the end of the header and end of this region. *)
  head ++ region ++ post = common ++ extra ->
  (length head <= length common <= length head + length region)%nat ->
  exists data tail, common = head++data /\ region=data++tail.
Proof.
  intros E B.
  exists (firstn (length common - length head) region),
         (skipn (length common - length head) region).
  split; [|symmetry; apply firstn_skipn].
  apply (f_equal (firstn (length common))) in E.
  rewrite (firstn_app _ common extra), firstn_all, Nat.sub_diag, app_nil_r in E.
  rewrite firstn_app, firstn_all2 in E by lia.
  rewrite firstn_app in E. replace (length common - length head - length region)%nat with 0%nat in E by lia. cbn [firstn] in E; rewrite app_nil_r in E. congruence.
Qed.


Lemma region_guard ph ts (Hp : (ph<6)%nat) (Ht : Forall (fun t => length t=6%nat) ts) :
  fst (mark36 (phase_prefix ph ++ region36 ph ts) 0) = phase_guard ph.
Proof.
  pose proof (region_facts36 ph ts Hp Ht) as H.
  rewrite mark36_app; destruct (mark36 (region36 ph ts) 0) as [k bs].
  destruct H as [-> _]. pose proof (prefix_facts36 ph Hp) as P.
  destruct (mark36 (phase_prefix ph) 0) as [g bp]; exact (proj1 P).
Qed.

Lemma mark_guard_prefix p t :
 fst (mark36 p (fst (mark36 t 0))) = fst (mark36 (p++t) 0).
Proof. rewrite mark36_app. destruct (mark36 t 0). cbn. now destruct (mark36 p n). Qed.

Theorem deep_covered_step ph data halo d charge :
  (ph<6)%nat -> covered36 ph data -> length halo=3%nat -> (29<=d)%nat ->
  let p := phase_prefix ph ++ data in
  52 <= Z.of_nat (length p)-4*Z.of_nat charge ->
  (fst (mark36 halo d)<=charge+1)%nat ->
  exists nd changed rlen,
    let np := phase_prefix (next ph) ++ nd in
    covered36 (next ph) nd /\
    fst (mark36 (p++halo) d)=phase_guard ph /\
    protected_output (p++halo) d=np++changed::repeat true (rlen+3) /\
    -2*Z.of_nat d-27 <= Z.of_nat (length np)-Z.of_nat (length p) /\
    (length np+S rlen=length (guard36 (phase_guard ph))+length p)%nat /\
    Z.Even (Z.of_nat (length (p++halo))+Z.of_nat d-
        (Z.of_nat (length np)-Z.of_nat (length (guard36 (phase_guard ph))))).
Proof.
  intros Hp [ts [ext [Ht Et]]] Hh Hd p Hres Hk.
  set (ts' := ts ++ [repeat false 6]).
  set (tail := ext ++ tile36 ph (repeat false 6)).
  assert (Ht' : Forall (fun t => length t=6%nat) ts').
  { unfold ts'; apply Forall_app; split; [exact Ht|repeat constructor]. }
  assert (Et' : data++tail=region36 ph ts').
  { unfold ts', tail; rewrite region_app, <- Et. cbn [region36 map concat].
    rewrite app_nil_r, app_assoc; reflexivity. }
  assert (F : factor (data++tail) (tiles_word ph 0 (concat ts'))).
  { exists [], []; cbn [app]; rewrite app_nil_r, Et', (region_segments36 ph ts' Ht').
    reflexivity. }
  pose proof (prefix_is_factor_of_factor data tail _ F) as Fd.
  pose proof (suffix_is_factor_of_factor data tail _ F) as Ft.
  pose proof (phase_prefix_length ph Hp) as P.
  pose proof (phase_prefix_length (next ph) (next_bound ph Hp)) as P'.
  assert (L : length p=(26+length data)%nat) by (unfold p; now rewrite length_app,P).
  assert (K : (fst (mark36 halo d) <= openings36 (snd (mark36 data 0)))%nat).
  { eapply (protected_has_survivors ph 0 (concat ts') data (Z.of_nat charge));
    [exact Hp|exact Fd|lia|lia|lia]. }
  destruct (large_debt_splice ph 0 (concat ts') 0 (concat ts') data (phase_prefix ph)
                             tail halo d Hp Fd Ft Hh Hd K)
    as [common [changed [rest [n [G [R [A [Lex [Dx Par]]]]]]]]].
  fold p in G,R,A,Lex,Dx,Par.
  assert (Gref : fst (mark36 p (fst (mark36 tail 0)))=phase_guard ph).
  { rewrite mark_guard_prefix. unfold p. rewrite <- app_assoc,Et'. apply region_guard; assumption. }
  rewrite Gref in G,Lex,Par.
  assert (Ws := reference_sweep36 ph ts' Hp Ht').
  rewrite <- Et', app_assoc in Ws. fold p in Ws.
  destruct (protected_prefix_step _ _ _ Ws) as [rest2 O].
  rewrite R, <- app_assoc in O.
  pose proof (pad_size ph Hp) as Pad.
  assert (Cap : (length common <= length (phase_prefix (next ph)) + length (region36 (next ph) ts'))%nat).
  { rewrite next_region_length by assumption. rewrite <- Et', length_app, P'.
    unfold tail; rewrite length_app. pose proof (maximal_header (phase_guard ph)). lia. }
  assert (Floor : (length (phase_prefix (next ph)) <= length common)%nat).
  { pose proof (L36HighDebt.halo_erased halo d ltac:(lia)) as [_ B].
    assert (B' : bal36 halo <= Z.of_nat (length halo)).
    { clear. induction halo as [|[] r IH]; cbn [length bal36]; rewrite ?Nat2Z.inj_succ; lia. }
    lia. }
  destruct (common_covered _ _ _ _ _ O ltac:(lia)) as [nd [te [Ec Er]]].
  exists nd,(negb changed),n. cbn zeta. rewrite <- Ec.
  split; [exists ts', te; auto|]. split; [exact G|].
  split; [now rewrite <- Hh|]. split; [exact Dx|]. split; [exact Lex|].
  unfold p; now rewrite <- app_assoc.
Qed.

End L36Deep.
