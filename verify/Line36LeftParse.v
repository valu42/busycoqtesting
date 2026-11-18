From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Left Line36LeftStep Line36LeftPotential Line36LeftCheck Line36Tiles Line36Matching.
Import ListNotations L36Left L36Tiles L36LeftStep L36LeftGroups.
Local Open Scope nat_scope.

Module L36LeftParse.
Lemma read_piece_spec p w :
  let '(n,r) := read_piece p w in
  n <= length w /\
  match r with Some rest => n = length p /\ length w = n + length rest
             | None => n < length p end.
Proof.
  revert w. induction p as [|b p IH]; intros [|a w]; cbn [read_piece length]; try lia.
  destruct (Bool.eqb b a); [|lia].
  specialize (IH w). destruct (read_piece p w) as [n [r|]];
   cbn [length] in *; lia.
Qed.

Lemma parse_bounds gas ph k n b pos w p :
  k < 6 -> reparse gas ph k n b pos w = Some p ->
  next_kind p < 6 /\ partial p < length (piece ph (next_kind p) (next_bit p)) /\
  cut p <= pos+length w.
Proof.
  revert k n b pos w p. induction gas as [|gas IH]; intros k n b pos w p K R;
  cbn [reparse] in R; [discriminate|].
  pose proof (read_piece_spec (piece ph k false) w) as E0.
  destruct (read_piece (piece ph k false) w) as [len0 [rest0|]].
  - specialize (IH _ _ _ _ _ _ (Nat.mod_upper_bound (S k) 6 ltac:(lia)) R).
    lia.
  - pose proof (read_piece_spec (piece ph k true) w) as E1.
    destruct (read_piece (piece ph k true) w) as [len1 [rest1|]].
    + specialize (IH _ _ _ _ _ _ (Nat.mod_upper_bound (S k) 6 ltac:(lia)) R).
      lia.
    + destruct (len0 <? len1); inversion R; cbn; lia.
Qed.

Lemma encode_halo_bound w : encode_halo w <= 8.
Proof.
  destruct w as [|[] [|[] [|[] r]]]; reflexivity || (cbn; lia).
Qed.

Theorem step_success_wf s hist d e :
  phase s < 6 -> step s hist d = Some e ->
  well_formed (target e) /\ (dx e <= Z.of_nat (phase_header (phase s)))%Z.
Proof.
  intro Bounded. unfold step, evaluate. set (c := prepare s hist).
  set (t := phase s). set (pn := S t mod 6).
  destruct (mark36 (full c) d) as [g bits].
  destruct (negb (g =? phase_guard t)) eqn:E; [discriminate|].
  apply Bool.negb_false_iff, Nat.eqb_eq in E.
  set (out := physical_header g ++ derivative (g =? 1) bits).
  set (w := firstn (x c + length (physical_header g)) out).
  pose proof (read_piece_spec (pre pn) w) as Pre.
  destruct (read_piece (pre pn) w) as [np [r|]]; [|discriminate].
  destruct (reparse 24 pn 0 0 false np r) as [p|] eqn:P; [|discriminate].
  destruct (complete p <? piece_count (kind s) - 4); [discriminate|].
  set (hi := skipn (cut p) out).
  destruct (encode_halo hi =? 8) eqn:H; [discriminate|].
  destruct (scan hi _ _ 0) as [a k].
  intros R. inversion R; subst e. cbn [target dx].
  pose proof (parse_bounds 24 pn 0 0 false np r p ltac:(lia) P) as B.
  apply Nat.eqb_neq in H. pose proof (encode_halo_bound hi).
  assert (PN : pn < 6) by (unfold pn; apply Nat.mod_upper_bound; lia).
  split; [unfold well_formed; cbn [phase kind last_choice partial_choice partial_len halo]; lia|].
  assert (W : length w <= x c + length (physical_header g)) by
    (unfold w; rewrite firstn_length; lia).
  assert (HG : length (physical_header g) = phase_header t).
  { change (t < 6) in Bounded. subst g. unfold phase_guard, phase_header.
    destruct t as [|[|[|[|[|[|t ]]]]]]; try reflexivity; lia. }
  lia.
Qed.
End L36LeftParse.
