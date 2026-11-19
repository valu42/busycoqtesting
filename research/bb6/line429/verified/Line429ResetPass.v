(** Complete four-way split at an original F reading 00 on a finite tape.
    The bit immediately to the left is zero everywhere F is reachable from blank. *)
From BusyCoq Require Import Individual62 Line429Sibling Line429Reset.
From Coq Require Import Lia List Arith.
Import Sibling429 Reset429 ListNotations.
Open Scope sym_scope.
Module ResetPass429.
Fixpoint pairs (k:nat) (r:side) : side :=
  match k with O => r | S j => 1 >> 0 >> pairs j r end.
Fixpoint ones (n:nat) (r:side) : side :=
  match n with O => r | S j => 1 >> ones j r end.
Lemma ones_last n r : ones n (1 >> r) = 1 >> ones n r.
Proof. induction n; cbn; congruence. Qed.

Ltac literal_tick := eapply multistep_S; [apply step_c_spec; reflexivity|simpl_tape].
Lemma cross_pairs k : forall l r,
  l {{B}}> pairs k r -[machine429]->> (2*k)%nat / (ones (2*k) l) {{B}}> r.
Proof.
  induction k as [|k IH]; intros l r; [constructor|].
  replace (2*S k)%nat with (S (S (2*k))) by lia. cbn [pairs ones]. do 2 literal_tick.
  rewrite <- !ones_last. apply IH.
Qed.
Lemma erase_left n : forall l r,
  (ones n l) <{{E}} r -[machine429]->> n / l <{{E}} (ones n r).
Proof.
  induction n as [|n IH]; intros l r; [constructor|]. cbn [ones]. literal_tick.
  rewrite <- ones_last. apply IH.
Qed.

Lemma enter k l x : (0 >> l) {{F}}> (0 >> 0 >> pairs k x)
  -[machine429]->> (2+2*k)%nat / (ones (2*k) (1 >> 0 >> 0 >> l)) {{B}}> x.
Proof. do 2 literal_tick. apply cross_pairs. Qed.

Theorem exit_01 k l t : (0 >> l) {{F}}> (0 >> 0 >> pairs k (0 >> 1 >> t))
  -[machine429]->> (2*k+4)%nat /
  (0 >> 1 >> ones (2*k) (1 >> 0 >> 0 >> l)) {{F}}> t.
Proof.
  replace (2*k+4)%nat with ((2+2*k)+2)%nat by lia.
  eapply multistep_trans; [apply enter|]. do 2 literal_tick. constructor.
Qed.
Theorem exit_11 k l t : (0 >> l) {{F}}> (0 >> 0 >> pairs k (1 >> 1 >> t))
  -[machine429]->> (2*k+6)%nat /
  (0 >> 0 >> ones (2*k) (1 >> 0 >> 0 >> l)) {{A}}> t.
Proof.
  replace (2*k+6)%nat with ((2+2*k)+4)%nat by lia.
  eapply multistep_trans; [apply enter|]. do 4 literal_tick. constructor.
Qed.
Theorem exit_000 k l t : (0 >> l) {{F}}> (0 >> 0 >> pairs k (0 >> 0 >> 0 >> t))
  -[machine429]->> (4*k+20)%nat /
  l <{{C}} (0 >> 1 >> 1 >> 0 >> 1 >> ones (2*k) (0 >> t)).
Proof.
  replace (4*k+20)%nat with (((2+2*k)+3)+(2*k+15))%nat by lia.
  eapply multistep_trans; [eapply multistep_trans; [apply enter|do 3 literal_tick; apply multistep_0]|].
  rewrite ones_last.
  replace (2*k+15)%nat with (S (S (S (2*k))) + 12)%nat by lia.
  eapply multistep_trans with (c':= (0 >> 0 >> l) <{{E}} (ones (S (S (S (2*k)))) (0 >> t))).
  - exact (erase_left (S (S (S (2*k)))) (0 >> 0 >> l) (0 >> t)).
  - cbn [ones]. do 12 literal_tick. constructor.
Qed.
Lemma pattern_is_word k t : pairs k (0 >> 0 >> 1 >> t) = word k t.
Proof. induction k; cbn; congruence. Qed.
Theorem exit_001 k l t :
  halts_in machine429 ((0 >> l) {{F}}> (0 >> 0 >> pairs k (0 >> 0 >> 1 >> t))) (2*k+4)%nat.
Proof. rewrite pattern_is_word; apply reset_count. Qed.

Inductive ending : side -> Prop :=
  | end01 t : ending (0 >> 1 >> t)
  | end11 t : ending (1 >> 1 >> t)
  | end000 t : ending (0 >> 0 >> 0 >> t)
  | end001 t : ending (0 >> 0 >> 1 >> t).
Lemma blank_end : ending 0inf.
Proof. pose proof (end000 0inf) as H. now repeat rewrite <- (const_unfold _ S0) in H. Qed.
Theorem complete w : exists k s, w *> 0inf = pairs k s /\ ending s.
Proof.
  assert (G : forall n (v:list Sym), length v = n ->
    exists k s, v *> 0inf = pairs k s /\ ending s).
  { intro n; induction n as [n IH] using lt_wf_ind. intros [|a [|b v]] N.
    - exists O,0inf; split; [reflexivity|apply blank_end].
    - destruct a.
      + exists O,0inf; split; [symmetry; apply const_unfold|apply blank_end].
      + exists 1%nat,0inf; split; [change (1 >> 0inf = 1 >> 0 >> 0inf); f_equal; apply const_unfold|apply blank_end].
    - destruct a,b.
      + exists O,(0 >> 0 >> (v *> 0inf)); split; [reflexivity|].
        destruct (v *> 0inf) as [[|] t]; constructor.
      + exists O,(0 >> 1 >> (v *> 0inf)); split; [reflexivity|constructor].
      + destruct (IH (length v) ltac:(cbn in N; lia) v eq_refl) as [k [s [R H]]].
        exists (S k),s. split; [cbn; now rewrite R|exact H].
      + exists O,(1 >> 1 >> (v *> 0inf)); split; [reflexivity|constructor]. }
  apply (G (length w) w eq_refl).
Qed.
End ResetPass429.
Print Assumptions ResetPass429.exit_000.
Print Assumptions ResetPass429.complete.
