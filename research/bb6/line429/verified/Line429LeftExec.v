(** Executable complete leftward sweep on eventually-zero half-tapes. *)
From BusyCoq Require Import Individual62 Line429Engine Line429LeftLanguage Line429LeftOutput.
From Coq Require Import List Arith Lia.
Import ListNotations Bell429 LeftLanguage429 LeftOutput429.
Open Scope list_scope.
Open Scope sym_scope.
Module LeftExec429.
Definition word := list sym.
Definition pop (w:word) := match w with []=>(S0,[]) | b::v=>(b,v) end.
Lemma pop_spec w b v : pop w=(b,v) -> w *> 0inf=b >> (v *> 0inf) /\
 length v<=length w /\ (b=S1 -> length v<length w).
Proof. destruct w as [|c t]; cbn; intro E; inversion E;subst; repeat split;
 try solve [apply const_unfold|reflexivity|lia|discriminate]. Qed.

(** Pop the remaining ones of a positive run and its terminating zero. *)
Fixpoint ones (w:word) : nat*word :=
 match w with []=>(O,[]) | S0::v=>(O,v) | S1::v=>let '(n,t):=ones v in (S n,t) end.
Lemma ones_spec w n x : ones w=(n,x) ->
 w *> 0inf=copies S1 n (S0 >> (x *> 0inf)) /\ length x<=length w.
Proof. revert n x. induction w as [|[|] w IH]; intros n x E; cbn [ones] in E.
 - inversion E;subst;split;[apply const_unfold|lia].
 - inversion E;subst;split;[reflexivity|cbn;lia].
 - destruct (ones w) as [k t] eqn:J. inversion E;subst.
   destruct (IH _ _ eq_refl) as [G L]. cbn;rewrite G;split;[reflexivity|lia].
Qed.

Definition tailword (m:mode) : word := match m with ML=>[1;1;1]|MJ=>[1;1;0;0] end.
Inductive action := halt | turn (y v:word) | scan (m:mode) (y v:word).
Definition zeros_row m (w:word) :=
 let '(b,v):=pop w in
 match b with
 | S0=>let '(c,x):=pop v in match c with S0=>turn x (tailword m)|S1=>halt end
 | S1=>let '(n,t):=ones v in let '(c,x):=pop t in
       let z:=repeat S0 n ++ tailword m in
       match c with S0=>scan MJ x z |S1=>turn x (S0::z) end
 end.
Definition row m w :=
 let '(a,t):=pop w in match m,a with
 | MJ,S1=>scan ML t [1;0;0]
 | MJ,S0=>zeros_row MJ t
 | ML,_=>let '(b,x):=pop t in
    match a,b with
    | S0,S0=>zeros_row ML x | S0,S1=>scan ML x [1;1]
    | S1,S0=>scan MJ x [] | S1,S1=>turn x [0] end end.

Definition evidence m s a := match a with
 | halt=>emit m s stopped | turn x v=>emit m s (returned (x *> 0inf) v)
 | scan m' x v=>forall o, emit m' (x *> 0inf) o -> emit m s (feed o v) end.
Definition decreases n a := match a with scan _ x _=>length x<n|_=>True end.
Definition leading (m:mode) (s:side) :=
 match m with ML=>S0 >> S0 >> s | MJ=>S0 >> s end.
Lemma zeros_correct m w : evidence m (leading m (w *> 0inf)) (zeros_row m w) /\
 decreases (length w) (zeros_row m w).
Proof.
 unfold zeros_row. destruct (pop w) as [b v] eqn:P. destruct (pop_spec _ _ _ P) as [W [V Pv]].
 rewrite W. destruct b.
 - destruct (pop v) as [c x] eqn:J. destruct (pop_spec _ _ _ J) as [U _]. rewrite U.
   destruct m,c;split; cbn [evidence leading decreases tailword]; try exact I; constructor.
 - destruct (ones v) as [n t] eqn:J. destruct (ones_spec _ _ _ J) as [U T].
   destruct (pop t) as [c x] eqn:K. destruct (pop_spec _ _ _ K) as [Y [X _]]. rewrite U,Y.
   specialize (Pv eq_refl). destruct m,c;split; cbn [evidence leading decreases tailword];
     try solve [lia|exact I|constructor|intros;constructor;assumption].
Qed.
Lemma decreases_le n k a : n<=k -> decreases n a -> decreases k a.
Proof. destruct a; cbn [decreases]; tauto || lia. Qed.
Lemma feed_nil o : feed o [] = o. Proof. destruct o; cbn [feed]; rewrite ?app_nil_r;reflexivity. Qed.
Lemma row_correct m w : evidence m (w *> 0inf) (row m w) /\ decreases (length w) (row m w).
Proof.
 unfold row. destruct (pop w) as [a t] eqn:J. destruct (pop_spec _ _ _ J) as [W [T Pt]]. rewrite W.
 destruct m.
 - destruct (pop t) as [b x] eqn:P. destruct (pop_spec _ _ _ P) as [V [X Px]]. rewrite V.
   destruct a,b.
   + destruct (zeros_correct ML x) as [E D]. split; [exact E|eapply decreases_le; [|exact D]; lia].
   + split; [intros; constructor;assumption|cbn [decreases];specialize (Px eq_refl);lia].
   + split; [intros o H; rewrite feed_nil; constructor;assumption|cbn [decreases];specialize (Pt eq_refl);lia].
   + split; [constructor|exact I].
 - destruct a.
   + destruct (zeros_correct MJ t) as [E D]. split; [exact E|exact (decreases_le _ _ _ T D)].
   + split;[intros;constructor;assumption|exact (Pt eq_refl)].
Qed.
Definition answer := option (word*word).
Definition add_output (z:answer) (v:word) : answer :=
 match z with None=>None | Some (y,p)=>Some (y,p++v) end.
Fixpoint iterate (n:nat) (m:mode) (w:word) : answer :=
 match n with O=>None |S k=>match row m w with
 | halt=>None | turn y v=>Some (y,v) | scan m' x v=>add_output (iterate k m' x) v end end.
Definition left_words m w := iterate (S (length w)) m w.
Definition lift (z:answer) := match z with None=>stopped|Some (y,v)=>returned (y *> 0inf) v end.
Lemma lift_app z v : lift (add_output z v)=feed (lift z) v.
Proof. destruct z as [[x t]|];reflexivity. Qed.
Lemma iterate_spec n m w : length w<n -> emit m (w *> 0inf) (lift (iterate n m w)).
Proof.
 revert m w; induction n;intros m w L;[lia|]. cbn [iterate]. destruct (row_correct m w) as [E D].
 destruct (row m w) as [|x v|m' x v]; try exact E. rewrite lift_app. apply E, IHn;cbn [decreases] in D;lia.
Qed.
Theorem left_words_spec m w : match left_words m w with
 | None => emit m (w *> 0inf) stopped
 | Some (y,v)=>emit m (w *> 0inf) (returned (y *> 0inf) v) end.
Proof. pose proof (iterate_spec (S (length w)) m w ltac:(lia)) as H.
 change (emit m (w *> 0inf) (lift (left_words m w))) in H.
 destruct (left_words m w) as [[y v]|];exact H.
Qed.
End LeftExec429.
Print Assumptions LeftExec429.left_words_spec.
