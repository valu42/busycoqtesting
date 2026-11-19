From BusyCoq Require Import Individual62 Line448Engine.
Require Import Line448Sweeps ChunkTools.
Require S0 Part0 Part1 Part2 Part3 Part4 J245760 J249856 J253952 J258048 J262144 J266240 J270336 J274432 J278528 J282624 J286720 J290816 J294912 J299008 J303104 J307200 J311296 J315392 J319488 J323584 J327680 J331776 J335872 J339968 J344064 J348160 J352256 J356352 J360448 J364544 J368640 J372736 J376832 J380928 J385024 J389120 J393216 J395264 J397312 J399360 J401408 J403456 J405504 J407552 J409600 J411648 J413696 J415744 J417792 J419840 J421888 Part17.
From Coq Require Import List.
Import ListNotations.

Module E := Line448Engine.H155900.

(* The shared T4 engine uses a reflected tape. Its C is this machine's A. *)
Definition rename448 (q : Q) : Q :=
  match q with
  | A => C | B => D | C => A | D => B | E => E | F => F
  end.

Lemma table448 : Perm (flip E.src_tm) line448 rename448.
Proof.
  split.
  - intros q b H. destruct q, b; cbv in H |- *; try discriminate; reflexivity.
  - intros q b b' d q' H. destruct q, b; cbv in H |- *; inversion H; subst; reflexivity.
Qed.


Theorem line448_halts : halts line448 c0.
Proof.
  assert (H : halts E.src_tm (C;; tape0)).
  { change (halts E.src_tm (E.fs_denote S0.checkpoint)).
    apply Part0.segment.
    apply Part1.segment.
    apply Part2.segment.
    apply Part3.segment.
    apply Part4.segment.
    apply J245760.segment.
    apply J249856.segment.
    apply J253952.segment.
    apply J258048.segment.
    apply J262144.segment.
    apply J266240.segment.
    apply J270336.segment.
    apply J274432.segment.
    apply J278528.segment.
    apply J282624.segment.
    apply J286720.segment.
    apply J290816.segment.
    apply J294912.segment.
    apply J299008.segment.
    apply J303104.segment.
    apply J307200.segment.
    apply J311296.segment.
    apply J315392.segment.
    apply J319488.segment.
    apply J323584.segment.
    apply J327680.segment.
    apply J331776.segment.
    apply J335872.segment.
    apply J339968.segment.
    apply J344064.segment.
    apply J348160.segment.
    apply J352256.segment.
    apply J356352.segment.
    apply J360448.segment.
    apply J364544.segment.
    apply J368640.segment.
    apply J372736.segment.
    apply J376832.segment.
    apply J380928.segment.
    apply J385024.segment.
    apply J389120.segment.
    apply J393216.segment.
    apply J395264.segment.
    apply J397312.segment.
    apply J399360.segment.
    apply J401408.segment.
    apply J403456.segment.
    apply J405504.segment.
    apply J407552.segment.
    apply J409600.segment.
    apply J411648.segment.
    apply J413696.segment.
    apply J415744.segment.
    apply J417792.segment.
    apply J419840.segment.
    apply J421888.segment.
    apply Part17.segment.
    exact I. }
  apply flip_halts in H.
  change (flip_conf (C;; tape0)) with (C;; tape0) in H.
  exact (perm_halts _ _ _ _ _ table448 H).
Qed.
Print Assumptions line448_halts.
