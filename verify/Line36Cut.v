(** Represent any covered cut by its complete pieces and strictly partial
    next piece. This convention also covers cuts exactly between pieces. *)
From Coq Require Import List Arith Lia.
From BusyCoq Require Import Line36Cover.
Import ListNotations L36Tiles.

Module L36Cut.

Lemma piece_nonempty ph k v : ph < 6 -> k < 6 -> 0 < length (phase_pieces ph k v).
Proof. intros Hp Hk. cases_six ph; cases_six k; destruct v; vm_compute; lia. Qed.

Lemma index_mod k : k < 6 -> next k = (S k) mod 6.
Proof. intro H; cases_six k; reflexivity. Qed.

Lemma index_after ph choices : ph < 6 -> after36 choices ph = (ph + length choices) mod 6.
Proof.
  revert ph. induction choices as [|b r IH]; intros k Hk.
  - cbn [length after36]; rewrite Nat.add_0_r, Nat.mod_small by auto; reflexivity.
  - cbn [after36 length]. rewrite IH by (apply next_bound; auto).
    rewrite index_mod by auto. rewrite Nat.Div0.add_mod_idemp_l. f_equal; lia.
Qed.

Lemma data_grammar ph choices k data :
  ph<6 -> k<6 -> prefix data (segments ph k choices) ->
  exists cs mode len, len < length (phase_pieces ph (after36 cs k) mode) /\
    data = segments ph k cs ++ firstn len (phase_pieces ph (after36 cs k) mode).
Proof.
  intros Hp. revert k data.
  induction choices as [|b cs IH]; intros k data Hk [post E].
  - destruct data; cbn [segments] in E; [|discriminate].
    exists [],false,0. cbn [after36 segments]; auto using piece_nonempty.
  - cbn [segments] in E. set (p := phase_pieces ph k b) in *.
    destruct (lt_dec (length data) (length p)) as [H|H].
    + exists [],b,(length data). split; [exact H|].
      apply (f_equal (firstn (length data))) in E.
      rewrite !firstn_app, firstn_all, Nat.sub_diag, app_nil_r in E.
      replace (length data-length p) with 0 in E by lia.
      cbn [firstn] in E; rewrite app_nil_r in E. exact (eq_sym E).
    + assert (Left : data=p++skipn (length p) data).
      { rewrite <- (firstn_skipn (length p) data) at 1.
        f_equal. apply (f_equal (firstn (length p))) in E.
        rewrite !firstn_app, firstn_all, Nat.sub_diag, app_nil_r in E.
        replace (length p-length data) with 0 in E by lia.
        cbn [firstn] in E; rewrite app_nil_r in E. exact (eq_sym E). }
      assert (Fr : prefix (skipn (length p) data) (segments ph (next k) cs)).
      { exists post. rewrite Left in E at 1. rewrite <- app_assoc in E.
        now apply app_inv_head in E. }
      destruct (IH (next k) _ (next_bound k Hk) Fr) as [c [mode [len [Bound Eq]]]].
      exists (b::c),mode,len. split; [exact Bound|].
      cbn [segments after36]. rewrite Left at 1. rewrite Eq, <- app_assoc. reflexivity.
Qed.

Theorem covered_cut ph data :
  ph < 6 -> covered36 ph data ->
  exists cs mode len,
    len < length (phase_pieces ph (length cs mod 6) mode) /\
    data=segments ph 0 cs ++ firstn len (phase_pieces ph (length cs mod 6) mode).
Proof.
  intros Hp [ts [t [Ht Et]]].
  destruct (data_grammar ph (concat ts) 0 data Hp ltac:(lia)) as [cs [mode [len H]]].
  - exists t. rewrite <- region_segments36 by exact Ht. now symmetry.
  - exists cs,mode,len. now rewrite index_after in H by lia.
Qed.


Lemma piece_width ph k b : ph<6 -> k<6 -> length (phase_pieces ph k b) <= 30.
Proof. intros Hp Hk; cases_six ph; cases_six k; destruct b; vm_compute; lia. Qed.

Lemma segments_width ph cs k : ph<6 -> k<6 -> length (segments ph k cs)<=30*length cs.
Proof.
  intros Hp. revert k. induction cs as [|b cs IH]; intros k Hk; [reflexivity|].
  cbn [segments length]. rewrite length_app. specialize (IH (next k) (next_bound _ Hk)).
  pose proof (piece_width ph k b Hp Hk); lia.
Qed.

Theorem canonical_width ph cs mode len :
  ph<6 -> len < length (phase_pieces ph (length cs mod 6) mode) ->
  length (phase_prefix ph ++ segments ph 0 cs ++ firstn len (phase_pieces ph (length cs mod 6) mode))
    < 26 + 30*(S (length cs)).
Proof.
  intros Hp Hlen. rewrite !length_app, phase_prefix_length36 by exact Hp.
  rewrite length_firstn. pose proof (segments_width ph cs 0 Hp ltac:(lia)).
  pose proof (piece_width ph _ mode Hp (Nat.mod_upper_bound (length cs) 6 ltac:(lia))). lia.
Qed.

Lemma group_sixes cs n : length cs=6*n ->
  exists ts, Forall (fun t : list bool => length t=6) ts /\ concat ts=cs.
Proof.
  revert cs. induction n as [|n IH]; intros cs H.
  - destruct cs; [exists []; auto|discriminate H].
  - destruct (IH (skipn 6 cs)) as [ts [Ht Et]]; [rewrite length_skipn; lia|].
    exists (firstn 6 cs :: ts). split.
    + constructor; [rewrite length_firstn; lia|exact Ht].
    + cbn [concat]; rewrite Et; apply firstn_skipn.
Qed.

Lemma group_with_padding (cs : list bool) :
  exists ts padding, Forall (fun t : list bool => length t=6) ts /\ concat ts=cs++padding.
Proof.
  set (padding := repeat false (6*length cs-length cs)).
  destruct (group_sixes (cs++padding) (length cs)) as [ts [H E]].
  - unfold padding. rewrite length_app, repeat_length; lia.
  - exists ts,padding; auto.
Qed.

Theorem canonical_covered ph cs mode len :
  covered36 ph (segments ph 0 cs ++ firstn len (phase_pieces ph (length cs mod 6) mode)).
Proof.
  destruct (group_with_padding (cs++[mode])) as [ts [pad [Ht E]]].
  exists ts,(skipn len (phase_pieces ph (length cs mod 6) mode) ++
            segments ph (next (length cs mod 6)) pad).
  split; [exact Ht|]. rewrite (region_segments36 ph ts Ht),E,<-(app_assoc cs [mode] pad),segments_app36.
  change ((segments ph 0 cs ++ firstn len (phase_pieces ph (length cs mod 6) mode)) ++
          skipn len (phase_pieces ph (length cs mod 6) mode) ++
          segments ph (next (length cs mod 6)) pad =
          segments ph 0 cs ++ phase_pieces ph (after36 cs 0) mode ++
          segments ph (next (after36 cs 0)) pad).
  rewrite (index_after 0 cs ltac:(lia)). cbn [Nat.add].
  rewrite <-app_assoc. f_equal. rewrite app_assoc,firstn_skipn. reflexivity.
Qed.

End L36Cut.
