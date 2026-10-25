(* Research checkpoint: counter shortcuts, NOT a blank-run classification.

   P0_n adapts the existing rule and induction from CounterClass3v1.v.
   The other lemmas batch complete forward and backward phases.
   All rules allow an arbitrary D0 transition: these phases do not use it.

   Lists on the left of a head are written nearest cell first. Thus frontier
   turns 2*n+1 zeros on the left and n ones on the right of F0 into a zero
   followed by n physical 110 blocks on the left, preserving arbitrary tails.
   back_sweep consumes n left-hand blocks and transfers their count to the
   right-hand counters. Neither lemma proves that the blank run stays in
   these forms or that it halts. frontier_positive adds strict progress for
   a nonempty forward phase.

   AI-assisted work by Codex using BusyCoq's execution/shift tactics.
*)
From BusyCoq Require Import Individual62 ES_v2 ES_v3.
From Coq Require Import Lia String.
Open Scope sym_scope.
Ltac counter_unfold_config :=
match goal with
| |- ?a -[_]->* ?b -> _ =>
  unfold_config_expr a;
  unfold_config_expr b
end.

Ltac counter_follow x :=
  pose proof x as Hx;
  gen Hx;
  counter_unfold_config;
  simpl_rotate;
  intro Hx;
  try (
  follow Hx;
  clear Hx).

Definition counter_tm (d0 : option (sym * dir * Q)) : TM := fun qs =>
 match qs with
 | (A,S0) => Some (S1,L,B) | (A,S1) => Some (S1,L,A)
 | (B,S0) => Some (S1,L,C) | (B,S1) => Some (S1,R,B)
 | (C,S0) => Some (S0,R,D) | (C,S1) => Some (S0,L,A)
 | (D,S0) => d0 | (D,S1) => Some (S1,R,E)
 | (E,S0) => None          | (E,S1) => Some (S1,R,F)
 | (F,S0) => Some (S1,R,C) | (F,S1) => Some (S0,R,F)
 end.
Section Rules.
Variable d0 : option (sym * dir * Q).
Notation tm := (counter_tm d0).
Notation "c -->* c'" := (c -[tm]->* c') (at level 40).
Notation "l <| r" := (l <{{B}} [1;1] *> r) (at level 30).
Lemma P0_n n:
  forall l r,
  l <* [0;0]^^n <| [0] *> [1]^^n *> r -->*
  l <| [1;1]^^n *> [0] *> [1]^^n *> r.
Proof.
  induction n; intros.
  1: es.
  counter_follow (IHn ([0;0]*>l) ([1]*>r)).
  es; er.
  follow IHn.
  es.
Qed.
Lemma frontier n : forall l r,
 l <* [0]^^(n*2+1) {{F}}> [0] *> [1]^^n *> [0] *> r -->*
 l <* [0] <* [0;1;1]^^n {{F}}> [0;0] *> r.
Proof.
 induction n; intros.
 - es.
 - do 4 step.
   rewrite lpow_mul.
   counter_follow (P0_n n (l <* [0;0]) ([0] *> r)).
   eapply evstep_trans with (c' := (l <* [1;1;0] <* [0]^^(n*2+1) {{F}}> [0] *> [1]^^n *> [0] *> r)).
   + es.
   + counter_follow (IHn (l <* [1;1;0]) r).
     es.
Qed.
Lemma back_sweep n : forall l r m,
 l <* [1;1;0]^^n {{A}}> [0] *> [1]^^m *> [0] *> r -->*
 l {{A}}> [0] *> [1]^^(m+n*2) *> [0] *> [1]^^n *> r.
Proof.
 induction n; intros.
 - es.
 - eapply evstep_trans with (c' := (l <* [1;1;0]^^n {{A}}> [0] *> [1]^^(m+2) *> [0;1] *> r)).
   + es.
   + counter_follow (IHn l ([1] *> r) (m+2)).
     replace (m+2+n*2) with (m+S (S (n*2))) by lia.
     apply evstep_refl.
Qed.
Lemma frontier_positive n l r :
 l <* [0]^^(S n*2+1) {{F}}> [0] *> [1]^^(S n) *> [0] *> r -[tm]->+
 l <* [0] <* [0;1;1]^^(S n) {{F}}> [0;0] *> r.
Proof.
 eapply evstep_progress.
 - apply frontier.
 - cbn [lpow]. discriminate.
Qed.
End Rules.
Print Assumptions P0_n.
Print Assumptions frontier.

Print Assumptions back_sweep.
Print Assumptions frontier_positive.
