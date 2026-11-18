(** A large exterior demand changes exactly one derivative digit and leaves
    only openings to its right, up to the end of the known halo. *)
From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Word Line36Tiles Line36TileShield Line36HighDebt.
Import ListNotations L36Tiles L36TileShield L36HighDebt.
Local Open Scope Z_scope.

Module L36Splice.

Definition protected_output (w : list bool) (d : nat) : list bool :=
  let '(g, bits) := mark36 w d in guard36 g ++ deriv36 (Nat.eqb g 1) bits.

Lemma guard_nonempty g : (1 <= length (guard36 g))%nat.
Proof. destruct g as [|[|[|[|[|g]]]]]; simpl; lia. Qed.

Lemma length_balance_even w :
  exists q, Z.of_nat (length w) - bal36 w = 2*q.
Proof.
  induction w as [|b r [q H]].
  - exists 0; reflexivity.
  - destruct b; [exists q|exists (q+1)]; cbn [length bal36]; rewrite Nat2Z.inj_succ; lia.
Qed.

Theorem large_debt_splice ph start choices kref rchoices data old reference_tail halo d :
  (ph < 6)%nat ->
  factor data (tiles_word ph start choices) ->
  factor reference_tail (tiles_word ph kref rchoices) ->
  length halo = 3%nat -> (29 <= d)%nat ->
  (fst (mark36 halo d) <= openings36 (snd (mark36 data 0)))%nat ->
  let q := fst (mark36 reference_tail 0) in
  let k := fst (mark36 halo d) in
  let guard := fst (mark36 (old++data) q) in
  exists common changed rest relevant_len,
    fst (mark36 ((old++data)++halo) d) = guard /\
    protected_output (old++data) q = common ++ changed :: rest /\
    protected_output ((old++data)++halo) d =
      common ++ negb changed :: repeat true (relevant_len + length halo) /\
    (* The matcher may retain at least [common]. Its endpoint is within
       the inspected part, and moving to this endpoint loses at most 2d+27. *)
    (length common + S relevant_len = length (guard36 guard) + length (old++data))%nat /\
    -2 * Z.of_nat d - 27 <= Z.of_nat (length common) - Z.of_nat (length (old++data)) /\
    (* If the flipped digit is a closing, its normalized label already
       equals the terminal label, so it costs no additional switch. *)
    Z.Even (Z.of_nat (length (old++data++halo)) + Z.of_nat d
          - (Z.of_nat (length common) - Z.of_nat (length (guard36 guard)))).
Proof.
  intros Hp F Fr Hh Hd Havailable.
  cbn zeta.
  set (q := fst (mark36 reference_tail 0)).
  assert (Hq : (q<=11)%nat) by (apply (continuation_debt_le_eleven ph kref rchoices); auto).
  pose proof (halo_erased halo d ltac:(lia)) as [Zeros Bhalo].
  pose proof (erased_halo_bounds halo d Hh Hd) as Kbounds.
  destruct (mark36 halo d) as [k mk] eqn:Mh; cbn [fst snd] in *; subst mk.
  destruct (rank_splice ph start choices data old q k Hp F ltac:(lia))
    as [l [r [g [pre [rb [E [L [Br [Mr [Ma Lpre]]]]]]]]]].
  destruct (deriv_splice (Nat.eqb g 1) pre rb (length r+length halo))
    as [common [changed [rest [Dr [Da Lc]]]]].
  assert (M : mark36 ((old++data)++halo) d =
        (g, pre++repeat false (S (length r + length halo)))).
  { rewrite mark36_app, Mh, Ma. f_equal. rewrite <- app_assoc.
    rewrite <- repeat_app. reflexivity. }
  exists (guard36 g ++ common),changed,rest,(length r).
  rewrite Mr; cbn [fst].
  split; [now rewrite M|].
  split; [unfold protected_output; rewrite Mr,Dr; apply app_assoc|].
  split; [unfold protected_output; rewrite M,Da; apply app_assoc|].
  pose proof (guard_nonempty g).
  pose proof (length_balance_even (true::r)) as [u U].
  pose proof (length_balance_even halo) as [v V].
  rewrite E. rewrite !length_app, Lc, Lpre.
  cbn [length] in *. rewrite ?Nat2Z.inj_succ in *.
  split; [lia|]. split; [lia|].
  exists (u+v+Z.of_nat d). lia.
Qed.

End L36Splice.
