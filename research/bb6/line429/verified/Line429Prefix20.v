(** A finite certificate for the stronger near-halt pattern, independent of
    the state of the symbol beyond the zero under the head. *)
From BusyCoq Require Import Individual62 Line429Engine.
From BusyCoq Require Import Line429Escape.
From Coq Require Import Lia PeanoNat.
Import Bell429 Escape429.
Module Prefix429.
Definition near (s:FastState) : bool :=
  match fs_mode s with RAW D L => match fst (runs_pop (fs_L s)) with S0=>true|S1=>false end
  | _=>false end.
Fixpoint audited (k:nat) (s:FastState) : option FastState :=
 match k with O=>if near s then None else stepFast s
 | S a=>match audited a s with Some t=>audited a t|None=>None end end.
Lemma append_calls i j s t : calls i s=Some t -> calls (i+j) s=calls j t.
Proof.
 intro E. induction j. now rewrite Nat.add_0_r.
 rewrite Nat.add_succ_r. cbn [calls]. now rewrite IHj.
Qed.
Lemma audit_sound k s t : audited k s=Some t ->
 calls (2^k) s=Some t /\ forall i u, i<2^k -> calls i s=Some u -> near u=false.
Proof.
 revert s t. induction k as [|k IH]; intros s t H.
 - cbn [audited] in H; destruct (near s) eqn:E; [discriminate|]. split; [exact H|].
   intros i u I J. replace i with O in J by (cbn in I; lia).
   inversion J;subst;exact E.
 - cbn [audited] in H; destruct (audited k s) as [v|] eqn:E; [|discriminate].
   destruct (IH _ _ E) as [M left]. destruct (IH _ _ H) as [P right].
   replace (2^S k) with (2^k+2^k) by (rewrite Nat.pow_succ_r' ; lia).
   split; [rewrite (append_calls _ _ _ _ M);exact P|].
   intros i u J N. destruct (Nat.lt_ge_cases i (2^k)) as [small|big]; [apply (left i);assumption|].
   replace i with (2^k + (i-2^k)) in N by lia. rewrite (append_calls _ _ _ _ M) in N.
   apply (right (i-2^k)); [lia|exact N].
Qed.
Definition fourth := match calls 4 initFastB with Some t=>t |None=>initFastB end.
Lemma four : calls 4 initFastB=Some fourth.
Proof. vm_compute;reflexivity. Qed.
Definition reported k :=
 match audited k fourth with None=>false|Some _=>true end.
Lemma certificate : reported 20=true.
Proof. vm_check_eq. Qed.
Lemma window i b : i<4+b -> 4<=i -> i-4<b. Proof. lia. Qed.
Lemma split_four i : 4<=i -> 4+(i-4)=i. Proof. lia. Qed.
Lemma beyond_three i : 4<=i -> i<>3. Proof. lia. Qed.
Lemma unique_if k i s : reported k=true -> i<4+2^k -> calls i initFastB=Some s ->
  (near s=true <-> i=3).
Proof.
 intros M B C. destruct (Nat.lt_ge_cases i 4) as [small|large].
 - destruct i as [|[|[|[|i]]]]; try lia; vm_compute in C; inversion C; subst; vm_compute; intuition discriminate.
 - unfold reported in M. destruct (audited k fourth) as [t|] eqn:E; [|discriminate].
   destruct (audit_sound _ _ _ E) as [_ safe].
   rewrite <-(split_four _ large) in C. rewrite (append_calls _ _ _ _ four) in C.
   pose proof (window _ _ B large) as L. clear B.
   rewrite (safe _ _ L C). split; [discriminate|intro J;exfalso;exact (beyond_three _ large J)].
Qed.
Theorem unique_near_1048580 i s : i<4+2^20 -> calls i initFastB=Some s -> (near s=true <-> i=3).
Proof. exact (unique_if _ _ _ certificate). Qed.
End Prefix429.
Print Assumptions Prefix429.unique_near_1048580.
