(** The literal two-state, five-symbol machine on row 36, including a direct
    computation from the blank tape to the checkpoint at epoch 331. *)
From Coq Require Import Lists.List Strings.String Strings.Ascii PArith.BinPos.
From BusyCoq Require Export Compute.
Import ListNotations.

Inductive state := A | B.
Inductive sym := S0 | S1 | S2 | S3 | S4.

Module BB25 <: Ctx.
  Definition Q := state.
  Definition Sym := sym.
  Definition q0 := A.
  Definition q1 := B.
  Definition s0 := S0.
  Definition s1 := S1.
  Lemma q0_neq_q1 : q0 <> q1.
  Proof. discriminate. Qed.
  Lemma s0_neq_s1 : s0 <> s1.
  Proof. discriminate. Qed.
  Definition eqb_q (x y : Q) : {x = y} + {x <> y}.
  Proof. decide equality. Defined.
  Definition eqb_sym (x y : Sym) : {x = y} + {x <> y}.
  Proof. decide equality. Defined.
  Definition all_qs := [A; B].
  Lemma all_qs_spec : forall q, In q all_qs.
  Proof. destruct q; simpl; auto. Qed.
  Definition all_syms := [S0; S1; S2; S3; S4].
  Lemma all_syms_spec : forall s, In s all_syms.
  Proof. destruct s; simpl; auto 6. Qed.
End BB25.

Module M36 := Compute BB25.
Export M36.

(** 1RB2LA1LA4RA2LA_0LA3RB3LB2RB--- *)
Definition line36 : TM :=
  fun qs => match qs with
  | (A,S0) => Some (S1,R,B) | (A,S1) => Some (S2,L,A)
  | (A,S2) => Some (S1,L,A) | (A,S3) => Some (S4,R,A)
  | (A,S4) => Some (S2,L,A) | (B,S0) => Some (S0,L,A)
  | (B,S1) => Some (S3,R,B) | (B,S2) => Some (S3,L,B)
  | (B,S3) => Some (S2,R,B) | (B,S4) => None
  end.

Definition data_symbol (b : bool) : sym := if b then S1 else S2.
Definition finite_checkpoint (w : list bool) : Q * ctape :=
  (A, ([], S0, map data_symbol w)).
Definition checkpoint (w : list bool) : Q * tape := lift (finite_checkpoint w).

Lemma checkpoint_nil : checkpoint [] = c0.
Proof. reflexivity. Qed.

