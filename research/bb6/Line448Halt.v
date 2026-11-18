From BusyCoq Require Import Individual62 Line448Engine.
Require Import Line448Sweeps.
From Coq Require Import List.
Import ListNotations.

Module E := Line448Engine.H155900.

(* The shared T4 engine uses a reflected tape. Its C is this machine's A. *)
Definition rename448 (q : Q) : Q :=
  match q with
  | A => C | B => D | C => A | D => B | E => E | F => F
  end.

Lemma table448 : Perm (flip E.src_tm) line448 rename448.
Proof.
  split.
  - intros q b H. destruct q, b; cbv in H |- *; try discriminate; reflexivity.
  - intros q b b' d q' H. destruct q, b; cbv in H |- *; inversion H; subst; reflexivity.
Qed.

Definition start448 : E.FastState :=
  E.MkFastState [] (E.MkRTape [] [] [] []) (E.RAW C R).

Definition stopped448 (s : option E.FastState) : bool :=
  match s with None => true | Some _ => false end.

(* The search found 427055 successful calls before the first None.
   The power-of-two evaluator stops as soon as a call returns None. *)
Lemma certificate448 : stopped448 (E.run_pow 19 start448) = true.
Proof. vm_check_eq. Qed.

Theorem line448_halts : halts line448 c0.
Proof.
  pose proof (E.run_pow_spec 19 start448) as H.
  pose proof certificate448 as finished.
  destruct (E.run_pow 19 start448); [discriminate |].
  change (halts E.src_tm (C;; tape0)) in H.
  apply flip_halts in H.
  change (flip_conf (C;; tape0)) with (C;; tape0) in H.
  exact (perm_halts _ _ _ _ _ table448 H).
Qed.

Print Assumptions line448_halts.
