(** Nonhalting of BB(2,5) holdout 36, from the blank initial configuration. *)
From Coq Require Import List Arith Lia Strings.String.
From BusyCoq Require Import Individual25.
From BusyCoq Require Export Line36Nonhalt.
From BusyCoq Require Import Line36LowBranch Line36HighBranch Line36LeftCertificate.

Theorem nonhalt : ~ halts (TM_from_str "1RB2LA1LA4RA2LA_0LA3RB3LB2RB---"%string) c0.
Proof.
  change (~ halts line36 c0).
  apply line36_nonhalt_from_successor. intros f h F Cap Credit.
  destruct (Nat.lt_ge_cases (fst (mark36 (skipn 3 (ftail f)) 0)) 29) as [Low|High].
  - exact (low_branch36 L36LeftCertificate.finite_step f h F Cap Credit Low).
  - exact (high_branch36 f h F Cap Credit High).
Qed.

Print Assumptions nonhalt.
