From BusyCoq Require Import Individual62 Line429Engine Line429Frontier Line429Progress.
From BusyCoq Require Import Line429Escape.
From Coq Require Import List NArith PeanoNat.
Import ListNotations Bell429 Escape429.
Module Watch429.
Definition label (s:FastState) : Q := match fs_mode s with
 | MR=>A | ML=>B | MJ=>C | RAW q _=>q end.
Lemma label_spec s : fst (fs_denote s) = label s.
Proof. destruct s as [l rt [| | | q [|]]]; reflexivity. Qed.
Definition qeq (x y : Q) : {x=y}+{x<>y}. Proof. decide equality. Defined.
Definition literal (s:FastState) := toRawAndStep (fs_L s) (fs_R s) (fs_mode s).
Fixpoint watch (k:nat) (s:FastState) : option FastState :=
 match stepFast s with
 | None => None
 | Some t => if qeq (label s) (label t) then
    match k with O=>literal t | S n=>watch n t end else Some t
 end.
Lemma watch_spec k s : match watch k s with
 | Some t => fs_denote s -[src_tm]->+ fs_denote t
 | None => halts src_tm (fs_denote s) end.
Proof.
 revert s. induction k as [|k IH]; intro s; cbn [watch]; pose proof (stepFast_spec s) as E;
 destruct (stepFast s) as [t|]; try exact E;
 destruct (qeq (label s) (label t)) as [H|H].
 - destruct t as [l rt m]. pose proof (Progress429.literal_tick l rt m) as P.
   unfold literal; cbn [fs_L fs_R fs_mode]. destruct (toRawAndStep l rt m); [eapply evstep_progress_trans; [exact E|apply progress_base;exact P]|eapply evstep_halts; [exact E|apply halted_halts;exact P]].
 - apply evstep_progress; [exact E|]. intro C. apply H. rewrite <-!label_spec, C. reflexivity.
 - specialize (IH t). destruct (watch k t); [eapply evstep_progress_trans|eapply evstep_halts]; eassumption.
 - apply evstep_progress; [exact E|]. intro C. apply H. rewrite <-!label_spec, C. reflexivity.
Qed.
Lemma equiv_initial : halts tm c0 <-> halts src_tm (fs_denote initFastB).
Proof.
 rewrite initFastB_denote. split; [|exact halts_iso]. intro H.
 apply flip_halts in H. change (flip_conf c0) with (A;;tape0) in H.
 exact (perm_halts _ _ _ A tape0 Progress429.perm_back H).
Qed.
Theorem complete k : halts tm c0 <-> iter_halts (watch k) initFastB.
Proof. rewrite equiv_initial. eapply (halts_iff src_tm FastState initFastB (watch k) fs_denote (fun _=>True)).
 - intros s _. pose proof (watch_spec k s) as P. destruct (watch k s); auto.
 - exact I.
Qed.
Lemma Dchanges s t : label s = D -> stepFast s = Some t -> label t <> D.
Proof.
 destruct s as [l rt [| | |q d]]; cbn [label fs_mode]; try discriminate.
 intros ->. destruct d; cbn [stepFast fs_L fs_R fs_mode stepRaw]; unfold rawStep;
 [destruct (runs_pop l) as [[] u]|destruct (popBitRTape (normRTape rt)) as [[] u]];
 intros H; inversion H; discriminate.
Qed.
Lemma risk_label s : risk s -> label s=D.
Proof. destruct s as [l rt [| | |q d]]; try destruct q; try destruct d; cbn [risk label fs_mode]; tauto. Qed.
Lemma nonD_literal s : label s <> D -> on_result (literal s).
Proof.
 destruct s as [l rt [| | |q d]]; intro H; unfold literal; cbn [fs_L fs_R fs_mode];
 [apply fromMR|apply fromML|apply fromMJ|apply raw_clean;exact H].
Qed.
Lemma literal_stop s : literal s=None <-> ishalt s.
Proof.
 destruct s as [l rt m]. pose proof (Progress429.literal_tick l rt m) as H.
 unfold literal; cbn [fs_L fs_R fs_mode]. destruct (toRawAndStep l rt m) as [t|].
 - split; [discriminate|intro P]. exfalso. exact (halted_no_step _ _ _ P H).
 - intuition.
Qed.
Definition watch_front (s:FastState) (o:option FastState) : Prop :=
  match o with Some t=>guardD t /\ (ishalt t <-> risk s) /\ ~ishalt s |None=>ishalt s end.
Lemma front_spec k s : guardD s -> watch_front s (watch k s).
Proof.
 revert s. induction k as [|k IH]; intros s G; cbn [watch]; destruct (stepFast s) as [t|] eqn:E;
 try solve [apply stop_is_halted; exact E];
 pose proof (one_call_frontier _ _ G E) as [Gt It];
 assert (Ls: ~ishalt s) by (rewrite <-stop_is_halted;congruence);
 destruct (qeq (label s) (label t)) as [H|H]; try solve [cbn [watch_front]; tauto];
 assert (Ds: label s <> D) by (intro Ds; apply (Dchanges _ _ Ds E); congruence);
 assert (Dt: label t <> D) by congruence;
 assert (Rs: ~risk s) by (intro R; apply Ds,risk_label,R);
 assert (Rt: ~risk t) by (intro R; apply Dt,risk_label,R);
 assert (Lt: ~ishalt t) by tauto.
 - pose proof (nonD_literal _ Dt) as C. destruct (literal t) as [u|] eqn:M.
   + cbn [on_result] in C. cbn [watch_front]. pose proof (clean_protected _ C). pose proof (clean_unhalted _ C). tauto.
   + exfalso. apply Lt,literal_stop,M.
 - specialize (IH t Gt). destruct (watch k t) as [u|]; cbn [watch_front] in *; tauto.
