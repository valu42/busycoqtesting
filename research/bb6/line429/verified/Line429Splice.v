(** A configuration that splices two genuine blank-orbit half-tapes. *)
From BusyCoq Require Import Individual62 Line429Engine.
From Coq Require Import List.
Import ListNotations.
Open Scope sym_scope.
Module Splice429.
Definition after (n:nat) (c:Q*tape) : Q*tape :=
  match multistep_c tm n c with Some d => d | None => c0 end.
Definition defined (n:nat) (c:Q*tape) : bool :=
  match multistep_c tm n c with Some _ => true | None => false end.
Lemma after_spec n c : defined n c = true -> c -[tm]->> n / after n c.
Proof.
  unfold after,defined. destruct (multistep_c tm n c) as [d|] eqn:H;
    [intros _; apply multistep_c_spec,H|discriminate].
Qed.
Fixpoint first_bits (n:nat) (s:side) :=
  match n with O => [] | S k => Streams.hd s :: first_bits k (Streams.tl s) end.
Definition neighborhood (c:Q*tape) :=
  let '(q,(l,b,r)):=c in (q,rev (first_bits 3 l) ++ (b :: first_bits 2 r)).
Definition cross (c d:Q*tape) :=
  let '(_, (l,_,_)):=c in let '(q,(_,b,r)):=d in (q,(l,b,r)).
Definition left_source := after 217 c0.
Definition right_source := after 4436 c0.
Definition hybrid := cross left_source right_source.
Theorem source_left : c0 -[tm]->> 217 / left_source.
Proof. apply after_spec. vm_compute. reflexivity. Qed.
Theorem source_right : c0 -[tm]->> 4436 / right_source.
Proof. apply after_spec. vm_compute. reflexivity. Qed.
Theorem common_neighborhood : neighborhood left_source = neighborhood right_source.
Proof. vm_compute. reflexivity. Qed.
Theorem hybrid_halts : halts_in tm hybrid 92.
Proof.
  exists (after 92 hybrid). split.
  - apply after_spec. vm_compute. reflexivity.
  - vm_compute. reflexivity.
Qed.
Theorem actual_neighborhood :
  neighborhood left_source = (C, [0; 1; 0; 0; 0; 1]).
Proof. vm_compute. reflexivity. Qed.
(** This formulation includes an arbitrary relation between each complete
    half-tape and the six-symbol neighborhood. *)
Theorem no_inductive_splice_closed_invariant (I : Q*tape -> Prop) :
  I c0 ->
  (forall n c d, I c -> c -[tm]->> n / d -> I d) ->
  (forall c d, I c -> I d -> neighborhood c = neighborhood d -> I (cross c d)) ->
  (forall c, I c -> ~halted tm c) -> False.
Proof.
  intros H0 Closed Mix Safe.
  pose proof (Closed _ _ _ H0 source_left) as Lc.
  pose proof (Closed _ _ _ H0 source_right) as Rc.
  pose proof (Mix _ _ Lc Rc common_neighborhood) as Joined.
  destruct hybrid_halts as [d [Run Halt]].
  exact (Safe d (Closed _ _ _ Joined Run) Halt).
Qed.
End Splice429.
Print Assumptions Splice429.hybrid_halts.

Print Assumptions Splice429.no_inductive_splice_closed_invariant.
