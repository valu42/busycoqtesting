(* Research checkpoint: counter return rules, NOT a blank-run classification.

   These rules complement ResearchCounterBatch.v. They describe the A/0 and
   F/0 phases on finite runs of ones and zeros, preserving arbitrary tails.
   The six rules in General work for every D0 transition. The two D0-specific
   rules cover the F and B variants. Three initialization bridges and two
   counterexamples concern the F variant.

   F_zero_one_halts proves halting from its stated local pattern; no theorem
   here says that a blank run reaches that pattern. Likewise, the progress
   rules do not yet supply a closed invariant or a complete recurrence for
   either blank start. Exponents and left-side lists use BusyCoq notation;
   lists on the left are written nearest cell first.

   AI-assisted work by Codex using BusyCoq's existing execution/shift tactics.
   The counter table and the underlying P0 induction are from the repository's
   CounterClass3v1.v; the generalized table is in ResearchCounterBatch.v.
*)
From BusyCoq Require Import Individual62 ResearchCounterBatch ES_v2 ES_v3.
From Coq Require Import Lia String.
Open Scope sym_scope.
Section General.
Variable d0 : option (sym * dir * Q).
Notation tm := (counter_tm d0).
Notation "c -->+ c'" := (c -[tm]->+ c') (at level 40).
Ltac first_step := eapply progress_intro; [prove_step | simpl_tape].

Lemma A_ones l r k m:
 l <* [0] <* [1]^^(k+1) {{A}}> [0] *> [1]^^m *> [0] *> r -->+
 l {{A}}> [0] *> [1]^^(k+1+m) *> [0;1] *> r.
Proof. first_step; es. Qed.

Lemma A_two_zeros l r m:
 l <* [0;0] {{A}}> [0] *> [1]^^m *> [0] *> r -->+
 l <* [1;1;0] <* [0]^^m {{F}}> [0] *> r.
Proof. first_step; es. Qed.

Lemma A_one_zero l r k m:
 l <* [0] <* [1]^^(k+1) <* [0] {{A}}> [0] *> [1]^^m *> [0] *> r -->+
 l {{A}}> [0] *> [1]^^k *> [0] *> [1]^^(m+2) *> [0] *> r.
Proof. first_step; es. Qed.

Lemma F_ones l r k n:
 l <* [0] <* [1]^^k {{F}}> [0] *> [1]^^(n+1) *> [0] *> r -->+
 l {{A}}> [0] *> [1]^^(k+1) *> [0] *> [1]^^n *> [0] *> r.
Proof. first_step; es. Qed.

Lemma F_zero_two_ones l r n:
 l {{F}}> [0;0] *> [1]^^(n+2) *> [0] *> r -->+
 l <* [1;1;0;1] <* [0]^^n {{F}}> [0] *> r.
Proof. first_step; es. Qed.

Lemma F_zero_one_halts l r:
 halts tm (l {{F}}> [0;0;1;0] *> r).
Proof. esx. Qed.
End General.

Lemma F_two_zeros_F l r:
 l {{F}}> [0;0;0] *> r -[counter_tm (Some (S1,L,F))]->+
 l <* [1] {{F}}> [0;1] *> r.
Proof. eapply progress_intro; [prove_step | simpl_tape]; es. Qed.

Lemma F_two_zeros_B l r k:
 l <* [0] <* [1]^^k {{F}}> [0;0;0] *> r -[counter_tm (Some (S1,L,B))]->+
 l {{A}}> [0] *> [1]^^k *> [0;1;1] *> r.
Proof. eapply progress_intro; [prove_step | simpl_tape]; es. Qed.

Lemma blank_A_to_four:
 c0 -[counter_tm (Some (S1,L,F))]->+
 0inf {{A}}> [0;1;1;1;1] *> 0inf.
Proof. eapply progress_intro; [prove_step | simpl_tape]; es. Qed.

Lemma blank_F_to_two:
 0inf {{F}}> 0inf -[counter_tm (Some (S1,L,F))]->+
 0inf {{A}}> [0;1;1] *> 0inf.
Proof. eapply progress_intro; [prove_step | simpl_tape]; es. Qed.

Lemma blank_F_to_twelve_five:
 0inf {{F}}> 0inf -[counter_tm (Some (S1,L,F))]->+
 0inf {{A}}> [0] *> [1]^^12 *> [0] *> [1]^^5 *> 0inf.
Proof. eapply progress_intro; [prove_step | simpl_tape]; es. Qed.

(* Two checked counterexamples keep tempting false global invariants out of
   future proofs. Positive block sizes alone do not imply nonhalting; a
   decreasing list of block sizes is not preserved at every A/0 return. *)
Lemma two_two_halts r:
 halts (counter_tm (Some (S1,L,F)))
  (0inf {{A}}> [0;1;1;0;1;1;0] *> r).
Proof. esx. Qed.

Lemma nineteen_return:
 0inf {{A}}> [0] *> [1]^^19 *> 0inf
 -[counter_tm (Some (S1,L,F))]->+
 0inf {{A}}> [0] *> [1]^^7 *> [0] *> [1]^^15 *> [0] *> [1]^^5 *> 0inf.
Proof. eapply progress_intro; [prove_step | simpl_tape]; es. Qed.

Print Assumptions two_two_halts.
Print Assumptions nineteen_return.
Print Assumptions blank_F_to_twelve_five.
Print Assumptions A_ones.
Print Assumptions A_two_zeros.
Print Assumptions A_one_zero.
Print Assumptions F_ones.
Print Assumptions F_zero_two_ones.
Print Assumptions F_zero_one_halts.
Print Assumptions F_two_zeros_F.
Print Assumptions F_two_zeros_B.
Print Assumptions blank_A_to_four.
Print Assumptions blank_F_to_two.
