(* Rightward returns for the normalized form of BB(6) line 429.
   Bits in words are ordered from the head outward on both half-tapes. *)
From BusyCoq Require Import Individual62 Line429Engine.
From Coq Require Import List Arith Lia.
Import ListNotations Bell429.
Open Scope list_scope.
Open Scope sym_scope.

Definition AR (l r : side) := l {{A}}> r.

Tactic Notation "literal" int_or_var(n) :=
  unfold AR, CfgL; simpl_tape;
  do n (eapply multistep_S; [prove_step | simpl_tape]);
  apply multistep_0.

Lemma ar_one l r :
  AR l (1 >> r) -[src_tm]->> 1 / AR (1 >> l) r.
Proof. literal 1. Qed.

Lemma ar_zerozero l r :
  AR l ([0;0] *> r) -[src_tm]->> 3 / CfgL l (1 >> r).
Proof. literal 3. Qed.

Lemma ar_010 l r :
  AR l ([0;1;0] *> r) -[src_tm]->> 5 / AR ([1;0;1] *> l) r.
Proof. literal 5. Qed.

Lemma ar_011 l r :
  AR l ([0;1;1] *> r) -[src_tm]->> 8 / AR ([1;0] *> l) (0 >> r).
Proof. literal 8. Qed.

(* A block of three zeroes makes all tape farther to the right immaterial.
   The same output words and move count work for every external context. *)
Inductive Generated : list Sym -> Prop :=
| gNil : Generated []
| gOne p : Generated p -> Generated (p ++ [1])
| g010 p : Generated p -> Generated (p ++ [1;0;1])
| g011 p : Generated p -> Generated (p ++ [1;0]).

Definition SweepsTokens (w : list Sym) :=
  exists (p q : list Sym) (t : nat),
    Generated p /\ (3 <= t <= 4 * length w + 3)%nat /\
    forall l r : side,
      AR l (w *> [0;0;0] *> r) -[src_tm]->> t / CfgL (p *> l) (q *> r).

Lemma tokens_nil : SweepsTokens [].
Proof. unfold SweepsTokens. exists (@nil Sym), [1;0], 3%nat. split; [constructor |]. split; [cbn; lia | intros l r; exact (ar_zerozero l (0 >> r))]. Qed.

Lemma tokens_step (w u f : list Sym) (c : nat) :
  (forall p, Generated p -> Generated (p ++ f)) ->
  (c + 4 * length u <= 4 * length w)%nat ->
  (forall l r, AR l (w *> [0;0;0] *> r) -[src_tm]->> c /
               AR (f *> l) (u *> [0;0;0] *> r)) ->
  SweepsTokens u -> SweepsTokens w.
Proof.
  intros gen bound row [p [q [t [G [time path]]]]].
  exists (p ++ f), q, (c + t)%nat. split; [apply gen,G |]. split; [lia |].
  intros l r. rewrite Str_app_assoc.
  eapply multistep_trans; [apply row | apply path].
Qed.

Theorem right_triple_tokens : forall w, SweepsTokens w.
Proof.
  assert (sized : forall n w, length w = n -> SweepsTokens w).
  { intro n. induction n as [n IH] using lt_wf_ind. intros w N.
    destruct w as [|a w]; [apply tokens_nil |].
    destruct a.
    - destruct w as [|b w].
      + exists (@nil Sym), [1;0;0], 3%nat.
        split; [constructor |]. split; [cbn; lia | intros l r; exact (ar_zerozero l ([0;0] *> r))].
      + destruct b.
        * exists (@nil Sym), (1 :: (w ++ [0;0;0])), 3%nat.
          split; [constructor |]. split; [cbn; lia |].
          intros l r. cbn [Str_app]. rewrite Str_app_assoc.
          exact (ar_zerozero l (w *> [0;0;0] *> r)).
        * destruct w as [|c w].
          -- exists [1;0;1], [1], 8%nat. split; [exact (g010 [] gNil) |]. split; [cbn; lia |].
             intros l r. eapply (multistep_trans _ 5 3).
             ++ exact (ar_010 l ([0;0] *> r)).
             ++ exact (ar_zerozero ([1;0;1] *> l) r).
          -- destruct c.
             ++ eapply (tokens_step _ w [1;0;1] 5); [apply g010 | cbn; lia | |].
                ** intros l r. exact (ar_010 l (w *> [0;0;0] *> r)).
                ** apply (IH (length w)); [cbn in N; lia | reflexivity].
             ++ eapply (tokens_step _ (0 :: w) [1;0] 8); [apply g011 | cbn; lia | |].
                ** intros l r. exact (ar_011 l (w *> [0;0;0] *> r)).
                ** apply (IH (length (S0 :: w))); [cbn in N; subst n; cbn; auto with arith | reflexivity].
    - eapply (tokens_step _ w [1] 1); [apply gOne | cbn; lia | |].
      + intros l r. exact (ar_one l (w *> [0;0;0] *> r)).
      + apply (IH (length w)); [cbn in N; lia | reflexivity].
  }
  intro w. exact (sized (length w) w eq_refl).
Qed.

Definition SweepsRight (w : list Sym) :=
  exists (p q : list Sym) (t : nat),
    (3 <= t <= 4 * length w + 3)%nat /\
    forall l r : side,
      AR l (w *> [0;0;0] *> r) -[src_tm]->> t / CfgL (p *> l) (q *> r).

Corollary right_triple_barrier : forall w, SweepsRight w.
Proof.
  intros w. destruct (right_triple_tokens w) as [p [q [t [G H]]]].
  exists p,q,t. exact H.
Qed.

Corollary right_finite_tokens (w : list Sym) :
  exists (p q : list Sym) (t : nat),
    Generated p /\ (3 <= t <= 4 * length w + 3)%nat /\
    forall l, AR l (w *> 0inf) -[src_tm]->> t / CfgL (p *> l) (q *> 0inf).
Proof.
  destruct (right_triple_tokens w) as [p [q [t [G [time path]]]]].
  exists p, q, t. split; [exact G |]. split; [exact time |].
  intro l. specialize (path l 0inf).
  cbn [Str_app] in path. repeat rewrite <- (const_unfold _ S0) in path.
  exact path.
Qed.

Corollary right_finite (w : list Sym) :
  exists (p q : list Sym) (t : nat),
    (3 <= t <= 4 * length w + 3)%nat /\
    forall l, AR l (w *> 0inf) -[src_tm]->> t / CfgL (p *> l) (q *> 0inf).
Proof.
  destruct (right_triple_barrier w) as [p [q [t [time path]]]].
  exists p, q, t. split; [exact time |].
  intro l. specialize (path l 0inf).
  cbn [Str_app] in path. repeat rewrite <- (const_unfold _ S0) in path.
  exact path.
Qed.

Corollary right_total (w : list Sym) (l : side) :
  exists l' r', (l {{A}}> (w *> 0inf) -[src_tm]->* CfgL l' r').
Proof.
  destruct (right_finite w) as [p [q [t [_ path]]]].
  exists (p *> l), (q *> 0inf). apply without_counter with (n := t), path.
Qed.
