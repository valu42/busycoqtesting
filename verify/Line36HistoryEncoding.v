From Coq Require Import List Bool Arith Lia.
From BusyCoq Require Import Line36Word Line36Tiles Line36Front Line36History Line36Left Line36LeftStep.
Import ListNotations L36Tiles L36History L36Left L36LeftStep.
Local Open Scope nat_scope.

Definition encode4 (a b c d : bool) :=
  (if a then 1 else 0) + (if b then 2 else 0) +
  (if c then 4 else 0) + (if d then 8 else 0).

Lemma encode4_range a b c d : encode4 a b c d < 16.
Proof. destruct a,b,c,d; cbv; lia. Qed.

Lemma boundary_length36 cs k : k<6 -> boundary k cs = (k+length cs) mod 6.
Proof.
  revert k. induction cs as [|b cs IH]; intros k H.
  - cbn [boundary length]. rewrite Nat.add_0_r. symmetry; now apply Nat.mod_small.
  - cbn [boundary length]. rewrite IH by (now apply next_bound).
    rewrite <- next_mod by assumption. rewrite Nat.Div0.add_mod_idemp_l.
    now replace (S k + length cs) with (k + S (length cs)) by lia.
Qed.

Lemma flat_pieces36 ph count start variants : ph < 6 ->
  flat_map (fun j => piece ph (j mod 6) (variants j)) (seq start count) =
  segments ph (start mod 6) (map variants (seq start count)).
Proof.
  intros Hp; revert start. induction count as [|n IH]; intros j; [reflexivity|].
  cbn [seq map flat_map segments]. rewrite IH, piece_exact by auto using Nat.mod_upper_bound.
  f_equal. f_equal. rewrite <- next_mod by (apply Nat.mod_upper_bound; lia).
  replace (S (j mod 6)) with (j mod 6 + 1) by lia.
  rewrite Nat.Div0.add_mod_idemp_l. now replace (j+1) with (S j) by lia.
Qed.

Definition older36 k := repeat false (piece_count k - 5).

Lemma representative_choices36 k a b c d e : k<6 ->
  let cnt := piece_count k in
  let variant := fun j => if S j =? cnt then e else if j <? cnt-5 then false
                           else Nat.testbit (encode4 a b c d) (j-(cnt-5)) in
  map variant (seq 0 cnt) = older36 k ++ [a;b;c;d;e].
Proof.
  intro H. cases_six k; destruct a,b,c,d; reflexivity.
Qed.

Lemma representative_shape36 ph k a b c d e option n halo :
  ph<6 -> k<6 ->
  representative (State ph k e option n halo) (encode4 a b c d) =
  front ph (older36 k) ++
  segments ph (boundary 0 (older36 k)) [a;b;c;d;e] ++
  firstn n (phase_pieces ph k option).
Proof.
  intros Hp Hk. unfold representative. cbn [kind phase last_choice partial_len partial_choice].
  rewrite pre_exact by assumption. rewrite flat_pieces36 by assumption.
  rewrite representative_choices36 by assumption. rewrite piece_exact by assumption.
  unfold front. rewrite segments_app. repeat rewrite <- app_assoc. reflexivity.
Qed.

Lemma peel_five36 (cs:list bool) : 5<=length cs ->
  exists old a b c d e, cs=old++[a;b;c;d;e].
Proof.
  intros H. rewrite <- (rev_involutive cs). rewrite <- length_rev in H.
  destruct (rev cs) as [|e [|d [|c [|b [|a old]]]]]; cbn [length] in H; try lia.
  exists (rev old),a,b,c,d,e; cbn [rev]. now repeat rewrite <- app_assoc.
Qed.

Lemma history_halo36 tail : 3<=length tail ->
  halo_word (encode_halo tail)=firstn 3 tail.
Proof.
  destruct tail as [|a [|b [|c rest]]]; cbn [length]; try lia.
  destruct a,b,c; reflexivity.
Qed.

Theorem concrete_history36 f : fvalid f -> 5<=length (fchoices f) ->
  exists actual padded a b c d e hist,
   fchoices f = actual++[a;b;c;d;e] /\ hist<16 /\
   boundary 0 actual = boundary 0 padded /\
   length padded + 5 = piece_count (fkind f) /\
   representative (fstate f) hist =
     front (fphase f) padded ++ segments (fphase f) (boundary 0 actual) [a;b;c;d;e] ++ fpart f /\
   halo_word (halo (fstate f)) = firstn 3 (ftail f).
Proof.
  intros [Hp [Hlen Ht]] Hg. destruct (peel_five36 _ Hg) as [old [a [b [c [d [e E]]]]]].
  exists old,(older36 (fkind f)),a,b,c,d,e,(encode4 a b c d).
  assert (K : fkind f < 6) by (apply Nat.mod_upper_bound; lia).
  assert (B : boundary 0 old = boundary 0 (older36 (fkind f))).
  { rewrite !boundary_length36 by lia. cbn [Nat.add].
    unfold older36, fkind. rewrite repeat_length, E, length_app.
    cbn [length]. unfold piece_count.
    rewrite <- (Nat.Div0.add_mod_idemp_l (length old) 5 6).
    pose proof (Nat.mod_upper_bound (length old) 6 ltac:(lia)) as Z.
    remember (length old mod 6) as j. cases_six j; reflexivity. }
  split; [exact E|]. split; [apply encode4_range|]. split; [exact B|].
  split; [unfold older36,piece_count; rewrite repeat_length; lia|].
  split.
  - unfold fstate. assert (L: last (fchoices f) false = e).
    { rewrite E, last36_app; reflexivity. }
    rewrite L, B. apply representative_shape36; assumption.
  - apply history_halo36; lia.
Qed.
