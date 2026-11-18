From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Left Line36LeftStep Line36LeftPotential Line36LeftCheck.
Import ListNotations L36Left L36LeftStep L36LeftCheck L36LeftGroups L36LeftPotential.
Lemma group0_0_false_false : check_group 0 0 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_0_false_true : check_group 0 0 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_0_true_false : check_group 0 0 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_0_true_true : check_group 0 0 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_1_false_false : check_group 0 1 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_1_false_true : check_group 0 1 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_1_true_false : check_group 0 1 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_1_true_true : check_group 0 1 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_2_false_false : check_group 0 2 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_2_false_true : check_group 0 2 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_2_true_false : check_group 0 2 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_2_true_true : check_group 0 2 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_3_false_false : check_group 0 3 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_3_false_true : check_group 0 3 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_3_true_false : check_group 0 3 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_3_true_true : check_group 0 3 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_4_false_false : check_group 0 4 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_4_false_true : check_group 0 4 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_4_true_false : check_group 0 4 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_4_true_true : check_group 0 4 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_5_false_false : check_group 0 5 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_5_false_true : check_group 0 5 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_5_true_false : check_group 0 5 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group0_5_true_true : check_group 0 5 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma certified_phase0 : check_phase 0 = true.
Proof. cbn [check_phase seq forallb check_kind].
  rewrite group0_0_false_false.
  rewrite group0_0_false_true.
  rewrite group0_0_true_false.
  rewrite group0_0_true_true.
  rewrite group0_1_false_false.
  rewrite group0_1_false_true.
  rewrite group0_1_true_false.
  rewrite group0_1_true_true.
  rewrite group0_2_false_false.
  rewrite group0_2_false_true.
  rewrite group0_2_true_false.
  rewrite group0_2_true_true.
  rewrite group0_3_false_false.
  rewrite group0_3_false_true.
  rewrite group0_3_true_false.
  rewrite group0_3_true_true.
  rewrite group0_4_false_false.
  rewrite group0_4_false_true.
  rewrite group0_4_true_false.
  rewrite group0_4_true_true.
  rewrite group0_5_false_false.
  rewrite group0_5_false_true.
  rewrite group0_5_true_false.
  rewrite group0_5_true_true.
  reflexivity. Qed.
