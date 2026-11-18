(** Verification independent of the program that generates the packed witness.
    A terminal value [Some v] stands for the integer potential [-v].
    At a branching node, openings take its low child and closings its high
    child. Traverse a physical cap from its rightmost cell to its leftmost. *)
From Coq Require Import Bool List Arith PArith Uint63 PArray.
From BusyCoq Require Import Line36Matching Line36Right Line36CapModel Line36CapData.

Local Open Scope uint63_scope.
(** Two levels of primitive arrays store the children of each node. *)
Definition cap_table := cap_chunks.
Definition cap_root : int := 1342830.
Definition child (node : int) (opening : bool) :=
  let bits := PArray.get (PArray.get cap_table (node >> 12)) (node land 4095) in
  if opening then bits land 2097151 else bits >> 21.
Definition cap_dead (node : int) := PrimInt63.eqb node 0.
Close Scope uint63_scope.

Definition leaf_values : array (option nat) :=
 [| None; Some 0; Some 1; Some 2; Some 3; Some 4; Some 5; Some 6; Some 7;
    Some 8; Some 9; Some 10; Some 11; Some 12; Some 13; Some 14; Some 15;
    Some 16; Some 17; Some 18; Some 19; Some 20; Some 21 | None |].
Import ListNotations.
Fixpoint cap_read (input : list bool) (node : int) : option nat :=
  if cap_dead node then None else
  match input with
  | [] => PArray.get leaf_values node
  | b::rest => cap_read rest (child node b)
  end.
Definition cap_value (physical : list bool) := cap_read (rev_append physical []) cap_root.
Definition bounded_successor (current cancellations : nat) (following : list bool) :=
  match cap_value following with
  | Some v => Nat.leb (S v) (current + 3*cancellations)
  | None => false
  end.
Definition cap_condition (w : list bool) (v : nat) :=
  let '(d, bits) := mark36 w 0 in
  let c := cap_loss (cap_after_anchor w) in
  let update := fun previous =>
    let ds := cap_deriv (andb previous (Nat.eqb d 0)) bits in
    if last w false then tl ds ++ [false] else ds in
  Nat.leb v 21 && existsb id bits && existsb negb w &&
  bounded_successor v c (update false) &&
  (if Nat.eqb d 0 && negb (last w false)
   then bounded_successor v c (update true) else true).
(** A zero child excludes all words below it. At an accepted leaf the
    accumulated word already has physical left-to-right order. *)
Fixpoint check_tree (n : nat) (w : list bool) (node : int) : bool :=
  if cap_dead node then true else
  match n with
  | O => match PArray.get leaf_values node with
         | Some v => cap_condition w v | None => true end
  | S m => if check_tree m (true :: w) (child node true)
           then check_tree m (false :: w) (child node false) else false
  end.
Lemma check_tree_sound :
  forall n suffix w node v,
    List.length suffix=n -> cap_read suffix node=Some v ->
    check_tree n w node=true -> cap_condition (rev suffix ++ w) v=true.
Proof.
  induction n as [|n IH]; intros [|b tail] w node v Len R C; cbn in Len; try discriminate.
  - cbn [cap_read] in R. cbn [check_tree] in C.
    destruct (cap_dead node); try discriminate. rewrite R in C. exact C.
  - injection Len as Len. cbn [cap_read] in R. cbn [check_tree] in C.
    destruct (cap_dead node); try discriminate.
    destruct (check_tree n (true::w) (child node true)) eqn:L; try discriminate.
    cbn [rev]. rewrite <- app_assoc. cbn [app]. destruct b.
    + exact (IH tail (true::w) _ v Len R L).
    + exact (IH tail (false::w) _ v Len R C).
Qed.

Theorem cap_condition_from_root :
  check_tree 50 [] cap_root=true -> forall w v,
  List.length w=50 -> cap_value w=Some v -> cap_condition w v=true.
Proof.
  intros H w v L V. unfold cap_value in V. rewrite <- rev_alt in V.
  pose proof (check_tree_sound 50 (rev w) [] cap_root v) as I.
  rewrite length_rev, rev_involutive, app_nil_r in I. exact (I L V H).
Qed.
