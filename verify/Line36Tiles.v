(* Spatial certificates for BB(2,5) line 36. Words are in reading order;
   true is an opening (symbol 1) and false is a closing (symbol 2). *)
From Coq Require Import List Bool Arith ZArith Lia Ascii String.
From BusyCoq Require Import Line36Matching.
Import ListNotations.
Local Open Scope Z_scope.

Module L36Tiles.

Fixpoint digits (s : string) : list bool :=
  match s with
  | EmptyString => []
  | String a r => Ascii.eqb a "1"%char :: digits r
  end.

Definition piece_table : list (list (string * string)) := [
  [("112111211121112121211111112"%string, "1112111211121112121211111112"%string);
   ("11122121212121212111112111"%string, "111212121212121212111112111"%string);
   ("11212211111111111111121112121"%string, "112121211111111111111121112121"%string);
   ("121111121111111111111212121"%string, "1121111121111111111111212121"%string);
   ("11221211121211111111111211"%string, "112121211121211111111111211"%string);
   ("11122111112121112111111111212"%string, "111212111112121112111111111212"%string)];
  [("112111221212121212121111121"%string, "1121112121212121212121111121"%string);
   ("11112122111111111111111211"%string, "111121212111111111111111211"%string);
   ("12121121111121111111111111212"%string, "121211121111121111111111111212"%string);
   ("121112212111212111111111112"%string, "1211121212111212111111111112"%string);
   ("11111221111121211121111111"%string, "111112121111121211121111111"%string);
   ("11212112111211121112121211111"%string, "112121112111211121112121211111"%string)];
  [("112122111111111111111211121"%string, "1121212111111111111111211121"%string);
   ("21121111121111111111111212"%string, "211121111121111111111111212"%string);
   ("12111221211121211111111111211"%string, "121112121211121211111111111211"%string);
   ("111221111121211121111111112"%string, "1112121111121211121111111112"%string);
   ("12112111211121112121211111"%string, "121112111211121112121211111"%string);
   ("11211122121212121212111112111"%string, "112111212121212121212111112111"%string)];
  [("121111121111111111111212121"%string, "1121111121111111111111212121"%string);
   ("11221211121211111111111211"%string, "112121211121211111111111211"%string);
   ("11122111112121112111111111212"%string, "111212111112121112111111111212"%string);
   ("112111211121112121211111112"%string, "1112111211121112121211111112"%string);
   ("11122121212121212111112111"%string, "111212121212121212111112111"%string);
   ("11212211111111111111121112121"%string, "112121211111111111111121112121"%string)];
  [("121112212111212111111111112"%string, "1211121212111212111111111112"%string);
   ("11111221111121211121111111"%string, "111112121111121211121111111"%string);
   ("11212112111211121112121211111"%string, "112121112111211121112121211111"%string);
   ("112111221212121212121111121"%string, "1121112121212121212121111121"%string);
   ("11112122111111111111111211"%string, "111121212111111111111111211"%string);
   ("12121121111121111111111111212"%string, "121211121111121111111111111212"%string)];
  [("111221111121211121111111112"%string, "1112121111121211121111111112"%string);
   ("12112111211121112121211111"%string, "121112111211121112121211111"%string);
   ("11211122121212121212111112111"%string, "112111212121212121212111112111"%string);
   ("112122111111111111111211121"%string, "1121212111111111111111211121"%string);
   ("21121111121111111111111212"%string, "211121111121111111111111212"%string);
   ("12111221211121211111111111211"%string, "121112121211121211111111111211"%string)]
].

Definition phase_prefix (ph : nat) : list bool := digits (nth ph [
"22211111221112111111111212"%string;
  "22112111121121112121211111"%string;
  "11122121121221212111112111"%string;
  "22211111111111111121112121"%string;
  "22112111121111111111111212"%string;
  "11122121121211111111111211"%string] ""%string).

Definition phase_pieces (ph k : nat) (b : bool) : list bool :=
  let p := nth k (nth ph piece_table []) (""%string, ""%string) in
  digits (if b then snd p else fst p).

Definition next (k : nat) := if Nat.eqb k 5 then 0%nat else S k.
Definition phase_header (ph : nat) : nat := nth ph [6;1;1;6;1;1]%nat 0%nat.
Definition phase_guard (ph : nat) : nat := nth ph [3;2;0;3;2;0]%nat 0%nat.
Definition phase_overlap (ph : nat) : list bool :=
  digits (nth ph ["112111"%string;"1"%string;"1"%string;
                  "121112"%string;"1"%string;"1"%string] ""%string).
Definition phase_last (ph : nat) : bool :=
  nth ph [false;true;true;true;false;true] false.

