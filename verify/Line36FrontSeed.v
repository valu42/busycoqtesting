(** The concrete seed as a frontier record consumed by the moving-cut proof. *)
From Coq Require Import List ZArith Lia.
From BusyCoq Require Import Line36Machine Line36Seed Line36Front Line36Left
  Line36LeftPotential Line36Cap Line36CapInvariant.
Import ListNotations.
Local Open Scope nat_scope.

Module L36FrontSeed.

Definition seed : front36 := Front36 0 L36Seed.choices false 0 L36Seed.tail.

Lemma exact_word : fword seed = line36_blank_seed.
Proof.
  vm_compute. reflexivity.
Qed.

Lemma valid_seed : fvalid seed.
Proof. vm_compute; repeat split; lia. Qed.

Theorem exact_front :
  length (fprefix seed) = 530 /\ length (ftail seed) = 505 /\
  L36Seed.budget (fprefix seed) (ftail seed) = 7 /\
  fstate seed = L36Left.State 0 0 true false 0 0 /\
  L36LeftPotential.value (fstate seed) = 0%Z /\
  cap_value (L36Seed.cap50 (fword seed)) = Some 5 /\
  L36CapInvariant.terminal_bit (fword seed) = 1%Z.
Proof. vm_compute; repeat split. Qed.

(** The physical blank run reaches this precise frontier. *)
Theorem reached : evstep line36 c0 (checkpoint (fword seed)).
Proof. rewrite exact_word. exact line36_seed_reached. Qed.

End L36FrontSeed.
