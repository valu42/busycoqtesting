(** Even matching the individual gate results does not permit exchanging the two tapes. *)
From BusyCoq Require Import Individual62 Line429Engine Line429ShapePrefix Line429RightSweep
  Line429LeftLanguage Line429LeftDFA Line429Gate Line429GateBlank Line429GateSplice.
From Coq Require Import List.
Import ListNotations Bell429 ShapePrefix429 GateBlank429 LeftLanguage429.
Open Scope sym_scope.
Module MatchingGates429.
Fixpoint run n s :=
  match n with O => Some s | S k => match advance s with None => None | Some v => run k v end end.
Lemma run_sound n : forall s t, run n s = Some t -> decode s -[src_tm]->> n / decode t.
Proof.
  induction n; intros s t R; cbn in R.
  - inversion R; constructor.
  - destruct (advance s) as [v|] eqn:E; [|discriminate].
    eapply multistep_S; [apply literal,E|eapply IHn,R].
Qed.
Definition sample : snapshot :=
  Eval vm_compute in (match run 13671 blank with Some c=>c | None=>blank end).
Lemma reached : (B;;tape0) -[src_tm]->> 13671 / decode sample.
Proof. change (decode blank -[src_tm]->> 13671 / decode sample).
  apply run_sound. vm_compute; reflexivity. Qed.

Definition u := rest (west sample).
Definition w := east sample.
Theorem source : (B;;tape0) -[src_tm]->> 13671 / checkpoint u w.
Proof. exact reached. Qed.
Definition hybrid := mk A (S0::u) S1 GateSplice429.w.
Definition terminal := Eval vm_compute in
  (match run 107 hybrid with Some c=>c | None=>blank end).
Theorem hybrid_halts : halts_in src_tm (checkpoint u GateSplice429.w) 107.
Proof. exists (decode terminal); split; [apply (run_sound 107 hybrid); vm_compute; reflexivity|reflexivity]. Qed.
Definition results (x z:list Sym) := (LeftDFA429.decide MJ x, Gate429.gate Gate429.fresh true true z).
Theorem same_results :
  results u w = (Turn,false) /\ results [] GateSplice429.w = (Turn,false).
Proof. vm_compute; auto. Qed.

Theorem results_do_not_separate
  (P H : outcome*bool -> list Sym -> Prop) :
  (forall x z, (B;;tape0) -[src_tm]->* checkpoint x z -> P (results x z) x /\ H (results x z) z) ->
  (forall x z, P (results x z) x -> H (results x z) z -> ~halts src_tm (checkpoint x z)) -> False.
Proof.
  intros cover safe. destruct same_results as [E F].
  destruct (cover _ _ (without_counter _ _ _ _ source)) as [Pu _].
  destruct (cover _ _ (without_counter _ _ _ _ GateSplice429.source_39)) as [_ Hw].
  rewrite E in Pu; rewrite F in Hw.
  assert (K : results u GateSplice429.w = (Turn,false)) by (vm_compute; reflexivity).
  specialize (safe u GateSplice429.w). rewrite K in safe. apply (safe Pu Hw).
  exists 107%nat; exact hybrid_halts.
Qed.
End MatchingGates429.
Print Assumptions MatchingGates429.results_do_not_separate.
