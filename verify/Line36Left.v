From Coq Require Import List Bool ZArith Lia.
Import ListNotations.
Open Scope Z_scope.

Module L36Left.
Record state := State {
  phase : nat;
  kind : nat;
  last_choice : bool;
  partial_choice : bool;
  partial_len : nat;
  halo : nat
}.
Record edge := Edge {
  target : state;
  dx : Z;
  charge : Z
}.
Definition weight (e : edge) : Z := 6 * dx e - 24 * charge e - 4.
Definition edge_ok (V : state -> Z) (s : state) (e : edge) : bool :=
  Z.leb (V (target e) - V s) (weight e).

Lemma edge_ok_sound V s e :
  edge_ok V s e = true -> V (target e) - V s <= weight e.
Proof. exact (proj1 (Z.leb_le _ _)). Qed.

Inductive walk (E : state -> edge -> Prop) : state -> state -> Z -> Prop :=
| walk_nil s : walk E s s 0
| walk_cons s e t sum : E s e -> walk E (target e) t sum ->
    walk E s t (weight e + sum).

Theorem path_bound E (V : state -> Z)
    (edges : forall s e, E s e -> edge_ok V s e = true)
    s t total (p : walk E s t total) :
  V t - V s <= total.
Proof.
  induction p as [s | s e t sum Hstep Htail IH]; [lia|].
  apply edges, edge_ok_sound in Hstep. lia.
Qed.

Definition clipped (V : state -> Z) (s : state) : Z :=
  Z.max (-110) (Z.min 0 (V s)).

Lemma clipped_range V s : -110 <= clipped V s <= 0.
Proof. unfold clipped. lia. Qed.

Lemma deep_edge V s e d :
  29 <= d -> 12*d - 238 <= weight e -> edge_ok (clipped V) s e = true.
Proof.
  intros. apply Z.leb_le.
  pose proof (clipped_range V s). pose proof (clipped_range V (target e)). lia.
Qed.

Section Enumeration.
Variable step : state -> nat -> nat -> option edge.
Variable V : state -> Z.

Definition check_case s history debt : bool :=
  match step s history debt with Some e => edge_ok V s e | None => false end.

Definition check_range {A : Type} (test : A -> bool) (domain : list A) :=
  forallb test domain.

Lemma check_range_member {A : Type} (test : A -> bool) domain x :
  check_range test domain = true -> In x domain -> test x = true.
Proof. intros H I. unfold check_range in H. now apply forallb_forall with (x := x) in H. Qed.

Definition check_state s :=
  forallb (fun h => forallb (check_case s h) (seq 0 29)) (seq 0 16).

Theorem checked_step s history d :
  check_state s = true -> (history < 16)%nat -> (d < 29)%nat ->
  exists e, step s history d = Some e /\ V (target e) - V s <= weight e.
Proof.
  intros H Hh Hd.
  unfold check_state in H.
  apply forallb_forall with (x := history) in H.
  2: apply in_seq; lia.
  apply forallb_forall with (x := d) in H.
  2: apply in_seq; lia.
  unfold check_case in H.
  destruct (step s history d) as [e|] eqn:E; [|discriminate].
  exists e; split; [reflexivity|apply edge_ok_sound; exact H].
Qed.
End Enumeration.
End L36Left.