(** A positive binary counter computes literal transitions with logarithmic
    stack depth. Each individual transition is the repository's [cstep]. *)
Definition finite36 := (Q * ctape)%type.
Definition advance_one (o : option finite36) : option finite36 :=
  match o with
  | None => None
  | Some c => match cstep line36 c with
              | inleft (exist _ d _) => Some d
              | inright _ => None
              end
  end.

Fixpoint literal_run (n : positive) (o : option finite36) : option finite36 :=
  match n with
  | xH => advance_one o
  | xO p => literal_run p (literal_run p o)
  | xI p => advance_one (literal_run p (literal_run p o))
  end.

Fixpoint literal_count (n : positive) : nat :=
  match n with
  | xH => 1
  | xO p => literal_count p + literal_count p
  | xI p => (literal_count p + literal_count p) + 1
  end.

Definition records_steps (n : nat) (x y : option finite36) : Prop :=
  match x, y with
  | Some c, Some d => multistep line36 n (lift c) (lift d)
  | None, Some _ => False
  | _, None => True
  end.

Lemma advance_one_records : forall x, records_steps 1 x (advance_one x).
Proof.
  intros [c|]; [unfold advance_one | exact I].
  destruct (cstep line36 c) as [[d H]|H]; cbn [records_steps].
  - eapply multistep_S; [exact H | apply multistep_0].
  - exact I.
Qed.

Lemma records_compose : forall n m x y z,
  records_steps n x y -> records_steps m y z -> records_steps (n+m) x z.
Proof.
  intros n m [a|] [b|] [c|]; cbn [records_steps]; intuition eauto using multistep_trans.
Qed.

Lemma literal_run_records : forall n o,
  records_steps (literal_count n) o (literal_run n o).
Proof.
  induction n as [p IH|p IH|]; intro o; cbn [literal_count literal_run].
  - eapply records_compose; [| apply advance_one_records].
    eapply records_compose; apply IH.
  - eapply records_compose; apply IH.
  - apply advance_one_records.
Qed.

(** The seed is a finite literal with 1 for an opening and 2 for a closing.
    The equality below checks it against the elementary machine, independently
    of any sweep recurrence or choice of tile grammar. *)
Fixpoint read_digits (s : string) : list bool :=
  match s with
  | EmptyString => []
  | String c rest => Ascii.eqb c "1"%char :: read_digits rest
  end.

Definition line36_blank_seed : list bool :=
  read_digits "222111112211121111111112121112111211121112121211111112111221212121212121111121111121212111111111111111211121211211111211111111111112121211121212111212111111111112111112121111121211121111111112121121112111211121212111111121112212121212121211111211111212211111111111111121112121121111121111111111111212121112121211121211111111111211111212111112121112111111111212111211121112111212121111111211121212121212121211111211111212121111111111111112111212111211111211111111111112121211121212111212111111111112111112121111121211121111111112121112121212121212111211111211111211111212121111111112121112111111121212121112111111121111111112111112121111111112111212111111111111111211111211111212212111111111121112111111121211111112121212111111121212111112111111111111111111121211121212121112111112121211111212121111111212111212121112121112121211121212121211121211111211111211111112121112121212112121212121111111221112111111111111121112111111121111121112121211111211121211121112111112121112121212121211121211121112111211121111121212121211111221211112111"%string.

Definition seed_finite_result : finite36 :=
  (A, ([], S0, (map data_symbol line36_blank_seed ++ [S0])%list)).

Lemma line36_seed_length : List.length line36_blank_seed = 1035.
Proof. vm_compute. reflexivity. Qed.

Lemma line36_seed_computation :
  literal_run 612729%positive (Some starting) = Some seed_finite_result.
Proof. vm_compute. reflexivity. Qed.

Lemma lift_side_trailing_blank : forall xs,
  lift_side (xs ++ [S0])%list = lift_side xs.
Proof.
  induction xs as [|x xs IH]; cbn [List.app lift_side].
  - symmetry. apply const_unfold.
  - now rewrite IH.
Qed.

Lemma line36_seed_lifts : lift seed_finite_result = checkpoint line36_blank_seed.
Proof.
  unfold seed_finite_result, checkpoint, finite_checkpoint, lift, lift_tape.
  now rewrite lift_side_trailing_blank.
Qed.

Theorem line36_seed_steps :
  multistep line36 (literal_count 612729%positive) c0 (checkpoint line36_blank_seed).
Proof.
  pose proof (literal_run_records 612729%positive (Some starting)) as H.
  rewrite line36_seed_computation in H.
  change (multistep line36 (literal_count 612729%positive)
            (lift starting) (lift seed_finite_result)) in H.
  now rewrite lift_starting, line36_seed_lifts in H.
Qed.

Theorem line36_seed_reached : evstep line36 c0 (checkpoint line36_blank_seed).
Proof. eapply without_counter; exact line36_seed_steps. Qed.

Theorem line36_checkpoint_nonhalting (P : list bool -> Prop) :
  P line36_blank_seed ->
  (forall w, P w -> exists v, progress line36 (checkpoint w) (checkpoint v) /\ P v) ->
  ~ halts line36 c0.
Proof.
  intros seed closed.
  eapply multistep_nonhalt; [exact line36_seed_reached|].
  eapply progress_nonhalt_cond; [exact closed | exact seed].
Qed.
