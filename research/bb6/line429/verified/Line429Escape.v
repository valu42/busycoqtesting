From BusyCoq Require Import Individual62 Line429Engine Line429Frontier Line429Progress.
From Coq Require Import List NArith PeanoNat.
Import ListNotations Bell429.
Open Scope sym_scope.
Module Escape429.
Definition macro (m:FMode) := match m with RAW _ _ => False | _ => True end.
Definition guardD (s:FastState) := match fs_mode s with RAW D R => Streams.hd (runs_denote (fs_L s)) = S0 | _=>True end.
Definition clean (s:FastState) := match fs_mode s with RAW F _=>False | _=>guardD s end.
Definition on_result (f:option FastState) := match f with Some t=>clean t|None=>True end.
Create HintDb escape429.
Ltac cleanlit := solve [exact I | reflexivity].
Lemma pushed_zero l : Streams.hd (runs_denote (runs_push (SW_raw [0]) 1 l)) = S0.
Proof. rewrite runs_push_spec; reflexivity. Qed.
Lemma raw_clean l rt q d : q<>D -> on_result (rawStep l rt q d).
Proof.
  intro H. destruct q; try contradiction; destruct d; unfold rawStep;
  repeat match goal with |- context [runs_pop ?x] => destruct (runs_pop x) as [[] ?] end;
  repeat match goal with |- context [popBitRTape ?x] => destruct (popBitRTape x) as [[] ?] end;
  first [exact I|apply pushed_zero].
Qed.
#[local] Hint Resolve raw_clean : escape429.
#[local] Hint Extern 1 (_ <> D) => discriminate : escape429.
Lemma fromMR l rt : on_result (toRawAndStep l rt MR).
Proof. apply raw_clean; discriminate. Qed.
Lemma fromML l rt : on_result (toRawAndStep l rt ML).
Proof. apply raw_clean; discriminate. Qed.
Lemma fromMJ l rt : on_result (toRawAndStep l rt MJ).
Proof. apply raw_clean; discriminate. Qed.
#[local] Hint Resolve fromMR fromML fromMJ : escape429.
Ltac bysyntax := first [cleanlit | solve [cbn [on_result]; eauto 2 with escape429] | solve [eauto 2 with escape429] |
  lazymatch goal with |- context [match ?x with _=>_ end] =>
    first [ let O := fresh "O" in assert (O : on_result x) by (eauto 2 with escape429; fail); destruct x; bysyntax
    | destruct x; bysyntax ] end ].
Lemma mr_D l df db r : clean (stepMR_D l df db r).
Proof. unfold stepMR_D; bysyntax. Qed.
#[local] Hint Resolve mr_D : escape429.
Lemma mr_imm l rt : on_result (stepMR_imm l rt).
Proof. unfold stepMR_imm; bysyntax. Qed.
#[local] Hint Resolve mr_imm : escape429.
Lemma mr_noimm l rt : on_result (stepMR_tailNoImm l rt).
Proof. unfold stepMR_tailNoImm; bysyntax. Qed.
#[local] Hint Resolve mr_noimm : escape429.
Lemma mr_rest l rt : on_result (stepMR_tailRest l rt).
Proof. unfold stepMR_tailRest; bysyntax. Qed.
#[local] Hint Resolve mr_rest : escape429.
Lemma mr_tail l rt : on_result (stepMR_tail l rt).
Proof. unfold stepMR_tail; bysyntax. Qed.
#[local] Hint Resolve mr_tail : escape429.
Lemma mr l rt : on_result (stepMR l rt).
Proof. unfold stepMR; bysyntax. Qed.
#[local] Hint Resolve mr : escape429.
Definition goodLeft s := match s with SLS_cont _ _ _ _ _ _ => True | SLS_stop _ _ _ _ _ m => macro m end.
Lemma one_left p b l df db r : goodLeft (sweepLeftOne p b l df db r).
Proof. unfold sweepLeftOne; bysyntax. Qed.
Lemma pow_left k s : goodLeft s -> goodLeft (sweepLeftPow k s).
Proof.
  revert s. induction k as [|k IH]; intros [p b l df db r|p l df db r m] good; cbn [sweepLeftPow]; try exact good; try apply one_left.
  apply IH, IH; exact good.
Qed.
Definition tuple_good (tuple : bool*Runs*Digits*Digits*Runs*FMode) := macro (snd tuple).
Lemma run_left k p b l df db r : tuple_good (sweepLeftRun k p b l df db r).
Proof.
  pose proof (pow_left k (SLS_cont p b l df db r) I) as H. unfold sweepLeftRun.
  destruct (sweepLeftPow k (SLS_cont p b l df db r)) as [p' [] l' df' db' r' |p' l' df' db' r' m]; first [exact I|exact H].
