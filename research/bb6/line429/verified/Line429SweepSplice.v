(** One-sided languages at the E / normalized AR sweep entry cannot
    independently describe a safe invariant containing the blank orbit. *)
From BusyCoq Require Import Individual62 Line429Engine.
From Coq Require Import List.
Import ListNotations.
Open Scope sym_scope.
Module SweepSplice429.

Definition result n := multistep_c tm n c0.
Definition present n := match result n with Some _ => true | None => false end.
Definition after n := match result n with Some d => d | None => c0 end.

Lemma reach n : present n = true -> c0 -[tm]->> n / after n.
Proof.
  unfold present,after. destruct (result n) as [d|] eqn:H; [|discriminate].
  intros _. apply multistep_c_spec,H.
Qed.

Definition left_source := after 54.
Definition right_source := after 107.
Definition mix (c d : Q*tape) : Q*tape :=
  let '(_, (l,b,_)) := c in let '(_, (_,_,r)) := d in (E,(l,b,r)).
Definition hybrid := mix left_source right_source.

Lemma first_source : c0 -[tm]->> 54 / left_source.
Proof. apply reach. vm_compute. reflexivity. Qed.
Lemma second_source : c0 -[tm]->> 107 / right_source.
Proof. apply reach. vm_compute. reflexivity. Qed.
Lemma both_E : fst left_source = E /\ fst right_source = E.
Proof. vm_compute. auto. Qed.
Theorem hybrid_halts : halts_in tm hybrid 17.
Proof.
  remember (multistep_c tm 17 hybrid) as outcome eqn:result.
  destruct outcome as [c|].
  - exists c. split; [apply multistep_c_spec; symmetry; exact result|].
    assert (match multistep_c tm 17 hybrid with Some d => halted tm d | None => False end) as H by (vm_compute; reflexivity).
    rewrite <- result in H. exact H.
  - vm_compute in result. discriminate.
Qed.

Definition rectangular_at_E (I : Q*tape -> Prop) :=
  forall l b r l' b' r', I (E,(l,b,r)) -> I (E,(l',b',r')) -> I (E,(l,b,r')).

Theorem requires_correlation (I : Q*tape -> Prop) :
  (forall c, c0 -[tm]->* c -> I c) ->
  (forall c, I c -> ~halts tm c) ->
  ~rectangular_at_E I.
Proof.
  intros cover safe rect. pose proof both_E as [qa qb].
  assert (I left_source) as Hl by (apply cover; apply multistep_evstep_iff; exists 54%nat; exact first_source).
  assert (I right_source) as Hr by (apply cover; apply multistep_evstep_iff; exists 107%nat; exact second_source).
  assert (I hybrid) as H.
  { unfold hybrid,mix.
    destruct left_source as [q [[l b] r]], right_source as [q' [[l' b'] r']].
    cbn in qa,qb. subst q q'. eapply rect; eassumption. }
  apply (safe _ H). exists 17%nat. exact hybrid_halts.
Qed.

(* Two short checks of misleading regular-language guesses about F00.
   The tail of F00 can start with 01. It can also contain 001 farther out. *)
Definition reads (w:list Sym) (c:Q*tape) : Prop :=
  let '(q,(l,b,r)) := c in q = F /\ exists rest, b >> r = w *> rest.
Lemma hybrid_reset : exists d, hybrid -[tm]->> 13 / d /\ reads [0;0;0;0;1] d.
Proof.
  destruct (multistep_c tm 13 hybrid) as [d|] eqn:P.
  - exists d. split; [apply multistep_c_spec,P|].
    assert (match multistep_c tm 13 hybrid with
            | Some c => reads [0;0;0;0;1] c | None => False end) as H.
    { vm_compute. split; [reflexivity|]. eexists; reflexivity. }
    rewrite P in H. exact H.
  - vm_compute in P. discriminate.
Qed.
Definition first_F_01_example := after 123.
Definition internal_001_example := after 118.

Lemma example_123 : c0 -[tm]->> 123 / first_F_01_example /\ reads [0;0;0;1;1;0;1;1;0;1] first_F_01_example.
Proof. split; [apply reach; vm_compute; reflexivity|]. vm_compute. split; [reflexivity|]. eexists; reflexivity. Qed.
Lemma example_118 : c0 -[tm]->> 118 / internal_001_example /\ reads [0;0;1;1;0;0;1;1;0;1;1;0;1] internal_001_example.
Proof. split; [apply reach; vm_compute; reflexivity|]. vm_compute. split; [reflexivity|]. eexists; reflexivity. Qed.

(* An initially blank right exterior at a B frontier is by itself
   insufficient to guarantee a safe return. Both tapes are eventually zero;
   the left word is listed from the neighboring cell outward. *)
Definition false_frontier : Q*tape :=
  (B, ([1;0;0;0;1;0;0;1;1;0;1] *> 0inf, S0, 0inf)).
Theorem false_frontier_halts : halts_in tm false_frontier 90.
Proof.
  destruct (multistep_c tm 90 false_frontier) as [c|] eqn:P.
  - exists c. split; [apply multistep_c_spec,P|].
    assert (match multistep_c tm 90 false_frontier with
            | Some d => halted tm d | None => False end) as H by (vm_compute; reflexivity).
    rewrite P in H. exact H.
  - vm_compute in P. discriminate.
Qed.

End SweepSplice429.
Print Assumptions SweepSplice429.requires_correlation.
Print Assumptions SweepSplice429.example_123.
Print Assumptions SweepSplice429.example_118.
Print Assumptions SweepSplice429.false_frontier_halts.
Print Assumptions SweepSplice429.hybrid_reset.
