(** The actual finite-debt branch of the nonhalting invariant. *)
From Coq Require Import List Arith ZArith Lia.
From BusyCoq Require Import Line36Nonhalt Line36FrontContext Line36LowFront
  Line36FrontCharge Line36Left Line36LeftStep Line36LeftCheck Line36Charge.
Import L36Left L36LeftStep L36LeftGroups.
Local Open Scope Z_scope.

Lemma low_branch36
  (certificate : forall s hist d,
    well_formed s -> (hist < 16)%nat -> (d < 29)%nat ->
    exists e, step s hist d = Some e /\ well_formed (target e) /\
      dx e <= Z.of_nat (L36Tiles.phase_header (phase s)) /\
      L36LeftPotential.value (target e) - L36LeftPotential.value s <= weight e)
  f h : fvalid f -> fcap36 f h -> 2844 <= credit36 (fledger36 f h) ->
  (fst (mark36 (skipn 3 (ftail f)) 0) < 29)%nat ->
  exists g j, fvalid g /\ step36 (fword f) = Some (fword g) /\
    fcap36 g j /\ credit36 (fledger36 f h) <= credit36 (fledger36 g j).
Proof.
  intros F Hcap Credit Small.
  set (halo := firstn 3 (ftail f)).
  set (ext := skipn 3 (ftail f)) in *.
  set (d := fst (mark36 ext 0)) in *.
  destruct (front_tail36 f F) as [Split [Three Wide]].
  fold halo ext in Split, Three, Wide.
  destruct (front_context36 f F (front_reserve36 f h F Hcap Credit))
    as [Wf [Pieces [w' S]]].
  destruct (low_front36 f w' F Pieces S ltac:(fold ext d; lia)) as [hist [I T]].
  destruct (certificate (fstate f) hist d Wf I Small) as [e [Edge [_ [_ Bound]]]].
  destruct (T e Edge) as (g & hi & rest & G & Word & State & _ & _ & _ & Known & Guard & Dx & C).
  fold ext d halo in Known, Guard, C.
  rewrite <- Word in S.
  pose proof (front_cut_charge cap_checked_condition f g halo ext hi d h
    F G Split Three eq_refl Known S Hcap) as Cap.
  cbv zeta in Cap. rewrite Guard, <- C in Cap.
  destruct Cap as [j [Next [_ [_ [Move [Flip Cost]]]]]].
  exists g,j. split; [exact G|]. split; [exact S|]. split; [exact Next|].
  apply (credit36_step (fledger36 f h) (fledger36 g j) (charge e)
     (Z.of_nat (L36CapInvariant.real_loss (fword f)))).
  - exact Cost.
  - change (L36LeftPotential.value (fstate g) - L36LeftPotential.value (fstate f) <=
      6 * (Z.of_nat (length (fprefix g)) - Z.of_nat (length (fprefix f))) - 24 * charge e - 4).
    rewrite State, <- Dx. exact Bound.
  - change (-Z.of_nat h <= 3*Z.of_nat (L36CapInvariant.real_loss (fword f))-1+ -Z.of_nat j).
    lia.
  - exact Flip.
Qed.
