(** Closed, replayable witnesses for the left cut and the right caps. *)
From Coq Require Import Lists.List Bool.Bool Arith.PeanoNat Strings.String
                        NArith.BinNat PArith.BinPos.
From BusyCoq Require Import Line36Machine Line36Tiles.
Import ListNotations.
Local Open Scope list_scope.

Module L36Seed.

(** Each group of six choices is one complete tile in phase zero. *)
Definition choices0 := [true; false; true; false; true; true].
Definition choices1 := [false; false; false; false; true; true].
Definition choices2 := [true; true; true; true; true; true].
Definition choices := choices0 ++ choices1 ++ choices2.
Definition protected := L36Tiles.phase_prefix 0 ++ L36Tiles.segments 0 0 choices.
Definition tail := skipn 530 line36_blank_seed.

Theorem three_tiles :
  List.length choices0 = 6 /\ List.length choices1 = 6 /\ List.length choices2 = 6 /\
  protected = L36Tiles.phase_prefix 0 ++ L36Tiles.segments 0 0 choices0 ++
              L36Tiles.segments 0 0 choices1 ++ L36Tiles.segments 0 0 choices2.
Proof. vm_compute. repeat split. Qed.

Theorem actual_cut :
  line36_blank_seed = protected ++ tail /\
  List.length protected = 530 /\ List.length tail = 505 /\
  firstn 3 tail = [true;true;true].
Proof. vm_compute. repeat split. Qed.

(** The dummy is the last protected closing. Its initial fallback is position
    -1, of odd parity. On exhausting the tail, the terminal sentinel has the
    parity of the position immediately before the current one. *)
Fixpoint last_color (w : list bool) (next_odd previous_odd : bool) : bool :=
  match w with
  | [] => previous_odd
  | b :: rest => last_color rest (negb next_odd) (if b then previous_odd else next_odd)
  end.

Definition change (a b : bool) : nat := if xorb a b then 1 else 0.

Fixpoint tail_charge (w : list bool) (next_odd previous_odd : bool) : nat :=
  match w with
  | [] => change previous_odd (negb next_odd)
  | true :: rest => tail_charge rest (negb next_odd) previous_odd
  | false :: rest => change previous_odd next_odd + tail_charge rest (negb next_odd) next_odd
  end.

Definition budget (p t : list bool) : nat :=
  tail_charge t (Nat.odd (List.length p)) (last_color p false true).

Theorem seed_budget :
  last_color protected false true = true /\
  last_color line36_blank_seed false true = true /\
  budget protected tail = 7 /\ List.length protected - 4 * budget protected tail = 502.
Proof. vm_compute. repeat split. Qed.

Definition epoch32_word := read_digits
  "22112111121121112121211111112111212121212121211121212111221211121211111121211121221221112112"%string.
Definition result32 : finite36 := (A, ([], S0, map data_symbol epoch32_word ++ [S0])).

Theorem epoch32_reached :
  multistep line36 (literal_count 5319%positive) c0 (checkpoint epoch32_word).
Proof.
  assert (E : literal_run 5319%positive (Some starting) = Some result32)
    by (vm_compute; reflexivity).
  pose proof (literal_run_records 5319%positive (Some starting)) as H.
  rewrite E in H.
  change (multistep line36 (literal_count 5319%positive) (lift starting) (lift result32)) in H.
  replace (lift result32) with (checkpoint epoch32_word) in H.
  - now rewrite lift_starting in H.
  - unfold result32, checkpoint, finite_checkpoint, lift, lift_tape.
    now rewrite lift_side_trailing_blank.
Qed.

Definition cap50 (w : list bool) := skipn (List.length w - 50) w.
Definition seed_cap32 := read_digits "21211121212111221211121211111121211121221221112112"%string.
Definition seed_cap331 := read_digits "21211121112111211121111121212121211111221211112111"%string.

(** Encoding used by the right-hand integer graph. Bit zero is the rightmost
    cell and each bit is set exactly for a closing. *)
Definition pack (w : list bool) : N :=
  fold_left (fun (acc : N) (opening : bool) => if opening then N.double acc else N.succ_double acc) w 0%N.

Theorem exact_caps :
  List.length epoch32_word = 92 /\
  List.length seed_cap32 = 50 /\ List.length seed_cap331 = 50 /\
  cap50 epoch32_word = seed_cap32 /\ cap50 line36_blank_seed = seed_cap331 /\
  pack seed_cap32 = 715288484654473%N /\ pack seed_cap331 = 713069842533640%N.
Proof. vm_compute. repeat split. Qed.

(** Count nonempty normal-form visits, inspecting the entire used tape.
    An unused blank suffix, including an explicitly stored one, is allowed. *)
Definition is_blank (s : sym) : bool :=
  match s with S0 => true | _ => false end.

Fixpoint data_then_blanks (r : list sym) : bool :=
  match r with
  | [] => true
  | (S1 :: xs) | (S2 :: xs) => data_then_blanks xs
  | S0 :: xs => forallb is_blank xs
  | _ => false
  end.

Definition at_nonempty_checkpoint (c : finite36) : bool :=
  match c with
  | (A, (l, S0, (S1 :: r))) | (A, (l, S0, (S2 :: r))) =>
      andb (forallb is_blank l) (data_then_blanks r)
  | _ => false
  end.

Definition count_one (ck : option finite36 * nat) : option finite36 * nat :=
  let '(o,k) := ck in
  let t := advance_one o in
  (t, match t with
      | Some c => if at_nonempty_checkpoint c then S k else k
      | None => k
      end).

Fixpoint counted_run (n : positive) (ck : option finite36 * nat) : option finite36 * nat :=
  match n with
  | xH => count_one ck
  | xO p => counted_run p (counted_run p ck)
  | xI p => count_one (counted_run p (counted_run p ck))
  end.

Lemma counted_preserves_run n ck :
  fst (counted_run n ck) = literal_run n (fst ck).
Proof.
  induction n as [n IH|n IH|] in ck |- *; cbn [literal_run counted_run].
  - destruct (counted_run n (counted_run n ck)) as [o k] eqn:E.
    change (advance_one o = advance_one (literal_run n (literal_run n (fst ck)))). f_equal.
    change (fst (o,k) = literal_run n (literal_run n (fst ck))). rewrite <- E. now rewrite !IH.
  - now rewrite !IH.
  - destruct ck. reflexivity.
Qed.

Theorem checkpoint_ordinals :
  snd (counted_run 5319%positive (Some starting,0)) = 32 /\
  snd (counted_run 612729%positive (Some starting,0)) = 331.
Proof. vm_compute. split; reflexivity. Qed.

End L36Seed.
