(** Closing the physical blank-run proof from a successor at each real frontier. *)
From Coq Require Import List Bool ZArith Lia.
From BusyCoq Require Export Line36CapCertificate Line36CapInvariant
  Line36FrontSeed Line36Safety Line36Physical Line36Front Line36Machine
  Line36Seed Line36Left Line36LeftPotential Line36Tiles Line36Cover Line36Cap
  Line36Word Line36Cut.
Import ListNotations.
Local Open Scope Z_scope.

Definition fcap36 (f : front36) (h : nat) : Prop :=
  cap_value (L36Seed.cap50 (fword f)) = Some h.

Definition fledger36 (f : front36) (h : nat) : ledger36 :=
  Ledger36 (Z.of_nat (length (fprefix f)))
           (Z.of_nat (L36Seed.budget (fprefix f) (ftail f)))
           (L36LeftPotential.value (fstate f)) (- Z.of_nat h)
           (L36CapInvariant.terminal_bit (fword f)).

Definition front_successor36 : Prop :=
  forall f h, fvalid f -> fcap36 f h -> 2844 <= credit36 (fledger36 f h) ->
  exists g j, fvalid g /\ step36 (fword f) = Some (fword g) /\
              fcap36 g j /\ credit36 (fledger36 f h) <= credit36 (fledger36 g j).

Lemma front_width36 f : fvalid f -> (50 < length (fword f))%nat.
Proof. intros [_ [_ H]]. unfold fword. rewrite length_app. lia. Qed.

Lemma fledger_range36 f h : fvalid f -> fcap36 f h -> in_range36 (fledger36 f h).
Proof.
  intros OK V. pose proof (front_width36 f OK) as W.
  pose proof (L36CapInvariant.real_cap_features cap_checked_condition (fword f) h W V) as [Bound _].
  pose proof (L36Left.clipped_range L36LeftPotential.raw (fstate f)) as Left.
  unfold in_range36, fledger36; cbn [left_potential36 cap_potential36 terminal36].
  unfold L36LeftPotential.value. unfold L36CapInvariant.terminal_bit.
  destruct (last (fword f) false); lia.
Qed.

Lemma front_reserve36 f h : fvalid f -> fcap36 f h ->
  2844 <= credit36 (fledger36 f h) ->
  454 <= Z.of_nat (length (fprefix f)) - 4 * Z.of_nat (L36Seed.budget (fprefix f) (ftail f)).
Proof.
  intros OK V C. exact (credit36_safe _ (fledger_range36 f h OK V) C).
Qed.

Lemma actual_front_step36 f h :
  fvalid f -> fcap36 f h -> 2844 <= credit36 (fledger36 f h) ->
  exists out, step36 (fword f) = Some out /\
              progress line36 (checkpoint (fword f)) (checkpoint out).
Proof.
  intros OK V Credit.
  pose proof (front_reserve36 f h OK V Credit) as N.
  destruct OK as [Phase _].
  apply (reserve_sweep36 (fphase f) (fdata f) (ftail f) Phase).
  - exact (L36Cut.canonical_covered (fphase f) (fchoices f) (foption f) (flen f)).
  - change (52 <= Z.of_nat (length (fprefix f)) -
                   4 * Z.of_nat (L36Seed.budget (fprefix f) (ftail f))). lia.
Qed.

(** Once either debt branch supplies its switch bound and the left potential
    inequality, all the right-hand and temporal bounds follow from the real
    tape. No cap value has to be guessed for that branch. *)
Lemma common_front_gain36 f g h C :
  fvalid f -> fcap36 f h -> step36 (fword f) = Some (fword g) ->
  Z.of_nat (L36Seed.budget (fprefix g) (ftail g)) <=
    Z.of_nat (L36Seed.budget (fprefix f) (ftail f)) + C +
      (1 - L36CapInvariant.terminal_bit (fword f)) -
      Z.of_nat (L36CapInvariant.real_loss (fword f)) ->
  L36LeftPotential.value (fstate g) - L36LeftPotential.value (fstate f) <=
    6 * (Z.of_nat (length (fprefix g)) - Z.of_nat (length (fprefix f))) - 24*C - 4 ->
  exists j, fcap36 g j /\ credit36 (fledger36 f h) <= credit36 (fledger36 g j).
Proof.
  intros OK Val Sweep Switches Left.
  pose proof (front_width36 f OK) as Wide.
  destruct (L36CapInvariant.real_cap_step cap_checked_condition
     (fword f) (fword g) h Wide Val Sweep)
    as [j [Next [_ [_ [_ [Bound Final]]]]]].
  exists j; split; [exact Next|].
  eapply (credit36_step _ _ C (Z.of_nat (L36CapInvariant.real_loss (fword f))));
    cbn [fledger36 cut36 switches36 left_potential36 cap_potential36 terminal36]; lia.
Qed.

Lemma seed_credit36 :
  fvalid L36FrontSeed.seed /\ fcap36 L36FrontSeed.seed 5 /\
  credit36 (fledger36 L36FrontSeed.seed 5) = 2984.
Proof.
  destruct L36FrontSeed.exact_front as [Width [_ [Charge [_ [L [R T]]]]]].
  split; [apply L36FrontSeed.valid_seed|]. split; [exact R|].
  unfold credit36, fledger36; cbn [cut36 switches36 left_potential36 cap_potential36 terminal36].
  now rewrite Width, Charge, L, T.
Qed.

(** In particular the only machine-specific premise below, [front_successor36],
    is about actual finite tape words and their concrete frontier witnesses. *)
Theorem line36_nonhalt_from_successor : front_successor36 -> ~halts line36 c0.
Proof.
  intro Next.
  eapply (line36_checkpoint_nonhalting
    (fun w => exists f h, fword f = w /\ fvalid f /\ fcap36 f h /\
                                  2844 <= credit36 (fledger36 f h))).
  - exists L36FrontSeed.seed, 5%nat. split; [apply L36FrontSeed.exact_word|].
    destruct seed_credit36 as [OK [V Credit]]. split; [exact OK|]. split; [exact V|]. rewrite Credit. lia.
  - intros w [f [h [Same [OK [V Credit]]]]].
    destruct (Next f h OK V Credit) as [g [j [Valid [Step [Cap Gain]]]]].
    exists (fword g); split.
    + rewrite <- Same. now apply step36_physical.
    + exists g,j. split; [reflexivity|]. split; [exact Valid|]. split; [exact Cap|lia].
Qed.