Qed.
Lemma finish_left p l df db r m : macro m -> on_result (sweepLeftFinish p l df db r m).
Proof. intros H; unfold sweepLeftFinish; destruct m; try contradiction; bysyntax. Qed.
#[local] Hint Resolve finish_left : escape429.
Lemma run_finish k p b l df db r : on_result
  (let '(a,v,x,y,t,m) := sweepLeftRun k p b l df db r in sweepLeftFinish a v x y t m).
Proof. pose proof (run_left k p b l df db r) as H.
  destruct (sweepLeftRun k p b l df db r) as [[[[[a v] x] y] t] m]. exact (finish_left a v x y t m H).
Qed.
Lemma super_body k b l rt : on_result (sweepLeftSuperBody k b l rt).
Proof. unfold sweepLeftSuperBody.
 set (rt1:=match r_raw rt with []=>rt|_::_=>flushAllToTail rt end).
 destruct (r_tail rt1); [|apply run_finish].
 destruct (sweepLeftBlank l false b (d_front rt1) (d_back rt1)) as [[[[p l1] df] db] j].
 destruct l1 as [|[w n] tl]; [destruct j;apply finish_left;exact I|].
 destruct w; first [apply run_finish|destruct j;apply finish_left;exact I].
Qed.
#[local] Hint Resolve super_body : escape429.
Lemma super b l rt : on_result (sweepLeftSuper b l rt).
Proof. unfold sweepLeftSuper; bysyntax. Qed.
#[local] Hint Resolve super : escape429.
Lemma stepML_raw_clean l rt : on_result (stepML_raw l rt).
Proof. unfold stepML_raw; bysyntax. Qed.
#[local] Hint Resolve stepML_raw_clean : escape429.
Lemma stepML_col_clean l rt : on_result (stepML_col l rt).
Proof. unfold stepML_col; bysyntax. Qed.
#[local] Hint Resolve stepML_col_clean : escape429.
Lemma stepML_afterZero1_clean l rt : on_result (stepML_afterZero1 l rt).
Proof. unfold stepML_afterZero1; bysyntax. Qed.
#[local] Hint Resolve stepML_afterZero1_clean : escape429.
Lemma stepML_tailRest_clean l rt : on_result (stepML_tailRest l rt).
Proof. unfold stepML_tailRest; bysyntax. Qed.
#[local] Hint Resolve stepML_tailRest_clean : escape429.
Lemma stepML_tail_clean l rt : on_result (stepML_tail l rt).
Proof. unfold stepML_tail; bysyntax. Qed.
#[local] Hint Resolve stepML_tail_clean : escape429.
Lemma stepML_clean l rt : on_result (stepML l rt).
Proof. unfold stepML; bysyntax. Qed.
#[local] Hint Resolve stepML_clean : escape429.
Lemma stepMJ_turn_clean l rt : on_result (stepMJ_turn l rt).
Proof. unfold stepMJ_turn; bysyntax. Qed.
#[local] Hint Resolve stepMJ_turn_clean : escape429.
Lemma stepMJ_afterZero_clean l rt : on_result (stepMJ_afterZero l rt).
Proof. unfold stepMJ_afterZero; bysyntax. Qed.
#[local] Hint Resolve stepMJ_afterZero_clean : escape429.
Lemma stepMJ_clean l rt : on_result (stepMJ l rt).
Proof. unfold stepMJ; bysyntax. Qed.
#[local] Hint Resolve stepMJ_clean : escape429.
Lemma stepRawA0Scan_clean l rt : on_result (stepRawA0Scan l rt).
Proof. unfold stepRawA0Scan; bysyntax. Qed.
#[local] Hint Resolve stepRawA0Scan_clean : escape429.
Lemma ordinary_clean l rt q d : q<>D -> on_result (stepRaw l rt q d).
Proof. intros H; destruct q,d; try contradiction; cbn [stepRaw]; bysyntax. Qed.
Lemma clean_protected s : clean s -> guardD s.
Proof. destruct s as [l rt [| | |q d]]; try exact (fun H=>H); destruct q,d; cbn [clean guardD fs_mode]; tauto. Qed.
Lemma nonD s : (forall d, fs_mode s <> RAW D d) -> on_result (stepFast s).
Proof.
  destruct s as [l rt [| | |q d]]; intros H; cbn [stepFast fs_mode fs_L fs_R]; try apply mr; try apply stepML_clean; try apply stepMJ_clean.
  apply ordinary_clean. intros ->. exact (H d eq_refl).
Qed.
Definition risk (s:FastState) : Prop :=
  match fs_mode s with
  | RAW D L => Streams.hd (runs_denote (fs_L s))=S0 /\ Streams.hd (Streams.tl (runs_denote (fs_L s)))=S1
  | _ => False end.
Definition ishalt s := halted src_tm (fs_denote s).
Lemma clean_unhalted s : clean s -> ~ishalt s.
Proof. destruct s as [l rt [| | |q d]]; unfold clean,ishalt; cbn [fs_mode fs_denote fs_L fs_R];
  try (destruct q,d); cbn [halted CfgR CfgL CfgJ]; intros H P;
  repeat match type of P with context [Streams.hd ?x] => destruct (Streams.hd x) eqn:? end; discriminate || contradiction.
Qed.
Lemma D_out l rt d t : guardD (MkFastState l rt (RAW D d)) ->
  rawStep l (normRTape rt) D d = Some t ->
  guardD t /\ (ishalt t <-> risk (MkFastState l rt (RAW D d))).
Proof.
  destruct d; unfold rawStep.
  - pose proof (runs_pop_spec l) as H.
    destruct (runs_pop l) as [[] u] eqn:E; cbn [fst snd] in H;
    intros _ P; inversion P; subst t; split; [exact I| |exact I|];
    unfold risk,ishalt; cbn [fs_mode fs_L fs_denote fs_R halted]; rewrite H; cbn [Streams.hd Streams.tl];
    destruct (Streams.hd (runs_denote u)); cbv [src_tm halted]; intuition discriminate.
  - destruct (popBitRTape (normRTape rt)) as [[] u] eqn:E; intros G P; inversion P; subst t; split; [exact I| |exact I|];
    unfold guardD in G; cbn [fs_mode fs_L] in G; unfold ishalt,risk;
    cbn [fs_denote fs_mode fs_L fs_R halted]; rewrite G; cbn [src_tm]; intuition discriminate.
Qed.
Theorem one_call_frontier s t : guardD s -> stepFast s = Some t ->
  guardD t /\ (ishalt t <-> risk s).
Proof.
  intros G P. destruct s as [l rt [| | |q d]];
  try (destruct q); try (apply (D_out l rt d t G); exact P);
  lazymatch goal with |- guardD ?t /\ (ishalt ?t <-> risk ?s) =>
    assert (C : clean t) by (pose proof (nonD s ltac:(intros []; discriminate)) as O; rewrite P in O; exact O);
    split; [apply clean_protected; exact C|unfold risk; cbn [fs_mode]; pose proof (clean_unhalted t C); tauto] end.
Qed.
Lemma initial_protected : guardD initFastB. Proof. exact I. Qed.
Fixpoint calls (n:nat) (s:FastState) := match n with O=>Some s|S k=>
  match calls k s with Some t=>stepFast t|None=>None end end.
Lemma all_protected n t : calls n initFastB = Some t -> guardD t.
Proof.
 revert t. induction n; intros t H; cbn [calls] in H.
 - inversion H; exact initial_protected.
 - destruct (calls n initFastB) as [u|] eqn:E; [|discriminate]. exact (proj1 (one_call_frontier _ _ (IHn _ eq_refl) H)).
Qed.
Theorem exact_predecessor n s t : calls n initFastB = Some s -> stepFast s = Some t ->
  (ishalt t <-> risk s).
Proof. intros H K. exact (proj2 (one_call_frontier _ _ (all_protected _ _ H) K)). Qed.
Lemma physical_terminal s : Frontier429.terminal s = true <-> ishalt s.
Proof.
 destruct s as [l rt [| | |q d]]; unfold Frontier429.terminal,ishalt; cbn [fs_mode fs_L fs_R fs_denote];
 try (destruct q); try (destruct d); cbn [halted CfgR CfgL CfgJ];
 try solve [first [destruct (Streams.hd (runs_denote l))|idtac]; first [destruct (Streams.hd (rt_denote rt))|idtac]; intuition discriminate].
 - pose proof (runs_pop_spec l) as P. destruct (runs_pop l) as [[] u]; cbn [fst snd] in *; rewrite P; cbn [Streams.hd]; intuition discriminate.
 - pose proof (popBitRTape_spec (normRTape rt)) as P. rewrite normRTape_spec in P.
   destruct (popBitRTape (normRTape rt)) as [[] u]; cbn [fst snd] in *; rewrite P; cbn [Streams.hd]; intuition discriminate.
Qed.
Lemma stop_is_halted s : stepFast s = None <-> ishalt s.
Proof. rewrite <-physical_terminal, <-(Frontier429.exact_stop s). destruct (stepFast s); simpl; intuition discriminate. Qed.
Theorem native_stop_predecessor n s t : calls n initFastB = Some s -> stepFast s = Some t ->
  (stepFast t = None <-> risk s).
Proof. intros E H. rewrite stop_is_halted. exact (exact_predecessor _ _ _ E H). Qed.
End Escape429.
Print Assumptions Escape429.native_stop_predecessor.
