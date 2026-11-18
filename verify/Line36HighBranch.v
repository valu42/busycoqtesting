(** Close the high-debt branch of the actual-front successor theorem. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Nonhalt Line36DeepFront Line36FrontCharge Line36Left.
Import ListNotations.
Local Open Scope Z_scope.

Theorem high_branch36 f h :
  fvalid f -> fcap36 f h -> 2844 <= credit36 (fledger36 f h) ->
  (29 <= fst (mark36 (skipn 3 (ftail f)) 0))%nat ->
  exists g j, fvalid g /\ step36 (fword f)=Some (fword g) /\ fcap36 g j /\
    credit36 (fledger36 f h)<=credit36 (fledger36 g j).
Proof.
  intros OK Cap Credit High.
  set (halo:=firstn 3 (ftail f)). set (ext:=skipn 3 (ftail f)) in *.
  assert (E : ftail f=halo++ext) by (unfold halo,ext; symmetry; apply firstn_skipn).
  assert (H3 : length halo=3%nat).
  { unfold halo. rewrite length_firstn. destruct OK as [_ [_ Ht]]. lia. }
  destruct (mark36 ext 0) as [d bits] eqn:M; cbn [fst] in High.
  pose proof (front_reserve36 f h OK Cap Credit) as Reserve.
  destruct (deep_front36 f halo ext d bits OK E H3 M High ltac:(lia))
    as [g [hi [V [Ph [S [Tail [Few [Dx Charge]]]]]]]].
  destruct (front_cap_step cap_checked_condition f g halo ext d bits false h
     (3-Z.of_nat d) OK E H3 M S Cap Charge) as [j [Cj [Hj [Hj' [Dc [Alt Db]]]]]].
  exists g,j. split; [exact V|]. split; [exact S|]. split; [exact Cj|].
  apply (credit36_step (fledger36 f h) (fledger36 g j) (3-Z.of_nat d)
     (Z.of_nat (L36CapInvariant.real_loss (fword f)))).
  - exact Db.
  - pose proof (L36Left.clipped_range L36LeftPotential.raw (fstate f)) as L.
    pose proof (L36Left.clipped_range L36LeftPotential.raw (fstate g)) as L'.
    change (L36LeftPotential.value (fstate g) - L36LeftPotential.value (fstate f) <=
      6*(Z.of_nat (length (fprefix g))-Z.of_nat (length (fprefix f)))-24*(3-Z.of_nat d)-4).
    unfold L36LeftPotential.value. lia.
  - change (-Z.of_nat h <= 3*Z.of_nat (L36CapInvariant.real_loss (fword f))-1+ -Z.of_nat j).
    lia.
  - exact Alt.
Qed.
