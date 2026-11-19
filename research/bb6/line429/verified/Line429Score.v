(** Count the ones in a compressed tape and bound the number of original moves. *)
From BusyCoq Require Import Individual62 Line429Engine.
From Coq Require Import List NArith PeanoNat Lia.
Import ListNotations Bell429.
Open Scope sym_scope.

Module Score429.
Ltac transport_count H :=
  lazymatch type of H with
  | sigma_score_side _ ?n =>
    lazymatch goal with |- sigma_score_side _ ?m => replace m with n by nia; exact H end
  | sigma_score _ ?n =>
    lazymatch goal with |- sigma_score _ ?m => replace m with n by (cbn; lia); exact H end
  end.

Fixpoint word_count (w : list Sym) : nat :=
  match w with [] => O | b :: t => sigma_score_sym b + word_count t end.

Lemma count_app w v : word_count (w ++ v) = word_count w + word_count v.
Proof. induction w; simpl; lia. Qed.
Lemma count_pow w k : word_count (w^^k) = k * word_count w.
Proof. induction k; cbn [lpow]; [reflexivity | rewrite count_app, IHk; lia]. Qed.
Lemma count_D n : word_count (D_word n) = 2*n+1.
Proof. unfold D_word; rewrite !count_app, count_pow; cbn; lia. Qed.
Lemma count_S n : word_count (S_word n) = n+2.
Proof. unfold S_word; rewrite count_app, count_pow; cbn; lia. Qed.
Lemma count_PL n : word_count (PL_word n) = 3*n+8.
Proof. unfold PL_word; rewrite !count_app, !count_pow, !count_S; cbn; lia. Qed.
Lemma count_DEF a k : word_count (DefWord a k) = a+k+3.
Proof. unfold DefWord; rewrite !count_app, !count_pow, count_S; cbn; lia. Qed.

Lemma side_prefix w t n : sigma_score_side t n ->
  sigma_score_side (w *> t) (word_count w + n).
Proof.
  intro H. induction w as [|b w IH]; cbn; [exact H|].
  replace (sigma_score_sym b + word_count w + n) with
    (sigma_score_sym b + (word_count w + n)) by lia.
  constructor; [reflexivity | exact IH].
Qed.

Fixpoint digits_count (ds : Digits) : N :=
  match ds with [] => 0 | (d,k)::rest => (2*d+1)*k + digits_count rest end%N.

Lemma digits_side ds : forall t n, sigma_score_side t n ->
  sigma_score_side (denD ds t) (N.to_nat (digits_count ds) + n).
Proof.
  induction ds as [|[d k] ds IH]; intros t n H; cbn [denD digits_count]; [exact H|].
  pose proof (side_prefix ((D_word (N.to_nat d))^^(N.to_nat k)) _ _ (IH _ _ H)) as P.
  rewrite count_pow,count_D in P. repeat (rewrite N2Nat.inj_add || rewrite N2Nat.inj_mul).
  cbn [N.to_nat Pos.to_nat] in *. transport_count P.
Qed.
Lemma digits_rev_side ds : forall t n, sigma_score_side t n ->
  sigma_score_side (denDRev ds t) (N.to_nat (digits_count ds) + n).
Proof.
  induction ds as [|[d k] ds IH]; intros t n H; cbn [denDRev digits_count]; [exact H|].
  pose proof (IH _ _ (side_prefix ((D_word (N.to_nat d))^^(N.to_nat k)) _ _ H)) as P.
  rewrite count_pow,count_D in P. repeat (rewrite N2Nat.inj_add || rewrite N2Nat.inj_mul).
  cbn [N.to_nat Pos.to_nat] in *. transport_count P.
Qed.
Lemma digits_word ds : word_count (digitsToList ds) = N.to_nat (digits_count ds).
Proof.
  pose proof (digits_side ds _ _ sigma_score_side_O) as H.
  pose proof (side_prefix (digitsToList ds) _ _ sigma_score_side_O) as P.
  rewrite digitsToList_plug in P. apply (sigma_score_side_unique _ _ _ P) in H. lia.
Qed.
Lemma rev_digits_word ds : word_count (digitsRevToList ds) = N.to_nat (digits_count ds).
Proof.
  pose proof (digits_rev_side ds _ _ sigma_score_side_O) as H.
  pose proof (side_prefix (digitsRevToList ds) _ _ sigma_score_side_O) as P.
  rewrite digitsRevToList_plug in P. apply (sigma_score_side_unique _ _ _ P) in H. lia.
Qed.
Definition symword_count (w : SymWord) : N :=
  match w with
  | SW_raw w => N.of_nat (word_count w)
  | SW_D n => 2*n+1 | SW_S n => n+2 | SW_PL n => 3*n+8 | SW_DEF a k => a+k+3
  | SW_DF ds | SW_DB ds => digits_count ds
  end%N.
Lemma symword_correct w : word_count (sw_toList w) = N.to_nat (symword_count w).
Proof.
  destruct w; cbn [sw_toList symword_count];
  rewrite ?count_D,?count_S,?count_PL,?count_DEF,?digits_word,?rev_digits_word,
    ?Nat2N.id,?N2Nat.inj_add,?N2Nat.inj_mul; cbn; lia.
