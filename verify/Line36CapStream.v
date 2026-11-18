(** A streaming implementation of the finite cap check. The proof at the end
    identifies its Boolean result with the specification that calls [mark36],
    [cap_loss] and tests the actual derivative words. *)
From Coq Require Import List Bool Arith Uint63 PArray Lia.
From BusyCoq Require Import Line36Matching Line36Right Line36CapModel Line36Cap.
Import ListNotations.

Definition hop (r : int) (b : bool) := if cap_dead r then r else child r b.
Definition finish (r : int) :=
  if cap_dead r then None else PArray.get leaf_values r.

Lemma fold_dead l r : cap_dead r = true -> fold_left hop l r = r.
Proof. induction l as [|b l IH]; intros D; [reflexivity|].
  change (fold_left hop l (hop r b) = r). unfold hop at 2. rewrite D. apply IH, D. Qed.

Lemma read_fold l r : cap_read l r = finish (fold_left hop l r).
Proof.
  revert r. induction l as [|b l IH]; intros r.
  - reflexivity.
  - cbn [cap_read fold_left]. unfold hop at 2.
    destruct (cap_dead r) eqn:D.
    + rewrite fold_dead by auto. unfold finish. rewrite D. reflexivity.
    + apply IH.
Qed.
Lemma value_fold l : cap_value l = finish (fold_left hop (rev l) cap_root).
Proof. unfold cap_value. rewrite <- rev_alt. apply read_fold. Qed.

Definition middle (bits : list bool) :=
  match bits with [] => [] | s::rest => cap_deriv s rest end.
Definition core_node bits (append : bool) :=
  fold_left hop (rev (middle bits ++ (if append then [false] else []))) cap_root.
Lemma core_prepend a b rest endbit :
  core_node (a::b::rest) endbit = hop (core_node (b::rest) endbit) (Bool.eqb a b).
Proof.
  unfold core_node, middle. cbn [cap_deriv]. cbn [app rev].
  rewrite fold_left_app. reflexivity.
Qed.
Lemma next_follows bits (endbit prev:bool) :
  bits <> [] ->
  cap_value (if endbit then tl (cap_deriv prev bits) ++ [false] else cap_deriv prev bits)
   = finish (if endbit then core_node bits endbit
             else hop (core_node bits endbit) (Bool.eqb prev (hd false bits))).
Proof.
  intros NE. destruct bits as [|b bits]; [contradiction|].
  rewrite value_fold. destruct endbit.
  - reflexivity.
  - unfold core_node, middle. rewrite app_nil_r. cbn [cap_deriv rev].
    rewrite fold_left_app. reflexivity.
Qed.

(** On a nonempty suffix, [m0,m1] are the costs of the word and its tail.
    [run0,run1] record both incoming run parities, so prepending a surviving
    opener merely exchanges them. [cursor] has consumed all determined
    rightmost bits of the output, leaving its boundary bit if needed. *)
Record summary := {
  debt : nat; left_mark : bool; has_mark : bool; has_closing : bool;
  m0 : nat; m1 : nat; run0 : nat; run1 : nat; loss : nat;
  cursor : int; append : bool
}.

Definition reference (w : list bool) : summary :=
  let '(d,bits) := mark36 w 0 in
  {| debt:=d; left_mark:=hd false bits; has_mark:=existsb id bits;
     has_closing:=existsb negb w; m0:=monomers w; m1:=monomers (tl w);
     run0:=run_cost bits false; run1:=run_cost bits true;
     loss:=cap_loss (cap_after_anchor w); cursor:=core_node bits (last w false);
     append:=last w false |}.

(** Prepending a closing moves the anchor, making the entire former suffix
    the input to [cap_loss]. Prepending an opening keeps the anchor. *)
Definition prepend (b : bool) (s : summary) : summary :=
  let m := b && Nat.eqb (debt s) 0 in
  {| debt:=if b then Nat.pred (debt s) else S (debt s);
     left_mark:=m; has_mark:=m || has_mark s; has_closing:=negb b || has_closing s;
     m0:=if b then m1 s else S (m0 s); m1:=m0 s;
     run0:=if m then run1 s else run0 s;
     run1:=if m then run0 s else S (run0 s);
     loss:=if b then loss s else m0 s - (debt s + run0 s);
     cursor:=hop (cursor s) (Bool.eqb m (left_mark s)); append:=append s |}.

