(** A global criterion from the two independent tests at a shaped return to A. *)
From BusyCoq Require Import Individual62 Line429Engine Line429Progress
  Line429RightSweep Line429LeftLanguage Line429Returns Line429Criterion Line429Round Line429Gate Line429LeftDFA.
From Coq Require Import List Arith Lia Wf_nat.
Import ListNotations Bell429 LeftLanguage429.
Open Scope list_scope.
Open Scope sym_scope.
Module GateBlank429.
Definition checkpoint (u w:list Sym) :=
  AR (0 >> (u *> 0inf)) (1 >> (w *> 0inf)).

Lemma startup : (B;;tape0) -[src_tm]->> 4 / checkpoint [] [1;1].
Proof. unfold checkpoint, AR; do 4 (eapply multistep_S; [prove_step|simpl_tape]).
  replace (0 >> 0inf) with (0inf:side) by apply const_unfold. apply multistep_0.
Qed.
Lemma supported_checkpoint u w : Criterion429.supported (checkpoint u w).
Proof. split; [exists (S0::u)|exists w];reflexivity. Qed.

Section ByGate.
Variable gate : list Sym->bool.
Hypothesis parse : forall w u, exists l r t, (4<=t)%nat /\
  checkpoint u w -[src_tm]->> t / CfgL l r /\
  forall o, accepts MJ (u *> 0inf) o -> accepts ML l (Round429.choose (gate w) o).

Definition flagged u w := gate w=true /\ accepts MJ (u *> 0inf) Stop.
Definition hits c := exists u w, c -[src_tm]->* checkpoint u w /\ flagged u w.

Lemma turn_return u w l r t : (4<=t)%nat -> checkpoint u w -[src_tm]->> t / CfgL l r ->
 accepts ML l Turn -> exists u' w', checkpoint u w -[src_tm]->+ checkpoint u' w'.
Proof.
 intros time M parser. destruct (accepts_turn_shape _ _ parser r) as [y [v P]].
 pose proof (before_path _ _ P) as path.
 assert (forward:checkpoint u w -[src_tm]->+ AR (0 >> y) (1 >> v)).
 { eapply progress_evstep_trans; [|exact path]. destruct t; [lia|]. exact (multistep_progress _ _ _ _ M). }
 destruct (Criterion429.path_support _ _ _ (progress_evstep _ _ _ forward) (supported_checkpoint _ _)) as [left right].
 apply Returns429.finite_rest in left. destruct left as [u' L]. destruct right as [w' R].
 unfold checkpoint. exists u',w'. rewrite <-L, <-R. exact forward.
Qed.
Lemma alternative u w : flagged u w \/ exists u' w', checkpoint u w -[src_tm]->+ checkpoint u' w'.
Proof.
 destruct (parse w u) as [l [r [t [time [M test]]]]].
 destruct (accepts_total u MJ) as [o P]. specialize (test _ P).
 destruct (gate w) eqn:G, o; cbn [Round429.choose] in test; try (right; eapply turn_return;eassumption).
 left; split; assumption.
Qed.
Lemma flag_halts u w : flagged u w -> halts src_tm (checkpoint u w).
Proof.
 intros [G O]. destruct (parse w u) as [l [r [t [time [M P]]]]].
 specialize (P _ O). rewrite G in P. destruct (accepts_first_shape _ _ _ P r) as [z [B stop]].
 eapply evstep_halts; [apply (without_counter _ _ _ _ M)|].
 eapply evstep_halts; [exact (before_path _ _ B)|apply halted_halts;exact stop].
Qed.
Lemma from_checkpoint n u w : halts_in src_tm (checkpoint u w) n -> hits (checkpoint u w).
Proof.
 revert u w; induction n using lt_wf_ind; intros u w stopN.
 destruct (alternative u w) as [flag|[v [r P]]].
 - exists u,w; split; [constructor|exact flag].
 - destruct (progress_multistep _ _ _ P) as [k M].
   pose proof (within_halt _ _ _ _ _ stopN M) as L.
   pose proof (preceeds_halt _ _ _ _ _ stopN M L) as smaller.
   destruct (H (n-S k)%nat ltac:(lia) v r smaller) as [a [b [reach yes]]].
   exists a,b;split; [eapply evstep_trans; [apply progress_evstep,P|exact reach]|exact yes].
Qed.
Theorem generic_blank : halts tm c0 <-> hits (B;;tape0).
Proof.
 split.
 - intros H. apply flip_halts in H. change (flip_conf c0) with (A;;tape0) in H.
   pose proof (perm_halts _ _ _ A tape0 Progress429.perm_back H) as init.
   pose proof (without_counter _ _ _ _ startup) as P. apply (proj1 (halts_evstep_iff _ _ _ P)) in init.
   destruct init as [n Hn]. destruct (from_checkpoint _ _ _ Hn) as [u [w [R F]]].
   exists u,w;split; [eapply evstep_trans;eassumption|exact F].
 - intros [u [w [R F]]]. apply halts_iso. eapply evstep_halts; [exact R|apply flag_halts,F].
Qed.
End ByGate.
(** Equivalent finite words may differ by trailing zeroes. The gate reads
    the same value for every finite representation of a half-tape. *)
Lemma gate_blank w : forall h a b, w *> 0inf=0inf -> Gate429.gate h a b w=a.
Proof.
 induction w as [|x w IH]; intros h a b E; [reflexivity|].
 pose proof (f_equal (@Streams.hd _) E) as X. pose proof (f_equal (@Streams.tl _) E) as R.
 change (w *> 0inf=0inf) in R. destruct x; [|discriminate X].
 destruct h; cbn [Gate429.gate]; first [reflexivity|apply IH;exact R].
Qed.
Lemma gate_extensional w v : forall h a b, w *> 0inf=v *> 0inf ->
 Gate429.gate h a b w=Gate429.gate h a b v.
Proof.
 revert v. induction w as [|x w IH]; intros [|y v] h a b E; [reflexivity| | |].
 - symmetry. apply gate_blank. symmetry;exact E.
 - apply gate_blank;exact E.
 - pose proof (f_equal (@Streams.hd _) E) as X. change (x=y) in X. subst y.
   pose proof (f_equal (@Streams.tl _) E) as R. change (w *> 0inf=v *> 0inf) in R.
   destruct h,x; cbn [Gate429.gate]; first [reflexivity|apply IH;exact R].
Qed.

(** Both words are finite, represented nearest symbol first. *)
Theorem blank_halt_iff_gate : halts tm c0 <->
  exists u w, (B;;tape0) -[src_tm]->* checkpoint u w /\
    Gate429.gate Gate429.fresh true true w=true /\ accepts MJ (u *> 0inf) Stop.
Proof. exact (generic_blank _ Gate429.filtered_parse). Qed.
(** Both halves can be checked by evaluating a finite word. *)
Theorem blank_halt_iff_two_tests : halts tm c0 <->
  exists u w, (B;;tape0) -[src_tm]->* checkpoint u w /\
    Gate429.gate Gate429.fresh true true w=true /\ LeftDFA429.decide MJ u=Stop.
Proof.
  rewrite blank_halt_iff_gate. split; intros [u [w [R [G H]]]]; exists u,w.
  - split; [exact R|]. split; [exact G|apply LeftDFA429.decide_exact; exact H].
  - split; [exact R|]. split; [exact G|apply LeftDFA429.decide_exact; exact H].
Qed.
End GateBlank429.
Print Assumptions GateBlank429.blank_halt_iff_two_tests.