Qed.
Fixpoint runs_count (xs : Runs) : N :=
  match xs with [] => 0 | (w,k)::rest => symword_count w * k + runs_count rest end%N.
Lemma plug_count xs t n : sigma_score_side t n ->
  sigma_score_side (plug xs t) (N.to_nat (runs_count xs) + n).
Proof.
  intro H. induction xs as [|[w k] xs IH]; cbn [runs_count plug]; [exact H|].
  pose proof (side_prefix ((sw_toList w)^^(N.to_nat k)) _ _ IH) as P.
  rewrite count_pow,symword_correct in P. rewrite N2Nat.inj_add,N2Nat.inj_mul.
  transport_count P.
Qed.
Lemma runs_correct xs : sigma_score_side (runs_denote xs) (N.to_nat (runs_count xs)).
Proof. rewrite denote_eq_plug_0inf. pose proof (plug_count xs _ _ sigma_score_side_O) as H. now rewrite Nat.add_0_r in H. Qed.
Definition right_count rt := (runs_count (r_raw rt) + digits_count (d_front rt) +
   digits_count (d_back rt) + runs_count (r_tail rt))%N.
Lemma right_correct rt : sigma_score_side (rt_denote rt) (N.to_nat (right_count rt)).
Proof.
  unfold rt_denote,right_count. rewrite !N2Nat.inj_add.
  pose proof (plug_count (r_raw rt) _ _ (digits_side (d_front rt) _ _ (digits_rev_side (d_back rt) _ _ (runs_correct (r_tail rt))))) as H.
  rewrite <- !Nat.add_assoc. exact H.
Qed.

Lemma side_head t n : sigma_score_side t n ->
  exists k, sigma_score_side (Streams.tl t) k /\ n = sigma_score_sym (Streams.hd t) + k.
Proof.
  destruct 1 as [|b t x k H P]; [exists O; split; [constructor|reflexivity]|].
  exists k; split; [exact P | cbn; rewrite H; reflexivity].
Qed.
Lemma face_right q l r a b : sigma_score_side l a -> sigma_score_side r b ->
  sigma_score (l {{q}}> r) (a+b).
Proof. intros L R. destruct (side_head _ _ R) as [k [H ->]].
  rewrite Nat.add_assoc. constructor; [exact L|reflexivity|exact H]. Qed.
Lemma face_left q l r a b : sigma_score_side l a -> sigma_score_side r b ->
  sigma_score (l <{{q}} r) (a+b).
Proof. intros L R. destruct (side_head _ _ L) as [k [H ->]].
  replace (sigma_score_sym (Streams.hd l)+k+b) with (k+sigma_score_sym (Streams.hd l)+b) by lia.
  constructor; [exact H|reflexivity|exact R]. Qed.
Definition config_count (s : FastState) :=
  (runs_count (fs_L s) + right_count (fs_R s) + match fs_mode s with RAW _ _ => 0 | _ => 1 end)%N.
Lemma config_correct s : sigma_score (fs_denote s) (N.to_nat (config_count s)).
Proof.
  destruct s as [l r m]. unfold fs_denote,config_count; cbn [fs_L fs_R fs_mode].
  pose proof (runs_correct l) as L. pose proof (right_correct r) as R.
  destruct m as [| | |q [|]]; rewrite !N2Nat.inj_add;
  [pose proof (face_right A _ _ _ _ L (side_prefix [0;1;0;0] _ _ R)) as H
  |pose proof (face_left B _ _ _ _ L (side_prefix [1] _ _ R)) as H
  |pose proof (face_left C _ _ _ _ L (side_prefix [1;0;0] _ _ R)) as H
  |pose proof (face_left q _ _ _ _ L R) as H
  |pose proof (face_right q _ _ _ _ L R) as H];
  unfold CfgR,CfgL,CfgJ; transport_count H.
Qed.

(** A finite checkpoint implies an elementary-move lower bound on the literal machine. *)
Theorem checkpoint_bound k v :
  (match run_pow k initFastB with Some s => (v <=? config_count s)%N | None => false end) = true ->
  exists n c, c0 -[ tm ]->> n / c /\ (N.to_nat v <= n)%nat.
Proof.
  pose proof (blank_engine k) as reachable. destruct (run_pow k initFastB) as [s|]; [|discriminate].
  intros H. apply N.leb_le in H. assert (Hv : (N.to_nat v <= N.to_nat (config_count s))%nat) by lia.
  destruct (evstep_multistep _ _ _ reachable) as [n run].
  assert (blank_score : sigma_score (B;;tape0) O).
  { change O with (O+O+O). constructor; [constructor|reflexivity|constructor]. }
  pose proof (sigma_score_bounded _ _ _ _ _ _ run blank_score (config_correct s)) as steps.
  apply flip_multistep in run. destruct (flip_conf (fs_denote s)) as [q t] eqn:E.
  change (flip_conf (B;;tape0)) with (B;;tape0) in run.
  exists n,(permState q;;t). split; [exact (perm_multistep _ _ _ perm_src _ _ _ _ _ run)|lia].
Qed.
End Score429.
