(** Every finite-debt concrete transition obeys the integer potential bound.
    Each of the six constituent proofs recomputes all corresponding histories
    using the physical mask and the explicit advancing parse. *)
From Coq Require Import Arith ZArith Lia.
From BusyCoq Require Import Line36Tiles Line36Left Line36LeftStep Line36LeftPotential Line36LeftCheck
   Line36LeftParse Line36LeftPhase0 Line36LeftPhase1 Line36LeftPhase2
   Line36LeftPhase3 Line36LeftPhase4 Line36LeftPhase5.
Import L36Left L36LeftStep L36LeftPotential L36LeftCheck L36LeftGroups L36LeftParse.
Module L36LeftCertificate.

Theorem every_phase ph : (ph < 6)%nat -> check_phase ph = true.
Proof.
  destruct ph as [|[|[|[|[|[|n]]]]]]; intros B.
  - exact certified_phase0.
  - exact certified_phase1.
  - exact certified_phase2.
  - exact certified_phase3.
  - exact certified_phase4.
  - exact certified_phase5.
  - lia.
Qed.

Theorem finite_step s hist d :
  well_formed s -> (hist<16)%nat -> (d<29)%nat ->
  exists e, step s hist d = Some e /\ well_formed (target e) /\
    (dx e <= Z.of_nat (L36Tiles.phase_header (phase s)))%Z /\
    (value (target e) - value s <= weight e)%Z.
Proof.
  intros W H D. pose proof W as W'. destruct W' as [P _].
  pose proof (checked_phase s (every_phase _ P) W) as C.
  destruct (check_one_sound _ _ _ C H D) as [e [S I]].
  pose proof (step_success_wf _ _ _ _ P S) as [T X].
  exists e. auto.
Qed.
(** For a larger incoming debt, the analytic displacement and charge bounds
    cover any pair of states, including a newly selected legal cut. *)
Theorem unbounded_step s t displacement fee d :
  (29 <= d)%Z -> (-2*d-27 <= displacement)%Z -> (fee <= 3-d)%Z ->
  (value t - value s <= weight (Edge t displacement fee))%Z.
Proof.
  intros D X C. apply (edge_ok_sound value s (Edge t displacement fee)).
  apply (deep_edge raw s (Edge t displacement fee) d D).
  unfold weight. cbn [dx charge]; lia.
Qed.
End L36LeftCertificate.
