(* Natural-number versions of five existing CubicCap certificates.
   The tables, recurrence definitions, and proof tactics are the existing
   authors' work. Rechecking just the nat model avoids the Uint63 assumptions
   in their optimized evaluation wrappers. This does not certify a native run.
   AI-assisted by Codex. *)
From BusyCoq Require Import Individual62 CubicCap ES_v2 ES_v3.
From Coq Require Import String NArith.

Module CubicModels.
Record Model := {
  table : string;
  shape : nat -> nat -> nat -> Q*tape;
  initial : nat*nat*nat;
  bounce : nat*nat*nat -> nat*nat*nat;
  calc : nat*nat*nat -> option (nat*nat*nat)
}.
Definition machine m := TM_from_str (table m).
Definition cfg m := config (shape m).
Definition NatWF m :=
  (c0 -[machine m]->* cfg m (initial m)) /\
  (forall x, cfg m x -[machine m]->* cfg m (bounce m x)) /\
  (forall x, match calc m x with
    | Some y => cfg m x -[machine m]->* cfg m y
    | None => halts (machine m) (cfg m x)
    end).

Ltac from_certificate H :=
  let T := type of H in
  match T with Cert_WF ?s (cert1 ?S ?x ?b _ ?c _) =>
    exact (Build_Model s S x b c)
  end.
Definition entry35 : Model. Proof. from_certificate WF17. Defined.
Definition entry269 : Model. Proof. from_certificate WF32. Defined.
Definition entry494 : Model. Proof. from_certificate WF33. Defined.
Definition entry138 : Model. Proof. from_certificate WF35. Defined.
Definition entry409 : Model. Proof. from_certificate WF36. Defined.

(* This repeats the nat portions of solve_Cert_WF. The optimized N' program
   and its equivalence proof are deliberately absent from the proposition. *)
Ltac solve_nat_model :=
  unfold NatWF, machine, cfg; cbn [table shape initial bounce calc];
  split; [unfold config; solve_rule|]; split;
  [ intros [[a b] c]; eapply CapIncs; unfold config; solve_rule
  | intros [[a b] c]; unfold config; solve_calc_step_spec ].

Lemma entry35_wf : NatWF entry35.
Proof. unfold entry35; solve_nat_model. Qed.
Lemma entry269_wf : NatWF entry269.
Proof. unfold entry269; solve_nat_model. Qed.
Lemma entry494_wf : NatWF entry494.
Proof. unfold entry494; solve_nat_model. Qed.
Lemma entry138_wf : NatWF entry138.
Proof. unfold entry138; solve_nat_model. Qed.
Lemma entry409_wf : NatWF entry409.
Proof. unfold entry409; solve_nat_model. Qed.

Definition run m T := calc_steps (bounce m) (calc m) T (initial m).
Theorem completed_run m : NatWF m -> forall T,
  match run m T with
  | Some x => c0 -[machine m]->* cfg m x
  | None => halts (machine m) c0
  end.
Proof.
  intros [HI [HB HC]] T.
  pose proof (calc_steps_spec (machine m) (shape m) (bounce m) (calc m)
    HB HC T (initial m)) as H.
  unfold run; destruct (calc_steps (bounce m) (calc m) T (initial m));
    [eapply evstep_trans; eauto|eapply halts_evstep; eauto].
Qed.

(* The four other inputs use reflected versions of the certificate tables.
   Check both maps directly, without functional extensionality. *)
Lemma reflected_equiv a b :
  Perm (flip a) b (fun q => q) -> Perm (flip b) a (fun q => q) ->
  (halts a c0 <-> halts b c0).
Proof.
  intros HF HB; split; intro H.
  - exact (perm_halts _ _ (fun q => q) A tape0 HF (flip_halts a c0 H)).
  - exact (perm_halts _ _ (fun q => q) A tape0 HB (flip_halts b c0 H)).
Qed.
Ltac check_reflection := apply reflected_equiv;
  (split;
   [ intros [] [] H; unfold flip in H; cbn in H; try discriminate; reflexivity
   | intros [] [] s' d q' H; unfold flip in H; cbn in H; inversion H; reflexivity ]).
Lemma entry269_blank :
  halts (TM_from_str "1RB1RD_0LC1RA_1RA1LC_0RB1LE_1RF0LD_---0RE") c0 <->
  halts (machine entry269) c0.
Proof. check_reflection. Qed.
Lemma entry494_blank :
  halts (TM_from_str "1RB1LE_1RC1RA_0LD1RB_1LE1LD_1RF0LA_---0RE") c0 <->
  halts (machine entry494) c0.
Proof. check_reflection. Qed.
Lemma entry138_blank :
  halts (TM_from_str "1RB1RD_0LC1RA_1LA1LC_1RA1LE_1RF0LD_---0RE") c0 <->
  halts (machine entry138) c0.
Proof. check_reflection. Qed.
Lemma entry409_blank :
  halts (TM_from_str "1RB1RD_0LC1RA_0RA1LC_1RA1LE_1RF0LD_---0RE") c0 <->
  halts (machine entry409) c0.
Proof. check_reflection. Qed.

Print Assumptions entry35_wf.
Print Assumptions entry269_wf.
Print Assumptions entry494_wf.
Print Assumptions entry138_wf.
Print Assumptions entry409_wf.
Print Assumptions completed_run.
Print Assumptions entry269_blank.
Print Assumptions entry494_blank.
Print Assumptions entry138_blank.
Print Assumptions entry409_blank.
End CubicModels.
