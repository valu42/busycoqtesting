(** High-demand one-step invariant on actual protected machine fronts. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Front Line36Cut Line36Cover Line36Deep
  Line36Splice Line36HighDebt Line36Safety Line36Word Line36Right Line36Halo Line36Seed.
Import ListNotations L36Tiles L36Cut L36Splice L36Deep.
Local Open Scope Z_scope.

Lemma deep_last_mask p halo d :
  length halo=3%nat -> (3<=d)%nat ->
  let '(g,bits) := mark36 (p++halo) d in last bits (Nat.eqb g 1)=false.
Proof.
 intros L D. pose proof (L36HighDebt.halo_erased halo d ltac:(lia)) as [Hm _].
 rewrite mark36_app. destruct (mark36 halo d) as [k m]; cbn [snd] in Hm. subst m.
 destruct (mark36 p k) as [g b]. now rewrite last36_app,L.
Qed.

Lemma deep_split_image p halo ext d bits :
  length halo=3%nat -> (3<=d)%nat -> mark36 ext 0=(d,bits) ->
  (fst (mark36 (p++halo) d)<6)%nat ->
  step36 ((p++halo)++ext)=Some (protected_output (p++halo) d ++ body36 false bits).
Proof.
  intros Hh Hd M G.
  pose proof (deep_last_mask p halo d Hh Hd) as Last.
  unfold step36,protected_output. rewrite mark36_app,M.
  destruct (mark36 (p++halo) d) as [g b]. cbn [fst] in G.
  apply Nat.ltb_lt in G; rewrite G.
  unfold output36,body36,carry36. rewrite deriv36_app,last36_app,Last.
  now repeat rewrite <-app_assoc.
Qed.

Lemma phase_guard_bound ph : (ph<6)%nat -> (phase_guard ph<6)%nat.
Proof. intros Hp; cases_six ph; vm_compute; lia. Qed.

Lemma body_length_at_least prev bits : (length bits <= length (body36 prev bits))%nat.
Proof. unfold body36; rewrite length_app, derivative_length. lia. Qed.

Theorem deep_front36 f halo ext d bits :
  fvalid f -> ftail f=halo++ext -> length halo=3%nat -> mark36 ext 0=(d,bits) ->
  (29<=d)%nat ->
  52 <= Z.of_nat (length (fprefix f))-4*Z.of_nat (L36Seed.budget (fprefix f) (ftail f)) ->
  exists g hi,
    fvalid g /\ fphase g=next (fphase f) /\ step36 (fword f)=Some (fword g) /\
    ftail g=hi++body36 false bits /\ (closing_count hi<=1)%nat /\
    -2*Z.of_nat d-27 <= Z.of_nat (length (fprefix g))-Z.of_nat (length (fprefix f)) /\
    (forall pre cap, ext=pre++false::cap -> In true bits ->
      Z.of_nat (L36Seed.budget (fprefix g) (ftail g)) <=
      Z.of_nat (L36Seed.budget (fprefix f) (ftail f)) + (3-Z.of_nat d) +
      Z.of_nat (bit_cost (negb (last bits false)))- Z.of_nat (cap_loss cap)).
Proof.
  intros [Hp [Hl Ht]] E Hh M D R.
  pose proof (tail_budget_debt36 (fprefix f) (ftail f)) as K.
  rewrite E,mark36_app,M in K. destruct (mark36 halo d) as [k m] eqn:Hm.
  cbn [fst] in K.
  assert (A : (fst (mark36 halo d)<=L36Seed.budget (fprefix f) (ftail f)+1)%nat).
  { rewrite Hm,E. cbn [fst]. lia. }
  destruct (deep_covered_step _ (fdata f) halo d
    (L36Seed.budget (fprefix f) (ftail f)) Hp (canonical_covered _ _ _ _) Hh D R A)
     as [nd [b [rlen [C [G [O [Dx _]]]]]]].
  fold (fprefix f) in G,O,Dx.
  pose proof (next_bound _ Hp) as Hnext.
  destruct (covered_cut _ _ Hnext C) as [cs [mode [len [B N]]]].
  set (exposed := b::repeat true (rlen+3)).
  set (g := Front36 (next (fphase f)) cs mode len (exposed++body36 false bits)).
  assert (P : fprefix g=phase_prefix (next (fphase f))++nd).
  { unfold fprefix,fdata,fpart,fkind,g; cbn [fphase fchoices foption flen]; now rewrite N. }
  assert (T : ftail g=exposed++body36 false bits) by reflexivity.
  assert (Few : (closing_count exposed<=1)%nat).
  { apply (suffix_of_flat_output b (rlen+3) [] exposed); reflexivity. }
  assert (LB := mark36_length ext 0). rewrite M in LB; cbn [snd] in LB.
  assert (Valid : fvalid g).
  { split; [exact Hnext|]. split; [exact B|]. rewrite T,length_app.
    pose proof (body_length_at_least false bits). unfold exposed.
    cbn [length]. rewrite repeat_length. rewrite E,length_app,Hh in Ht. lia. }
  assert (S : step36 (fword f)=Some (fword g)).
  { unfold fword. rewrite E,app_assoc,deep_split_image with (d:=d) (bits:=bits)
       by (assumption || lia || (rewrite G; now apply phase_guard_bound)).
    rewrite O,P,T. f_equal. now rewrite <-app_assoc. }
  exists g,exposed. split; [exact Valid|]. split; [reflexivity|]. split; [exact S|].
  split; [exact T|]. split; [exact Few|]. split; [now rewrite P|].
  intros pre cap Ec Live.
  unfold L36Seed.budget. rewrite !tail_charge_gap36,T,E,Ec.
  rewrite Ec in M. now apply halo_high_debt; [exact M|exact Live|lia|exact Few].
Qed.
