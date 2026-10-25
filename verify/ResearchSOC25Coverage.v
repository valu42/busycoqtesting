(* Explicit links from the supplied 623 ordering to existing SOC25 models.
   The model equivalences are BusyCoq's existing results, not new resolutions.
   No dependency on the unmerged SOC25_Iter PR is introduced here.
   AI-assisted by Codex. *)
From BusyCoq Require Import Individual62 Eqv_WordPairs ES_v2 ES_v3.
From Coq Require Import String.

Module SOC25Coverage.
Definition entry535 := Eval compute in
  TM_from_str "1RB1LA_1LC1RD_1LA0LC_1RE0RB_1RF0LE_1RA---".
Definition entry572 := Eval compute in
  TM_from_str "1RB1LA_1LC1RD_1LA0LC_1RE0RB_1RF1RC_1RA---".
Definition entry573 := Eval compute in
  TM_from_str "1RB1LD_1RC0RB_1LA1RC_1LE0LA_1LF---_1LC---".

Theorem entry535_eqv : halts entry535 c0 <-> halts TM93.tm c0.
Proof. symmetry; exact TM93.eqv. Qed.
Theorem entry572_eqv : halts entry572 c0 <-> halts TM97.tm c0.
Proof. symmetry; exact TM97.eqv. Qed.

Lemma reflected_forward : Perm (flip entry573) TM90.tm' (fun q => q).
Proof.
  split.
  - intros [] [] H; unfold flip in H; cbn in H; try discriminate; reflexivity.
  - intros [] [] s' d q' H; unfold flip in H; cbn in H; inversion H; reflexivity.
Qed.
Lemma reflected_backward : Perm (flip TM90.tm') entry573 (fun q => q).
Proof.
  split.
  - intros [] [] H; unfold flip in H; cbn in H; try discriminate; reflexivity.
  - intros [] [] s' d q' H; unfold flip in H; cbn in H; inversion H; reflexivity.
Qed.
Theorem entry573_eqv : halts entry573 c0 <-> halts TM90.tm c0.
Proof.
  rewrite TM90.eqv. split; intro H.
  - exact (perm_halts _ _ (fun q => q) A tape0 reflected_forward
      (flip_halts entry573 c0 H)).
  - exact (perm_halts _ _ (fun q => q) A tape0 reflected_backward
      (flip_halts TM90.tm' c0 H)).
Qed.
Print Assumptions entry535_eqv.
Print Assumptions entry572_eqv.
Print Assumptions entry573_eqv.
End SOC25Coverage.
