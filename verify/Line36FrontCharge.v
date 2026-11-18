(** Combine the exact physical switch count and the independently verified
    cap potential on a single step between two actual tiled fronts. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Word Line36Right Line36Halo Line36Charge
  Line36Front Line36Tiles Line36Seed Line36Cap Line36CapModel
  Line36CapBridge Line36CapInvariant.
Import ListNotations L36CapInvariant.
Local Open Scope nat_scope.

Definition switch_bound_front f g C :=
  (Z.of_nat (L36Seed.budget (fprefix g) (ftail g)) <=
   Z.of_nat (L36Seed.budget (fprefix f) (ftail f)) +
   C + (1-terminal_bit (fword f)) - Z.of_nat (real_loss (fword f)))%Z.

Definition cap_success_front f g h C :=
  exists j, cap_value (L36Seed.cap50 (fword g)) = Some j /\
  h <= 21 /\ j <= 21 /\
  (Z.of_nat j - Z.of_nat h <= 3*Z.of_nat (real_loss (fword f))-1)%Z /\
  terminal_bit (fword g)=(1-terminal_bit (fword f))%Z /\
  switch_bound_front f g C.

Lemma apply_front_cap (G : graph_spec) f g h C : fvalid f ->
  cap_value (L36Seed.cap50 (fword f))=Some h ->
  step36 (fword f)=Some (fword g) ->
  switch_bound_front f g C -> cap_success_front f g h C.
Proof.
  intros [_ [_ Wide]] V S B.
  assert (W : 50<length (fword f)) by (unfold fword; rewrite length_app; lia).
  destruct (real_cap_step G _ _ _ W V S) as [j [J [H [K [_ [D E]]]]]].
  exists j. exact (conj J (conj H (conj K (conj D (conj E B))))).
Qed.

Lemma front_terminal_ext f halo ext :
  ftail f=halo++ext -> ext<>[] ->
  terminal_bit (fword f) = (if last ext false then 1 else 0)%Z.
Proof.
  intros E N. unfold terminal_bit,fword. rewrite E,!last36_app.
  destruct ext as [|b ext]; [contradiction|]. now rewrite !last36_cons.
Qed.

Lemma missing_terminal_unit b :
  Z.of_nat (bit_cost (negb b)) = (1-(if b then 1 else 0))%Z.
Proof. destruct b; reflexivity. Qed.

(** This wrapper applies in particular with the generic, arbitrarily
    large-debt [C=3-d].  The terminal default can be chosen freely. *)
Theorem front_cap_step (G:graph_spec) f g halo ext d bits previous h C :
  fvalid f -> ftail f = halo++ext -> length halo = 3 ->
  mark36 ext 0 = (d,bits) -> step36 (fword f) = Some (fword g) ->
  cap_value (L36Seed.cap50 (fword f)) = Some h ->
  (forall before u, ext=before++false::u -> In true bits ->
     (Z.of_nat (L36Seed.budget (fprefix g) (ftail g)) <=
      Z.of_nat (L36Seed.budget (fprefix f) (ftail f)) + C +
      Z.of_nat (bit_cost (negb (last bits previous))) -
      Z.of_nat (cap_loss u))%Z) ->
  cap_success_front f g h C.
Proof.
  intros V E H M S Hcap U. apply (apply_front_cap G _ _ _ _ V Hcap S).
  destruct V as [_ [_ W]]. rewrite E,length_app,H in W.
  assert (Total : fword f = (fprefix f++halo)++ext) by (unfold fword; rewrite E,app_assoc; reflexivity).
  rewrite Total in Hcap. assert (Big : 50<length ((fprefix f++halo)++ext))
     by (rewrite !length_app,H; lia).
  destruct (tail_anchor G (fprefix f++halo) ext h ltac:(lia) Big Hcap)
    as [before [u [Decomp [Loss Live]]]].
  rewrite M in Live. specialize (U before u Decomp Live).
  assert (Non : ext<>[]) by (intros ->; discriminate || cbn in W; lia).
  pose proof (L36CapBridge.final_mask ext 0 previous Non) as Last.
  rewrite M in Last. cbn [snd Nat.eqb] in Last. rewrite andb_true_r in Last.
  unfold switch_bound_front. rewrite (front_terminal_ext _ _ _ E Non),Total,Loss.
  now rewrite Last,missing_terminal_unit in U.
Qed.

Lemma protected_has_closing f : fvalid f -> In false (fprefix f).
Proof.
  intros [P _]. unfold fprefix. apply in_or_app; left.
  destruct (fphase f) as [|[|[|[|[|[|p]]]]]]; try lia; vm_compute; tauto.
Qed.

(** The finite/deep shared cut form returned by the real representative:
    the entire known new image ends with the newly exposed [hi]. *)
Theorem front_cut_charge (G:graph_spec) f g halo ext hi d h :
  fvalid f -> fvalid g -> ftail f = halo++ext -> length halo=3 ->
  fst (mark36 ext 0) = d ->
  known_image (fprefix f++halo) d = fprefix g ++ hi ->
  step36 (fword f) = Some (fword g) ->
  cap_value (L36Seed.cap50 (fword f)) = Some h ->
  let head := length (guard36 (fst (mark36 (fprefix f++halo) d))) in
  cap_success_front f g h (checked_charge (fprefix f) halo (fprefix g) hi head d).
Proof.
  intros F Gv E H M K S Val. cbv zeta.
  apply (apply_front_cap G _ _ _ _ F Val S).
  pose proof (protected_has_closing _ F) as A.
  pose proof (protected_has_closing _ Gv) as A'.
  destruct F as [_ [_ W]]. rewrite E,length_app,H in W.
  assert (Non : ext<>[]) by (intros ->; cbn in W; lia).
  set (pre := firstn (length ext-50) ext). set (cap := skipn (length ext-50) ext).
  assert (D : ext=pre++cap) by (unfold pre,cap; symmetry; apply firstn_skipn).
  assert (L : length cap=50) by (unfold cap; rewrite length_skipn; lia).
  assert (Total : fword f = ((fprefix f++halo)++pre)++cap).
  { unfold fword. rewrite E,D. now rewrite !app_assoc. }
  assert (Cap : L36Seed.cap50 (fword f)=cap).
  { rewrite Total. apply L36CapBridge.window_suffix; exact L. }
  assert (Big : 50<length (fword f)) by (rewrite Total,!length_app,L,H; lia).
  destruct (real_cap_features G (fword f) h Big Val) as [_ [Close Live]].
  rewrite Cap in Close,Live.
  assert (Bclose : existsb negb cap=true).
  { apply existsb_exists. exists false. auto. }
  assert (Blive : existsb id (snd (mark36 cap 0))=true).
  { apply existsb_exists. exists true. auto. }
  rewrite D in M. set (z:=length (fprefix g)).
  assert (Zcut : z<=length(known_image (fprefix f++halo) d)).
  { rewrite K,length_app. unfold z. lia. }
  assert (Pz : firstn z (known_image (fprefix f++halo) d)=fprefix g).
  { unfold z. rewrite K,firstn_app,firstn_all,Nat.sub_diag,firstn_O,app_nil_r. reflexivity. }
  assert (Tz : skipn z (known_image (fprefix f++halo) d)=hi).
  { unfold z. rewrite K,skipn_app,skipn_all,Nat.sub_diag. reflexivity. }
  assert (T : fword f = (fprefix f++halo)++(pre++cap)) by now rewrite Total,app_assoc.
  assert (SS:= S). rewrite T in SS.
  pose proof (physical_charge_bound (fprefix f) halo pre cap (fword g) z d H A Bclose Blive M SS) as B.
  cbv zeta in B. specialize (B Zcut ltac:(rewrite Pz; exact A')).
  rewrite Pz,Tz in B.
  assert (Fz : firstn z (fword g)=fprefix g).
  { unfold fword,z. rewrite firstn_app,firstn_all,Nat.sub_diag,firstn_O,app_nil_r. reflexivity. }
  assert (Sz : skipn z (fword g)=ftail g).
  { unfold fword,z; rewrite skipn_app,skipn_all,Nat.sub_diag. reflexivity. }
  rewrite Fz,Sz,<-D,<-E,missing_terminal_unit in B.
  unfold switch_bound_front,real_loss.
  now rewrite Cap,(front_terminal_ext _ _ _ E Non).
Qed.
