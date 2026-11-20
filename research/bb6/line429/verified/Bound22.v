(** A lower bound in elementary transitions for line 429 from its blank tape. *)
From BusyCoq Require Import Individual62 Line429Engine Line429Score.
From Coq Require Import NArith.
Import Bell429 Score429.
Definition witness_threshold : N := (10^581)%N.
Lemma checkpoint_survives :
  (match run_pow 22 initFastB with
   | Some s => (witness_threshold <=? config_count s)%N
   | None => false end) = true.
Proof. vm_check_eq. Qed.
Theorem blank_moves : exists n c, c0 -[ tm ]->> n / c /\ (N.to_nat witness_threshold <= n)%nat.
Proof. exact (checkpoint_bound 22 witness_threshold checkpoint_survives). Qed.
Print Assumptions blank_moves.
