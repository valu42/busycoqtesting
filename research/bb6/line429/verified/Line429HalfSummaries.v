(** One exact half-tape and all transition information of the opposite sweep
    test can still describe a tape that halts. Both examples start at a shape
    actually attained from blank and replace just one finite word. *)
From BusyCoq Require Import Individual62 Line429Engine Line429RightSweep Line429LeftLanguage
  Line429LeftDFA Line429Gate Line429GateBlank Line429ShapePrefix Line429GateSplice Line429MatchingGates Line429WordOrbit.
From Coq Require Import List.
Import ListNotations Bell429 LeftLanguage429 GateBlank429 ShapePrefix429 MatchingGates429.
Open Scope sym_scope.
Module HalfSummaries429.
Definition old_left s := WordOrbit429.trim (rest (west s)).
Definition old_right s := WordOrbit429.trim (east s).
Lemma shape s : st s=A -> under s=S1 -> here (west s)=S0 ->
  decode s = checkpoint (old_left s) (old_right s).
Proof.
  intros A1 B1 C1. unfold checkpoint, AR, old_left, old_right, decode.
  change ((st s,(west s *> 0inf,under s,east s *> 0inf)) = (A,(0 >> (WordOrbit429.trim (rest (west s)) *> 0inf),S1,(WordOrbit429.trim (east s) *> 0inf)))).
  rewrite !WordOrbit429.trim_ok, A1, B1. pose proof (unroll (west s)) as K. rewrite C1 in K. now rewrite K at 1.
Qed.

Definition at542 := Eval vm_compute in
  (match run 542 blank with Some s=>s | None=>blank end).
Definition at13814 := Eval vm_compute in
  (match run 13814 blank with Some s=>s | None=>blank end).
Lemma blank542 : (B;;tape0) -[src_tm]->> 542 / checkpoint (old_left at542) (old_right at542).
Proof. rewrite <- (shape at542 eq_refl eq_refl eq_refl). apply (run_sound _ blank); vm_compute; reflexivity. Qed.
Lemma blank13814 : (B;;tape0) -[src_tm]->> 13814 / checkpoint (old_left at13814) (old_right at13814).
Proof. rewrite <- (shape at13814 eq_refl eq_refl eq_refl). apply (run_sound _ blank); vm_compute; reflexivity. Qed.

Definition changed_left : list Sym := [1;0;0;0;0;0;1].
Definition changed_right : list Sym := [0;0;1;1;0;1].
Definition cp x z := mk A (S0::x) S1 z.

Theorem exact_right_insufficient : exists u x w,
  (B;;tape0) -[src_tm]->> 542 / checkpoint u w /\
  (forall q, LeftDFA429.feed q u=LeftDFA429.feed q x) /\
  halts_in src_tm (checkpoint x w) 140.
Proof.
  exists (old_left at542),changed_left,(old_right at542). split; [exact blank542|]. split.
  - intros [| | | | | | | |o]; reflexivity.
  - let s := constr:(cp changed_left (old_right at542)) in
    let term := eval vm_compute in (match run 140 s with Some t=>t | None=>blank end) in
    exists (decode term); split; [apply (run_sound 140 s); vm_compute; reflexivity|reflexivity].
Qed.
Theorem exact_left_insufficient : exists u w z,
  (B;;tape0) -[src_tm]->> 13814 / checkpoint u w /\
  (forall h a b suffix, Gate429.gate h a b (w++suffix)=Gate429.gate h a b (z++suffix)) /\
  halts_in src_tm (checkpoint u z) 202.
Proof.
  exists (old_left at13814),(old_right at13814),changed_right. split; [exact blank13814|]. split.
  - intros h a b suffix; destruct h,a,b; reflexivity.
  - let s := constr:(cp (old_left at13814) changed_right) in
    let term := eval vm_compute in (match run 202 s with Some t=>t | None=>blank end) in
    exists (decode term); split; [apply (run_sound 202 s); vm_compute; reflexivity|reflexivity].
Qed.
(** The five-round positive control uses the two genuine halves crossed in GateSplice429. *)
Example crossed_four : WordOrbit429.iterate 4 (GateSplice429.u,GateSplice429.w) =
  Some (GateSplice429.u93,GateSplice429.w93).
Proof. reflexivity. Qed.
Example crossed_five : WordOrbit429.iterate 5 (GateSplice429.u,GateSplice429.w) = None.
Proof. reflexivity. Qed.
End HalfSummaries429.
Print Assumptions HalfSummaries429.exact_right_insufficient.
Print Assumptions HalfSummaries429.exact_left_insufficient.
