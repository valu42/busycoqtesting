(* Frontier rules for a public monotone-list holdout. These are not a
   blank-run classification. In particular, no00_counterexample disproves
   safety for arbitrary finite left words without adjacent zeros.
   AI-assisted research by Codex, using BusyCoq's execution tactics. *)
From BusyCoq Require Import Individual62 ES_v2 ES_v3.
From Coq Require Import List String Lia.
Import ListNotations.
Open Scope sym_scope.

Module MonotoneFrontier.
Definition tm := Eval compute in
  (TM_from_str "1RB0LE_0RC---_1RD0LA_1RE0RA_1LC0LF_0RC1LC").
Notation "c -->* c'" := (c -[tm]->* c') (at level 40).
Notation "c -->+ c'" := (c -[tm]->+ c') (at level 40).
Ltac first_step := eapply progress_intro; [prove_step | simpl_tape].

Lemma enter l :
  l {{B}}> 0inf -->+ l <{{C}} [1;0;0;1] *> 0inf.
Proof. first_step; es. Qed.

Lemma left_four l r :
  l <* [1;1;1;1] <{{C}} r -->+
  l <{{C}} [1;0;0;0] *> r.
Proof. first_step; es. Qed.

Lemma left_three l r :
  l <* [1;1;0] <{{C}} r -->+
  l <{{C}} [1;0;0] *> r.
Proof. first_step; es. Qed.

Lemma left_marker l r :
  l <* [1;1;1;0] <{{C}} r -->+
  l <{{C}} [1;0;0;1] *> r.
Proof. first_step; es. Qed.

Lemma right_four l r :
  l {{D}}> [1;0;0;0] *> r -->+
  l <* [1;0;1;0] {{D}}> r.
Proof. first_step; es. Qed.

Lemma right_end l :
  l {{D}}> [1;0;0;1] *> 0inf -->+
  l <* [1;1;0] {{B}}> 0inf.
Proof. first_step; es. Qed.

Lemma root_one l :
  l <* [1;0] {{B}}> 0inf -->+ l <* [1;1;1;1] {{B}}> 0inf.
Proof. first_step; es. Qed.

Lemma root_fours l n :
  l <* [0] <* [1;1;1;1]^^n {{B}}> 0inf -->+
  l <* [1] <* [1;0;1;0]^^n <* [1;1;0] {{B}}> 0inf.
Proof. first_step; es. Qed.

(* An interior run of four is created from a single run of five. This
   rejects the proposed grammar restricting every interior run to 1 or 2
   modulo four, even before considering an unbounded number of returns. *)
Lemma five_ones_return :
  0inf <* [1;1;1;1;1] {{B}}> 0inf -->+
  0inf <* [1;1;0;1;0;1;1;1;1;0;1] {{B}}> 0inf.
Proof. first_step; es. Qed.

Lemma blank_A :
  0inf {{A}}> 0inf -->+ 0inf <* [1] {{B}}> 0inf.
Proof. first_step; es. Qed.

Lemma blank_E :
  0inf {{E}}> 0inf -->+ 0inf <* [1;0;1] {{B}}> 0inf.
Proof. first_step; es. Qed.

Fixpoint no_adjacent_zeros (w : list sym) : bool :=
  match w with
  | S0 :: S0 :: _ => false
  | _ :: rest => no_adjacent_zeros rest
  | [] => true
  end.

Definition bad_word : list sym :=
  [1;1;1;1;1;1;0;1;0;1;1;0;1;0;1;1;0;1;1;1;1;1;1;0;1;1].
Lemma bad_word_no_adjacent_zeros : no_adjacent_zeros bad_word = true.
Proof. reflexivity. Qed.

Lemma no00_counterexample : halts tm (0inf <* bad_word {{B}}> 0inf).
Proof. unfold bad_word; esx. Qed.

Print Assumptions enter.
Print Assumptions left_four.
Print Assumptions left_three.
Print Assumptions left_marker.
Print Assumptions right_four.
Print Assumptions right_end.
Print Assumptions root_one.
Print Assumptions root_fours.
Print Assumptions five_ones_return.
Print Assumptions blank_A.
Print Assumptions blank_E.
Print Assumptions bad_word_no_adjacent_zeros.
Print Assumptions no00_counterexample.
End MonotoneFrontier.