Qed.
Theorem watch_stop k s : guardD s -> (watch k s=None <-> ishalt s).
Proof. intro G. pose proof (front_spec k s G) as H. destruct (watch k s); cbn [watch_front] in H; intuition discriminate. Qed.
Fixpoint endpoint (k n:nat) : option FastState :=
 match n with O=>Some initFastB|S m=>match endpoint k m with Some s=>watch k s|None=>None end end.
Lemma endpoint_guard k n s : endpoint k n=Some s -> guardD s.
Proof. revert s. induction n; intros s E; cbn [endpoint] in E.
 - inversion E. exact initial_protected.
 - destruct (endpoint k n) as [u|] eqn:J; [|discriminate]. pose proof (front_spec k u (IHn u eq_refl)) as H. rewrite E in H; exact (proj1 H).
Qed.
Lemma reachable_halt k s : iter_halts (watch k) s -> forall n, endpoint k n=Some s ->
  exists i u, endpoint k i=Some u /\ ishalt u.
Proof. intro H. induction H as [s E|s t E H IH]; intros n N.
 - exists n,s. split; [exact N|]. apply (proj1 (watch_stop k _ (endpoint_guard _ _ _ N)));exact E.
 - apply IH with (n:=S n). cbn [endpoint]. now rewrite N.
Qed.
Lemma backwards k n s : endpoint k n=Some s -> iter_halts (watch k) s ->
  iter_halts (watch k) initFastB.
Proof.
 revert s. induction n; intros s N H; cbn [endpoint] in N.
 - inversion N;subst;exact H.
 - destruct (endpoint k n) as [u|] eqn:E; [|discriminate]. apply (IHn u eq_refl).
   eapply iter_halts_S; eassumption.
Qed.
Lemma risk_unhalted s : risk s -> ~ishalt s.
Proof.
 destruct s as [l rt [| | |q d]]; try destruct q; try destruct d; cbn [risk fs_mode]; try contradiction.
 unfold ishalt; cbn [fs_denote fs_mode fs_L fs_R halted]. destruct (Streams.hd (runs_denote l)); discriminate.
Qed.
Theorem halts_iff_risk k : halts tm c0 <-> exists n s, endpoint k n=Some s /\ risk s.
Proof.
 rewrite complete with (k:=k). split.
 - intro H. destruct (reachable_halt _ _ H O eq_refl) as [[|n] [t [M T]]].
   + inversion M; subst. vm_compute in T; discriminate.
   + cbn [endpoint] in M. destruct (endpoint k n) as [s|] eqn:E; [|discriminate].
     exists n,s. split; [exact E|]. pose proof (front_spec k s (endpoint_guard _ _ _ E)) as F.
     rewrite M in F. exact (proj1 (proj1 (proj2 F)) T).
 - intros [n [s [N R]]]. apply (backwards _ _ _ N).
   pose proof (front_spec k s (endpoint_guard _ _ _ N)) as H. destruct (watch k s) as [t|] eqn:E.
   + eapply iter_halts_S; [exact E|]. apply iter_halts_O, (watch_stop k t (proj1 H)).
     exact (proj2 (proj1 (proj2 H)) R).
   + now apply iter_halts_O.
Qed.
Lemma native_path n s t : calls n s=Some t -> fs_denote s -[src_tm]->* fs_denote t.
Proof.
 revert t. induction n; intros t H; cbn [calls] in H.
 - inversion H;constructor.
 - destruct (calls n s) as [u|] eqn:E; [|discriminate].
   pose proof (stepFast_spec u) as M. rewrite H in M.
   eapply evstep_trans; [exact (IHn u eq_refl)|exact M].
Qed.

(** Group any finite number of unmodified engine calls. Their count may vary
    without bound. A control-state change anywhere before the return certifies
    progress, even when the return itself has the initial label. *)
Theorem native_return_nonhalt (family:FastState->Prop) :
 family initFastB ->
 (forall s, family s -> exists i u j t, calls i s=Some u /\ label s<>label u /\
   calls j u=Some t /\ family t) ->
 ~halts tm c0.
Proof.
 intros S C. rewrite equiv_initial.
 apply (progress_nonhalt_cond src_tm FastState initFastB fs_denote family); [|exact S].
 intros s G. destruct (C s G) as [i [u [j [t [E [D [R F]]]]]]]. exists t. split; [|exact F].
 eapply progress_evstep_trans; [|exact (native_path _ _ _ R)].
 apply evstep_progress; [exact (native_path _ _ _ E)|].
 intro H. apply D. rewrite <-!label_spec, H. reflexivity.
Qed.
End Watch429.
Print Assumptions Watch429.halts_iff_risk.
Print Assumptions Watch429.native_return_nonhalt.
