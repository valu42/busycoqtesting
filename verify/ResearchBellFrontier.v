(* Research checkpoint: local progress rules, NOT a blank-run classification.

   The exact table below is publicly listed as a starting-state variant of
   the lottery-like Bell family:
   https://wiki.bbchallenge.org/wiki/1RB1RD_1LC0LE_1RA0LB_1RA1RF_0RA0RC_1RE---

   Racheline and -d analyzed this family before this work. A related starting
   state has a conditional halting proof in int-y1/proofs, commit
   1929f57df4dd7afcc11c3f458e20526fd1f991e0. These short Rocq lemmas record
   independently checked local transformations only; they do not settle the
   family's outstanding reachability problem.

   Generated with Codex using BusyCoq's existing execution/shift tactics.
   All six statements were checked by coqc and independently by coqchk.
*)
From BusyCoq Require Import Individual62 ES_v2 ES_v3.
From Coq Require Import Lia String.
Open Scope sym_scope.
Definition tm := Eval compute in (TM_from_str "1RB1RD_1LC0LE_1RA0LB_1RA1RF_0RA0RC_1RE---").
Notation "c -->+ c'" := (c -[tm]->+ c') (at level 40).
Notation "c -->* c'" := (c -[tm]->* c') (at level 40).

Lemma prefix11 l :
 l <* [1;1] {{A}}> 0inf -->+ l <* [1;0;1;0] {{A}}> 0inf.
Proof. execute. Qed.

Lemma prefix0111 l :
 l <* [0;1;1;1] {{A}}> 0inf -->+ l <* [1;0;1;0;1;0] {{A}}> 0inf.
Proof. execute. Qed.

Lemma pairs_triple l b :
 l <* [1;1;1] <* [1;0]^^(b+1) {{A}}> 0inf -->+
 l <* [1;0]^^(b+5) {{A}}> 0inf.
Proof. es. Qed.

Lemma zero_pairs_zero l b :
 l <* [0] <* [1;0]^^b <* [0] {{A}}> 0inf -->+
 l <* [1]^^(b*2+5) {{A}}> 0inf.
Proof. es. Qed.

Lemma pairs_zero l b :
 l <* [0] <* [1;0]^^(b+1) {{A}}> 0inf -->+
 l <* [1]^^(b*2+6) <* [0] {{A}}> 0inf.
Proof. es. Qed.

Lemma pairs_double_zero l b :
 l <* [1;1;0;0] <* [1;0]^^(b+2) {{A}}> 0inf -->+
 l <* [1]^^6 <* [0] <* [1]^^(b*2+4) <* [0] {{A}}> 0inf.
Proof. es. Qed.

Print Assumptions prefix11.
Print Assumptions prefix0111.
Print Assumptions pairs_triple.
Print Assumptions zero_pairs_zero.
Print Assumptions pairs_zero.
Print Assumptions pairs_double_zero.