Lemma prepend_reference b w :
  w <> [] -> prepend b (reference w) = reference (b :: w).
Proof.
  destruct w as [|e w]; [contradiction|]. intros _.
  pose proof (mark36_length (e::w) 0) as Len.
  assert (Cons : forall q word,
    mark36 (q::word) 0 = let '(k,bs) := mark36 word 0 in
        if q then match k with O => (0,true::bs) | S t => (t,false::bs) end
             else (S k,false::bs)) by reflexivity.
  unfold reference. rewrite (Cons b (e::w)).
  destruct (mark36 (e::w) 0) as [d [|bit bs]] eqn:M; [discriminate Len|].
  cbn [snd] in Len. unfold prepend.
  assert (Last : last (b :: e :: w) false = last (e::w) false) by reflexivity.
  rewrite Last.
  destruct b, d; cbn [debt left_mark has_mark has_closing m0 m1 run0 run1 loss cursor append
    Nat.eqb Nat.pred andb orb negb existsb hd monomers tl run_cost cap_after_anchor];
  rewrite ?core_prepend; try reflexivity.
  all: try (unfold cap_loss; rewrite M; reflexivity).
Qed.

Definition stream_edge (v c : nat) (r : int) :=
  match finish r with
  | None => false
  | Some next => Nat.leb (S next) (v + 3*c)
  end.
Definition follow (s : summary) (previous : bool) :=
  if append s then cursor s
  else hop (cursor s) (Bool.eqb (previous && Nat.eqb (debt s) 0) (left_mark s)).
Definition stream_leaf (s : summary) (v : nat) :=
  Nat.leb v 21 && has_mark s && has_closing s &&
  stream_edge v (loss s) (follow s false) &&
  (if Nat.eqb (debt s) 0 && negb (append s)
   then stream_edge v (loss s) (follow s true) else true).
Lemma stream_leaf_exact w v :
  w <> [] -> cap_condition w v = stream_leaf (reference w) v.
Proof.
  intros NE. pose proof (mark36_length w 0) as Len.
  unfold cap_condition, reference. destruct (mark36 w 0) as [d bits] eqn:E.
  assert (NEB : bits <> []).
  { intros ->. cbn in Len. apply NE. apply length_zero_iff_nil. symmetry. exact Len. }
  unfold stream_leaf, follow, stream_edge, bounded_successor.
  cbn [append debt left_mark cursor loss has_mark has_closing].
  repeat rewrite next_follows by exact NEB. reflexivity.
Qed.

Fixpoint fast_tree (fuel : nat) (node : int) (state : summary) :=
  if cap_dead node then true else
  match fuel with
  | O => match PArray.get leaf_values node with
         | Some v => stream_leaf state v | None => true end
  | S n => if fast_tree n (child node true) (prepend true state)
           then fast_tree n (child node false) (prepend false state) else false
  end.
Lemma fast_tree_exact n w node : w <> [] ->
  check_tree n w node = fast_tree n node (reference w).
Proof.
  revert w node. induction n as [|n IH]; intros w node NE.
  - cbn [check_tree fast_tree]. destruct (cap_dead node); [reflexivity|].
    destruct (PArray.get leaf_values node); [apply stream_leaf_exact, NE|reflexivity].
  - cbn [check_tree fast_tree]. destruct (cap_dead node); [reflexivity|].
    rewrite (IH (true::w)) by discriminate. rewrite (IH (false::w)) by discriminate.
    repeat rewrite prepend_reference by auto. reflexivity.
Qed.

Definition fast_whole n r :=
  if cap_dead r then true else
  if fast_tree n (child r true) (reference [true])
  then fast_tree n (child r false) (reference [false]) else false.
Definition cap_fast_certificate := fast_whole 49 cap_root.
Local Opaque child cap_root cap_dead reference cap_table.
Lemma fast_whole_exact n r : check_tree (S n) [] r = fast_whole n r.
Proof.
  cbn [check_tree]. unfold fast_whole.
  rewrite (fast_tree_exact n [true] (child r true)) by discriminate.
  rewrite (fast_tree_exact n [false] (child r false)) by discriminate.
  reflexivity.
Qed.
Definition fast_root_exact : check_tree 50 [] cap_root = cap_fast_certificate :=
  fast_whole_exact 49 cap_root.
