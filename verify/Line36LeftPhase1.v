From Coq Require Import List Bool Arith ZArith Lia.
From BusyCoq Require Import Line36Left Line36LeftStep Line36LeftPotential Line36LeftCheck.
Import ListNotations L36Left L36LeftStep L36LeftCheck L36LeftGroups L36LeftPotential.
Lemma group1_0_false_false : check_group 1 0 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_0_false_true : check_group 1 0 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_0_true_false : check_group 1 0 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_0_true_true : check_group 1 0 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_1_false_false : check_group 1 1 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_1_false_true : check_group 1 1 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_1_true_false : check_group 1 1 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_1_true_true : check_group 1 1 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_2_false_false : check_group 1 2 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_2_false_true : check_group 1 2 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_2_true_false : check_group 1 2 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_2_true_true : check_group 1 2 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_3_false_false : check_group 1 3 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_3_false_true : check_group 1 3 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_3_true_false : check_group 1 3 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_3_true_true : check_group 1 3 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_4_false_false : check_group 1 4 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_4_false_true : check_group 1 4 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_4_true_false : check_group 1 4 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_4_true_true : check_group 1 4 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_5_false_false : check_group 1 5 false false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_5_false_true : check_group 1 5 false true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_5_true_false : check_group 1 5 true false = true.
Proof. vm_compute. reflexivity. Qed.
Lemma group1_5_true_true : check_group 1 5 true true = true.
Proof. vm_compute. reflexivity. Qed.
Lemma certified_phase1 : check_phase 1 = true.
Proof. cbn [check_phase seq forallb check_kind].
  rewrite group1_0_false_false.
  rewrite group1_0_false_true.
  rewrite group1_0_true_false.
  rewrite group1_0_true_true.
  rewrite group1_1_false_false.
  rewrite group1_1_false_true.
  rewrite group1_1_true_false.
  rewrite group1_1_true_true.
  rewrite group1_2_false_false.
  rewrite group1_2_false_true.
  rewrite group1_2_true_false.
  rewrite group1_2_true_true.
  rewrite group1_3_false_false.
  rewrite group1_3_false_true.
  rewrite group1_3_true_false.
  rewrite group1_3_true_true.
  rewrite group1_4_false_false.
  rewrite group1_4_false_true.
  rewrite group1_4_true_false.
  rewrite group1_4_true_true.
  rewrite group1_5_false_false.
  rewrite group1_5_false_true.
  rewrite group1_5_true_false.
  rewrite group1_5_true_true.
  reflexivity. Qed.
