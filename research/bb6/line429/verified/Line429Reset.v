(** A necessary and sufficient halting pattern at the end of an original F sweep.
    Words start at the head and run to the right, in the original orientation. *)
From BusyCoq Require Import Individual62 Line429Sibling.
From Coq Require Import Lia.
Import Sibling429.
Open Scope sym_scope.
Module Reset429.

Fixpoint word (k:nat) (tail:side) : side :=
  match k with
  | O => 0 >> 0 >> 1 >> tail
  | S j => 1 >> 0 >> word j tail
  end.

Definition danger (s:side) := exists k t, s = word k t.
Lemma pair_danger s : danger s -> danger (1 >> 0 >> s).
Proof. intros [k [t ->]]. exists (S k),t; reflexivity. Qed.
Lemma base_danger s : danger (0 >> 0 >> 1 >> s).
Proof. exists O,s; reflexivity. Qed.
Lemma no_11 s : ~ danger (1 >> 1 >> s).
Proof. intros [[] [t H]]; discriminate. Qed.
Lemma no_blank : ~ danger 0inf.
Proof.
  intros [[] [t H]].
  - apply (f_equal (fun s => Streams.hd (Streams.tl (Streams.tl s)))) in H. discriminate.
  - apply (f_equal (@Streams.hd Sym)) in H. discriminate.
Qed.

Definition reset (c:Q*tape) :=
  match c with
  | (F,(_,S0,S0 >> r)) => danger r
  | _ => False
  end.
Definition hit := exists c, c0 -[machine429]->* c /\ reset c.

(** Propagate a past reachable reset back through the unique incoming
    instructions of B, C and D. E and F retain one freshly written neighbor. *)
Definition history (c:Q*tape) : Prop :=
  let '(q,(l,b,r)) := c in match q with
  | A => b = S0 -> danger r -> hit
  | B => danger (b >> r) -> hit
  | C => b = S0 -> Streams.hd r = S1 -> hit
  | D => (b = S1 -> hit) /\ Streams.hd l = S1
  | E => b = S0 -> Streams.hd r = S1
  | F => Streams.hd l = S0
  end.

Lemma preserve c c' : c0 -[machine429]->* c -> history c ->
  c -[machine429]-> c' -> history c'.
Proof.
  intros R H T. apply step_c_spec in T.
  destruct c as [q [[[a l] b] [v r]]].
  destruct q,b; cbn in T; try discriminate; inversion T; subst c'; clear T;
    cbn [history move_left move_right Streams.hd Streams.tl] in *.
  - apply H; reflexivity.
  - discriminate.
  - intros -> K. destruct r as [d r]. cbn in K. subst d. apply H, base_danger.
  - intros -> K. apply H, pair_danger, K.
  - split; [intro K; now apply H|reflexivity].
  - reflexivity.
  - destruct H as [_ ->]. discriminate.
  - intros Ha K. exfalso. specialize (H eq_refl). subst v. exact (no_11 r K).
  - reflexivity.
  - intros -> K. exists (F, (a >> l, S0, S0 >> r)). split; assumption.
  - reflexivity.
Qed.

Lemma history_reached c : c0 -[machine429]->* c -> history c.
Proof.
  intro R. apply evstep_multistep in R as [n R].
  remember c0 as cstart. assert (P : c0 -[machine429]->* cstart /\ history cstart).
  { subst cstart. split; [constructor|]. intros _ K. exfalso; exact (no_blank K). }
  clear Heqcstart. induction R as [x|n x y z S T IH]; [apply P|].
  apply IH. destruct P as [R H]. split.
  - eapply evstep_trans; [exact R|now apply evstep_one].
  - eapply preserve; eassumption.
Qed.

Theorem halt_requires_reset : halts machine429 c0 -> hit.
Proof.
  intros [n [c [R stop]]]. assert (E : c0 -[machine429]->* c).
  { apply multistep_evstep_iff. eauto. }
  pose proof (history_reached c E) as H. destruct c as [q [[l b] r]].
  destruct q,b; cbn in stop; try discriminate. apply H; reflexivity.
Qed.

Lemma b_count k : forall l t,
    halts_in machine429 (l {{B}}> word k t) (2*k+2)%nat.
Proof.
  induction k as [|k IH]; intros l t.
  - eexists. split; [apply multistep_c_spec; reflexivity|reflexivity].
  - replace (2 * S k + 2)%nat with (S (S (2*k+2))) by lia.
    cbn [word]. do 2 (eapply halts_in_S; [|apply step_c_spec; reflexivity]). apply IH.
Qed.

Theorem reset_count k l t :
  halts_in machine429 (l {{F}}> (0 >> 0 >> word k t)) (2*k+4)%nat.
Proof.
  replace (2*k+4)%nat with (S (S (2*k+2))) by lia.
  do 2 (eapply halts_in_S; [|apply step_c_spec; reflexivity]). apply b_count.
Qed.

Theorem blank_reset : halts machine429 c0 <->
  exists k l t, c0 -[machine429]->* l {{F}}> (0 >> 0 >> word k t).
Proof.
  split.
  - intro stop. destruct (halt_requires_reset stop) as [[q [[l b] [v r]]] [R H]].
    destruct q,b,v; cbn in H; try contradiction. destruct H as [k [t ->]]. eauto.
  - intros [k [l [t R]]]. eapply halts_evstep; [exists (2*k+4)%nat; apply reset_count|exact R].
Qed.

(** The following B launch has outward left prefix 100 on the actual orbit. *)
Theorem blank_launch : halts machine429 c0 <->
  exists k l t, c0 -[machine429]->* (1 >> 0 >> 0 >> l) {{B}}> word k t.
Proof.
  split.
  - intro stop. apply blank_reset in stop as [k [l [t R]]].
    pose proof (history_reached _ R) as H. destruct l as [a l]. change (a=S0) in H; subst a.
    exists k,l,t. eapply evstep_trans; [exact R|].
    do 2 (eapply evstep_step; [apply step_c_spec; reflexivity|]). constructor.
  - intros [k [l [t R]]]. eapply halts_evstep; [exists (2*k+2)%nat; apply b_count|exact R].
Qed.
End Reset429.
Print Assumptions Reset429.blank_reset.
Print Assumptions Reset429.blank_launch.
Print Assumptions Reset429.reset_count.
