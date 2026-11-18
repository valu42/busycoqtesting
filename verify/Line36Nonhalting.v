(** Nonhalting of BB(2,5) holdout 36, from the blank initial configuration. *)
From Coq Require Import List Arith Lia.
From BusyCoq Require Export Line36Nonhalt.
From BusyCoq Require Import Line36LowBranch Line36HighBranch Line36LeftCertificate.

Theorem line36_nonhalting : ~ halts line36 c0.
Proof.
  apply line36_nonhalt_from_successor. intros f h F Cap Credit.
  destruct (Nat.lt_ge_cases (fst (mark36 (skipn 3 (ftail f)) 0)) 29) as [Low|High].
  - exact (low_branch36 L36LeftCertificate.finite_step f h F Cap Credit Low).
  - exact (high_branch36 f h F Cap Credit High).
Qed.

Print Assumptions line36_nonhalting.
