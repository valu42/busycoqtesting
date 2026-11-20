(** Exactly which compressed configurations can report a halt. *)
From BusyCoq Require Import Individual62 Line429Engine.
Import Bell429.
Module Frontier429.
Definition live (v:option FastState) := exists s, v = Some s.
Create HintDb live429.
Ltac split_live := first [solve [eexists; reflexivity] | solve [eauto 2 with live429] |
  lazymatch goal with |- context [match ?x with _ => _ end] => destruct x; split_live end].
Lemma raw_live l rt q d : q <> F -> live (rawStep l rt q d).
Proof.
  intros H; destruct q; try contradiction; destruct d; unfold rawStep;
  repeat match goal with |- context [runs_pop ?x] => destruct (runs_pop x) as [[] ?] end;
  repeat match goal with |- context [popBitRTape ?x] => destruct (popBitRTape x) as [[] ?] end;
  eexists; reflexivity.
Qed.
#[local] Hint Resolve raw_live : live429.
#[local] Hint Extern 1 (_ <> F) => discriminate : live429.
Lemma fallMR l rt : live (toRawAndStep l rt MR).
Proof. apply raw_live; discriminate. Qed.
Lemma fallML l rt : live (toRawAndStep l rt ML).
Proof. apply raw_live; discriminate. Qed.
Lemma fallMJ l rt : live (toRawAndStep l rt MJ).
Proof. apply raw_live; discriminate. Qed.
#[local] Hint Resolve fallMR fallML fallMJ : live429.
Lemma mr_tail l rt : live (stepMR_tail l rt).
Proof. unfold stepMR_tail; split_live. Qed.
#[local] Hint Resolve mr_tail : live429.
Lemma mr l rt : live (stepMR l rt).
Proof. unfold stepMR; split_live. Qed.
Lemma ml_col l rt : live (stepML_col l rt).
Proof. unfold stepML_col; split_live. Qed.
#[local] Hint Resolve ml_col : live429.
Lemma ml_zero l rt : live (stepML_afterZero1 l rt).
Proof. unfold stepML_afterZero1; split_live. Qed.
#[local] Hint Resolve ml_zero : live429.
Lemma ml_rest l rt : live (stepML_tailRest l rt).
Proof. unfold stepML_tailRest; split_live. Qed.
#[local] Hint Resolve ml_rest : live429.
Lemma ml_tail l rt : live (stepML_tail l rt).
Proof. unfold stepML_tail; split_live. Qed.
#[local] Hint Resolve ml_tail : live429.
Lemma ml l rt : live (stepML l rt).
Proof. unfold stepML; split_live. Qed.
Lemma mj_turn l rt : live (stepMJ_turn l rt).
Proof. unfold stepMJ_turn; split_live. Qed.
#[local] Hint Resolve mj_turn : live429.
Lemma mj_zero l rt : live (stepMJ_afterZero l rt).
Proof. unfold stepMJ_afterZero; split_live. Qed.
#[local] Hint Resolve mj_zero : live429.
Lemma mj l rt : live (stepMJ l rt).
Proof. unfold stepMJ; split_live. Qed.
Lemma a_scan l rt : live (stepRawA0Scan l rt).
Proof. unfold stepRawA0Scan; split_live. Qed.
#[local] Hint Resolve a_scan : live429.
Lemma ordinary l rt q d : q <> F -> live (stepRaw l rt q d).
Proof. intro H; destruct q,d; try contradiction; cbn [stepRaw]; split_live. Qed.
Definition terminal (s:FastState) : bool :=
  match fs_mode s with
  | RAW F d => let b := match d with L => fst (runs_pop (fs_L s)) | R => fst (popBitRTape (normRTape (fs_R s))) end in
    match b with S0=>false | S1=>true end
  | _ => false end.
Theorem exact_stop s : is_none (stepFast s) = terminal s.
Proof.
  destruct s as [l rt m]. destruct m as [| | |q d]; cbn [stepFast terminal fs_L fs_R fs_mode].
  - destruct (mr l (normRTape rt)) as [t ->]; reflexivity.
  - destruct (ml l (normRTape rt)) as [t ->]; reflexivity.
  - destruct (mj l (normRTape rt)) as [t ->]; reflexivity.
  - destruct q; try (lazymatch goal with |- is_none (stepRaw _ _ ?a _) = _ => destruct (ordinary l (normRTape rt) a d ltac:(discriminate)) as [t ->]; reflexivity end).
    destruct d; cbn [stepRaw]; unfold rawStep; [destruct (runs_pop l) as [[] u]|destruct (popBitRTape (normRTape rt)) as [[] t]]; reflexivity.
Qed.
End Frontier429.
Print Assumptions Frontier429.exact_stop.
