From Coq Require Import List.
From BusyCoq Require Import Line36Cap Line36CapStream.
Import ListNotations.

(** The witness is data only. This Boolean equality checks every admitted
    cap and both possibilities allowed for its exterior cell. *)
Lemma all_fast_cap_states : cap_fast_certificate = true.
Proof. Time vm_compute. reflexivity. Qed.

Definition cap_all_states_checked : check_tree 50 [] cap_root = true :=
  eq_trans fast_root_exact all_fast_cap_states.

Theorem cap_checked_condition w v :
  length w = 50 -> cap_value w = Some v -> cap_condition w v = true.
Proof. exact (cap_condition_from_root cap_all_states_checked w v). Qed.
Print Assumptions cap_checked_condition.