Fixpoint segments (ph k : nat) (choices : list bool) : list bool :=
  match choices with
  | [] => []
  | b :: r => phase_pieces ph k b ++ segments ph (next k) r
  end.

Definition tiles_word (ph start : nat) (choices : list bool) : list bool :=
  segments ph (start mod 6)%nat choices.

Definition balance := bal36.

Lemma balance_app : forall p w, balance (p++w) = balance p + balance w.
Proof. exact bal36_app. Qed.

Definition factor (fragment whole : list bool) : Prop :=
  exists left right, whole = left ++ fragment ++ right.
Definition prefix (fragment whole : list bool) : Prop :=
  exists right, whole = fragment ++ right.

Definition weight (b : bool) : Z := if b then -1 else 3.
Fixpoint score (w : list bool) : Z :=
  match w with [] => 0 | b::r => weight b + score r end.

Lemma score_balance : forall w,
  score w = Z.of_nat (List.length w) - 2 * balance w.
Proof.
  induction w as [|b w IH]; [reflexivity|].
  change (weight b + score w =
          Z.of_nat (S (List.length w)) - 2 * ((if b then 1 else -1) + balance w)).
  rewrite Nat2Z.inj_succ, IH. destruct b; unfold weight; lia.
Qed.

(* At a piece boundary, the scan stores the maximum score of a suffix
   ending at this boundary, including the empty suffix. A positive witness
   for a factor would appear as a large scan value at the factor's end. *)
Definition step (z : Z) (b : bool) := Z.max 0 (z + weight b).
Fixpoint scan (z : Z) (w : list bool) : Z :=
  match w with [] => z | b::r => scan (step z b) r end.
Fixpoint within (z : Z) (w : list bool) : bool :=
  match w with
  | [] => z <=? 22
  | b::r => (z <=? 22) && within (step z b) r
  end.

Lemma scan_app : forall w v z,
  scan z (w++v) = scan (scan z w) v.
Proof. induction w; intros; simpl; auto. Qed.

Lemma within_app : forall w v z,
  within z (w ++ v) = true <->
  within z w = true /\ within (scan z w) v = true.
Proof.
  induction w as [|b w IH]; intros v z; simpl.
  - destruct v; simpl; [tauto|]. rewrite andb_true_iff. tauto.
  - rewrite !andb_true_iff, IH. tauto.
Qed.

Lemma step_mono : forall x y b, x <= y -> step x b <= step y b.
Proof. intros; unfold step; apply Z.max_le_compat_l; lia. Qed.

Lemma scan_mono : forall w x y, x <= y -> scan x w <= scan y w.
Proof. induction w; intros; simpl; auto using step_mono. Qed.

Lemma within_mono : forall w x y,
  x <= y -> within y w = true -> within x w = true.
Proof.
  induction w as [|b w IH]; intros x y Hxy; simpl.
  - rewrite !Z.leb_le; lia.
  - rewrite !andb_true_iff, !Z.leb_le. intros [Hy Hw]; split; [lia|].
    eapply IH; [apply step_mono; exact Hxy|exact Hw].
Qed.

Lemma scan_nonnegative : forall w z, 0 <= z -> 0 <= scan z w.
Proof.
  induction w as [|b w IH]; intros z Hz; simpl; auto.
  apply IH. unfold step; apply Z.le_max_l.
Qed.

Lemma scan_score : forall w z, z + score w <= scan z w.
Proof.
  induction w as [|b w IH]; intros z; simpl; [lia|].
  specialize (IH (step z b)). assert (z + weight b <= step z b)
    by (unfold step; apply Z.le_max_r). lia.
Qed.

Lemma within_end : forall w z, within z w = true -> scan z w <= 22.
Proof.
  induction w as [|b w IH]; intros z H; simpl in *.
  - apply Z.leb_le; exact H.
  - apply andb_true_iff in H as [_ H]. auto.
Qed.

Definition boundary_bound (ph k : nat) : Z :=
  nth k (nth ph [
    [5;6;16;11;6;4]; [5;18;8;5;6;0]; [16;9;5;4;3;5];
    [11;6;4;5;6;16]; [5;6;0;5;18;8]; [4;3;5;16;9;5]
  ] []) 0.

Ltac cases_six x :=
  destruct x as [|[|[|[|[|[|x]]]]]]; try lia.

Lemma next_bound : forall k, (k < 6)%nat -> (next k < 6)%nat.
Proof. intros k H; cases_six k; reflexivity || (cbv; lia). Qed.

Lemma boundary_local : forall ph k b, (ph < 6)%nat -> (k < 6)%nat ->
  ((0 <=? boundary_bound ph k) &&
   within (boundary_bound ph k) (phase_pieces ph k b) &&
   (scan (boundary_bound ph k) (phase_pieces ph k b) <=? boundary_bound ph (next k))) = true.
Proof. intros ph k b Hp Hk; cases_six ph; cases_six k; destruct b; vm_compute; reflexivity. Qed.

Lemma boundary_nonnegative : forall ph k, (ph < 6)%nat -> (k < 6)%nat ->
  0 <= boundary_bound ph k.
Proof.
  intros ph k Hp Hk. pose proof (boundary_local ph k false Hp Hk) as H.
  apply andb_true_iff in H as [H _]; apply andb_true_iff in H as [H _].
  apply Z.leb_le; exact H.
Qed.

Lemma whole_within : forall ph choices k z, (ph < 6)%nat -> (k < 6)%nat ->
  z <= boundary_bound ph k -> within z (segments ph k choices) = true.
Proof.
  intros ph choices. induction choices as [|b choices IH]; intros k z Hp Hk Hz.
  - simpl. apply Z.leb_le.
    pose proof (boundary_local ph k false Hp Hk) as H.
    apply andb_true_iff in H as [H _]; apply andb_true_iff in H as [_ H].
    destruct (phase_pieces ph k false) as [|u us]; simpl in H;
      [|apply andb_true_iff in H as [H _]]; apply Z.leb_le in H; lia.
  - simpl. apply within_app.
    pose proof (boundary_local ph k b Hp Hk) as H.
    apply andb_true_iff in H as [H Hs]; apply andb_true_iff in H as [_ Hw].
    split.
    + eapply within_mono; eauto.
    + apply IH; auto using next_bound. apply Z.leb_le in Hs.
      eapply Z.le_trans; [apply scan_mono; exact Hz|exact Hs].
Qed.

Theorem factor_density : forall ph start choices w,
  (ph < 6)%nat -> factor w (tiles_word ph start choices) ->
  Z.of_nat (List.length w) - 2 * balance w <= 22.
Proof.
  intros ph start choices w Hp [l [r HE]].
  assert (Hk : (start mod 6 < 6)%nat) by (apply Nat.mod_upper_bound; lia).
  pose proof (whole_within ph choices (start mod 6)%nat 0 Hp Hk
                (boundary_nonnegative ph _ Hp Hk)) as H.
  change (within 0 (tiles_word ph start choices) = true) in H.
  rewrite HE in H. apply within_app in H as [_ H]. apply within_app in H as [H _].
  apply within_end in H. pose proof (scan_score w (scan 0 l)).
  pose proof (scan_nonnegative l 0 ltac:(lia)).
  rewrite <- score_balance. lia.
Qed.

(* For the finite-debt part, four recent pieces more than absorb an
   incoming debt of 28, even with a partial piece and a three-bit halo. *)
Fixpoint prefix_min (w : list bool) : Z :=
  match w with
  | [] => 0
  | b::r => Z.min 0 ((if b then 1 else -1) + prefix_min r)
  end.

Lemma prefix_min_le : forall p r, prefix_min (p++r) <= balance p.
Proof.
  induction p as [|b p IH]; intros r; simpl.
  - destruct r; simpl; [lia|apply Z.le_min_l].
  - eapply Z.le_trans; [apply Z.le_min_r|]. specialize (IH r); lia.
Qed.

Definition small_balance ph k := Z.min (balance (phase_pieces ph k false))
                                       (balance (phase_pieces ph k true)).
Lemma small_balance_le : forall ph k b, small_balance ph k <= balance (phase_pieces ph k b).
Proof. intros ph k b; destruct b; unfold small_balance; auto using Z.le_min_l,Z.le_min_r. Qed.

Lemma four_minima : forall ph k, (ph < 6)%nat -> (k < 6)%nat ->
  49 <= small_balance ph k + small_balance ph (next k) +
        small_balance ph (next (next k)) + small_balance ph (next (next (next k))).
Proof. intros ph k Hp Hk; cases_six ph; cases_six k; vm_compute; discriminate. Qed.

Lemma piece_prefix_min : forall ph k b, (ph < 6)%nat -> (k < 6)%nat ->
  -1 <= prefix_min (phase_pieces ph k b).
Proof. intros ph k b Hp Hk; cases_six ph; cases_six k; destruct b; vm_compute; discriminate. Qed.

Lemma balance_lower_length : forall w, - Z.of_nat (List.length w) <= balance w.
Proof.
  induction w as [|b w IH]; [reflexivity|].
  change (- Z.of_nat (S (List.length w)) <= (if b then 1 else -1) + balance w).
  rewrite Nat2Z.inj_succ. destruct b; lia.
Qed.

Theorem four_piece_shield : forall ph k b0 b1 b2 b3 choice part halo,
  (ph < 6)%nat -> (k < 6)%nat ->
  prefix part (phase_pieces ph (next (next (next (next k)))) choice) ->
  (List.length halo <= 3)%nat ->
  28 < balance (segments ph k [b0;b1;b2;b3] ++ part ++ halo).
Proof.
  intros ph k b0 b1 b2 b3 choice part halo Hp Hk [right Er] Hlen.
  pose proof (four_minima ph k Hp Hk) as Hsum.
  pose proof (small_balance_le ph k b0).
  pose proof (small_balance_le ph (next k) b1).
  pose proof (small_balance_le ph (next (next k)) b2).
  pose proof (small_balance_le ph (next (next (next k))) b3).
  assert (Hnext : (next (next (next (next k))) < 6)%nat) by auto using next_bound.
  pose proof (piece_prefix_min ph _ choice Hp Hnext) as Hpart.
  rewrite Er in Hpart. pose proof (prefix_min_le part right).
  pose proof (balance_lower_length halo). cbn [segments]; rewrite !balance_app; replace (balance []) with 0 by reflexivity; lia.
Qed.

Definition max_piece_length ph k :=
  Nat.max (List.length (phase_pieces ph k false)) (List.length (phase_pieces ph k true)).
Lemma max_piece_length_ge : forall ph k b,
  (List.length (phase_pieces ph k b) <= max_piece_length ph k)%nat.
Proof. intros ph k b; destruct b; unfold max_piece_length; auto using Nat.le_max_l, Nat.le_max_r. Qed.

Lemma five_maxima : forall ph k, (ph < 6)%nat -> (k < 6)%nat ->
  (max_piece_length ph k + max_piece_length ph (next k) +
   max_piece_length ph (next (next k)) + max_piece_length ph (next (next (next k))) +
   max_piece_length ph (next (next (next (next k)))) <= 143)%nat.
Proof. intros ph k Hp Hk; cases_six ph; cases_six k; vm_compute; lia. Qed.

Theorem five_piece_length : forall ph k b0 b1 b2 b3 b4, (ph < 6)%nat -> (k < 6)%nat ->
  (List.length (segments ph k [b0;b1;b2;b3;b4]) <= 143)%nat.
Proof.
  intros ph k b0 b1 b2 b3 b4 Hp Hk. pose proof (five_maxima ph k Hp Hk).
  pose proof (max_piece_length_ge ph k b0).
  pose proof (max_piece_length_ge ph (next k) b1).
  pose proof (max_piece_length_ge ph (next (next k)) b2).
  pose proof (max_piece_length_ge ph (next (next (next k))) b3).
  pose proof (max_piece_length_ge ph (next (next (next (next k)))) b4).
  cbn [segments]; rewrite !length_app; simpl; lia.
Qed.

Theorem phase_prefix_length : forall ph, (ph < 6)%nat -> List.length (phase_prefix ph) = 26%nat.
Proof. intros ph H; cases_six ph; vm_compute; reflexivity. Qed.

Theorem phase_overlap_length : forall ph, (ph < 6)%nat ->
  List.length (phase_overlap ph) = phase_header ph.
Proof. intros ph H; cases_six ph; vm_compute; reflexivity. Qed.

(** The numeric shield has the operational meaning that changing the exterior
    demand through 28 cannot affect the debt delivered to older pieces. *)
Theorem old_guard_shield ph k b0 b1 b2 b3 choice part halo d :
  (ph < 6)%nat -> (k < 6)%nat ->
  prefix part (phase_pieces ph (next (next (next (next k)))) choice) ->
  (List.length halo <= 3)%nat -> (d <= 28)%nat ->
  let recent := segments ph k [b0;b1;b2;b3] ++ part ++ halo in
  fst (mark36 recent d) = fst (mark36 recent 0).
Proof.
  intros Hp Hk Hpart Hhalo Hd. cbn zeta. apply mark36_shield.
  pose proof (four_piece_shield ph k b0 b1 b2 b3 choice part halo Hp Hk Hpart Hhalo).
  unfold balance in *; lia.
Qed.

(** A continuation made of complete or partial legal pieces cannot send more
    than eleven units of debt to the left. The stronger bound two happens to
    hold in these tables; the finite-front proof needs only the bound eleven. *)
Theorem factor_balance_floor : forall ph k choices w,
  (ph < 6)%nat -> factor w (tiles_word ph k choices) -> -11 <= balance w.
Proof.
  intros ph k choices w Hph F.
  pose proof (factor_density ph k choices w Hph F). lia.
Qed.

End L36Tiles.
