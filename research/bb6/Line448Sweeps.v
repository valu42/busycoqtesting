From BusyCoq Require Import Individual62.
From Coq Require Import String List PeanoNat Lia.
Import ListNotations.
Open Scope sym_scope.

Definition line448 : TM :=
  TM_from_str "1RB1RD_1LC0RE_1LD1LC_1RA0LB_0RD0RF_0LC---".

(* Both streams point away from the cut. The D sweep carries one known
   1 immediately to the right of the cut, outside its argument r. *)
Definition scanA (l r : side) := l {{A}}> r.
Definition scanC (l r : side) := l <{{C}} r.
Definition scanD (l r : side) := l <{{D}} 1 >> r.
Notation "x '--(' n ')-->' y" := (multistep line448 n x y) (at level 40).

Ltac local_run l r :=
  destruct l as [a l], r as [b r]; apply multistep_c_spec; reflexivity.

Lemma right_00 l r : scanA l ([0;0] *> r) --(3)--> scanC l ([1;1] *> r).
Proof. local_run l r. Qed.
Lemma right_0100 l r : scanA l ([0;1;0;0] *> r) --(4)--> scanA ([1;0;0;1] *> l) r.
Proof. local_run l r. Qed.
Lemma right_0101 l r : scanA l ([0;1;0;1] *> r) --(6)--> scanD (1 >> l) ([1;0] *> r).
Proof. local_run l r. Qed.
Lemma right_0110 l r : scanA l ([0;1;1;0] *> r) --(8)--> scanA ([1;1;1;1] *> l) r.
Proof. local_run l r. Qed.
Lemma right_0111 l r :
  scanA l ([0;1;1;1] *> r) --(3)--> (F;; ([0;0;1] *> l) {{1}} r).
Proof. local_run l r. Qed.
Lemma right_10 l r : scanA l ([1;0] *> r) --(2)--> scanA ([1;1] *> l) r.
Proof. local_run l r. Qed.
Lemma right_110 l r : scanA l ([1;1;0] *> r) --(5)--> scanA ([1;0;0] *> l) r.
Proof. local_run l r. Qed.
Lemma right_111 l r : scanA l ([1;1;1] *> r) --(7)--> scanD l ([1;0] *> r).
Proof. local_run l r. Qed.

Lemma leftC_1 l r : scanC (1 >> l) r --(1)--> scanC l (1 >> r).
Proof. local_run l r. Qed.
Lemma leftC_0 l r : scanC (0 >> l) r --(1)--> scanD l r.
Proof. local_run l r. Qed.
Lemma leftD_0 l r : scanD (0 >> l) r --(1)--> scanA (1 >> l) (1 >> r).
Proof. local_run l r. Qed.
Lemma leftD_01 l r : scanD ([1;0] *> l) r --(2)--> scanC l ([1;0;1] *> r).
Proof. local_run l r. Qed.
Lemma leftD_11 l r : scanD ([1;1] *> l) r --(6)--> scanD l ([1;0] *> r).
Proof. local_run l r. Qed.

(* Any concatenation of the four continuing input words can be crossed in
   one right sweep. The theorem retains the exact elementary step count. *)
Inductive token := Ten | OneTen | ZeroOneOneZero | ZeroOneZeroZero.
Definition input (t : token) : list Sym :=
  match t with
  | Ten => [1;0] | OneTen => [1;1;0]
  | ZeroOneOneZero => [0;1;1;0] | ZeroOneZeroZero => [0;1;0;0]
  end.
Definition output (t : token) : list Sym :=
  match t with
  | Ten => [1;1] | OneTen => [0;0;1]
  | ZeroOneOneZero => [1;1;1;1] | ZeroOneZeroZero => [1;0;0;1]
  end.
Definition cost (t : token) : nat :=
  match t with Ten => 2 | OneTen => 5 | ZeroOneOneZero => 8 | ZeroOneZeroZero => 4 end.
Fixpoint inputs (ts : list token) (r : side) : side :=
  match ts with [] => r | t :: rest => input t *> inputs rest r end.
Fixpoint outputs (ts : list token) (l : side) : side :=
  match ts with [] => l | t :: rest => outputs rest (rev (output t) *> l) end.
Fixpoint costs (ts : list token) : nat :=
  match ts with [] => 0 | t :: rest => cost t + costs rest end.

Lemma cross_one t l r :
  scanA l (input t *> r) --(cost t)--> scanA (rev (output t) *> l) r.
Proof. destruct t; apply multistep_c_spec; destruct l, r; reflexivity. Qed.

Theorem cross_right ts l r :
  scanA l (inputs ts r) --(costs ts)--> scanA (outputs ts l) r.
Proof.
  revert l; induction ts as [|t rest IH]; intros l; simpl.
  - constructor.
  - eapply multistep_trans; [apply cross_one | apply IH].
Qed.

Theorem halting_suffix ts l r :
  scanA l (inputs ts ([0;1;1;1] *> r)) --(costs ts + 3)-->
    (F;; ([0;0;1] *> outputs ts l) {{1}} r) /\
  halted line448 (F;; ([0;0;1] *> outputs ts l) {{1}} r).
Proof.
  split; [eapply multistep_trans; [apply cross_right | apply right_0111] | reflexivity].
Qed.

(* After a right sweep on 10, 110 and 0110, the D sweep can always
   cross the emitted words in the opposite direction. *)
Definition return_word (t : token) : list Sym :=
  match t with
  | Ten => [1;0] | OneTen => [1;0;1] | ZeroOneOneZero => [1;0;1;0]
  | ZeroOneZeroZero => []
  end.
Definition return_cost (t : token) : nat :=
  match t with Ten => 6 | OneTen => 3 | ZeroOneOneZero => 12 | ZeroOneZeroZero => 0 end.
Fixpoint returns (ts : list token) (r : side) : side :=
  match ts with [] => r | t :: rest => return_word t *> returns rest r end.
Fixpoint return_costs (ts : list token) : nat :=
  match ts with [] => 0 | t :: rest => return_cost t + return_costs rest end.

Lemma cross_back_one t l r : t <> ZeroOneZeroZero ->
  scanD (rev (output t) *> l) r --(return_cost t)--> scanD l (return_word t *> r).
Proof. destruct t; intro H; try contradiction; local_run l r. Qed.

Theorem cross_back ts l r : Forall (fun t => t <> ZeroOneZeroZero) ts ->
  scanD (outputs ts l) r --(return_costs ts)--> scanD l (returns ts r).
Proof.
  intros H; revert l r. induction H as [|t rest Ht Hr IH]; intros l r; simpl.
  - constructor.
  - rewrite Nat.add_comm. eapply multistep_trans; [apply IH | apply cross_back_one, Ht].
Qed.
